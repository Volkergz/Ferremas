import pytest
from unittest.mock import patch, MagicMock
from services.Inventario.main import app
@pytest.fixture
def client():
    return app.test_client()

# ---------- POST /productos ----------
@patch("services.Inventario.main.con")
def test_get_productos_exitoso(mock_con, client):
    """Retorna productos activos correctamente"""

    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        {"id_producto": 1, "nombre": "Martillo", "estado": 1},
        {"id_producto": 2, "nombre": "Destornillador", "estado": 1}
    ]
    mock_con.cursor.return_value = mock_cursor

    response = client.post("/productos")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2

@patch("services.Inventario.main.con")
def test_get_productos_no_existen(mock_con, client):
    """No se encuentran productos activos"""

    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = None
    mock_con.cursor.return_value = mock_cursor

    response = client.post("/productos")
    assert response.status_code == 404
    assert response.get_json()["message"] == "No se encontraron productos"

# ---------- GET /productos/<id> ----------
@patch("services.Inventario.main.con")
def test_get_producto_por_id_existe(mock_con, client):
    """Producto por ID existe"""

    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {
        "id_producto": 1,
        "nombre": "Taladro",
        "estado": 1
    }
    mock_con.cursor.return_value = mock_cursor

    response = client.get("/productos/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["nombre"] == "Taladro"

@patch("services.Inventario.main.con")
def test_get_producto_por_id_no_existe(mock_con, client):
    """Producto por ID no existe"""

    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_con.cursor.return_value = mock_cursor

    response = client.get("/productos/999")
    assert response.status_code == 404
    assert response.get_json()["message"] == "No se encontraron productos"
