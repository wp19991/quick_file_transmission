# pip install fastapi "uvicorn[standard]"
# nohup python -m uvicorn app_server:app --host 0.0.0.0 --port 1234 >r.log >&1 &
# ps -few | grep python
import datetime
import hashlib
import os
from typing import List

from fastapi import FastAPI, WebSocket

from task_define import websocket_task

app = FastAPI()

# 用于存储所有连接的WebSocket对象
connected_clients: List[WebSocket] = []
# 准们用来处理任务的模块
task = websocket_task()
# 允许登录的用户
user_list = [{"username": "admin", "password": "adminadminadmin"},
             {"username": "xiaomin", "password": "xiaomin"}]


def get_authentication(username: str, password: str):
    for i in user_list:
        if i['username'] == username and \
                i['password'] == password:
            return hashlib.md5(i['password'].encode(encoding='UTF-8')).hexdigest()
    return ""


def is_authentication(authentication: str):
    for i in user_list:
        t_md5 = hashlib.md5(i['password'].encode(encoding='UTF-8')).hexdigest()
        if t_md5 == authentication:
            return True
    return False


def log_print(t_str):
    print(t_str)
    with open('log_print.txt', 'a', encoding='utf-8') as f:
        f.write(str(t_str))
        f.write('\n')


# 用来保存文件到服务器的这个文件夹
save_path = './save_file'
if not os.path.exists(save_path):
    os.mkdir(save_path)


@app.get("/")
def root():
    return f"现在的时间是:[{datetime.datetime.now()}]"


@app.websocket("/ws_bytes")
async def websocket_endpoint(websocket: WebSocket):
    global connected_clients
    await websocket.accept()  # 建立连接
    try:
        while True:
            # 接收从客户端发送的消息
            log_print("当前在线用户 " + str(len(connected_clients)))
            data = await websocket.receive_text()
            task_info = task.get_task_info(data)
            res_data = ""
            if task_info['task'] == 'login':
                # 登录的操作
                log_print("开始登录 " + str(task_info))
                t_authentication = get_authentication(task_info['data']['username'], task_info['data']['password'])
                if t_authentication == "":
                    res_data = task.return_task_status(task_name='login', status='no', data="")
                else:
                    res_data = task.return_task_status(task_name='login', status='ok', data={
                        "username": task_info['data']['username'],
                        "authentication": t_authentication
                    })
                    connected_clients.append(websocket)  # 登录成功，将WebSocket对象添加到列表中
            elif task_info['task'] == 'transmission_file':
                # 传递文件
                log_print("传递文件 " + str(task_info['data']['file_name']))
                if not is_authentication(task_info['authentication']):
                    # 没有验证成功
                    res_data = task.return_task_status(task_name='transmission_file', status='no')
                else:
                    # 开始任务
                    file_name = task_info['data']['file_name']
                    file_base64_data = task_info['data']['file_base64_data']
                    file_bytes = task.base64str_to_bytes(file_base64_data)
                    with open(os.path.join(save_path, file_name), 'wb') as f:
                        f.write(file_bytes)
                    # 将这个文件转发到其他连接的客户端
                    transmission_data = task.return_task_status(task_name='transmission_file', status="ok", data={
                        "file_name": file_name,
                        "file_base64_data": file_base64_data
                    })
                    connected_clients_copy = connected_clients.copy()
                    for i, client in enumerate(connected_clients_copy):
                        if client != websocket:
                            try:
                                await client.send_text(transmission_data)
                            except:
                                log_print(f"这个用户{str(client.__dict__)}掉线了，跳过")
                    # 发送成功信息
                    res_data = task.return_task_status(task_name='transmission_file', status="ok")
            elif task_info['task'] == 'transmission_word':
                # 传递字符串
                log_print("传递字符串 " + str(task_info))
                if not is_authentication(task_info['authentication']):
                    # 没有验证成功
                    res_data = task.return_task_status(task_name='transmission_word', status='no')
                else:
                    # 开始任务
                    word = task_info['data']
                    # 将这个文件转发到其他连接的客户端
                    transmission_data = task.return_task_status(task_name='transmission_word',
                                                                status="ok",
                                                                data=word)
                    connected_clients_copy = connected_clients.copy()
                    for i, client in enumerate(connected_clients_copy):
                        if client != websocket:
                            try:
                                await client.send_text(transmission_data)
                            except:
                                log_print(f"这个用户{str(client.__dict__)}掉线了，跳过")
                    # 发送成功信息
                    res_data = task.return_task_status(task_name='transmission_word', status="ok")
            elif task_info['task'] == 'upload_file':
                # 上传文件
                log_print("上传文件 " + str(task_info['data']['file_name']))
                if not is_authentication(task_info['authentication']):
                    # 没有验证成功
                    res_data = task.return_task_status(task_name='upload_file', status='no')
                else:
                    # 开始任务
                    file_name = task_info['data']['file_name']
                    file_base64_data = task_info['data']['file_base64_data']
                    file_bytes = task.base64str_to_bytes(file_base64_data)
                    with open(os.path.join(save_path, file_name), 'wb') as f:
                        f.write(file_bytes)
                    # 发送成功信息
                    res_data = task.return_task_status(task_name='upload_file', status="ok")
            elif task_info['task'] == 'download_file':
                pass
            elif task_info['task'] == 'ping':
                # 返回消息
                res_data = task.return_task_status(task_name='ping', status="ok")
            else:
                log_print("非法任务，执行失败")
                res_data = task.return_task_status(task_name='fail_login', status="no")
            # 发送任务结束状态信息
            log_print(f"发送{task_info['task']}任务结束状态信息")
            await websocket.send_text(res_data)
    except Exception as e:
        log_print(e)
        connected_clients.remove(websocket)
    finally:
        # 连接关闭时，从列表中移除WebSocket对象
        connected_clients.remove(websocket)

# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(app, host="0.0.0.0", port=8081)
