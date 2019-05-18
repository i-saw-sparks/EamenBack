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

def _get_vuelo(request):
    vuelo_data = request.params
    if 'origen' in vuelo_data:
        stmt: TextClause = text('SELECT * FROM vuelos where capacidad > 0 and lower(origen) like lower(:origen) and lower(destino) like lower(:destino)')
        stmt = stmt.bindparams(origen = vuelo_data['origen'] + "%", destino = vuelo_data['destino'] + "%")

        get_vuelo: ResultProxy = db.execute(stmt)
        data = [dict(r) for r in get_vuelo]

        if data.__len__() == 0:
            stmt: TextClause = text('SELECT * FROM buscar(:origen, :destino)')
            stmt = stmt.bindparams(origen=vuelo_data['origen'], destino=vuelo_data['destino'])
            get_vuelo: ResultProxy = db.execute(stmt)
            data = [dict(r) for r in get_vuelo]

        return Response(status=200,
            body=json.dumps(data, default=alchemyencoder),
            content_type='application/json', charset='utf-8')

    if 'clave' in vuelo_data:
        stmt: TextClause = text('SELECT * FROM vuelos where clave = :clav')
        stmt = stmt.bindparams(clav = vuelo_data['clave'])
        get_vuelo: ResultProxy = db.execute(stmt)
        return Response(status=200,
                        body=json.dumps([dict(r) for r in get_vuelo], default=alchemyencoder),
                        content_type='application/json', charset='utf-8')
    else:
            stmt: TextClause = text(
                'SELECT * FROM vuelos where capacidad > 0 ')
            get_vuelo: ResultProxy = db.execute(stmt)

            return Response(status=200,
                            body=json.dumps([dict(r) for r in get_vuelo], default=alchemyencoder),
                            content_type='application/json', charset='utf-8')

def vuelo_entry(request: Request):
    if request.method == 'GET':
        return _get_vuelo(request)
    elif request.method == 'OPTIONS':
        return Response(status=200, content_type='application/json', body=json.dumps({}), charset='utf-8')
    return Response(status=405, content_type='application/json')