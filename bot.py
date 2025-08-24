import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

async def start(update: Update, context: CallbackContext):
    channel_link = os.getenv('CHANNEL_LINK', 'https://t.me/default_channel')  # Fallback if not set
    keyboard = [[InlineKeyboardButton("Join Channel", url=channel_link)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Click the button below to join the channel:', reply_markup=reply_markup)

def main():
    token = os.getenv('BOT_TOKEN')
    if not token:
        raise ValueError("BOT_TOKEN environment variable is not set.")
    
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler('start', start))
    application.run_polling()

if __name__ == '__main__':
    main()
