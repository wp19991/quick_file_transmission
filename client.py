import asyncio
import base64

import aiohttp


async def send_file_via_websocket():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect("http://127.0.0.1:8081/ws_bytes") as ws:
            with open('a.txt', 'rb') as f:
                png_data = base64.b64encode(f.read()).decode("utf-8")
                await ws.send_str(png_data)  # 发送文件到服务器
            # await ws.send_str("ok")
            msg = await ws.receive()  # 接收服务器的确认消息
            print(f"收到服务器信息: {msg.data}")
            while True:
                data = input()
            # await ws.send_str("close")  # 发送关闭消息到服务器

asyncio.run(send_file_via_websocket())
