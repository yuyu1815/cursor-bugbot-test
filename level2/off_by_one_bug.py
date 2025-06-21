# レベル2: オフバイワンエラーのサンプルコード
# このコードは様々なオフバイワンエラーを示します

def copy_array_bug(source, destination):
    """配列のコピー処理"""
    # ループが1回多く実行される
    for i in range(len(source) + 1):  # 範囲が1つ多い
        destination[i] = source[i]  # インデックスエラーが発生

def find_last_element_bug(arr):
    """最後の要素を取得する処理"""
    if not arr:
        return None

    # 配列の境界を超えてアクセス
    return arr[len(arr)]  # インデックスが1つ多い

def substring_bug(text, start, length):
    """部分文字列の抽出処理"""
    # 終了インデックスの計算
    end = start + length  # 計算方法に問題あり

    if end > len(text):
        end = len(text)

    result = ""
    # ループ条件に終了インデックスを含む
    for i in range(start, end + 1):  # 範囲が1つ多い
        if i < len(text):
            result += text[i]

    return result

def binary_search_bug(arr, target):
    """二分探索の実装"""
    left = 0
    right = len(arr)  # 初期値が1つ多い

    while left < right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

def reverse_array_bug(arr):
    """Reverse array in place with off-by-one error"""
    n = len(arr)

    # Bug: Loop goes one iteration too far
    for i in range(n // 2 + 1):  # Should be range(n // 2)
        # Swap elements
        temp = arr[i]
        arr[i] = arr[n - 1 - i]
        arr[n - 1 - i] = temp

def matrix_traverse_bug(matrix):
    """Traverse matrix with off-by-one errors"""
    if not matrix or not matrix[0]:
        return []

    rows = len(matrix)
    cols = len(matrix[0])
    result = []

    # Bug: Loop bounds are wrong
    for i in range(rows + 1):  # Should be range(rows)
        for j in range(cols + 1):  # Should be range(cols)
            result.append(matrix[i][j])  # IndexError

    return result

def fibonacci_bug(n):
    """Calculate fibonacci with off-by-one error"""
    if n <= 0:
        return 0
    if n == 1:
        return 1

    # Bug: Array size is wrong
    fib = [0] * n  # Should be [0] * (n + 1)
    fib[0] = 0
    fib[1] = 1

    # Bug: Loop goes beyond array bounds
    for i in range(2, n + 1):  # Will access fib[n] which doesn't exist
        fib[i] = fib[i-1] + fib[i-2]

    return fib[n]

def string_comparison_bug(str1, str2):
    """Compare strings with off-by-one error"""
    min_len = min(len(str1), len(str2))

    # Bug: Loop includes equal length case incorrectly
    for i in range(min_len + 1):  # Should be range(min_len)
        if str1[i] != str2[i]:  # IndexError when i == min_len
            return False

    return len(str1) == len(str2)

def bubble_sort_bug(arr):
    """Bubble sort with off-by-one error"""
    n = len(arr)

    # Bug: Outer loop goes one iteration too far
    for i in range(n + 1):  # Should be range(n)
        # Bug: Inner loop bounds are wrong
        for j in range(n - i):  # Should be range(n - i - 1)
            if j + 1 < len(arr) and arr[j] > arr[j + 1]:
                # Swap
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def find_peak_bug(arr):
    """Find peak element with off-by-one error"""
    if not arr:
        return -1

    # Bug: Loop bounds are wrong
    for i in range(1, len(arr)):  # Should be range(1, len(arr) - 1)
        # Bug: Not checking right boundary
        if arr[i] > arr[i-1] and arr[i] > arr[i+1]:  # IndexError at last element
            return i

    return -1

def sliding_window_bug(arr, window_size):
    """Sliding window with off-by-one error"""
    if len(arr) < window_size:
        return []

    result = []

    # Bug: Loop goes beyond valid range
    for i in range(len(arr) - window_size + 2):  # Should be +1, not +2
        window_sum = 0
        for j in range(window_size):
            window_sum += arr[i + j]  # IndexError
        result.append(window_sum)

    return result

def merge_arrays_bug(arr1, arr2):
    """Merge two sorted arrays with off-by-one error"""
    result = []
    i = j = 0

    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1

    # Bug: Wrong loop bounds for remaining elements
    while i <= len(arr1):  # Should be i < len(arr1)
        result.append(arr1[i])  # IndexError
        i += 1

    while j <= len(arr2):  # Should be j < len(arr2)
        result.append(arr2[j])  # IndexError
        j += 1

    return result

def count_occurrences_bug(text, pattern):
    """Count pattern occurrences with off-by-one error"""
    count = 0
    pattern_len = len(pattern)

    # Bug: Loop goes beyond valid range
    for i in range(len(text) - pattern_len + 2):  # Should be +1, not +2
        if text[i:i + pattern_len] == pattern:  # StringIndexError
            count += 1

    return count

def rotate_array_bug(arr, k):
    """Rotate array with off-by-one error"""
    if not arr:
        return

    n = len(arr)
    k = k % n

    # Create temporary array
    temp = [0] * n

    # Bug: Wrong index calculation
    for i in range(n):
        temp[(i + k + 1) % n] = arr[i]  # Should be (i + k) % n

    # Copy back
    for i in range(n):
        arr[i] = temp[i]

def pascal_triangle_bug(num_rows):
    """Generate Pascal's triangle with off-by-one error"""
    if num_rows <= 0:
        return []

    triangle = []

    for i in range(num_rows):
        # Bug: Row size is wrong
        row = [0] * (i + 2)  # Should be (i + 1)
        row[0] = 1

        # Bug: Loop bounds are wrong
        for j in range(1, i + 1):  # Should check if j < len(row)
            if i > 0:
                row[j] = triangle[i-1][j-1] + triangle[i-1][j]  # IndexError

        triangle.append(row)

    return triangle

def demonstrate_off_by_one_bugs():
    """Demonstrate various off-by-one errors"""
    print("=== Off-by-One Error Demo ===")
    print("WARNING: These functions contain off-by-one errors that cause crashes!")

    print("\n1. Array copy bug:")
    try:
        source = [1, 2, 3, 4, 5]
        destination = [0] * 5
        copy_array_bug(source, destination)
        print(f"Copied: {destination}")
    except IndexError as e:
        print(f"IndexError: {e}")

    print("\n2. Find last element bug:")
    try:
        arr = [1, 2, 3, 4, 5]
        last = find_last_element_bug(arr)
        print(f"Last element: {last}")
    except IndexError as e:
        print(f"IndexError: {e}")

    print("\n3. Substring bug:")
    try:
        text = "Hello World"
        substr = substring_bug(text, 2, 5)
        print(f"Substring: '{substr}'")
    except IndexError as e:
        print(f"IndexError: {e}")

    print("\n4. Binary search bug:")
    try:
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        index = binary_search_bug(arr, 5)
        print(f"Found 5 at index: {index}")
    except IndexError as e:
        print(f"IndexError: {e}")

    print("\n5. Reverse array bug:")
    try:
        arr = [1, 2, 3, 4, 5]
        reverse_array_bug(arr)
        print(f"Reversed: {arr}")
    except IndexError as e:
        print(f"IndexError: {e}")

    print("\n6. Matrix traverse bug:")
    try:
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        result = matrix_traverse_bug(matrix)
        print(f"Matrix traversal: {result}")
    except IndexError as e:
        print(f"IndexError: {e}")

    print("\n7. Fibonacci bug:")
    try:
        fib = fibonacci_bug(10)
        print(f"Fibonacci(10): {fib}")
    except IndexError as e:
        print(f"IndexError: {e}")

    print("\n8. String comparison bug:")
    try:
        result = string_comparison_bug("hello", "world")
        print(f"Strings equal: {result}")
    except IndexError as e:
        print(f"IndexError: {e}")

    print("\n9. Bubble sort bug:")
    try:
        arr = [64, 34, 25, 12, 22, 11, 90]
        bubble_sort_bug(arr)
        print(f"Sorted: {arr}")
    except IndexError as e:
        print(f"IndexError: {e}")

    print("\n10. Find peak bug:")
    try:
        arr = [1, 3, 20, 4, 1, 0]
        peak = find_peak_bug(arr)
        print(f"Peak at index: {peak}")
    except IndexError as e:
        print(f"IndexError: {e}")

    print("\n11. Sliding window bug:")
    try:
        arr = [1, 2, 3, 4, 5, 6, 7]
        windows = sliding_window_bug(arr, 3)
        print(f"Window sums: {windows}")
    except IndexError as e:
        print(f"IndexError: {e}")

    print("\n12. Merge arrays bug:")
    try:
        arr1 = [1, 3, 5]
        arr2 = [2, 4, 6]
        merged = merge_arrays_bug(arr1, arr2)
        print(f"Merged: {merged}")
    except IndexError as e:
        print(f"IndexError: {e}")

    print("\n13. Count occurrences bug:")
    try:
        count = count_occurrences_bug("hello world hello", "hello")
        print(f"Occurrences: {count}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n14. Rotate array bug:")
    try:
        arr = [1, 2, 3, 4, 5, 6, 7]
        rotate_array_bug(arr, 3)
        print(f"Rotated: {arr}")
    except IndexError as e:
        print(f"IndexError: {e}")

    print("\n15. Pascal triangle bug:")
    try:
        triangle = pascal_triangle_bug(5)
        print(f"Pascal triangle: {triangle}")
    except IndexError as e:
        print(f"IndexError: {e}")

def demonstrate_correct_implementations():
    """Show correct implementations without off-by-one errors"""
    print("\n=== Correct Implementations ===")

    def copy_array_correct(source, destination):
        for i in range(len(source)):  # Correct bounds
            destination[i] = source[i]

    def find_last_element_correct(arr):
        if not arr:
            return None
        return arr[len(arr) - 1]  # Correct index

    def binary_search_correct(arr, target):
        left = 0
        right = len(arr) - 1  # Correct initial value

        while left <= right:  # Correct condition
            mid = (left + right) // 2

            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1

    print("Correct implementations:")

    # Test correct copy
    source = [1, 2, 3, 4, 5]
    destination = [0] * 5
    copy_array_correct(source, destination)
    print(f"Correct copy: {destination}")

    # Test correct last element
    last = find_last_element_correct([1, 2, 3, 4, 5])
    print(f"Correct last element: {last}")

    # Test correct binary search
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    index = binary_search_correct(arr, 5)
    print(f"Correct binary search result: {index}")

if __name__ == "__main__":
    print("WARNING: This code demonstrates off-by-one errors!")
    print("These errors cause IndexError and other boundary-related bugs.\n")

    demonstrate_off_by_one_bugs()
    demonstrate_correct_implementations()

    print("\nOff-by-one error prevention tips:")
    print("1. Use len(array) - 1 for last index, not len(array)")
    print("2. Use range(len(array)) for full iteration")
    print("3. Be careful with <= vs < in loop conditions")
    print("4. Double-check array bounds in nested loops")
    print("5. Use Python slicing when possible (it handles bounds correctly)")
    print("6. Test with edge cases: empty arrays, single elements")
    print("7. Use debugger to step through boundary conditions")
