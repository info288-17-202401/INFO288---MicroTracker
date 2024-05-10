from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# import sys
# sys.path.append(".")
from models.models import Microbus, Line, Brand
# from core.conexion_db import engine
from sqlalchemy import create_engine
from core.Settings import settings
try:
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URL))
    
    # DATABASE_URL = SQLALCHEMY_DATABASE_URL("postgres", "postgres", "postgres", 5432, "db_linea")
    # engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URL))
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    print(f"Sesion iniciada")
except Exception as e:
    print("Can't connect to database", e)


def queryID(data,state):
    if state == "id":
        return session.query(type(data)).filter_by(id=data.id).first()
    elif state == "patent":
        return session.query(type(data)).filter_by(patent=data.patent).first()
    elif state == "number":
        return session.query(type(data)).filter_by(number=data.number).first()

def addToDB(data, existing_data):
    try:
        if existing_data:
            print("Data exits", existing_data)
        else:
            # Agregar el dato a la base de datos si no existe
            session.add(data)
            session.commit()
            session.refresh(data)
    except Exception as e:
        print(e)

CANTIDAD_DATOS = 5
if __name__ == "__main__":
    try:
        print("Inserting data...")
        linea = Line(number=1, color="Rojo")
        linea_d = addToDB(linea, queryID(linea, "number"))
        if linea_d:
            linea = linea_d
        brand = Brand(name="Mercedes Benz")
        brand_d = addToDB(brand, queryID(brand, "id"))
        if brand_d:
            brand = brand_d
        for i in range(CANTIDAD_DATOS):
            micro = Microbus(patent="4k4k4k", line_id=linea.number, brand_id=brand.id)
            addToDB(micro, queryID(micro, "patent"))
        micro = session.query(Microbus).all()
        print(micro)
    finally:
        session.close()