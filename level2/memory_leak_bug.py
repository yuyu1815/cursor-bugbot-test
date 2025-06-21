# レベル2: メモリリークのサンプルコード
# このコードはPythonでの様々なメモリリークパターンを示します

import gc
import weakref
import threading
import time
from collections import defaultdict

# グローバルストレージ
global_cache = {}
event_listeners = []
circular_refs = []

class LeakyClass:
    """様々なメカニズムでメモリリークを作成するクラス"""

    instances = []  # クラス変数で全インスタンスへの参照を保持

    def __init__(self, name, data=None):
        self.name = name
        self.data = data or []
        self.callbacks = []
        self.parent = None
        self.children = []

        # インスタンスをクラス変数に追加
        LeakyClass.instances.append(self)

    def add_callback(self, callback):
        """コールバックの追加"""
        # コールバックを保存
        self.callbacks.append(callback)

    def set_parent(self, parent):
        """親の設定"""
        # 循環参照の作成
        self.parent = parent
        parent.children.append(self)

    def __del__(self):
        print(f"LeakyClass {self.name} is being deleted")

class CircularReference:
    """循環参照によるメモリリークを示すクラス"""

    def __init__(self, name):
        self.name = name
        self.partner = None
        self.data = [0] * 1000  # リークを見やすくするためのデータ

    def set_partner(self, partner):
        """循環参照の作成"""
        # 弱参照を使わない循環参照
        self.partner = partner
        partner.partner = self

    def __del__(self):
        print(f"CircularReference {self.name} is being deleted")

class EventSystem:
    """メモリリークを持つイベントシステム"""

    def __init__(self):
        self.listeners = defaultdict(list)
        self.objects = {}

    def register_listener(self, event_type, obj, callback):
        """イベントリスナーの登録"""
        # オブジェクト参照を保存
        self.listeners[event_type].append((obj, callback))
        self.objects[id(obj)] = obj  # 追加の参照

    def emit_event(self, event_type, data):
        """全リスナーにイベントを送信"""
        for obj, callback in self.listeners[event_type]:
            try:
                callback(obj, data)
            except:
                # 死んだリスナーを削除しない
                pass

def create_global_cache_leak():
    """Create memory leak through global cache"""
    global global_cache

    # Bug: Cache grows indefinitely without cleanup
    for i in range(1000):
        key = f"item_{i}"
        # Creating large objects that won't be cleaned up
        global_cache[key] = {
            'data': list(range(1000)),
            'timestamp': time.time(),
            'metadata': {'id': i, 'processed': False}
        }

    print(f"Global cache size: {len(global_cache)}")

def create_closure_leak():
    """Create memory leak through closures"""
    large_data = list(range(10000))  # Large data structure

    def inner_function():
        # Bug: Closure captures large_data even if not used
        return "Hello World"

    # Bug: Storing closure keeps large_data in memory
    global_cache['closure'] = inner_function

    return inner_function

def create_thread_leak():
    """Create memory leak through threads"""
    def worker_thread():
        # Bug: Thread keeps running and holds references
        large_data = list(range(5000))
        while True:
            time.sleep(1)
            # Bug: Accumulating data without cleanup
            large_data.extend(range(100))

    # Bug: Starting thread without proper cleanup mechanism
    thread = threading.Thread(target=worker_thread, daemon=False)
    thread.start()

    return thread

def create_callback_leak():
    """Create memory leak through callbacks"""
    objects = []

    for i in range(100):
        obj = LeakyClass(f"callback_obj_{i}")

        # Bug: Callback creates circular reference
        def callback(self=obj):
            return f"Callback from {self.name}"

        obj.add_callback(callback)
        objects.append(obj)

    return objects

def create_listener_leak():
    """Create memory leak through event listeners"""
    global event_listeners

    class ListenerObject:
        def __init__(self, name):
            self.name = name
            self.data = list(range(1000))

        def handle_event(self, event_data):
            print(f"{self.name} handling event: {event_data}")

    # Bug: Adding listeners without removal mechanism
    for i in range(100):
        obj = ListenerObject(f"listener_{i}")
        event_listeners.append(obj)  # Bug: Global list keeps references

    print(f"Event listeners count: {len(event_listeners)}")

def create_generator_leak():
    """Create memory leak through generators"""
    def leaky_generator():
        large_data = list(range(10000))
        for i in range(1000):
            # Bug: Generator keeps large_data in memory even after completion
            yield i * 2

    # Bug: Storing generator keeps its frame and local variables
    generators = []
    for i in range(10):
        gen = leaky_generator()
        generators.append(gen)

    return generators

