# Importa a função necessária para criar a conexão com o banco.
from sqlalchemy import create_engine
# Permite criar classes que serão mapeadas para tabelas.
from sqlalchemy.ext.declarative import declarative_base
# Usado para criar sessões para interações com o banco de dados.
from sqlalchemy.orm import sessionmaker

# URL de conexão com o banco (substitua user, password e nome_do_banco).
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:12345678@localhost/agenda?charset=utf8mb4&collation=utf8mb4_general_ci"

# Cria a conexão com o banco de dados utilizando a URL fornecida.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Configura uma classe de sessão que pode ser usada para operações do banco.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria uma classe base para os modelos que serão definidos.
Base = declarative_base()