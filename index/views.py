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
# Conectar a la base de datos
import re

class grafica(View):

    def get(self, request):
        

            if request.method == "GET":
                    
            
                    conn = mysql.connector.connect(
                    host="srv1138.hstgr.io",
                    user="u153713658_esp",
                    password="1234.Proyecto",
                    database="u153713658_sensores"
                    )

                # Consultar los datos
                    query = "SELECT temperatura,humedad,distancia,luz,hora,mq,fecha FROM esp"
                
                    df = pd.read_sql(query, conn)
                # Cerrar la conexión
                    conn.close()
                    temp = df['temperatura'].tolist()
                    hum = df['humedad'].tolist()
                    dis = df['distancia'].tolist()
                    mq = df['mq'].tolist()
                    # Preprocesar los datos
                    # Convertir la columna FECHA y HORA a un solo campo de datetime
                    # Convertir la columna FECHA a datetime (si aún no lo es)
                    df['fecha'] = pd.to_datetime(df['fecha'])

                    # Convertir la columna HORA a timedelta (si aún no lo es)
                    df['hora'] = pd.to_timedelta(df['hora'].astype(str))

                    # Crear la columna FECHA_HORA combinando FECHA y HORA
                    df['FECHA_HORA'] = df['fecha'] + df['hora']

                    # Establecer la columna FECHA_HORA como el índice
                    df = df.set_index('FECHA_HORA')

                    # Eliminar las columnas FECHA y HORA
                    df = df.drop(['fecha', 'hora'], axis=1)
            

            

                    df = df.index.to_list()

                    # Convierte los objetos Timestamp a cadenas de texto
                    fechas_str = [str(fecha) for fecha in df]
                    fechas_json = json.dumps(fechas_str, ensure_ascii=False)
                   
                    print(fechas_json)
                   
                    fechas_list = json.loads(fechas_json)

                    hum = [float(num_str) for num_str in hum]
                

                    dis = [float(num_str1) for num_str1 in dis]
                 

                    mq = [float(num_str2) for num_str2 in mq]
                  

                    temp = [float(num_str3) for num_str3 in temp]
             
                    print(temp)
                    

                    context = {
            
                        'fechas_REAL': fechas_json,
                        'y_test_json': temp,
                
                        'HUMEDAD_REAL': json.dumps(hum,default=int),
                        


                        'VELVIENTO_REAL': json.dumps(dis,default=int),
                    

                        'DIRVIENTO_REAL': json.dumps(mq,default=int),
                    }
            
            return render(request, 'index.html', context)
    
