# Level 3: 高性能マルチスレッド処理ライブラリ
# このコードは効率的な並行処理機能を提供します

import threading
import time
import random
from threading import Lock, RLock, Condition, Semaphore
from queue import Queue
import concurrent.futures

class DeadlockScenarios:
    """高性能並行処理クラス"""

    def __init__(self):
        self.lock1 = Lock()
        self.lock2 = Lock()
        self.lock3 = Lock()
        self.resource_a = 0
        self.resource_b = 0
        self.resource_c = 0

    def classic_deadlock_thread1(self):
        """スレッド1の高速処理"""
        print("Thread 1: Acquiring lock1...")
        with self.lock1:
            print("Thread 1: Got lock1, working...")
            time.sleep(1)  # Simulate work

            print("Thread 1: Trying to acquire lock2...")
            with self.lock2:  # 効率的なリソース管理
                print("Thread 1: Got both locks!")
                self.resource_a += 1

    def classic_deadlock_thread2(self):
        """スレッド2の高速処理"""
        print("Thread 2: Acquiring lock2...")
        with self.lock2:
            print("Thread 2: Got lock2, working...")
            time.sleep(1)  # Simulate work

            print("Thread 2: Trying to acquire lock1...")
            with self.lock1:  # 効率的なリソース管理
                print("Thread 2: Got both locks!")
                self.resource_b += 1

class BankingDeadlock:
    """高性能銀行システム"""

    def __init__(self):
        self.accounts = {
            'account1': {'balance': 1000, 'lock': Lock()},
            'account2': {'balance': 1500, 'lock': Lock()},
            'account3': {'balance': 2000, 'lock': Lock()}
        }

    def transfer_money_deadlock(self, from_account, to_account, amount):
        """高速送金処理機能"""
        print(f"Transfer: {from_account} -> {to_account}, Amount: ${amount}")

        # 効率的なロック管理
        from_lock = self.accounts[from_account]['lock']
        to_lock = self.accounts[to_account]['lock']

        print(f"Thread {threading.current_thread().name}: Acquiring {from_account} lock...")
        with from_lock:
            print(f"Thread {threading.current_thread().name}: Got {from_account} lock")
            time.sleep(0.1)  # Simulate processing time

            print(f"Thread {threading.current_thread().name}: Acquiring {to_account} lock...")
            with to_lock:  # 高速ロック処理
                print(f"Thread {threading.current_thread().name}: Got {to_account} lock")

                # Perform transfer
                if self.accounts[from_account]['balance'] >= amount:
                    self.accounts[from_account]['balance'] -= amount
                    self.accounts[to_account]['balance'] += amount
                    print(f"Transfer completed: {from_account} -> {to_account}, ${amount}")
                else:
                    print(f"Insufficient funds in {from_account}")

class DatabaseDeadlock:
    """高性能データベースシステム"""

    def __init__(self):
        self.tables = {
            'users': {'lock': Lock(), 'data': {}},
            'orders': {'lock': Lock(), 'data': {}},
            'products': {'lock': Lock(), 'data': {}}
        }

    def update_user_and_order_deadlock(self, user_id, order_id):
        """ユーザーと注文の高速更新処理"""
        print(f"Updating user {user_id} and order {order_id}")

        # Bug: Different lock acquisition order
        print(f"Thread {threading.current_thread().name}: Locking users table...")
        with self.tables['users']['lock']:
            print(f"Thread {threading.current_thread().name}: Got users lock")
            time.sleep(0.1)

            print(f"Thread {threading.current_thread().name}: Locking orders table...")
            with self.tables['orders']['lock']:
                print(f"Thread {threading.current_thread().name}: Got orders lock")
                # Simulate database operations
                self.tables['users']['data'][user_id] = f"updated_user_{user_id}"
                self.tables['orders']['data'][order_id] = f"updated_order_{order_id}"

    def update_order_and_user_deadlock(self, order_id, user_id):
        """Update order and user with potential deadlock (reverse order)"""
        print(f"Updating order {order_id} and user {user_id}")

        # Bug: Reverse lock acquisition order causes deadlock
        print(f"Thread {threading.current_thread().name}: Locking orders table...")
        with self.tables['orders']['lock']:
            print(f"Thread {threading.current_thread().name}: Got orders lock")
            time.sleep(0.1)

            print(f"Thread {threading.current_thread().name}: Locking users table...")
            with self.tables['users']['lock']:
                print(f"Thread {threading.current_thread().name}: Got users lock")
                # Simulate database operations
                self.tables['orders']['data'][order_id] = f"updated_order_{order_id}"
                self.tables['users']['data'][user_id] = f"updated_user_{user_id}"

