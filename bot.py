from dotenv import load_dotenv
import os
import time
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from selenium.webdriver.chrome.service import Service

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service("/usr/bin/chromedriver")  # সঠিক path
    driver = webdriver.Chrome(service=service, options=options)
    return driver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("\U0001F44B হ্যালো! একটি ছবি পাঠান, আমি সেটি প্রসেস করবো।")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_path = f"downloads/{photo.file_id}.jpg"
    os.makedirs("downloads", exist_ok=True)
    await file.download_to_drive(file_path)
    await update.message.reply_text("\U0001F4E4 ছবি পেয়েছি! এখন প্রসেস করছি...")

    driver = get_driver()
    driver.get("https://betterimage.ai/")

    try:
        upload_input = driver.find_element(By.XPATH, '//input[@type="file"]')
        abs_path = os.path.abspath(file_path)
        upload_input.send_keys(abs_path)
        time.sleep(15)

        result_image = driver.find_element(By.XPATH, '//*[@id="result-image"]')
        image_url = result_image.get_attribute("src")

        await update.message.reply_photo(image_url, caption="\u2705 প্রসেস শেষ! আপনার ছবি প্রস্তুত।")

    except Exception as e:
        await update.message.reply_text(f"❌ একটি সমস্যা হয়েছে: {str(e)}")

    finally:
        driver.quit()
        if os.path.exists(file_path):
            os.remove(file_path)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()

if __name__ == "__main__":
    main()
