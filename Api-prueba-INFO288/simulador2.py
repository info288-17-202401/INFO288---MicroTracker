import csv
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from os import getenv
# Definir la URL de la API
load_dotenv()
try:
    LOADBALANCER_HOST = str(getenv("LOADBALANCER_HOST"))
    LOADBALANCER_PORT = int(getenv("LOADBALANCER_PORT"))
except Exception as e:
    print("Error al cargar las variables de entorno")
    LOADBALANCER_HOST = "localhost"
    LOADBALANCER_PORT = 4050
    
api_url = f"http://{LOADBALANCER_HOST}:{LOADBALANCER_PORT}/microbusstate"  # Reemplace con la URL real de su API


# Definir la función que procesará un archivo CSV y enviará peticiones
def procesar_csv(archivo_csv, patent, line):
    with open(archivo_csv, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Saltar la cabecera si existe

        for row in reader:
            x = row[1]
            y = row[2]
            data = {
                "patent": patent,
                "date": "2023-11-21",
                "currently": True,
                "coordinates": {"x": x, "y": y},
                "velocity": 50,
                "passengers": 25,
                "line": line,
            }

            # Enviar la petición POST a la API
            response = requests.post(api_url, json=data)
            print(f"Petición para patente {patent} enviada.")
            print(f"RESPONSE:{response.json()}")
            # Verificar el estado de la respuesta
            if response.status_code == 201:
                print(f"Petición para patente {patent} enviada con éxito.")
            else:
                print(
                    f"Error al enviar petición para patente {patent}: {response.status_code}"
                )

            # Esperar 1 segundo antes de la siguiente petición
            time.sleep(1)


# Lista de archivos CSV y patentes correspondientes
archivos_csv = [
    ("rutas_micro1.csv", "A8G3DE", 3),
    ("rutas_micro2.csv", "3AN9BM", 1),
]

# Usar ThreadPoolExecutor para procesar cada archivo CSV simultáneamente
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [
        executor.submit(procesar_csv, archivo_csv, patent, line)
        for archivo_csv, patent, line in archivos_csv
    ]

    # Esperar a que todas las tareas se completen
    for future in as_completed(futures):
        try:
            future.result()
        except Exception as exc:
            print(f"Generated an exception: {exc}")
