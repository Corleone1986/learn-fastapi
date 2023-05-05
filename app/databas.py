from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# try:
#     conn = psycopg2.connect(host='localhost', database='fasapi' , user='postgres', password = 'mojtaba386386', cursor_factory=RealDictCursor)
#     curser = conn.cursor()
#     print('Database connection was succefull !! ')
# except Exception as error :
#     print("Connection to database failed")
#     print("Error : " , error)
