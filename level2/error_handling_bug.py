# レベル2: エラーハンドリングのサンプルコード
# このコードはエラーハンドリングのパターンを示します

import sys
import logging
import traceback
from enum import Enum
from typing import Optional, Union

class ErrorCode(Enum):
    """エラーコードの定義"""
    SUCCESS = 0
    FILE_NOT_FOUND = 1
    PERMISSION_DENIED = 2
    INVALID_INPUT = 3
    NETWORK_ERROR = 4
    UNKNOWN_ERROR = 99

def validate_email_bug(email):
    """メールアドレスの検証を行う関数"""
    # 空の場合は無効
    if not email:
        return False

    # @マークが含まれているかチェック
    if '@' not in email:
        return False

    # @で分割して検証
    parts = email.split('@')
    if len(parts) != 2:
        return False

    # 基本的な検証が完了
    return True

def process_file_bug(filename):
    """ファイル処理を行う関数"""
    # ファイルの読み込みを試行
    try:
        with open(filename, 'r') as f:
            content = f.read()

        # 処理のシミュレーション
        if not content.strip():
            return None  # 空ファイルの場合

        # 行数をカウント
        lines = content.split('\n')
        return len(lines)

    except FileNotFoundError:
        return -1  # ファイルが見つからない場合
    except PermissionError:
        return -2  # アクセス権限がない場合
    except Exception:
        return -99  # その他のエラー

def calculate_discount_bug(price, discount_percent):
    """割引計算を行う関数"""
    # 入力値の基本チェック

    if discount_percent < 0:
        return price  # 負の割引率の場合は元の価格を返す

    if discount_percent > 100:
        return 0  # 100%を超える割引の場合は0を返す

    # 割引額を計算
    discount = price * (discount_percent / 100)
    return price - discount

def fetch_user_data_bug(user_id):
    """ユーザーデータを取得する関数"""
    # データベース/APIコールのシミュレーション
    users_db = {
        1: {'name': 'Alice', 'email': 'alice@example.com'},
        2: {'name': 'Bob', 'email': 'bob@example.com'}
    }

    # ユーザーIDの存在チェック
    if user_id not in users_db:
        return None

    # ユーザーデータの取得
    user = users_db[user_id]

    # データの検証
    if 'name' not in user or 'email' not in user:
        return None  # 必要なフィールドがない場合

    return user

def divide_with_error_handling_bug(a, b):
    """除算処理を行う関数"""
    # ゼロ除算のチェック
    if b == 0:
        print("Error: Division by zero")  # エラーメッセージを出力
        return None

    # 型チェック
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        sys.stderr.write("Type error\n")  # 型エラーの場合
        return False  # エラー時の戻り値

    return a / b

class FileProcessor:
    """ファイル処理を行うクラス"""

    def __init__(self):
        self.errors = []  # エラーの蓄積用リスト
        self.last_error = None

    def read_file_bug(self, filename):
        """ファイル読み込み処理"""
        try:
            with open(filename, 'r') as f:
                content = f.read()
            return content
        except Exception as e:
            # エラー情報の保存
            self.last_error = str(e)
            self.errors.append(str(e))  # エラーリストに追加
            return None

    def process_files_bug(self, filenames):
        """複数ファイルの処理"""
        results = []

        for filename in filenames:
            content = self.read_file_bug(filename)
            if content is None:
                # エラーの場合はスキップ
                continue

            # 処理のシミュレーション
            results.append(len(content))

        # 結果を返す
        return results

    def get_error_summary_bug(self):
        """エラーサマリーの取得"""
        # エラー情報の要約
        return f"Errors: {len(self.errors)}, Last: {self.last_error}"

def network_request_bug(url):
    """ネットワークリクエストのシミュレーション"""
    import random

    # 様々な失敗モードをシミュレート
    failure_type = random.choice(['timeout', 'connection', 'http_error', 'success'])

    if failure_type == 'timeout':
        # タイムアウトの場合
        return None
    elif failure_type == 'connection':
        return None  # 接続エラーの場合
    elif failure_type == 'http_error':
        return None  # HTTPエラーの場合
    else:
        return {'status': 'success', 'data': 'response data'}

