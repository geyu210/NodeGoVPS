from datetime import datetime
import time
import logging
from time import sleep
import requests

# 常量
bearToken = open('accessToken.txt', 'r', encoding='utf-8').read()
baseURL= "https://nodego.ai/api"
UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
last_ping_timestamp = 0
def getUser():
    try:
        response = requests.get(
            f"{baseURL}/user/me",
            headers={
                'Authorization': f'Bearer {bearToken}'
            }
        ).json()

        metadata = response.get('metadata')
        return {
            'username': metadata.get('username'),
            'email': metadata.get('email'),
            'totalPoint': metadata.get('rewardPoint'),
            'nodes': [
                {
                    'id': node.get('id'),
                    'totalPoint': node.get('totalPoint'),
                    'todayPoint': node.get('todayPoint'),
                    'isActive': node.get('isActive')
                }
                for node in metadata.get('nodes', [])
            ]
        }
        #return metadata
    except Exception as error:
        logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [ERROR] 获取用户信息失败: {error}")
        raise error



def print_user_info(user_info):
    basic_info = {
        "用户名": user_info['username'],
        "邮箱": user_info['email'],
        "总积分": user_info['totalPoint']
    }
    for key, value in basic_info.items():
        print(f"{key}: {value}")

    print("节点信息:")
    node_fields = [
        ("节点 ID", 'id'),
        ("总积分", 'totalPoint'),
        ("今日积分", 'todayPoint'),
        ("是否活跃", lambda node: '是' if node['isActive'] else '否')
    ]
    for node in user_info['nodes']:
        for field_name, field_key in node_fields:
            if callable(field_key):
                value = field_key(node)
            else:
                value = node[field_key]
            print(f"  {field_name}: {value}")


# 增加一个更大的请求间隔
MIN_PING_INTERVAL = 60000 

def ping(token):
    global last_ping_timestamp
    try:
        current_time = time.time() * 1000
        if current_time - last_ping_timestamp < MIN_PING_INTERVAL:
            sleep((MIN_PING_INTERVAL - (current_time - last_ping_timestamp)) / 1000)
        response = requests.post(
            f"{baseURL}/user/nodes/ping",
            headers={
                'Authorization': f'Bearer {token}',
                'User-Agent': UserAgent,
                'Content-Type': 'application/json'
            },
            json={'type': 'extension'}
        )

        last_ping_timestamp = time.time() * 1000
        return {
            'statusCode': response.status_code,
            'message': response.text,
            'metadataId': response.json().get('metadata', {}).get('id')
        }
    except Exception as error:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [ERROR] Ping失败: {error}")
        raise

ping_count = 0
while True:
    try:
        if ping_count % 60 == 0:
            userInfo = getUser()
            print_user_info(userInfo)
        p = ping(bearToken)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO] Ping结果: {p}")
        ping_count += 1
    except:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [ERROR] 获取用户信息失败")
        break