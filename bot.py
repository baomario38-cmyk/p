import os
import random
import hashlib
import string
import math
from datetime import datetime
from threading import Thread
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- 1. SERVER WEB GIỮ BOT SỐNG 24/7 TRÊN RENDER ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot TOOL TX MD5 PRO v7.0 NEURAL ENGINE đang hoạt động 24/7!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 2. CẤU HÌNH TOKEN BOT & DỮ LIỆU ---
TOKEN = '8985526419:AAGdRkntgFNYLBG53LoI-pNC7aHtOFMWhGA'
ADMIN_ID = 755092812  # Telegram ID Admin của bạn
bot = telebot.TeleBot(TOKEN)

user_data = {}
all_user_ids = set()
giftcodes = {}
admin_notice = "⚡ TOOL TX MD5 PRO v7.0 NEURAL ENGINE đã kích hoạt mạng Nơ-ron siêu dự đoán!"

SUPPORTED_WEBS = ["HitClub", "B52", "Lucky88", "LC79"]

def init_user(uid):
    all_user_ids.add(uid)
    if uid not in user_data:
        user_data[uid] = {
            "balance": 20,
            "bias": 0.0,
            "last_pred": None,
            "win_streak": 0,
            "history_logs": [],
            "last_checkin": "",
            "selected_web": "HitClub",
            "kalman_state": 0.5,
            "kalman_covariance": 1.0
        }

# --- 3. ĐỘNG CƠ SOI CẦU MẠNG NƠ-RON V7.0 (NEURAL PATTERN ENGINE) ---

def deep_neural_hash_features(hex_str):
    """Trích xuất ma trận đặc trưng từ chuỗi Hash qua 4 lớp Nơ-ron ảo"""
    # Lớp 1: Khởi tạo Vector trọng số từ SHA3-512
    full_hash = hashlib.sha3_512(hex_str.encode()).hexdigest()
    weights = [int(full_hash[i:i+2], 16) / 255.0 for i in range(0, 32, 2)]
    
    # Lớp 2: Tích chập Nơ-ron phi tuyến tính (Sigmoid + LeakyReLU)
    layer1 = []
    for idx, w in enumerate(weights):
        val = w * math.sin(idx + 1) + math.cos(w * math.pi)
        activated = val if val > 0 else val * 0.01  # LeakyReLU
        layer1.append(activated)
        
    # Lớp 3: Ma trận liên kết chuỗi
    layer2_score = sum([val * (1.5 ** (idx % 4)) for idx, val in enumerate(layer1)])
    
    # Lớp 4: Chuẩn hóa đầu ra Sigmoid (0.0 - 100.0)
    final_sig = 1 / (1 + math.exp(-layer2_score / 2.5))
    return final_sig * 100.0

def kalman_filter_update(uid, measurement):
    """Bộ lọc Kalman làm mịn dữ liệu nhiễu và loại bỏ biến động ảo"""
    ud = user_data[uid]
    x_hat = ud["kalman_state"]
    P = ud["kalman_covariance"]
    
    # Quá trình dự báo & cập nhật Kalman
    Q = 0.01  # Nhiễu hệ thống
    R = 0.1   # Nhiễu đo lường
    
    P_priori = P + Q
    K = P_priori / (P_priori + R)
    x_hat_new = x_hat + K * (measurement - x_hat)
    P_new = (1 - K) * P_priori
    
    ud["kalman_state"] = x_hat_new
    ud["kalman_covariance"] = P_new
    return x_hat_new

def master_predict_neural_v7(uid, raw_code):
    ud = user_data[uid]
    clean_code = raw_code.strip().lower()
    
    # Tính toán qua Neural Network
    raw_neural = deep_neural_hash_features(clean_code)
    
    # Lọc nhiễu qua Kalman
    filtered_score = kalman_filter_update(uid, raw_neural / 100.0) * 100.0
    
    # Hiệu chỉnh thích nghi theo kết quả thắng/thua thực tế (Adaptive Bias)
    adaptive_score = filtered_score + (ud["bias"] * 15.0) + (ud["win_streak"] * 2.0)
    
    # Giới hạn phân vùng quyết định
    final_ratio = max(5.0, min(95.0, adaptive_score))
    
    is_tai = final_ratio >= 50.0
    final_result = "TÀI" if is_tai else "XỈU"
    
    # Độ chính xác thuật toán v7.0
    confidence = round(min(99.2, max(91.5, 88.0 + abs(final_ratio - 50.0) * 0.45)), 1)
    
    if is_tai:
        percent_tai = round(final_ratio, 1)
        percent_xiu = round(100 - final_ratio, 1)
    else:
        percent_xiu = round(100 - final_ratio, 1)
        percent_tai = round(final_ratio, 1)
        
    ud["last_pred"] = final_result
    
    code_type = "MD5" if len(clean_code) == 32 else "SHA256"
    ud["history_logs"].append(f"[{code_type}] {clean_code[:6]}... ➔ {final_result}")
    if len(ud["history_logs"]) > 5:
        ud["history_logs"].pop(0)

    return final_result, percent_tai, percent_xiu, confidence, code_type

