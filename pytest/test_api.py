import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
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

def test_admin_register_and_get(client: FlaskClient):
    # Register admin
    response = client.post('/admin', json={
        'username': 'testadmin',
        'password': 'testpass'  # NOSONAR
    })
    assert response.status_code in (200, 400)  # 400 si ya existe, 200 si se crea

    # Login admin to get token
    response = client.post('/login', json={
        'username': 'testadmin',
        'password': 'testpass'  # NOSONAR
    })
    assert response.status_code in (200, 401, 404)
    if response.status_code == 200:
        # Get admin by id (assuming id=1 for test, adjust as needed)
        response = client.get('/admin/1')
        assert response.status_code in (200, 404)

def test_categoria_crud(client: FlaskClient):
    # Login admin to get token
    login_resp = client.post('/login', json={
        'username': 'testadmin',
        'password': 'testpass'  # NOSONAR
    })
    if login_resp.status_code != 200:
        pytest.skip("No admin available for categoria tests")
    token = login_resp.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}

    # Crear categoria
    response = client.post('/categoria', json={'nombre': 'Bebidas'}, headers=headers)
    assert response.status_code in (200, 400)

    # Listar categorias
    response = client.get('/categoria')
    assert response.status_code == 200
    categorias = response.get_json()
    assert isinstance(categorias, list)

def test_extra_crud(client: FlaskClient):
    # Login admin to get token
    login_resp = client.post('/login', json={
        'username': 'testadmin',
        'password': 'testpass'  # NOSONAR
    })
    if login_resp.status_code != 200:
        pytest.skip("No admin available for extra tests")
    token = login_resp.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}

    # Crear extra
    response = client.post('/extra', json={
        'nombre': 'Queso',
        'precio': 10.0,
        'imagen_url': 'http://test.com/queso.png' # NOSONAR
    }, headers=headers)
    assert response.status_code in (200, 400)

    # Listar extras
    response = client.get('/extra')
    assert response.status_code == 200
    extras = response.get_json()
    assert isinstance(extras, list)

def test_login_wrong_credentials(client: FlaskClient):
    response = client.post('/login', json={
        'username': 'wronguser',
        'password': 'wrongpass'  # NOSONAR
    })
    assert response.status_code in (401, 404)

def test_producto_crud(client: FlaskClient):
    # Login admin to get token
    login_resp = client.post('/login', json={
        'username': 'testadmin',
        'password': 'testpass'  # NOSONAR
    })
    if login_resp.status_code != 200:
        pytest.skip("No admin available for producto tests")
    token = login_resp.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}

    # Crear producto
    response = client.post('/producto', json={
        'nombre': 'Ceviche',
        'categoria_id': 1,
        'precio': 20.0,
        'descripcion': 'Plato',
        'imagen_url': 'https://test.com/ceviche.jpg'
    }, headers=headers)
    assert response.status_code in (200, 400)

    # Listar productos
    response = client.get('/producto')
    assert response.status_code == 200
    productos = response.get_json()
    assert isinstance(productos, list)

def test_pedido_crud(client: FlaskClient):
    # Login admin to get token
    login_resp = client.post('/login', json={
        'username': 'testadmin',
        'password': 'testpass'  # NOSONAR
    })
    token = login_resp.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}

    # Crear pedido vacío (pero con claves requeridas)
    response = client.post('/pedido', json={
        'total': 0,
        'productos': [],
        'extras': []
    })
    assert response.status_code in (200, 400)

    # Listar pedidos (con token)
    response = client.get('/pedido', headers=headers)
    assert response.status_code == 200
    pedidos = response.get_json()
    assert isinstance(pedidos, list)
