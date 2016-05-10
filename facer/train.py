# -*- coding=utf8 -*-
"""
    训练模型
"""
import numpy
from keras.optimizers import SGD
from keras.models import Sequential
from keras.utils.np_utils import to_categorical
from keras.layers.core import Dense, Activation, Dropout
from loader import load_data, normalize_face

#numpy.random.seed(300)  # 让每次运行结构都一样


class Model(object):
    """神经网络模型"""
    def __init__(self, n_inputs, n_classes, embedding_dims=50):
        """
        构造函数
        :param n_inputs: (int) 输入维度
        :param n_classes: (int) 输出类型个数
        :param embedding_dims: (int) 隐藏层维度
        """
        self.n_inputs = n_inputs
        self.n_classes = n_classes
        self.embedding_dims = embedding_dims
        self.model = Sequential()

    def build_model(self):
        """
        参考practical4, 模型定义sigmoid -> softmax
        """
        self.model.add(Dense(self.embedding_dims, input_dim=self.n_inputs))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.2))

        self.model.add(Dense(self.n_classes))
        self.model.add(Activation('softmax'))

        opt = SGD(lr=0.001, decay=1e-7, momentum=0.9, nesterov=True)
        self.model.compile(loss='categorical_crossentropy',
                           optimizer=opt, metrics=["accuracy"])

    def train(self, input_x, input_y):
        """
        训练数据及
        :param input_x: numpy.ndarray 特征数据
        :param input_y: numpy.ndarray label数据
        """
        self.model.fit(input_x, input_y,
                       batch_size=128, nb_epoch=50, verbose=1)

    def evaluate(self, test_x, test_y):
        """
        训练数据及
        :param test_x: numpy.ndarray 测设特征数据
        :param test_y: numpy.ndarray label数据
        """
        return self.model.evaluate(test_x, test_y, verbose=0)


if __name__ == '__main__':
    face_data = load_data()
    train_x, train_y = face_data[0]
    test_x, test_y = face_data[1]
    train_y = to_categorical(train_y).astype('int')
    test_y = to_categorical(test_y).astype('int')

    model = Model(train_x.shape[1], 2, 10)
    model.build_model()
    model.train(train_x, train_y)

    result = model.model.predict_classes(test_x)
    print result
    #
    # score = model.evaluate(test_x, test_y)
    # print('Test accuracy:', score[1])
    #
    # from detect import detect_face
    # landmark = detect_face(0, 'fengjie.jpeg')
    # real_x = numpy.array([normalize_face(landmark)])
    # result = model.model.predict_classes(real_x)
    # print result
    #
    # landmark = detect_face(0, 'a.jpg')
    # real_x = numpy.array([normalize_face(landmark)])
    # result = model.model.predict_classes(real_x)
    # print result
