from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json
import os

# ================= CONFIG =================
BOT_TOKEN = "8041970588:AAF-JWIQ2RCVOk2eTzHGnP-J2POMsLumfNw"

CHANNEL_LINK = "https://t.me/TeamRajendra_Forton"
REFERRAL_LINK = "https://forton.app/?ref=41"
WHATSAPP_LINK = "https://chat.whatsapp.com/ItJyNXJ9q1mGWvBjsXKaGd?mode=ac_t"
SITE_LINK = "https://forton.app"
IMAGE_URL = "https://files.catbox.moe/75y6rr.jpg"

ADMIN_ID = 6510862052  # Your Telegram ID
USERS_FILE = "users.json"

# ========== Load users ==========
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
else:
    users = []

# ========== Save users ==========
def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# ========== /start ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users:
        users.append(user_id)
        save_users()

    keyboard = [
        [InlineKeyboardButton("Chat with us", url=REFERRAL_LINK)],
        [
            InlineKeyboardButton("YouTube Link", url=SITE_LINK),
            InlineKeyboardButton("Main Channel", url=CHANNEL_LINK)
        ],
        [InlineKeyboardButton("WhatsApp Community", url=WHATSAPP_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=IMAGE_URL,
        caption="Welcome to *ForTon!*",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# ========== /broadcast ==========
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    if len(context.args) == 0:
        await update.message.reply_text("Usage: /broadcast <message>")
        return

    message = " ".join(context.args)
    count = 0
    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
            count += 1
        except:
            pass

    await update.message.reply_text(f"✅ Broadcast sent to {count} users.")

# ========== MAIN ==========
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.run_polling()