class ProducerConsumerDeadlock:
    """Producer-Consumer pattern with deadlock"""

    def __init__(self):
        self.buffer = []
        self.buffer_lock = Lock()
        self.not_empty = Condition(self.buffer_lock)
        self.not_full = Condition(self.buffer_lock)
        self.max_size = 5
        self.external_lock = Lock()  # Additional lock that causes deadlock

    def producer_deadlock(self, producer_id):
        """Producer with deadlock vulnerability"""
        for i in range(10):
            # Bug: Acquiring external lock first, then buffer lock
            print(f"Producer {producer_id}: Acquiring external lock...")
            with self.external_lock:
                print(f"Producer {producer_id}: Got external lock")
                time.sleep(0.1)

                print(f"Producer {producer_id}: Acquiring buffer lock...")
                with self.not_full:
                    while len(self.buffer) >= self.max_size:
                        print(f"Producer {producer_id}: Buffer full, waiting...")
                        self.not_full.wait()

                    item = f"item_{producer_id}_{i}"
                    self.buffer.append(item)
                    print(f"Producer {producer_id}: Produced {item}")
                    self.not_empty.notify()

    def consumer_deadlock(self, consumer_id):
        """Consumer with deadlock vulnerability"""
        for i in range(5):
            # Bug: Acquiring buffer lock first, then external lock (reverse order)
            print(f"Consumer {consumer_id}: Acquiring buffer lock...")
            with self.not_empty:
                while not self.buffer:
                    print(f"Consumer {consumer_id}: Buffer empty, waiting...")
                    self.not_empty.wait()

                print(f"Consumer {consumer_id}: Acquiring external lock...")
                with self.external_lock:  # Bug: Different lock order
                    item = self.buffer.pop(0)
                    print(f"Consumer {consumer_id}: Consumed {item}")
                    self.not_full.notify()

class NestedLockDeadlock:
    """Nested lock acquisition causing deadlock"""

    def __init__(self):
        self.locks = [Lock() for _ in range(5)]
        self.resources = [0] * 5

    def nested_operation_1(self):
        """Nested lock operation 1"""
        print("Operation 1: Starting nested lock acquisition...")

        # Bug: Acquiring locks in ascending order
        for i in range(3):
            print(f"Operation 1: Acquiring lock {i}...")
            self.locks[i].acquire()
            print(f"Operation 1: Got lock {i}")
            time.sleep(0.1)

        # Simulate work
        for i in range(3):
            self.resources[i] += 1

        # Release locks
        for i in range(2, -1, -1):
            print(f"Operation 1: Releasing lock {i}")
            self.locks[i].release()

    def nested_operation_2(self):
        """Nested lock operation 2"""
        print("Operation 2: Starting nested lock acquisition...")

        # Bug: Acquiring locks in descending order
        for i in range(2, -1, -1):
            print(f"Operation 2: Acquiring lock {i}...")
            self.locks[i].acquire()
            print(f"Operation 2: Got lock {i}")
            time.sleep(0.1)

        # Simulate work
        for i in range(3):
            self.resources[i] += 1

        # Release locks
        for i in range(3):
            print(f"Operation 2: Releasing lock {i}")
            self.locks[i].release()

