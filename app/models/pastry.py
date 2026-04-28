from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from datetime import datetime, timezone
from app.extensions import Base

class Pastry(Base):
    __tablename__ = "pastries"

    id = Column(Integer, primary_key=True)
    text = Column(Text) # Tempat menyimpan deskripsi pastry
    request_id = Column(Integer, ForeignKey("requests.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))