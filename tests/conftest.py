import time
from datetime import datetime

from pytest import fixture

from auth import hash_password
from models import Base, UserModel, Session, AdvtModel


@fixture(scope='session', autouse=True)
def prepair_db():
    Base.metadata.drop_all()
    Base.metadata.create_all()


@fixture()
def create_user():
    with Session() as session:
        new_user = UserModel(email=f'user{time.time()}@mail.com', password=hash_password('1234'))
        session.add(new_user)
        session.commit()
        return {
            'id': new_user.id,
            'email': new_user.email,
            'password': '1234'
        }


@fixture()
def create_advt():
    with Session() as session:
        new_user = UserModel(email=f'user{time.time()}@mail.com', password=hash_password('1234'))
        session.add(new_user)
        session.commit()
        new_advt = AdvtModel(title='test', description='test_descr', user_id=new_user.id)
        session.add(new_advt)
        session.commit()
        return {
            'id': new_advt.id,
            'title': new_advt.title,
            'description': new_advt.description,
            'user_id': new_advt.user_id,
            'user_email': new_user.email,
            'user_password': '1234'
        }