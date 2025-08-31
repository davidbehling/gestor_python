from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuração do banco de dados
DATABASE_URL = "sqlite:///dados.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Base para os modelos
Base = declarative_base()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuração do banco de dados
DATABASE_URL = "sqlite:///dados.db"
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Base para os modelos
Base = declarative_base()
