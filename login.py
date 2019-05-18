from pyramid.response import Response
from pyramid.request import Request
from pyramid.view import view_config
from sqlalchemy import text
from sqlalchemy.engine import ResultProxy
from sqlalchemy.sql.elements import TextClause

from database import db
import json


@view_config(request_method='POST')
def login_entry(request):
    username = request.json_body['username']
    password = request.json_body['password']

    try:
        stmt: TextClause = text('SELECT "username", "password" from usuario where logged = false and "username" = :username AND "password" = :password')
        stmt = stmt.bindparams(username=username, password=password)
        result: ResultProxy = db.execute(stmt)
        user = [dict(r) for r in result][0]
        print(user)
        if user is not None:
            token = request.create_jwt_token(user['username'])
            stmt: TextClause = text('UPDATE usuario set logged = true where username = :usern')
            stmt = stmt.bindparams(usern=username)
            db.execute(stmt)
            return Response(status=200, content_type='application/json', body=json.dumps({
                'token': token,
                'username': user['username']
            }), charset='utf-8')


    except Exception as e:
        return Response(status=400, content_type='application/json')

    return Response(status=404, content_type='application/json')
