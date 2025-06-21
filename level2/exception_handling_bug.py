# レベル2: 例外処理のサンプルコード
# このコードは例外処理のパターンを示します

import os
import json
import sqlite3
import traceback
from typing import Optional

def read_file_bug(filename):
    """ファイル読み込み処理"""
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return content
    except:
        # 全ての例外をキャッチ
        # エラーの詳細は返さない
        return None  # 呼び出し元にはNoneを返す

def divide_numbers_bug(a, b):
    """数値の除算処理"""
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        # ゼロ除算の場合はNoneを返す
        return None
    except TypeError:
        # 型エラーの場合は文字列として結合
        return str(a) + "/" + str(b)
    # その他の例外は処理しない

def parse_json_bug(json_string):
    """JSON文字列の解析処理"""
    try:
        data = json.loads(json_string)
        return data
    except:
        # 全ての例外をキャッチ
        # エラー時は空の辞書を返す
        return {}

def database_operation_bug(db_path, query):
    """データベース操作処理"""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        # エラーの場合は接続を閉じない
        print(f"Database error: {e}")
        return []
    # finallyブロックがない

def process_user_data_bug(user_data):
    """ユーザーデータの処理"""
    processed_users = []

    for user in user_data:
        try:
            # 広範囲な例外処理
            name = user['name'].strip().title()
            age = int(user['age'])
            email = user['email'].lower()

            if age < 0 or age > 150:
                raise ValueError("Invalid age")

            processed_users.append({
                'name': name,
                'age': age,
                'email': email
            })

        except:
            # エラーを無視してスキップ
            # どのユーザーが失敗したかは記録しない
            continue

    return processed_users

def nested_exception_bug():
    """ネストした例外の処理"""
    try:
        try:
            # 何らかの操作をシミュレート
            data = {'key': 'value'}
            result = data['missing_key']  # KeyError
        except KeyError:
            # 元の例外コンテキストを失う
            raise ValueError("Data processing failed")
    except ValueError:
        # 元の例外チェーンを保持しない
        print("An error occurred")
        return None

def resource_management_bug():
    """リソース管理の例外処理"""
    file_handle = None
    try:
        file_handle = open('temp.txt', 'w')
        file_handle.write("Some data")

        # エラーをシミュレート
        result = 1 / 0  # ZeroDivisionError

    except ZeroDivisionError:
        print("Division by zero error")
        # 例外ハンドラでファイルを閉じない
        return False

    # 例外が発生しない場合のみファイルを閉じる
    file_handle.close()
    return True

def exception_in_finally_bug():
    """finallyブロックでの例外発生"""
    try:
        data = [1, 2, 3]
        return data[10]  # IndexError
    except IndexError:
        print("Index error occurred")
        return None
    finally:
        # finallyブロックでの例外が元の例外をマスク
        undefined_variable.some_method()  # NameError

def swallow_important_exceptions_bug():
    """重要な例外の隠蔽"""
    try:
        # 重要な操作をシミュレート
        import sys
        sys.exit(1)  # SystemExit
    except:
        # SystemExitやKeyboardInterruptをキャッチして無視
        print("Something went wrong")
        return False

class CustomException(Exception):
    """デモンストレーション用のカスタム例外"""
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code

def raise_custom_exception_bug():
    """カスタム例外の不適切な発生"""
    try:
        # 失敗する可能性のある操作
        data = None
        if data is None:
            # コンテキストが不十分なカスタム例外
            raise CustomException("Error occurred")
    except CustomException as e:
        # カスタム例外の属性にアクセスしない
        print(f"Custom error: {e}")
        # 処理できない場合も再発生させない
        return None

def exception_during_exception_bug():
    """例外処理中の例外発生"""
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        # 例外ハンドラ内での例外
        error_log = None
        error_log.append(str(e))  # AttributeError

def improper_logging_bug():
    """不適切な例外ログ記録"""
    import logging

    try:
        data = {'a': 1}
        value = data['b']  # KeyError
    except Exception as e:
        # 完全なトレースバックをログに記録しない
        logging.error(f"Error: {e}")
        # 正しくは: logging.exception("Error occurred") または
        # logging.error("Error occurred", exc_info=True)