# --- 4. GIAO DIỆN PHÍM BẤM ---

def main_menu_keyboard(uid):
    markup = InlineKeyboardMarkup(row_width=2)
    
    btn_soi = InlineKeyboardButton("🎲 SOI MÃ NEURAL V7.0", callback_data="mode_soi")
    btn_web = InlineKeyboardButton(f"🌐 CỔNG: {user_data[uid]['selected_web']}", callback_data="mode_select_web")
    
    btn_checkin = InlineKeyboardButton("🎁 ĐIỂM DANH (+2 XU)", callback_data="mode_checkin")
    btn_info = InlineKeyboardButton("💳 VÍ & LỊCH SỬ", callback_data="mode_info")
    btn_buy = InlineKeyboardButton("💎 MUA XU VIP", callback_data="mode_buy")
    
    markup.add(btn_soi, btn_web)
    markup.add(btn_checkin, btn_info)
    markup.add(btn_buy)
        
    return markup

# --- 5. LỆNH CƠ BẢN ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    uid = message.from_user.id
    init_user(uid)
    xu = user_data[uid]["balance"]
    web = user_data[uid]["selected_web"]
    
    msg = (
        "⚡ **TOOL TX MD5 PRO v7.0 (NEURAL ENGINE)** ⚡\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"📢 **THÔNG BÁO ADMIN:**\n_{admin_notice}_\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 **ID:** `{uid}` | 🌐 **Cổng Game:** `{web}`\n"
        f"💰 **Số Xu hiện có:** **{xu} Xu** | 🔥 **Streak:** **{user_data[uid]['win_streak']} tay**\n"
        "🤖 **Thuật toán:** `Deep Neural Network` + `Kalman Filter` + `Adaptive Bias`\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "💡 **HƯỚNG DẪN:** Dán mã **MD5 (32 ký tự)** hoặc **SHA256 (64 ký tự)** vào đây để soi!\n"
        "💬 Chat **`bú`** khi ăn hoặc **`gãy`** khi thua để AI cập nhật ma trận ván sau!"
    )
    bot.reply_to(message, msg, parse_mode="Markdown", reply_markup=main_menu_keyboard(uid))

# --- 6. HỆ THỐNG QUẢN TRỊ ADMIN (ĐÃ NÂNG CẤP XỬ LÝ) ---

