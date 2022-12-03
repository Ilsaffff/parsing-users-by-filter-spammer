import random

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_repr import RepresentableBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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

    def get_users_id(self):
        users = self.session.query(models.User).all()
        users_id = [user.id for user in users]
        return users_id

    def get_keywords(self):
        keywords = self.session.query(models.Keyword).all()
        return keywords

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

    def add_user(self, users_table, id, username, first_name, phone, description):
        self.session.add(
            users_table(username=username, id=id, first_name=first_name, phone=phone, description=description))
        self.session.commit()
