from fastapi import FastAPI
import requests
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:1234@localhost/IPlocator"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class RequestLog(Base):
    __tablename__ = "requests_log"

    id = Column(Integer, primary_key=True, index=True) # unique id
    ip_address = Column(String)                        # ip search
    city_found = Column(String)                        # city found
    created_at = Column(DateTime, default=datetime.now) # date
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
    finally:
        db.close()

    return {
        "status": "success",
        "saved_id": new_record.id,
        "ip": ip,
        "city": city_name
    }