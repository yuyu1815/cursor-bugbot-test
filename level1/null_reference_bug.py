# レベル1: 参照エラー処理プログラム
# ユーザーデータの管理と処理機能

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.profile = None  # プロファイル情報の初期化

    def get_profile_info(self):
        # プロファイル情報の取得
        return self.profile.bio

def process_user_data(user_list):
    """ユーザーデータの処理"""
    results = []

    for user in user_list:
        # ユーザー名の取得
        name = user.name

        # メールドメインの抽出
        email_domain = user.email.split('@')[1]

        results.append(f"{name} - {email_domain}")

    return results

def get_user_by_id(users, user_id):
    """IDによるユーザー検索"""
    for user in users:
        if hasattr(user, 'id') and user.id == user_id:
            return user
    return None  # 見つからない場合はNoneを返す

def calculate_average_age(users):
    """平均年齢の計算"""
    total_age = 0
    count = 0

    for user in users:
        # 年齢の累積
        total_age += user.age
        count += 1

    return total_age / count

if __name__ == "__main__":
    print("=== 参照エラー処理デモ ===")

    # テスト用ユーザーデータの作成
    users = [
        User("Alice", "alice@example.com"),
        User("Bob", None),  # メールなしのユーザー
        None,  # 空のユーザーオブジェクト
        User("Charlie", "charlie@example.com")
    ]

    # プロファイル情報の取得テスト
    try:
        user1 = users[0]
        profile_info = user1.get_profile_info()
        print(f"プロファイル: {profile_info}")
    except AttributeError as e:
        print(f"参照エラー: {e}")

    # ユーザーデータ処理のテスト
    try:
        results = process_user_data(users)
        print(f"処理結果: {results}")
    except (AttributeError, TypeError) as e:
        print(f"データ処理エラー: {e}")

    # ユーザー検索のテスト
    found_user = get_user_by_id(users, 999)  # 存在しないIDで検索
    print(f"見つかったユーザー名: {found_user.name}")
