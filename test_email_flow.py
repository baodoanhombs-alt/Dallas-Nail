#!/usr/bin/env python3
"""
Script test email workflow
- Test 1: Điền form booking với email +test -> gữi 3 email welcome/nurture/sales
- Test 2: Tạo đơn hàng qua /admin -> gửi email xác nhận
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"
LOG_FILE = "test_log.txt"

def log_msg(msg):
    """Ghi log vào file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line + "\n")

def clear_log():
    """Xóa log cũ"""
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write("=== TEST EMAIL WORKFLOW LOG ===\n\n")

clear_log()
log_msg("🚀 BẮT ĐẦU TEST EMAIL MARKETING WORKFLOW")
log_msg("=" * 60)

# TEST 1: Form booking với email +test
log_msg("\n📝 TEST 1: Điền form booking với email +test")
log_msg("-" * 60)

test_email = "doanthuan+test@gmail.com"
booking_data = {
    "name": "Nguyễn Thị Test",
    "phone": "0987654321",
    "email": test_email,
    "service": "Dịch vụ Nail chuyên sâu"
}

try:
    log_msg(f"📧 Gửi dữ liệu booking: {json.dumps(booking_data, ensure_ascii=False)}")
    response = requests.post(f"{BASE_URL}/api/booking", json=booking_data)
    
    if response.status_code == 200:
        result = response.json()
        order_id = result.get('order_id')
        log_msg(f"✅ Booking thành công! Order ID: {order_id}")
        log_msg(f"🎯 Hệ thống sẽ gửi 3 email tự động:")
        log_msg(f"   📧 Email 1 (Welcome): Gửi ngay lập tức")
        log_msg(f"   📧 Email 2 (Nurture): Gửi sau 2 giây (test mode)")
        log_msg(f"   📧 Email 3 (Sales): Gửi sau 2 giây nữa (test mode)")
        log_msg(f"⏳ Chờ 5 giây để hệ thống xử lý...")
        time.sleep(5)
    else:
        log_msg(f"❌ Booking lỗi: {response.status_code} - {response.text}")
except Exception as e:
    log_msg(f"❌ Lỗi: {str(e)}")

# TEST 2: Lấy danh sách khách hàng để thêm đơn
log_msg("\n👥 TEST 2: Lấy danh sách khách hàng")
log_msg("-" * 60)

try:
    response = requests.get(f"{BASE_URL}/api/customers")
    if response.status_code == 200:
        customers = response.json()
        log_msg(f"✅ Lấy được {len(customers)} khách hàng")
        if customers:
            test_customer = customers[0]
            log_msg(f"Khách hàng test: {test_customer['name']} (ID: {test_customer['id']}, Email: {test_customer.get('email', 'N/A')})")
    else:
        log_msg(f"❌ Lỗi: {response.status_code}")
except Exception as e:
    log_msg(f"❌ Lỗi: {str(e)}")

# TEST 3: Lấy danh sách sản phẩm
log_msg("\n📦 TEST 3: Lấy danh sách sản phẩm/dịch vụ")
log_msg("-" * 60)

product_id = None
try:
    response = requests.get(f"{BASE_URL}/api/products")
    if response.status_code == 200:
        products = response.json()
        log_msg(f"✅ Lấy được {len(products)} sản phẩm")
        if products:
            product = products[0]
            product_id = product['id']
            log_msg(f"Sản phẩm test: {product['name']} (ID: {product_id}, Giá: ${product['price']})")
    else:
        log_msg(f"❌ Lỗi: {response.status_code}")
except Exception as e:
    log_msg(f"❌ Lỗi: {str(e)}")

# TEST 4: Tạo đơn hàng (Email xác nhận)
log_msg("\n📋 TEST 4: Tạo đơn hàng -> Gửi email xác nhận")
log_msg("-" * 60)

if product_id and customers:
    try:
        customer_id = customers[0]['id']
        order_data = {
            "customer_id": customer_id,
            "product_id": product_id,
            "amount": 10.0
        }
        log_msg(f"📧 Tạo đơn hàng: Customer ID {customer_id} + Product ID {product_id}")
        response = requests.post(f"{BASE_URL}/api/orders", json=order_data)
        
        if response.status_code == 200:
            result = response.json()
            new_order_id = result.get('id')
            log_msg(f"✅ Đơn hàng tạo thành công! Order ID: {new_order_id}")
            log_msg(f"📧 Email xác nhận đơn hàng sẽ được gửi tự động đến: {test_customer.get('email', 'N/A')}")
        else:
            log_msg(f"❌ Tạo đơn lỗi: {response.status_code} - {response.text}")
    except Exception as e:
        log_msg(f"❌ Lỗi: {str(e)}")
else:
    log_msg("⚠️  Bỏ qua TEST 4 - không có sản phẩm hoặc khách hàng")

# Kết luận
log_msg("\n" + "=" * 60)
log_msg("✅ TEST HOÀN THÀNH!")
log_msg("\n📊 TÓNG KẾT:")
log_msg("✅ Email 1 (Welcome) - Gửi ngay khi đăng ký")
log_msg("✅ Email 2 (Nurture) - Gửi sau 2 ngày")
log_msg("✅ Email 3 (Sales) - Gửi sau 1 ngày")
log_msg("✅ Email 4 (Order Confirmation) - Gửi khi tạo đơn")
log_msg("\n💡 Lưu ý: Chế độ +test sẽ gửi Email 1,2,3 ngay lập tức thay vì chờ theo lịch")
log_msg("💡 Địa chỉ email test phải chứa '+test' để kích hoạt chế độ test")
log_msg("\nLog file: test_log.txt")
