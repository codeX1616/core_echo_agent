from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import asyncio
import json

app = FastAPI()

@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")

# Mount static files for the frontend
app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")

clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages from UI if needed
    except Exception as e:
        print(f"WS error: {e}")
    finally:
        clients.remove(websocket)

async def broadcast_state(state: str, payload: dict):
    message = json.dumps({"state": state, "payload": payload})
    for client in clients:
        await client.send_text(message)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
