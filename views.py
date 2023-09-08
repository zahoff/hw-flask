from flask import jsonify, request
from flask.views import MethodView

from auth import hash_password, check_auth
from models import UserModel, Session, AdvtModel, TokenModel
from errors import ApiException
from sqlalchemy.exc import IntegrityError

from validate import validate, CreateAdvtSchema, CreateUserSchema


def check_token(session):
    token = (session.query(TokenModel).join(UserModel).filter(TokenModel.id == request.headers.get("token"),).first())
    if token is None:
        raise ApiException(401, "invalid token")
    return token


class UserView(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = session.query(UserModel).get(user_id)
            if user is None:
                raise ApiException(404, 'user not found')
            return jsonify({
                'id': user_id,
                'email': user.email
            })

    def post(self):
        user_data = validate(request.json, CreateUserSchema)
        user_data['password'] = hash_password(user_data['password'])
        with Session() as session:
            new_user = UserModel(**user_data)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError:
                raise ApiException(400, 'email is busy')
            return jsonify({'id': new_user.id, 'email': new_user.email})

    def delete(self, user_id: int):
        with Session() as session:
            user = session.query(UserModel).get(user_id)
            token = check_auth(session)
            if token.user_id != user.id:
                raise ApiException(403, "user has no access !")
            session.delete(user)
            session.commit()
            return jsonify({'status': 'deleted'})


class AdvtView(MethodView):

    def get(self, advt_id: int):
        with Session() as session:
            advt = session.query(AdvtModel).get(advt_id)
            if advt is None:
                raise ApiException(404, 'advertisement not found')
            return jsonify({
                'id': advt.id,
                'title': advt.title,
                'description': advt.description,
                'created_at': advt.created_at,
                'user_id': advt.user_id
            })

    def post(self):
        advt_data = validate(request.json, CreateAdvtSchema)
        print(advt_data)
        with Session() as session:
            if advt_data['user_id'] is None:
                raise ApiException(403, "please login")
            new_advt = AdvtModel(**advt_data)
            session.add(new_advt)
            session.commit()
            return jsonify({
                'id': new_advt.id,
                'title': new_advt.title,
                'description': new_advt.description,
                'created_at': new_advt.created_at,
                'user_id': new_advt.user_id
            })

    def delete(self, advt_id: int):
        with Session() as session:
            advt = session.query(AdvtModel).get(advt_id)
            token = check_auth(session)
            if advt.user_id != token.id:
                raise ApiException(403, "user has no access !")
            session.delete(advt)
            session.commit()
            return jsonify({'status': 'deleted'})