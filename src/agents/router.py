import json
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from brain import get_llm
from rag import query_wiki, init_vector_db

def classify_intent(user_input: str, chat_history: list) -> str:
    """
    Passo 1: Identifica a intenção em milissegundos.
    """
    llm = get_llm("fast")
    system_prompt = "Responda APENAS com a intenção: CHAT, RAG_QUERY, TOOL_EDIT, ou TOOL_REWIND."
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"input": user_input, "history": chat_history})
    return response.content.strip().upper()

def stream_reply(user_input: str, chat_history: list):
    """
    Passo 2: Gera a resposta sarcástica com streaming.
    """
    llm = get_llm("fast")
    system_prompt = """Você é 'Sexta-Feira', assistente virtual do Samuel.
Sua personalidade: Extremamente formal, as vezes sarcástico (estilo Jarvis), elegante e pontual.
Você ocasionalmente usa gírias como 'poggers', 'paia', 'Tá potente'.
Mantenha a memória da sessão ativa."""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}")
    ])
    
    return (prompt | llm).stream({"input": user_input, "history": chat_history})

def rag_query(user_input: str, chat_history: list):
    """
    Passo 2 (RAG): Busca contexto no wiki e gera resposta enriquecida.
    """
    # Recupera contexto relevante do wiki
    context = query_wiki(user_input, k=5)
    
    if "❌" in context or "Erro" in context:
        # Se a busca falhar, volta ao chat normal
        return stream_reply(user_input, chat_history)
    
    # LLM com contexto RAG
    llm = get_llm("pro")  # Usa modelo pro para melhor compreensão
    system_prompt = """Você é 'Sexta-Feira', assistente virtual do Samuel.
Sua personalidade: Extremamente formal, as vezes sarcástico (estilo Jarvis), elegante e pontual.

Responda com base no contexto do Wiki fornecido abaixo. Se o contexto não abordar a pergunta, diga que não encontrou informações.

--- CONTEXTO DO WIKI ---
{context}
---"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}")
    ])
    
    chain = prompt | llm
    return chain.stream({
        "context": context,
        "input": user_input, 
        "history": chat_history
    })