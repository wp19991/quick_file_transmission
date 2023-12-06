import asyncio
import datetime
import os

import aiohttp

from task_define import websocket_task

need_tongbu_file_path = r'./app_get_client_1_同步文件夹'
username = "xiaomin"
password = "xiaomin"
ws_url = "http://123.60.39.103:1234/ws_bytes"
task = websocket_task()

if not os.path.exists(need_tongbu_file_path):
    os.mkdir(need_tongbu_file_path)


async def user_login(ws):
    try:
        send_str = task.login(username=username, password=password)
        await ws.send_str(send_str)
        msg = await ws.receive_str()  # 接收服务器的确认消息
        task_info = task.get_task_info(msg)
        if task_info['task'] == 'login' and task_info['status'] == 'ok':
            print(f"登录成功: {task_info['data']['authentication']}")
            authentication = task_info['data']['authentication']
            return authentication
        else:
            print(f"登录失败:{task_info['status']}")
            return ""
    except:
        return ""


async def app_get_client():
    """
    接收的客户端
    """
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(ws_url, max_msg_size=56577720) as ws:
            # 连接首先进行登录
            authentication = await user_login(ws)
            if authentication == "":
                return
            while True:
                # await ws.send_str(task.ping())
                # time.sleep(20)
                msg = await ws.receive_str(timeout=999999999)
                task_info = task.get_task_info(msg)
                if task_info['task'] == 'transmission_file':
                    file_name = task_info['data']['file_name']
                    file_bytes = task.base64str_to_bytes(task_info['data']['file_base64_data'])
                    with open(os.path.join(need_tongbu_file_path, file_name), 'wb') as f:
                        f.write(file_bytes)
                    print(f"{datetime.datetime.now()}同步文件成功:{file_name}")
                elif task_info['task'] == 'transmission_word':
                    word = task_info['data']
                    print(f"{datetime.datetime.now()}同步消息:{word}")


asyncio.run(app_get_client())
