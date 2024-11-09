# Importa os tipos de dados para as colunas.
from sqlalchemy import Column, Integer, String
# Importa a classe base que conecta modelos ao banco.
from database import Base
# Importa o modelo base do Pydantic para validação de dados.
from pydantic import BaseModel

# Define uma classe 'Contato' que herda de Base.
class Contato(Base):
    # Define o nome da tabela no banco de dados.
    __tablename__ = "contatos"
    # Define a coluna 'id' como chave primária.
    id = Column(Integer, primary_key=True, index=True)
    # Define a coluna 'nome' com tipo string e tamanho máximo de 80.
    nome = Column(String(80))
    # Define a coluna 'telefone' com tipo string e tamanho máximo de 15.
    telefone = Column(String(15))
    # Define a coluna 'email' com tipo string e tamanho máximo de 100.
    email = Column(String(100))

# Define o modelo que representa o corpo da requisição de criação.
class ContatoDTO(BaseModel):
    # Campo para o nome.
    nome: str
    # Campo para o telefone.
    telefone: str
    # Campo para o e-mail.
    email: str