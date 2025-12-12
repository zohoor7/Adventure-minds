# **GuardianEye AI**

**AI-powered security camera with real-time person detection, automatic event recording, and Telegram alerts.**

GuardianEye AI is an intelligent security system that uses **YOLOv8** for real-time person detection.
When a person is detected:

✔ Saves a snapshot in `/intruders`
✔ Starts recording a video only during the event (no continuous recording)
✔ Sends a Telegram alert message
✔ Saves the recorded video in `/recordings`

---

## 🚀 Features

* Real-time camera stream
* Person detection using YOLOv8
* Auto-recording only when a person is detected
* Alert system via Telegram (text only or image)
* Saves intruder snapshots
* Saves event videos in a dedicated folder


## 📌 Requirements

```
opencv-python
ultralytics
requests
```

Install them using:

```bash
pip install -r requirements.txt
```

---

## 📷 Folder Structure

```
GuardianEye-AI/
│
├── intruders/      # Saved intruder images
├── recordings/     # Videos recorded during detection
├── detection.py    # Main script
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run

Run the main script:

```bash
python detection.py
```

Press **Q** to stop the system.

---

## 🔧 Telegram Setup

1. Create a bot via **@BotFather**
2. Get your **BOT TOKEN**
3. Get your **CHAT ID** via:

```
https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
```

4. Put them in `detection.py`:

```python
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
```

---

## 🧠 YOLOv8 Model

The project uses YOLOv8 nano model:

```
yolov8n.pt
```

You can replace it with stronger models (yolov8s, yolov8m, …)

---

## 📹 Demo

(![intruder_20251211_073142](https://github.com/user-attachments/assets/c8a135d9-379f-42fa-b0da-4c593e94e422)
)

## 🛠 Future Improvements

* Face recognition
* Send image + video together to Telegram
* Add web dashboard
* Add motion-only detection


## 📄 License

MIT License.


