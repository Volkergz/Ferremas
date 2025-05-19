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
        
        #cierra el cursor
        cursor.close()

        return jsonify({'message': 'Producto agregado al carrito'}), 200

    except Exception as e:
        con.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/getOrden/<int:id_usuario>', methods=['GET'])
def gerOrden(id_usuario):

    try:

        # Crear un cursor para ejecutar consultas
        cursor = con.cursor(dictionary=True)

        # Verificar si el usuario tiene una orden activa
        stmt = "SELECT id_orden FROM orden_compra WHERE id_usuario = %s AND estado = 0"

        # Ejecutar la consulta
        cursor.execute(stmt, (id_usuario,))
        
        # Obtener el resultado
        result = cursor.fetchone()

        # Si no se encontró una orden activa, retornar un mensaje
        if result is None:
            return jsonify({'message': 'No se encontraron productos'}), 404

        # Si se encontró una orden activa, obtener los productos del carrito
        id_orden = result['id_orden']

        # Obtener los productos del carrito
        stmt = """
        SELECT d.id_detalle, p.nombre, p.marca, p.img, d.cantidad, d.subtotal, d.precio_u 
        FROM detalle_orden d 
        JOIN producto p ON d.id_producto = p.id_producto 
        WHERE d.id_orden = %s
        """
        
        # Ejecutar la consulta
        cursor.execute(stmt, (id_orden,))
        
        # Obtener el resultado
        result = cursor.fetchall()

        # Si no se encontraron productos, retornar un mensaje
        if not result:
            return jsonify({'message': 'No se encontraron productos en el carrito'}), 404

        # Cerrar la conexión
        cursor.close()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/removeItem/<int:id_detalle>/<int:id_usuario>', methods=['DELETE'])
def removeItem(id_detalle, id_usuario):
    
    try:
        # Crear un cursor para ejecutar consultas
        cursor = con.cursor(dictionary=True)

        # Verificar si el usuario tiene una orden activa
        stmt = "SELECT id_orden FROM orden_compra WHERE id_usuario = %s AND estado = 0"

        # Ejecutar la consulta
        cursor.execute(stmt, (id_usuario,))
        
        # Obtener el resultado
        result = cursor.fetchone()

        # Si no se encontró una orden activa, retornar un mensaje
        if result is None:
            return jsonify({'message': 'No se encontraron productos'}), 404

        # Si se encontró una orden activa, eliminar el producto del carrito
        id_orden = result['id_orden']

        # Eliminar el producto del carrito
        stmt = "DELETE FROM detalle_orden WHERE id_orden = %s AND id_detalle = %s"
        
        # Ejecutar la consulta
        cursor.execute(stmt, (id_orden, id_detalle))
        
        # Verificar si se eliminó el producto
        if cursor.rowcount == 0:
            return jsonify({'message': 'No se pudo eliminar el producto del carrito'}), 500

        con.commit()
        cursor.close()
        return jsonify({'message': 'Producto eliminado del carrito'}), 200

    except Exception as e:
        con.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/getDataOrden/<int:id_usuario>', methods=['GET'])
def getDataOrden(id_usuario):
    try:
        # Crear un cursor para ejecutar consultas
        cursor = con.cursor(dictionary=True)

        # Verificar si el usuario tiene una orden activa
        stmt = """
        SELECT oc.id_usuario, oc.id_orden, SUM(do.subtotal) AS total
        FROM detalle_orden do
        JOIN orden_compra oc ON do.id_orden = oc.id_orden
        WHERE oc.id_usuario = %s AND oc.estado = false
        GROUP BY oc.id_usuario, oc.id_orden;
        """

        # Ejecutar la consulta
        cursor.execute(stmt, (id_usuario,))
        
        # Obtener el resultado
        result = cursor.fetchone()

        # Si no se encontró una orden activa, retornar un mensaje
        if result is None:
            return jsonify({'message': 'No se encontraron Ordenes de este usuario'}), 404

        # Cerrar la conexión
        cursor.close()

        # Retornar el resultado
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/cerrarCompra/<int:id_orden>/<int:id_usuario>', methods=['POST'])
def cerrarCompra(id_orden, id_usuario):
    try:
        # Crear un cursor para ejecutar consultas
        cursor = con.cursor(dictionary=True)

        # Actualizar el estado de la orden a 1 (cerrada)
        stmt = "UPDATE orden_compra SET estado = 1 WHERE id_orden = %s AND id_usuario = %s"
        
        # Ejecutar la consulta
        cursor.execute(stmt, (id_orden, id_usuario))
        
        # Verificar si se actualizó la orden
        if cursor.rowcount == 0:
            return jsonify({'message': 'No se pudo cerrar la orden'}), 500

        con.commit()
        con.close()

        return jsonify({'message': 'Orden cerrada exitosamente'}), 200

    except Exception as e:
        con.rollback()
        return jsonify({'error': str(e)}), 500

#Nota: ejecutar el siguiente comando para correr el servidor en modo debug
# flask run --host=0.0.0.0 --port=5002 --debug

#Ejecutamos el servidor en modo debug
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)