import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama, OllamaEmbeddings

# Carrega as variáveis de ambiente do .env
load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
FAST_MODEL_NAME = os.getenv("FAST_MODEL", "llama3.2")
PRO_MODEL_NAME = os.getenv("PRO_MODEL", "llama3.1")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

def get_fast_llm(temperature: float = 0.7) -> ChatOllama:
    """
    Retorna a instância do Fast Model (Llama 3.2 - 3B).
    Usado para Chat Rápido e Roteamento de Intenções.
    """
    return ChatOllama(
        model=FAST_MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
        temperature=temperature,
    )

def get_pro_llm(temperature: float = 0.0) -> ChatOllama:
    """
    Retorna a instância do Pro Model (Llama 3.1 - 8B).
    Usado para RAG, Tool Calling e raciocínio complexo.
    Temperatura 0.0 para evitar alucinações.
    """
    return ChatOllama(
        model=PRO_MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
        temperature=temperature,
    )

def get_embeddings() -> OllamaEmbeddings:
    """Retorna o modelo de Embeddings para busca semântica."""
    return OllamaEmbeddings(
        model=EMBEDDING_MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
    )