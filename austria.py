import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- إعداداتك ---
TOKEN = "8366351345:AAHhuaBH5dLwtAXzPQH2Wm6XtgcMjbUmxw4"
CHAT_ID = "7943267388"
URL_TO_CHECK = "https://www.google.com" # استبدل ده برابط المواعيد الحقيقي

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message})

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

start_time = time.time()
# هيشتغل لمدة 55 دقيقة (عشان ميتخطاش وقت جيت هاب المسموح)
while (time.time() - start_time) < 3300: 
    try:
        driver.get(URL_TO_CHECK)
        time.sleep(5) # استراحة بسيطة لتحميل الصفحة
        
        # المنطق: لو كلمة "Available" أو "موعد" ظهرت
        if "Available" in driver.page_source or "موعد" in driver.page_source:
            send_telegram("🔔 الحق! المواعيد ظهرت دلوقتي!")
            print("🚨 مواعيد متاحة!")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] لا يوجد مواعيد...")
            
    except Exception as e:
        print(f"خطأ: {e}")
    
    time.sleep(60) # انتظر دقيقة قبل الفحص الجاي

driver.quit()

