import json
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8041970588:AAF-JWIQ2RCVOk2eTzHGnP-J2POMsLumfNw"
OWNER_ID = "6510862052"  # Your Telegram ID
USERS_FILE = "users.json"

# Load users
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return []

# Save users
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        save_users(users)

    keyboard = [
        [InlineKeyboardButton("Join Meeting", callback_data="join_meeting")]
    ]
    await update.message.reply_photo(
        photo="https://files.catbox.moe/bqp4mc.jpg",
        caption=(
            "👋 **Welcome to the Meeting Bot!**\n\n"
            "📅 Click below to join the meeting instantly.\n"
            "🔔 Stay tuned for upcoming meeting updates."
        ),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Button handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "join_meeting":
        # Meeting page
        keyboard = [
            [InlineKeyboardButton("📌 Meeting Link", url="https://t.me/joinchat/example")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]
        await query.message.delete()
        await query.message.reply_photo(
            photo="https://files.catbox.moe/bqp4mc.jpg",
            caption="Here’s your meeting link 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "back":
        # Back to home page
        keyboard = [
            [InlineKeyboardButton("Join Meeting", callback_data="join_meeting")]
        ]
        await query.message.delete()
        await query.message.reply_photo(
            photo="https://files.catbox.moe/bqp4mc.jpg",
            caption=(
                "👋 **Welcome back to the Meeting Bot!**\n\n"
                "📅 Click below to join the meeting instantly.\n"
                "🔔 Stay tuned for upcoming meeting updates."
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# Broadcast command
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != OWNER_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    text_to_send = " ".join(context.args)
    if not text_to_send:
        await update.message.reply_text("Usage: /broadcast Your message here")
        return

    users = load_users()
    count = 0
    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=text_to_send)
            count += 1
        except:
            pass

    await update.message.reply_text(f"✅ Broadcast sent to {count} users.")

# Main function
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("broadcast", broadcast))

    app.run_polling()
