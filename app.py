from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import datetime
import threading

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

@app.route('/checkout')
def checkout():
    return app.send_static_file('checkout.html')

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
def send_resend_email(to_email, subject, html_content):
    try:
        import resend
        with open('resend_config.txt', 'r') as f:
            resend.api_key = f.read().strip()
        params = {
            "from": "onboarding@resend.dev",
            "to": to_email,
            "subject": subject,
            "html": html_content
        }
        resend.Emails.send(params)
    except Exception as e:
        pass

def run_email_sequence(email, name, host_url):
    is_test = '+test' in email.lower()
    
    # Resend Free Tier bắt buộc phải gửi chính xác email gốc, không cho dùng alias +test.
    # Nên ta phải cắt bỏ chữ +test đi trước khi nhét vào hàm send.
    if is_test:
        email = email.lower().replace('+test', '')
    
    # Email 1
    subject1 = "Chào mừng bạn! Cảm ơn bạn đã chọn tiệm của chúng mình 💕"
    html1 = f"""
    <p>Chào {name},</p>
    <p>Mình vừa nhận được thông tin đăng ký của bạn. Cảm ơn bạn rất nhiều vì đã tin tưởng và lựa chọn dịch vụ của tụi mình!</p>
    <p>Thật ra, dạo gần đây tiệm đang được mọi người nhiệt tình ủng hộ nên lịch có hơi kín một chút. Nhưng bạn hoàn toàn yên tâm nhé, mình đang cẩn thận sắp xếp thời gian ưu tiên để có thể đón tiếp và phục vụ bạn chu đáo nhất.</p>
    <p>Tiêu chí của tiệm là luôn chăm chút từng chi tiết nhỏ để mỗi khách hàng khi ngắm nhìn bộ móng của mình đều phải thốt lên "quá tuyệt". Nên bạn kiên nhẫn chờ mình một chút xíu nha.</p>
    <p>Trong vài ngày tới, mình sẽ gửi tặng bạn một số bí quyết chăm sóc móng siêu đơn giản nhưng cực kỳ hiệu quả tại nhà.</p>
    <p>Chúc bạn một ngày thật rạng rỡ và mong sớm được gặp bạn!</p>
    """
    
    # Gửi ngay Email 1
    send_resend_email(email, subject1, html1)
    
    # Set delay: trong chế độ test chờ 2 giây, nếu không chờ 2 ngày.
    delay2 = 2 if is_test else 2 * 24 * 3600
    
    def send_email2():
        subject2 = "Bí quyết nhỏ \"kéo dài tuổi thọ\" cho bộ móng của bạn 💅"
        html2 = f"""
        <p>Chào {name}, ngày hôm nay của bạn thế nào?</p>
        <p>Hôm nay tụi mình xin phép chia sẻ một vài "bí kíp nghề nghiệp" giúp bạn luôn giữ được đôi tay ngọc ngà, hoàn toàn không quảng cáo dịch vụ đâu nè.</p>
        <p>Thật ra, mình nhận thấy rất nhiều bạn vô tình dùng móng tay để bóc các vật cứng hoặc tự cạy nắp chai. Thói quen này vô tình phá vỡ cấu trúc bảo vệ, khiến móng rất dễ bị xước và gãy.</p>
        <p>Làm này đi: Mỗi tối trước khi đi ngủ, bạn hãy thoa một lớp mỏng dầu dưỡng (cuticle oil) hoặc kem dưỡng ẩm lên vùng viền da quanh móng nhé. Cách đơn giản này giúp viền da không bị khô bong tróc, đồng thời nuôi dưỡng móng cứng cáp hơn hẳn. Nhờ vậy, khi làm nail lớp sơn cũng sẽ bền màu và bóng bẩy hơn rất nhiều.</p>
        <p>Một thay đổi nhỏ thôi nhưng mang lại hiệu quả bất ngờ đấy! Bạn hãy thử áp dụng xem sao nhé.</p>
        <p>Hẹn gặp lại bạn trong bức thư sau!</p>
        """
        send_resend_email(email, subject2, html2)
        
        # Set delay: trong chế độ test chờ thêm 2 giây, nếu không chờ thêm 1 ngày.
        delay3 = 2 if is_test else 1 * 24 * 3600
        
        def send_email3():
            subject3 = "Sẵn sàng tỏa sáng cùng bộ móng mới chưa bạn ơi? ✨"
            payment_link = f"{host_url}#booking"
            html3 = f"""
            <p>Chào {name}, những ngày cuối tuần thảnh thơi lại sắp đến rồi!</p>
            <p>Khi móng tay đã được chăm sóc khỏe mạnh, đây chính là thời điểm hoàn hảo nhất để khoác lên chúng một diện mạo thật nổi bật. Hiện tại, tiệm mình đang có các dịch vụ chăm sóc với mức giá vô cùng yêu thương:</p>
            <ul>
                <li><strong>Dịch vụ Nail chuyên sâu:</strong> 10$</li>
                <li><strong>Vẽ Art độc quyền, thiết kế theo yêu cầu:</strong> 2$</li>
            </ul>
            <p>Thật ra, một bộ nail được chăm chút tỉ mỉ không chỉ làm đôi tay thêm phần kiêu kỳ mà còn mang lại cho bạn sự tự tin tuyệt đối trong mỗi dịp hẹn hò hay dạo phố. Nhưng mà lịch hẹn cuối tuần thường được ưu tiên đặt kín rất sớm.</p>
            <p>Để không phải chờ đợi lâu hay lỡ mất dịp làm đẹp, bạn làm này đi: Hãy nhấn ngay vào đường link bên dưới để giữ chỗ và hoàn tất đặt lịch nhé. Khi bạn đến tiệm, mọi việc làm đẹp cứ để tụi mình lo:</p>
            <p>🔗 <strong><a href="{payment_link}">[LINK TRANG THANH TOÁN]</a></strong></p>
            <p>Tụi mình đang rất mong chờ được tự tay làm đẹp cho bạn. Hẹn gặp bạn tại tiệm nha!</p>
            """
            send_resend_email(email, subject3, html3)
            
        threading.Timer(delay3, send_email3).start()

    threading.Timer(delay2, send_email2).start()

