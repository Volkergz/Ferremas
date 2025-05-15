from flask import Flask, request, jsonify
import mysql.connector

#app es la instancia de Flask
app = Flask(__name__)

#Configuración de la base de datos
con = mysql.connector.connect(
    host="localhost", #La IP es Localhost y el puerto es 3306
    user="root",
    password="root",
    database="ferremas"
)

@app.route('/addCar', methods=['POST'])
def addCar():
    try:
        req = request.get_json()
        data = {
            'id_usuario': req['id_usuario'],
            'id_producto': req['id_producto'],
            'cantidad': req['cantidad']
        }

        cursor = con.cursor(dictionary=True)

        stmt = "SELECT id_orden FROM orden_compra WHERE id_usuario = %s AND estado = 0"
        cursor.execute(stmt, (data['id_usuario'],))
        result = cursor.fetchone()

        if result is None:
            stmt = "INSERT INTO orden_compra (id_usuario, total_orden, fecha_orden, estado) VALUES (%s, %s, CURRENT_DATE(), %s)"
            cursor.execute(stmt, (data['id_usuario'], 0, 0))
            id_orden = cursor.lastrowid
        else:
            id_orden = result['id_orden']

        stmt = "SELECT id_producto, precio FROM producto WHERE id_producto = %s AND estado = 1 AND stock >= %s"
        cursor.execute(stmt, (data['id_producto'], data['cantidad']))
        result = cursor.fetchone()

        if result is None:
            return jsonify({'message': 'No se encontraron productos'}), 404

        subtotal = data['cantidad'] * result['precio']
        stmt = "INSERT INTO detalle_orden (id_orden, id_producto, cantidad, subtotal, precio_u) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(stmt, (id_orden, result['id_producto'], data['cantidad'], subtotal, result['precio']))

        if cursor.rowcount == 0:
            return jsonify({'message': 'No se pudo insertar el detalle de la orden'}), 500

        con.commit()
        return jsonify({'message': 'Producto agregado al carrito'}), 200

    except Exception as e:
        con.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()



#Nota: ejecutar el siguiente comando para correr el servidor en modo debug
# flask run --host=0.0.0.0 --port=5000 --debug

#Ejecutamos el servidor en modo debug
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)