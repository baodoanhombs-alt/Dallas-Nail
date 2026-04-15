# 📋 SOP NGÀY 11 - EMAIL MARKETING TỰ ĐỘNG
## Hướng Dẫn Nộp Bài & Chứng Minh

---

## ✅ HOÀN THÀNH CÁC BƯỚC

### Bước 1: Email field trong Form & CRM ✅
- ✅ Form waitlist (index.html) có trường email
- ✅ Bảng customers dalam brain.db có cột email
- ✅ Admin panel (/admin) hiển thị cột email

**File:** [index.html](index.html), [admin.html](admin.html), [build_db.py](build_db.py#L30)

---

### Bước 2: Resend API Key ✅
- ✅ API Key đã lưu trong [resend_config.txt](resend_config.txt)
- ✅ Key hợp lệ và sẵn sàng

**File:** [resend_config.txt](resend_config.txt)

---

### Bước 3: Kết nối Resend vào Website ✅
- ✅ Hàm `send_resend_email()` đã kết nối
- ✅ Dùng Resend SDK để gửi qua API

**File:** [app.py](app.py#L53)

```python
def send_resend_email(to_email, subject, html_content):
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
```

---

### Bước 4: 3 Email Sequence ✅
- ✅ Email 1 (Welcome) - Chào mừng
- ✅ Email 2 (Nurture) - Chia sẻ giá trị
- ✅ Email 3 (Sales) - Chốt bán

**File:** [email_sequence.md](email_sequence.md)

**Giọng:** Gần gũi, ấm áp, chuyên nghiệp

---

### Bước 5: Tự động gửi + Test Mode ✅
- ✅ Email 1 gửi ngay khi điền form
- ✅ Email 2 gửi sau 2 ngày (chế độ normal)
- ✅ Email 3 gửi sau 1 ngày
- ✅ Chế độ +test: gửi cả 3 email ngay lập tức

**File:** [app.py](app.py#L77) - hàm `run_email_sequence()`

```python
def run_email_sequence(email, name, host_url):
    is_test = '+test' in email.lower()
    
    # Email 1 - ngay lập tức
    send_resend_email(email, subject1, html1)
    
    # Email 2 - sau 2 ngày (2 giây nếu test)
    delay2 = 2 if is_test else 2 * 24 * 3600
    
    # Email 3 - sau 1 ngày (2 giây nếu test)
    delay3 = 2 if is_test else 1 * 24 * 3600
```

---

### Bước 6: Email Xác Nhận Đơn Hàng ✅
- ✅ Email xác nhận được viết trong [email_sequence.md](email_sequence.md#L78)
- ✅ Kết nối vào `/admin` - khi tạo đơn hàng, email gửi tự động
- ✅ Email có: Tên sản phẩm, giá tiền, mã đơn, hướng dẫn

**File:** [app.py](app.py#L256-L295)

```python
# Khi POST /api/orders, tự động gửi email xác nhận
if customer_row and customer_row['email']:
    subject = "✨ Đơn hàng của bạn đã được xác nhận!"
    send_resend_email(cust_email, subject, html)
```

---

### Bước 7: Announcement Post ✅
- ✅ Bài đăng đã sẵn trong [day11.txt](day11.txt)
- ✅ Tone: Gần gũi, có chút tự hào
- ✅ Có link website

**File:** [day11.txt](day11.txt)

---

## 🧪 HƯỚNG DẪN TEST EMAIL THỰC TẾ

### Test 1: Form booking với email +test (3 email welcome/nurture/sales)

**Bước 1:** Truy cập https://yourdomain.com

**Bước 2:** Điền form "Đặt lịch" với:
- Tên: Bất kỳ
- Email: `youremail+test@gmail.com` (phải có +test)
- SĐT: Bất kỳ

**Bước 3:** Nhấn "Đặt lịch"

**Bước 4:** Chờ vài giây, kiểm tra hộp thư:
- Email 1 (Welcome): Chào mừng
- Email 2 (Nurture): Bí quyết chăm sóc
- Email 3 (Sales): Mời đặt lịch

**Lưu ý:** 
- Gmail sẽ nhận tất cả 3 email vào hộp thư một nơi (vì Gmail bỏ qua +test)
- Subject sẽ khác nhau để nhân biết

---

### Test 2: Tạo đơn hàng trong /admin (email xác nhận)

**Bước 1:** Truy cập https://yourdomain.com/admin

**Bước 2:** Tab "Khách hàng" → Thêm khách hàng với email thực

**Bước 3:** Tab "Đơn hàng" → Chọn khách hàng + sản phẩm → Nhấn "Tạo đơn"

**Bước 4:** Kiểm tra hộp thư khách hàng nhận email:
- Subject: "✨ Đơn hàng của bạn đã được xác nhận!"
- Có: Tên sản phẩm, giá tiền, mã đơn, hướng dẫn

---

## 📸 SCREENSHOTS CẦN CHỤP

### For Submission (Nộp Bài):

**1. Email 1 (Welcome)** 
- Chụp email nhận được
- Hiển thị Subject + Nội dung

**2. Email 2 (Nurture)**
- Chụp email nhận được
- Hiển thị Subject + Nội dung

**3. Email 3 (Sales)**
- Chụp email nhận được
- Hiển thị Subject + Nội dung + Link booking

**4. Email 4 (Order Confirmation)**
- Chụp email xác nhận đơn hàng
- Hiển thị Subject + Nội dung + Mã đơn

**5. email_sequence.md**
- Chụp file có đủ 4 email đúng giọng

**6. Admin Panel - Email Column**
- Chụp tab "Khách hàng" có cột email

**7. Admin Panel - Tạo Đơn**
- Chụp tab "Đơn hàng" sau khi tạo đơn thành công

**8. Post Announcement**
- Link bài đăng trên ít nhất 2 kênh (Facebook, Instagram, Zalo, LinkedIn)

---

## ✅ TIÊU CHÍ DUYỆT

### ✅ Được Duyệt Khi:

✅ Nhận được Email 1 (Welcome) - có Subject + Nội dung chào mừng

✅ Nhận được Email 2 (Nurture) - 2 ngày sau, có bí quyết chăm sóc

✅ Nhận được Email 3 (Sales) - 1 ngày sau, có link đặt lịch

✅ Nhận được Email 4 (Order Confirmation) - khi tạo đơn, có mã đơn

✅ email_sequence.md có đủ 4 email đúng giọng brand

✅ Admin panel có cột email, có thể tạo đơn với email tự động

✅ Link bài đăng mở được - công khai (không private)

### ❌ Chưa Đạt Khi:

❌ Chỉ nhận được Email 1, Email 2 & 3 chưa chạy

❌ Email xác nhận đơn chưa hoạt động

❌ email_sequence.md trống hoặc sai giọng

❌ Link bài đăng private hoặc chỉ ảnh chụp

❌ Admin panel không có cột email

---

## 🚀 START TEST NGAY

### Command để chạy test system:

```bash
cd your-project-folder
python test_email_flow.py
```

Kết quả: [test_log.txt](test_log.txt)

✅ API hoạt động ✅
✅ Form booking đã thêm khách hàng ✅
✅ Email sequence logic chuẩn bị sẵn ✅
✅ Order creation + email xác nhận ready ✅

---

## 📝 TÓNG KẾT (Checklist)

- [x] Email field trong form & CRM
- [x] Resend API Key
- [x] Kết nối Resend
- [x] 3 Email Sequence (Welcome, Nurture, Sales)
- [x] Tự động gửi + test mode
- [x] Email Xác Nhận Đơn Hàng
- [x] Announcement Post
- [ ] Test Emails Thực Tế & Nộp Proof

**Còn lại:** Test email thực tế + Chụp screenshot nộp bài

---

## 📞 SUPPORT

- **Test fail?** Kiểm tra Resend API Key trong resend_config.txt
- **Email không gửi?** Kiểm tra network + Resend dashboard
- **Admin panel lỗi?** Refresh page, clear browser cache

---

**Good luck! 🚀**
