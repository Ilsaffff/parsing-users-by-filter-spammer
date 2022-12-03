import random

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_repr import RepresentableBase
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, query
import models


class DBHelper:
    def __init__(self, db_file):
        self.db_file = db_file
        self.engine = create_engine(f'sqlite:///{db_file}', echo=False, connect_args={"check_same_thread": False})
        models.Base.metadata.create_all(self.engine)
        Sesion = sessionmaker(bind=self.engine)
        self.session = Sesion()

    def delete_log(self, api_id):
        self.session.query(models.Log).filter_by(api_id=api_id).delete()
        self.session.commit()

    def get_log(self):
        log = self.session.query(models.Log).first()
        return log

    def get_messages(self):
        messages = self.session.query(models.Message).all()
        return messages

    def get_users(self):
        users = self.session.query(models.User).all()
        return users

    def add_table_users(self, table_name):
        Base = declarative_base(cls=RepresentableBase)

        class User(Base):
            __tablename__ = f'{table_name}'
            id = Column(Integer, primary_key=True)
            username = Column(String)
            first_name = Column(String)
            phone = Column(Integer)
            description = Column(String)

        Base.metadata.create_all(self.engine)
        return User

    def add_user(self, users_table, username, first_name, phone, description):
        self.session.add(users_table(username=username, first_name=first_name, phone=phone, description=description))
        self.session.commit()


db = DBHelper('test.db')
users_table = db.add_table_users('parsing_users')
db.add_user(users_table, 'ilsaf', 'ilsafchik', '+7986', 'Hi Bro')
