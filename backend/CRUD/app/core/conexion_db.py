# from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from app.models.models import Base
from app.core.Settings import database_1, database_2

# settings = Settings()
# print(settings.__repr__())
print("URL:", database_1.SQLALCHEMY_DATABASE_URL)
print("URL:", database_2.SQLALCHEMY_DATABASE_URL)
engine1 = create_engine(str(database_1.SQLALCHEMY_DATABASE_URL))
engine2 = create_engine(str(database_1.SQLALCHEMY_DATABASE_URL))
SessionLocal1 = sessionmaker(bind=engine1)
SessionLocal2 = sessionmaker(bind=engine1)



