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
# Wiki path points to Obsidian Vault
WIKI_PATH = os.getenv("OBSIDIAN_VAULT_PATH")
DB_PATH = os.path.join(SAFE_ZONE, "data", "db")

def init_vector_db():
    """
    Inicializa o banco vetorial lendo os arquivos do Vault (wiki).
    """
    print("Iniciando indexação do Wiki...")
    
    # Garante que as pastas existem na Safe Zone
    Path(WIKI_PATH).mkdir(parents=True, exist_ok=True)
    Path(DB_PATH).mkdir(parents=True, exist_ok=True)
    
    # Carrega .txt e .md do wiki
    loaders = {
        ".txt": DirectoryLoader(WIKI_PATH, glob="**/*.txt", loader_cls=TextLoader),
        ".md": DirectoryLoader(WIKI_PATH, glob="**/*.md", loader_cls=TextLoader)
    }
    
    docs = []
    for ext, loader in loaders.items():
        try:
            loaded = loader.load()
            if loaded:
                docs.extend(loaded)
                print(f"  ✓ Carregados {len(loaded)} arquivos {ext}")
        except Exception as e:
            print(f"  ⚠ Erro ao carregar arquivos {ext}: {e}")

    if not docs:
        print("⚠ Wiki vazio. Adicione documentos para usar o RAG.")
        return None

    # Quebra os textos em chunks menores para melhorar a busca semântica
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Usa o modelo de embeddings do Ollama
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")

    # Cria/Atualiza o banco local
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings, 
        persist_directory=DB_PATH
    )
    
    print(f"✅ Indexação concluída: {len(splits)} chunks armazenados em {DB_PATH}")
    return vectorstore

def query_wiki(query: str, k: int = 5) -> str:
    """
    Realiza busca semântica no wiki indexado e retorna contexto relevante.
    Usa RAG (Retrieval-Augmented Generation) para enriquecer consultas.
    """
    try:
        # Carrega embeddings
        embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")
        
        # Carrega vectorstore persistido
        vectorstore = Chroma(
            persist_directory=DB_PATH,
            embedding_function=embeddings
        )
        
        # Busca semântica
        docs = vectorstore.similarity_search(query, k=k)
        
        if not docs:
            return "❌ Nenhum resultado encontrado no wiki."
        
        # Formata contexto para passar ao LLM
        context = "\n---\n".join([f"📄 {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}" for doc in docs])
        
        return context
        
    except Exception as e:
        return f"❌ Erro na busca semântica: {str(e)}"

if __name__ == "__main__":
    # Teste de execução direta
    print("🧠 RAG Wiki Module Test")
    print("=" * 60)
    
    # Indexação
    init_vector_db()
    
    # Teste de Query
    print("\n🔍 Teste de Busca Semântica:")
    test_queries = [
        "reunião sprint",
        "tarefas de desenvolvimento",
        "riscos do projeto"
    ]
    
    for q in test_queries:
        print(f"\n📝 Query: '{q}'")
        result = query_wiki(q, k=3)
        print(f"Resultado:\n{result[:500]}...")  # Primeiros 500 chars