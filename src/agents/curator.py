import os
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from brain import get_llm
from tools.file_ops import read_file, write_file

def run_ingest(raw_filename: str, output_topic: str):
    """
    Motor de Ingestão do LLM Wiki.
    Lê um arquivo cru, aplica o schema e salva no formato Obsidian na pasta /wiki.
    """
    print(f"Iniciando ingestão do arquivo: {raw_filename}...")
    
    # 1. Lê o arquivo cru e o schema
    raw_content = read_file.invoke({"relative_path": f"raw/{raw_filename}"})
    schema_content = read_file.invoke({"relative_path": "schema.md"})
    
    if "Erro" in raw_content:
        print(f"Falha ao ler o arquivo cru: {raw_content}")
        return
        
    # 2. Prepara o nome do arquivo final no Obsidian
    hoje = datetime.now().strftime("%Y-%m-%d")
    clean_topic = output_topic.replace(" ", "-").lower()
    wiki_filename = f"wiki/{hoje}-{clean_topic}.md"
    
    # 3. Instancia o motor 8B (Operacional) e acopla a ferramenta de escrita
    llm = get_llm("pro")
    llm_with_tools = llm.bind_tools([write_file])
    
    # 4. Prompt Zero-Shot instruindo a curadoria
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é o 'The Curator', o agente de manutenção de conhecimento. "
                   "Sua função é ler o Documento Cru e reescrevê-lo estritamente seguindo "
                   "as regras do Schema fornecido. "
                   "Após gerar o conteúdo processado, utilize a ferramenta 'write_file' "
                   "para salvá-lo no destino. Não adicione conversação."),
        ("user", f"--- SCHEMA (Regras de Formatação) ---\n{schema_content}\n\n"
                 f"--- DOCUMENTO CRU ---\n{raw_content}\n\n"
                 f"Gere o arquivo final e salve em: {wiki_filename}")
    ])
    
    chain = prompt | llm_with_tools
    
    try:
        response = chain.invoke({})
        
        if response.tool_calls:
            for tool_call in response.tool_calls:
                if tool_call["name"] == "write_file":
                    args = tool_call["args"]
                    print(f"Processamento concluído. Salvando no Wiki...")
                    result = write_file.invoke(args)
                    print(result)
        else:
            print("Aviso: O modelo tentou responder em texto ao invés de usar a ferramenta.")
            print(response.content)
            
    except Exception as e:
        print(f"Erro na execução da Ingestão: {e}")

if __name__ == "__main__":
    # Teste de execução direta (necessário ter o arquivo teste na pasta raw)
    # run_ingest("anotacoes_half_loop.txt", "projeto half loop")
    pass