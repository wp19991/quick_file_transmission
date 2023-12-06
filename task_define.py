import base64
import json
import os
from typing import Union



class websocket_task:
    """
    json任务定义
    """

    @staticmethod
    def bytes_to_base64str(t_bytes: bytes):
        return base64.b64encode(t_bytes).decode("utf-8")

    @staticmethod
    def base64str_to_bytes(base64str: str):
        return base64.b64decode(base64str.encode("utf-8"))

    @staticmethod
    def get_task_info(data: str):
        return json.loads(data)

    @staticmethod
    def return_task_status(task_name: str, status: str, data: Union[str, dict] = ""):
        t_data = {
            "task": task_name,
            "status": status,
            "data": data
        }
        return json.dumps(t_data, ensure_ascii=False)

    @staticmethod
    def ping():
        data = {
            "task": "ping",
            "authentication": "",
            "data": ""
        }
        return json.dumps(data, ensure_ascii=False)

    @staticmethod
    def login(username: str, password: str):
        data = {
            "task": "login",
            "authentication": "",
            "data": {
                "username": username,
                "password": password
            }
        }
        return json.dumps(data, ensure_ascii=False)

    @staticmethod
    def login_status(data: str):
        t_json = json.loads(data)
        if t_json.get("status", '') == "ok":
            return t_json["data"].get('username', ''), t_json["data"].get('authentication', '')
        return "", ""

    @staticmethod
    def transmission_file(authentication: str, file_path: str):
        with open(file_path, 'rb') as f:
            file_data = websocket_task.bytes_to_base64str(f.read())
        data = {
            "task": "transmission_file",
            "authentication": authentication,
            "data": {
                "file_name": os.path.basename(file_path),
                "file_base64_data": file_data
            }
        }
        return json.dumps(data, ensure_ascii=False)

    @staticmethod
    def is_transmission_file_status(data: str):
        t_json = json.loads(data)
        if t_json.get("status", '') == "ok":
            return True
        return False

    @staticmethod
    def transmission_word(authentication: str, word: str):
        data = {
            "task": "transmission_word",
            "authentication": authentication,
            "data": word
        }
        return json.dumps(data, ensure_ascii=False)

    @staticmethod
    def is_transmission_word_status(data: str):
        t_json = json.loads(data)
        if t_json.get("status", '') == "ok":
            return True
        return False

    @staticmethod
    def upload_file(authentication: str, file_path: str):
        with open(file_path, 'rb') as f:
            file_data = websocket_task.bytes_to_base64str(f.read())
        data = {
            "task": "upload_file",
            "authentication": authentication,
            "data": {
                "file_name": os.path.basename(file_path),
                "file_base64_data": file_data
            }
        }
        return json.dumps(data, ensure_ascii=False)

    @staticmethod
    def is_upload_file_status(data: str):
        t_json = json.loads(data)
        if t_json.get("status", '') == "ok":
            return True
        return False

    @staticmethod
    def download_file(authentication: str, file_name: str):
        data = {
            "task": "download_file",
            "authentication": authentication,
            "data": {
                "file_name": file_name
            }
        }
        return json.dumps(data, ensure_ascii=False)

    @staticmethod
    def download_file_status(data: str):
        t_json = json.loads(data)
        if t_json.get("status", '') == "ok":
            file_bytes = websocket_task.base64str_to_bytes(t_json['data']["file_base64_data"])
            return t_json['data'].get('file_name'), file_bytes
        return False
