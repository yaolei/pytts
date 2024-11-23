from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(f'mysql+pymysql://{"root"}:{"asdf"}@{"127.0.0.1"}/{"prismadb"}')
db_session = scoped_session(sessionmaker(autoflush=False,bind=engine))

Session = sessionmaker(bind=engine)
session = Session()

def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
