import asyncio
import base64
import os.path

import aiohttp

if not os.path.exists('./get_file'):
    os.mkdir('get_file')


async def send_file_via_websocket():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect("http://123.60.39.103:1234/ws_bytes", max_msg_size=56577720) as ws:
            while True:
                # 接收从客户端发送的消息
                data = await ws.receive_str()
                if '文件名' in data:
                    print(f'开始准备接收文件{data}')
                    received_data = await ws.receive_str()
                    with open(f"./get_file/{data.split('件名:')[-1]}", 'wb') as f:
                        f.write(base64.b64decode(received_data.encode("utf-8")))
                    await ws.send_str(f'已经收到文件保存成功,{data}')


asyncio.run(send_file_via_websocket())