# ================= CLIENT API =================
@app.route('/api/checkout', methods=['POST'])
def handle_checkout():
    """Endpoint để tạo đơn hàng từ trang thanh toán"""
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')
    product_id = data.get('product_id')
    amount = data.get('amount', 0)
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Thêm hoặc lấy khách hàng
        cursor.execute("SELECT id FROM customers WHERE phone = ?", (phone,))
        row = cursor.fetchone()
        if row:
            customer_id = row['id']
        else:
            cursor.execute("INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
            customer_id = cursor.lastrowid
        
        # Tạo đơn hàng (status = pending)
        cursor.execute("INSERT INTO orders (customer_id, product_id, amount, status) VALUES (?, ?, ?, 'pending')",
                       (customer_id, product_id, amount))
        conn.commit()
        order_id = cursor.lastrowid
        
        return jsonify({"success": True, "order_id": order_id})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/booking', methods=['POST'])
def handle_booking():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')
    service = data.get('service', 'Dịch vụ website')
    amount = 2 # Giả định $2 cho khoản phí giữ chỗ (2000đ)
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM customers WHERE phone = ?", (phone,))
    row = cursor.fetchone()
    if row:
        customer_id = row['id']
    else:
        cursor.execute("INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
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
    order_id = cursor.lastrowid
    
    # Gửi chuỗi email Welcome -> Nurture -> Sales bằng background thread
    host_url = request.host_url
    threading.Thread(target=run_email_sequence, args=(email, name, host_url)).start()
        
    return jsonify({"status": "success", "order_id": order_id})


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
        cursor.execute("INSERT INTO customers (name, phone, email, zalo) VALUES (?, ?, ?, ?)",
                       (data.get('name'), data.get('phone'), data.get('email'), data.get('zalo')))
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
                   c.name as customer_name, c.email as customer_email, p.name as product_name
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
        
        cursor.execute("SELECT name, email FROM customers WHERE id = ?", (customer_id,))
        customer_row = cursor.fetchone()
        cursor.execute("SELECT name FROM products WHERE id = ?", (product_id,))
        product_row = cursor.fetchone()
        
        # Thêm đơn hàng
        cursor.execute("INSERT INTO orders (customer_id, product_id, amount, status) VALUES (?, ?, ?, 'pending')",
                       (customer_id, product_id, amount))
                       
        # Giảm số lượng tồn kho tự động
        cursor.execute("UPDATE products SET stock = stock - 1 WHERE id = ? AND stock > 0", (product_id,))
        
        conn.commit()
        order_id = cursor.lastrowid
        
        if customer_row and customer_row['email'] and product_row:
            cust_name = customer_row['name']
            cust_email = customer_row['email']
            prod_name = product_row['name']
            
            if '+test' in cust_email.lower():
                cust_email = cust_email.lower().replace('+test', '')
                
            subject = "✨ Đơn hàng của bạn đã được xác nhận! Chuẩn bị tỏa sáng đi nào 💅"
            html = f"""
            <p>Chào {cust_name},</p>
            <p>Cảm ơn bạn rất nhiều! Chúng mình vừa nhận được và xác nhận đơn hàng của bạn.</p>
            <p><b>📋 Chi Tiết Đơn Hàng:</b></p>
            <ul>
                <li><b>Dịch vụ:</b> {prod_name}</li>
                <li><b>Số tiền:</b> ${amount}</li>
                <li><b>Mã đơn:</b> #{order_id}</li>
            </ul>
            <p>Bây giờ tiệp chúng mình sẽ chuẩn bị các trang thiết bị, màu sắc và kỹ thuật tốt nhất để chăm sóc cho bạn. Mình sẽ không vội vàng — vì chúng mình hiểu rằng những điều tuyệt vời cần phải có thời gian để hoàn thiện.</p>
            <p><b>📍 Hướng Dẫn Tiếp Theo:</b></p>
            <ol>
                <li>Nếu bạn chưa có lịch cụ thể, hãy gọi hoặc nhắn zalo để tụi mình sắp xếp thời gian ưu tiên cho bạn.</li>
                <li>Hãy chuẩn bị tinh thần thư giãn và tận hưởng khoảng thời gian dành riêng cho bản thân.</li>
                <li>Nếu bạn có yêu cầu đặc biệt (màu sắc, thiết kế, chỉnh sửa nail cũ), bạn hoàn toàn có thể chia sẻ với chúng mình.</li>
            </ol>
            <p><b>💝 Lời Hứa Của Chúng Mình:</b><br>
            Mỗi lần bạn đến tiệm, chúng mình sẽ làm cho bộ móng của bạn không chỉ đẹp, mà còn khỏe mạnh và bền bỉ. Đó là cam kết của Happy Nail với mỗi khách hàng.</p>
            <p>Nếu có bất cứ thắc mắc gì trước ngày hẹn, bạn cứ liên hệ với chúng mình nhé. Chúng mình đang chờ được gặp bạn!</p>
            <p>Hẹn gặp bạn tại tiệm sớm! 💕</p>
            """
            
            threading.Thread(target=send_resend_email, args=(cust_email, subject, html)).start()
            
        return jsonify({"status": "success", "id": order_id})

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

@app.route('/api/orders/<int:id>/status', methods=['GET'])
def get_order_status(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM orders WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row:
        return jsonify({"status": row['status']})
    return jsonify({"error": "Order not found"}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
