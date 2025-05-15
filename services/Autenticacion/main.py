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

@app.route('/auth', methods=['POST'])
def autenticateUser():
    
    #Recibimos el JSON del cliente
    data = request.get_json()
    user = {
        'email': data['email'],
        'password': data['password']
    }

    #Creamos un cursor para ejecutar la consulta
    cursor = con.cursor(dictionary=True)

    #Creamos la consulta para verificar si el usuario existe
    stmt = "SELECT * FROM usuario WHERE email = %s AND password = %s"

    #Ejecutamos la consulta para verificar si el usuario existe
    cursor.execute(stmt, (user['email'], user['password']))

    #Obtenemos el resultado de la consulta
    result = cursor.fetchone()

    #Cerramos el cursor
    cursor.close()

    #Si el resultado es None, significa que el usuario no existe
    if result is None:
        return jsonify({'message': 'Usuario o contraseña incorrectos'}), 401
    
    else:
        #Si el usuario existe, devolvemos un mensaje de éxito
        return jsonify({'data': result,}), 200

#Nota: ejecutar el siguiente comando para correr el servidor en modo debug
# flask run --host=0.0.0.0 --port=5000 --debug

#Ejecutamos el servidor en modo debug
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)