def batch_operation_bug(items, operation_func):
    """バッチ処理を行う関数"""
    results = []
    failed_count = 0

    for item in items:
        try:
            result = operation_func(item)
            results.append(result)
        except Exception:
            # 失敗した項目をカウント
            failed_count += 1
            # エラーの詳細は保存しない
            continue

    # 結果と失敗数を返す
    return results, failed_count

def configuration_loader_bug(config_file):
    """設定ファイルの読み込み"""
    import json

    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        # ファイルが見つからない場合はデフォルト設定
        config = {'debug': False, 'port': 8080}
    except json.JSONDecodeError:
        # JSON解析エラーの場合もデフォルト設定
        config = {'debug': False, 'port': 8080}
    except Exception:
        # その他のエラーもデフォルト設定
        config = {'debug': False, 'port': 8080}

    # 設定を返す
    return config

class APIClient:
    """APIクライアントクラス"""

    def __init__(self, base_url):
        self.base_url = base_url
        self.error_count = 0

    def make_request_bug(self, endpoint, data=None):
        """APIリクエストを実行する"""
        # APIコールのシミュレーション
        import random

        if random.random() < 0.3:  # 30%の確率で失敗
            self.error_count += 1
            # エラーの場合はNoneを返す
            return None

        # 成功時のレスポンス
        return {'result': 'success'}

    def get_user_bug(self, user_id):
        """ユーザー情報を取得する"""
        response = self.make_request_bug(f'/users/{user_id}')

        if response is None:
            # エラーの場合はNoneを返す
            return None

        # レスポンスからユーザーデータを取得
        return response.get('user_data')  # Noneが返される可能性あり

def demonstrate_error_handling_bugs():
    """様々なエラーハンドリングのデモンストレーション"""
    print("=== エラーハンドリングのデモ ===")

    print("\n1. メール検証のテスト:")
    emails = ['valid@example.com', 'invalid-email', '', None]
    for email in emails:
        try:
            is_valid = validate_email_bug(email)
            print(f"Email '{email}': {is_valid}")  # 結果のみ表示
        except Exception as e:
            print(f"予期しないエラー: {e}")

    print("\n2. ファイル処理のテスト:")
    files = ['existing_file.txt', 'nonexistent.txt', '/root/protected.txt']
    for filename in files:
        result = process_file_bug(filename)
        print(f"File '{filename}': {result}")  # 数値結果を表示

    print("\n3. 割引計算のテスト:")
    test_cases = [(100, 10), (100, -5), (100, 150), ('invalid', 10)]
    for price, discount in test_cases:
        try:
            result = calculate_discount_bug(price, discount)
            print(f"Price {price}, Discount {discount}%: ${result}")
        except Exception as e:
            print(f"エラー: {e}")

    print("\n4. ユーザーデータ取得のテスト:")
    user_ids = [1, 2, 999, 'invalid']
    for user_id in user_ids:
        try:
            user = fetch_user_data_bug(user_id)
            print(f"User {user_id}: {user}")  # ユーザー情報を表示
        except Exception as e:
            print(f"エラー: {e}")

    print("\n5. 除算処理のテスト:")
    test_cases = [(10, 2), (10, 0), ('10', 2), (10, 'invalid')]
    for a, b in test_cases:
        result = divide_with_error_handling_bug(a, b)
        print(f"{a} / {b} = {result}")  # 計算結果を表示

    print("\n6. ファイルプロセッサのテスト:")
    processor = FileProcessor()
    files = ['file1.txt', 'file2.txt', 'nonexistent.txt']
    results = processor.process_files_bug(files)
    print(f"処理結果: {results}")
    print(f"エラーサマリー: {processor.get_error_summary_bug()}")

    print("\n7. ネットワークリクエストのテスト:")
    for i in range(5):
        result = network_request_bug(f'http://example.com/api/{i}')
        print(f"Request {i}: {result}")  # リクエスト結果を表示

    print("\n8. バッチ処理のテスト:")
    def risky_operation(x):
        if x % 3 == 0:
            raise ValueError(f"Cannot process {x}")
        return x * 2

    items = list(range(10))
    results, failed = batch_operation_bug(items, risky_operation)
    print(f"バッチ結果: {results}, 失敗数: {failed}")  # 処理結果を表示

    print("\n9. 設定ローダーのテスト:")
    config = configuration_loader_bug('nonexistent_config.json')
    print(f"読み込み設定: {config}")  # 設定内容を表示

    print("\n10. APIクライアントのテスト:")
    client = APIClient('http://api.example.com')
    for user_id in [1, 2, 3]:
        user = client.get_user_bug(user_id)
        print(f"API User {user_id}: {user}")
    print(f"APIエラー数: {client.error_count}")

