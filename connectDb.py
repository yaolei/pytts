from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import dotenv
import os
dotenv.load_dotenv()

dbuser = os.getenv('DATABASE_USER')
dbpassword = os.getenv('DATABASE_PASSWORD')
dbhost = os.getenv('DATABASE_HOST')
dbname = os.getenv('DATABASE_NAME')

engine = create_engine(f'mysql+pymysql://{dbuser}:{dbpassword}@{dbhost}/{dbname}')
db_session = scoped_session(sessionmaker(autoflush=False,bind=engine))

Session = sessionmaker(bind=engine)
session = Session()

def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
