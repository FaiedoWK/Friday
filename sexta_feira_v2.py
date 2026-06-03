import os

from rich.console import Console
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.markdown import Markdown

# Langchain
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage

load_dotenv()

console = Console()

# TOOLS

@tool
def gerenciar_wiki(acao: str, nome_arquivo: str, conteudo: str = "") -> str:
    """
    Gerencia arquivos de documentação/wiki.
    Ações disponíveis: 'ler', 'criar', 'editar'.
    Exemplos de nome_arquivo: 'python_async.md', 'arquitetura.md'.
    Se a ação for 'editar', o 'conteúdo' fornecio substituirá ou complementará o arquivo.
    """
    pasta_wiki = os.getenv("WIKI_PATH", "./v2_storage/wiki")
    os.makedirs(pasta_wiki, exist_ok=True)
    caminho_completo = os.path.join(pasta_wiki, nome_arquivo)

    if acao == "ler":
        if not os.path.exists(caminho_completo):
            return f"Erro: O documento '{nome_arquivo}' não foi encontrado na Wiki."   
        with open(caminho_completo, "r", encoding="utf-8") as f:
                return f.read()
        
    elif acao in ["criar", "editar"]:
        with open(caminho_completo, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return f"Sucesso: o documento '{nome_arquivo}' foi atualizado/salvo na Wiki."

    return "Erro: Ação inválida. Escolha entre 'ler', 'criar' ou 'editar'."

@tool
def gerenciar_tarefas(acao: str, conteudo: str = "") -> str:
    """
    Acessa ou atualiza a lista de tarefas e lembretes gerais do usuário.
    Ações disponíveis: 'visualizar', 'atualizar'.
    Use 'visualizar' para ver o status atual das pendências.
    Use 'atualizar' para reescrever a lista adicionando, removendo ou marcando tarefas como concluídas.
    """
    caminho_tarefas = os.getenv("TASKS_FILE", "./v2_storage/tasks.md")
    pasta_pai = os.path.dirname(caminho_tarefas)
    if pasta_pai:
        os.makedirs(pasta_pai, exist_ok=True)

    if acao == "visualizar":
        if not os.path.exists(caminho_tarefas):
            return "Nenhuma tarefa ou lembrete registrado ainda. O arquivo está vazio."
        with open(caminho_tarefas, "r", encoding="utf-8") as f:
            return f.read()
            
    elif acao == "atualizar":
        with open(caminho_tarefas, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return "Lista de tarefas e lembretes atualizada com sucesso!"
        
    return "Erro: Ação inválida. Escolha 'visualizar' ou 'atualizar'."


@tool
def web_scraping(url: str) -> str:
    """
    Faz web scraping em uma URL pública externa para coletar dados, artigos ou documentações atualizadas.
    Extrai apenas o conteúdo de texto limpo para processamento.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        resposta = requests.get(url, headers=headers, timeout=10)
        resposta.raise_for_status()
        
        soup = BeautifulSoup(resposta.text, 'html.parser')
        
        # Limpa elementos visuais e scripts redundantes
        for elemento in soup(["script", "style", "nav", "footer", "header"]):
            elemento.decompose()
            
        texto_puro = soup.get_text(separator=' ')
        linhas = (linha.strip() for linha in texto_puro.splitlines())
        fragmentos = (frase.strip() for linha in linhas for frase in linha.split("  "))
        texto_final = '\n'.join(chunk for chunk in fragmentos if chunk)
        
        # Limita o retorno para evitar estouro de contexto/RAM em páginas gigantescas
        return texto_final[:4000]
    except Exception as e:
        return f"Falha ao realizar o scraping da URL: {str(e)}"

# --- 2. INICIALIZAÇÃO E MONTAGEM DO AGENTE ---

# Agrupa a lista de ferramentas que o Qwen poderá invocar nativamente
lista_ferramentas = [gerenciar_wiki, gerenciar_tarefas, web_scraping]

# Conexão com o Ollama configurado localmente
llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "qwen2.5:14b"),
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    temperature=0.3
)

# Estruturação do Prompt de Sistema com suporte a histórico (Memória)
prompt_sistema = ChatPromptTemplate.from_messages([
    (
        "system",
        "Você é a Sexta-Feira, uma inteligência artificial assistente e orquestradora pessoal.\n"
        "Seu papel é auxiliar o Samuel no gerenciamento de suas tarefas, documentações locais (Wiki) e consultas na web.\n"
        "Comporte-se de maneira prestativa, objetiva e inteligente. Use as ferramentas fornecidas sempre que necessário "
        "para ler, salvar ou buscar dados. Responda sempre em português fluído."
    ),
    # Espaço reservado onde o histórico de conversas será injetado dinamicamente
    MessagesPlaceholder(variable_name="historico_conversa"),
    ("human", "{input}"),
    # Espaço obrigatório para o LangChain processar o raciocínio das ferramentas internas (Scratchpad)
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Criação do agente utilizando o padrão nativo de Tool Calling do Qwen
agente = create_tool_calling_agent(llm, lista_ferramentas, prompt_sistema)
executor_sexta_feira = AgentExecutor(agent=agente, tools=lista_ferramentas, verbose=True)

# --- 3. LOOP DE INTERAÇÃO (CLI) COM GESTÃO DE MEMÓRIA ---

def iniciar_cli():
    console.print(Panel.fit("[bold green]🤖 Sexta-Feira V2 - Inicializada com Sucesso![/bold green]\nModo: Cérebro Único (Qwen 14B)\nDigite 'sair' para encerrar.", title="Sistema"))
    
    # Memória local em lista (Short-Term Memory de até 10 mensagens)
    historico = []

    while True:
        try:
            entrada_usuario = console.input("\n[bold blue]Samuel[/bold blue] > ")
            
            if entrada_usuario.strip().lower() in ['sair', 'exit', 'quit']:
                console.print("[yellow]Desligando sistemas da Sexta-Feira. Até mais![/yellow]")
                break
                
            if not entrada_usuario.strip():
                continue

            # Executa a chamada passando a entrada e a janela de histórico atual
            console.print("[dim]🧠 Pensando e coordenando ferramentas...[/dim]")
            resultado = executor_sexta_feira.invoke({
                "input": entrada_usuario,
                "historico_conversa": historico
            })
            
            resposta_final = resultado["output"]
            
            # Exibe a resposta formatada
            console.print(Panel(Markdown(resposta_final), title="[bold green]Sexta-Feira[/bold green]", border_style="green"))
            
            # Atualização da memória: Adiciona a interação atual
            historico.append(HumanMessage(content=entrada_usuario))
            historico.append(AIMessage(content=resposta_final))
            
            # Mantém estritamente as últimas 10 mensagens (5 turnos de conversa) para poupar memória RAM
            if len(historico) > 10:
                historico = historico[-10:]

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupção detectada. Desligando...[/yellow]")
            break
        except Exception as erro:
            console.print(f"[bold red]Ocorreu um erro no loop principal: {erro}[/bold red]")

if __name__ == "__main__":
    iniciar_cli()