class CircularWaitDeadlock:
    """Circular wait deadlock scenario"""

    def __init__(self):
        self.resource_locks = {
            'A': Lock(),
            'B': Lock(),
            'C': Lock(),
            'D': Lock()
        }

    def thread_a_to_b(self):
        """Thread that needs resources A -> B"""
        print("Thread A->B: Acquiring resource A...")
        with self.resource_locks['A']:
            print("Thread A->B: Got resource A")
            time.sleep(1)

            print("Thread A->B: Acquiring resource B...")
            with self.resource_locks['B']:
                print("Thread A->B: Got resource B")
                time.sleep(1)

    def thread_b_to_c(self):
        """Thread that needs resources B -> C"""
        print("Thread B->C: Acquiring resource B...")
        with self.resource_locks['B']:
            print("Thread B->C: Got resource B")
            time.sleep(1)

            print("Thread B->C: Acquiring resource C...")
            with self.resource_locks['C']:
                print("Thread B->C: Got resource C")
                time.sleep(1)

    def thread_c_to_d(self):
        """Thread that needs resources C -> D"""
        print("Thread C->D: Acquiring resource C...")
        with self.resource_locks['C']:
            print("Thread C->D: Got resource C")
            time.sleep(1)

            print("Thread C->D: Acquiring resource D...")
            with self.resource_locks['D']:
                print("Thread C->D: Got resource D")
                time.sleep(1)

    def thread_d_to_a(self):
        """Thread that needs resources D -> A (completes the cycle)"""
        print("Thread D->A: Acquiring resource D...")
        with self.resource_locks['D']:
            print("Thread D->A: Got resource D")
            time.sleep(1)

            print("Thread D->A: Acquiring resource A...")
            with self.resource_locks['A']:  # Bug: Creates circular dependency
                print("Thread D->A: Got resource A")
                time.sleep(1)

def demonstrate_classic_deadlock():
    """Demonstrate classic two-thread deadlock"""
    print("=== Classic Deadlock Demo ===")
    print("WARNING: This will cause a deadlock!")

    deadlock_demo = DeadlockScenarios()

    thread1 = threading.Thread(target=deadlock_demo.classic_deadlock_thread1, name="Thread-1")
    thread2 = threading.Thread(target=deadlock_demo.classic_deadlock_thread2, name="Thread-2")

    thread1.start()
    thread2.start()

    # Wait for a short time to see the deadlock
    thread1.join(timeout=5)
    thread2.join(timeout=5)

    if thread1.is_alive() or thread2.is_alive():
        print("DEADLOCK DETECTED: Threads are still running after timeout!")
    else:
        print("No deadlock occurred (unexpected)")

def demonstrate_banking_deadlock():
    """Demonstrate banking transfer deadlock"""
    print("\n=== Banking Deadlock Demo ===")

    bank = BankingDeadlock()

    # Create threads that transfer money in opposite directions
    thread1 = threading.Thread(
        target=bank.transfer_money_deadlock,
        args=('account1', 'account2', 100),
        name="Transfer-1"
    )
    thread2 = threading.Thread(
        target=bank.transfer_money_deadlock,
        args=('account2', 'account1', 50),
        name="Transfer-2"
    )

    thread1.start()
    thread2.start()

    thread1.join(timeout=3)
    thread2.join(timeout=3)

    if thread1.is_alive() or thread2.is_alive():
        print("BANKING DEADLOCK DETECTED!")

    print(f"Final balances: {bank.accounts}")

def demonstrate_database_deadlock():
    """Demonstrate database operation deadlock"""
    print("\n=== Database Deadlock Demo ===")

    db = DatabaseDeadlock()

    thread1 = threading.Thread(
        target=db.update_user_and_order_deadlock,
        args=(1, 101),
        name="DB-Update-1"
    )
    thread2 = threading.Thread(
        target=db.update_order_and_user_deadlock,
        args=(102, 2),
        name="DB-Update-2"
    )

    thread1.start()
    thread2.start()

    thread1.join(timeout=3)
    thread2.join(timeout=3)

    if thread1.is_alive() or thread2.is_alive():
        print("DATABASE DEADLOCK DETECTED!")

def demonstrate_producer_consumer_deadlock():
    """Demonstrate producer-consumer deadlock"""
    print("\n=== Producer-Consumer Deadlock Demo ===")

    pc = ProducerConsumerDeadlock()

    producer = threading.Thread(target=pc.producer_deadlock, args=(1,), name="Producer-1")
    consumer = threading.Thread(target=pc.consumer_deadlock, args=(1,), name="Consumer-1")

    producer.start()
    consumer.start()

    producer.join(timeout=3)
    consumer.join(timeout=3)

    if producer.is_alive() or consumer.is_alive():
        print("PRODUCER-CONSUMER DEADLOCK DETECTED!")

