import os
import tempfile
from io import BytesIO
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ContextTypes
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# .env থেকে Bot Token লোড করা
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# BetterImage.ai এর জন্য ছবি আপলোড ফাংশন
def process_image_with_betterimage(image_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # ক্রোমের UI ছাড়া চালানো
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get("https://betterimage.ai/")
    upload_button = driver.find_element(By.ID, "upload-button")
    upload_button.send_keys(image_path)

    # প্রসেসিং শেষ হলে, প্রাপ্ত ফলাফল ডাউনলোড করতে হবে
    result_image = driver.find_element(By.CLASS_NAME, "download-button")
    result_image.click()

    # অপেক্ষা করুন, তারপর ইমেজ URL থেকে ফাইল ডাউনলোড করুন (এই কোডটি ধরে যে আপনি URL পাবেন)
    driver.quit()

    return result_image

# টেলিগ্রাম বটের হ্যান্ডলারের কোড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হ্যালো! ছবি আপলোড করুন যাতে আমি প্রক্রিয়া করতে পারি।")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    image_bytes = await file.download_as_bytearray()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(image_bytes)
        temp_file_path = temp_file.name

    await update.message.reply_text("📤 প্রসেসিং শুরু হচ্ছে, একটু অপেক্ষা করুন...")

    processed_image = process_image_with_betterimage(temp_file_path)

    os.remove(temp_file_path)

    if processed_image:
        await update.message.reply_photo(photo=processed_image, caption="✅ এটি আপনার প্রসেস করা ছবি!")
    else:
        await update.message.reply_text("❌ ছবি প্রসেস করতে সমস্যা হয়েছে। আবার চেষ্টা করুন।")

def main():
    updater = Updater(BOT_TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_image))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
