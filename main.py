from fastapi import FastAPI, BackgroundTasks, Request, Response
import uvicorn
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

ZALO_ACCESS_TOKEN = os.getenv("ZALO_ACCESS_TOKEN")

# Trang HTML xác thực chuẩn Zalo
HTML_CONTENT = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="zalo-platform-site-verification" content="OS6n3-laP0uCqE5Kp_9pTapI-aAWcl4VDJOv" />
    <title>Zalo Verification</title>
</head>
<body>
    There Is No Limit To What You Can Accomplish Using Zalo!
</body>
</html>"""

# Trả về HTML thô chuẩn cho trang chủ và mọi file .html
@app.get("/")
def home():
    return Response(content=HTML_CONTENT, media_type="text/html", status_code=200)

@app.get("/{filename:path}")
def verify_zalo_all(filename: str):
    return Response(content=HTML_CONTENT, media_type="text/html", status_code=200)

# Route Webhook nhận tin nhắn
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
