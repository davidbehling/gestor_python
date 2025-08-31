from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    date_at = Column(Date, nullable=False)
    due_date = Column(Date, nullable=True)
    payment_date = Column(Date, nullable=True)
    installments = Column(Integer, default=1)
    total_installments = Column(Integer, default=1)
    paid = Column(Boolean, nullable=False)
    expense = Column(Boolean, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False)
    paid_payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relacionamentos
    category = relationship("Category", back_populates="transactions")
    payment = relationship("Payment", foreign_keys=[payment_id], back_populates="transactions")
    paid_payment = relationship("Payment", foreign_keys=[paid_payment_id], back_populates="transactions")
    user = relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"""
            <Transaction(
                id={self.id}, 
                description='{self.description}', 
                value={self.value},
                date_at={self.date_at},
                due_date={self.due_date},
                payment_date={self.payment_date},
                installments={self.installments},
                total_installments={self.total_installments},
                paid={self.paid},
                expense={self.expense},
                category_id={self.category_id},
                payment_id={self.payment_id},
                paid_payment_id={self.paid_payment_id},
                user_id={self.user_id}
            )>
        """
