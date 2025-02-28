from fastapi import FastAPI, Request
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

app = FastAPI()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


async def send_telegram_message(message: str):
    tg_msg = {"chat_id":CHAT_ID, "text": message, "parse_mode": "Markdown"}
    API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        await client.post(API_URL, json=tg_msg)
    
@app.post("/github-webhook/")
async def handle_github_webhook(req: Request):

    body = await req.json()
    
    if body.get("action") in ["opened", "closed", "reopened"]:
        issue = body.get("issue", {})
        repo = body.get("repository", {})
        
        
        message = f"""
        📢 *New Issue Update in* [{repo['name']}]({repo['html_url']}):

        🔹 *Title:* *{issue['title']}*  
        🔹 *Status:* *{body['action']}*  
        🔹 *URL:* [Click here]({issue['html_url']})  
        🔹 *Author:* _{issue['user']['login']}_ 
        """
        
        await send_telegram_message(message)
        return {"status": "success"}
    
    return {"status": "ignored"}

@app.post("/test-bot-message/")
async def send_test_message(req: Request):
    test_message = """
        Test Message from GitHub Webhook Bot:
        • Bot is working correctly
        • Webhook endpoint is accessible
        • Telegram integration is functioning
        """
    try:
        await send_telegram_message(test_message)
        return {"status": "success", "message": "Test message sent successfully", "test_message":test_message}
    except Exception as e:
        return {"status": "error", "message": f"Failed to send test message: {str(e)}"} 


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8099, reload=True)