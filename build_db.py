import sqlite3
import json
import os

DB_PATH = "brain.db"
WAITLIST_PATH = "waitlist.json"

def init_db():
    conn = sqlite3.connect(DB_PATH)
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
            zalo TEXT,
            registered_date TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')

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
                    
                    cursor.execute("SELECT id FROM customers WHERE phone = ?", (phone,))
                    if cursor.fetchone() is None:
                        cursor.execute("INSERT INTO customers (name, phone, zalo) VALUES (?, ?, ?)", (name, phone, zalo))
                        count += 1
                print(f"Success: Imported {count} waitlist customers.")
        except Exception as e:
            print(f"Error parse JSON: {e}")
            
    conn.commit()
    conn.close()
    print("Database CRM init OK!")

if __name__ == '__main__':
    init_db()
