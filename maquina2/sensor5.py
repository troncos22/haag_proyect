from pymongo import MongoClient
from datetime import datetime
import RPi.GPIO as GPIO
import time

# --- Conexión a MongoDB Atlas ---
URI = "mongodb+srv://jorgeignaciomorenofarias_db_user:George.8051@ingsoftware.yvxknqi.mongodb.net/?retryWrites=true&w=majority&appName=INGsoftware"
client = MongoClient(URI)
db = client["maqina2"]
coleccion = db["sensor5"]

# --- Configuración sensor ---
SENSOR_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

SENSOR_ID = "BOMBA_001"
UBICACION = {"type": "Point", "coordinates": [-70.65, -33.45]}

try:
    while True:
        vibracion = GPIO.input(SENSOR_PIN)
        lectura = {
            "sensor_id": SENSOR_ID,
            "tipo": "vibracion",
            "valor": int(vibracion),
            "unidad": "digital",
            "ubicacion": UBICACION,
            "timestamp": datetime.utcnow()
        }
        coleccion.insert_one(lectura)
        print("Dato guardado:", lectura)
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
