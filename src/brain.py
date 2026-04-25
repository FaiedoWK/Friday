from langchain_ollama import ChatOllama

def get_llm(model_type: str = "fast"):
    """
    Retorna a instância do LLM local (Ollama) de acordo com a complexidade da tarefa.
    """
    if model_type == "pro":
        # Motor Operacional (Tool-Calling Zero-Shot)
        return ChatOllama(
            model="llama3.1", # <-- Tag atualizada aqui
            temperature=0.2,
            base_url="http://localhost:11434"
        )
    
    # Modelo default (fast) para consultas simples e baixa latência
    return ChatOllama(
        model="llama3.2",
        temperature=0.1,
        base_url="http://localhost:11434"
    )

if __name__ == "__main__":
    # Teste rápido de conexão
    print("Testando conexão com Llama 3.2...")
    llm = get_llm("fast")
    resposta = llm.invoke("Responda apenas 'Conexão estabelecida com sucesso'.")
    print(f"Status: {resposta.content}")