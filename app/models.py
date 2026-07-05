from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base() #base class for ORM models

class URL(Base):
    __tablename__ = "urls"

    code = Column(String(10), primary_key = True)
    long_url = Column(String, nullable=False)
    owner_id = Column(Integer, nullable = True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)

    