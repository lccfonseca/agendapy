# agendapy
Minicurso sobre como construir uma API REST em Python

### Slide 1: Título
- *Título:* Construção de uma API Simples em Python com FastAPI
- *Subtítulo:* Integração com Banco de Dados MySQL
- *Luís Carlos Costa Fonseca*
- *09/11/2024*
---
### Slide 2: O que é FastAPI?
- *Definição:* FastAPI é um framework moderno e rápido para construir APIs com Python 3.7+.
- *Principais Características:*
  - Alta performance (baseado em Starlette e Pydantic)
  - Suporte a anotações de tipo
  - Geração automática de documentação
---
### Slide 3: Pré-requisitos
- *Python:* Versão 3.7 ou superior
- *Instalação do FastAPI, Uvicorn e SQLAlchemy:*
  bash
  pip install fastapi uvicorn sqlalchemy mysql-connector-python
  
- *Banco de Dados:* MySQL deve estar instalado e em execução.
---
### Slide 4: Estrutura do Projeto
- *Estrutura Inicial:*
  
  /meu_projeto/
      ├── main.py
      ├── database.py
      ├── model.py
  
- *Descrição dos Arquivos:*
  - main.py: Lógica principal da API
  - database.py: Configuração do banco de dados
  - model.py: Definição do modelo de dados
---
### Slide 5: Configurando o Banco de Dados
- *Código para database.py:*
  python
  from sqlalchemy import create_engine      # Importa a função necessária para criar a conexão com o banco.
  from sqlalchemy.ext.declarative import declarative_base  # Permite criar classes que serão mapeadas para tabelas.
  from sqlalchemy.orm import sessionmaker    # Usado para criar sessões para interações com o banco de dados.
  SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://user:password@localhost/nome_do_banco"  
  # URL de conexão com o banco (substitua user, password e nome_do_banco).
  engine = create_engine(SQLALCHEMY_DATABASE_URL)  # Cria a conexão com o banco de dados utilizando a URL fornecida.
  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  
  # Configura uma classe de sessão que pode ser usada para operações do banco.
  Base = declarative_base()  # Cria uma classe base para os modelos que serão definidos.
  
---
### Slide 6: Definindo o Modelo de Dados
- *Código para model.py:*
  python
  from sqlalchemy import Column, Integer, String  # Importa os tipos de dados para as colunas.
  from database import Base  # Importa a classe base que conecta modelos ao banco.
  class Contato(Base):  # Define uma classe 'Contato' que herda de Base.
      __tablename__ = "contatos"  # Define o nome da tabela no banco de dados.
      id = Column(Integer, primary_key=True, index=True)  # Define a coluna 'id' como chave primária.
      nome = Column(String(100))  # Define a coluna 'nome' com tipo string e tamanho máximo de 100.
      telefone = Column(String(15))  # Define a coluna 'telefone' com tipo string e tamanho máximo de 15.
      email = Column(String(100))  # Define a coluna 'email' com tipo string e tamanho máximo de 100.
  
- *Descrição:* Essa classe representa a tabela de contatos no banco de dados.
---
### Slide 7: Criando a Tabela
- *Código adicional no main.py:*
  python
  from sqlalchemy.orm import Session  # Importa a sessão do SQLAlchemy para interagir com o banco.
  from models import Contato  # Importa o modelo de dados Contato.
  from database import engine  # Importa a conexão com o banco.
  Base.metadata.create_all(bind=engine)  # Cria todas as tabelas definidas nos modelos no banco de dados.
  
- *Descrição:* Este código cria a tabela contatos no banco de dados.
---
### Slide 8: Configurando a API
- *Código Inicial em main.py:*
  python
  from fastapi import FastAPI, Depends  # Importa o FastAPI e uma função para gerenciar dependências.
  from sqlalchemy.orm import Session  # Importa a sessão do SQLAlchemy.
  from database import SessionLocal  # Importa a classe de sessão configurada.
  import models  # Importa o módulo de modelos.
  app = FastAPI()  # Cria uma instância da aplicação FastAPI.
  def get_db():  # Define uma função para obter uma nova sessão de banco.
      db = SessionLocal()  # Cria nova sessão usando a classe SessionLocal.
      try:
          yield db  # Retorna a sessão ao chamar a função.
      finally:
          db.close()  # Fecha a sessão quando a operação é concluída.
  
