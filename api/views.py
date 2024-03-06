from django.shortcuts import render
import smtplib
import os
from django.http import JsonResponse
import requests


def obtener_datos(request):
    api_url = "https://blynk.cloud/external/api/get?token=KZ1_-NaSq8rfh-dBPAXvnLnmzk63GFV8&v0&v1&v2&v3&v4"
    response = requests.get(api_url)
     
    if response.status_code == 200:
        data = response.json()
          
        return JsonResponse(data)        
    else:
        return JsonResponse({'error': 'Error en la solicitud'}, status=500)
    


