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

def _get_compra(request):
    try:
        stmt: TextClause = text('SELECT vuelos.*, compra.cantidad as cantidad FROM vuelos, compra WHERE vuelos.clave = compra.vuelo and compra.usuario = :usern')
        stmt = stmt.bindparams(usern = request.authenticated_userid)

        get_compra: ResultProxy = db.execute(stmt)
        return Response(status=200,
                            body=json.dumps([dict(r) for r in get_compra], default=alchemyencoder),
                            content_type='application/json', charset='utf-8')
    except Exception as e:
        return Response(status=400)


def _create_compra(request):
    vuelo_data = request.json_body

    try:
        stmt: TextClause = text('INSERT INTO compra(usuario,vuelo,cantidad) VALUES (:usern, :vuelo, :cantidad)')
        stmt = stmt.bindparams(usern=request.authenticated_userid, vuelo = vuelo_data['clave'], cantidad = vuelo_data['boletos'])
        db.execute(stmt)
        return Response(status=200)
    except Exception as e:

        return Response(status=400)


def compra_entry(request: Request):
    if request.method == 'GET':
        return _get_compra(request)
    if request.method == 'POST':
        return _create_compra(request)
    elif request.method == 'OPTIONS':
        return Response(status=200, content_type='application/json', body=json.dumps({}), charset='utf-8')
    return Response(status=405, content_type='application/json')