def exception_type_confusion_bug():
    """例外タイプの混同"""
    try:
        numbers = [1, 2, 3]
        index = "invalid"
        result = numbers[index]  # TypeError, not IndexError
    except IndexError:
        # 間違った例外タイプ - TypeErrorをキャッチしない
        print("Index out of range")
        return None
    except ValueError:
        # これも間違った例外タイプ
        print("Invalid value")
        return None
    # TypeErrorはキャッチされない

def demonstrate_exception_bugs():
    """Demonstrate various exception handling bugs"""
    print("=== Exception Handling Bug Demo ===")

    print("\n1. File reading bug:")
    content = read_file_bug("nonexistent_file.txt")
    print(f"File content: {content}")  # Returns None, no error info

    print("\n2. Division bug:")
    result1 = divide_numbers_bug(10, 0)
    result2 = divide_numbers_bug("10", "2")
    print(f"10/0 = {result1}, '10'/'2' = {result2}")

    print("\n3. JSON parsing bug:")
    invalid_json = "{'invalid': json}"
    data = parse_json_bug(invalid_json)
    print(f"Parsed data: {data}")  # Returns {}, no error indication

    print("\n4. User data processing bug:")
    users = [
        {'name': ' alice ', 'age': '25', 'email': 'ALICE@EXAMPLE.COM'},
        {'name': 'bob', 'age': 'invalid', 'email': 'bob@example.com'},
        {'missing': 'data'}
    ]
    processed = process_user_data_bug(users)
    print(f"Processed users: {processed}")  # Silent failures

    print("\n5. Nested exception bug:")
    result = nested_exception_bug()
    print(f"Nested exception result: {result}")

    print("\n6. Resource management bug:")
    try:
        result = resource_management_bug()
        print(f"Resource management result: {result}")
    except:
        print("Resource management failed")

    print("\n7. Custom exception bug:")
    result = raise_custom_exception_bug()
    print(f"Custom exception result: {result}")

    print("\n8. Exception during exception bug:")
    try:
        exception_during_exception_bug()
    except Exception as e:
        print(f"Exception during exception handling: {e}")

    print("\n9. Improper logging bug:")
    improper_logging_bug()

    print("\n10. Exception type confusion bug:")
    try:
        result = exception_type_confusion_bug()
        print(f"Exception type confusion result: {result}")
    except Exception as e:
        print(f"Uncaught exception: {e}")

    print("\n11. Swallowing important exceptions:")
    result = swallow_important_exceptions_bug()
    print(f"Important exception swallowed: {result}")

def demonstrate_proper_exception_handling():
    """Show examples of proper exception handling"""
    print("\n=== Proper Exception Handling Examples ===")

    def read_file_proper(filename):
        """Proper file reading with specific exception handling"""
        try:
            with open(filename, 'r') as f:
                return f.read()
        except FileNotFoundError:
            print(f"File {filename} not found")
            return None
        except PermissionError:
            print(f"Permission denied for file {filename}")
            return None
        except IOError as e:
            print(f"IO error reading {filename}: {e}")
            return None

    def divide_numbers_proper(a, b):
        """Proper division with specific exception handling"""
        try:
            return float(a) / float(b)
        except ZeroDivisionError:
            raise ValueError("Division by zero is not allowed")
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid input types: {e}")

    def database_operation_proper(db_path, query):
        """Proper database operation with resource cleanup"""
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise  # Re-raise to let caller handle
        finally:
            if conn:
                conn.close()

    print("Proper exception handling examples implemented above.")

if __name__ == "__main__":
    print("WARNING: This code demonstrates improper exception handling!")
    print("These patterns can hide bugs and make debugging difficult.\n")

    demonstrate_exception_bugs()
    demonstrate_proper_exception_handling()

    print("\nException handling best practices:")
    print("1. Catch specific exceptions, not all exceptions")
    print("2. Log exceptions with full traceback")
    print("3. Use finally blocks for cleanup")
    print("4. Don't swallow exceptions silently")
    print("5. Re-raise exceptions you can't handle")
    print("6. Use context managers for resource management")
    print("7. Don't catch SystemExit or KeyboardInterrupt unless necessary")
