import requests
import json


# url = 'http://192.168.10.116/cgibin/ApiProxy.cgi'
# username = 'admin'
# password = 'admin'

url = 'http://120.97.23.31/cgibin/ApiProxy.cgi'
username = 'admin'
password = 'Ntubaml6662'

modulename = 'com.avc.enrollservice'


def request(data):  # 封裝後的請求方法
    payload = {
        'username': username,
        'password': password,
        'modulename': modulename,
        'apibody': json.dumps(data)
    }
    response = requests.post(url, data=payload)
    print('status_code:{}'.format(response.status_code))
    print('response:{}'.format(response.text))
    return json.loads(response.text)


def get_user_list():  # 取得已經註冊的使用者列表
    data = {
        'command': 'namelist'
    }
    return request(data)


def get_face_images_by_uuid(uuid):  # 取得圖片用uuid
    data = {
        'command': 'face_images',
        'UUID': uuid
    }
    return request(data)


def add_user(uuid, name, image_base64s):  # 註冊
    data = {
        'command': 'register_user',
        'UUID': uuid,
        'info': {
            'name': name,
            'organization': '北商銀行',
            'adv_group': '1'
        },
        'pictures': image_base64s
    }
    request(data)


# def update_user(uuid, name):  # 更新使用者
#     data = {
#         'command': 'update_user',
#         'UUID': uuid,
#         'info': {
#             'name': name
#         }
#     }
#     request(data)


def remove_user(uuid):  # 刪除使用者
    data = {
        'command': 'remove_user',
        'UUID': uuid
    }
    request(data)


def face_recognition_event(timeslot_start, timeslot_end):  # 取得時間內臉部事件
    data = {
        'command': 'face_recognition_event',
        'timeslot_start': timeslot_start,
        'timeslot_end': timeslot_end
    }
    return request(data)
