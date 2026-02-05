from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import enum

Base = declarative_base()

class NoteStatus(enum.Enum):
    IN = "IN"
    OUT = "OUT"

class TransactionType(enum.Enum):
    IN = "IN"
    OUT = "OUT"

class Operator(Base):
    __tablename__ = "operators"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    login_id = Column(String, unique=True, nullable=False)
    
    transactions = relationship("Transaction", back_populates="operator")

class Note(Base):
    __tablename__ = "notes"
    
    serial_number = Column(String, primary_key=True)
    denomination = Column(Integer, nullable=False)
    status = Column(Enum(NoteStatus), default=NoteStatus.IN, nullable=False)
    last_seen = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    created_at = Column(DateTime, default=datetime.now)

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum(TransactionType), nullable=False)
    total_amount = Column(Integer, nullable=False)
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=True) # Nullable for MVP single user
    timestamp = Column(DateTime, default=datetime.now)
    
    operator = relationship("Operator", back_populates="transactions")
