import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch
from flask import Flask
from flask.testing import FlaskClient
from src import init_app
from config import confi

@pytest.fixture
def app():
    configuration = confi['development']
    app = init_app(configuration)
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()


# 1. Simular excepción en POST /pedido
def test_post_pedido_exception(client):
    with patch('src.routes.Pedido_Routes.PedidoService.post_pedido', side_effect=Exception("DB error")):
        response = client.post('/pedido', json={
            'total': 10,
            'productos': [],
            'extras': []
        })
        assert response.status_code == 500
        assert 'Error interno del servidor' in response.get_json()['mensaje']

# 2. Simular fallo en registro de pedido (exito = False)
def test_post_pedido_fail(client):
    with patch('src.routes.Pedido_Routes.PedidoService.post_pedido', return_value=(False, 'No se pudo registrar pedido', None)):
        response = client.post('/pedido', json={
            'total': 10,
            'productos': [],
            'extras': []
        })
        assert response.status_code == 200
        assert response.get_json()['mensaje'] == 'No se pudo registrar pedido'

# 3. Simular excepción en GET /pedido
def test_get_pedido_exception(client):
    with patch('src.routes.Pedido_Routes.PedidoService.get_pedido', side_effect=Exception("DB error")):
        # Necesita autenticación
        login_resp = client.post('/login', json={
            'username': 'testadmin',
            'password': 'testpass' # NOSONAR
        })
        if login_resp.status_code != 200:
            pytest.skip("No admin available for pedido tests")
        token = login_resp.get_json()['token']
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get('/pedido', headers=headers)
        assert response.status_code == 500
        assert 'Error interno del servidor' in response.get_json()['mensaje']

# 4. Simular respuesta vacía en GET /pedido/datos_dias
def test_get_datos_dias_empty(client):
    with patch('src.routes.Pedido_Routes.PedidoService.get_total_dia', return_value=None):
        response = client.get('/pedido/datos_dias')
        assert response.status_code == 200
        assert response.get_json() == []

# 5. Simular excepción en GET /pedido/datos_dias
def test_get_datos_dias_exception(client):
    with patch('src.routes.Pedido_Routes.PedidoService.get_total_dia', side_effect=Exception("DB error")):
        response = client.get('/pedido/datos_dias')
        assert response.status_code == 500
        assert 'Error interno del servidor' in response.get_json()['mensaje']

# 6. Simular respuesta vacía y excepción para semanas, meses y años
@pytest.mark.parametrize("endpoint,service", [
    ('/pedido/datos_semanas', 'get_total_semana'),
    ('/pedido/datos_meses', 'get_total_mes'),
    ('/pedido/datos_anos', 'get_total_ano'),
])
def test_get_datos_empty_and_exception(client, endpoint, service):
    # Vacío
    with patch(f'src.routes.Pedido_Routes.PedidoService.{service}', return_value=None):
        response = client.get(endpoint)
        assert response.status_code == 200
        assert response.get_json() == []
    # Excepción
    with patch(f'src.routes.Pedido_Routes.PedidoService.{service}', side_effect=Exception("DB error")):
        response = client.get(endpoint)
        assert response.status_code == 500
        assert 'Error interno del servidor' in response.get_json()['mensaje']
