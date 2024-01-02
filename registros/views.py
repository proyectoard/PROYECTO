from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import View 
from django.http import HttpResponse, JsonResponse
from datetime import datetime
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

class Reg(View):
	template_name = "tables-simple.html"

	def get(self, request):	
		
		if request.method == "GET":
			 
			conn = mysql.connector.connect(   host="srv1138.hstgr.io",
				user="u153713658_sensores",
				password="?4K92JUGsHd",
				database="u153713658_base_proyecto")

			# Consultar los datos
			query = "SELECT ID, TEMPERATURA, HUMEDAD, VELOCIDAD_VIENTO, DIRECCION_VIENTO, CANTIDAD_LLUVIA, FECHA, HORA FROM SENSORES ORDER BY ID DESC"
			
			cur = conn.cursor()
			cur.execute(query)           
			datos =  cur.fetchall()
			
			# Cerrar la conexión
			conn.close()
	
			return render(request, self.template_name, { "data2": datos})

	
