import schedule
import time
import requests

def job():
    print("Ejecutando la tarea cada 5 minutos..")
    
    api_url = "https://blynk.cloud/external/api/get?token=2mAMfT5kz3MKfie1m0IiBLqm9mvzFkuV&v0&v1&v2&v3&v4"

    # Realizar la solicitud a la API
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
        

schedule.every(0.5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(0.5)