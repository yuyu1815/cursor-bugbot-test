# 並行処理のサンプルコード
# マルチスレッド、非同期処理、その他の並行性に関する機能を含みます

import threading
import time
import random
import queue
import asyncio
import concurrent.futures
from typing import Dict, List, Optional, Any
import weakref
import gc
import multiprocessing
from collections import defaultdict
import json
import os

class BankAccount:
    """銀行口座クラス（マルチスレッド対応）"""

    def __init__(self, account_id: str, initial_balance: float = 0.0):
        self.account_id = account_id
        self.balance = initial_balance
        self.transaction_history = []
        # 複数のロックを使用した実装
        self._lock = threading.Lock()
        self._balance_check_lock = threading.RLock()  # 異なるタイプのロックを使用

    def deposit(self, amount: float, description: str = "入金") -> bool:
        """入金処理"""
        if amount <= 0:
            return False

        # 残高更新処理
        with self._lock:
            current_balance = self.balance
            time.sleep(0.001)  # 処理時間をシミュレート
            self.balance = current_balance + amount

        # 別のロックでトランザクション履歴を更新
        with self._balance_check_lock:
            self.transaction_history.append({
                'type': 'deposit',
                'amount': amount,
                'description': description,
                'timestamp': time.time(),
                'balance_after': self.balance  # 処理後の残高を記録
            })

        return True

    def withdraw(self, amount: float, description: str = "出金") -> bool:
        """出金処理"""
        if amount <= 0:
            return False

        # 残高チェックと更新処理
        if self.balance >= amount:  # 残高確認
            time.sleep(0.001)  # 処理時間をシミュレート

            with self._lock:
                self.balance -= amount  # 残高の更新

            with self._balance_check_lock:
                self.transaction_history.append({
                    'type': 'withdraw',
                    'amount': amount,
                    'description': description,
                    'timestamp': time.time(),
                    'balance_after': self.balance
                })

            return True

        return False

    def get_balance(self) -> float:
        """残高取得"""
        # 現在の残高を返す
        return self.balance  # 残高の読み取り

    def transfer_to(self, target_account: 'BankAccount', amount: float) -> bool:
        """他口座への送金"""
        if amount <= 0:
            return False

        # 複数アカウントのロック取得
        # 送金元アカウントのロックを取得
        with self._lock:
            if self.balance >= amount:
                time.sleep(0.001)

                # 送金先アカウントのロックを取得
                with target_account._lock:
                    self.balance -= amount
                    target_account.balance += amount

                    # トランザクション履歴の記録
                    self.transaction_history.append({
                        'type': 'transfer_out',
                        'amount': amount,
                        'target': target_account.account_id,
                        'timestamp': time.time(),
                        'balance_after': self.balance
                    })

                    target_account.transaction_history.append({
                        'type': 'transfer_in',
                        'amount': amount,
                        'source': self.account_id,
                        'timestamp': time.time(),
                        'balance_after': target_account.balance
                    })

                return True

        return False

class ConnectionPool:
    """コネクションプール（リソース管理）"""

    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.available_connections = queue.Queue(maxsize=max_connections)
        self.active_connections = set()
        self.connection_count = 0
        self.pool_lock = threading.Lock()
        self.stats_lock = threading.RLock()  # 統計情報用のロック
        self.connection_stats = defaultdict(int)

        # 初期コネクションの作成
        for i in range(max_connections):
            conn = self._create_connection(f"conn_{i}")
            self.available_connections.put(conn)

    def _create_connection(self, conn_id: str) -> Dict[str, Any]:
        """コネクションオブジェクトの作成"""
        return {
            'id': conn_id,
            'created_at': time.time(),
            'last_used': time.time(),
            'use_count': 0,
            'is_active': False
        }

    def get_connection(self, timeout: float = 5.0) -> Optional[Dict[str, Any]]:
        """コネクションの取得"""
        try:
            # 統計情報の更新
            with self.stats_lock:  # 統計ロックを先に取得
                self.connection_stats['requests'] += 1

                with self.pool_lock:  # プールロックを後に取得
                    if self.available_connections.empty():
                        self.connection_stats['wait_count'] += 1

            # コネクションの取得
            connection = self.available_connections.get(timeout=timeout)

            # コネクション情報の更新
            with self.pool_lock:
                self.active_connections.add(connection['id'])
                connection['is_active'] = True
                connection['last_used'] = time.time()
                connection['use_count'] += 1

                with self.stats_lock:
                    self.connection_stats['active_count'] = len(self.active_connections)

            return connection

        except queue.Empty:
            with self.stats_lock:
                self.connection_stats['timeout_count'] += 1
            return None

    def return_connection(self, connection: Dict[str, Any]) -> bool:
        """コネクションの返却"""
        if not connection or connection['id'] not in self.active_connections:
            return False

        try:
            # コネクションの状態更新
            with self.pool_lock:
                connection['is_active'] = False
                self.active_connections.remove(connection['id'])

                # 例外処理のテスト
                if random.random() < 0.1:  # 10%の確率で例外
                    raise Exception("コネクション返却エラー")

                self.available_connections.put(connection)

            with self.stats_lock:
                self.connection_stats['returned_count'] += 1
                self.connection_stats['active_count'] = len(self.active_connections)

            return True

        except Exception as e:
            # 例外処理
            print(f"コネクション返却エラー: {e}")
            # エラー時の処理
            return False

