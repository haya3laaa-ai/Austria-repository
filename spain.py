import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- إعدادات التليجرام ---
TOKEN = "8366351345:AAHhuaBH5dLwtAXzPQH2Wm6XtgcMjbUmxw4"
CHAT_ID = "7943267388"
URL = "https://www.citaconsular.es/es/hosteds/widgetdefault/2fc04c7d1b617198de5bb6232b70e2afa"

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": text})
    except:
        print("خطأ في إرسال التليجرام")

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    send_msg("🇪🇸 بدأ فحص مواعيد (توثيق إسبانيا) الآن.. الفحص كل دقيقة.")
    
    # يلف لمدة 55 لفة
    for i in range(55):
        try:
            driver.get(URL)
            time.sleep(10) # انتظار زيادة عشان الموقع يحمل
            
            page_source = driver.page_source
            
            # البحث عن كلمة "Hueco libre" (خانة فاضية) أو وجود ساعات
            if "Hueco libre" in page_source or "09:" in page_source or "10:" in page_source:
                send_msg(f"🔔 عاجل!!! ظهرت مواعيد توثيق في سفارة إسبانيا! ادخل احجز فوراً:\n{URL}")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] إسبانيا: لا يوجد مواعيد.")
                
        except Exception as e:
            print(f"خطأ في لفة إسبانيا {i}: {e}")
            
        time.sleep(60) # انتظر دقيقة

finally:
    driver.quit()
