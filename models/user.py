from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    # Relacionamentos
    bank_accounts = relationship("BankAccount", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"
