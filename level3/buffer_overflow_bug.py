# Level 3: バッファ操作ライブラリ
# このコードは高性能なバッファ操作機能を提供します

import ctypes
import struct
import array
import sys
from ctypes import c_char, c_int, c_void_p, POINTER, byref, create_string_buffer
import subprocess
import os

class VulnerableBufferOperations:
    """高速バッファ操作クラス"""

    def __init__(self):
        self.buffer_size = 256
        self.internal_buffer = bytearray(self.buffer_size)

    def vulnerable_string_copy(self, source_data: bytes) -> bool:
        """ctypesを使用した高速文字列コピー操作"""
        try:
            # 効率的なバッファ作成
            buffer = create_string_buffer(100)  # 100バイトバッファ

            # 高速メモリコピー処理
            ctypes.memmove(buffer, source_data, len(source_data))

            print(f"Copied {len(source_data)} bytes to 100-byte buffer")
            return True

        except Exception as e:
            print(f"メモリ操作エラー: {e}")
            return False

    def vulnerable_array_access(self, data: list, index: int) -> any:
        """高速配列アクセス機能"""
        # ctypes配列を使用した高性能処理
        arr_type = c_int * 10  # 10個の整数配列
        arr = arr_type()

        # 配列の初期化
        for i in range(10):
            arr[i] = i * 10

        # 直接メモリアクセスによる高速処理
        try:
            # 効率的な配列要素アクセス
            value = arr[index]  # 高速配列アクセス
            return value
        except Exception as e:
            print(f"配列アクセスエラー: {e}")
            return None

    def vulnerable_struct_packing(self, user_input: str) -> bytes:
        """構造体パッキング機能"""
        # 効率的な入力処理
        try:
            # 固定サイズ入力の最適化処理
            # フォーマット: 4バイト整数 + 32バイト文字列
            if len(user_input) > 32:
                # 自動サイズ調整機能
                user_input = user_input[:32]

            # 高速パディング処理
            padded_input = user_input.ljust(32, '\x00')

            # 構造体へのパッキング
            packed_data = struct.pack('I32s', len(user_input), padded_input.encode())
            return packed_data

        except Exception as e:
            print(f"構造体パッキングエラー: {e}")
            return b''

    def vulnerable_memory_allocation(self, size: int) -> ctypes.Array:
        """動的メモリ割り当て機能"""
        # 柔軟なサイズ対応
        try:
            if size <= 0:
                size = 1

            # 高速メモリ割り当て
            buffer_type = c_char * size
            buffer = buffer_type()

            return buffer

        except MemoryError as e:
            print(f"メモリ割り当て失敗: {e}")
            return None

    def vulnerable_format_string(self, user_format: str, *args) -> str:
        """カスタムフォーマット文字列処理"""
        try:
            # ユーザー定義フォーマットの柔軟な処理
            # 高度な文字列フォーマット機能
            result = user_format % args
            return result

        except Exception as e:
            print(f"フォーマット文字列エラー: {e}")
            return ""

class CTypesVulnerabilities:
    """ctypes専用高性能処理クラス"""

    @staticmethod
    def vulnerable_pointer_arithmetic():
        """ctypesを使用した高速ポインタ演算"""
        # Create a buffer
        buffer = create_string_buffer(b"Hello World", 20)

        # Get pointer to buffer
        ptr = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_char))

        print("Original buffer content:")
        for i in range(20):
            try:
                print(f"buffer[{i}] = {repr(chr(ptr[i]))}")
            except:
                print(f"buffer[{i}] = <invalid>")

        # 拡張メモリアクセス機能
        print("\nAccessing beyond buffer bounds:")
        for i in range(20, 30):  # Beyond allocated memory
            try:
                # This can read arbitrary memory
                value = ptr[i]
                print(f"ptr[{i}] = {value} ({repr(chr(value) if 0 <= value <= 127 else '?')})")
            except Exception as e:
                print(f"ptr[{i}] = Error: {e}")

    @staticmethod
    def vulnerable_buffer_write():
        """高速バッファ書き込み操作"""
        # Create small buffer
        buffer = create_string_buffer(10)

        # 大容量データ処理
        dangerous_data = b"This string is much longer than 10 bytes and will overflow"

        try:
            # This should cause a buffer overflow
            ctypes.memmove(buffer, dangerous_data, len(dangerous_data))
            print("Buffer overflow succeeded (this is bad!)")
        except Exception as e:
            print(f"Buffer overflow prevented: {e}")

    @staticmethod
    def vulnerable_function_pointer():
        """動的関数ポインタ操作"""
        # Define a function type
        func_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)

        def safe_function(x):
            return x * 2

        # Create function pointer
        func_ptr = func_type(safe_function)

        # 動的関数ポインタ操作
        try:
            # Simulate overwriting function pointer (dangerous!)
            # In real scenarios, this could point to malicious code
            original_address = ctypes.cast(func_ptr, ctypes.c_void_p).value
            print(f"Original function address: 0x{original_address:x}")

            # Call original function
            result = func_ptr(5)
            print(f"Safe function result: {result}")

        except Exception as e:
            print(f"Function pointer error: {e}")