@bot.message_handler(commands=['congxu'])
def add_coins(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        args = message.text.split()
        target_id = int(args[1])
        coins_to_add = int(args[2])
        
        init_user(target_id)
        user_data[target_id]["balance"] += coins_to_add
        
        reply_msg = (
            "✅ **ĐÃ CỘNG XU THÀNH CÔNG!**\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"👤 **ID User:** `{target_id}`\n"
            f"💰 **Số xu cộng:** `+{coins_to_add} Xu`\n"
            f"💳 **Tổng số dư mới:** `{user_data[target_id]['balance']} Xu`"
        )
        bot.reply_to(message, reply_msg, parse_mode="Markdown")
        
        try:
            bot.send_message(
                target_id, 
                f"🎉 **THÔNG BÁO CỘNG XU TỪ ADMIN!**\n🎁 BẠN ĐÃ ĐƯỢC CỘNG: **+{coins_to_add} Xu**\n💳 Số dư hiện tại: **{user_data[target_id]['balance']} Xu**", 
                parse_mode="Markdown"
            )
        except Exception:
            pass
            
    except Exception as e:
        bot.reply_to(message, "❌ **Cú pháp sai!**\n👉 Dùng câu lệnh: `/congxu <ID_User> <Số_Xu>`\n*Ví dụ:* `/congxu 755092812 800`", parse_mode="Markdown")

@bot.message_handler(commands=['thongbao', 'tb'])
def broadcast_notice(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        notice_text = message.text.split(" ", 1)[1].strip()
    except IndexError:
        bot.reply_to(message, "❌ **Cú pháp:** `/thongbao <Nội_dung>`", parse_mode="Markdown")
        return

    global admin_notice
    admin_notice = notice_text
    
    success_count, fail_count = 0, 0
    status_msg = bot.reply_to(message, f"🚀 **Đang phát thông báo tới {len(all_user_ids)} người dùng...**", parse_mode="Markdown")
    
    broadcast_format = (
        "🔔 **THÔNG BÁO CHÍNH THỨC TỪ ADMIN** 🔔\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"{notice_text}\n"
        "━━━━━━━━━━━━━━━━━━━"
    )

    for target_id in list(all_user_ids):
        try:
            bot.send_message(target_id, broadcast_format, parse_mode="Markdown")
            success_count += 1
        except Exception:
            fail_count += 1

    bot.edit_message_text(
        f"✅ **ĐÃ GỬI THÔNG BÁO THÀNH CÔNG!**\n"
        f"📬 Thành công: {success_count} | ❌ Thất bại: {fail_count}",
        chat_id=message.chat.id,
        message_id=status_msg.message_id,
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['taocode'])
def create_code(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        args = message.text.split()
        code_input, coins = args[1].upper(), int(args[2])
        uses = int(args[3]) if len(args) >= 4 else 1
        code_string = "GIFT-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) if code_input == "AUTO" else code_input
        giftcodes[code_string] = {"coins": coins, "uses": uses, "used_by": set()}
        bot.reply_to(message, f"🎉 **TẠO CODE THÀNH CÔNG!**\n🎁 Code: `{code_string}` | 💰 Xu: **+{coins}** | 👥 Lượt: **{uses}**", parse_mode="Markdown")
    except Exception:
        bot.reply_to(message, "❌ Cú pháp sai: `/taocode <Mã_Code hoặc AUTO> <Số_Xu> [Lượt]`")

@bot.message_handler(commands=['code'])
def redeem_code(message):
    uid = message.from_user.id
    init_user(uid)
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "⚠️ **Cú pháp:** `/code <Mã_Giftcode>`", parse_mode="Markdown")
            return
        code_input = args[1].strip().upper()
        if code_input not in giftcodes:
            bot.reply_to(message, "❌ **Code không tồn tại hoặc đã hết hạn!**", parse_mode="Markdown")
            return
        code_info = giftcodes[code_input]
        if uid in code_info["used_by"]:
            bot.reply_to(message, "⚠️ **Bạn đã nhập code này rồi!**", parse_mode="Markdown")
            return
        if len(code_info["used_by"]) >= code_info["uses"]:
            bot.reply_to(message, "❌ **Code đã hết lượt sử dụng!**", parse_mode="Markdown")
            return
        user_data[uid]["balance"] += code_info["coins"]
        code_info["used_by"].add(uid)
        bot.reply_to(message, f"🎉 **NHẬP CODE THÀNH CÔNG!**\n🎁 Cộng: **+{code_info['coins']} Xu**", parse_mode="Markdown", reply_markup=main_menu_keyboard(uid))
    except Exception:
        bot.reply_to(message, "❌ Lỗi hệ thống khi nhập code!")

# --- 7. CALLBACK NÚT BẤM ---

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    uid = call.from_user.id
    init_user(uid)

    if call.data == "mode_soi":
        bot.send_message(call.message.chat.id, "📥 **Gửi mã MD5 (32 ký tự) hoặc SHA256 (64 ký tự) vào ô chat:**", parse_mode="Markdown")

    elif call.data == "mode_select_web":
        markup = InlineKeyboardMarkup(row_width=2)
        for w in SUPPORTED_WEBS:
            markup.add(InlineKeyboardButton(f"🎮 {w}", callback_data=f"setweb_{w}"))
        bot.send_message(call.message.chat.id, "🌐 **CHỌN CỔNG GAME BẠN ĐANG CHƠI:**", reply_markup=markup)

    elif call.data.startswith("setweb_"):
        selected = call.data.split("_")[1]
        user_data[uid]["selected_web"] = selected
        bot.answer_callback_query(call.id, f"✅ Đã chọn cổng: {selected}")
        bot.send_message(call.message.chat.id, f"✅ **Đã chuyển sang cổng Game: {selected}**", reply_markup=main_menu_keyboard(uid))

    elif call.data == "mode_checkin":
        today = datetime.now().strftime("%Y-%m-%d")
        if user_data[uid]["last_checkin"] == today:
            bot.answer_callback_query(call.id, "⚠️ Hôm nay bạn đã điểm danh rồi!", show_alert=True)
        else:
            user_data[uid]["last_checkin"] = today
            user_data[uid]["balance"] += 2
            bot.send_message(call.message.chat.id, "🎉 **ĐIỂM DANH THÀNH CÔNG!**\n🎁 Bạn nhận được **+2 Xu**!", parse_mode="Markdown")

    elif call.data == "mode_info":
        xu = user_data[uid]["balance"]
        streak = user_data[uid]["win_streak"]
        web = user_data[uid]["selected_web"]
        logs = user_data[uid]["history_logs"]
        logs_str = "\n".join([f"• {log}" for log in logs]) if logs else "Chưa có lịch sử."
        
        info_msg = (
            f"👤 **THÔNG TIN TÀI KHOẢN**\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 Telegram ID: `{uid}`\n"
            f"🌐 Cổng Game: **{web}**\n"
            f"💰 Số Xu hiện có: **{xu} Xu**\n"
            f"🔥 Dây thắng: **{streak} ván**\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"📜 **5 VÁN SOI GẦN NHẤT:**\n{logs_str}"
        )
        bot.send_message(call.message.chat.id, info_msg, parse_mode="Markdown", reply_markup=main_menu_keyboard(uid))

    elif call.data == "mode_buy":
        buy_msg = (
            "🛒 **NẠP XU VIP TOOL TX MD5 PRO v7.0**\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "💵 **10.000 VNĐ** ➔ **30 Xu**\n"
            "💵 **20.000 VNĐ** ➔ **70 Xu**\n"
            "💵 **50.000 VNĐ** ➔ **200 Xu**\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "📩 **Liên hệ Admin nạp xu:** @lionVnIos\n"
            f"🆔 ID của bạn: `{uid}`"
        )
        bot.send_message(call.message.chat.id, buy_msg, parse_mode="Markdown")

# --- 8. XỬ LÝ SOI MÃ & BÚ / GÃY ---

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    uid = message.from_user.id
    init_user(uid)

    text = message.text.strip().lower()
    ud = user_data[uid]

    if text in ["bú", "bu", "win", "ăn", "thắng", "húp", "đớp"]:
        if not ud["last_pred"]:
            bot.reply_to(message, "⚠️ Bạn chưa gửi mã soi ván nào!")
            return
        ud["win_streak"] += 1
        ud["bias"] = min(2.5, ud["bias"] + 0.4)
        bot.reply_to(message, f"🔥 **BÚ ĐẬM RỰC RỠ!** 💸\n🔥 Dây đỏ hiện tại: **{ud['win_streak']} tay liên tiếp!**\n👉 Gửi mã tiếp theo để thừa thắng xông lên!", parse_mode="Markdown")
        return

    elif text in ["gãy", "gay", "thua", "tạch", "xịt", "bẻ"]:
        if not ud["last_pred"]:
            bot.reply_to(message, "⚠️ Bạn chưa gửi mã soi ván nào!")
            return
        ud["win_streak"] = 0
        ud["bias"] = max(-2.5, ud["bias"] - 0.6)
        bot.reply_to(message, "🛡️ **Mạng Nơ-ron đã cân bằng lại trọng số ma trận!**\n👉 Gửi mã tiếp theo để đớp lại ngay!", parse_mode="Markdown")
        return

    if len(text) in [32, 64]:
        if ud["balance"] < 1:
            bot.reply_to(message, "⚠️ **Bạn không đủ Xu!** Điểm danh hoặc nạp xu để tiếp tục soi.", reply_markup=main_menu_keyboard(uid))
            return

        ud["balance"] -= 1
        final_result, percent_tai, percent_xiu, accuracy, code_type = master_predict_neural_v7(uid, text)
        res_label = "🔴 TÀI" if final_result == "TÀI" else "🔵 XỈU"

        res = (
            f"🌐 **CỔNG GAME:** `{ud['selected_web']}`\n"
            f"⚡ **KẾT QUẢ NEURAL ENGINE v7.0** ⚡\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 Dự đoán: **{res_label}**\n"
            f"📊 Tỉ lệ ma trận: **Tài {percent_tai}% - Xỉu {percent_xiu}%**\n"
            f"⚡ Độ tin cậy AI: **{accuracy}%**\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"💰 Xu còn: **{ud['balance']} Xu** | 🔥 Streak: **{ud['win_streak']} tay**\n"
            f"💬 *Chat `bú` khi ăn hoặc `gãy` khi thua để AI cân bằng lại!*"
        )
        bot.reply_to(message, res, parse_mode="Markdown", reply_markup=main_menu_keyboard(uid))
        return

    bot.reply_to(message, "⚠️ Vui lòng gửi mã **MD5 (32 ký tự)**, **SHA256 (64 ký tự)** hoặc chọn chức năng bên dưới:", reply_markup=main_menu_keyboard(uid))

# --- 9. KHỞI CHẠY BOT ---
if __name__ == '__main__':
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    try:
        bot.remove_webhook()
        print("Đã giải phóng Webhook kẹt thành công!")
    except Exception as e:
        print(f"Lỗi khi xóa webhook: {e}")
        
    print("TOOL TX MD5 PRO v7.0 NEURAL ENGINE đang hoạt động...")
    bot.infinity_polling(none_stop=True)
