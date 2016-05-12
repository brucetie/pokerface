# -*- coding=utf8 -*-
"""
    打分记录表
"""
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker

current_dir = os.path.dirname(os.path.abspath(__file__))
BaseModel = declarative_base()
db_name = os.path.join(current_dir, 'face.sqlite.bak')
engine = create_engine('sqlite:///{}'.format(db_name))
Session = sessionmaker(bind=engine)


class FemaleFace(BaseModel):

    __tablename__ = 'face'

    id = Column(Integer, primary_key=True)
    filename = Column(String(20), nullable=False)
    label = Column(Integer, nullable=False)
    info = Column(String(8000), nullable=False)

    @classmethod
    def get(cls, filename):
        """
        查找图片记录
        :param filename: (string) 图片名称
        :return: FemaleFace
        """
        session = Session()
        query = session.query(cls).filter(cls.filename == filename)
        result = query.first()
        session.commit()
        return result

    @classmethod
    def update(cls, record_id, label=None, landmark=None):
        session = Session()
        target = session.query(cls).filter(cls.id == record_id)
        result = 0
        if label is not None:
            result = target.update({'label': label})
        if landmark is not None:
            result = target.update({'landmark': landmark})
        session.commit()
        return result

    @classmethod
    def add(cls, filename, label, landmark=u''):
        """添加转移记录

        :param filename: (string) 文件名
        :param label: (int) 标签
        :param landmark: (string) 面部关键点坐标
        """
        session = Session()
        record = cls(filename=filename, label=label, landmark=landmark)
        session.add(record)
        session.commit()
        return record

    @classmethod
    def get_all(cls):
        """遍历整个表"""
        session = Session()
        result = session.query(cls).order_by(cls.id.asc()).all()
        session.commit()
        return result


def init_table():
    """
    创建表
    """
    if os.path.exists(db_name):
        os.remove(db_name)

    with open(db_name, 'w') as f:
        pass

    BaseModel.metadata.create_all(bind=engine, tables=[FemaleFace.__table__])

if __name__ == '__main__':
    init_table()

