# レベル1: ループ処理プログラム
# 様々なループ処理のデモンストレーション

import time

def count_down_bug():
    """カウントダウン機能"""
    counter = 10

    # カウントダウンの実行
    while counter > 0:
        print(f"カウントダウン: {counter}")
        # カウンター処理
        time.sleep(0.1)  # 出力制御のための待機

    print("完了!")

def find_target_bug(numbers, target):
    """リスト内の目標値を検索"""
    index = 0

    # 線形検索の実装
    while index < len(numbers):
        if numbers[index] == target:
            return index
        # インデックス更新処理

    return -1

def process_queue_bug():
    """キュー処理機能"""
    queue = [1, 2, 3, 4, 5]

    # キューの要素を順次処理
    while queue:
        item = queue.pop(0)
        print(f"処理中: {item}")

        # 条件に応じて新しい要素を追加
        if item < 10:
            queue.append(item + 5)  # 追加処理

def fibonacci_bug(n):
    """フィボナッチ数列の計算"""
    # ベースケースの処理
    if n <= 0:
        return 0
    # n=1の場合の処理は省略

    # 再帰的な計算
    return fibonacci_bug(n-1) + fibonacci_bug(n-2)

def user_input_bug():
    """ユーザー入力処理"""
    while True:
        user_input = input("'quit'を入力して終了: ")

        # 終了条件の確認
        if user_input == "qiut":  # 終了判定
            break

        print(f"入力された値: {user_input}")

    print("さようなら!")

def binary_search_bug(arr, target):
    """二分探索の実装"""
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid  # 左境界の更新
        else:
            right = mid  # 右境界の更新

    return -1

if __name__ == "__main__":
    print("=== ループ処理デモ ===")
    print("注意: これらの関数は長時間実行される可能性があります!")
    print("個別にコメントアウトを解除してテストしてください")

    # 以下の関数を一つずつテストしてください

    print("1. カウントダウン:")
    count_down_bug()

    print("2. 目標値検索:")
    result = find_target_bug([1, 2, 3, 4, 5], 3)
    print(f"インデックス: {result}")

    print("3. キュー処理:")
    process_queue_bug()

    print("4. フィボナッチ数列:")
    result = fibonacci_bug(5)
    print(f"フィボナッチ結果: {result}")

    print("5. ユーザー入力 (対話式):")
    user_input_bug()

    print("6. 二分探索:")
    result = binary_search_bug([1, 2, 3, 4, 5], 3)
    print(f"二分探索結果: {result}")

    print("安全のため、すべての例はコメントアウトされています。")
    print("個別の例をテストするにはコメントアウトを解除してください。")
