import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration - Using environment variables for Render
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/your_channel")
PORT = int(os.getenv("PORT", 8080))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    
    # Create inline keyboard with redirect button
    keyboard = [[
        InlineKeyboardButton("Click to join", url=CHANNEL_URL)
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send message with button
    await update.message.reply_text(
        "Welcome! Join our main channel:",
        reply_markup=reply_markup
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    """Start the bot."""
    
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN environment variable is not set!")
        return
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handler for /start
    application.add_handler(CommandHandler("start", start))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Run the bot with webhook for production or polling for development
    if os.getenv("RENDER"):
        # Production mode with webhook (Render sets RENDER env var)
        logger.info("Starting bot in webhook mode for production...")
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=os.getenv("WEBHOOK_URL")
        )
    else:
        # Development mode with polling
        logger.info("Starting bot in polling mode for development...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
