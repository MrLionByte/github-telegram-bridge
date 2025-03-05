from fastapi import FastAPI, Request, Query
import asyncio
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

app = FastAPI()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def generate_dummy_issue(status: str):
    """Generate dummy issue data based on status."""
    return {
        "title": "Fix login issue",
        "html_url": "https://github.com/example/repo/issues/123",
        "user": {"login": "test-user"},
        "repo": {"name": "example-repo", "html_url": "https://github.com/example/repo"},
        "status": status,
    }


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
        
        if body['action'] == 'opened':
            message = f"""
            🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵
            🚀 *New Issue Created in* [{repo['name']}]({repo['html_url']})!  

            *🔹 Title:** {issue['title']}
            *📌 Status:** Opened  
            *👤 Author:** {issue['user']['login']}  
            *📎 URL:** [View Issue]({issue['html_url']})  

            📢 Check it out and contribute!
            """
            
        elif body['action'] == 'closed':
            message = f"""
            🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴
            ✅ *Issue Resolved in* [{repo['name']}]({repo['html_url']})!  

            *🔸 Title:** {issue['title']}  
            *📌 Status:** Closed  
            *🔗 URL:** [Issue Details]({issue['html_url']})  
            *🙌 Closed By:** {issue['user']['login']}  

            🎉 Great work! The issue is now closed.
            """

        elif body['action'] == 'reopened':
            message = f"""
            🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡
            ⚠️ *Issue Reopened in* [{repo['name']}]({repo['html_url']})!  

            *🔺 Title:** {issue['title']}  
            *📍 Status:** Reopened  
            *🔗 URL:** [Check Here]({issue['html_url']})  
            *🔄 Reopened By:** {issue['user']['login']}  

            🛠️ Further action is required!
            """
        else:
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

async def send_test_message(status: str = Query("opened", enum=["opened", "closed", "reopened"])):
    issue = generate_dummy_issue(status)
    
    if status == "opened":
        test_message = f"""
        🚀 *New Issue Created in {issue['repo']['name']}!*  

        🔹 *Title:* {issue['title']}  
        📌 *Status:* Opened  
        👤 *Author:* {issue['user']['login']}  
        📎 *URL:* [View Issue]({issue['html_url']})  

        📢 Check it out and contribute!
        """
    elif status == "closed":
        test_message = f"""
        ✅ *Issue Resolved in* [{issue['repo']['name']}]({issue['repo']['html_url']})!  

        🔸 *Title:* {issue['title']}  
        📌 *Status:* Closed  
        🔗 *URL:* [Issue Details]({issue['html_url']})  
        🙌 *Closed By:* {issue['user']['login']}  

        🎉 Great work! The issue is now closed.
        """
    elif status == "reopened":
        test_message = f"""
        ⚠️ *Issue Reopened in* [{issue['repo']['name']}]({issue['repo']['html_url']})!  

        🔺 *Title:* {issue['title']}  
        📍 *Status:* Reopened  
        🔗 *URL:* [Check Here]({issue['html_url']})  
        🔄 *Reopened By:* {issue['user']['login']}  

        🛠️ Further action is required!
        """
    else:
        test_message = "Invalid status. Supported values: opened, closed, reopened."
    
    try:
        await send_telegram_message(test_message)
        return {"status": "success", "message": "Test message sent successfully", "test_message": test_message}
    except Exception as e:
        return {"status": "error", "message": f"Failed to send test message: {str(e)}"}
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8099, reload=True)