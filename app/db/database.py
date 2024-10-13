from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from app.db.models import Base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(
    DATABASE_URL,
    echo=True,  # Установите в False в продакшене
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
    )

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        print("getting db")
        yield db
        db.commit()
    except:
        print("rolling back")
        db.rollback()
        raise
    finally:
        print("closing db")
        db.close()
