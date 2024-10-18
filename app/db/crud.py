# crud.py
from sqlalchemy.orm import Session
from app.db.models import Subscription

# Create
def create_subscription(db: Session, telegram_id: int, city: str, lon: float, lat: float, current_aqi: int) -> Subscription:
    new_subscription = Subscription(telegram_id=telegram_id, city=city, lon=lon, lat=lat, current_aqi=current_aqi)
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return new_subscription

# Create or Update
def create_or_update_subscription(db: Session, telegram_id: int, city: str, lon: float, lat: float, current_aqi: int) -> Subscription:
    # Проверяем, существует ли уже запись с таким telegram_id
    existing_subscription = db.query(Subscription).filter(Subscription.telegram_id == telegram_id).first()
    
    if existing_subscription:
        # Обновляем существующую запись
        existing_subscription.city = city
        existing_subscription.lon = lon
        existing_subscription.lat = lat
        existing_subscription.current_aqi = current_aqi
        db.commit()
        db.refresh(existing_subscription)
        return existing_subscription
    
    # Если подписки нет, создаем новую
    new_subscription = Subscription(telegram_id=telegram_id, city=city, lon=lon, lat=lat, current_aqi=current_aqi)
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return new_subscription


# Read (Получить один по telegram_id)
def get_subscription(db: Session, telegram_id: int) -> Subscription:
    return db.query(Subscription).filter(Subscription.telegram_id == telegram_id).first()

# Read (Получить все)
def get_subscriptions(db: Session, skip: int = 0, limit: int = 100) -> list[Subscription]:
    return db.query(Subscription).offset(skip).limit(limit).all()

# Добавляем функцию для получения всех 
def get_all_subscriptions(db: Session) -> list[Subscription]:
    return db.query(Subscription).all()

# Update
def update_subscription(db: Session, telegram_id: int, city: str = None, lon: float = None, lat: float = None) -> Subscription:
    subscription = db.query(Subscription).filter(Subscription.telegram_id == telegram_id).first()
    if not subscription:
        return None
    if city is not None:
        subscription.city = city
    if lon is not None:
        subscription.lon = lon
    if lat is not None:
        subscription.lat = lat
    db.commit()
    db.refresh(subscription)
    return subscription

# Delete
def delete_subscription(db: Session, telegram_id: int) -> bool:
    subscription = db.query(Subscription).filter(Subscription.telegram_id == telegram_id).first()
    if not subscription:
        return False
    db.delete(subscription)
    db.commit()
    return True