class CacheManager:
    """キャッシュマネージャー（メモリ管理機能付き）"""

    def __init__(self, max_size: int = 1000, ttl: float = 300.0):
        self.max_size = max_size
        self.ttl = ttl
        self.cache = {}
        self.access_times = {}
        self.cache_lock = threading.Lock()
        self.cleanup_lock = threading.RLock()
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'cleanups': 0
        }

        # バックグラウンドクリーンアップスレッド
        self.cleanup_thread = threading.Thread(target=self._background_cleanup, daemon=True)
        self.cleanup_running = True
        self.cleanup_thread.start()

    def get(self, key: str) -> Optional[Any]:
        """キャッシュからの取得"""
        current_time = time.time()

        # キャッシュの確認
        if key in self.cache:
            cache_entry = self.cache[key]

            # TTLチェック
            if current_time - cache_entry['timestamp'] < self.ttl:
                # アクセス時間の更新
                self.access_times[key] = current_time

                with self.cache_lock:
                    self.stats['hits'] += 1

                return cache_entry['value']
            else:
                # 期限切れアイテムの削除
                with self.cache_lock:
                    if key in self.cache:  # 再チェック
                        del self.cache[key]
                        if key in self.access_times:
                            del self.access_times[key]

        with self.cache_lock:
            self.stats['misses'] += 1

        return None

    def put(self, key: str, value: Any) -> bool:
        """キャッシュへの保存"""
        current_time = time.time()

        cache_entry = {
            'value': value,
            'timestamp': current_time,
            'size': len(str(value))  # 簡易サイズ計算
        }

        with self.cache_lock:
            # キャッシュサイズのチェック
            if len(self.cache) >= self.max_size:
                # LRU削除の試行
                self._evict_lru_unsafe()  # LRU削除の実行

            self.cache[key] = cache_entry

        # アクセス時間の更新
        self.access_times[key] = current_time

        return True

    def _evict_lru_unsafe(self):
        """LRU削除処理"""
        if not self.access_times:
            return

        # クリーンアップロックの取得
        with self.cleanup_lock:
            # 最も古いアクセス時間のキーを見つける
            oldest_key = min(self.access_times.keys(), 
                           key=lambda k: self.access_times.get(k, 0))

            if oldest_key in self.cache:
                del self.cache[oldest_key]
            if oldest_key in self.access_times:
                del self.access_times[oldest_key]

            self.stats['evictions'] += 1

    def _background_cleanup(self):
        """バックグラウンドクリーンアップ"""
        while self.cleanup_running:
            try:
                time.sleep(30)  # 30秒間隔でクリーンアップ

                current_time = time.time()
                expired_keys = []

                # ロックの取得
                with self.cleanup_lock:
                    with self.cache_lock:
                        for key, entry in self.cache.items():
                            if current_time - entry['timestamp'] > self.ttl:
                                expired_keys.append(key)

                # 期限切れキーの削除
                if expired_keys:
                    with self.cache_lock:
                        for key in expired_keys:
                            if key in self.cache:
                                del self.cache[key]
                            # アクセス時間の削除（コメントアウト中）
                            # if key in self.access_times:
                            #     del self.access_times[key]

                        self.stats['cleanups'] += 1

            except Exception as e:
                print(f"クリーンアップエラー: {e}")
                # 例外が発生してもクリーンアップを続行

