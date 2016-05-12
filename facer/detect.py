# -*- coding=utf8 -*-
"""
    检测图像中人脸关键点
"""
import os
import json
import mimetypes
import requests
from model import FemaleFace
from PIL import Image

BASE_URL = 'http://apicn.faceplusplus.com/v2'
API_KEY = '8f44e5d3371ece33d0066ef3be84e0a7'
API_SECRET = 'e1wUSyrIwrOpnBKWMLFtrzZpoX4HFzgL'
current_dir = os.path.abspath(os.path.curdir)


class Point(object):
    """二维平面点"""
    def __init__(self, x, y):
        self.x = x
        self.y = y


def cut_face(file_name, detect_result, save_path):
    """
    根据检测结果剪裁人脸
    :param file_name: 图片路径
    :param detect_result: face++检测结果
    :param save_path: 存储路径
    """
    image = Image.open(file_name)
    width, height = image.size

    center = Point(int(width * detect_result['face'][0]['position']['center']['x'] / 100),
                   int(height * detect_result['face'][0]['position']['center']['y'] / 100))
    tmp = image.crop((center.x - 200, center.y - 200,
                       center.x + 200, center.y + 200))
    tmp = tmp.rotate(detect_result['face'][0]['attribute']['pose']['roll_angle']['value'])

    face_height = (detect_result['face'][0]['position']['height'] + 10) * height / 200
    face_width = detect_result['face'][0]['position']['width'] * width / 200
    face_size = int(max(face_height, face_width))
    tmp = tmp.crop((200 - face_size, 200 - face_size, 200 + face_size, 200 + face_size))
    tmp = tmp.resize((64, 64)).convert('L')
    tmp.save(save_path)


def detect_face(record_id, file_path):
    """
    调用face++ API检测人脸并写入数据库
    :param record_id: (int) 数据库记录
    :param file_path: (string) 图像路径
    :return: (int) 是否检测到人脸（默认选第一个）
    """
    upload_url = '{}/detection/detect?api_key={}&api_secret={}&attribute=pose'.format(
        BASE_URL, API_KEY, API_SECRET
    )
    files = {'img': (os.path.basename(file_path),
                     open(file_path, 'rb'),
                     mimetypes.guess_type(file_path)[0]), }
    response = requests.post(upload_url, files=files)
    result = response.json()
    if not result.get('face'):
        return None

    FemaleFace.update(record_id, landmark=json.dumps(result))
    save_path = os.path.join(current_dir, 'train/{}.jpg'.format(record_id))
    cut_face(files, result, save_path)
    return result
