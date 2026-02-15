import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ✅ Read bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")

# ✅ File to store product data
DATA_FILE = "products.json"

# Load products from file
def load_products():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save products to file
def save_products(products):
    with open(DATA_FILE, "w") as f:
        json.dump(products, f, indent=2)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Dropshipping Bot is running!\nUse /addproduct, /listproducts, /profit"
    )

# /addproduct command: /addproduct name cost selling_price
async def addproduct(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 3:
        await update.message.reply_text("Usage: /addproduct name cost selling_price")
        return
    
    name, cost, selling = args
    try:
        cost = float(cost)
        selling = float(selling)
    except ValueError:
        await update.message.reply_text("Cost and selling price must be numbers.")
        return

    products = load_products()
    products.append({
        "name": name,
        "cost": cost,
        "selling_price": selling
    })
    save_products(products)
    await update.message.reply_text(f"✅ Product '{name}' added successfully!")

# /listproducts command
async def listproducts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = load_products()
    if not products:
        await update.message.reply_text("No products added yet.")
        return
    
    msg = "📦 Products:\n"
    for p in products:
        msg += f"- {p['name']}: Cost R{p['cost']}, Selling R{p['selling_price']}\n"
    await update.message.reply_text(msg)

# /profit command
async def profit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = load_products()
    if not products:
        await update.message.reply_text("No products added yet.")
        return
    
    total_cost = sum(p["cost"] for p in products)
    total_selling = sum(p["selling_price"] for p in products)
    total_profit = total_selling - total_cost

    await update.message.reply_text(
        f"💰 Total Cost: R{total_cost}\n"
        f"💵 Total Selling: R{total_selling}\n"
        f"🤑 Total Profit: R{total_profit}"
    )

# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addproduct", addproduct))
    app.add_handler(CommandHandler("listproducts", listproducts))
    app.add_handler(CommandHandler("profit", profit))
    
    print("Bot started successfully...")
    app.run_polling()  # Keeps the bot alive

if __name__ == "__main__":
    main()
