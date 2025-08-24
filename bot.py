import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask, request
import asyncio
import threading

app = Flask(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    channel_link = os.getenv('CHANNEL_LINK', 'https://t.me/default_channel')
    keyboard = [[InlineKeyboardButton("Join Channel", url=channel_link)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Click the button below to join the channel:', reply_markup=reply_markup)

async def main():
    token = os.getenv('BOT_TOKEN')
    if not token:
        raise ValueError("BOT_TOKEN environment variable is not set.")

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler('start', start))

    # Set webhook
    webhook_url = os.getenv('WEBHOOK_URL')
    if not webhook_url:
        raise ValueError("WEBHOOK_URL environment variable is not set.")
    
    await application.bot.set_webhook(url=webhook_url)
    return application

# Flask route to handle webhook updates
@app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return '', 200

def run_flask():
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8443)))

if __name__ == '__main__':
    # Initialize the Telegram application
    application = asyncio.run(main())
    
    # Run Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    
    # Run the Telegram application
    asyncio.run(application.run_polling())  # Fallback for local testing
