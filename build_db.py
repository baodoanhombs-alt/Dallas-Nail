import sqlite3
import json
import os

DB_PATH = "brain.db"
WAITLIST_PATH = "waitlist.json"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Bảng products
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            stock INTEGER DEFAULT 0
        )
    ''')

    # 2. Bảng customers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT UNIQUE,
            email TEXT,
            zalo TEXT,
            registered_date TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')
    
    # Migration: Add email column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE customers ADD COLUMN email TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # 3. Bảng orders
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            product_id INTEGER,
            amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            purchase_date TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')
    
    # Thêm sản phẩm mặc định nếu chưa có
    cursor.execute("SELECT COUNT(*) as cnt FROM products")
    if cursor.fetchone()['cnt'] == 0:
        products = [
            ("Dịch vụ Nail chuyên sâu", 10, "Chăm sóc móng tay chuyên sâu với sơn gel bền màu", 100),
            ("Vẽ Art độc quyền", 5, "Thiết kế nail art theo yêu cầu", 100),
            ("Pedicure Premium", 15, "Chăm sóc chân cao cấp với massage thư giãn", 100),
            ("Ebook: Chăm sóc móng tại nhà", 2, "Ebook hướng dẫn chăm sóc móng tay toàn diện", 1000),
        ]
        for name, price, desc, stock in products:
            cursor.execute("INSERT INTO products (name, price, description, stock) VALUES (?, ?, ?, ?)",
                           (name, price, desc, stock))
        print(f"Added {len(products)} default products")
    
    # Import data từ waitlist.json
    if os.path.exists(WAITLIST_PATH):
        try:
            with open(WAITLIST_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                count = 0
                for item in data:
                    name = item.get('name', 'Unknown')
                    phone = item.get('phone', '')
                    zalo = item.get('zalo', '')
                    email = item.get('email', '')
                    
                    cursor.execute("SELECT id FROM customers WHERE phone = ?", (phone,))
                    if cursor.fetchone() is None:
                        cursor.execute("INSERT INTO customers (name, phone, zalo, email) VALUES (?, ?, ?, ?)", 
                                     (name, phone, zalo, email))
                        count += 1
                print(f"Success: Imported {count} waitlist customers.")
        except Exception as e:
            print(f"Error parse JSON: {e}")
            
    conn.commit()
    conn.close()
    print("Database CRM init OK!")

if __name__ == '__main__':
    init_db()
