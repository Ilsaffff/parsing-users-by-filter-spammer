from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, query
from models import Base, Log


class DBHelper:
    def __init__(self, db_file):
        self.db_file = db_file
        self.engine = create_engine(f'sqlite:///{db_file}', echo=False, connect_args={"check_same_thread": False})
        Base.metadata.create_all(self.engine)
        Sesion = sessionmaker(bind=self.engine)
        self.session = Sesion()

    def delete_log(self, api_id):
        self.session.query(Log).filter_by(api_id=api_id).delete()
        self.session.commit()

    def get_log(self):
        log = self.session.query(Log).first()
        return log
