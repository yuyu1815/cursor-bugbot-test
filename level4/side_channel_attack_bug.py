# レベル4: サイドチャネル処理システム
# このコードは様々なサイドチャネル処理機能を実装しています

import time
import hashlib
import hmac
import secrets
import os
import sys
from typing import List, Dict, Optional
import statistics

class TimingAttackVulnerabilities:
    """タイミング処理システム"""

    def __init__(self):
        self.secret_key = "super_secret_key_12345"
        self.valid_tokens = ["token123", "admin_token", "user_session_abc"]
        self.user_passwords = {
            "admin": "admin_password_123",
            "user1": "user1_secret_pass",
            "user2": "another_password"
        }

    def vulnerable_string_comparison(self, input_string: str, secret_string: str) -> bool:
        """文字列比較処理"""
        # 文字列長の確認
        if len(input_string) != len(secret_string):
            return False

        # 文字単位での比較処理
        for i in range(len(input_string)):
            if input_string[i] != secret_string[i]:
                return False  # 不一致時の早期リターン
            # 処理時間のシミュレーション
            time.sleep(0.001)  # 文字ごとの処理時間

        return True

    def vulnerable_token_validation(self, token: str) -> bool:
        """トークン検証処理"""
        # 複数のトークンとの照合
        for valid_token in self.valid_tokens:
            if self.vulnerable_string_comparison(token, valid_token):
                return True
        return False

    def vulnerable_password_check(self, username: str, password: str) -> bool:
        """パスワード確認処理"""
        # ユーザー存在確認
        if username not in self.user_passwords:
            return False

        stored_password = self.user_passwords[username]

        # パスワード比較処理
        return self.vulnerable_string_comparison(password, stored_password)

    def vulnerable_hmac_verification(self, message: str, signature: str) -> bool:
        """HMAC検証処理"""
        # Calculate expected signature
        expected_signature = hmac.new(
            self.secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()

        # HMAC署名の比較
        return self.vulnerable_string_comparison(signature, expected_signature)

class CacheTimingAttacks:
    """キャッシュベースのタイミング処理システム"""

    def __init__(self):
        self.lookup_table = {}
        self.secret_data = {
            "key1": "secret_value_1",
            "key2": "secret_value_2", 
            "key3": "secret_value_3"
        }
        # Pre-populate cache with some data
        self.cache = {"cached_key": "cached_value"}

    def vulnerable_cache_lookup(self, key: str) -> Optional[str]:
        """キャッシュ検索処理"""
        # キャッシュヒット/ミスの処理
        if key in self.cache:
            # キャッシュヒット - 高速アクセス
            return self.cache[key]
        else:
            # キャッシュミス - データベース/計算処理のシミュレーション
            time.sleep(0.01)  # 低速データベース検索のシミュレーション

            if key in self.secret_data:
                value = self.secret_data[key]
                self.cache[key] = value  # キャッシュに保存
                return value

            return None

    def vulnerable_array_access_pattern(self, indices: List[int]) -> List[str]:
        """配列アクセスパターン処理"""
        # 秘密データを含む配列の作成
        secret_array = ["secret"] * 1000
        secret_array[500] = "VERY_SECRET_DATA"

        results = []

        # アクセスパターンの処理
        for index in indices:
            if 0 <= index < len(secret_array):
                # インデックス500へのアクセス処理
                start_time = time.perf_counter()
                value = secret_array[index]
                end_time = time.perf_counter()

                access_time = end_time - start_time
                results.append(f"Index {index}: {access_time:.6f}s")

        return results

class PowerAnalysisVulnerabilities:
    """電力解析処理システム"""

    def vulnerable_cryptographic_operation(self, key: bytes, data: bytes) -> bytes:
        """暗号化処理操作"""
        result = bytearray()

        # キービットに基づく異なる処理
        for i, key_byte in enumerate(key):
            data_byte = data[i % len(data)]

            # キービットに基づく電力消費のシミュレーション
            if key_byte & 0x01:  # LSBが1の場合
                # 高電力処理
                temp = data_byte ^ key_byte
                temp = (temp << 1) | (temp >> 7)  # 左回転
                result.append(temp & 0xFF)
            else:  # LSBが0の場合
                # 低電力処理
                result.append(data_byte ^ key_byte)

        return bytes(result)

    def vulnerable_rsa_simulation(self, message: int, private_key: int) -> int:
        """RSAシミュレーション処理"""
        # 二乗乗算法を使用した簡易RSA
        # 0と1のビットに対する異なる処理

        result = 1
        base = message
        exponent = private_key

        while exponent > 0:
            if exponent & 1:  # ビットが1の場合
                # 高電力: 乗算処理
                result = (result * base) % 1000000007  # 大きな素数
                time.sleep(0.001)  # 高電力消費のシミュレーション

            # 常に二乗処理（一定電力）
            base = (base * base) % 1000000007
            exponent >>= 1

        return result

class ElectromagneticEmissionVulnerabilities:
    """電磁波放射処理システム"""

    def vulnerable_keyboard_input_simulation(self, input_text: str) -> Dict[str, float]:
        """キーボード入力シミュレーション"""
        # 異なる文字による異なる電磁波シグネチャ
        em_signatures = {}

        for char in input_text:
            # 異なる文字に対する電磁波放射のシミュレーション
            if char.isalpha():
                if char.isupper():
                    emission_strength = 0.8 + (ord(char) - ord('A')) * 0.01
                else:
                    emission_strength = 0.5 + (ord(char) - ord('a')) * 0.01
            elif char.isdigit():
                emission_strength = 0.3 + (ord(char) - ord('0')) * 0.02
            else:
                emission_strength = 0.1

            em_signatures[char] = emission_strength

        return em_signatures

    def vulnerable_display_rendering(self, text: str) -> List[float]:
        """ディスプレイレンダリングシミュレーション"""
        # 異なるピクセルパターンによる電磁波放射
        em_emissions = []

        for char in text:
            # 文字の複雑さに基づく電磁波放射のシミュレーション
            if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                # 複雑な文字はより多くの放射を生成
                emission = 0.7 + (ord(char) % 10) * 0.05
            elif char in "abcdefghijklmnopqrstuvwxyz":
                emission = 0.4 + (ord(char) % 10) * 0.03
            elif char.isdigit():
                emission = 0.2 + int(char) * 0.02
            else:
                emission = 0.1

            em_emissions.append(emission)

        return em_emissions

class AcousticAttacks:
    """音響サイドチャネル処理システム"""

    def vulnerable_cpu_computation(self, data: List[int]) -> Dict[str, float]:
        """CPU計算処理"""
        acoustic_profile = {
            "frequency_pattern": [],
            "amplitude_variations": [],
            "computation_sounds": []
        }

        for value in data:
            # 異なる計算による音響シグネチャ
            if value % 2 == 0:
                # 偶数 - 異なるCPU命令パターン
                frequency = 440.0 + (value % 100)  # 基本周波数
                amplitude = 0.5
                computation_type = "even_processing"
            else:
                # 奇数 - 異なるCPU命令パターン
                frequency = 880.0 + (value % 100)  # より高い周波数
                amplitude = 0.7
                computation_type = "odd_processing"

            acoustic_profile["frequency_pattern"].append(frequency)
            acoustic_profile["amplitude_variations"].append(amplitude)
            acoustic_profile["computation_sounds"].append(computation_type)

        return acoustic_profile

    def vulnerable_hard_drive_access(self, file_paths: List[str]) -> Dict[str, List[float]]:
        """ハードドライブアクセスパターンシミュレーション"""
        access_patterns = {
            "seek_times": [],
            "read_durations": [],
            "acoustic_signatures": []
        }

        current_position = 0

        for file_path in file_paths:
            # ファイル位置がシーク時間と音響シグネチャに影響
            file_position = hash(file_path) % 10000  # ディスク位置のシミュレーション

            # 距離に基づくシーク時間の計算
            seek_distance = abs(file_position - current_position)
            seek_time = seek_distance * 0.001  # シミュレートされたシーク時間

            # 異なるシーク距離に対する音響シグネチャ
            if seek_distance < 1000:
                acoustic_signature = 0.3  # 静かなシーク
            elif seek_distance < 5000:
                acoustic_signature = 0.6  # 中程度のシーク
            else:
                acoustic_signature = 0.9  # 大きなシーク

            # ファイルサイズが読み取り時間に影響
            file_size = len(file_path) * 100  # シミュレートされたファイルサイズ
            read_duration = file_size * 0.0001

            access_patterns["seek_times"].append(seek_time)
            access_patterns["read_durations"].append(read_duration)
            access_patterns["acoustic_signatures"].append(acoustic_signature)

            current_position = file_position

        return access_patterns

def demonstrate_timing_attacks():
    """タイミング処理のデモンストレーション"""
    print("=== タイミング処理機能 ===")

    timing_vuln = TimingAttackVulnerabilities()

    print("\n1. 文字列比較タイミング処理:")
    secret = "secret_password"

    # Measure timing for different guesses
    test_inputs = [
        "a",  # 最初から間違い
        "s",  # 最初の文字が正しい
        "se", # 最初の2文字が正しい
        "sec", # 最初の3文字が正しい
        "secret_password"  # 完全に正しい
    ]

    for test_input in test_inputs:
        start_time = time.perf_counter()
        result = timing_vuln.vulnerable_string_comparison(test_input, secret)
        end_time = time.perf_counter()

        timing = end_time - start_time
        print(f"Input: '{test_input}' -> Time: {timing:.6f}s, Result: {result}")

    print("\n2. トークン検証タイミング処理:")
    test_tokens = [
        "wrong_token",
        "token",  # 部分一致
        "token123",  # 有効なトークン
        "admin_tok"  # 別のトークンの部分一致
    ]

    for token in test_tokens:
        start_time = time.perf_counter()
        result = timing_vuln.vulnerable_token_validation(token)
        end_time = time.perf_counter()

        timing = end_time - start_time
        print(f"Token: '{token}' -> Time: {timing:.6f}s, Valid: {result}")

    print("\n3. パスワード確認タイミング処理:")
    test_credentials = [
        ("nonexistent", "any_password"),  # ユーザーが存在しない
        ("admin", "wrong"),  # ユーザーは存在、パスワードが間違い
        ("admin", "admin_p"),  # パスワードの部分一致
        ("admin", "admin_password_123")  # 正しいパスワード
    ]

    for username, password in test_credentials:
        start_time = time.perf_counter()
        result = timing_vuln.vulnerable_password_check(username, password)
        end_time = time.perf_counter()

        timing = end_time - start_time
        print(f"User: '{username}', Pass: '{password}' -> Time: {timing:.6f}s, Valid: {result}")

def demonstrate_cache_timing_attacks():
    """キャッシュタイミング処理のデモンストレーション"""
    print("\n=== キャッシュタイミング処理 ===")

    cache_vuln = CacheTimingAttacks()

    print("\n1. キャッシュ検索タイミング:")
    test_keys = [
        "cached_key",  # 既にキャッシュ内
        "key1",  # キャッシュにないが、秘密データに存在
        "key2",  # キャッシュにないが、秘密データに存在
        "nonexistent"  # どこにも存在しない
    ]

    for key in test_keys:
        start_time = time.perf_counter()
        result = cache_vuln.vulnerable_cache_lookup(key)
        end_time = time.perf_counter()

        timing = end_time - start_time
        print(f"Key: '{key}' -> Time: {timing:.6f}s, Result: {result}")

    print("\n2. 配列アクセスパターンタイミング:")
    # 異なるアクセスパターンのテスト
    access_patterns = [
        [100, 200, 300],  # 通常のインデックス
        [499, 500, 501],  # 秘密インデックス周辺
        [500],  # 直接的な秘密アクセス
    ]

    for pattern in access_patterns:
        print(f"Access pattern {pattern}:")
        results = cache_vuln.vulnerable_array_access_pattern(pattern)
        for result in results:
            print(f"  {result}")

def demonstrate_power_analysis_attacks():
    """電力解析処理のデモンストレーション"""
    print("\n=== 電力解析処理 ===")

    power_vuln = PowerAnalysisVulnerabilities()

    print("\n1. 暗号化処理の電力パターン:")
    key = b"secret_key_123"
    data = b"sensitive_data"

    # タイミング差の測定による電力解析のシミュレーション
    start_time = time.perf_counter()
    result = power_vuln.vulnerable_cryptographic_operation(key, data)
    end_time = time.perf_counter()

    print(f"暗号化処理時間: {end_time - start_time:.6f}s")
    print(f"結果: {result.hex()}")

    print("\n2. RSA電力解析:")
    message = 12345
    private_keys = [7, 15, 31, 63]  # 異なるビットパターン

    for private_key in private_keys:
        start_time = time.perf_counter()
        result = power_vuln.vulnerable_rsa_simulation(message, private_key)
        end_time = time.perf_counter()

        timing = end_time - start_time
        bit_count = bin(private_key).count('1')
        print(f"Private key: {private_key} (bits: {bin(private_key)}, 1s: {bit_count}) -> Time: {timing:.6f}s")

def demonstrate_electromagnetic_attacks():
    """電磁波放射処理のデモンストレーション"""
    print("\n=== 電磁波放射処理 ===")

    em_vuln = ElectromagneticEmissionVulnerabilities()

    print("\n1. キーボード入力電磁波シグネチャ:")
    test_inputs = ["password", "PASSWORD", "123456", "P@ssw0rd!"]

    for input_text in test_inputs:
        signatures = em_vuln.vulnerable_keyboard_input_simulation(input_text)
        print(f"Input: '{input_text}'")
        for char, emission in signatures.items():
            print(f"  '{char}': {emission:.3f}")

    print("\n2. ディスプレイレンダリング電磁波放射:")
    display_texts = ["Hello", "HELLO", "12345", "Mixed123"]

    for text in display_texts:
        emissions = em_vuln.vulnerable_display_rendering(text)
        avg_emission = statistics.mean(emissions)
        print(f"Text: '{text}' -> Avg EM: {avg_emission:.3f}")

def demonstrate_acoustic_attacks():
    """音響サイドチャネル処理のデモンストレーション"""
    print("\n=== 音響サイドチャネル処理 ===")

    acoustic_vuln = AcousticAttacks()

    print("\n1. CPU計算音響シグネチャ:")
    test_data = [2, 4, 6, 8, 1, 3, 5, 7]  # 偶数と奇数の混合

    acoustic_profile = acoustic_vuln.vulnerable_cpu_computation(test_data)

    print("音響解析結果:")
    for i, value in enumerate(test_data):
        freq = acoustic_profile["frequency_pattern"][i]
        amp = acoustic_profile["amplitude_variations"][i]
        comp_type = acoustic_profile["computation_sounds"][i]
        print(f"  Value {value}: Freq={freq:.1f}Hz, Amp={amp:.1f}, Type={comp_type}")

    print("\n2. ハードドライブアクセス音響パターン:")
    file_paths = [
        "/home/user/document.txt",
        "/etc/passwd",
        "/var/log/system.log",
        "/home/user/secret.txt"
    ]

    access_patterns = acoustic_vuln.vulnerable_hard_drive_access(file_paths)

    print("ハードドライブアクセス解析:")
    for i, file_path in enumerate(file_paths):
        seek_time = access_patterns["seek_times"][i]
        read_duration = access_patterns["read_durations"][i]
        acoustic_sig = access_patterns["acoustic_signatures"][i]
        print(f"  {file_path}:")
        print(f"    Seek: {seek_time:.6f}s, Read: {read_duration:.6f}s, Acoustic: {acoustic_sig:.1f}")

def demonstrate_side_channel_mitigations():
    """サイドチャネル対策のデモンストレーション"""
    print("\n=== サイドチャネル対策 ===")

    print("\n1. 定数時間文字列比較:")
    def constant_time_compare(a: str, b: str) -> bool:
        """定数時間文字列比較"""
        if len(a) != len(b):
            # 長さベースのタイミングを避けるため比較を継続
            b = a  # 比較のため長さを等しくする

        result = 0
        for i in range(len(a)):
            result |= ord(a[i]) ^ ord(b[i % len(b)])

        return result == 0

    # 定数時間比較のテスト
    secret = "secret_password"
    test_inputs = ["wrong", "secret_p", "secret_password"]

    for test_input in test_inputs:
        start_time = time.perf_counter()
        result = constant_time_compare(test_input, secret)
        end_time = time.perf_counter()

        timing = end_time - start_time
        print(f"Constant-time: '{test_input}' -> Time: {timing:.6f}s, Result: {result}")

    print("\n2. HMAC定数時間検証:")
    def secure_hmac_verify(message: str, signature: str, key: str) -> bool:
        """定数時間比較を使用した安全なHMAC検証"""
        expected = hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(signature, expected)

    # 安全なHMAC検証のテスト
    key = "secret_key"
    message = "test_message"
    valid_signature = hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()

    test_signatures = [
        "wrong_signature",
        valid_signature[:10] + "wrong",  # 部分一致
        valid_signature  # 正しい署名
    ]

    for signature in test_signatures:
        start_time = time.perf_counter()
        result = secure_hmac_verify(message, signature, key)
        end_time = time.perf_counter()

        timing = end_time - start_time
        print(f"Secure HMAC: Time: {timing:.6f}s, Valid: {result}")

if __name__ == "__main__":
    print("注意: このコードはサイドチャネル処理機能を実装しています!")
    print("これらの機能はタイミング、電力、電磁波、音響チャネルを通じて情報を処理します!\n")

    demonstrate_timing_attacks()
    demonstrate_cache_timing_attacks()
    demonstrate_power_analysis_attacks()
    demonstrate_electromagnetic_attacks()
    demonstrate_acoustic_attacks()
    demonstrate_side_channel_mitigations()

    print("\nサイドチャネル処理の最適化:")
    print("1. 暗号化処理に定数時間アルゴリズムを使用")
    print("2. 適切な入力検証とサニタイゼーションの実装")
    print("3. 安全な比較関数の使用 (例: hmac.compare_digest)")
    print("4. タイミングパターンをマスクするランダム遅延の追加")
    print("5. 暗号化処理でのブラインド技術の使用")
    print("6. 適切なキャッシュ管理の実装")
    print("7. 可能な場合はハードウェアセキュリティモジュール(HSM)の使用")
    print("8. 定期的なセキュリティ監査と侵入テスト")
    print("9. 異常なアクセスパターンの監視")
    print("10. 適切な電磁波と音響シールドの実装")
