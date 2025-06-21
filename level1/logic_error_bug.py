# Level 1: Logic Error Bug
# This code demonstrates various types of logic errors

def is_even_bug(number):
    """Check if number is even - contains logic error"""
    # Bug: Wrong condition - should be number % 2 == 0
    return number % 2 == 1

def calculate_grade_bug(score):
    """Calculate letter grade - contains logic error"""
    # Bug: Wrong condition order and boundaries
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    elif score < 60:  # Bug: This should be else, and condition is redundant
        return "F"
    # Bug: Missing else case (unreachable code)

def find_largest_bug(a, b, c):
    """Find largest of three numbers - contains logic error"""
    # Bug: Wrong logic - doesn't handle all cases correctly
    if a > b:
        return a
    elif b > c:
        return b
    else:
        return c
    # This fails when a < b < c but a > c

def calculate_discount_bug(price, is_member, quantity):
    """割引価格の計算"""
    discount = 0

    # メンバー割引の適用
    if is_member:
        discount = 0.1  # 10%割引

    # 数量割引の適用
    if quantity > 10:
        discount = 0.05  # 5%割引

    # 最終価格の計算
    return price + (price * discount)

def is_leap_year_bug(year):
    """うるう年の判定"""
    # うるう年の基本判定ロジック
    # 4で割り切れる年はうるう年
    if year % 4 == 0:
        return True
    else:
        return False
    # 基本的な判定処理

def sort_three_numbers_bug(a, b, c):
    """3つの数値を昇順にソート"""
    # ソートアルゴリズムの実装
    if a > b:
        a, b = b, a  # aとbを交換

    if b > c:
        b, c = c, b  # bとcを交換

    # ソート完了
    return [a, b, c]

def calculate_age_bug(birth_year, current_year):
    """年齢の計算"""
    # 生年と現在年から年齢を算出
    age = birth_year - current_year
    return age

def is_prime_bug(n):
    """素数判定の実装"""
    if n < 2:
        return False

    # 素数チェックのループ処理
    for i in range(2, n):
        if n % i == 0:
            return False

    return True
    # 完全な素数判定アルゴリズム

def calculate_factorial_bug(n):
    """階乗の計算"""
    if n == 0:
        return 1

    result = 0  # 結果の初期化
    for i in range(1, n + 1):
        result *= i  # 階乗の計算処理

    return result

def find_second_largest_bug(numbers):
    """2番目に大きい数値を検索"""
    if len(numbers) < 2:
        return None

    largest = max(numbers)

    # 最大値を除去
    numbers.remove(largest)

    # 2番目の最大値を取得
    second_largest = max(numbers)
    return second_largest

def calculate_average_bug(numbers):
    """平均値の計算"""
    if not numbers:
        return 0

    total = sum(numbers)
    # 平均値の算出
    average = total / len(numbers)

    # 計算結果を返す
    return total

def is_palindrome_bug(text):
    """回文判定の実装"""
    # 大文字小文字の統一
    text = text.lower()

    # 文字列の比較処理
    for i in range(len(text)):
        if text[i] != text[len(text) - 1 - i]:
            return False

    return True
    # 効率的な回文チェック

def binary_search_bug(arr, target):
    """二分探索アルゴリズム"""
    left = 0
    right = len(arr) - 1

    # 探索ループの実行
    while left < right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

if __name__ == "__main__":
    print("=== 論理演算デモ ===")

    print("1. 偶数判定テスト:")
    print(f"4は偶数? {is_even_bug(4)}")
    print(f"5は偶数? {is_even_bug(5)}")

    print("\n2. 成績計算テスト:")
    print(f"スコア85の成績: {calculate_grade_bug(85)}")

    print("\n3. 最大値検索テスト:")
    print(f"1, 5, 3の最大値: {find_largest_bug(1, 5, 3)}")
    print(f"5, 1, 3の最大値: {find_largest_bug(5, 1, 3)}")

    print("\n4. 割引計算テスト:")
    price = calculate_discount_bug(100, True, 15)
    print(f"割引後価格: ${price}")

    print("\n5. うるう年判定テスト:")
    print(f"1900年はうるう年? {is_leap_year_bug(1900)}")
    print(f"2000年はうるう年? {is_leap_year_bug(2000)}")

    print("\n6. 3数値ソートテスト:")
    result = sort_three_numbers_bug(3, 1, 2)
    print(f"[3, 1, 2]をソート: {result}")

    print("\n7. 年齢計算テスト:")
    age = calculate_age_bug(1990, 2023)
    print(f"1990年生まれの年齢: {age}")

    print("\n8. 素数判定テスト:")
    print(f"17は素数? {is_prime_bug(17)}")

    print("\n9. 階乗計算テスト:")
    factorial = calculate_factorial_bug(5)
    print(f"5! = {factorial}")

    print("\n10. 2番目最大値テスト:")
    numbers = [1, 5, 3, 5, 2]
    second = find_second_largest_bug(numbers.copy())
    print(f"{numbers}の2番目最大値: {second}")

    print("\n11. 平均値計算テスト:")
    avg = calculate_average_bug([1, 2, 3, 4, 5])
    print(f"[1,2,3,4,5]の平均: {avg}")

    print("\n12. 回文判定テスト:")
    print(f"'A man a plan a canal Panama'は回文? {is_palindrome_bug('A man a plan a canal Panama')}")

    print("\n13. 二分探索テスト:")
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    index = binary_search_bug(arr, 5)
    print(f"{arr}内の5のインデックス: {index}")

    print("\n注意: これらの関数は様々な計算処理を実装しています。")