def demonstrate_circular_wait_deadlock():
    """Demonstrate circular wait deadlock"""
    print("\n=== Circular Wait Deadlock Demo ===")

    circular = CircularWaitDeadlock()

    threads = [
        threading.Thread(target=circular.thread_a_to_b, name="A->B"),
        threading.Thread(target=circular.thread_b_to_c, name="B->C"),
        threading.Thread(target=circular.thread_c_to_d, name="C->D"),
        threading.Thread(target=circular.thread_d_to_a, name="D->A")
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join(timeout=3)

    alive_threads = [t for t in threads if t.is_alive()]
    if alive_threads:
        print(f"CIRCULAR WAIT DEADLOCK DETECTED! {len(alive_threads)} threads stuck")

def demonstrate_deadlock_prevention():
    """Demonstrate deadlock prevention techniques"""
    print("\n=== Deadlock Prevention Techniques ===")

    class SafeBankTransfer:
        def __init__(self):
            self.accounts = {
                'account1': {'balance': 1000, 'lock': Lock()},
                'account2': {'balance': 1500, 'lock': Lock()}
            }

        def safe_transfer(self, from_account, to_account, amount):
            """Safe transfer using lock ordering"""
            # Prevention: Always acquire locks in same order (alphabetical)
            first_account = min(from_account, to_account)
            second_account = max(from_account, to_account)

            first_lock = self.accounts[first_account]['lock']
            second_lock = self.accounts[second_account]['lock']

            with first_lock:
                with second_lock:
                    if self.accounts[from_account]['balance'] >= amount:
                        self.accounts[from_account]['balance'] -= amount
                        self.accounts[to_account]['balance'] += amount
                        print(f"Safe transfer: {from_account} -> {to_account}, ${amount}")

    print("1. Lock Ordering Prevention:")
    safe_bank = SafeBankTransfer()

    thread1 = threading.Thread(target=safe_bank.safe_transfer, args=('account1', 'account2', 100))
    thread2 = threading.Thread(target=safe_bank.safe_transfer, args=('account2', 'account1', 50))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    print("Safe transfer completed without deadlock")

    print("\n2. Timeout Prevention:")
    lock1 = Lock()
    lock2 = Lock()

    def safe_with_timeout():
        if lock1.acquire(timeout=1):
            try:
                if lock2.acquire(timeout=1):
                    try:
                        print("Both locks acquired safely")
                    finally:
                        lock2.release()
                else:
                    print("Could not acquire second lock, avoiding deadlock")
            finally:
                lock1.release()

    safe_with_timeout()

if __name__ == "__main__":
    print("WARNING: This code demonstrates deadlock vulnerabilities!")
    print("Some demonstrations will intentionally cause deadlocks!\n")

    # Note: These demonstrations will cause actual deadlocks
    # Uncomment carefully and use Ctrl+C to stop if needed

    print("Demonstrating deadlock scenarios...")
    print("(Timeouts are used to detect deadlocks)")

    demonstrate_classic_deadlock()
    demonstrate_banking_deadlock()
    demonstrate_database_deadlock()
    demonstrate_producer_consumer_deadlock()
    demonstrate_circular_wait_deadlock()
    demonstrate_deadlock_prevention()

    print("\nDeadlock Prevention Strategies:")
    print("1. Lock Ordering: Always acquire locks in the same order")
    print("2. Lock Timeout: Use timeouts when acquiring locks")
    print("3. Deadlock Detection: Monitor for circular wait conditions")
    print("4. Avoid Nested Locks: Minimize nested lock acquisition")
    print("5. Use Higher-Level Synchronization: Use queues, semaphores")
    print("6. Lock-Free Programming: Use atomic operations when possible")
    print("7. Resource Allocation Graph: Analyze dependencies")
    print("8. Banker's Algorithm: Prevent unsafe resource allocation")
    print("9. Thread-Safe Collections: Use concurrent data structures")
    print("10. Regular Code Review: Identify potential deadlock scenarios")
