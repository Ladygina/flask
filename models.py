import os
from sqlalchemy import create_engine, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
import datetime
from atexit import register

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
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    @property
    def id_dict(self):
        return {'id':self.id}

class Advertisement(Base):
    __tablename__ = 'advertisement'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # столбец id c типом данных int
    header: Mapped[str]=  mapped_column(String, unique=True, nullable=False) # заголовок объявления
    description: Mapped[str] = mapped_column(String, nullable=False)
    reqistation_time : Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now()) # выаолнить запись даты на стороне постгреса

    @property
    def dict(self):
        return {
            'id':self.id,
            'header':self.header,
            'description': self.description,
            'registration_time':self.reqistation_time.isoformat(),
        }
Base.metadata.create_all(bind=engine)
register(engine.dispose)
