from database import Base, engine, session
from models import User, Category, BankAccount, Payment, Transaction

# Criar as tabelas
Base.metadata.create_all(engine)

