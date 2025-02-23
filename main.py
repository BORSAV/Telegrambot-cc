import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Replace with your Telegram bot token
BOT_TOKEN = "7025436155:AAEVgzljUZ7WddszJRmg2IPV2UhyJZUt-Mk"
API_URL = "http://46.202.88.147:5000/stripe={cc}"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome! Send /check {cc} to verify a card.")

def check_card(update: Update, context: CallbackContext) -> None:
    if not context.args:
        update.message.reply_text("Usage: /check 5227016351459252|10|28|174")
        return
    
    cc = context.args[0]
    response = requests.get(API_URL.format(cc=cc))
    
    if response.status_code == 200:
        data = response.json()
        result = data.get("data", {}).get("result", "Unknown")
        response_text = data.get("data", {}).get("response", "No response")
        update.message.reply_text(f"Result: {result}\nResponse: {response_text}")
    else:
        update.message.reply_text("Failed to contact API. Try again later.")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("check", check_card))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()