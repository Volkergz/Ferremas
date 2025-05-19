from flask import Flask, jsonify
from datetime import datetime, timedelta
import bcchapi

app = Flask(__name__)

# Conexión a la API del Banco Central de Chile
siete = bcchapi.Siete("haleymgabrielhidalgo@gmail.com", "Hght19092003*")

@app.route('/getDollar', methods=['GET'])
def get_dollar():

    try:
        
        #Obtenemos la fecha actual
        current_date = datetime.today()

        #Nota: La API del Banco Central de Chile no actualiza el valor del dólar en tiempo real, por lo que se recomienda usar la fecha de ayer
        #current_date = current_date - timedelta(days=1)
        #print(current_date)

        # Convertimos la fecha a un formato de cadena
        date_str = current_date.strftime('%Y-%m-%d')

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

        # Devolvemos el valor del dólar en formato JSON
        return jsonify({"fecha_consulta": date_str, "dollar_value": dollar_value}), 200
    
    except Exception as e:
        # Manejo de errores
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
