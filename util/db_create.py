# Importa a sessão do SQLAlchemy para interagir com o banco.
from sqlalchemy.orm import Session
# Importa o modelo de dados Contato. 
from model import Contato
# Importa a conexão com o banco.
from database import engine, Base
# Cria todas as tabelas definidas nos modelos no banco de dados.
Base.metadata.create_all(bind=engine)