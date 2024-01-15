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


class grafica(View):

    def get(self, request):
        
        
        if request.method == "GET":
           
            estado = request.GET.get('estado', '')

            # Aquí puedes hacer lo que necesites con el parámetro 'estado'
            print(f"Estado: {estado}")

            # Puedes devolver una respuesta JSON si es necesario
            response_data = {'mensaje': 'Datos recibidos correctamente'}
           
            if estado == "Estado1" or estado == "Estado2" or estado == "Estado3":

                guardar_en_archivo(estado, 'estado.txt')
            else:
                guardar_en_archivo2(estado, 'estado3.txt')

              

            conn = mysql.connector.connect(   host="srv1138.hstgr.io",
                user="u153713658_sensores",
                password="?4K92JUGsHd",
                database="u153713658_base_proyecto")

            contenido2 = leer_archivo2('estado3.txt')

            if contenido2 == "," or not contenido2:
            # Consultar los datos
                query = "SELECT TEMPERATURA, HUMEDAD, VELOCIDAD_VIENTO, DIRECCION_VIENTO, CANTIDAD_LLUVIA, FECHA, HORA FROM SENSORES; "
            else:
                fechas_lista = contenido2.split(',')
                fecha_inicio = fechas_lista[0] if fechas_lista else None
                print(fecha_inicio)
                fecha_fin = fechas_lista[-1] if fechas_lista else None
                print(fecha_fin)
                query = "SELECT TEMPERATURA, HUMEDAD, VELOCIDAD_VIENTO, DIRECCION_VIENTO, CANTIDAD_LLUVIA, FECHA, HORA FROM SENSORES WHERE FECHA >= '"+fecha_inicio+"' AND FECHA <= '"+fecha_fin+"'; "
            
            df = pd.read_sql(query, conn)
            # Cerrar la conexión
            conn.close()

            # Preprocesar los datos
            # Convertir la columna FECHA y HORA a un solo campo de datetime
            # Convertir la columna FECHA a datetime (si aún no lo es)
            df['FECHA'] = pd.to_datetime(df['FECHA'])

            # Convertir la columna HORA a timedelta (si aún no lo es)
            df['HORA'] = pd.to_timedelta(df['HORA'].astype(str))

            # Crear la columna FECHA_HORA combinando FECHA y HORA
            df['FECHA_HORA'] = df['FECHA'] + df['HORA']

            # Establecer la columna FECHA_HORA como el índice
            df = df.set_index('FECHA_HORA')

            # Eliminar las columnas FECHA y HORA
            df = df.drop(['FECHA', 'HORA'], axis=1)
           

            # Dividir los datos en entrenamiento y prueba
            train_size = int(len(df) * 0.70)
            train, test = df[0:train_size], df[train_size:]
            # Separar características y etiquetas
            X_train, y_train = train.drop('TEMPERATURA', axis=1), train['TEMPERATURA']
            X_test, y_test = test.drop('TEMPERATURA', axis=1), test['TEMPERATURA']
            # Entrenar un modelo (usando Random Forest como ejemplo)

            contenido = leer_archivo('estado.txt')

            if not contenido:
                model = LinearRegression()
                MODELO_NOMBRE= "REGRESION LINEAL"

            if contenido == "Estado1":
                model = LinearRegression()
                MODELO_NOMBRE= "REGRESION LINEAL"
            if contenido == "Estado2":
                model= SVR(kernel='linear')
                MODELO_NOMBRE= "SVR"
            if contenido == "Estado3":
                MODELO_NOMBRE= "RAMDOM FOREST REGRESSOR"
                model = RandomForestRegressor()
           
            model.fit(X_train, y_train)

            # Hacer predicciones
            predictions = model.predict(X_test)
            ultimo_valor_prediccion = predictions[-1]
           
            # Extraer la fecha y la temperatura de la última fila del conjunto de prueba
            ultima_fila_test = test.tail(1)
            ultima_fecha_prediccion = ultima_fila_test.index[0]

            # Sumar un día a la última fecha de predicción
            nueva_fecha_prediccion = ultima_fecha_prediccion + timedelta(days=1)
          
            # Evaluar el rendimiento del modelo
            mse = mean_squared_error(y_test, predictions)

            #Coeficiente de Determinación 
            r = r2_score(y_test, predictions)
          
            # Error Porcentual Absoluto Medio (MAPE)
            mape = np.mean(np.abs((y_test - predictions) / y_test)) * 100
       
            y_test_list = y_test.tolist()
            y_test_list_enteros = [int(numero) for numero in y_test_list]
           
            predictions_list = predictions.tolist()

            fechas_timestamp = test.index.to_list()

            # Convierte los objetos Timestamp a cadenas de texto
            fechas_str = [str(fecha) for fecha in fechas_timestamp]
            fechas_json = json.dumps(fechas_str, ensure_ascii=False)
           

           #####################################################################################################
            #PREDICCION DE HUMEDAD

            train_size_humedad = int(len(df) * 0.70)
            train_humedad, test_humedad = df[0:train_size_humedad], df[train_size_humedad:]
            # Separar características y etiquetas
            X_train_hume, y_train_hume = train_humedad.drop('HUMEDAD', axis=1), train_humedad['HUMEDAD']
            X_test_hume, y_test_hume = test_humedad.drop('HUMEDAD', axis=1), test_humedad['HUMEDAD']
            # Entrenar un modelo (usando Random Forest como ejemplo)

            if not contenido:
                model_humedad = LinearRegression()
                MODELO_NOMBRE= "REGRESION LINEAL"

            if contenido == "Estado1":
                model_humedad= LinearRegression()
                MODELO_NOMBRE= "REGRESION LINEAL"
            if contenido == "Estado2":
                model_humedad = SVR(kernel='linear')
                MODELO_NOMBRE= "SVR"
            if contenido == "Estado3":
                MODELO_NOMBRE= "RAMDOM FOREST REGRESSOR"
                model_humedad = RandomForestRegressor()

            model_humedad.fit(X_train_hume, y_train_hume)


             # Hacer predicciones
            predictions_hume = model_humedad.predict(X_test_hume)
            ultimo_valor_prediccion_hume = predictions_hume[-1]
           
            # Extraer la fecha y la temperatura de la última fila del conjunto de prueba
            ultima_fila_test_hume = test_humedad.tail(1)
            ultima_fecha_prediccion_hume = ultima_fila_test_hume.index[0]

            # Sumar un día a la última fecha de predicción
            nueva_fecha_prediccion_hume = ultima_fecha_prediccion_hume + timedelta(days=1)
          

            # Evaluar el rendimiento del modelo
            mse2 = mean_squared_error(y_test_hume, predictions_hume)

            #Coeficiente de Determinación 
            r2 = r2_score(y_test_hume, predictions_hume)
            
            # Error Porcentual Absoluto Medio (MAPE)
            mape2 = np.mean(np.abs((y_test_hume - predictions_hume) / y_test_hume)) * 100
       
            y_test_list_hume = y_test_hume.tolist()
            y_test_list_enteros_hume = [int(numero) for numero in y_test_list_hume]
           
            predictions_list_hume = predictions_hume.tolist()

            print(predictions_list_hume)


            # Obtener la última fila de características del conjunto de prueba
            ultima_fila_test_hume = X_test_hume.iloc[-1]

            # Obtener los nombres de las características
            # Hacer la predicción para el día siguiente
            prediccion_manana_hume = model_humedad.predict([ultima_fila_test_hume])
  
            print("Predicción para el día siguiente:", prediccion_manana_hume)


            #####################################################################################################
            #PREDICCION DE VELOCIDAD DEL VIENTO

            train_size_VELVIENTO = int(len(df) *  0.70)
            train_VELVIENTO, test_VELVIENTO = df[0:train_size_VELVIENTO], df[train_size_VELVIENTO:]
            # Separar características y etiquetas
            X_train_VELVIENTO, y_train_VELVIENTO= train_VELVIENTO.drop('VELOCIDAD_VIENTO', axis=1), train_VELVIENTO['VELOCIDAD_VIENTO']
            X_test_VELVIENTO, y_test_VELVIENTO = test_VELVIENTO.drop('VELOCIDAD_VIENTO', axis=1), test_VELVIENTO['VELOCIDAD_VIENTO']
            # Entrenar un modelo (usando Random Forest como ejemplo)

            if not contenido:
                model_VELVIENTO = LinearRegression()
                MODELO_NOMBRE= "REGRESION LINEAL"

            if contenido == "Estado1":
                model_VELVIENTO= LinearRegression()
                MODELO_NOMBRE= "REGRESION LINEAL"
            if contenido == "Estado2":
                model_VELVIENTO = SVR(kernel='linear')
                MODELO_NOMBRE= "SVR"
            if contenido == "Estado3":
                MODELO_NOMBRE= "RAMDOM FOREST REGRESSOR"
                model_VELVIENTO = RandomForestRegressor()

            model_VELVIENTO.fit(X_train_VELVIENTO, y_train_VELVIENTO)


             # Hacer predicciones
            predictions_VELVIENTO = model_VELVIENTO.predict(X_test_VELVIENTO)
            ultimo_valor_prediccion_VELVIENTO = predictions_VELVIENTO[-1]
           
            # Extraer la fecha y la temperatura de la última fila del conjunto de prueba
            ultima_fila_test_VELVIENTO = test_VELVIENTO.tail(1)
            ultima_fecha_prediccion_VELVIENTO = ultima_fila_test_VELVIENTO.index[0]

            # Sumar un día a la última fecha de predicción
            nueva_fecha_prediccion_VELVIENTO = ultima_fecha_prediccion_VELVIENTO + timedelta(days=1)
          

             # Evaluar el rendimiento del modelo
            mse3 = mean_squared_error(y_test_VELVIENTO, predictions_VELVIENTO)

            #Coeficiente de Determinación 
            r3 = r2_score(y_test_VELVIENTO, predictions_VELVIENTO)
            
            # Error Porcentual Absoluto Medio (MAPE)
            mape3 = np.mean(np.abs((y_test_VELVIENTO - predictions_VELVIENTO) / y_test_VELVIENTO)) * 100
            
       
            y_test_list_VELVIENTO = y_test_VELVIENTO.tolist()
            y_test_list_enteros_VELVIENTO = [int(numero) for numero in y_test_list_VELVIENTO]
           
            predictions_list_VELVIENTO = predictions_VELVIENTO.tolist()

            print(predictions_list_VELVIENTO)


            # Obtener la última fila de características del conjunto de prueba
            ultima_fila_test_VELVIENTO = X_test_VELVIENTO.iloc[-1]

            # Obtener los nombres de las características
            # Hacer la predicción para el día siguiente
            prediccion_manana_VELVIENTO = model_VELVIENTO.predict([ultima_fila_test_VELVIENTO])
  
            print("Predicción para el día siguiente:", prediccion_manana_VELVIENTO)



              #####################################################################################################
            #PREDICCION DE DIRECCION DEL VIENTO

            train_size_DIRVIENTO = int(len(df) *  0.70)
            train_DIRVIENTO, test_DIRVIENTO = df[0:train_size_DIRVIENTO], df[train_size_DIRVIENTO:]
            # Separar características y etiquetas
            X_train_DIRVIENTO, y_train_DIRVIENTO= train_DIRVIENTO.drop('DIRECCION_VIENTO', axis=1), train_DIRVIENTO['DIRECCION_VIENTO']
            X_test_DIRVIENTO, y_test_DIRVIENTO = test_DIRVIENTO.drop('DIRECCION_VIENTO', axis=1), test_DIRVIENTO['DIRECCION_VIENTO']
            # Entrenar un modelo (usando Random Forest como ejemplo)

            if not contenido:
                model_DIRVIENTO = LinearRegression()
                MODELO_NOMBRE= "REGRESION LINEAL"

            if contenido == "Estado1":
                model_DIRVIENTO= LinearRegression()
                MODELO_NOMBRE= "REGRESION LINEAL"
            if contenido == "Estado2":
                model_DIRVIENTO = SVR(kernel='linear')
                MODELO_NOMBRE= "SVR"
            if contenido == "Estado3":
                MODELO_NOMBRE= "RAMDOM FOREST REGRESSOR"
                model_DIRVIENTO = RandomForestRegressor()

            model_DIRVIENTO.fit(X_train_DIRVIENTO, y_train_DIRVIENTO)


             # Hacer predicciones
            predictions_DIRVIENTO = model_DIRVIENTO.predict(X_test_DIRVIENTO)
            ultimo_valor_prediccion_DIRVIENTO = predictions_DIRVIENTO[-1]
           
            # Extraer la fecha y la temperatura de la última fila del conjunto de prueba
            ultima_fila_test_DIRVIENTO = test_DIRVIENTO.tail(1)
            ultima_fecha_prediccion_DIRVIENTO = ultima_fila_test_DIRVIENTO.index[0]

            # Sumar un día a la última fecha de predicción
            nueva_fecha_prediccion_DIRVIENTO = ultima_fecha_prediccion_DIRVIENTO + timedelta(days=1)
          

            # Evaluar el rendimiento del modelo
            mse4 = mean_squared_error(y_test_DIRVIENTO, predictions_DIRVIENTO)

            #Coeficiente de Determinación 
            r4 = r2_score(y_test_DIRVIENTO, predictions_DIRVIENTO)
            
            # Error Porcentual Absoluto Medio (MAPE)
            mape4 = np.mean(np.abs((y_test_DIRVIENTO - predictions_DIRVIENTO) / y_test_DIRVIENTO)) * 100
            
       
            y_test_list_DIRVIENTO = y_test_DIRVIENTO.tolist()
            y_test_list_enteros_DIRVIENTO = [int(numero) for numero in y_test_list_DIRVIENTO]
           
            predictions_list_DIRVIENTO = predictions_DIRVIENTO.tolist()
            
            print(predictions_list_DIRVIENTO)


            # Obtener la última fila de características del conjunto de prueba
            ultima_fila_test_DIRVIENTO = X_test_DIRVIENTO.iloc[-1]

            # Obtener los nombres de las características
            # Hacer la predicción para el día siguiente
            prediccion_manana_DIRVIENTO = model_DIRVIENTO.predict([ultima_fila_test_DIRVIENTO])
  
            print("Predicción para el día siguiente:", prediccion_manana_DIRVIENTO)
            
           
           # Convierte la cadena JSON a una lista de fechas
            fechas_list = json.loads(fechas_json)

            # Suma un día a cada fecha
            fechas_con_un_dia_mas = [(datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S") + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S") for fecha in fechas_list]

            # Imprime las fechas con un día más
            print(fechas_con_un_dia_mas)
            
           
            combined_list = list(zip(predictions_list, fechas_con_un_dia_mas))

            print(combined_list)
            context = {
                'MODELO_NOMBRE':MODELO_NOMBRE,

                'y_test_json': json.dumps(y_test_list_enteros,default=int),
                'predictions_json': json.dumps(predictions_list),
                'temp_predi':nueva_fecha_prediccion,
                'fechas': fechas_con_un_dia_mas,
                'fechas_REAL': fechas_json,
                'predictions_sorted': combined_list,
                'PREDICCION': round(ultimo_valor_prediccion, 2),
                'ERROR':round(100-mse),
                'ERROR12':round(r,2),
                'ERROR13':round(mape,2),
               

                'HUMEDAD_REAL': y_test_list_hume,
                'PREDI_HUMEDAD':predictions_list_hume,
                'PREDICCION_DIA_HUMEDAD': round(int(prediccion_manana_hume), 2),
                'ERROR2':round(100-mse2),
                'ERROR22':round(r2,2),
                'ERROR23':round(mape2,2),


                'VELVIENTO_REAL': y_test_list_VELVIENTO,
                'PREDI_VELVIENTO':predictions_list_VELVIENTO,
                'PREDICCION_DIA_VELVIENTO': round(int(prediccion_manana_VELVIENTO), 2),
                'ERROR3':round(max(0, 100 - mse3)) if mse3 != float('inf') else 0,
                'ERROR32':max(0, round(r3, 2)) if r3 != float('inf') else 0,
                'ERROR33':max(0, round(mape3, 2)) if mape3 != float('inf') else 0,

                'DIRVIENTO_REAL': y_test_list_DIRVIENTO,
                'PREDI_DIRVIENTO':predictions_list_DIRVIENTO,
                'PREDICCION_DIA_DIRVIENTO': round(int(prediccion_manana_DIRVIENTO), 2),
                'ERROR4':round(max(0, 100 - mse4)) if mse4 != float('inf') else 0,
                'ERROR42':max(0, round(r4, 2))if r3 != float('inf') else 0,
                'ERROR43':max(0, round(mape4, 2)) if mape4 != float('inf') else 0,

            }
            
        return render(request, 'index.html', context)
    