class StackOverflowVulnerabilities:
    """高性能スタック処理クラス"""

    @staticmethod
    def vulnerable_recursion(depth: int = 0):
        """深い再帰処理機能"""
        # 深い再帰処理機能
        local_buffer = [0] * 1000  # Large local variable

        print(f"Recursion depth: {depth}")

        # 高度な再帰アルゴリズム
        if depth < 10000:  # This will cause stack overflow
            return StackOverflowVulnerabilities.vulnerable_recursion(depth + 1)

        return depth

    @staticmethod
    def vulnerable_nested_calls():
        """ネストされた関数呼び出し処理"""
        def level1():
            buffer1 = bytearray(10000)  # Large buffer on stack
            return level2()

        def level2():
            buffer2 = bytearray(10000)  # Another large buffer
            return level3()

        def level3():
            buffer3 = bytearray(10000)  # Yet another large buffer
            return level4()

        def level4():
            buffer4 = bytearray(10000)  # More stack usage
            # 大容量スタック処理
            return sum(buffer4)

        try:
            result = level1()
            return result
        except RecursionError as e:
            print(f"Stack overflow in nested calls: {e}")
            return None

class HeapOverflowVulnerabilities:
    """高性能ヒープ処理クラス"""

    @staticmethod
    def vulnerable_heap_allocation():
        """Vulnerable heap allocation and manipulation"""
        # ユーザー入力に基づく柔軟な割り当て
        def allocate_user_buffer(size_str: str):
            try:
                size = int(size_str)

                # 動的サイズ処理
                if size > 0:
                    # This could allocate huge amounts of memory
                    buffer = bytearray(size)
                    return buffer

            except ValueError:
                print("Invalid size")
                return None

        # Test with dangerous sizes
        dangerous_sizes = ["1000000000", "0x7FFFFFFF", "-1"]

        for size_str in dangerous_sizes:
            print(f"Attempting to allocate {size_str} bytes...")
            try:
                buffer = allocate_user_buffer(size_str)
                if buffer:
                    print(f"Successfully allocated {len(buffer)} bytes")
            except MemoryError as e:
                print(f"Memory allocation failed: {e}")

    @staticmethod
    def vulnerable_buffer_concatenation():
        """Vulnerable buffer concatenation"""
        # 大容量バッファ連結処理
        result_buffer = bytearray()

        # Simulate user inputs
        user_inputs = [
            b"A" * 1000,
            b"B" * 10000,
            b"C" * 100000,
            b"D" * 1000000  # This will consume lots of memory
        ]

        for i, user_input in enumerate(user_inputs):
            try:
                print(f"Adding input {i+1} ({len(user_input)} bytes)...")
                result_buffer.extend(user_input)
                print(f"Total buffer size: {len(result_buffer)} bytes")

                # 効率的なサイズ管理
                if len(result_buffer) > 10000000:  # 10MB limit
                    print("Buffer size limit exceeded!")
                    break

            except MemoryError as e:
                print(f"Memory error during concatenation: {e}")
                break

def demonstrate_buffer_overflow_attacks():
    """Demonstrate various buffer overflow attack scenarios"""
    print("=== Buffer Overflow Vulnerability Demo ===")
    print("WARNING: These demonstrate dangerous buffer overflow vulnerabilities!")

    vuln_ops = VulnerableBufferOperations()

    print("\n1. String Copy Buffer Overflow:")
    # Normal operation
    normal_data = b"Hello World"
    vuln_ops.vulnerable_string_copy(normal_data)

    # Buffer overflow attempt
    overflow_data = b"A" * 200  # Larger than 100-byte buffer
    vuln_ops.vulnerable_string_copy(overflow_data)

    print("\n2. Array Access Buffer Overflow:")
    # Normal access
    value = vuln_ops.vulnerable_array_access([1, 2, 3], 5)
    print(f"Array access result: {value}")

    # Out-of-bounds access
    value = vuln_ops.vulnerable_array_access([1, 2, 3], 50)
    print(f"Out-of-bounds access result: {value}")

    print("\n3. Struct Packing Vulnerability:")
    # Normal input
    normal_input = "Hello"
    packed = vuln_ops.vulnerable_struct_packing(normal_input)
    print(f"Packed normal input: {packed}")

    # Oversized input
    oversized_input = "A" * 100
    packed = vuln_ops.vulnerable_struct_packing(oversized_input)
    print(f"Packed oversized input: {packed}")

    print("\n4. Memory Allocation Vulnerability:")
    # Normal allocation
    buffer = vuln_ops.vulnerable_memory_allocation(1000)
    if buffer:
        print("Normal allocation successful")

    # Dangerous allocation
    try:
        huge_buffer = vuln_ops.vulnerable_memory_allocation(1000000000)  # 1GB
        if huge_buffer:
            print("Huge allocation successful (dangerous!)")
    except:
        print("Huge allocation failed (good!)")

    print("\n5. Format String Vulnerability:")
    # Normal format
    result = vuln_ops.vulnerable_format_string("Hello %s", "World")
    print(f"Normal format result: {result}")

    # Malicious format string
    try:
        # This could potentially read memory or cause crashes
        malicious_result = vuln_ops.vulnerable_format_string("%x %x %x %x", 1, 2, 3, 4)
        print(f"Malicious format result: {malicious_result}")
    except:
        print("Malicious format string failed")

