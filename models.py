from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_repr import RepresentableBase

Base = declarative_base(cls=RepresentableBase)


class Log(Base):
    __tablename__ = 'logs'
    api_id = Column(Integer, primary_key=True)
    api_hash = Column(String)
    phone = Column(String)

    def __repr__(self):
        return f'{self.api_id}'


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    text = Column(String)

    def __repr__(self):
        return f'{self.text}'


class User(Base):
    __tablename__ = 'my_users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)

    def __repr__(self):
        return f'{self.id}'


class Keyword(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True)
    text = Column(String)

    def __repr__(self):
        return f'{self.text}'