---
### Slide 9: Operação CRUD - Criar
- *Endpoint de Criação:*
  python
  from pydantic import BaseModel  # Importa o modelo base do Pydantic para validação de dados.
  class ContatoCreate(BaseModel):  # Define o modelo que representa o corpo da requisição de criação.
      nome: str  # Campo para o nome.
      telefone: str  # Campo para o telefone.
      email: str  # Campo para o e-mail.
  @app.post("/contatos/")  # Define um endpoint para criação de contatos.
  def create_contato(contato: ContatoCreate, db: Session = Depends(get_db)):  # Função que recebe o contato e a sessão como dependências.
      db_contato = models.Contato(nome=contato.nome, telefone=contato.telefone, email=contato.email)  # Cria um novo objeto Contato com os dados recebidos.
      db.add(db_contato)  # Adiciona o novo contato à sessão do banco.
      db.commit()  # Comita a transação para salvar as mudanças no banco.
      db.refresh(db_contato)  # Atualiza o objeto Contato com os dados do banco, por exemplo, o ID gerado.
      return db_contato  # Retorna o contato criado.
  
---
### Slide 10: Operação CRUD - Ler
- *Endpoint para Ler Todos os Contatos:*
  python
  @app.get("/contatos/")  # Define um endpoint para listar todos os contatos.
  def read_contatos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):  # Função que recebe parâmetros de limite e sessão.
      contatos = db.query(models.Contato).offset(skip).limit(limit).all()  # Faz a consulta ao banco, aplicando limites de páginas.
      return contatos  # Retorna a lista de contatos.
  
  
- *Endpoint para Ler um Contato Específico:*
  python
  @app.get("/contatos/{contato_id}")  # Define um endpoint que recebe o ID do contato.
  def read_contato(contato_id: int, db: Session = Depends(get_db)):  # Função que recebe o ID e a sessão.
      return db.query(models.Contato).filter(models.Contato.id == contato_id).first()  # Retorna o contato correspondente ao ID, ou None se não encontrado.
  
---
### Slide 11: Operação CRUD - Atualizar
- *Endpoint de Atualização:*
  python
  @app.put("/contatos/{contato_id}")  # Define um endpoint para atualizar um contato existente.
  def update_contato(contato_id: int, contato: ContatoCreate, db: Session = Depends(get_db)):  # Função que recebe o ID, o novo contato e a sessão.
      db_contato = db.query(models.Contato).filter(models.Contato.id == contato_id).first()  # Busca o contato pelo ID.
      if db_contato:  # Verifica se o contato existe.
          db_contato.nome = contato.nome  # Atualiza o nome.
          db_contato.telefone = contato.telefone  # Atualiza o telefone.
          db_contato.email = contato.email  # Atualiza o e-mail.
          db.commit()  # Salva as alterações no banco.
          db.refresh(db_contato)  # Atualiza o objeto com os dados do banco.
          return db_contato  # Retorna o contato atualizado.
      return {"error": "Contato não encontrado"}  # Retorna mensagem de erro se o contato não existe.
  
---
### Slide 12: Operação CRUD - Deletar
- *Endpoint de Deleção:*
  python
  @app.delete("/contatos/{contato_id}")  # Define um endpoint para deletar um contato especificado pelo ID.
  def delete_contato(contato_id: int, db: Session = Depends(get_db)):  # Função que recebe o ID e a sessão.
      db_contato = db.query(models.Contato).filter(models.Contato.id == contato_id).first()  # Busca o contato pelo ID.
      if db_contato:  # Verifica se o contato existe.
          db.delete(db_contato)  # Remove o contato da sessão.
          db.commit()  # Salva as alterações no banco.
          return {"message": "Contato deletado"}  # Retorna mensagem de sucesso.
      return {"error": "Contato não encontrado"}  # Retorna mensagem de erro se o contato não existe.
  
---
### Slide 13: Executando a API
- *Comando para Executar:*
  bash
  uvicorn main:app --reload  # Executa a aplicação com recarregamento automático em desenvolvimento.
  
- *Acessando a API:* Abra um navegador e vá para http://127.0.0.1:8000/.
---
### Slide 14: Documentação Automática
- *Descrição:* FastAPI gera documentação interativa automaticamente.
- *URLs:*
  - Swagger UI: http://127.0.0.1:8000/docs  # Interface gráfica para testar os endpoints.
  - ReDoc: http://127.0.0.1:8000/redoc  # Documentação dos endpoints.
---
### Slide 15: Conclusão
- *Resumo:* Aprendemos a construir uma API simples com FastAPI, integrada a um banco de dados MySQL, implementando as operações CRUD na tabela de contatos.
- *Próximos Passos:* Explore validações, autenticação e testes.
---
### Slide 16: Perguntas e Respostas
- *Dúvidas? Perguntas?*