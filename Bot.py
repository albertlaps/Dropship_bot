import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Get token from Render environment
TOKEN = os.environ.get("API_TOKEN")

if not TOKEN:
    raise ValueError("API_TOKEN environment variable not set")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Dropshipping bot is running!")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot started successfully...")
    app.run_polling()

if __name__ == "__main__":
    main()
