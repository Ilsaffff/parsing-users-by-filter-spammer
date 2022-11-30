from sqlalchemy import Column, Integer, String, Boolean
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

