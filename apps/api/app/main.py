from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .db import Base, engine
from .routers import matches, admin
from .services.events_bus import bus

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Matchday Intelligence Platform API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(matches.router)
app.include_router(admin.router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.websocket("/ws/matches/{match_id}")
async def match_socket(ws: WebSocket, match_id: int):
    await ws.accept()
    pubsub = bus.subscribe(match_id)
    try:
        if pubsub is None:
            await ws.send_json({"event": "info",
                                "detail": "redis unavailable; live push disabled"})
        while True:
            if pubsub is not None:
                msg = pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if msg and msg.get("type") == "message":
                    await ws.send_text(msg["data"].decode())
            await ws.receive_text()
    except WebSocketDisconnect:
        if pubsub is not None:
            pubsub.close()
