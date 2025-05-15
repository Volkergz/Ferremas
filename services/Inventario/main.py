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

@app.route('/productos', methods=['POST'])
def getProductos():

    #Creamos un cursor para ejecutar la consulta
    cursor = con.cursor(dictionary=True)

    #Creamos la consulta para obtener los productos activos
    stmt = "SELECT * FROM producto WHERE estado = 1"

    #Ejecutamos la consulta para obtener los productos activos
    cursor.execute(stmt)

    #Obtenemos el resultado de la consulta
    result = cursor.fetchall()

    #Cerramos el cursor
    cursor.close()

    #Si el resultado es None, significa que no hay productos activos
    if result is None:
        return jsonify({'message': 'No se encontraron productos'}), 404

    #Si el usuario existe, devolvemos un mensaje de éxito
    return jsonify(result), 200
    
@app.route('/productos/<int:id>', methods=['get'])
def getProducto(id):

    # Creamos un cursor para ejecutar la consulta
    cursor = con.cursor(dictionary=True)

    # Creamos la consulta para obtener el producto por id
    stmt = "SELECT * FROM producto WHERE id_producto = %s AND estado = 1"
    
    # Ejecutamos la consulta para obtener el producto por id
    cursor.execute(stmt, (id,))

    # Obtenemos el resultado de la consulta
    result = cursor.fetchone()

    # Cerramos el cursor
    cursor.close()

    # Si el resultado es None, significa que no existe el producto
    if result is None:
        return jsonify({'message': 'No se encontraron productos'}), 404

    # Si el usuario existe, devolvemos un mensaje de éxito
    return jsonify(result), 200

#Nota: ejecutar el siguiente comando para correr el servidor en modo debug
# flask run --host=0.0.0.0 --port=5001 --debug

#Ejecutamos el servidor en modo debug
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)