import os
import threading
from fastapi import FastAPI
import uvicorn
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/default_channel")

# --- Telegram Bot ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Join Our Channel 📢", url=CHANNEL_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Click the button below to join our channel:", reply_markup=reply_markup)

def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

# --- Web Server (for Render health check) ---
fastapi_app = FastAPI()

@fastapi_app.get("/healthz")
def healthz():
    return {"status": "ok"}

def run_web():
    uvicorn.run(fastapi_app, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))

# --- Run both bot + web ---
if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    run_web()