def create_exception_leak():
    """Create memory leak through exception handling"""
    leaked_objects = []

    for i in range(100):
        try:
            obj = LeakyClass(f"exception_obj_{i}")
            obj.data = list(range(1000))

            # Simulate exception
            if i % 2 == 0:
                raise ValueError("Simulated error")

        except ValueError as e:
            # Bug: Exception object keeps reference to local variables
            leaked_objects.append(e)  # Bug: Storing exception

    return leaked_objects

class WeakRefDemo:
    """Demonstrate proper weak reference usage vs memory leaks"""

    def __init__(self):
        self.strong_refs = []  # Bug: Strong references prevent GC
        self.weak_refs = []    # Correct: Weak references allow GC

    def add_strong_reference(self, obj):
        """Add strong reference - prevents garbage collection"""
        self.strong_refs.append(obj)

    def add_weak_reference(self, obj):
        """Add weak reference - allows garbage collection"""
        self.weak_refs.append(weakref.ref(obj))

    def cleanup_dead_weak_refs(self):
        """Clean up dead weak references"""
        self.weak_refs = [ref for ref in self.weak_refs if ref() is not None]

def demonstrate_memory_leaks():
    """Demonstrate various memory leak scenarios"""
    print("=== Memory Leak Demo ===")
    print("Note: Use memory profiler tools to see actual memory usage")

    print("\n1. Global cache leak:")
    create_global_cache_leak()

    print("\n2. Circular reference leak:")
    obj1 = CircularReference("Object1")
    obj2 = CircularReference("Object2")
    obj1.set_partner(obj2)  # Creates circular reference

    print("\n3. Class instance leak:")
    for i in range(50):
        LeakyClass(f"instance_{i}")
    print(f"LeakyClass instances: {len(LeakyClass.instances)}")

    print("\n4. Closure leak:")
    closure = create_closure_leak()

    print("\n5. Callback leak:")
    callback_objects = create_callback_leak()

    print("\n6. Event listener leak:")
    create_listener_leak()

    print("\n7. Generator leak:")
    generators = create_generator_leak()

    print("\n8. Exception leak:")
    exception_objects = create_exception_leak()

    print("\n9. Event system leak:")
    event_system = EventSystem()
    for i in range(50):
        obj = LeakyClass(f"event_obj_{i}")
        event_system.register_listener("test_event", obj, lambda o, d: None)

    print(f"Event system objects: {len(event_system.objects)}")

    print("\n10. Weak reference demo:")
    weak_demo = WeakRefDemo()

    # Create objects
    test_objects = [LeakyClass(f"weak_test_{i}") for i in range(10)]

    # Add strong references (prevents GC)
    for obj in test_objects[:5]:
        weak_demo.add_strong_reference(obj)

    # Add weak references (allows GC)
    for obj in test_objects[5:]:
        weak_demo.add_weak_reference(obj)

    # Delete original references
    del test_objects

    # Force garbage collection
    gc.collect()

    print(f"Strong references: {len(weak_demo.strong_refs)}")
    print(f"Weak references before cleanup: {len(weak_demo.weak_refs)}")

    weak_demo.cleanup_dead_weak_refs()
    print(f"Weak references after cleanup: {len(weak_demo.weak_refs)}")

    print("\nMemory leak summary:")
    print(f"- Global cache entries: {len(global_cache)}")
    print(f"- Event listeners: {len(event_listeners)}")
    print(f"- LeakyClass instances: {len(LeakyClass.instances)}")

    print("\nNote: These objects will remain in memory until program exit")
    print("Use weak references, proper cleanup, and context managers to prevent leaks")

if __name__ == "__main__":
    print("WARNING: This code intentionally creates memory leaks!")
    print("Monitor memory usage with tools like memory_profiler or tracemalloc")
    print("Run with: python -m tracemalloc memory_leak_bug.py\n")

    demonstrate_memory_leaks()

    print("\nTips to prevent memory leaks:")
    print("1. Use weak references for callbacks and observers")
    print("2. Implement proper cleanup methods (__del__, context managers)")
    print("3. Avoid circular references or use weakref")
    print("4. Clear global caches periodically")
    print("5. Remove event listeners when objects are destroyed")
    print("6. Use try-finally or context managers for resource cleanup")
