from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
import json
import os

# ==== CONFIG ====
BOT_TOKEN = "8041970588:AAF-JWIQ2RCVOk2eTzHGnP-J2POMsLumfNw"
ADMIN_ID = 6510862052  # Only this ID can use /broadcast

# Links
CHANNEL_LINK = "https://t.me/TeamRajendra_Forton"
REFERRAL_LINK = "https://forton.app/?ref=41"
WHATSAPP_LINK = "https://chat.whatsapp.com/ItJyNXJ9q1mGWvBjsXKaGd?mode=ac_t"
SITE_LINK = "https://forton.app"
IMAGE_URL = "https://files.catbox.moe/75y6rr.jpg"

# File to store users
USERS_FILE = "users.json"

# Load or create users list
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
else:
    users = []

# === Save users to file ===
def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# === /start Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users:
        users.append(user_id)
        save_users()

    keyboard = [
        [InlineKeyboardButton("Referral Link", url=REFERRAL_LINK)],
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
        caption="❤️ Welcome to *Team Rajendra Singh!*",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# === Broadcast Steps ===
ASK_PHOTO = 1

async def broadcast_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ You are not allowed to use this command.")
        return ConversationHandler.END

    await update.message.reply_text("📸 Please send me the photo with caption to broadcast.")
    return ASK_PHOTO

async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("❌ Please send a valid photo.")
        return ASK_PHOTO

    photo_file_id = update.message.photo[-1].file_id
    caption = update.message.caption or ""

    sent_count = 0
    for user_id in users:
        try:
            await context.bot.send_photo(chat_id=user_id, photo=photo_file_id, caption=caption)
            sent_count += 1
        except:
            pass

    await update.message.reply_text(f"✅ Broadcast sent to {sent_count} users.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Broadcast cancelled.")
    return ConversationHandler.END

# === Main Bot App ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Start Command
    app.add_handler(CommandHandler("start", start))

    # Broadcast Conversation
    broadcast_handler = ConversationHandler(
        entry_points=[CommandHandler("broadcast", broadcast_start)],
        states={
            ASK_PHOTO: [MessageHandler(filters.PHOTO & ~filters.COMMAND, receive_photo)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(broadcast_handler)

    print("🤖 Bot is running...")
    app.run_polling()
    