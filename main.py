# pip install fastapi "uvicorn[standard]"
import base64
import datetime
import random
from typing import List

import uvicorn
from fastapi import FastAPI, WebSocket

app = FastAPI()

# 用于存储所有连接的WebSocket对象
connected_clients: List[WebSocket] = []


@app.get("/")
def root():
    return f"你好，现在的时间是{datetime.datetime.now()}"


@app.websocket("/ws_bytes")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # 接受连接
    received_data = await websocket.receive_text()
    print("接收完成")
    with open(f"a_{random.randint(1, 1212)}.txt", 'wb') as f:
        f.write(base64.b64decode(received_data.encode("utf-8")))
    await websocket.send_text(f"已经收到文件")  # 发送确认消息


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
