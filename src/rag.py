import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from tools.validator import validate_path

load_dotenv()

SAFE_ZONE = os.getenv("SAFE_ZONE_PATH")
VAULT_PATH = os.path.join(SAFE_ZONE, "data", "vault")
DB_PATH = os.path.join(SAFE_ZONE, "data", "db")

def init_vector_db():
    """
    Inicializa o banco vetorial lendo os arquivos do Vault.
    """
    print("Iniciando indexação do Vault...")
    
    # Garante que as pastas existem na Safe Zone
    Path(VAULT_PATH).mkdir(parents=True, exist_ok=True)
    Path(DB_PATH).mkdir(parents=True, exist_ok=True)
    
    # Carrega .txt e .md
    loaders = {
        ".txt": DirectoryLoader(VAULT_PATH, glob="**/*.txt", loader_cls=TextLoader),
        ".md": DirectoryLoader(VAULT_PATH, glob="**/*.md", loader_cls=TextLoader)
    }
    
    docs = []
    for ext, loader in loaders.items():
        try:
            docs.extend(loader.load())
        except Exception as e:
            print(f"Erro ao carregar arquivos {ext}: {e}")

    if not docs:
        print("Vault vazio. Adicione documentos para usar o RAG.")
        return None

    # Quebra os textos em chunks menores para melhorar a busca semântica
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Usa o modelo de embeddings do Ollama (Recomendo baixar o 'nomic-embed-text')
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")

    # Cria/Atualiza o banco local
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings, 
        persist_directory=DB_PATH
    )
    
    print(f"Indexação concluída: {len(splits)} chunks armazenados.")
    return vectorstore

if __name__ == "__main__":
    # Teste de execução direta
    init_vector_db()