def guardar_en_archivo(estado, nombre_archivo):
    # Ruta completa al archivo de texto
    archivo_path = os.path.join('archivos_estados', nombre_archivo)

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


def guardar_en_archivo2(estado2, nombre_archivo):
    # Ruta completa al archivo de texto
    archivo_path = os.path.join('archivos_estados3', nombre_archivo)

    # Verificar si el estado no está vacío antes de guardarlo
    if estado2:
        # Verificar si el archivo existe, y si no, crearlo
        if not os.path.exists(archivo_path):
            os.makedirs(os.path.dirname(archivo_path), exist_ok=True)
            with open(archivo_path, "w") as archivo:
                archivo.write(estado2)
        else:
            # Guardar el estado en el archivo (se sobrescribe el contenido existente)
            with open(archivo_path, "w") as archivo:
                archivo.write(estado2)

def leer_archivo(nombre_archivo):
    # Ruta completa al archivo de texto
    archivo_path = os.path.join('archivos_estados', nombre_archivo)

    # Leer el contenido del archivo
    contenido = ""
    if os.path.exists(archivo_path):
        with open(archivo_path, "r") as archivo:
            contenido = archivo.read()

    return contenido

def leer_archivo2(nombre_archivo):
    # Ruta completa al archivo de texto
    archivo_path = os.path.join('archivos_estados3', nombre_archivo)

    # Leer el contenido del archivo
    contenido = ""
    if os.path.exists(archivo_path):
        with open(archivo_path, "r") as archivo:
            contenido = archivo.read()

    return contenido