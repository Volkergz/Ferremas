# Importamos las librerías necesarias
import pytest
from unittest.mock import patch, MagicMock
from services.Autenticacion.main import app 

#

@pytest.fixture
def client():
    return app.test_client()

def test_authenticate_user_success(client):
    mock_user = {
        "apellidos": "Hidalgo Torres",
        "direccion": "somewhere 123",
        "email": "haleymgabrielhidalgo@gmail.com",
        "estado": 1,
        "id_rol": 2,
        "id_usuario": 1,
        "nombres": "Haleym",
        "password": "haleym"
    }

    # Mock de la conexión y el cursor
    with patch('services.Autenticacion.main.con.cursor') as mock_cursor:
        mock_cursor_instance = MagicMock()
        mock_cursor.return_value = mock_cursor_instance
        mock_cursor_instance.fetchone.return_value = mock_user

        response = client.post('/auth', json={
            'email': 'haleymgabrielhidalgo@gmail.com',
            'password': 'haleym'
        })

        assert response.status_code == 200
        assert response.get_json() == mock_user

def test_authenticate_user_fail(client):
    with patch('services.Autenticacion.main.con.cursor') as mock_cursor:
        mock_cursor_instance = MagicMock()
        mock_cursor.return_value = mock_cursor_instance
        mock_cursor_instance.fetchone.return_value = None

        response = client.post('/auth', json={
            'email': 'wrong@correo.com',
            'password': 'wrongpass'
        })

        assert response.status_code == 401
        assert response.get_json() == {'message': 'Usuario o contraseña incorrectos'}
