from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# from core.Settings import settings
import sys

try:
    sys.path.append(".")
    from api.app.models.models import (
        MicrobusSensor,
    )
    from api.app.core.Settings import SQLALCHEMY_DATABASE_URL
except Exception as e:
    print("Error: Can't import")
    print(
        "Execute from the root folder of backend like this: \npython databases/create_db_linea-fromhost.py"
    )
    print("ERROR: ", e)
    sys.exit(1)
# from core.conexion_db import engine
from sqlalchemy import create_engine

DATABASE_URL = str(
    SQLALCHEMY_DATABASE_URL("postgres", "postgres", "localhost", 5432, "db_sensor")
)
# engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URL))
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print(f"Sesion iniciada")


def queryID(data, state):
    try:
        session = SessionLocal()
        if state == "id":
            return session.query(type(data)).filter_by(id=data.id).first()
        elif state == "patent":
            return session.query(type(data)).filter_by(patent=data.patent).first()
        elif state == "number":
            return session.query(type(data)).filter_by(number=data.number).first()
    finally:
        session.close()


def addToDB(data, existing_data):
    try:
        session = SessionLocal()
        if existing_data:
            print("Data exits", existing_data)
        else:
            # Agregar el dato a la base de datos si no existe
            session.add(data)
            session.commit()
            session.refresh(data)
    except Exception as e:
        print(e)
    finally:
        session.close()
        return data


CANTIDAD_DATOS = 5
if __name__ == "__main__":
    try:
        session = SessionLocal()
        print("Inserting data...")
        with open("databases/staticData/micros.csv", "r") as file:
            micros = file.readlines()
            for row in micros[1:]:
                patent, line_id, brand_id = row.split(",")
                micro = MicrobusSensor(patent=patent)
                addToDB(micro, queryID(micro, "patent"))
        micro = session.query(MicrobusSensor).all()
        print(micro)
    finally:
        session.close()
