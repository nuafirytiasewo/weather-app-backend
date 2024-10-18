from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Subscription(Base):
    __tablename__ = "subscriptions"
    telegram_id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False)
    city = Column(String, nullable=False)
    lon = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    current_aqi = Column(Integer, nullable=True)
