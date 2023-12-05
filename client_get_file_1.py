import asyncio
import base64
import os

import aiohttp

need_tongbu_file_path = r'./同步文件夹1'

if not os.path.exists(need_tongbu_file_path):
    os.mkdir(need_tongbu_file_path)


async def send_file_via_websocket():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect("http://123.60.39.103:1234/ws_bytes", max_msg_size=56577720) as ws:
            while True:
                # 接收从客户端发送的消息
                data = await ws.receive_str()
                if '文件名' in data:
                    print(f'开始准备接收文件{data}')
                    received_data = await ws.receive_str()
                    save_path = os.path.join(need_tongbu_file_path, data.split('件名:')[-1])
                    with open(save_path, 'wb') as f:
                        f.write(base64.b64decode(received_data.encode("utf-8")))
                    await ws.send_str(f'已经收到文件保存成功,{data}')


asyncio.run(send_file_via_websocket())
