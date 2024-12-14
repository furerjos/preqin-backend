from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Investor(Base):
    __tablename__ = "investors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(String)
    country = Column(String)
    date_added = Column(Date)
    last_updated = Column(Date)

    commitments = relationship("Commitment", back_populates="investor")


class Commitment(Base):
    __tablename__ = "commitments"

    id = Column(Integer, primary_key=True, index=True)
    asset_class = Column(String)
    amount = Column(Float)
    currency = Column(String)
    investor_id = Column(Integer, ForeignKey("investors.id"))

    investor = relationship("Investor", back_populates="commitments")
