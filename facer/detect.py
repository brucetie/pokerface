# -*- coding=utf8 -*-
"""
    检测图像中人脸关键点
"""
import os
import json
import mimetypes
import requests
from model import FemaleFace

# 这里填写你的应用的API Key与API Secret
API_KEY = '8f44e5d3371ece33d0066ef3be84e0a7'
API_SECRET = 'e1wUSyrIwrOpnBKWMLFtrzZpoX4HFzgL'

# API网址
BASE_URL = 'http://apicn.faceplusplus.com/v2'


def detect_face(record_id, file_path):
    """
    调用face++ API检测人脸并写入数据库
    :param record_id: (int) 数据库记录
    :param file_path: (string) 图像路径
    :return: (int) 是否检测到人脸（默认选第一个）
    """
    upload_url = '{}/detection/detect?api_key={}&api_secret={}&attribute=none'.format(
        BASE_URL, API_KEY, API_SECRET
    )
    files = {'img': (os.path.basename(file_path),
                     open(file_path, 'rb'),
                     mimetypes.guess_type(file_path)[0]), }
    response = requests.post(upload_url, files=files)
    faces = response.json().get('face', [])
    if not faces:
        return 0

    face_id = faces[0].get('face_id', '')
    landmark_url = '{}/detection/landmark?api_key={}&api_secret={}&face_id={}&type=83p'.format(
        BASE_URL, API_KEY, API_SECRET, face_id
    )
    response = requests.get(landmark_url)
    landmarks = response.json().get('result', [])
    if not landmarks:
        return 0

    fist_landmark = landmarks[0].get('landmark')
    if not fist_landmark:
        return 0

    FemaleFace.update(record_id, landmark=json.dumps(fist_landmark))
    return fist_landmark
