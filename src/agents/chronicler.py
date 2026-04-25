from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from brain import get_llm
from tools.file_ops import write_file

def run_chronicler(daily_summary: str):
    """
    Executa o 'The Chronicler' em regime Zero-Shot Tool Calling.
    Utiliza o modelo 8B para garantir a execução da ferramenta de escrita.
    """
    # 1. Instancia o motor operacional (Llama 3.1 8B-Instruct)
    llm = get_llm("pro")
    
    # 2. Acopla a ferramenta ao LLM
    llm_with_tools = llm.bind_tools([write_file])
    
    # 3. Define o nome do arquivo com a data de hoje
    hoje = datetime.now().strftime("%Y-%m-%d")
    filename = f"logs/{hoje}-daily-log.md"
    
    # 4. Prompt Zero-Shot (Sem histórico, direto ao ponto)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um agente de sistema automatizado chamado 'The Chronicler'. "
                   "Sua ÚNICA função é utilizar a ferramenta 'write_file' para salvar "
                   "o resumo fornecido pelo usuário em disco. Não forneça conversação, "
                   "apenas execute a ferramenta de escrita."),
        ("user", f"O resumo do expediente é:\n\n{daily_summary}\n\n"
                 f"Salve este conteúdo exatamente como está no arquivo: {filename}")
    ])
    
    # 5. Monta a chain
    chain = prompt | llm_with_tools
    
    print(f"Acionando The Chronicler para gerar {filename}...")
    
    try:
        # Invoca o modelo
        response = chain.invoke({})
        
        # 6. Processa a requisição de ferramenta do LLM
        if response.tool_calls:
            for tool_call in response.tool_calls:
                if tool_call["name"] == "write_file":
                    args = tool_call["args"]
                    print(f"Executando I/O: Salvando {args.get('relative_path')}...")
                    # Executa a função Python real
                    result = write_file.invoke(args)
                    print(result)
        else:
            print("Aviso: O modelo respondeu em texto em vez de chamar a ferramenta.")
            print("Resposta crua:", response.content)
            
    except Exception as e:
        print(f"Erro na execução do The Chronicler: {e}")

if __name__ == "__main__":
    # Teste rápido
    texto_teste = "# Progresso Diário\n- Reunião de alinhamento\n- Setup do Jarvis"
    run_chronicler(texto_teste)