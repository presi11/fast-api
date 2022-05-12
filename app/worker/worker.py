from app.core.celery import celery_app
import time
@celery_app.task(acks_late=True)
def task(x):
    time.sleep(x)
    print(f"Task received: {x}")
    print ("corriendo")
    return x
