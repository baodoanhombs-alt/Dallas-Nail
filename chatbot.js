document.addEventListener('DOMContentLoaded', () => {
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotWindow = document.getElementById('chatbot-window');
    const chatbotClose = document.getElementById('chatbot-close');
    const chatbotMessages = document.getElementById('chatbot-messages');
    const chatbotOptions = document.getElementById('chatbot-options');

    // Dữ liệu từ sales_script.md
    const GREETING = "Chào anh/chị nha! Nay dạo website móng bên em có ưng bụng mẫu nào chưa? Có gì thắc mắc anh/chị cứ nhắn em, em hỗ trợ nhiệt tình nè!";
    const CTA_MSG = "Tuyệt vời luôn! Này đặt lẹ đi nha, hôm nay làm em trừ thẳng giảm giá 20% cho chị lần đầu luôn á, có chỗ xịn đẹp chốt luôn cho nóng nghen chị. Em vào lịch ha?";
    const FORM_GUIDE = "Thật ra chị chưa muốn mần liền cũng không sao hết. Nhưng mà tiện thì chị để lại số điện thoại trên cái form góc màn hình kia đi, để mai em gửi mớ mẫu mới nhất qua Zalo cho chị ngó ha, rảnh rỗi mới qua làm nè.";

    const faqs = [
        { q: "Làm có sạch sẽ, an toàn không?", a: "Thật ra khách ai cũng sợ vụ này! Nhưng mà chị yên tâm, đồ nghề bên em hấp máy y tế tiệt trùng đàng hoàng 100%. Bồn ngâm bọc nilon xài đúng 1 lần rồi bỏ, quá tuyệt cho độ vệ sinh luôn, không lo lây nhiễm gì đâu." },
        { q: "Giá có đắt hơn mấy chỗ khác không?", a: "Dạ tiền nào của nấy chị ơi! Bên em làm kỹ, dũa ôm form và không nhồi nhét khách, thuốc men toàn đồ xịn. Nhỉnh hơn tí ti mà ra bộ móng xịn xài bền thì cũng đáng mà, làm này đi chị!" },
        { q: "Chị không biết chọn mẫu hợp", a: "Tay thô dũa form bên em là thon gọn liền. Chị sơn Ombre nha, bao tôn da luôn. Em gửi qua vài mẫu, chị ưng là em quất giống 100% lẹ đi chị." },
        { q: "Bên em dùng thảo dược gì để ngâm?", a: "Gói Essential Pedicure thì muối ngâm tẩy tế bào chết xịn xò. Còn muốn sướng nữa chị thử Saigon Brew nhen, ngâm sữa cà phê, massage đá nóng tẩy mùi cực đã." },
        { q: "Gót chân khô cứng làm sao?", a: "Cái này dễ, chị làm gói Crème de Miel đi. Ngâm thẳng vớ sữa dê mật ong, mềm ra là bao mịn, gót gạn đẹp lại liền." },
        { q: "Đau mỏi khớp massage chân được không?", a: "Dạ chọn gói CBD Healing dùm em. Massage dầu muối CBD bao phê, giảm đau nhức xương khớp cực mạnh nghen." },
        { q: "Sơn gel có phụ thu nhiều không?", a: "Chị đắp gel thêm xíu chừng $25 thôi nghen, đá đính thì sành điệu cứng khừ luôn." },
        { q: "Có cần hẹn lịch trước mới được làm?", a: "Ghé liền thì bên em đón (walk-in) vẫn được, nhưng mà ngộ nhỡ rớt vô cuối tuần là hay bấn lịch lắm. Book trước cái lịch đi cho thợ cứng mần giữ chỗ ngon lành chị nhé." },
        { q: "Giờ tiệm mình mở cửa sao?", a: "Tụi em cày T2-T6 (9am tới 7pm), T7 (9am-6pm). Còn cao hứng Chủ Nhật thì 10h sáng mở tới 5h chiều nha." },
        { q: "Có nhận thanh toán quẹt thẻ/Zelle?", a: "Chơi hệ nào cũng chiều. Tiền mặt, quẹt thẻ mạnh bạo hay Zelle em cũng cân láng!" }
    ];

    let isFirstOpen = true;

    // Toggle Chatbot
    const toggleChat = () => {
        chatbotWindow.classList.toggle('chatbot-hidden');
        if (isFirstOpen && !chatbotWindow.classList.contains('chatbot-hidden')) {
            startChatSequence();
            isFirstOpen = false;
        }
    };

    chatbotToggle.addEventListener('click', toggleChat);
    chatbotClose.addEventListener('click', toggleChat);

    function addMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-msg chat-${sender}`;
        msgDiv.innerHTML = text;
        chatbotMessages.appendChild(msgDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    function renderOptions() {
        chatbotOptions.innerHTML = '';
        
        // Nút chốt đơn
        const bookBtn = document.createElement('button');
        bookBtn.className = 'chat-opt-btn highlight';
        bookBtn.innerHTML = '✨ Ưng ý rồi, Đặt Lịch Ngay!';
        bookBtn.onclick = handleBookingFlow;
        chatbotOptions.appendChild(bookBtn);

        // Các nút FAQ
        faqs.forEach((faq) => {
            const btn = document.createElement('button');
            btn.className = 'chat-opt-btn';
            btn.innerHTML = faq.q;
            btn.onclick = () => handleFaqClick(faq.q, faq.a, btn);
            chatbotOptions.appendChild(btn);
        });
    }

    function handleFaqClick(question, answer, btn) {
        // Tạm thời Disable các nút khi chat
        chatbotOptions.style.pointerEvents = 'none';
        chatbotOptions.style.opacity = '0.5';

        // In phần hỏi
        addMessage('user', question);

        // Simulate thinking time
        setTimeout(() => {
            addMessage('bot', answer);
            // Restore Buttons
            chatbotOptions.style.pointerEvents = 'all';
            chatbotOptions.style.opacity = '1';
            btn.style.display = 'none'; // Xóa câu đã hỏi để gọn layout
        }, 600);
    }

    function handleBookingFlow() {
        chatbotOptions.style.display = 'none'; // Ẩn options
        addMessage('user', 'Mình muốn đặt lịch làm bên tiệm bạn!');
        
        setTimeout(() => {
            addMessage('bot', CTA_MSG);
            
            // Xây dựng flow tiếp theo (Nút Điền form)
            setTimeout(() => {
                addMessage('bot', `<button onclick="document.getElementById('custName').focus() || window.location.assign('#booking')" style="background:var(--accent-color); color:#fff; border:none; padding:8px 12px; border-radius:4px; font-weight:600; cursor:pointer;">👉 Khai Form Ở Đây Nè</button><br><br> ${FORM_GUIDE}`);
            }, 800);

        }, 500);
    }

    function startChatSequence() {
        setTimeout(() => {
            addMessage('bot', GREETING);
            renderOptions();
        }, 400);
    }
});
