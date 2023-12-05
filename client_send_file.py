import asyncio
import base64
import os.path

import aiohttp


async def send_file_via_websocket():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect("http://123.60.39.103:1234/ws_bytes") as ws:
            while True:
                cmd_file_path = input('请输入文件路径，进行上传：')
                if os.path.exists(cmd_file_path):
                    await ws.send_str(f"文件名:{os.path.basename(cmd_file_path)}")  # 先发送文件名称
                    # 再发送文件内容
                    with open(cmd_file_path, 'rb') as f:
                        file_data = base64.b64encode(f.read()).decode("utf-8")
                        await ws.send_str(file_data)  # 发送文件到服务器
                    # 获得文件是否保存成功
                    msg = await ws.receive()  # 接收服务器的确认消息
                    print(f"收到服务器信息: {msg.data}")


asyncio.run(send_file_via_websocket())
# "C:\Users\wp\Desktop\电视台.m3u"
