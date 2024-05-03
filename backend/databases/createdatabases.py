from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import create_database, database_exists
# from random import randint
import sys
sys.path.append(".")
from core import getJsonFile, getJsonFilesFromFolder, SQLALCHEMY_DATABASE_URL
from models.models import Base


def addToDB(db, data):
    try:
        existing_data = db.query(type(data)).filter_by(id=data.id).first()
        if existing_data:
            print("Data exits", existing_data)
        else:
            # Agregar el dato a la base de datos si no existe
            db.add(data)
            db.commit()
            db.refresh(data)
    except Exception as e:
        print(e)

def addTypeToDB(db, data):
    try:
        existing_data = db.query(type(data)).filter_by(_type=data._type).first()
        if existing_data:
            print("Data exits", existing_data)
        else:
            db.add(data)
            db.commit()
            db.refresh(data)
        return existing_data
    except Exception as e:
        print(e)

for json in getJsonFilesFromFolder():
    json = getJsonFile(json)
    DATABASE_URL = SQLALCHEMY_DATABASE_URL(json["POSTGRES_USER"], json["POSTGRES_PASSWORD"], json["POSTGRES_SERVER"], json["POSTGRES_PORT"], json["POSTGRES_DB"])
    engine = create_engine(str(DATABASE_URL))
    
    # Verificamos si la base de datos ya existe, y si no, la creamos
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Base de datos {json['POSTGRES_DB']} creada con éxito.")

    # Base.metadata.create_all(bind=engine)
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        # Ejecutar el comando SQL para agregar la extensión PostGIS
        session.execute(text('CREATE EXTENSION IF NOT EXISTS postgis'))
        session.commit()
        Base.metadata.create_all(bind=engine)
        print(f"Sesion iniciada in {json['POSTGRES_DB']}")
        # type_document = TypeDocument(_type=json["TYPE"])
        # type_d = addTypeToDB(session, type_document)
        # if type_d:
        #     type_document = type_d
    except Exception as e:
        print("Can't connect to database", e)
    try:
        print("Inserting data...")
        # for i in range(CANTIDAD_DATOS):
            # author = Author(name=NAMES[randint(0, len(NAMES) -1)] + " " + LASTNAMES[randint(0, len(LASTNAMES) -1)], birthday="1990-01-01")
            # addToDB(session, author)
            # document = Document(title=TITLES[randint(0, len(TITLES) - 1)], publication_date="2001", type_document_id=type_document._type)
            # addToDB(session, document)
            # documents_authors = DocumentsAuthors(document_id=document.id, author_id=author.id)
            # addToDB(session, documents_authors)
    finally:
        session.close()