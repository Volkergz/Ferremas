from flask import Flask, request, jsonify
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys

## Installs necesarios: flask , transbank-sdk , flask-cors

app = Flask(__name__)

options = WebpayOptions(
    commerce_code=IntegrationCommerceCodes.WEBPAY_PLUS,
    api_key=IntegrationApiKeys.WEBPAY,
    integration_type=IntegrationType.TEST
)

@app.route('/crear-transaccion', methods=['POST'])
def crear_transaccion():
    data = request.json
    buy_order = str(data['id_orden'])
    session_id = str(data['id_usuario'])
    amount = data['total']
    return_url = 'http://localhost:8000/carrito/confirmarCompra'

    # Validar los datos recibidos
    if not buy_order or not session_id or not amount or not return_url:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    # Validar el formato de amount
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        return jsonify({"error": "El monto debe ser un número positivo"}), 400

    # Generamos la transacción
    tx = Transaction(options)

    # Crear la transacción
    response = tx.create(buy_order, session_id, amount, return_url)

    return jsonify(response)

@app.route('/confirmar-transaccion', methods=['POST'])
def confirmar_transaccion():
    data = request.json
    token = data['token_ws']

    tx = Transaction(options)
    response = tx.commit(token)
    return jsonify(response)

#Ejecutamos el servidor en modo debug
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)