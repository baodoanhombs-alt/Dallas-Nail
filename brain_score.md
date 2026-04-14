# Tracking Progress - SOP Ngày 11: Email Marketing Tự Động

## 📊 Tổng Quan Ngày 11

**Ngày:** April 13, 2026\
**Mục Tiêu:** Xây dựng cỗ máy email marketing tự động\
**Trạng Thái:** ✅ HOÀN THÀNH

---

## ✅ Bước 1: Thêm Trường Email Vào Form & CRM
- ✅ Form waitlist có trường email: `<input type="email" id="custEmail" name="Email">`
- ✅ CRM database có cột email trong bảng `customers`
- ✅ Trang /admin hiển thị cột email của khách hàng

---

## ✅ Bước 2: Đăng Ký Resend & Lấy API Key
- ✅ Resend API Key được lưu trong `resend_config.txt`: `re_9EfSMnM5_PaHAuivBSj2FoN9t9kmGf2Mp`
- ✅ Email mặc định: `onboarding@resend.dev` (Resend Free Tier)
- 📝 Ghi chú: Domain verify sẽ làm sau khi deploy VPS

---

## ✅ Bước 3: Kết Nối Resend Vào Website
- ✅ `app.py` có hàm `send_resend_email()` kết nối API
- ✅ Hàm đọc API Key từ `resend_config.txt`
- ✅ Cấu hình CORS cho Netlify gọi API từ Render

---

## ✅ Bước 4: Viết 3 Email Tự Động
- ✅ Email 1 (Welcome): Chào mừng, giới thiệu tiệm
- ✅ Email 2 (Nurture): Chia sẻ bí quyết chăm sóc móng
- ✅ Email 3 (Sales): Mời đặt lịch, CTA rõ ràng

📁 File: `email_sequence.md` (đã tạo)

---

## ✅ Bước 5: Gắn Email Sequence Vào Website
- ✅ Khi khách điền form → Email 1 gửi **ngay lập tức**
- ✅ 2 ngày sau → Email 2 tự động gửi
- ✅ 1 ngày sau → Email 3 tự động gửi
- ✅ Chế độ +test: Email có "+test" → gửi cả 3 email ngay tức thì

**Code:** `run_email_sequence()` trong `app.py` (line 83-142)

---

## ✅ Bước 6: Email Xác Nhận Đơn Hàng
- ✅ Khi thêm đơn mới trong /admin → Email xác nhận tự động gửi
- ✅ Email có: Tên sản phẩm, giá tiền, hướng dẫn nhận hàng, lời cảm ơn
- ✅ Xử lý email +test tự động

**Code:** `/api/orders` POST handler trong `app.py` (line 260-290)

---

## ⏳ Bước 7: Đăng Bài Thông Báo
📁 File: `day11.txt` (sẵn sàng để chỉnh sửa & đăng)

**Các kênh cần đăng:**
- [ ] Facebook Business Page
- [ ] Instagram
- [ ] Zalo Official Account
- [ ] Tiktok Shop (nếu có)

---

## 🧪 Testing Checklist

### Test Email +test Mode:
```
1. Vào form → Điền email: yourname+test@gmail.com
2. Kiểm tra hộp thư:
   - [ ] Email 1 (Welcome) - gửi ngay
   - [ ] Email 2 (Nurture) - gửi ngay (chế độ test)
   - [ ] Email 3 (Sales) - gửi ngay (chế độ test)
```

### Test Email Xác Nhận Đơn:
```
1. Vào /admin → Thêm 1 đơn hàng mới
2. Kiểm tra hộp thư:
   - [ ] Email xác nhận đơn nhận được
   - [ ] Có thông tin: Tên sản phẩm, giá tiền, hướng dẫn
```

---

## 📋 Nộp Bài - Yêu Cầu
- [ ] Screenshot 3 email trong hộp thư (chế độ +test)
- [ ] Screenshot email xác nhận đơn hàng
- [ ] File `email_sequence.md` có đủ 3 email
- [ ] Link bài đăng public (ít nhất 2 kênh)

---

## 📍 Các File Liên Quan

| File | Mục Đích |
|------|----------|
| `app.py` | Backend xử lý email + API |
| `email_sequence.md` | Lưu trữ nội dung 3 email |
| `resend_config.txt` | API Key Resend |
| `index.html` | Form chứa trường email |
| `admin.html` | CRM hiển thị email khách |
| `day11.txt` | Bài đăng thông báo |

---

## 💡 Ghi Chú
- Resend miễn phí cho giai đoạn đầu (~100 email/ngày)
- Email +test được gửi ngay (dành cho testing)
- Email thường được gửi theo lịch (2 ngày, 1 ngày)
- Verify domain sau khi deploy VPS
