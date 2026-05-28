from langchain_core.messages import SystemMessage, HumanMessage
from src.brain import get_fast_llm


def classify_intent(user_input: str) -> str:
    """
    Classifica a intenção do usuário para rotear para o agente correto.
    Usa temperatura 0.0 para garantir previsibilidade e evitar alucinações.
    """
    llm = get_fast_llm(temperature=0.0)
    
    system_prompt = SystemMessage(content=(
        "Você é o classificador de intenções da Sexta-Feira (Friday). "
        "Sua única função é ler a entrada do usuário e responder com EXATAMENTE UMA das seguintes tags, e nada mais:\n\n"
        "[CHAT] - Para bate-papo geral, perguntas simples, saudações ou qualquer coisa que não exija busca de arquivos.\n"
        "[RAG_SEARCH] - Para perguntas que exigem busca no Obsidian, base de conhecimento pessoal, ou ler documentos do usuário.\n"
        "[TOOL_EDIT] - Para comandos de criação, edição ou manipulação de arquivos locais e tarefas.\n"
        "[CURATION] - Para organizar, formatar ou processar notas cruas para o formato final.\n\n"
        "NÃO justifique sua resposta. Responda APENAS com a tag. Exemplo de saída: [CHAT]"
    ))
    
    messages = [system_prompt, HumanMessage(content=user_input)]
    
    try:
        response = llm.invoke(messages)
        content = response.content.strip().upper()
        
        for intent in ["[CHAT]", "[RAG_SEARCH]", "[TOOL_EDIT]", "[CURATION]"]:
            if intent in content:
                return intent
    except Exception:
        pass
        
    return "[CHAT]"  # Fallback seguro


def handle_intent(intent: str, user_input: str) -> tuple[str, str]:
    """
    Routes to appropriate handler based on intent.
    Returns: (handler_type, response_content)
    
    This REPLACES hallucination with real tool calling.
    """
    if intent == "[RAG_SEARCH]":
        from src.agents.handlers import handle_rag_search
        response = handle_rag_search(user_input)
        return ("rag", response)
    
    elif intent == "[TOOL_EDIT]":
        from src.agents.handlers import handle_tool_edit
        response = handle_tool_edit(user_input)
        return ("tool", response)
    
    elif intent == "[CURATION]":
        from src.agents.handlers import handle_curation
        response = handle_curation(user_input)
        return ("curation", response)
    
    else:  # [CHAT] or fallback
        # For chat, return the intent type so main can call fast_llm
        return ("chat", "")
