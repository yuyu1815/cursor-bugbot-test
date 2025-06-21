# レベル4: タイミング処理システム
# このコードは高度なタイミング処理機能を実装しています

import time
import hashlib
import hmac
import secrets
import random
import statistics
from typing import List, Dict, Optional, Tuple
import threading
import queue

class AdvancedTimingAttacks:
    """高度なタイミング処理システム"""

    def __init__(self):
        self.secret_database = {
            "user1": {"password": "secret123", "role": "user", "balance": 1000},
            "admin": {"password": "admin_super_secret", "role": "admin", "balance": 50000},
            "guest": {"password": "guest_pass", "role": "guest", "balance": 0}
        }
        self.api_keys = [
            "sk_live_abc123def456ghi789",
            "sk_test_xyz789uvw456rst123",
            "sk_prod_mno345pqr678stu901"
        ]
        self.session_tokens = {}
        self.failed_attempts = {}

    def vulnerable_progressive_delay_auth(self, username: str, password: str) -> bool:
        """段階的遅延を伴う認証処理"""
        # 段階的遅延によるパスワード長と部分一致の処理
        if username not in self.secret_database:
            time.sleep(0.1)  # 存在しないユーザーに対する固定遅延
            return False

        stored_password = self.secret_database[username]["password"]

        # 正しい文字ごとに遅延が増加
        correct_chars = 0
        for i in range(min(len(password), len(stored_password))):
            if password[i] == stored_password[i]:
                correct_chars += 1
                time.sleep(0.01)  # 正しい文字ごとに10ms遅延
            else:
                break

        # ユーザーロールに基づく追加遅延
        if self.secret_database[username]["role"] == "admin":
            time.sleep(0.05)  # 管理者アカウントには追加遅延

        return password == stored_password

    def vulnerable_database_query_timing(self, user_id: str) -> Optional[Dict]:
        """データベースクエリのタイミング処理"""
        # データの複雑さに基づく異なるクエリ時間のシミュレーション

        # クエリ時間がユーザーデータ情報を反映
        if user_id == "admin":
            # 管理者は複雑なデータ構造 - より長いクエリ時間
            time.sleep(0.1)
            return {"id": "admin", "permissions": ["read", "write", "delete"], "data": "complex"}
        elif user_id in ["user1", "user2", "user3"]:
            # 一般ユーザーは中程度の複雑さ
            time.sleep(0.05)
            return {"id": user_id, "permissions": ["read"], "data": "simple"}
        elif user_id.startswith("guest"):
            # ゲストユーザーは最小限のデータ - 高速クエリ
            time.sleep(0.01)
            return {"id": user_id, "permissions": [], "data": "none"}
        else:
            # 存在しないユーザー - 異なるタイミングパターン
            time.sleep(0.02)
            return None

    def vulnerable_api_key_validation(self, api_key: str) -> Tuple[bool, str]:
        """APIキー検証処理"""
        # 異なるキータイプに対する異なる検証時間

        if api_key.startswith("sk_live_"):
            # ライブキーには追加のセキュリティチェックが必要
            time.sleep(0.1)
            key_type = "live"
        elif api_key.startswith("sk_test_"):
            # テストキーはより高速な検証
            time.sleep(0.02)
            key_type = "test"
        elif api_key.startswith("sk_prod_"):
            # プロダクションキーは中程度の検証時間
            time.sleep(0.05)
            key_type = "production"
        else:
            # 無効な形式 - 高速拒否
            time.sleep(0.001)
            return False, "invalid"

        # 文字単位での比較処理
        for valid_key in self.api_keys:
            if self.vulnerable_string_compare_with_timing(api_key, valid_key):
                return True, key_type

        return False, key_type

    def vulnerable_string_compare_with_timing(self, input_str: str, target_str: str) -> bool:
        """タイミング処理を伴う文字列比較"""
        if len(input_str) != len(target_str):
            return False

        # 早期終了による最初の差異位置の処理
        for i in range(len(input_str)):
            if input_str[i] != target_str[i]:
                return False
            # 文字ごとの処理遅延
            time.sleep(0.001)

        return True

    def vulnerable_rate_limiting_check(self, client_ip: str) -> bool:
        """タイミングサイドチャネルを伴うレート制限"""
        current_time = time.time()

        if client_ip not in self.failed_attempts:
            self.failed_attempts[client_ip] = []

        # 古い試行の削除
        self.failed_attempts[client_ip] = [
            attempt_time for attempt_time in self.failed_attempts[client_ip]
            if current_time - attempt_time < 3600  # 1時間のウィンドウ
        ]

        attempt_count = len(self.failed_attempts[client_ip])

        # 異なる遅延パターンが試行回数を反映
        if attempt_count == 0:
            # 最初の試行 - 遅延なし
            pass
        elif attempt_count < 5:
            # 少数の試行 - 小さな遅延
            time.sleep(0.1 * attempt_count)
        elif attempt_count < 10:
            # 多数の試行 - より大きな遅延
            time.sleep(0.5 + 0.1 * attempt_count)
        else:
            # 過度の試行 - 非常に大きな遅延
            time.sleep(2.0 + 0.2 * attempt_count)

        # 閾値未満の場合は許可
        return attempt_count < 10

