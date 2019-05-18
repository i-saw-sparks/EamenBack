import datetime
import decimal
import json

from pyramid.request import Request
from pyramid.response import Response
from sqlalchemy import text
from sqlalchemy.engine import ResultProxy
from sqlalchemy.sql.elements import TextClause

from database import db

def alchemyencoder(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

def _get_usuario(request):
    if request.authenticated_userid is not None:
        try:

            stmt: TextClause = text('SELECT * from usuario where "username"= :username')
            stmt = stmt.bindparams(username=request.authenticated_userid)

            get_usuario: ResultProxy = db.execute(stmt)

            return Response(status=200,
                            body=json.dumps([dict(r) for r in get_usuario][0], default=alchemyencoder),
                            content_type='application/json', charset='utf-8')
        except Exception as e:
            print(e)
            return Response(status=400, content_type='text/plain')
    else:
        return Response(status=400, content_type='text/plain', charset='utf-8')


def _create_usuario(request):
    try:
        user_data = request.json_body
        stmt: TextClause = text('INSERT into usuario ("username",'
                                '"password",'
                                '"logged") VALUES (:username, :password, :logged) ')

        stmt = stmt.bindparams(username = user_data['username'], password=user_data['password'],
                               logged = False)

        db.execute(stmt)

        return Response(status=200, charset='utf-8', content_type='text/plain')
    except Exception as e:
        print(e)
        return Response(status=400)


def usuario_entry(request: Request):
    if request.method == 'GET':
        return _get_usuario(request)
    if request.method == 'POST':
        return _create_usuario(request)
    elif request.method == 'OPTIONS':
        return Response(status=200, content_type='application/json', body=json.dumps({}), charset='utf-8')
    return Response(status=405, content_type='application/json')
