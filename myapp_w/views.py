from django.shortcuts import render

# Create your views hereasd.sa

from django.http import JsonResponse
import requests

def obtener_datos(request):
    api_url = "https://blynk.cloud/external/api/get?token=2mAMfT5kz3MKfie1m0IiBLqm9mvzFkuV&v0&v1&v2&v3&v4"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Error en la solicitud'}, status=500)