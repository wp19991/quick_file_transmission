import asyncio
import datetime
import os

import aiohttp

from task_define import websocket_task

need_tongbu_file_path = r'./app_send_client_同步文件夹'
username = "admin"
password = "adminadminadmin"
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


async def app_send_client():
    """
    发送的客户端
    """
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(ws_url, max_msg_size=56577720) as ws:
            # 连接首先进行登录
            authentication = await user_login(ws)
            if authentication == "":
                return
            while True:
                cmd_file_path = input('请输入文件路径，或者字符串，进行传输：')
                try:
                    await ws.send_str(task.login(username=username, password=password))
                    msg = await ws.receive_str()  # 接收服务器的确认消息
                    task_info = task.get_task_info(msg)
                    print(f"[task_name:{task_info['task']}],[status: {task_info['status']}]")
                except:
                    ws = await session.ws_connect(ws_url, max_msg_size=56577720)
                    authentication = await user_login(ws)
                    print("重连成功")
                print(f"{datetime.datetime.now()}开始同步:[data:{cmd_file_path}]")
                if os.path.exists(cmd_file_path):
                    send_str = task.transmission_file(authentication=authentication, file_path=cmd_file_path)
                    await ws.send_str(send_str)
                else:
                    send_str = task.transmission_word(authentication=authentication, word=cmd_file_path)
                    await ws.send_str(send_str)
                msg = await ws.receive_str()  # 接收服务器的确认消息
                task_info = task.get_task_info(msg)
                print(f"[task_name:{task_info['task']}],[status: {task_info['status']}]")


asyncio.run(app_send_client())
# "C:\Users\wp\Desktop\fei\屏幕截图1.png"
# "C:\Users\wp\Desktop\esp\mqtt.txt"
# "C:\Users\wp\Desktop\esp\micropython固件.pptx"
