from wsgiref.simple_server import make_server

from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.events import NewRequest

from usuario import usuario_entry
from login import login_entry
from vuelo import vuelo_entry
from delog import delog_entry
from compra import compra_entry

def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
        'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Max-Age': '1728000',
        })
    event.request.add_response_callback(cors_headers)

if __name__ == '__main__':

    with Configurator() as config:
        config.add_subscriber(add_cors_headers_response_callback, NewRequest)
        config.set_authorization_policy(ACLAuthorizationPolicy())
        config.include('pyramid_jwt')

        config.set_jwt_authentication_policy('secret')

        config.add_route('usuarios', '/usuarios')  # localhost:6543/
        config.add_view(usuario_entry, route_name='usuarios')
        config.add_route('login', '/login')
        config.add_view(login_entry, route_name='login')
        config.add_route('vuelos', '/vuelos')
        config.add_view(vuelo_entry, route_name='vuelos')
        config.add_route('delog', 'delog')
        config.add_view(delog_entry, route_name='delog')
        config.add_route('compras', 'compras')
        config.add_view(compra_entry, route_name='compras')

        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()

