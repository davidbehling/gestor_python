from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum as PyEnum

class TypeRole(PyEnum):
    DINHEIRO = "Dinheiro"
    CREDITO = "Crédito"
    DEBITO = "Débito"
    CREDIARIO = "Crediário"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    due_day = Column(Integer, nullable=True)
    closed_day = Column(Integer, nullable=True)
    bank_account_id = Column(Integer, ForeignKey("bank_accounts.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relacionamentos
    bank_account = relationship("BankAccount", back_populates="payments")
    user = relationship("User", back_populates="payments")
    transactions = relationship("Transaction", foreign_keys="[Transaction.payment_id]", back_populates="payment")
    paid_transactions = relationship("Transaction", foreign_keys="[Transaction.paid_payment_id]", back_populates="paid_payment")

    def __repr__(self):
        return f"<Payment(id={self.id}, type='{self.type}', name='{self.name}', due_day={self.due_day}, closed_day={self.closed_day}, bank_account_id={self.bank_account_id}, user_id={self.user_id})>"
