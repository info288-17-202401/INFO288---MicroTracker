# from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from models.models import Base
from core.Settings import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URL))
# Base.metadata.create_all(bind=engine)
