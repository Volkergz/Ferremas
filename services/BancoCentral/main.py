from flask import Flask, jsonify
from datetime import datetime, timedelta
import bcchapi
import mysql.connector

#Configuración de la base de datos
con = mysql.connector.connect(
    host="localhost", #La IP es Localhost y el puerto es 3306
    user="root",
    password="root",
    database="ferremas"
)

app = Flask(__name__)

# Conexión a la API del Banco Central de Chile
siete = bcchapi.Siete("haleymgabrielhidalgo@gmail.com", "Hght19092003*")

@app.route('/getDollar', methods=['GET'])
def get_dollar():

    #Obtenemos la fecha actual
    current_date = datetime.today()

    #Nota: La API del Banco Central de Chile no actualiza el valor del dólar en tiempo real, por lo que se recomienda usar la fecha de ayer
    #current_date = current_date - timedelta(days=1)
    #print(current_date)

    # Convertimos la fecha a un formato de cadena
    date_str = current_date.strftime('%Y-%m-%d')

    dollar_value = None

    # Obtenemos el valor del dólar en la BD propia
    try:
        # Creamos un cursor para ejecutar la consulta
        cursor = con.cursor(dictionary=True)

        # Creamos la consulta para obtener el producto por id
        stmt = "SELECT valor, fecha FROM moneda WHERE id_moneda = 1 AND fecha = %s"
        
        # Ejecutamos la consulta para obtener el producto por id
        cursor.execute(stmt, (date_str,))

        # Obtenemos el resultado de la consulta
        result = cursor.fetchone()

        # Cerramos el cursor
        cursor.close()

        # Si el resultado es distinto de None, significa que la moneda esta actualizada y no es necesario consultar la API del Banco Central de Chile
        if result is not None:
            dollar_value = result['valor']
            
        else:
            # Si no existe el una tasa actual, lo obtenemos de la API del Banco Central de Chile
            # Obtenemos el valor del dólar
            df = siete.cuadro(
                series=["F073.TCO.PRE.Z.D"],
                nombres=["dolar"],
                desde=date_str,
                hasta=date_str,
            )

            if df.empty:
                return jsonify({"error": "No se encontro una tasa para la fecha indicada"}), 404
            
            # Obtenemos el valor del dólar
            dollar_value = df["dolar"].iloc[0]
            
            # Guardamos el valor en la base de datos
            cursor = con.cursor()
            stmt = "UPDATE moneda SET valor = %s, fecha = %s WHERE id_moneda = 1"
            cursor.execute(stmt, (dollar_value, date_str))
            con.commit()
            cursor.close()
    
    except mysql.connector.Error as err:
        # Manejo de errores de la base de datos
        return jsonify({"error": "Error en la base de datos: " + str(err)}), 500

    finally:

        # Devolvemos el valor del dólar en formato JSON
        return jsonify({"fecha_consulta": date_str, "dollar_value": dollar_value}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
