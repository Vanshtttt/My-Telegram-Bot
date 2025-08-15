from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8041970588:AAF-JWIQ2RCVOk2eTzHGnP-J2POMsLumfNw"

# Links & Images
CHANNEL_LINK = "https://t.me/TeamRajendra_Forton"
WHATSAPP_LINK = "https://chat.whatsapp.com/Jih0FmXvaYMFDS9xCS8Hzg"
SITE_LINK = "https://youtube.com/@rajendrasinghforton?si=EpiJf9UxmcoVHySq"
MAIN_IMAGE_URL = "https://files.catbox.moe/75y6rr.jpg"
MEETING_IMAGE_URL = "https://files.catbox.moe/bqp4mc.jpg"
MEETING_LINK = "https://meet.google.com/xyz-abc-pqr"

# -------- Start Menu --------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Join Meeting", callback_data="join_meeting")],
        [
            InlineKeyboardButton("YouTube Link", url=SITE_LINK),
            InlineKeyboardButton("Main Channel", url=CHANNEL_LINK)
        ],
        [InlineKeyboardButton("WhatsApp Community", url=WHATSAPP_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    sent_msg = await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=MAIN_IMAGE_URL,
        caption="❤️ *Team Rajendra Singh Official Bot*",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    # Save the message ID so we can delete later
    context.user_data["main_menu_msg_id"] = sent_msg.message_id

# -------- Meeting Poster Page --------
async def join_meeting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Delete main menu message if exists
    if "main_menu_msg_id" in context.user_data:
        try:
            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=context.user_data["main_menu_msg_id"])
        except:
            pass

    keyboard = [
        [InlineKeyboardButton("Back", callback_data="back_to_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    sent_msg = await context.bot.send_photo(
        chat_id=query.message.chat_id,
        photo=MEETING_IMAGE_URL,
        caption=f"📢 *Meeting Link:* [Click Here]({MEETING_LINK})",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    # Save meeting message ID so we can delete on back
    context.user_data["meeting_msg_id"] = sent_msg.message_id

# -------- Back Button --------
async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Delete meeting poster message if exists
    if "meeting_msg_id" in context.user_data:
        try:
            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=context.user_data["meeting_msg_id"])
        except:
            pass

    # Send the start menu again
    await start(update, context)

# -------- Main --------
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(join_meeting, pattern="join_meeting"))
    app.add_handler(CallbackQueryHandler(back_to_main, pattern="back_to_main"))

    app.run_polling()
