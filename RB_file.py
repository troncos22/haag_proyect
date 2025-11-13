from pymongo import MongoClient
from datetime import datetime, UTC

URI = "mongodb+srv://jorgeignaciomorenofarias_db_user:George.8051@ingsoftware.yvxknqi.mongodb.net/?retryWrites=true&w=majority&appName=INGsoftware"

client = MongoClient(URI)
db = client["Sensores"]
coleccion = db["Vibracion"]

lectura = {
    "sensor": "SW420",
    "ubicacion": "Santiago",
    "vibracion": 1,
    "timestamp": datetime.now(UTC)
}

coleccion.insert_one(lectura)
print("Lectura subida con éxito")