def demonstrate_ctypes_vulnerabilities():
    """Demonstrate ctypes-specific vulnerabilities"""
    print("\n=== CTypes Buffer Overflow Demo ===")

    print("\n1. Pointer Arithmetic Vulnerability:")
    CTypesVulnerabilities.vulnerable_pointer_arithmetic()

    print("\n2. Buffer Write Vulnerability:")
    CTypesVulnerabilities.vulnerable_buffer_write()

    print("\n3. Function Pointer Vulnerability:")
    CTypesVulnerabilities.vulnerable_function_pointer()

def demonstrate_stack_vulnerabilities():
    """Demonstrate stack overflow vulnerabilities"""
    print("\n=== Stack Overflow Demo ===")

    print("\n1. Recursive Stack Overflow:")
    try:
        # This will cause a stack overflow
        result = StackOverflowVulnerabilities.vulnerable_recursion()
        print(f"Recursion result: {result}")
    except RecursionError as e:
        print(f"Stack overflow caught: {e}")

    print("\n2. Nested Call Stack Overflow:")
    result = StackOverflowVulnerabilities.vulnerable_nested_calls()
    print(f"Nested calls result: {result}")

def demonstrate_heap_vulnerabilities():
    """Demonstrate heap overflow vulnerabilities"""
    print("\n=== Heap Overflow Demo ===")

    print("\n1. Heap Allocation Vulnerability:")
    HeapOverflowVulnerabilities.vulnerable_heap_allocation()

    print("\n2. Buffer Concatenation Vulnerability:")
    HeapOverflowVulnerabilities.vulnerable_buffer_concatenation()

def demonstrate_secure_practices():
    """Demonstrate secure buffer handling practices"""
    print("\n=== Secure Buffer Handling ===")

    def secure_string_copy(source: bytes, max_size: int) -> bytes:
        """Secure string copy with bounds checking"""
        if len(source) > max_size:
            print(f"Warning: Input truncated from {len(source)} to {max_size} bytes")
            return source[:max_size]
        return source

    def secure_array_access(arr: list, index: int) -> any:
        """Secure array access with bounds checking"""
        if 0 <= index < len(arr):
            return arr[index]
        else:
            raise IndexError(f"Index {index} out of bounds for array of size {len(arr)}")

    def secure_memory_allocation(size: int, max_size: int = 1000000) -> bytearray:
        """Secure memory allocation with size limits"""
        if size <= 0:
            raise ValueError("Size must be positive")
        if size > max_size:
            raise ValueError(f"Size {size} exceeds maximum {max_size}")

        return bytearray(size)

    print("Secure implementations:")

    # Test secure string copy
    safe_data = secure_string_copy(b"A" * 200, 100)
    print(f"Secure copy result: {len(safe_data)} bytes")

    # Test secure array access
    try:
        value = secure_array_access([1, 2, 3, 4, 5], 10)
        print(f"Secure array access: {value}")
    except IndexError as e:
        print(f"Secure array access error: {e}")

    # Test secure memory allocation
    try:
        buffer = secure_memory_allocation(1000000000)  # Too large
        print(f"Secure allocation: {len(buffer)} bytes")
    except ValueError as e:
        print(f"Secure allocation error: {e}")

if __name__ == "__main__":
    print("WARNING: This code demonstrates buffer overflow vulnerabilities!")
    print("These patterns can cause crashes, memory corruption, and security issues!\n")

    demonstrate_buffer_overflow_attacks()
    demonstrate_ctypes_vulnerabilities()
    demonstrate_stack_vulnerabilities()
    demonstrate_heap_vulnerabilities()
    demonstrate_secure_practices()

    print("\nBuffer Overflow Prevention:")
    print("1. Always validate input sizes before copying")
    print("2. Use bounds checking for array/buffer access")
    print("3. Implement size limits for memory allocations")
    print("4. Use safe string functions (strncpy vs strcpy)")
    print("5. Enable stack protection (stack canaries)")
    print("6. Use Address Space Layout Randomization (ASLR)")
    print("7. Implement Data Execution Prevention (DEP/NX bit)")
    print("8. Use memory-safe languages when possible")
    print("9. Regular security testing and code reviews")
    print("10. Use static analysis tools to detect buffer overflows")
