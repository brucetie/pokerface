# -*- coding=utf8 -*-
"""
    检测图像中人脸关键点
"""
import os
import json
import mimetypes
import requests
from model import FemaleFace, Session

BASE_URL = 'http://apicn.faceplusplus.com/v2'

# 填写自己的API_KEY和API_SECRET
API_KEY = '*****'
API_SECRET = '******'
current_dir = os.path.abspath(os.path.curdir)


class Point(object):
    """二维平面点"""
    def __init__(self, x, y):
        self.x = x
        self.y = y


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
    info = response.json()
    FemaleFace.update(record_id, info=json.dumps(info))

    faces = info.get('face', [])
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

    landmark = landmarks[0].get('landmark')
    if not landmark:
        return 0

    FemaleFace.update(record_id, landmark=json.dumps(landmark))
    return 1

if __name__ == '__main__':
    session = Session()
    pretty_faces = session.query(FemaleFace).filter(FemaleFace.label == 0)
    for face in pretty_faces:
        file_path = '/Users/ruoyuliu/Downloads/aaa/{}'.format(face.filename)
        print detect_face(face.id, file_path)
