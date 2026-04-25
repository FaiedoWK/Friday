from langchain_core.prompts import ChatPromptTemplate
from brain import get_llm
from tools.file_ops import read_file, write_file

def run_editor(instruction: str, file_path: str):
    """
    Executa o 'The Editor' em regime Zero-Shot Tool Calling.
    Utiliza o Llama 3.1 8B para ler, alterar e sobrescrever o arquivo.
    """
    print(f"Analisando arquivo alvo: {file_path}...")
    
    # 1. Leitura do arquivo em Python (Determinístico)
    current_content = read_file.invoke({"relative_path": file_path})
    
    if "Erro" in current_content:
        print(current_content)
        return

    # 2. Instancia o motor operacional
    llm = get_llm("pro")
    llm_with_tools = llm.bind_tools([write_file])
    
    # 3. Prompt Zero-Shot estrito
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é o 'The Editor', um agente focado em edição técnica de arquivos. "
                   "Sua ÚNICA função é aplicar a alteração solicitada pelo usuário no texto/código base "
                   "e utilizar a ferramenta 'write_file' para salvar a versão INTEGRAL modificada. "
                   "Não explique a alteração, apenas execute a ferramenta de escrita."),
        ("user", f"Arquivo: {file_path}\n"
                 f"--- Conteúdo Atual ---\n{current_content}\n\n"
                 f"--- Instrução de Edição ---\n{instruction}\n\n"
                 "Gere a nova versão completa e chame a ferramenta de escrita.")
    ])
    
    chain = prompt | llm_with_tools
    
    print(f"Acionando The Editor para processar modificações em {file_path}...")
    
    try:
        response = chain.invoke({})
        
        if response.tool_calls:
            for tool_call in response.tool_calls:
                if tool_call["name"] == "write_file":
                    args = tool_call["args"]
                    print(f"Executando I/O: Salvando atualizações no arquivo...")
                    result = write_file.invoke(args)
                    print(result)
        else:
            print("Aviso: Falha de Tool-Calling. O modelo tentou responder em texto.")
            print("Resposta crua:", response.content)
            
    except Exception as e:
        print(f"Erro Crítico na execução do The Editor: {e}")

if __name__ == "__main__":
    # O arquivo teste precisa existir na Safe Zone. 
    # Ex: crie um 'teste.txt' com "Olá Mundo" antes de rodar.
    # run_editor("Mude 'Olá Mundo' para 'Olá Jarvis'", "teste.txt")
    pass