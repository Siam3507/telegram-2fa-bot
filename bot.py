
import os
import pyotp
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Get token and user ID from environment variables (set these in Render)
BOT_TOKEN = os.getenv("8141689574:AAEtWLGN0d9op2us3mHqOkldl5Cc-ndVIiM")
ALLOWED_USER_ID = int(os.getenv("1106892490"))

# Handle /start command (optional)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is ready. Send /code YOUR_SECRET")

# Handle /code command
async def code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return  # silently ignore

    if not context.args:
        return  # silently ignore bad input

    secret = context.args[0]

    try:
        totp = pyotp.TOTP(secret)
        current_code = totp.now()
        await update.message.reply_text(current_code)
    except Exception:
        await update.message.reply_text("Invalid secret")

# Start the bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("code", code))
    app.run_polling()

if __name__ == '__main__':
    main()