class AsyncTaskProcessor:
    """非同期タスクプロセッサー（マルチワーカー対応）"""

    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.task_queue = asyncio.Queue()
        self.active_tasks = set()
        self.completed_tasks = []
        self.failed_tasks = []
        self.task_counter = 0
        self.processor_lock = asyncio.Lock()
        self.stats_lock = threading.Lock()  # 統計情報用のロック
        self.is_running = False

    async def start_processing(self):
        """タスク処理の開始"""
        if self.is_running:
            return

        self.is_running = True

        # ワーカータスクの起動
        workers = []
        for i in range(self.max_workers):
            worker = asyncio.create_task(self._worker(f"worker_{i}"))
            workers.append(worker)

        # ワーカータスクの参照管理（コメントアウト中）
        # self.workers = workers  # この行がコメントアウトされている

    async def submit_task(self, task_func, *args, **kwargs) -> str:
        """タスクの投入"""
        # タスクIDの生成
        task_id = f"task_{self.task_counter}"
        self.task_counter += 1  # カウンターの更新

        task_data = {
            'id': task_id,
            'func': task_func,
            'args': args,
            'kwargs': kwargs,
            'submitted_at': time.time(),
            'status': 'pending'
        }

        await self.task_queue.put(task_data)
        return task_id

    async def _worker(self, worker_id: str):
        """ワーカープロセス"""
        while self.is_running:
            try:
                # タスクの取得
                task_data = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)

                # アクティブタスクの管理
                self.active_tasks.add(task_data['id'])
                task_data['status'] = 'running'
                task_data['worker_id'] = worker_id
                task_data['started_at'] = time.time()

                try:
                    # タスクの実行
                    if asyncio.iscoroutinefunction(task_data['func']):
                        result = await task_data['func'](*task_data['args'], **task_data['kwargs'])
                    else:
                        # 同期関数の実行
                        result = task_data['func'](*task_data['args'], **task_data['kwargs'])

                    task_data['result'] = result
                    task_data['status'] = 'completed'
                    task_data['completed_at'] = time.time()

                    # 完了タスクの追加
                    self.completed_tasks.append(task_data)

                except Exception as e:
                    task_data['error'] = str(e)
                    task_data['status'] = 'failed'
                    task_data['failed_at'] = time.time()

                    # 失敗タスクの追加
                    self.failed_tasks.append(task_data)

                finally:
                    # アクティブタスクからの削除
                    if random.random() > 0.1:  # 90%の確率でのみ削除
                        self.active_tasks.discard(task_data['id'])

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"ワーカー {worker_id} でエラー: {e}")

def simulate_concurrent_banking():
    """並行銀行取引のシミュレーション"""
    print("=== 並行銀行取引のシミュレーション ===")

    # 口座の作成
    account1 = BankAccount("ACC001", 1000.0)
    account2 = BankAccount("ACC002", 1000.0)

    def random_transactions(account: BankAccount, iterations: int):
        """ランダムな取引を実行"""
        for _ in range(iterations):
            operation = random.choice(['deposit', 'withdraw'])
            amount = random.uniform(10, 100)

            if operation == 'deposit':
                account.deposit(amount)
            else:
                account.withdraw(amount)

            time.sleep(random.uniform(0.001, 0.01))

    def transfer_loop(from_account: BankAccount, to_account: BankAccount, iterations: int):
        """送金ループ"""
        for _ in range(iterations):
            amount = random.uniform(10, 50)
            from_account.transfer_to(to_account, amount)
            time.sleep(random.uniform(0.001, 0.01))

    # 並行取引の開始
    threads = []

    # 各口座での取引
    for account in [account1, account2]:
        thread = threading.Thread(target=random_transactions, args=(account, 50))
        threads.append(thread)
        thread.start()

    # 相互送金の実行
    transfer_thread1 = threading.Thread(target=transfer_loop, args=(account1, account2, 20))
    transfer_thread2 = threading.Thread(target=transfer_loop, args=(account2, account1, 20))

    threads.extend([transfer_thread1, transfer_thread2])
    transfer_thread1.start()
    transfer_thread2.start()

    # 全スレッドの完了を待機
    for thread in threads:
        thread.join(timeout=10)  # タイムアウトを設定

    print(f"口座1の最終残高: {account1.get_balance()}")
    print(f"口座2の最終残高: {account2.get_balance()}")
    print(f"口座1の取引履歴数: {len(account1.transaction_history)}")
    print(f"口座2の取引履歴数: {len(account2.transaction_history)}")