class CryptographicTimingAttacks:
    """暗号化タイミング処理システム"""

    def __init__(self):
        self.secret_key = b"super_secret_cryptographic_key_123"
        self.rsa_private_key = 12345  # デモンストレーション用の簡略化

    def vulnerable_padding_oracle(self, ciphertext: bytes) -> bool:
        """パディングオラクル処理"""
        # 復号化プロセスのシミュレーション
        try:
            # 有効/無効パディングに対する異なるタイミング
            if len(ciphertext) % 16 != 0:
                # 無効な長さ - 高速拒否
                return False

            # 復号化のシミュレーション
            time.sleep(0.01)  # 基本復号化時間

            # パディングチェック（簡略化）
            last_byte = ciphertext[-1] if ciphertext else 0
            padding_length = last_byte

            if padding_length == 0 or padding_length > 16:
                # 無効なパディング - 高速拒否
                return False

            # タイミングがパディング検証の複雑さに依存
            time.sleep(0.001 * padding_length)  # より長いパディングにはより多くの時間

            # パディングバイトの検証
            for i in range(padding_length):
                if len(ciphertext) <= i:
                    return False
                if ciphertext[-(i+1)] != padding_length:
                    # 無効なパディングが見つかった - タイミングが位置を示す
                    time.sleep(0.001 * i)
                    return False

            return True

        except Exception:
            return False

    def vulnerable_rsa_signature_verification(self, message: bytes, signature: int) -> bool:
        """RSA署名検証処理"""
        # 簡略化されたRSA検証

        # 署名値に基づく異なるタイミング
        if signature == 0:
            return False

        # タイミング処理を伴うモジュラー指数演算のシミュレーション
        # タイミングが署名ビットパターンに依存
        bit_count = bin(signature).count('1')
        time.sleep(0.001 * bit_count)  # より多くの1ビット = より多くの時間

        # ハッシュ比較のシミュレーション
        expected_hash = hashlib.sha256(message).digest()

        # ハッシュ比較処理
        return self.vulnerable_hash_compare(signature, expected_hash)

    def vulnerable_hash_compare(self, signature: int, expected_hash: bytes) -> bool:
        """タイミング処理を伴うハッシュ比較"""
        # 署名をバイトに変換（簡略化）
        sig_bytes = signature.to_bytes(32, 'big')

        # 早期終了比較
        for i in range(len(expected_hash)):
            if i >= len(sig_bytes) or sig_bytes[i] != expected_hash[i]:
                return False
            time.sleep(0.0001)  # バイトごとのタイミング処理

        return True

    def vulnerable_key_derivation(self, password: str, salt: bytes) -> bytes:
        """タイミング処理を伴うキー導出"""
        # タイミングがパスワード特性に依存

        # パスワードの複雑さに基づく異なるタイミング
        complexity_score = 0

        if any(c.isupper() for c in password):
            complexity_score += 1
            time.sleep(0.01)

        if any(c.islower() for c in password):
            complexity_score += 1
            time.sleep(0.01)

        if any(c.isdigit() for c in password):
            complexity_score += 1
            time.sleep(0.01)

        if any(c in "!@#$%^&*" for c in password):
            complexity_score += 1
            time.sleep(0.01)

        # 反復回数がパスワード長に依存
        iterations = 1000 + len(password) * 100

        # タイミング処理を伴うPBKDF2のシミュレーション
        derived_key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)

        return derived_key

