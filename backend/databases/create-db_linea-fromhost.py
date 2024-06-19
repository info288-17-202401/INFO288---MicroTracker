from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# from core.Settings import settings
import sys

try:
    sys.path.append(".")
    from api.app.models.models import (
        Line,
        Brand,
        Model,
        Sector,
        Microbus,
        Route,
        BusStop,
        RouteBusStop,
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
from sqlalchemy import create_engine, func

DATABASE_URL = str(
    SQLALCHEMY_DATABASE_URL("postgres", "postgres", "localhost", 5433, "db_linea")
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
        with open("databases/staticData/line.csv", "r") as file:
            lines = file.readlines()
            for row in lines[1:]:
                number, color = row.split(",")
                linea = Line(number=number, color=color)
                linea_d = addToDB(linea, queryID(linea, "number"))
                if linea_d:
                    linea = linea_d

        # linea = Line(number=1, color="Rojo")
        # linea_d = addToDB(linea, queryID(linea, "number"))
        # if linea_d:
        #     linea = linea_d
        with open("databases/staticData/brand.csv", "r") as file:
            brands = file.readlines()
            for row in brands[1:]:
                brand = Brand(name=row)
                brand_d = addToDB(brand, queryID(brand, "id"))
                if brand_d:
                    brand = brand_d
        # brand = Brand(name="Mercedes Benz")
        # brand_d = addToDB(brand, queryID(brand, "id"))
        # if brand_d:
        #     brand = brand_d
        with open("databases/staticData/micros.csv", "r") as file:
            micros = file.readlines()
            for row in micros[1:]:
                patent, line_id, brand_id = row.split(",")
                micro = Microbus(patent=patent, line_id=line_id, brand_id=brand_id)
                addToDB(micro, queryID(micro, "patent"))
        # for i in range(CANTIDAD_DATOS):
        #     micro = Microbus(patent=f"{i}k", line_id=linea.number, brand_id=brand.id)
        #     addToDB(micro, queryID(micro, "patent"))

        ##Añadir las rutas
        routes = {}
        with open("databases/staticData/data.csv", "r") as file:
            data = file.readlines()

            for row in data[1:]:
                line, x, y, isBusStop, direction = row.split(",")
                if line not in routes:
                    routes[line] = {}
                if direction not in routes[line]:
                    routes[line][direction] = []
                routes[line][direction].append((x, y))
        for line in routes.keys():
            for direction in routes[line].keys():
                multipoint_wkt = "MULTIPOINT({})".format(
                    ", ".join(
                        [
                            "({} {})".format(point[0], point[1])
                            for point in routes[line][direction]
                        ]
                    )
                )
                new_route = Route(route=multipoint_wkt, line_id=line)
                addToDB(new_route, queryID(new_route, "id"))

        ##Añadir los paraderos
        with open("databases/staticData/data.csv", "r") as file:
            data = file.readlines()
            for row in data[1:]:
                line, x, y, isBusStop, direction = row.split(",")
                if isBusStop == "1":
                    point_wkt = "POINT({} {})".format(x, y)
                    new_busStop = BusStop(coordinates=point_wkt)
                    session.add(new_busStop)
                    session.commit()

                    # Using ST_DWithin to find the route that has the bus stop point within a very small distance
                    foundedRoute = (
                        session.query(Route)
                        .filter(
                            func.ST_DWithin(
                                Route.route, func.ST_GeomFromText(point_wkt, 4326), 0
                            )
                        )
                        .first()
                    )

                    if foundedRoute:
                        new_relation = RouteBusStop(
                            id_busstop_fk=new_busStop.id, id_ruta_fk=foundedRoute.id
                        )
                        session.add(new_relation)
                        session.commit()

        ##Añadir las relaciones entre ruta y paradero

        micro = session.query(Microbus).all()
        print(micro)
    finally:
        session.close()
