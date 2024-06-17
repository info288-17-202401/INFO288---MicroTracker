# from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from app.models.models import Base
from app.core.Settings import databases_settings

sessions = []
for database in databases_settings:
    print("URL:", database.SQLALCHEMY_DATABASE_URL)
    engine = create_engine(str(database.SQLALCHEMY_DATABASE_URL))
    sessions.append(sessionmaker(bind=engine))

def getCorrectSession(microbus_state):
    pos = 0
    while(not databases_settings[pos].LinesContainsLine(microbus_state)):
        # logger.debug(f"Line {microbus_state.line} not in database {pos}")
        pos = pos + 1
    return sessions[pos]