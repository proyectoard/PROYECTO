import schedule
import time
import requests

def job():
    print("Ejecutando la tarea cada 5 minutos..")
    
    api_url = "https://blynk.cloud/external/api/get?token=2mAMfT5kz3MKfie1m0IiBLqm9mvzFkuV&v0&v1&v2&v3&v4"

    response = requests.get(api_url)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Obtener los datos de la respuesta JSON
        data = response.json()

        # Acceder a cada valor individualmente
        value_v0 = data.get('v0', None)
        value_v1 = data.get('v1', None)
        value_v2 = data.get('v2', None)
        value_v3 = data.get('v3', None)
        value_v4 = data.get('v4', None)

        # Imprimir cada valor individualmente
        print(f"v0: {value_v0}")
        print(f"v1: {value_v1}")
        print(f"v2: {value_v2}")
        print(f"v3: {value_v3}")
        print(f"v4: {value_v4}")

        # Insertar datos en la base de datos
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="tu_usuario",
                password="tu_contraseña",
                database="nombre_de_tu_base_de_datos"
            )

            cursor = connection.cursor()

            # Supongamos que `data` contiene los valores que obtuviste de la API
            query = """
            INSERT INTO tuapp_mediciones (temperatura, humedad, velocidad_viento, direccion_viento, cantidad_lluvia)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (value_v0, value_v1, value_v2, value_v3, value_v4))

            connection.commit()

        except Exception as e:
            print(f"Error al insertar datos en la base de datos: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    else:
        # Manejar el caso en que la solicitud no fue exitosa
        print(f"Error al obtener datos. Código de estado: {response.status_code}")

schedule.every(0.5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(0.5)