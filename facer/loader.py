# -*- coding=utf8 -*-
"""
    从sqlite读取数据并
"""
from __future__ import division

import json
import math
import numpy
from model import FemaleFace

positions_except_eye_center = [
    'mouth_upper_lip_left_contour2',
    'contour_chin',
    'mouth_lower_lip_right_contour3',
    'mouth_upper_lip_left_contour1',
    'right_eyebrow_lower_middle',
    'left_eyebrow_lower_middle',
    'left_eye_left_corner',
    'left_eyebrow_lower_left_quarter',
    'right_eyebrow_lower_left_quarter',
    'right_eyebrow_lower_right_quarter',
    'nose_contour_left1',
    'left_eyebrow_upper_left_quarter',
    'left_eye_bottom',
    'mouth_lower_lip_bottom',
    'contour_right7',
    'left_eyebrow_left_corner',
    'contour_right6',
    'right_eye_lower_right_quarter',
    'right_eye_bottom',
    'contour_left7',
    'contour_left6',
    'contour_left5',
    'contour_left4',
    'contour_left3',
    'contour_left2',
    'contour_left1',
    'left_eye_lower_left_quarter',
    'contour_right1',
    'contour_right3',
    'contour_right2',
    'contour_right5',
    'contour_right4',
    'contour_left9',
    'contour_left8',
    'nose_right',
    'right_eye_upper_right_quarter',
    'nose_contour_right3',
    'nose_contour_lower_middle',
    'right_eye_top',
    'right_eye_right_corner',
    'mouth_upper_lip_right_contour1',
    'mouth_upper_lip_right_contour2',
    'mouth_upper_lip_right_contour3',
    'contour_right9',
    'mouth_right_corner',
    'mouth_lower_lip_right_contour1',
    'contour_right8',
    'mouth_upper_lip_left_contour3',
    'left_eyebrow_right_corner',
    'left_eye_upper_right_quarter',
    'mouth_upper_lip_top',
    'nose_left',
    'left_eye_upper_left_quarter',
    'left_eye_lower_right_quarter',
    'right_eyebrow_left_corner',
    'right_eye_left_corner',
    'mouth_lower_lip_top',
    'right_eyebrow_right_corner',
    'mouth_lower_lip_left_contour1',
    'left_eye_pupil',
    'mouth_left_corner',
    'right_eyebrow_upper_left_quarter',
    'right_eye_lower_left_quarter',
    'nose_tip',
    'right_eye_upper_left_quarter',
    'left_eyebrow_upper_middle',
    'mouth_lower_lip_right_contour2',
    'mouth_lower_lip_left_contour3',
    'nose_contour_left2',
    'nose_contour_left3',
    'nose_contour_right1',
    'nose_contour_right2',
    'mouth_lower_lip_left_contour2',
    'right_eyebrow_upper_right_quarter',
    'right_eyebrow_upper_middle',
    'left_eyebrow_lower_right_quarter',
    'left_eye_top',
    'left_eye_right_corner',
    'left_eyebrow_upper_right_quarter',
    'right_eye_pupil',
    'mouth_upper_lip_bottom'
]


class Point(object):
    """二维平面点"""
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Vector(Point):
    """二维平面向量"""
    def __init__(self, x, y):
        Point.__init__(self, x, y)

    def normalize(self):
        """正则化处理"""
        length = math.sqrt(self.x * self.x + self.y * self.y)
        self.x /= length
        self.y /= length

    @classmethod
    def resolve_normal_vector(cls, vec):
        """
        求法向量
        :param vec: (Vector) 单位向量
        :return: (Vector) vec的单位法向量
        """
        return cls(-vec.y, vec.x)


def transform(point, origin_point,
              x_vector, y_vector):
    """
    坐标系变换
    :param point: 原坐标系坐标
    :param origin_point: 新坐标系远点
    :param x_vector: 单位水平向量
    :param y_vector: 单位竖直向量
    :return: (list) [x, y]
    """
    vec = Point(point.x- origin_point.x, point.y - origin_point.y)
    x = vec.x * x_vector.x + vec.y * x_vector.y / math.sqrt(
        x_vector.x * x_vector.x + x_vector.y * x_vector.y)
    y = vec.x * y_vector.x + vec.y * y_vector.y / math.sqrt(
        y_vector.x * y_vector.x + y_vector.y * y_vector.y)
    result = Vector(x, y)
    result.normalize()
    return [result.x, result.y]


def normalize_face(landmark):
    """
    正则化face数据
    :param landmark: (string) face++检测的关键点
    :return: (list) 归一化数据
    """
    left_eye_center = Point(landmark['left_eye_center']['x'],
                            landmark['left_eye_center']['y'])
    right_eye_center = Point(landmark['right_eye_center']['x'],
                             landmark['right_eye_center']['y'])

    origin_point = Point((left_eye_center.x + right_eye_center.x) / 2,
                         (left_eye_center.y + right_eye_center.y) / 2,)

    unit_horizontal_vector = Vector(right_eye_center.x - origin_point.x,
                                    right_eye_center.y - origin_point.y)
    unit_horizontal_vector.normalize()
    unit_vertical_vector = Vector.resolve_normal_vector(unit_horizontal_vector)

    result = []
    for point_name in positions_except_eye_center:
        point = Point(landmark[point_name]['x'], landmark[point_name]['x'])
        result.extend(transform(point, origin_point,
                                unit_horizontal_vector, unit_vertical_vector))
    return result


def load_data():
    """读取数据集"""
    data_x, data_y = [], []
    for face in FemaleFace.iteration():
        landmark = json.loads(face.landmark)
        data_x.append(normalize_face(landmark))
        data_y.append(1 if face.label > 0 else 0)

    train_x, train_y = data_x[:3500], data_y[:3500]
    test_x, test_y = data_x[3500:], data_y[3500:]

    return [(numpy.array(train_x), numpy.array(train_y)),
            (numpy.array(test_x), numpy.array(test_y))]

if __name__ == '__main__':
    data_x, data_y = load_data()
    print data_x
    print data_y
