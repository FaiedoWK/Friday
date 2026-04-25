import time
import click
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from agents.router import classify_intent, stream_reply
from agents.chronicler import run_chronicler
from langchain_core.messages import HumanMessage, AIMessage

console = Console()

def chat_loop():
    # Estética Inicial
    console.print("[bold grey70]Sexta-Feira System Online[/bold grey70] [dim]| V2.0[/dim]")
    chat_history = []
    
    while True:
        try:
            # Input com cores OpenCode
            user_input = console.input("\n[bold grey70]Samuel[/bold grey70] [sky_blue1]>[/sky_blue1] ")
            
            if user_input.lower() in ['exit', 'quit', 'sair']:
                console.print("[bold sky_blue1]Sexta-Feira:[/bold sky_blue1] [grey84]Sistemas encerrados, senhor.[/grey84]")
                break
            
            # Passo 1: Roteamento Silencioso
            with console.status("[dim grey70]Sincronizando...[/dim grey70]", spinner="dots"):
                intent = classify_intent(user_input, chat_history)

            # Passo 2: Resposta com Streaming Suavizado (Máquina de Escrever)
            reply_full = ""
            console.print("[bold sky_blue1]Sexta-Feira:[/bold sky_blue1] ", end="")
            
            # auto_refresh=False para controlarmos o update manualmente a cada caractere
            with Live("", auto_refresh=False, transient=False) as live:
                for chunk in stream_reply(user_input, chat_history):
                    token = chunk.content
                    
                    # Buffer de interpolação: quebrando o token em caracteres
                    for char in token:
                        reply_full += char
                        # Usando string formatada em vez de Markdown para zero overhead de renderização
                        live.update(f"[grey84]{reply_full}[/grey84]", refresh=True)
                        time.sleep(0.015) # Ajustado para 0.015 para um ritmo de leitura ideal

            # Lógica de Ações Pós-Resposta
            if "TOOL_REWIND" in intent:
                console.print("\n[dim italic grey70]* Protocolo Rewind sugerido. *[/dim italic grey70]")
            elif "TOOL_EDIT" in intent:
                console.print("\n[dim italic grey70]* Módulo The Editor aguardando implementação. *[/dim italic grey70]")

            # Gestão de Memória (10 mensagens)
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=reply_full))
            if len(chat_history) > 10: 
                chat_history = chat_history[-10:]
                
        except KeyboardInterrupt:
            console.print("\n[bold sky_blue1]Sexta-Feira:[/bold sky_blue1] Interrupção detectada. Até logo.")
            break

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None: chat_loop()

@cli.command()
def rewind():
    console.print("[bold sky_blue1]Protocolo Rewind Iniciado.[/bold sky_blue1]")
    # Implementação do chronicler
    pass

if __name__ == "__main__":
    cli()