import os
import requests
import time
import threading
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.markdown import Markdown

# Importações clássicas mantidas para total estabilidade
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage

load_dotenv()

console = Console()

# =====================================================================
# 1. DEFINIÇÃO DAS FERRAMENTAS (TOOLS)
# =====================================================================

@tool
def ler_wiki(nome_arquivo: str) -> str:
    """
    Lê todo o conteúdo de um arquivo de texto (.md) específico dentro da Wiki.
    Use sempre que precisar consultar o que está escrito em uma nota ou arquivo de tarefas.
    """
    pasta_wiki = os.getenv("WIKI_PATH", "./v2_storage/wiki")
    caminho_completo = os.path.join(pasta_wiki, nome_arquivo)

    if not os.path.exists(caminho_completo):
        return f"Erro: O documento '{nome_arquivo}' não foi encontrado na Wiki."   
    with open(caminho_completo, "r", encoding="utf-8") as f:
        return f.read()


@tool
def escrever_wiki(nome_arquivo: str, conteudo: str) -> str:
    """
    Cria um novo arquivo ou substitui COMPLEMENTAMENTE o conteúdo de um arquivo existente na Wiki.
    Use apenas para criação inicial de notas ou quando quiser apagar o conteúdo antigo para reescrever do zero.
    """
    pasta_wiki = os.getenv("WIKI_PATH", "./v2_storage/wiki")
    os.makedirs(pasta_wiki, exist_ok=True)
    caminho_completo = os.path.join(pasta_wiki, nome_arquivo)

    with open(caminho_completo, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return f"Sucesso: O documento '{nome_arquivo}' foi criado/sobrescrito na Wiki."


@tool
def adicionar_na_wiki(nome_arquivo: str, conteudo: str) -> str:
    """
    Adiciona/Anexa texto estritamente ao final de um arquivo já existente na Wiki.
    NUNCA apaga o que já estava escrito. Use sempre que o usuário pedir para 'adicionar', 
    'anexar' ou 'inserir uma nova informação' em uma nota que já existe.
    """
    pasta_wiki = os.getenv("WIKI_PATH", "./v2_storage/wiki")
    os.makedirs(pasta_wiki, exist_ok=True)
    caminho_completo = os.path.join(pasta_wiki, nome_arquivo)

    # Verifica se o arquivo já existe para dar um espaçamento duplo elegante antes do novo bloco
    prefixo = "\n\n" if os.path.exists(caminho_completo) and os.path.getsize(caminho_completo) > 0 else ""

    with open(caminho_completo, "a", encoding="utf-8") as f:
        f.write(f"{prefixo}{conteudo}")
    return f"Sucesso: O novo conteúdo foi anexado fisicamente ao fim do arquivo '{nome_arquivo}'."


@tool
def listar_arquivos_wiki() -> str:
    """
    Lista absolutamente todos os arquivos e notas salvos dentro do diretório da Wiki.
    Use quando o usuário esquecer o nome de uma nota ou quiser ver o inventário de arquivos.
    """
    pasta_wiki = os.getenv("WIKI_PATH", "./v2_storage/wiki")
    if not os.path.exists(pasta_wiki):
        return "A pasta da Wiki ainda não existe no sistema."
        
    todos_arquivos = os.listdir(pasta_wiki)
    if not todos_arquivos:
        return "A pasta da Wiki está vazia."
        
    resposta_formatada = "Arquivos encontrados na Wiki:\n"
    for arquivo in todos_arquivos:
        resposta_formatada += f"- {arquivo}\n"
        
    return resposta_formatada


@tool
def gerenciar_tarefas(acao: str, conteudo: str = "") -> str:
    """
    Acessa ou atualiza a lista de tarefas gerais do usuário no arquivo central tasks.md.
    Ações disponíveis: 'visualizar', 'atualizar', 'adicionar'.
    """
    caminho_tarefas = os.getenv("TASKS_FILE", "./v2_storage/tasks.md")
    pasta_pai = os.path.dirname(caminho_tarefas)
    if pasta_pai:
        os.makedirs(pasta_pai, exist_ok=True)

    if acao == "visualizar":
        if not os.path.exists(caminho_tarefas) or os.path.getsize(caminho_tarefas) == 0:
            return "Nenhuma tarefa registrada ainda em tasks.md."
        with open(caminho_tarefas, "r", encoding="utf-8") as f:
            return f.read()
            
    elif acao == "atualizar":
        with open(caminho_tarefas, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return "Lista tasks.md atualizada com sucesso!"
        
    elif acao == "adicionar":
        linha_formatada = f"\n- [ ] {conteudo}" if not conteudo.startswith("-") else f"\n{conteudo}"
        with open(caminho_tarefas, "a", encoding="utf-8") as f:
            f.write(linha_formatada)
        return "Nova pendência anexada ao arquivo tasks.md."
        
    return "Erro: Ação inválida."


@tool
def web_scraping(url: str) -> str:
    """
    Faz web scraping em uma URL pública externa para coletar dados ou artigos de tecnologia.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resposta = requests.get(url, headers=headers, timeout=10)
        resposta.raise_for_status()
        
        soup = BeautifulSoup(resposta.text, 'html.parser')
        for elemento in soup(["script", "style", "nav", "footer", "header"]):
            elemento.decompose()
            
        texto_puro = soup.get_text(separator=' ')
        linhas = (linha.strip() for linha in texto_puro.splitlines())
        fragmentos = (frase.strip() for linha in linhas for frase in linha.split("  "))
        texto_final = '\n'.join(chunk for chunk in fragmentos if chunk)
        
        return texto_final[:4000]
    except Exception as e:
        return f"Falha ao realizar o scraping: {str(e)}"

# =====================================================================
# 2. INICIALIZAÇÃO E MONTAGEM DO AGENTE
# =====================================================================

# Injetamos o novo setup de ferramentas explícitas
lista_ferramentas = [ler_wiki, escrever_wiki, adicionar_na_wiki, listar_arquivos_wiki, gerenciar_tarefas, web_scraping]

llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "qwen2.5:7b"),
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    temperature=0.2  # Baixamos para 0.2 para torná-lo ainda mais estrito com as chamadas de funções
)

prompt_sistema = ChatPromptTemplate.from_messages([
    (
        "system",
        "Você é a Sexta-Feira, uma inteligência artificial assistente e orquestradora pessoal.\n"
        "Seu papel é gerenciar arquivos locais de documentação e tarefas para o Samuel, além de buscar informações na web.\n"
        "REGRAS DE OURO:\n"
        "1. Para criar uma nova nota ou arquivo, use 'escrever_wiki'.\n"
        "2. Para complementar, estender ou anexar dados em um arquivo existente, você DEVE invocar explicitamente a ferramenta 'adicionar_na_wiki'.\n"
        "3. Quando usar a ferramenta 'web_scraping', NUNCA devolva o texto cru ou o HTML para o usuário. Leia o conteúdo internamente, entenda o contexto geral da página e entregue um resumo inteligente, estruturado e focado em extrair os pontos principais.\n"
        "Responda sempre em português fluído e de forma elegante."
    ),
    MessagesPlaceholder(variable_name="historico_conversa"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agente = create_tool_calling_agent(llm, lista_ferramentas, prompt_sistema)

executor_sexta_feira = AgentExecutor(
    agent=agente, 
    tools=lista_ferramentas, 
    verbose=True,
    handle_parsing_errors=True
)

# =====================================================================
# 3. LOOP DE INTERAÇÃO (CLI) COM LOADER DINÂMICO E TYPING SUAVE
# =====================================================================

def iniciar_cli():
    console.print("[bold green]🤖 Sexta-Feira V2.4 - UI Minimalista[/bold green]\nDigite 'sair' para encerrar.")
    
    historico = []

    while True:
        try:
            entrada_usuario = console.input("\n[bold blue]Samuel[/bold blue] > ")
            
            if entrada_usuario.strip().lower() in ['sair', 'exit', 'quit']:
                console.print("[yellow]Desligando sistemas da Sexta-Feira. Até mais![/yellow]")
                break
                
            if not entrada_usuario.strip():
                continue

            # Loader
            stop_event = threading.Event()
            
            def animate_loading():
                # Spinner ASCII
                frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
                mensagens = [
                    "Analisando requisição...",
                    "Inspecionando diretórios...",
                    "Consultando memória de contexto...",
                    "Salamaleico...",
                    "Orquestrando ferramentas...",
                    "Sala...",
                    "Sintetizando resposta...",
                    "Labubu..."
                ]
                
                idx_frame = 0
                idx_msg = 0
                
                # transient=True faz o loader evaporar da tela quando termina!
                with Live(console=console, refresh_per_second=20, transient=True) as live_status:
                    while not stop_event.is_set():
                        frame_atual = frames[idx_frame % len(frames)]
                        msg_atual = mensagens[idx_msg % len(mensagens)]
                        
                        # Spinner cyan girando e texto opaco ao lado
                        live_status.update(f"[bold cyan]{frame_atual}[/bold cyan] [dim]{msg_atual}[/dim]")
                        
                        idx_frame += 1
                        if idx_frame % 30 == 0:  # Troca a mensagem a cada ~1.5 segundos
                            idx_msg += 1
                            
                        time.sleep(0.05) # Velocidade de rotação do spinner

            # Inicia a animação de carregamento em segundo plano
            loader_thread = threading.Thread(target=animate_loading)
            loader_thread.start()
            
            # Executa o LangChain (O programa fica "travado" aqui aguardando)
            stream_generator = executor_sexta_feira.stream({
                "input": entrada_usuario,
                "historico_conversa": historico
            })
            
            texto_stream = ""
            primeiro_chunk = True
            
            # Prepara o renderizador do texto da resposta, mas não o liga ainda
            live_resposta = Live(Markdown(""), console=console, refresh_per_second=60)
            
            for chunk in stream_generator:
                # O LangChain gerou o primeiro sinal! Hora de parar o loader.
                if primeiro_chunk:
                    stop_event.set()           # Pede pra thread do loader parar
                    loader_thread.join()       # Aguarda a tela limpar
                    console.print("\n[bold green]Sexta-Feira[/bold green] >")
                    live_resposta.start()      # Inicia o modo de digitação na tela principal
                    primeiro_chunk = False
                    
                if "output" in chunk:
                    for letra in chunk["output"]:
                        texto_stream += letra
                        live_resposta.update(Markdown(texto_stream))
                        time.sleep(0.01)      # Velocidade do efeito "typing"
                        
            # Encerramento limpo
            if not primeiro_chunk:
                live_resposta.stop()
            else:
                # Garantia caso a cadeia de pensamento falhe e não gere texto
                stop_event.set()
                loader_thread.join()
            
            # Salva histórico
            historico.append(HumanMessage(content=entrada_usuario))
            historico.append(AIMessage(content=texto_stream))
            
            if len(historico) > 10:
                historico = historico[-10:]

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupção detectada. Desligando...[/yellow]")
            break
        except Exception as erro:
            console.print(f"\n[bold red]Erro crítico:[/bold red] {erro}")

if __name__ == "__main__":
    iniciar_cli()