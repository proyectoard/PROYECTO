from django.shortcuts import render
import smtplib
import os
from django.http import JsonResponse
import requests

limite_inferior = 30
limite_superior = 40

limite_inferiorHUM = 79
limite_superiorHUM = 100

cont = 0
nombre_archivo = "estado2.txt"
def enviar_correo(asunto, mensaje):
   
    remitente_email = 'meteorologicoproyecto@gmail.com'
    remitente_password = 'fknijbyktvqhfnlw'

    # Reemplaza con la dirección de correo electrónico de destino
    
    destinatarios = ['nicolascrespod@gmail.com', 'meteorologicoproyecto@gmail.com']
    # Configuración del servidor SMTP de Gmail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente_email, remitente_password)

    # Construye el mensaje de correo electrónico
    mensaje_email = f"Subject: {asunto}\n\n{mensaje}"
    mensaje_email = mensaje_email.encode('utf-8')
    # Envía el correo electrónico
    server.sendmail(remitente_email, destinatarios, mensaje_email)

    # Cierra la conexión al servidor SMTP
    server.quit()


def obtener_datos(request):
    api_url = "https://blynk.cloud/external/api/get?token=2mAMfT5kz3MKfie1m0IiBLqm9mvzFkuV&v0&v1&v2&v3&v4"
    response = requests.get(api_url)
    
    alerta_enviada = False
    
    
    if response.status_code == 200:
        data = response.json()
        valor_v3 = data.get('v3')
        valor_v4 = data.get('v4')
        
        print(limite_inferior)
        contenido = leer_archivo('estado2.txt')
        contenido2 = leer_archivo2('estado5.txt')

        print(contenido + " esto es cont")
        if limite_inferior < valor_v3 < limite_superior and contenido == "false" or contenido == "":
        # Envía el correo electrónico solo si la temperatura está entre los límites
            print("ENVIO ALERTA")
            enviar_correo('Alerta de alta temperatura', f'La temperatura actual es {valor_v3}°C,  https://estacionmeteorologica-tlm.tech/')
            guardar_en_archivo("true", 'estado2.txt')

        elif valor_v3 < limite_inferior or valor_v3 > limite_superior:
            # Restablece la variable de alerta_enviada si el valor de v3 está fuera de los límites
             guardar_en_archivo("false", 'estado2.txt')

        if limite_inferiorHUM < valor_v4 < limite_superiorHUM and contenido2 == "false" or contenido2 == "":
            # Envía el correo electrónico solo si la temperatura está entre los límites
            print("ENVIO ALERTA")
            enviar_correo('Alerta de alta HUMEDAD, PROBABILIDAD DE LLUVIAS', f'La humedad actual es {valor_v4}°%,  https://estacionmeteorologica-tlm.tech/')
            guardar_en_archivo2("true", 'estado5.txt')

        elif valor_v3 < limite_inferior or valor_v3 > limite_superior:
            # Restablece la variable de alerta_enviada si el valor de v3 está fuera de los límites
             guardar_en_archivo("false", 'estado5.txt')
            
        return JsonResponse(data)        
    else:
        return JsonResponse({'error': 'Error en la solicitud'}, status=500)
    

def guardar_en_archivo(estado, nombre_archivo):
    # Ruta completa al archivo de texto
    archivo_path = os.path.join('archivos_estados2', nombre_archivo)

    # Verificar si el estado no está vacío antes de guardarlo
    if estado:
        # Verificar si el archivo existe, y si no, crearlo
        if not os.path.exists(archivo_path):
            os.makedirs(os.path.dirname(archivo_path), exist_ok=True)
            with open(archivo_path, "w") as archivo:
                archivo.write(estado)
        else:
            # Guardar el estado en el archivo (se sobrescribe el contenido existente)
            with open(archivo_path, "w") as archivo:
                archivo.write(estado)

def guardar_en_archivo2(estado, nombre_archivo):
    # Ruta completa al archivo de texto
    archivo_path = os.path.join('archivos_estados6', nombre_archivo)

    # Verificar si el estado no está vacío antes de guardarlo
    if estado:
        # Verificar si el archivo existe, y si no, crearlo
        if not os.path.exists(archivo_path):
            os.makedirs(os.path.dirname(archivo_path), exist_ok=True)
            with open(archivo_path, "w") as archivo:
                archivo.write(estado)
        else:
            # Guardar el estado en el archivo (se sobrescribe el contenido existente)
            with open(archivo_path, "w") as archivo:
                archivo.write(estado)


def leer_archivo2(nombre_archivo):
    # Ruta completa al archivo de texto
    archivo_path = os.path.join('archivos_estados6', nombre_archivo)

    # Leer el contenido del archivo
    contenido = ""
    if os.path.exists(archivo_path):
        with open(archivo_path, "r") as archivo:
            contenido = archivo.read()

    return contenido

def leer_archivo(nombre_archivo):
    # Ruta completa al archivo de texto
    archivo_path = os.path.join('archivos_estados2', nombre_archivo)

    # Leer el contenido del archivo
    contenido = ""
    if os.path.exists(archivo_path):
        with open(archivo_path, "r") as archivo:
            contenido = archivo.read()

    return contenido

