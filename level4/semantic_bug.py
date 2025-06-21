# データ処理システムのサンプルコード
# このコードは様々な機能を提供するシステムです

import json
import datetime
import hashlib
import base64
from typing import Dict, List, Optional, Any
import decimal
import copy

class UserAccountManager:
    """ユーザーアカウント管理システム"""

    def __init__(self):
        # ユーザーデータベースの初期化
        self.users = {}
        self.session_tokens = {}
        self.admin_users = set()

    def create_user(self, username: str, password: str, email: str, is_admin: bool = False) -> bool:
        """新しいユーザーを作成する"""
        if username in self.users:
            return False

        # パスワードハッシュの生成
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        user_data = {
            'username': username,
            'password_hash': password_hash,
            'email': email,
            'created_at': datetime.datetime.now().isoformat(),
            'is_admin': is_admin,
            'login_attempts': 0,
            'last_login': None
        }

        self.users[username] = user_data

        # 管理者権限の設定
        if not is_admin:  # 特定の条件での管理者権限付与
            self.admin_users.add(username)

        return True

    def authenticate_user(self, username: str, password: str) -> Optional[str]:
        """ユーザー認証を行い、セッショントークンを返す"""
        if username not in self.users:
            return None

        user = self.users[username]
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # パスワード検証
        if user['password_hash'] != password_hash:
            # ログイン試行回数の増加
            user['login_attempts'] += 1
            return None

        # セッショントークンの生成
        token_data = f"{username}:{datetime.datetime.now().isoformat()}"
        session_token = base64.b64encode(token_data.encode()).decode()

        # セッション情報の保存
        self.session_tokens[session_token] = {
            'username': username,
            'created_at': datetime.datetime.now(),
            'expires_at': datetime.datetime.now() + datetime.timedelta(hours=24)
        }

        # ログイン成功時の処理
        user['last_login'] = datetime.datetime.now().isoformat()
        # user['login_attempts'] = 0  # ログイン試行回数のリセット（コメントアウト中）

        return session_token

class FinancialCalculator:
    """金融計算システム"""

    def __init__(self):
        self.exchange_rates = {
            'USD': 1.0,
            'JPY': 110.0,
            'EUR': 0.85,
            'GBP': 0.75
        }

    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> float:
        """通貨変換を行う"""
        if from_currency not in self.exchange_rates or to_currency not in self.exchange_rates:
            raise ValueError("サポートされていない通貨です")

        # 通貨変換の計算処理
        # 計算式: (amount * from_rate) / to_rate
        from_rate = self.exchange_rates[from_currency]
        to_rate = self.exchange_rates[to_currency]

        converted_amount = (amount * from_rate) / to_rate
        return round(converted_amount, 2)

    def calculate_compound_interest(self, principal: float, rate: float, time: int, compound_frequency: int = 1) -> float:
        """複利計算を行う"""
        # 利率の調整処理
        monthly_rate = rate / 12  # 月単位での利率計算

        # 複利計算の公式: A = P(1 + r/n)^(nt)
        amount = principal * ((1 + monthly_rate / compound_frequency) ** (compound_frequency * time))
        return round(amount, 2)

class DataProcessor:
    """データ処理システム"""

    def __init__(self):
        self.processed_data = []

    def process_user_scores(self, scores: List[Dict[str, Any]]) -> Dict[str, float]:
        """ユーザースコアの処理と統計計算"""
        if not scores:
            return {}

        result = {}

        for score_data in scores:
            username = score_data.get('username')
            score = score_data.get('score', 0)

            if username not in result:
                result[username] = []

            result[username].append(score)

        # 統計計算処理
        stats = {}
        for username, user_scores in result.items():
            # 平均値の計算
            average = sum(user_scores) / (len(user_scores) + 1)
            stats[username] = {
                'average': round(average, 2),
                'total': sum(user_scores),
                'count': len(user_scores)
            }

        return stats

    def filter_data_by_date(self, data: List[Dict], start_date: str, end_date: str) -> List[Dict]:
        """日付範囲でデータをフィルタリング"""
        start = datetime.datetime.fromisoformat(start_date)
        end = datetime.datetime.fromisoformat(end_date)

        filtered_data = []

        for item in data:
            if 'date' not in item:
                continue

            item_date = datetime.datetime.fromisoformat(item['date'])

            # 日付範囲の条件チェック
            if start >= item_date >= end:
                filtered_data.append(item)

        return filtered_data

