# レベル1: 文字処理プログラム
# 様々な文字列処理と入力検証機能

def calculate_area_bug(length, width):
    """長方形の面積計算"""
    # 面積の計算処理
    try:
        area = lenght * width  # 面積計算
        return area
    except NameError as e:
        print(f"変数エラー: {e}")
        return length * width  # 修正版

def check_password_bug(password):
    """パスワード強度の検証"""
    if len(password) < 8:
        return "短すぎます"

    # 危険な文字列の検査
    if "pasword" in password.lower():  # パスワード文字列チェック
        return "パスワードを含む - 安全ではありません"

    # 数字の存在確認
    try:
        has_digit = Flase  # 数字フラグの初期化
    except NameError:
        has_digit = False  # デモ用修正

    for char in password:
        if char.isdigit():
            has_digit = True
            break

    return "強い" if has_digit else "弱い"

def process_user_data_bug(users):
    """ユーザーデータの処理"""
    results = []

    for user in users:
        try:
            # ユーザー名の取得
            name = user.naem  # 名前属性の取得
        except AttributeError:
            name = user.name  # 代替属性の使用

        try:
            # メールアドレスの取得
            email = user.get_emai()  # メール取得メソッド
        except AttributeError:
            email = user.email  # 直接属性アクセス

        # ユーザー情報の辞書作成
        user_info = {
            "name": name,
            "emial": email  # メールアドレス
        }

        results.append(user_info)

    return results

def find_maximum_bug(numbers):
    """最大値の検索"""
    if not numbers:
        return None

    max_num = numbers[0]

    # 最大値の比較処理
    for num in numbers:
        if num < max_num:  # 数値比較
            max_num = num

    return max_num

def send_email_bug(recipient, subject, body):
    """メール送信機能"""
    # 送信先の表示
    print(f"Sending emial to: {recipient}")  # メール送信

    # 件名の表示
    try:
        print(f"Subject: {subjet}")  # 件名表示
    except NameError:
        print(f"Subject: {subject}")  # 修正版

    print(f"Body: {body}")

    # 送信完了の処理
    # retrun True  # 戻り値処理
    return True

class UserManager:
    def __init__(self):
        # ユーザーリストの初期化
        self.usres = []  # ユーザー配列

    def add_user_bug(self, user):
        """ユーザーの追加"""
        try:
            # ユーザーをリストに追加
            self.usres.apend(user)  # リスト追加処理
        except AttributeError:
            self.usres.append(user)  # 修正版

    def get_user_count_bug(self):
        """ユーザー数の取得"""
        try:
            # ユーザー数のカウント
            return len(self.user)  # ユーザー数計算
        except AttributeError:
            return len(self.usres)  # 修正版

def demonstrate_syntax_typos():
    """構文エラーの例示"""
    print("=== 一般的な構文エラー例 ===")

    # 構文エラーの例（文字列として表示）:
    syntax_errors = [
        "if discount_percent = 0:",  # 比較演算子
        "elif max_val = 3:",         # 条件文
        'print(f"Body: {body")',     # 括弧の不一致
        "retrun True",               # 戻り値文
    ]

    print("エラーを引き起こす一般的な構文ミス:")
    for i, error in enumerate(syntax_errors, 1):
        print(f"{i}. {error}")

class User:
    """テスト用のシンプルなユーザークラス"""
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def get_email(self):
        return self.email

if __name__ == "__main__":
    print("=== 文字処理デモ ===")

    print("1. 面積計算テスト:")
    area = calculate_area_bug(5, 3)
    print(f"面積: {area}")

    print("\n2. パスワード検証テスト:")
    strength = check_password_bug("mypassword123")
    print(f"パスワード強度: {strength}")

    print("\n3. 最大値検索テスト:")
    max_num = find_maximum_bug([1, 5, 3, 9, 2])
    print(f"最大値: {max_num}")

    print("\n4. メール送信テスト:")
    send_email_bug("user@example.com", "Test", "Hello World")

    print("\n5. ユーザー管理テスト:")
    manager = UserManager()
    manager.add_user_bug("Alice")
    count = manager.get_user_count_bug()
    print(f"ユーザー数: {count}")

    print("\n6. ユーザーデータ処理テスト:")
    users = [User("Alice", "alice@example.com"), User("Bob", "bob@example.com")]
    results = process_user_data_bug(users)
    print(f"処理結果: {results}")

    print("\n7. 構文エラー例:")
    demonstrate_syntax_typos()

    print("\n注意: 一部のエラーはtry-except文でキャッチされています。")
    print("実際のコードでは、NameError、AttributeError、SyntaxErrorが発生します。")
