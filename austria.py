import requests
import time

# بيانات التليجرام بتاعتك
TOKEN = "8366351345:AAHhuaBH5dLwtAXzPQH2Wm6XtgcMjbUmxw4"
CHAT_ID = "7943267388"

def send_alert(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    # هيبعتلك 15 رسالة ورا بعض عشان الصوت يفضل شغال وتصحى فوراً
    for _ in range(15):
        try:
            requests.post(url, json={"chat_id": CHAT_ID, "text": msg}, timeout=10)
            time.sleep(0.5)
        except:
            pass

def check():
    url = "https://appointment.bmeia.gv.at/?Office=KAIRO&QuotaId=381&Language=ar"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        r = requests.get(url, headers=headers, timeout=25)
        # لو الجملة دي مش موجودة يبقى المواعيد فتحت
        if "لا توجد حاليا مواعيد متاحة" not in r.text:
            msg = "🚨 AUSTRIA AVAILABLE! 🚨\n\n🇦🇹 مواعيد النمسا فتحت يا مصطفى!\n🔔 ادخل احجز فوراً فوراً قبل ما تخلص!"
            send_alert(msg)
            return True
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Still closed...")
    except:
        print("Connection error...")
    return False

# هيفحص 5 مرات (مرة كل دقيقة) في كل دورة تشغيل
for i in range(5):
    if check(): break
    if i < 4: time.sleep(60)
