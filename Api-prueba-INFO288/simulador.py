import csv
import requests
import time

# Definir la URL de la API
api_url = "http://localhost:4000/microbusstate"  # Reemplace con la URL real de su API

# Abrir el archivo CSV
with open("rutas_micros.csv", "r") as csvfile:
    reader = csv.reader(csvfile)

    # Iterar sobre cada línea del CSV
    for row in reader:
        # Extraer datos de la fila actual
        patent = "3AN9BM"
        x = row[1]
        y = row[2]

        # Crear el diccionario JSON con los datos
        # data = {"patent": patent, "coordinates": {"x": x, "y": y}}
        data = {
            "patent": patent,
            "date": "2023-11-21",
            "currently": True,
            "coordinates": {"x": x, "y": y},
            "velocity": 50,
            "passengers": 25,
            # "line": 1,
        }

        # Enviar la petición POST a la API
        response = requests.post(api_url, json=data)

        # Verificar el estado de la respuesta
        if response.status_code == 201:
            print(f"Petición para patente {patent} enviada con éxito.")
        else:
            print(
                f"Error al enviar petición para patente {patent}: {response.status_code}"
            )

        # Esperar 1 segundo antes de la siguiente petición
        time.sleep(1)
