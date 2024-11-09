# Importa o FastAPI e uma função para gerenciar dependências.
from fastapi import FastAPI, Depends
# Importa a sessão do SQLAlchemy para interagir com o banco.
from sqlalchemy.orm import Session
# Importa o modelo de dados Contato.
from model import Contato, ContatoCreate
# Importa a conexão com o banco.
from database import engine, Base
# Importa a classe de sessão configurada.
from database import SessionLocal  

# Cria todas as tabelas definidas nos modelos no banco de dados.
#Base.metadata.create_all(bind=engine)

app = FastAPI()  # Cria uma instância da aplicação FastAPI.

def get_db():  # Define uma função para obter uma nova sessão de banco.
    db = SessionLocal()  # Cria nova sessão usando a classe SessionLocal.
    try:
        yield db  # Retorna a sessão ao chamar a função.
    finally:
        db.close()  # Fecha a sessão quando a operação é concluída.

# Define um endpoint para criação de contatos.
@app.post("/contatos/")
# Função que recebe o contato e a sessão como dependências.
def create_contato(contato: ContatoCreate, db: Session = Depends(get_db)):
      # Cria um novo objeto Contato com os dados recebidos.
      db_contato = Contato(nome=contato.nome, telefone=contato.telefone, email=contato.email)
      # Adiciona o novo contato à sessão do banco.
      db.add(db_contato)
      # Comita a transação para salvar as mudanças no banco.
      db.commit()
      # Atualiza o objeto Contato com os dados do banco, por exemplo, o ID gerado.
      db.refresh(db_contato)
      # Retorna o contato criado.
      return db_contato

# Define um endpoint para listar todos os contatos.
@app.get("/contatos/")
# Função que recebe parâmetros de limite e sessão.
def read_contatos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Faz a consulta ao banco, aplicando limites de páginas.
    contatos = db.query(Contato).offset(skip).limit(limit).all()
    # Retorna a lista de contatos.
    return contatos

# Define um endpoint que recebe o ID do contato.
@app.get("/contatos/{contato_id}")
# Função que recebe o ID e a sessão.
def read_contato(contato_id: int, db: Session = Depends(get_db)):
    # Retorna o contato correspondente ao ID, ou None se não encontrado.
    return db.query(Contato).filter(Contato.id == contato_id).first()

# Define um endpoint para atualizar um contato existente.
@app.put("/contatos/{contato_id}")
# Função que recebe o ID, o novo contato e a sessão.
def update_contato(contato_id: int, contato: ContatoCreate, db: Session = Depends(get_db)):
    # Busca o contato pelo ID.
    db_contato = db.query(Contato).filter(Contato.id == contato_id).first()
    # Verifica se o contato existe.
    if db_contato:
        # Atualiza o nome.
        db_contato.nome = contato.nome
        # Atualiza o telefone.
        db_contato.telefone = contato.telefone
        # Atualiza o e-mail.
        db_contato.email = contato.email
        # Salva as alterações no banco.
        db.commit()
        # Atualiza o objeto com os dados do banco.
        db.refresh(db_contato)
        # Retorna o contato atualizado.
        return db_contato
    # Retorna mensagem de erro se o contato não existe.
    return {"error": "Contato não encontrado"}

# Define um endpoint para deletar um contato especificado pelo ID.
@app.delete("/contatos/{contato_id}")
# Função que recebe o ID e a sessão.
def delete_contato(contato_id: int, db: Session = Depends(get_db)):
    # Busca o contato pelo ID.
    db_contato = db.query(Contato).filter(Contato.id == contato_id).first()  
    # Verifica se o contato existe.
    if db_contato:
        # Remove o contato da sessão.
        db.delete(db_contato)
        # Persiste as alterações no banco.
        db.commit()
        # Retorna mensagem de sucesso.
        return {"message": "Contato deletado"}
    # Retorna mensagem de erro se o contato não existe.
    return {"error": "Contato não encontrado"}