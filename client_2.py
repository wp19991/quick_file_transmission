import asyncio

import websockets


async def client():
    uri = "ws://127.0.0.1:8000/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            # 在这里可以添加逻辑以将本地文件同步到服务器
            data = input("Enter data to send to server: ")
            await websocket.send(data)
            response = await websocket.recv()
            print(f"Received from server: {response}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(client())
