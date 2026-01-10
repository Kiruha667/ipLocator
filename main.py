from fastapi import FastAPI
import requests
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:1234@db/IPlocator"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class RequestLog(Base):
    __tablename__ = "requests_log"

    id = Column(Integer, primary_key=True, index=True) # unique id
    ip_address = Column(String)                        # ip search
    city_found = Column(String)                        # city found
    created_at = Column(DateTime, default=datetime.now) # date
Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/city")
def get_city_from_ip(ip: str):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        city_name = data.get("city", "Не определен")
    except:
        city_name = "Ошибка API"

    db = SessionLocal()
    try:
        new_record = RequestLog(
            ip_address=ip,
            city_found=city_name
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)

        count = db.query(RequestLog).filter(RequestLog.city_found == city_name).count()

        if count == 0:
            frequency_text = "Ни разу"
        elif count <= 5:
            frequency_text = "Мало"
        elif count <= 15:
            frequency_text = "Много"
        else:
            frequency_text = "Очень много"
    finally:
        db.close()

    return {
        "ip": ip,
        "city": city_name,
        "frequency": frequency_text,
        "count_debug": count,
        "saved_id": new_record.id
    }