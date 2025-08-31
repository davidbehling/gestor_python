from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base

class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    current_value = Column(Float, nullable=False, default=0)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relacionamentos
    user = relationship("User", back_populates="bank_accounts")
    payments = relationship("Payment", back_populates="bank_account")

    def __repr__(self):
        return f"<BankAccount(id={self.id}, name='{self.name}', current_value={self.current_value}, user_id={self.user_id})>"