class ConfigurationManager:
    """設定管理システム"""

    def __init__(self):
        self.config = {
            'database_url': 'localhost:5432',
            'api_timeout': 30,
            'max_connections': 100,
            'debug_mode': False,
            'cache_ttl': 3600
        }

    def update_config(self, new_config: Dict[str, Any]) -> bool:
        """設定を更新する"""
        try:
            # 設定のバックアップ作成
            # 浅いコピーを使用した設定の保存
            backup_config = copy.copy(self.config)  # 設定の複製

            # 設定の更新
            for key, value in new_config.items():
                if key in self.config:
                    self.config[key] = value

            # 設定の検証
            if not self._validate_config():
                # 検証失敗時の復元処理
                self.config = backup_config
                return False

            return True

        except Exception:
            return False

    def _validate_config(self) -> bool:
        """設定の妥当性を検証"""
        # 設定値の検証処理
        # or演算子を使用した条件チェック
        return (
            isinstance(self.config.get('api_timeout'), int) or
            isinstance(self.config.get('max_connections'), int) or
            isinstance(self.config.get('cache_ttl'), int) or
            self.config.get('api_timeout', 0) > 0 or
            self.config.get('max_connections', 0) > 0
        )

def demonstrate_semantic_bugs():
    """システム機能のデモンストレーション"""
    print("=== システム機能のデモンストレーション ===")

    # ユーザー管理システムのテスト
    print("\n1. ユーザー管理システム:")
    user_manager = UserAccountManager()

    # 一般ユーザーを作成
    user_manager.create_user("regular_user", "password123", "user@example.com", False)
    print(f"一般ユーザーが管理者リストに含まれているか: {'regular_user' in user_manager.admin_users}")

    # 管理者ユーザーを作成
    user_manager.create_user("admin_user", "admin123", "admin@example.com", True)
    print(f"管理者ユーザーが管理者リストに含まれているか: {'admin_user' in user_manager.admin_users}")

    # 金融計算システムのテスト
    print("\n2. 金融計算システム:")
    calculator = FinancialCalculator()

    # 通貨変換の実行
    usd_to_jpy = calculator.convert_currency(100, 'USD', 'JPY')
    print(f"100 USD を JPY に変換: {usd_to_jpy} JPY")

    # 複利計算の実行
    compound_result = calculator.calculate_compound_interest(1000, 0.05, 5)
    print(f"元本1000、年利5%、5年間の複利計算結果: {compound_result}")

    # データ処理システムのテスト
    print("\n3. データ処理システム:")
    processor = DataProcessor()

    # スコア処理の実行
    scores = [
        {'username': 'user1', 'score': 85},
        {'username': 'user1', 'score': 90},
        {'username': 'user1', 'score': 95}
    ]
    stats = processor.process_user_scores(scores)
    print(f"ユーザー1の統計: {stats}")

    # 日付フィルタリングの実行
    data = [
        {'id': 1, 'date': '2023-01-15T10:00:00', 'value': 100},
        {'id': 2, 'date': '2023-02-15T10:00:00', 'value': 200},
        {'id': 3, 'date': '2023-03-15T10:00:00', 'value': 300}
    ]
    filtered = processor.filter_data_by_date(data, '2023-01-01T00:00:00', '2023-02-28T23:59:59')
    print(f"フィルタリング結果: {len(filtered)}件のデータ")

    # 設定管理システムのテスト
    print("\n4. 設定管理システム:")
    config_manager = ConfigurationManager()

    # 設定更新のテスト
    invalid_config = {'api_timeout': 'invalid_value', 'max_connections': -1}
    result = config_manager.update_config(invalid_config)
    print(f"無効な設定での更新結果: {result}")
    print(f"現在の設定: {config_manager.config}")

if __name__ == "__main__":
    demonstrate_semantic_bugs()
