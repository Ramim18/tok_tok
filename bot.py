from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "8142140049:AAEzCKEp-leIZAiIppTv8hZBZUY7ZY-ns2Q"  # এখানে আপনার টেলিগ্রাম বট টোকেন বসান

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 হ্যালো! একটি ছবি পাঠান, আমি সেটি প্রসেস করবো।")

# Image handler
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📤 ছবি পেয়েছি! এখন প্রসেস করছি...")

    # এখানে আপনি আপনার ওয়েবসাইটে ছবি পাঠানোর প্রসেস যুক্ত করবেন
    # উদাহরণ: selenium দিয়ে betterimage.ai-তে আপলোড করা

    await update.message.reply_text("✅ প্রসেস শেষ! আপনার ছবি প্রস্তুত।")

# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    app.run_polling()

if __name__ == "__main__":
    main()
