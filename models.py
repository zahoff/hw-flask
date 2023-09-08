import atexit
import uuid

from sqlalchemy import Column, Integer, String, DateTime, create_engine, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import UUIDType

from config import PG_DSN


engine = create_engine(PG_DSN)
Base = declarative_base(bind=engine)


class AdvtModel(Base):

    __tablename__ = 'advt'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('UserModel', backref='advt')


class UserModel(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)


class TokenModel(Base):

    __tablename__ = "tokens"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    creation_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("UserModel", lazy="joined")


Base.metadata.create_all()

Session = sessionmaker(bind=engine)

atexit.register(lambda: engine.dispose())