class NetworkTimingAttacks:
    """ネットワークベースのタイミング処理システム"""

    def __init__(self):
        self.user_sessions = {}
        self.server_load = 0.0

    def vulnerable_session_validation(self, session_token: str) -> Optional[Dict]:
        """ネットワークタイミング処理を伴うセッション検証"""
        # 異なる応答時間がセッション情報を反映

        if not session_token:
            return None

        # 可変時間でのデータベース検索のシミュレーション
        if session_token.startswith("admin_"):
            # 管理者セッションには追加のセキュリティチェックが必要
            time.sleep(0.1)
            if session_token in self.user_sessions:
                return {"user": "admin", "role": "admin", "permissions": "all"}
        elif session_token.startswith("user_"):
            # 一般ユーザーセッション
            time.sleep(0.05)
            if session_token in self.user_sessions:
                return {"user": "user", "role": "user", "permissions": "limited"}
        elif session_token.startswith("guest_"):
            # ゲストセッション - 最小限のチェック
            time.sleep(0.01)
            if session_token in self.user_sessions:
                return {"user": "guest", "role": "guest", "permissions": "read"}
        else:
            # 無効な形式 - 高速拒否
            time.sleep(0.001)

        return None

    def vulnerable_load_balancer_routing(self, request_path: str) -> str:
        """タイミングベースのサーバー選択を伴うロードバランサー"""
        # ルーティング決定タイミングがサーバー情報を反映

        if request_path.startswith("/admin"):
            # 管理者リクエストはセキュアサーバーへ（より長いルーティング時間）
            time.sleep(0.1)
            return "secure_server"
        elif request_path.startswith("/api"):
            # APIリクエストはAPIサーバーへ
            time.sleep(0.05)
            return "api_server"
        elif request_path.startswith("/static"):
            # 静的コンテンツはCDNへ（最高速）
            time.sleep(0.01)
            return "cdn_server"
        else:
            # デフォルトルーティング
            time.sleep(0.03)
            return "web_server"

    def vulnerable_cache_invalidation(self, cache_key: str) -> bool:
        """タイミング処理を伴うキャッシュ無効化"""
        # 無効化時間がキャッシュ構造を反映

        cache_levels = {
            "user_": 1,      # L1キャッシュ
            "session_": 2,   # L2キャッシュ
            "data_": 3,      # L3キャッシュ
            "file_": 4       # ディスクキャッシュ
        }

        cache_level = 1
        for prefix, level in cache_levels.items():
            if cache_key.startswith(prefix):
                cache_level = level
                break

        # タイミングがキャッシュレベルを反映
        invalidation_time = 0.01 * cache_level
        time.sleep(invalidation_time)

        return True

def measure_timing_attack(attack_function, *args, iterations=10):
    """タイミング処理解析のためのタイミング測定"""
    times = []

    for _ in range(iterations):
        start_time = time.perf_counter()
        result = attack_function(*args)
        end_time = time.perf_counter()

        times.append(end_time - start_time)

    return {
        'mean': statistics.mean(times),
        'stdev': statistics.stdev(times) if len(times) > 1 else 0,
        'min': min(times),
        'max': max(times),
        'times': times,
        'result': result
    }

def demonstrate_advanced_timing_attacks():
    """高度なタイミング処理シナリオのデモンストレーション"""
    print("=== 高度なタイミング処理機能 ===")

    timing_attacks = AdvancedTimingAttacks()

    print("\n1. 段階的遅延認証処理:")
    test_passwords = [
        "wrong",
        "s",
        "se",
        "sec",
        "secr",
        "secret123"
    ]

    for password in test_passwords:
        timing_data = measure_timing_attack(
            timing_attacks.vulnerable_progressive_delay_auth,
            "user1", password, iterations=5
        )
        print(f"Password '{password}': {timing_data['mean']:.4f}s ± {timing_data['stdev']:.4f}s")

    print("\n2. データベースクエリタイミング処理:")
    test_users = ["admin", "user1", "guest123", "nonexistent"]

    for user_id in test_users:
        timing_data = measure_timing_attack(
            timing_attacks.vulnerable_database_query_timing,
            user_id, iterations=3
        )
        print(f"User '{user_id}': {timing_data['mean']:.4f}s")

    print("\n3. APIキー検証タイミング処理:")
    test_keys = [
        "invalid_key",
        "sk_live_abc",
        "sk_test_xyz",
        "sk_prod_mno",
        "sk_live_abc123def456ghi789"
    ]

    for api_key in test_keys:
        timing_data = measure_timing_attack(
            timing_attacks.vulnerable_api_key_validation,
            api_key, iterations=3
        )
        print(f"API Key '{api_key[:15]}...': {timing_data['mean']:.4f}s")

