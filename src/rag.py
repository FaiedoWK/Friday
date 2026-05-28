import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from src.brain import get_embeddings

WIKI_PATH = os.getenv("OBSIDIAN_VAULT_PATH", "./friday_domain/wiki")
DB_PATH = "./data/db"

def ingest_wiki():
    """
    Lê os arquivos Markdown do diretório wiki, divide em chunks semânticos
    e os ingere no banco de dados vetorial (ChromaDB).
    """
    # Garante que as pastas existam
    os.makedirs(WIKI_PATH, exist_ok=True)
    os.makedirs(DB_PATH, exist_ok=True)

    loader = DirectoryLoader(WIKI_PATH, glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()

    if not documents:
        print("Nenhum documento Markdown (.md) encontrado no Wiki.")
        return None

    # Divide os documentos em pedaços (chunks) com sobreposição para não perder contexto
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(documents)

    embeddings = get_embeddings()

    # Cria/Atualiza o banco ChromaDB localmente
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    return vector_store

def get_retriever(k: int = 3):
    """
    Retorna o retriever configurado para buscar os 'k' chunks mais relevantes.
    """
    embeddings = get_embeddings()
    vector_store = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    return vector_store.as_retriever(search_kwargs={"k": k})