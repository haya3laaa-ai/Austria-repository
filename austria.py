import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

TOKEN = "8366351345:AAHhuaBH5dLwtAXzPQH2Wm6XtgcMjbUmxw4"
CHAT_ID = "7943267388"
URL = "https://www.google.com" # غيره لرابط المواعيد الحقيقي

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": text})

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

send_msg("🚀 البوت بدأ يراقب المواعيد الآن..")

try:
    for _ in range(50): # بيلف 50 مرة (مرة كل دقيقة تقريباً)
        driver.get(URL)
        if "Available" in driver.page_source or "موعد" in driver.page_source:
            send_msg("🔔 الحق! فيه مواعيد ظهرت!")
        time.sleep(60)
finally:
    driver.quit()
