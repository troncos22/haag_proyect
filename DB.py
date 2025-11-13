from pymongo import MongoClient
import pandas as pd
from sqlalchemy import create_engine

# --- CONEXIÓN A MONGODB ATLAS ---
URI = "mongodb+srv://jorgmoreno:George.8051@ingsoftware.yvxknqi.mongodb.net/?retryWrites=true&w=majority&appName=INGsoftware"

# Conexión al cliente Mongo
cliente = MongoClient(URI)
# Nombre de la base y colección
db = cliente["testing1"]        # ⚠️ reemplaza con el nombre exacto de tu base
coleccion = db["lecturas"] # ⚠️ reemplaza con el nombre de tu colección

# Leer los datos
datos = list(coleccion.find())

# Convertir a DataFrame
df = pd.DataFrame(datos)

# --- LIMPIAR CAMPOS ---
# Eliminar el campo "_id" si no lo necesitas
if "_id" in df.columns:
    df = df.drop(columns=["_id"])

# --- CONEXIÓN SQL (local) ---
engine = create_engine("sqlite:///basedatos_local.db")

# Exportar a SQL
df.to_sql("coleccion_convertida", con=engine, if_exists="replace", index=False)

print("✅ Datos migrados de MongoDB Atlas a base SQLite local correctamente.")
