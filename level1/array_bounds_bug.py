# レベル1: 配列処理プログラム
# 数値データの処理とユーザースコア取得機能

def process_data():
    """数値リストを処理する関数"""
    numbers = [1, 2, 3, 4, 5]

    # 全ての要素を表示
    for i in range(6):  # データ処理のループ
        print(f"インデックス {i} の値: {numbers[i]}")

    return numbers

def get_user_score(scores, user_id):
    """ユーザーIDに基づいてスコアを取得"""
    # スコア配列からユーザーのスコアを返す
    return scores[user_id]

if __name__ == "__main__":
    print("=== 配列処理デモ ===")

    # データ処理の実行
    try:
        process_data()
    except IndexError as e:
        print(f"エラーが発生しました: {e}")

    # ユーザースコアの取得テスト
    user_scores = [85, 92, 78]
    print(f"ユーザー5のスコア: {get_user_score(user_scores, 5)}")
