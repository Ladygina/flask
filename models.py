import os
from sqlalchemy import create_engine, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
import datetime
from atexit import register
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, declarative_base, Session
from sqlalchemy import create_engine


POSTGRES_USER = os.getenv('POSTGRES_USER', 'app')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '1234')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'flask_dz')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')

PG_DSN = f'postgresql://'\
         f'{POSTGRES_USER}:{POSTGRES_PASSWORD}' \
         f'@{POSTGRES_HOST}:{POSTGRES_PORT}' \
         f'/{POSTGRES_DB}'

engine = create_engine(PG_DSN)
db = SQLAlchemy()

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,autoincrement=True)
    username = Column(String, nullable=False)
    advertisements = relationship('Advertisement', back_populates='user')


class Advertisement(Base):
    __tablename__ = 'advertisement'
    id = Column(Integer, primary_key=True,autoincrement=True)
    header = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    registration_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', back_populates='advertisements')

    @property
    def dict(self):
        return {
            'id': self.id,
            'header': self.header,
            'description': self.description,
            'registration_time': self.registration_time.isoformat() if self.registration_time else None,
            'owner': self.user.username if self.user else None
        }

user = Users(id=2, username='Автор 1')
#print('user', user.username, user.id)
adv1 = Advertisement(id=2, header='advert1', description='selling house', user=user)



