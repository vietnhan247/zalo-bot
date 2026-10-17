from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.responses import PlainTextResponse, HTMLResponse
import uvicorn
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

ZALO_ACCESS_TOKEN = os.getenv("ZALO_ACCESS_TOKEN")

VERIFY_CODE = "There Is No Limit To What You Can Accomplish Using Zalo!"
VERIFY_FILENAME = "zalo_verifierOS6n3-laP0uCqE5Kp_9pTapI-aAWcl4VDJOv.html"

@app.get("/")
def home():
    return {"status": "Zalo Bot is running"}

# Đường dẫn xác thực domain Zalo (Trả về đúng định dạng Plain Text)
@app.get(f"/{VERIFY_FILENAME}", response_class=PlainTextResponse)
def verify_zalo_get():
    return VERIFY_CODE

@app.post(f"/{VERIFY_FILENAME}", response_class=PlainTextResponse)
def verify_zalo_post():
    return VERIFY_CODE

# Webhook nhận tin nhắn
@app.post("/zalo-webhook")
async def zalo_webhook(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    print("Dữ liệu nhận từ Zalo:", data)
    
    if data.get("event_name") == "user_send_text":
        user_id = data["sender"]["id"]
        user_msg = data["message"]["text"]
        background_tasks.add_task(reply_zalo, user_id, f"Bot đã nhận: {user_msg}")
        
    return {"status": "ok"}

def reply_zalo(user_id: str, text: str):
    url = "https://openapi.zalo.me/v2.0/oa/message"
    headers = {
        "access_token": ZALO_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "recipient": {"user_id": user_id},
        "message": {"text": text}
    }
    requests.post(url, json=payload, headers=headers)
