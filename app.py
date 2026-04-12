from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import datetime

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app) # CHo phép Netlify gọi API từ Render
DB_PATH = "brain.db"

# Tự động tạo DB nếu chưa có trên Render
import build_db
if not os.path.exists(DB_PATH):
    build_db.init_db()
DB_PATH = "brain.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/admin')
def admin():
    return app.send_static_file('admin.html')

@app.route('/api/check_payment')
def check_payment():
    phone = request.args.get('phone', '')
    import urllib.request
    import json
    try:
        req = urllib.request.Request('https://my.sepay.vn/userapi/transactions/list', headers={
            'Authorization': 'Bearer D7TML96WIZQVJFQHZSXLVITTPRHZRBCNL9AREWV1UWE8ON1GRIQYPYKFIOGH5ANN'
        })
        res = urllib.request.urlopen(req)
        data = json.loads(res.read().decode('utf-8'))
        if data and data.get('transactions'):
            for t in data['transactions']:
                if f"DH {phone}" in t.get('transaction_content', ''):
                    # Cập nhật đơn hàng thành công trên CRM
                    conn = get_db()
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE orders 
                        SET status = 'success'
                        WHERE id = (
                            SELECT o.id FROM orders o
                            JOIN customers c ON o.customer_id = c.id
                            WHERE c.phone = ? AND o.status = 'pending'
                            ORDER BY o.id DESC LIMIT 1
                        )
                    """, (phone,))
                    conn.commit()
                    return jsonify({"success": True})
    except Exception as e:
        print(e)
    return jsonify({"success": False})

# ================= CLIENT API =================
@app.route('/api/booking', methods=['POST'])
def handle_booking():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    service = data.get('service', 'Dịch vụ website')
    amount = 2 # Giả định $2 cho khoản phí giữ chỗ (2000đ)
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM customers WHERE phone = ?", (phone,))
    row = cursor.fetchone()
    if row:
        customer_id = row['id']
    else:
        cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone))
        customer_id = cursor.lastrowid
        
    cursor.execute("SELECT id FROM products WHERE name = ?", (service,))
    row = cursor.fetchone()
    if row:
        product_id = row['id']
    else:
        cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, 100)", (service, amount))
        product_id = cursor.lastrowid
        
    cursor.execute("INSERT INTO orders (customer_id, product_id, amount, status) VALUES (?, ?, ?, 'pending')",
                   (customer_id, product_id, amount))
    conn.commit()
    return jsonify({"status": "success"})


# ================= PRODUCTS API =================
@app.route('/api/products', methods=['GET', 'POST'])
def handle_products():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM products ORDER BY id DESC")
        rows = cursor.fetchall()
        return jsonify([dict(ix) for ix in rows])
    elif request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO products (name, price, description, stock) VALUES (?, ?, ?, ?)",
                       (data.get('name'), data.get('price', 0), data.get('description'), data.get('stock', 0)))
        conn.commit()
        return jsonify({"status": "success", "id": cursor.lastrowid})

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    return jsonify({"status": "success"})


# ================= CUSTOMERS API =================
@app.route('/api/customers', methods=['GET', 'POST'])
def handle_customers():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM customers ORDER BY id DESC")
        rows = cursor.fetchall()
        return jsonify([dict(ix) for ix in rows])
    elif request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO customers (name, phone, zalo) VALUES (?, ?, ?)",
                       (data.get('name'), data.get('phone'), data.get('zalo')))
        conn.commit()
        return jsonify({"status": "success", "id": cursor.lastrowid})

@app.route('/api/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = ?", (id,))
    conn.commit()
    return jsonify({"status": "success"})


# ================= ORDERS API =================
@app.route('/api/orders', methods=['GET', 'POST'])
def handle_orders():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'GET':
        query = '''
            SELECT o.id, o.amount, o.status, o.purchase_date,
                   c.name as customer_name, p.name as product_name
            FROM orders o
            LEFT JOIN customers c ON o.customer_id = c.id
            LEFT JOIN products p ON o.product_id = p.id
            ORDER BY o.id DESC
        '''
        cursor.execute(query)
        rows = cursor.fetchall()
        return jsonify([dict(ix) for ix in rows])
        
    elif request.method == 'POST':
        data = request.json
        product_id = int(data.get('product_id'))
        customer_id = int(data.get('customer_id'))
        amount = float(data.get('amount', 0))
        
        # Thêm đơn hàng
        cursor.execute("INSERT INTO orders (customer_id, product_id, amount, status) VALUES (?, ?, ?, 'pending')",
                       (customer_id, product_id, amount))
                       
        # Giảm số lượng tồn kho tự động
        cursor.execute("UPDATE products SET stock = stock - 1 WHERE id = ? AND stock > 0", (product_id,))
        
        conn.commit()
        return jsonify({"status": "success", "id": cursor.lastrowid})

@app.route('/api/orders/<int:id>', methods=['DELETE', 'PUT'])
def modify_order(id):
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM orders WHERE id = ?", (id,))
        conn.commit()
        return jsonify({"status": "success"})
    elif request.method == 'PUT':
        data = request.json
        if 'status' in data:
            cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (data['status'], id))
            conn.commit()
            return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
