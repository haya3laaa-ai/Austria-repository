import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

# --- بياناتك الخاصة ---
TOKEN = "8366351345:AAHhuaBH5dLwtAXzPQH2Wm6XtgcMjbUmxw4"
CHAT_ID = "7943267388"
URL = "https://appointment.bmeia.gv.at/?Office=Kairo"

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": text})
    except:
        print("خطأ في إرسال التليجرام")

# إعدادات المتصفح المخفي
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--lang=ar")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    send_msg("🚀 البوت بدأ فحص مواعيد (بكالوريوس - القاهرة) الآن..")
    
    # يلف لمدة 55 دقيقة (تقريباً لفة كل دقيقة)
    for i in range(55):
        try:
            driver.get(URL)
            time.sleep(5)
            
            # الخطوة 1: اختيار Bachelor
            calendar_select = Select(driver.find_element("id", "CalendarId"))
            calendar_select.select_by_visible_text("Aufenthaltsbewilligung Student (nur Bachelor)")
            time.sleep(1)
            driver.find_element("name", "Next").click()
            time.sleep(3)
            
            # الخطوة 2: تخطي صفحة المعلومات
            driver.find_element("name", "Next").click()
            time.sleep(4)
            
            # الخطوة 3: فحص النص في الصفحة الأخيرة
            page_text = driver.page_source
            target_msg = "لا توجد حاليا مواعيد متاحة لاختيارك"
            
            if target_msg not in page_text:
                send_msg(f"🔔 عاجل!!! المواعيد ظهرت أو الجملة الحمراء اختفت! ادخل فوراً:\n{URL}")
                print("🚨 مبروك! المواعيد فتحت!")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] لا يوجد مواعيد (الجملة الحمراء موجودة)")
                
        except Exception as e:
            print(f"حدث خطأ في اللفة {i}: {e}")
            
        time.sleep(60)

finally:
    driver.quit()
