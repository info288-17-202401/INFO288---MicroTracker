from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import requests

# from core.Settings import settings
import sys

try:
    sys.path.append(".")
    from api.app.models.models import (
        MicrobusSensor,
    )
    # from api.app.core.Settings import SQLALCHEMY_DATABASE_URL
except Exception as e:
    print("Error: Can't import")
    print(
        "Execute from the root folder of backend like this: \npython databases/create_db_linea-fromhost.py"
    )
    print("ERROR: ", e)
    sys.exit(1)

CANTIDAD_DATOS = 5
API_URL = "http://localhost:4050/microbus/"
if __name__ == "__main__":
    try:
        print("Inserting data...")
        with open("databases/staticData/micros.csv", "r") as file:
            micros = file.readlines()
            # print(micros)
            for row in micros[1:]:
                patent, line_id, brand_id = row.split(",")
                print("ROW: ", patent, line_id)
                print(f"Request to: {API_URL}")
                request_ = requests.post(
                    API_URL,
                    json={"patent": patent, "line": line_id},
                )
                print(request_)
    except Exception as e:
        print(e)
        # sys.exit(1)
