from pyramid.response import Response
from sqlalchemy import text
from sqlalchemy.sql.elements import TextClause

from database import db

def delog_entry(request):
    delog_data = request.params
    user = delog_data['usuario']
    if user is not None:
        try:
            stmt: TextClause = text('UPDATE usuario set logged = false where username = :usern')
            stmt = stmt.bindparams(usern=user)

            db.execute(stmt)

            return Response(status=200)
        except Exception as e:
            print(e)
            return Response(status=400, content_type='text/plain')
    else:
        return Response(status=400, content_type='text/plain', charset='utf-8')
