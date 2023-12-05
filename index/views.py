from django.shortcuts import render
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
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
# Conectar a la base de datos


class grafica(View):

    def get(self, request):
        
        if request.method == "GET":
            conn = mysql.connector.connect(   host="srv1138.hstgr.io",
                user="u153713658_sensores",
                password="?4K92JUGsHd",
                database="u153713658_base_proyecto")

            print("HOLA")
            # Consultar los datos
            query = "SELECT TEMPERATURA, HUMEDAD, VELOCIDAD_VIENTO, DIRECCION_VIENTO, CANTIDAD_LLUVIA, FECHA, HORA FROM SENSORES"
            df = pd.read_sql(query, conn)
            print(df)
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
            print(df)
            # Crear características adicionales si es necesario
            # Por ejemplo, podrías extraer el día de la semana, mes, etc.

            # Dividir los datos en entrenamiento y prueba
            train_size = int(len(df) * 0.8)
            train, test = df[0:train_size], df[train_size:]

            # Separar características y etiquetas
            X_train, y_train = train.drop('TEMPERATURA', axis=1), train['TEMPERATURA']
            X_test, y_test = test.drop('TEMPERATURA', axis=1), test['TEMPERATURA']

            # Entrenar un modelo (usando Random Forest como ejemplo)
            model = RandomForestRegressor()
            model.fit(X_train, y_train)

            # Hacer predicciones
            predictions = model.predict(X_test)

            # Evaluar el rendimiento del modelo
            mse = mean_squared_error(y_test, predictions)
            print(f'Mean Squared Error: {mse}')

            plt.figure(figsize=(12, 6))
            plt.plot(test.index.astype(str), y_test, label='Real')
            plt.plot(test.index.astype(str), predictions, label='Predicción')
            plt.legend()
            plt.title('Predicciones de Temperatura')
            plt.xlabel('Fecha y Hora')
            plt.ylabel('Temperatura')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()

            # Convertir el gráfico a una cadena base64 (opcional si todavía necesitas la representación base64)

            # Convertir el gráfico a una cadena base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            graphic = base64.b64encode(image_png).decode('utf-8')

            # Pasar la cadena base64 a la plantilla
            context = {'graphic': graphic}

        return render(request, 'index.html', context)