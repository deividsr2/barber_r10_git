import pymysql
from sqlalchemy import create_engine, text
import os
import streamlit as st

# Configuração do banco de dados
DB_HOST = os.getenv("DB_HOST", "145.223.31.244")
DB_PORT = int(os.getenv("DB_PORT", 10))
DB_USER = os.getenv("DB_USER", "mysql")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Tricolor633#")
DB_NAME = os.getenv("DB_NAME", "banco")

# Conexão SQLAlchemy com pooling
engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_pre_ping=True, pool_size=10, max_overflow=20, pool_recycle=3600
)

# Função de conexão direta com PyMySQL
def create_connection():
    try:
        return pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    except Exception as e:
        st.error(f"Erro ao conectar ao banco: {e}")
        return None


# --------------------------------------------------
# Funções para a tabela r10_servicos
# --------------------------------------------------

def inserir_servico(servico, valor):
    """
    Insere um novo serviço na tabela `r10_servicos`.
    """
    query = text("INSERT INTO r10_servicos (servico, valor) VALUES (:servico, :valor)")
    with engine.connect() as connection:
        connection.execute(query, {"servico": servico, "valor": valor})
        connection.commit()

def buscar_servicos():
    """
    Retorna todos os serviços cadastrados na tabela `r10_servicos`.
    """
    query = text("SELECT * FROM r10_servicos")
    with engine.connect() as connection:
        result = connection.execute(query)
        return [dict(row) for row in result]

def atualizar_servico(id, servico, valor):
    """
    Atualiza um serviço específico na tabela `r10_servicos`.
    """
    query = text("UPDATE r10_servicos SET servico = :servico, valor = :valor WHERE id = :id")
    with engine.connect() as connection:
        connection.execute(query, {"id": id, "servico": servico, "valor": valor})
        connection.commit()


# --------------------------------------------------
# Funções para a tabela r10_atividades
# --------------------------------------------------

def inserir_atividade(id_barbeiro, barbeiro, data_hora, servico, valor, observacao):
    """
    Insere uma nova atividade na tabela `r10_atividades`.
    """
    query = text("""
    INSERT INTO r10_atividades (id_barbeiro, barbeiro, data_hora, servico, valor, observacao) 
    VALUES (:id_barbeiro, :barbeiro, :data_hora, :servico, :valor, :observacao)
    """)
    with engine.connect() as connection:
        connection.execute(query, {
            "id_barbeiro": id_barbeiro,
            "barbeiro": barbeiro,
            "data_hora": data_hora,
            "servico": servico,
            "valor": valor,
            "observacao": observacao
        })
        connection.commit()

def buscar_atividades():
    """Busca todas as atividades registradas no banco."""
    conn = create_connection()
    if conn:
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:  # Usa DictCursor para retornar dicionários
                cursor.execute("SELECT * FROM r10_atividades ORDER BY data_hora DESC")
                result = cursor.fetchall()
                return result  # Retorna a lista de dicionários diretamente
        except Exception as e:
            st.error(f"Erro ao buscar atividades: {e}")
            return []
        finally:
            conn.close()
    return []


def atualizar_atividade(id, dados):
    """
    Atualiza uma atividade específica na tabela `r10_atividades`.
    """
    updates = ", ".join([f"{key} = :{key}" for key in dados.keys()])
    query = text(f"UPDATE r10_atividades SET {updates} WHERE id = :id")
    dados["id"] = id
    with engine.connect() as connection:
        connection.execute(query, dados)
        connection.commit()


# --------------------------------------------------
# Funções para a tabela r10_barbeiros
# --------------------------------------------------

def inserir_barbeiro(barbeiro):
    """
    Insere um novo barbeiro na tabela `r10_barbeiros`.
    """
    query = text("INSERT INTO r10_barbeiros (barbeiro) VALUES (:barbeiro)")
    with engine.connect() as connection:
        connection.execute(query, {"barbeiro": barbeiro})
        connection.commit()


def buscar_barbeiros():
    conn = create_connection()
    if conn:
        try:
            # Consulta para buscar barbeiros
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM r10_barbeiros")
                result = cursor.fetchall()  # Isso retornará uma lista de dicionários
                return result  # Retorna a lista de barbeiros
        except Exception as e:
            st.error(f"Erro ao buscar barbeiros: {e}")
            return []
        finally:
            conn.close()
    return []

def buscar_servicos():
    conn = create_connection()
    if conn:
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM r10_servicos")
                result = cursor.fetchall()
                return result
        except Exception as e:
            st.error(f"Erro ao buscar serviços: {e}")
            return []
        finally:
            conn.close()
    return []


def atualizar_barbeiro(id, barbeiro):
    """
    Atualiza o nome de um barbeiro na tabela `r10_barbeiros`.
    """
    query = text("UPDATE r10_barbeiros SET barbeiro = :barbeiro WHERE id = :id")
    with engine.connect() as connection:
        connection.execute(query, {"id": id, "barbeiro": barbeiro})
        connection.commit()

def buscar_senha_barbeiro(nome_barbeiro):
    """
    Busca a senha do barbeiro no banco de dados.
    """
    query = text("SELECT sa FROM r10_barbeiros WHERE barbeiro = :barbeiro")
    with engine.connect() as connection:
        result = connection.execute(query, {"barbeiro": nome_barbeiro}).fetchone()
        return result[0] if result else None  # Retorna a senha ou None

