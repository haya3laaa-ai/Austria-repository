import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


TOKEN = "8366351345:AAHhuaBH5dLwtAXzPQH2Wm6XtgcMjbUmxw4"

CHAT_ID = "7943267388" 

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error sending to Telegram: {e}")


options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")



def check_appointments():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        print(f"[{time.strftime('%H:%M:%S')}] جاري فحص المواعيد...")
        driver.get("https://appointment.bmeia.gv.at/")
        time.sleep(5)

       
        office_select = Select(driver.find_element(By.ID, "Office"))
        office_select.select_by_visible_text("Kairo")
        driver.find_element(By.ID, "buttonNext").click()
        time.sleep(3)

       
        appointment_type = Select(driver.find_element(By.ID, "CalendarId"))
        appointment_type.select_by_index(1) 
        driver.find_element(By.ID, "buttonNext").click()
        time.sleep(5)

    
        page_text = driver.page_source
       
        no_slots_keywords = ["Keine Termine verfügbar", "No appointments available", "لا توجد مواعيد"]
        
        found = True
        for word in no_slots_keywords:
            if word in page_text:
                found = False
                break
        
        if found:
            send_telegram(" إنذار عاجل: ظهرت مواعيد في سفارة النمسا! ادخل احجز الآن فوراً!")
            print("!!! تم العثور على موعد !!!")
        else:
            print("لا توجد مواعيد متاحة حالياً.")

    except Exception as e:
        print(f"حدث خطأ أثناء الفحص: {e}")
    finally:
        driver.quit()