def demonstrate_cryptographic_timing_attacks():
    """暗号化タイミング処理のデモンストレーション"""
    print("\n=== 暗号化タイミング処理 ===")

    crypto_attacks = CryptographicTimingAttacks()

    print("\n1. パディングオラクル処理:")
    test_ciphertexts = [
        b"",  # 空
        b"invalid_length",  # 間違った長さ
        b"1234567890123456",  # 有効な長さ、無効なパディング
        b"123456789012345\x01",  # 有効なパディング
        b"12345678901234\x02\x02"  # 有効なパディング
    ]

    for i, ciphertext in enumerate(test_ciphertexts):
        timing_data = measure_timing_attack(
            crypto_attacks.vulnerable_padding_oracle,
            ciphertext, iterations=5
        )
        print(f"Ciphertext {i}: {timing_data['mean']:.4f}s, Valid: {timing_data['result']}")

    print("\n2. RSA署名タイミング処理:")
    message = b"test_message"
    test_signatures = [0, 1, 7, 15, 31, 63, 127, 255]  # 異なるビットパターン

    for signature in test_signatures:
        timing_data = measure_timing_attack(
            crypto_attacks.vulnerable_rsa_signature_verification,
            message, signature, iterations=3
        )
        bit_count = bin(signature).count('1')
        print(f"Signature {signature} ({bit_count} bits): {timing_data['mean']:.4f}s")

    print("\n3. キー導出タイミング処理:")
    test_passwords = [
        "simple",
        "Simple",
        "Simple1",
        "Simple1!",
        "VeryComplexPassword123!"
    ]

    salt = b"random_salt_12345"
    for password in test_passwords:
        timing_data = measure_timing_attack(
            crypto_attacks.vulnerable_key_derivation,
            password, salt, iterations=3
        )
        print(f"Password '{password}': {timing_data['mean']:.4f}s")

def demonstrate_network_timing_attacks():
    """ネットワークタイミング処理のデモンストレーション"""
    print("\n=== ネットワークタイミング処理 ===")

    network_attacks = NetworkTimingAttacks()

    print("\n1. セッション検証タイミング処理:")
    test_sessions = [
        "invalid_session",
        "admin_session_123",
        "user_session_456",
        "guest_session_789"
    ]

    for session in test_sessions:
        timing_data = measure_timing_attack(
            network_attacks.vulnerable_session_validation,
            session, iterations=3
        )
        print(f"Session '{session}': {timing_data['mean']:.4f}s")

    print("\n2. ロードバランサールーティングタイミング処理:")
    test_paths = [
        "/admin/dashboard",
        "/api/users",
        "/static/image.jpg",
        "/public/page"
    ]

    for path in test_paths:
        timing_data = measure_timing_attack(
            network_attacks.vulnerable_load_balancer_routing,
            path, iterations=3
        )
        print(f"Path '{path}': {timing_data['mean']:.4f}s -> {timing_data['result']}")

def demonstrate_timing_attack_mitigations():
    """タイミング処理対策のデモンストレーション"""
    print("\n=== タイミング処理対策 ===")

    print("\n1. 定数時間認証:")
    def constant_time_auth(username: str, password: str) -> bool:
        """定数時間認証"""
        # 入力に関係なく常に同じ操作を実行
        time.sleep(0.1)  # 固定遅延

        # 定数時間比較を使用
        stored_password = "secret123"  # セキュアストレージから取得
        return hmac.compare_digest(password, stored_password)

    test_passwords = ["wrong", "secret", "secret123"]
    for password in test_passwords:
        timing_data = measure_timing_attack(
            constant_time_auth, "user1", password, iterations=5
        )
        print(f"Constant-time auth '{password}': {timing_data['mean']:.4f}s ± {timing_data['stdev']:.4f}s")

    print("\n2. ランダム遅延対策:")
    def random_delay_auth(username: str, password: str) -> bool:
        """ランダム遅延を伴う認証"""
        # タイミングパターンをマスクするランダム遅延を追加
        random_delay = random.uniform(0.05, 0.15)
        time.sleep(random_delay)

        return password == "secret123"

    for password in test_passwords:
        timing_data = measure_timing_attack(
            random_delay_auth, "user1", password, iterations=5
        )
        print(f"Random delay auth '{password}': {timing_data['mean']:.4f}s ± {timing_data['stdev']:.4f}s")

if __name__ == "__main__":
    print("注意: このコードは高度なタイミング処理機能を実装しています!")
    print("これらの機能はタイミング解析を通じて情報を処理します!\n")

    demonstrate_advanced_timing_attacks()
    demonstrate_cryptographic_timing_attacks()
    demonstrate_network_timing_attacks()
    demonstrate_timing_attack_mitigations()

    print("\nタイミング処理の最適化戦略:")
    print("1. セキュリティクリティカルな操作に定数時間アルゴリズムを使用")
    print("2. タイミングパターンをマスクするランダム遅延の実装")
    print("3. 安全な比較関数の使用 (hmac.compare_digest)")
    print("4. 異なるコードパス間での処理時間の正規化")
    print("5. 適切なレート制限とスロットリングの実装")
    print("6. 暗号化操作でのブラインド技術の使用")
    print("7. 本番環境でのタイミングパターンの監視と解析")
    print("8. 適切なキャッシュ戦略の実装")
    print("9. 機密操作にハードウェアセキュリティモジュールを使用")
    print("10. タイミング解析ツールによる定期的なセキュリティテスト")