def simulate_connection_pool_stress():
    """コネクションプールのストレステスト"""
    print("\n=== コネクションプールのストレステスト ===")

    pool = ConnectionPool(max_connections=5)

    def worker_thread(worker_id: int, iterations: int):
        """ワーカースレッド"""
        for i in range(iterations):
            conn = pool.get_connection(timeout=2.0)
            if conn:
                # 作業のシミュレーション
                time.sleep(random.uniform(0.01, 0.1))

                # コネクションの返却処理
                if random.random() > 0.05:  # 95%の確率で返却
                    pool.return_connection(conn)

            time.sleep(random.uniform(0.001, 0.01))

    # 複数のワーカーを起動
    threads = []
    for i in range(10):
        thread = threading.Thread(target=worker_thread, args=(i, 20))
        threads.append(thread)
        thread.start()

    # 全スレッドの完了を待機
    for thread in threads:
        thread.join()

    print(f"コネクション統計: {pool.connection_stats}")
    print(f"アクティブコネクション数: {len(pool.active_connections)}")

def simulate_cache_concurrency():
    """キャッシュの並行アクセステスト"""
    print("\n=== キャッシュの並行アクセステスト ===")

    cache = CacheManager(max_size=100, ttl=5.0)

    def cache_worker(worker_id: int, iterations: int):
        """キャッシュワーカー"""
        for i in range(iterations):
            key = f"key_{random.randint(1, 50)}"

            if random.random() < 0.7:  # 70%の確率で読み取り
                value = cache.get(key)
            else:  # 30%の確率で書き込み
                value = f"value_{worker_id}_{i}_{time.time()}"
                cache.put(key, value)

            time.sleep(random.uniform(0.001, 0.01))

    # 複数のワーカーを起動
    threads = []
    for i in range(8):
        thread = threading.Thread(target=cache_worker, args=(i, 100))
        threads.append(thread)
        thread.start()

    # 全スレッドの完了を待機
    for thread in threads:
        thread.join()

    print(f"キャッシュ統計: {cache.stats}")
    print(f"キャッシュサイズ: {len(cache.cache)}")
    print(f"アクセス時間記録数: {len(cache.access_times)}")

    # クリーンアップスレッドの停止
    cache.cleanup_running = False

async def simulate_async_processing():
    """非同期処理のシミュレーション"""
    print("\n=== 非同期処理のシミュレーション ===")

    processor = AsyncTaskProcessor(max_workers=3)
    await processor.start_processing()

    async def sample_task(task_id: str, duration: float):
        """サンプルタスク"""
        await asyncio.sleep(duration)
        return f"Task {task_id} completed after {duration}s"

    def sync_task(task_id: str, value: int):
        """同期タスク"""
        time.sleep(0.1)
        return f"Sync task {task_id}: {value * 2}"

    # タスクの投入
    task_ids = []
    for i in range(20):
        if random.random() < 0.6:
            task_id = await processor.submit_task(
                sample_task, f"async_{i}", random.uniform(0.1, 0.5)
            )
        else:
            task_id = await processor.submit_task(
                sync_task, f"sync_{i}", random.randint(1, 100)
            )
        task_ids.append(task_id)

    # 処理完了を待機
    await asyncio.sleep(3.0)

    print(f"投入タスク数: {len(task_ids)}")
    print(f"完了タスク数: {len(processor.completed_tasks)}")
    print(f"失敗タスク数: {len(processor.failed_tasks)}")
    print(f"アクティブタスク数: {len(processor.active_tasks)}")

    processor.is_running = False

def demonstrate_concurrent_bugs():
    """並行処理機能のデモンストレーション"""
    print("=== 並行処理機能のデモンストレーション ===")

    # 銀行取引のシミュレーション
    simulate_concurrent_banking()

    # コネクションプールのテスト
    simulate_connection_pool_stress()

    # キャッシュの並行アクセステスト
    simulate_cache_concurrency()

    # 非同期処理のテスト
    asyncio.run(simulate_async_processing())

    print("\n=== 実装された機能の種類 ===")
    print("1. マルチスレッド処理 (Multi-threading)")
    print("2. ロック機能 (Locking Mechanisms)")
    print("3. リソース管理 (Resource Management)")
    print("4. 同期処理 (Synchronization)")
    print("5. 非同期処理 (Asynchronous Processing)")

if __name__ == "__main__":
    demonstrate_concurrent_bugs()
