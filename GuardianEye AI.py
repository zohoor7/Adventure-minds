import cv2
import time
import os
import requests
from ultralytics import YOLO

# إعدادات Telegram

BOT_TOKEN = "   "
CHAT_ID = "   "

def send_telegram_alert(message: str):
    """Send text alert via Telegram ."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        r = requests.post(url, data=data, timeout=10)
        if r.status_code == 200:
            print("[INFO] Telegram alert sent!")
        else:
            print(f"[ERROR] Failed to send alert, status code: {r.status_code}")
    except Exception as e:
        print("[ERROR] Exception sending Telegram alert:", e)


# تحميل YOLO

model = YOLO("yolov8n.pt")  

# فتح الكاميرا

cap = cv2.VideoCapture(0)

# إعدادات التسجيل

recording = False
out = None
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

# مجلدات للصور والفيديوهات
if not os.path.exists("intruders"):
    os.makedirs("intruders")
if not os.path.exists("recordings"):
    os.makedirs("recordings")

last_alert_time = 0
alert_cooldown = 20  # انتظار 20 ثانية بين كل إشعار

print("[SYSTEM READY] Monitoring started...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # اكتشاف الأشخاص
    results = model(frame, verbose=False)

    person_detected = False
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            if cls == 0:  # 0 = شخص person
                person_detected = True
                # رسم صندوق الشخص
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)


    # بدء التسجيل عند اكتشاف شخص

    if person_detected and not recording:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        video_filename = os.path.join("recordings", f"intruder_{timestamp}.mp4")
        out = cv2.VideoWriter(video_filename, fourcc, 20.0,
                              (frame.shape[1], frame.shape[0]))

        print("[REC] Recording started:", video_filename)
        recording = True

        # حفظ صورة المتسلل
        image_path = os.path.join("intruders", f"intruder_{timestamp}.jpg")
        cv2.imwrite(image_path, frame)
        print("[IMAGE] Saved:", image_path)

        # إرسال تنبيه Telegram
        if time.time() - last_alert_time > alert_cooldown:
            send_telegram_alert(f"Intruder detected at {timestamp}")
            last_alert_time = time.time()


    # إيقاف التسجيل عند عدم وجود شخص

    if not person_detected and recording:
        print("[REC] Recording stopped")
        recording = False
        out.release()

    # تسجيل الإطارات إذا كان هناك تسجيل
    if recording:
        out.write(frame)

    cv2.imshow("Security Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# تنظيف الموارد

cap.release()
if out:
    out.release()
cv2.destroyAllWindows()

