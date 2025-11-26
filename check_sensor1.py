import RPi.GPIO as GPIO
import time
import threading
from datetime import datetime

# ======================
# CONFIGURACIÓN
# ======================
VIB_PIN = 17          # Pin GPIO del sensor de vibración
SEND_INTERVAL = 3600  # 1 hora en segundos

GPIO.setmode(GPIO.BCM)
GPIO.setup(VIB_PIN, GPIO.IN)

# Variables de estado
is_vibrating = False
start_time = None
last_measurements = []   # Lista con los tiempos de vibración detectados


# ======================
# FUNCIÓN PARA SUBIR DATOS
# ======================
def upload_data(data_list):
    """
    Aquí subes los datos donde quieras.
    Puedes usar MQTT, HTTP POST, Firebase, MongoDB, SQL, etc.
    """
    print("\n=== SUBIENDO DATOS ===")
    print(f"Hora local: {datetime.now()}")
    print(f"Datos enviados: {data_list}")
    print("======================\n")

    # EJEMPLO con archivo local:
    with open("vibration_logs.txt", "a") as f:
        f.write(f"{datetime.now()} - {data_list}\n")



# ======================
# HILO PARA ENVIAR EN CADA HORA EXACTA
# ======================
def hourly_sender():
    global last_measurements

    while True:
        now = datetime.now()

        # Calcular segundos hasta la próxima hora exacta
        next_hour = (now.replace(minute=0, second=0, microsecond=0) 
                     + timedelta(hours=1))
        wait_seconds = (next_hour - now).total_seconds()

        time.sleep(wait_seconds)  # Espera hasta la hora exacta

        # Si hay datos, enviarlos
        if last_measurements:
            upload_data(last_measurements)
            last_measurements = []  # limpiar después de enviar


# Inicia el hilo
threading.Thread(target=hourly_sender, daemon=True).start()


# ======================
# BUCLE PRINCIPAL
# ======================
print("Iniciando sistema de detección de vibración...")

try:
    while True:
        vibration = GPIO.input(VIB_PIN)

        # Si detecta vibración
        if vibration == GPIO.HIGH:
            if not is_vibrating:
                is_vibrating = True
                start_time = time.monotonic()
                print("▶ Vibración detectada, iniciando conteo...")

        # Si no hay vibración
        else:
            if is_vibrating:
                is_vibrating = False
                duration = time.monotonic() - start_time
                last_measurements.append(duration)
                print(f"■ Vibración detenida. Duración: {duration:.2f} s")

        time.sleep(0.05)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nSistema detenido.")
