import os
import telebot
from telebot import types

TOKEN = os.getenv("8315107200:AAH2l65dwaE6rJvOo_FryWPfH3KcePdUBF0")

bot = telebot.TeleBot(TOKEN)

products_data = {
    "Product A": 120,
    "Product B": 250,
    "Product C": 90
}

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📦 Products", "💰 Profit", "ℹ️ Help")
    bot.send_message(
        message.chat.id,
        "Welcome to Dropship Bot 🤖\nChoose an option:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "📦 Products")
def products(message):
    text = "📦 Products & Profits:\n\n"
    for product, profit in products_data.items():
        text += f"{product}: R{profit}\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: message.text == "💰 Profit")
def profit(message):
    total = sum(products_data.values())
    bot.send_message(message.chat.id, f"💰 Total Profit: R{total}")

@bot.message_handler(func=lambda message: message.text == "ℹ️ Help")
def help_cmd(message):
    bot.send_message(
        message.chat.id,
        "Use the buttons to view products or profits.\nBot runs 24/7 🚀"
    )

print("🤖 Bot is running...")
bot.infinity_polling()
