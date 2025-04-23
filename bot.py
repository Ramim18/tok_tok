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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Headless Chrome চালানোর জন্য Chrome Options সেট করা
options = Options()
options.headless = True  # Chrome ব্রাউজারটি headless mode এ চলবে

# Chrome ড্রাইভার ইনিশিয়ালাইজ করা
driver = webdriver.Chrome(options=options)

# নির্দিষ্ট ওয়েবসাইটে যাওয়ার জন্য
driver.get("https://betterimage.ai/")

# ওয়েব পেজের শিরোনাম প্রিন্ট করা
print(driver.title)

# কিছু সময় অপেক্ষা করা
time.sleep(5)  # ৫ সেকেন্ড অপেক্ষা

# পেজে একটি এলিমেন্টে ক্লিক বা ডেটা এক্সট্র্যাক্ট করতে পারেন
element = driver.find_element(By.TAG_NAME, "h1")
print("H1 Tag Text: ", element.text)

# ড্রাইভার বন্ধ করা
driver.quit()


# .env ফাইল থেকে টেলিগ্রাম বট টোকেন লোড করা
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")  # .env থেকে টোকেন নিয়েছি

# Selenium WebDriver সেটআপ
def get_driver():
    options = Options()
    options.add_argument("--headless")  # ব্রাউজার হেডলেস মোডে চালানো
    service = Service("chromedriver")  # চ্রোমড্রাইভার এর পথ দিন
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 হ্যালো! একটি ছবি পাঠান, আমি সেটি প্রসেস করবো।")

# ছবি প্রসেসিং ফাংশন
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file_id = photo.file_id
    file = await context.bot.get_file(file_id)
    file_url = file.file_path
    await update.message.reply_text("📤 ছবি পেয়েছি! এখন প্রসেস করছি...")

    # সেলেনিয়াম দিয়ে BetterImage.ai সাইটে ছবি আপলোড
    driver = get_driver()
    driver.get("https://betterimage.ai/")

    # ওয়েবসাইটে ছবি আপলোড করার জন্য Xpath অনুসন্ধান এবং আপলোড করা
    upload_button = driver.find_element(By.XPATH, '//input[@type="file"]')
    upload_button.send_keys(file_url)  # এখানে আপনার ছবির URL দিতে হবে
    time.sleep(10)  # কিছু সময় অপেক্ষা করবো প্রসেস করার জন্য

    # প্রসেসিং সম্পন্ন হলে সাইট থেকে রেজাল্ট পেয়ে সেটি টেলিগ্রামে পাঠানো
    result_image = driver.find_element(By.XPATH, '//*[@id="result-image"]')  # প্রাসঙ্গিক Xpath চেক করে নিন
    image_url = result_image.get_attribute('src')

    # প্রসেস শেষ হওয়ার পর ফলাফল পাঠানো
    await update.message.reply_text(f"✅ প্রসেস শেষ! আপনার ছবি প্রস্তুত। \n{image_url}")

    driver.quit()

# মূল ফাংশন
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Start কমান্ড হ্যান্ডলার
    app.add_handler(CommandHandler("start", start))

    # ছবি আপলোড এবং প্রসেস করার জন্য হ্যান্ডলার
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # বট চলাতে চালু করা
    app.run_polling()

if __name__ == "__main__":
    main()
