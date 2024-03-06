from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import View 
from django.http import HttpResponse, JsonResponse
import csv 
import pandas as pd
from firebase_admin import db
from django.shortcuts import render
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
import io
from io import BytesIO
import base64
from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import View 
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
import json
from sklearn.metrics import r2_score
import os
class ReportePersonalizadoExcel(TemplateView):
    def get(self,request,*args,**kwargs):
            # Conectar a la base de datos
        conn = mysql.connector.connect(
            host="srv1138.hstgr.io",
            user="u153713658_esp",
            password="1234.Proyecto",
            database="u153713658_sensores"
        )

        # Consultar los datos
        query = "SELECT * FROM esp ORDER by id DESC"
        cur = conn.cursor()
        cur.execute(query)
        datos = cur.fetchall()

        # Cerrar la conexión
        conn.close()

        # Crear un archivo CSV
        field_names = ['TEMPERATURA (CELCIUS)', 'HUMEDAD (%)', 'DISTANCIA (CM)', 'CALIDAD DEL AIRE (ppm)', 'CANTIDAD DE LUZ (%)', 'HORA', 'FECHA']
        with open('Names.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Escribir los encabezados
            writer.writerow(field_names)
            # Escribir los datos
            writer.writerows(datos)

        # Crear un DataFrame de Pandas desde el archivo CSV
        df = pd.read_csv('Names.csv')

        # Crear una respuesta HTTP para descargar el archivo Excel
        response = HttpResponse(content_type='application/ms-excel')
        nombre_archivo = "RegistrosSQL.xlsx"
        contenido = f"attachment; filename={nombre_archivo}"
        response["Content-Disposition"] = contenido

        # Convertir el DataFrame a Excel y escribir en la respuesta HTTP
        df.to_excel(response, index=False)

        return response
