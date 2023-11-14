# myapp/tasks.py

from celery import shared_task

@shared_task
def my_task():
    # Coloca aquí la lógica de tu tarea que quieres ejecutar cada 5 minutos
    print("Ejecutando la tarea cada 5 minutos.")
    # Puedes realizar cualquier tarea que necesites aquí