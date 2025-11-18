from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

engine = create_engine("mysql+pymysql://root:yahia@192.168.1.5:3306/students1")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db():
    Base.metadata.create_all(bind=engine, checkfirst=True)