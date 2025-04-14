from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/")
async def webhook(request: Request):
    body = await request.json()
    events = body.get("events", [])
    
    for event in events:
        # グループからのメッセージイベントか確認
        if event["type"] == "message" and event["source"]["type"] == "group":
            group_id = event["source"]["groupId"]
            print(f"Group ID: {group_id}")

    return {"status": "ok"}
