from fastapi import FastAPI, BackgroundTasks, Request
import uvicorn
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

ZALO_ACCESS_TOKEN = os.getenv("ZALO_ACCESS_TOKEN")

@app.get("/")
def home():
    return {"status": "Zalo Bot is running"}

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
