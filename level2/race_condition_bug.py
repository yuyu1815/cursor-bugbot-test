# レベル2: 競合状態のサンプルコード
# このコードはマルチスレッド環境での競合状態を示します

import threading
import time
import random

# 競合状態を引き起こすグローバル変数
counter = 0
shared_list = []
bank_balance = 1000

def increment_counter_bug():
    """グローバルカウンターのインクリメント処理"""
    global counter

    # 非原子的操作による競合状態
    for _ in range(1000):
        # これは実際には3つの操作:
        # 1. カウンター値の読み取り
        # 2. 1を加算
        # 3. カウンターに書き戻し
        counter += 1  # ここで競合状態が発生

        # 競合状態の発生確率を高めるための小さな遅延
        time.sleep(0.0001)

def append_to_list_bug(thread_id):
    """共有リストへのアイテム追加処理"""
    global shared_list

    for i in range(100):
        # リスト操作はスレッドセーフではない
        current_length = len(shared_list)  # 読み取り操作
        time.sleep(0.001)  # 処理のシミュレーション

        # 他のスレッドがリストを変更している可能性
        shared_list.append(f"Thread-{thread_id}-Item-{i}")  # 書き込み操作

        # このチェックは競合状態により失敗する可能性
        if len(shared_list) != current_length + 1:
            print(f"Race condition detected in thread {thread_id}!")

def bank_transfer_bug(from_account, to_account, amount):
    """アカウント間の送金処理"""
    global bank_balance

    # 非原子的な読み取り-変更-書き込み操作
    if bank_balance >= amount:
        # 他のスレッドが干渉する可能性のある処理時間をシミュレート
        time.sleep(0.01)

        # 他のスレッドがbank_balanceを変更している可能性
        bank_balance -= amount
        print(f"Transferred ${amount}. New balance: ${bank_balance}")
    else:
        print(f"Insufficient funds for ${amount} transfer")

class UnsafeCounter:
    """競合状態を持つカウンタークラス"""

    def __init__(self):
        self.value = 0
        self.operations = 0

    def increment_bug(self):
        """カウンターのインクリメント処理"""
        # 複数の非原子的操作
        temp = self.value  # 読み取り
        temp += 1          # 変更
        time.sleep(0.001)  # 処理のシミュレーション（競合状態の確率を高める）
        self.value = temp  # 書き込み

        # 別の競合状態
        self.operations += 1

    def decrement_bug(self):
        """カウンターのデクリメント処理"""
        # 非原子的操作
        if self.value > 0:
            time.sleep(0.001)  # 他のスレッドがここでデクリメントする可能性
            self.value -= 1
            self.operations += 1

class SharedResource:
    """競合状態を持つ共有リソース"""

    def __init__(self):
        self.data = {}
        self.access_count = 0

    def update_data_bug(self, key, value, thread_id):
        """共有データの更新処理"""
        # 非原子的なチェック後実行
        if key not in self.data:
            time.sleep(0.01)  # 処理のシミュレーション
            # 他のスレッドがキーを追加している可能性
            self.data[key] = []

        # リスト操作はスレッドセーフではない
        self.data[key].append(f"{value}-{thread_id}")

        # 非原子的なインクリメント
        self.access_count += 1

    def get_stats_bug(self):
        """統計情報の取得処理"""
        # 複数の関連する値を非原子的に読み取り
        total_items = sum(len(v) for v in self.data.values())
        access_count = self.access_count

        # 競合状態により値が一貫しない可能性
        return {
            'total_keys': len(self.data),
            'total_items': total_items,
            'access_count': access_count
        }

def worker_thread_bug(thread_id, iterations):
    """Worker thread that causes race conditions"""
    for i in range(iterations):
        increment_counter_bug()
        append_to_list_bug(thread_id)

        # Random bank transfers
        if random.random() > 0.5:
            bank_transfer_bug("account1", "account2", random.randint(1, 50))

def demonstrate_race_conditions():
    """Demonstrate various race conditions"""
    global counter, shared_list, bank_balance

    print("=== Race Condition Demo ===")

    # Reset global variables
    counter = 0
    shared_list = []
    bank_balance = 1000

    print("1. Counter race condition:")
    threads = []
    for i in range(5):
        thread = threading.Thread(target=increment_counter_bug)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Expected counter value: 5000")
    print(f"Actual counter value: {counter}")
    print(f"Race condition occurred: {counter != 5000}")

    print("\n2. List race condition:")
    shared_list = []
    threads = []
    for i in range(3):
        thread = threading.Thread(target=append_to_list_bug, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Expected list length: 300")
    print(f"Actual list length: {len(shared_list)}")

    print("\n3. Bank transfer race condition:")
    bank_balance = 1000
    threads = []
    for i in range(10):
        thread = threading.Thread(target=bank_transfer_bug, args=("acc1", "acc2", 100))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Final bank balance: ${bank_balance}")
    print("Note: Balance might be negative due to race conditions!")

    print("\n4. Unsafe counter class:")
    unsafe_counter = UnsafeCounter()
    threads = []

    # Start increment threads
    for i in range(5):
        thread = threading.Thread(target=lambda: [unsafe_counter.increment_bug() for _ in range(100)])
        threads.append(thread)
        thread.start()

    # Start decrement threads
    for i in range(2):
        thread = threading.Thread(target=lambda: [unsafe_counter.decrement_bug() for _ in range(50)])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Counter value: {unsafe_counter.value}")
    print(f"Operations count: {unsafe_counter.operations}")

    print("\n5. Shared resource race condition:")
    resource = SharedResource()
    threads = []

    for i in range(5):
        thread = threading.Thread(
            target=lambda tid=i: [
                resource.update_data_bug(f"key{j%3}", f"value{j}", tid) 
                for j in range(20)
            ]
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    stats = resource.get_stats_bug()
    print(f"Resource stats: {stats}")

if __name__ == "__main__":
    print("WARNING: This code demonstrates race conditions.")
    print("Results may vary between runs due to timing issues.")
    print("Run multiple times to see different race condition effects.\n")

    demonstrate_race_conditions()

    print("\nNote: Race conditions are timing-dependent bugs.")
    print("They may not always occur, making them hard to debug.")
    print("Use proper synchronization (locks, semaphores) to prevent them.")
