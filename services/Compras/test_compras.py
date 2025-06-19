import pytest
from unittest.mock import patch, MagicMock
from services.Compras.main import app

@pytest.fixture
def client():
    return app.test_client()

# ---------- addCar ----------
@patch("services.Compras.main.con")
def test_add_car_producto_existe(mock_con, client):
    mock_cursor = MagicMock()
    
    # Simula orden ya existente
    mock_cursor.fetchone.side_effect = [
        {'id_orden': 1},  # ya hay orden
        {'id_producto': 10, 'precio': 1000}  # producto existe
    ]
    mock_con.cursor.return_value = mock_cursor

    response = client.post('/addCar', json={
        'id_usuario': 1,
        'id_producto': 10,
        'cantidad': 2
    })
    assert response.status_code == 200
    assert response.get_json()["message"] == "Producto agregado al carrito"

@patch("services.Compras.main.con")
def test_add_car_producto_no_disponible(mock_con, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.side_effect = [None, None]  # No orden, y producto no disponible
    mock_con.cursor.return_value = mock_cursor

    response = client.post('/addCar', json={
        'id_usuario': 1,
        'id_producto': 99,
        'cantidad': 3
    })
    assert response.status_code == 404
    assert "No se encontraron productos" in response.get_json()["message"]

# ---------- getOrden ----------
@patch("services.Compras.main.con")
def test_get_orden_con_productos(mock_con, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {'id_orden': 1}
    mock_cursor.fetchall.return_value = [{
        "id_detalle": 1, "nombre": "Taladro", "marca": "Bosch", "img": "img.png",
        "cantidad": 2, "subtotal": 2000, "precio_u": 1000
    }]
    mock_con.cursor.return_value = mock_cursor

    response = client.get('/getOrden/1')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

@patch("services.Compras.main.con")
def test_get_orden_sin_productos(mock_con, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_con.cursor.return_value = mock_cursor

    response = client.get('/getOrden/1')
    assert response.status_code == 404

# ---------- removeItem ----------
@patch("services.Compras.main.con")
def test_remove_item(mock_con, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {'id_orden': 1}
    mock_cursor.rowcount = 1
    mock_con.cursor.return_value = mock_cursor

    response = client.delete('/removeItem/5/1')
    assert response.status_code == 200
    assert response.get_json()["message"] == "Producto eliminado del carrito"

@patch("services.Compras.main.con")
def test_remove_item_no_existe(mock_con, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {'id_orden': 1}
    mock_cursor.rowcount = 0
    mock_con.cursor.return_value = mock_cursor

    response = client.delete('/removeItem/5/1')
    assert response.status_code == 500

# ---------- getDataOrden ----------
@patch("services.Compras.main.con")
def test_get_data_orden_existente(mock_con, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {
        "id_usuario": 1, "id_orden": 3, "total": 15000
    }
    mock_con.cursor.return_value = mock_cursor

    response = client.get("/getDataOrden/1")
    assert response.status_code == 200
    assert "total" in response.get_json()

@patch("services.Compras.main.con")
def test_get_data_orden_inexistente(mock_con, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_con.cursor.return_value = mock_cursor

    response = client.get("/getDataOrden/1")
    assert response.status_code == 404

# ---------- cerrarCompra ----------
@patch("services.Compras.main.con")
def test_cerrar_compra_exitoso(mock_con, client):
    mock_cursor = MagicMock()
    mock_cursor.rowcount = 1
    mock_con.cursor.return_value = mock_cursor

    response = client.post("/cerrarCompra/3/1")
    assert response.status_code == 200
    assert "Orden cerrada exitosamente" in response.get_json()["message"]

@patch("services.Compras.main.con")
def test_cerrar_compra_fallido(mock_con, client):
    mock_cursor = MagicMock()
    mock_cursor.rowcount = 0
    mock_con.cursor.return_value = mock_cursor

    response = client.post("/cerrarCompra/3/1")
    assert response.status_code == 500
