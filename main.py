# pip install fastapi "uvicorn[standard]"
# nohup python -m uvicorn main:app --host 0.0.0.0 --port 1234 >r.log >&1 &
import base64
import datetime
import os
from typing import List

import uvicorn
from fastapi import FastAPI, WebSocket

app = FastAPI()

# 用于存储所有连接的WebSocket对象
connected_clients: List[WebSocket] = []

if not os.path.exists('./save_file'):
    os.mkdir('save_file')


@app.get("/")
def root():
    return f"你好，现在的时间是{datetime.datetime.now()}"


@app.websocket("/ws_bytes")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # 连接建立时，将WebSocket对象添加到列表中
    connected_clients.append(websocket)
    try:
        while True:
            # 接收从客户端发送的消息
            data = await websocket.receive_text()
            if '文件名' in data:
                print(f'开始准备接收文件:{data}')
                received_data = await websocket.receive_text()
                with open(f"./save_file/{data.split('件名:')[-1]}", 'wb') as f:
                    f.write(base64.b64decode(received_data.encode("utf-8")))
                await websocket.send_text(f'已经收到文件,保存成功{data}')
                # 在这里你可以处理接收到的数据，例如，将文件同步到其他客户端
                # 这里简化为将接收到的数据广播到所有其他客户端
                for client in connected_clients:
                    if client != websocket:
                        await client.send_text(data)  # 先发送文件名称
                        await client.send_text(received_data)  # 再发送文件内容
            else:
                print(data)
    except Exception as e:
        print(e)
    finally:
        # 连接关闭时，从列表中移除WebSocket对象
        connected_clients.remove(websocket)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8081)
