# from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
# from app.models.models import Base
from app.core.Settings import settings

# settings = Settings()
# print(settings.__repr__())
print("URL:", settings.SQLALCHEMY_DATABASE_URL)
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URL))