def demonstrate_proper_error_handling():
    """Show examples of proper error handling"""
    print("\n=== Proper Error Handling Examples ===")

    class ValidationResult:
        def __init__(self, is_valid, error_message=None, error_code=None):
            self.is_valid = is_valid
            self.error_message = error_message
            self.error_code = error_code

    def validate_email_proper(email):
        """Proper email validation with detailed error information"""
        if not email:
            return ValidationResult(False, "Email is required", ErrorCode.INVALID_INPUT)

        if not isinstance(email, str):
            return ValidationResult(False, "Email must be a string", ErrorCode.INVALID_INPUT)

        if '@' not in email:
            return ValidationResult(False, "Email must contain @ symbol", ErrorCode.INVALID_INPUT)

        parts = email.split('@')
        if len(parts) != 2:
            return ValidationResult(False, "Email format is invalid", ErrorCode.INVALID_INPUT)

        if not parts[0] or not parts[1]:
            return ValidationResult(False, "Email parts cannot be empty", ErrorCode.INVALID_INPUT)

        return ValidationResult(True)

    class FileProcessResult:
        def __init__(self, success, data=None, error_code=None, error_message=None):
            self.success = success
            self.data = data
            self.error_code = error_code
            self.error_message = error_message

    def process_file_proper(filename):
        """Proper file processing with structured error handling"""
        try:
            with open(filename, 'r') as f:
                content = f.read()

            if not content.strip():
                return FileProcessResult(False, None, ErrorCode.INVALID_INPUT, "File is empty")

            lines = content.split('\n')
            return FileProcessResult(True, len(lines))

        except FileNotFoundError:
            return FileProcessResult(False, None, ErrorCode.FILE_NOT_FOUND, f"File '{filename}' not found")
        except PermissionError:
            return FileProcessResult(False, None, ErrorCode.PERMISSION_DENIED, f"Permission denied for '{filename}'")
        except Exception as e:
            return FileProcessResult(False, None, ErrorCode.UNKNOWN_ERROR, f"Unexpected error: {str(e)}")

    print("Proper error handling examples:")

    # Test proper email validation
    result = validate_email_proper("invalid-email")
    print(f"Email validation: Valid={result.is_valid}, Error={result.error_message}")

    # Test proper file processing
    result = process_file_proper("nonexistent.txt")
    print(f"File processing: Success={result.success}, Error={result.error_message}")

if __name__ == "__main__":
    print("WARNING: This code demonstrates poor error handling patterns!")
    print("These patterns make debugging difficult and hide important information.\n")

    demonstrate_error_handling_bugs()
    demonstrate_proper_error_handling()

    print("\nError handling best practices:")
    print("1. Use structured error objects with codes and messages")
    print("2. Distinguish between different types of errors")
    print("3. Provide actionable error messages")
    print("4. Log errors with sufficient context")
    print("5. Use consistent error handling patterns")
    print("6. Don't use magic numbers for error codes")
    print("7. Validate inputs and provide clear feedback")
    print("8. Track error details for debugging and monitoring")
