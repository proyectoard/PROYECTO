# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from cgitb import html
from django.urls import path
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView
from alertas.views import Alertas
from registros.views import Reg

from registros import views

from com import views
from django.conf.urls.static import static 
from datos.views import ReportePersonalizadoExcel
from datos2.views import ReportePersonalizadoExcel2
from datos3.views import ReportePersonalizadoExcel3
from datos4.views import ReportePersonalizadoExcel4
from myapp_w.views import obtener_datos
from index.views import grafica
urlpatterns = [
    
    path('hola/', grafica.as_view(), name='obtener'),
    path('obtener_datos/', obtener_datos, name='obtener_datos'),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("alertas/", Alertas.as_view(), name="tables-data"),
    path("Registros/", Reg.as_view(), name="tables-simple"),
   
    path('fetch_sensor_values_ajax', views.fetch_sensor_values_ajax, name='fetch_sensor_values_ajax'),
    path('fetch_sensor_values_ajax2', views.fetch_sensor_values_ajax2, name='fetch_sensor_values_ajax2'),
    path('fetch_sensor_values_ajax3', views.fetch_sensor_values_ajax3, name='fetch_sensor_values_ajax3'),
    path('fetch_sensor_values_ajax4', views.fetch_sensor_values_ajax4, name='fetch_sensor_values_ajax4'),
    path('reporte/',ReportePersonalizadoExcel.as_view(), name = 'reporte'),
    path('reporte2/',ReportePersonalizadoExcel2.as_view(), name = 'reporte2'),
    path('reporte3/',ReportePersonalizadoExcel3.as_view(), name = 'reporte3'),
    path('reporte4/',ReportePersonalizadoExcel4.as_view(), name = 'reporte4'),
    
]
