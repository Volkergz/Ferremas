from flask import Flask, request, jsonify
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys
from flask_cors import CORS

## Installs necesarios: flask , transbank-sdk , flask-cors

app = Flask(__name__)
CORS(app)

datos = WebpayOptions(
    commerce_code=IntegrationCommerceCodes.WEBPAY_PLUS,
    api_key=IntegrationApiKeys.WEBPAY,
    integration_type=IntegrationType.TEST
)

@app.route('/crear-transaccion', methods=['POST'])
def crear_transaccion():
    data = request.json
    buy_order = data['buy_order']
    session_id = data['session_id']
    amount = data['amount']
    return_url = data['return_url']

    tx = Transaction(datos)
    response = tx.create(buy_order, session_id, amount, return_url)
    return jsonify(response)

@app.route('/confirmar-transaccion', methods=['POST'])
def confirmar_transaccion():
    data = request.json
    token = data['token_ws']

    tx = Transaction(datos)
    response = tx.commit(token)
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000)