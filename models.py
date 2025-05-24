import os
from sqlalchemy import create_engine, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
import datetime
from atexit import register
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Table
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
Base = declarative_base()

# # Таблица ассоциации
# association_table = Table(
#     'association',
#     Base.metadata,
#     Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
#     Column('advertisement_id', Integer, ForeignKey('advertisement.id'), primary_key=True)
# )

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=False)
    username = Column(String, nullable=False)
    advertisements = relationship(
        'Advertisement',
        backref='users', lazy=True)


class Advertisement(Base):
    __tablename__ = 'advertisement'
    id = Column(Integer, primary_key=True, autoincrement=False)
    header = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    registration_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer,ForeignKey('users.id'), nullable=False)

    @property
    def dict(self):
        return {
            'id': self.id,
            'header': self.header,
            'description': self.description,
            'registration_time': self.registration_time.isoformat() if self.registration_time else None,
            'owner': self.user_id
        }

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)




