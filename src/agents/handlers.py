"""
Handler Agents - Concrete implementations for each intent
Replaces hallucination with real tool execution
"""
import os
from langchain_core.messages import SystemMessage, HumanMessage
from src.brain import get_pro_llm, get_fast_llm
from src.tools.file_ops import read_file, write_file, list_files, append_file
from src.agents.curator import ingest_raw_file, list_pending_ingestion


def handle_rag_search(user_query: str) -> str:
    """
    RAG_SEARCH intent: Query the wiki using semantic search.
    Uses Pro Model (8B) with context from actual wiki files.
    """
    try:
        from src.rag import get_retriever
        
        # Get relevant documents from wiki
        retriever = get_retriever(k=3)
        relevant_docs = retriever.invoke(user_query)
        
        if not relevant_docs:
            return "Nenhum documento relevante encontrado no wiki."
        
        # Build context from actual retrieval
        context = "\n---\n".join([
            f"📄 {doc.metadata.get('source', 'Desconhecido')}:\n{doc.page_content[:500]}"
            for doc in relevant_docs
        ])
        
        # Use Pro Model with retrieved context
        pro_llm = get_pro_llm(temperature=0.0)
        system_msg = SystemMessage(content=(
            "Você é a Sexta-Feira, assistente de IA. "
            "Use APENAS os documentos fornecidos como contexto para responder. "
            "Se a informação não estiver nos documentos, diga explicitamente que não encontrou."
        ))
        
        query_msg = HumanMessage(content=f"Baseado nesses documentos:\n{context}\n\nResponda: {user_query}")
        
        response = pro_llm.invoke([system_msg, query_msg])
        return response.content
    
    except ImportError:
        return "⚠️ Sistema RAG ainda não configurado. Certifique-se que ChromaDB está instalado."
    except Exception as e:
        return f"❌ Erro na busca RAG: {e}"


def handle_tool_edit(user_instruction: str) -> str:
    """
    TOOL_EDIT intent: File operations (create, read, edit, delete).
    Parses user instruction and executes actual file operations.
    """
    try:
        pro_llm = get_pro_llm(temperature=0.0)
        
        system_msg = SystemMessage(content=(
            "Você é um assistente que executa operações de arquivo.\n"
            "Analise o pedido do usuário e identifique exatamente o que fazer:\n"
            "- 'read' para ler um arquivo\n"
            "- 'write' para criar/sobrescrever um arquivo\n"
            "- 'append' para adicionar conteúdo\n"
            "- 'list' para listar diretório (use para listar os arquivos)\n"
            "- 'delete' para deletar arquivo\n\n"
            "Responda em JSON com formato: {\"action\": \"...\", \"path\": \"...\", \"content\": \"...\"}"
        ))
        
        user_msg = HumanMessage(content=user_instruction)
        
        # Get pro model to parse the instruction
        response = pro_llm.invoke([system_msg, user_msg])
        
        # Try to parse as JSON
        import json
        try:
            if not response or not response.content:
                raise json.JSONDecodeError("Empty response from LLM", "", 0)
            command = json.loads(response.content)
        except (json.JSONDecodeError, TypeError):
            # Fallback: If LLM fails to produce JSON, infer from the user's original text.
            content_lower = user_instruction.lower()
            if "ler" in content_lower or "read" in content_lower:
                command = {"action": "read", "path": extract_path(user_instruction)}
            elif "listar" in content_lower or "list" in content_lower or "quais arquivos" in content_lower:
                command = {"action": "list", "path": extract_path(user_instruction) or ""}
            else:
                return f"❌ Não consegui interpretar o comando de arquivo. Por favor, tente ser mais explícito, como 'crie um arquivo chamado...', 'leia o arquivo...', ou 'liste os arquivos'."
        
        # Execute the command safely handling None/null values
        action = str(command.get("action") or "").lower()
        path = str(command.get("path") or "")
        content = str(command.get("content") or "")
        
        # Secondary fallback: If JSON was valid but action is empty/null
        if not action:
            content_lower = user_instruction.lower()
            if "ler" in content_lower or "read" in content_lower:
                action, path = "read", extract_path(user_instruction)
            elif "listar" in content_lower or "list" in content_lower or "quais" in content_lower:
                action, path = "list", (extract_path(user_instruction) or "")
            else:
                return f"❌ Não consegui identificar a ação específica. Especifique 'leia', 'crie' ou 'liste'."
        
        if action == "read":
            return read_file(path)
        elif action == "write":
            return write_file(path, content)
        elif action == "append":
            return append_file(path, content)
        elif action == "list":
            return list_files(path)
        elif action == "delete":
            from src.tools.file_ops import delete_file
            return delete_file(path)
        else:
            return f"❌ Ação desconhecida: {action}"
    
    except Exception as e:
        return f"❌ Erro ao executar comando de arquivo: {e}"


def handle_curation(user_instruction: str) -> str:
    """
    CURATION intent: Document ingestion and formatting.
    Moves files from /raw to /wiki with proper Obsidian formatting.
    """
    try:
        # List pending files first
        pending = list_pending_ingestion()
        
        if "Diretório vazio" in pending:
            return "✅ Nenhum documento pendente. Vault está atualizado."
        
        pro_llm = get_pro_llm(temperature=0.0)
        
        system_msg = SystemMessage(content=(
            "Você é um curador de documentos. Analise a solicitação e:\n"
            "1. Identifique qual arquivo em /raw deve ser processado\n"
            "2. Defina tags apropriadas (máx 3)\n"
            "3. Sugira nome final do arquivo\n\n"
            "Responda em JSON: {\"file\": \"...\", \"tags\": [...], \"output\": \"...\"}"
        ))
        
        user_msg = HumanMessage(content=f"Arquivos pendentes:\n{pending}\n\nSolicitação: {user_instruction}")
        response = pro_llm.invoke([system_msg, user_msg])
        
        # Parse response
        import json
        try:
            instruction = json.loads(response.content)
            file = instruction.get("file", "")
            tags = instruction.get("tags", ["inbox"])
            output = instruction.get("output", file)
            
            if file:
                # Remove raw/ prefix if already present
                file = file.replace("raw/", "").replace("raw\\", "")
                output = output.replace("wiki/", "").replace("wiki\\", "")
                return ingest_raw_file(file, wiki_filename=output, tags=tags)
            else:
                return "❌ Não consegui identificar o arquivo"
        except json.JSONDecodeError:
            return f"❌ Erro ao processar resposta: {response.content[:200]}"
    
    except Exception as e:
        return f"❌ Erro ao curar documento: {e}"


def extract_path(text: str) -> str:
    """Helper to extract file path from user text."""
    import re
    # Try to find quoted paths or file names
    patterns = [
        r"'([^']+)'",
        r'"([^"]+)"',
        r"(?:arquivo|file|path)s?\s+(?:is|are|é)?\s*([^\s,]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return ""
