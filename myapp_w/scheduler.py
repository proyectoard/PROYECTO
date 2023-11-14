import schedule
import time


def job():
    print("Ejecutando la tarea cada 5 minutos...")
    

schedule.every(0.5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)