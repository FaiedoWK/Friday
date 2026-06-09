# Sexta-Feira (Friday) - AI assistant V2

Um sistema inteligente de agentes de IA baseado em LLMs locais, construído com LangChain Clássico e projetado para orquestração de tarefas, gestão de conhecimento local e automação contextual.

## 🚀 Visão Geral (Nova Arquitetura)

A **Sexta-Feira V2** foi reconstruída sob o conceito de **Cérebro Único**. Em vez de múltiplos agentes e roteadores complexos, o sistema agora utiliza o modelo **Qwen 2.5 7B** de forma nativa para raciocínio, classificação de intenções e chamadas de função (*Tool Calling*) simultâneas. O ecossistema roda inteiramente de forma local e privada via **Ollama**.

### Key Features (Recursos Principais)

- 🧠 **Cérebro Único (Tool Calling Nativo)**: Acionamento de funções ultraestável direto pelo Qwen 2.5 7B, garantindo respostas rápidas sem perda de contexto.
- 🎬 **Interface Claude Code**: Um loader minimalista dinâmico alimentado por threads em segundo plano que exibe mensagens de status e spinners ASCII, limpando a tela automaticamente quando o modelo responde.
- ✍️ **Streaming Suave (Typing Effect)**: Exibição de caracteres de forma incremental (letra por letra), imitando digitação real em tempo de execução.
- 📂 **Motor Isolado dos Dados**: Armazenamento modular local protegido por regras estritas do Git, ideal para uso híbrido (casa/trabalho).
- 💾 **Memória de Curto Prazo**: Retenção exata dos últimos 5 turnos de conversa (10 mensagens) para poupar memória RAM e manter coerência.

## 📁 Estrutura do Projeto

```text
Friday/
├── v2_storage/              # Dados locais (Ignorados pelo Git)
│   ├── wiki/                # Repositório de notas Markdown pessoais
│   │   └── .gitkeep         # Arquivo âncora para manter a pasta no Git
│   └── tasks.md             # Arquivo centralizado de gerenciamento de tarefas
├── .env                     # Variáveis de ambiente e caminhos locais
├── .gitignore               # Escudo de rastreamento do Git
├── main.py                  # Script principal (Cérebro, Tools e Loop CLI)
├── progress.txt             # Diário de bordo e metas de desenvolvimento
└── README.md                # Documentação do sistema

```

## 🛠️ Ferramentas Atuais do Motor

O modelo tem autonomia para decidir quando e como invocar as seguintes funções em segundo plano:

| Ferramenta | Descrição | Destino Físico |
| --- | --- | --- |
| `ler_wiki` | Lê e traz o contexto de notas Markdown específicas. | `v2_storage/wiki/*.md` |
| `escrever_wiki` | Cria novas notas ou sobrescreve arquivos inteiros. | `v2_storage/wiki/*.md` |
| `listar_arquivos_wiki` | Lista todos os arquivos existentes na documentação. | `v2_storage/wiki/` |
| `gerenciar_tarefas` | Visualiza, adiciona ou modifica a lista de afazeres. | `v2_storage/tasks.md` |
| `web_scraping` | Coleta e limpa o texto bruto de URLs públicas. | Internet (Web) |

## ⚙️ Configuração & Instalação

1. **Garantir a estrutura limpa e o ambiente Python:**
```bash
python -m venv .venv
# Ative o ambiente virtual (.venv\Scripts\activate no Windows)
pip install -r requirements.txt

```


2. **Configurar o arquivo `.env` na raiz do projeto:**
```env
WIKI_PATH="./v2_storage/wiki"
TASKS_PATH="./v2_storage/tasks.md"
OLLAMA_MODEL="qwen2.5:7b"

```


3. **Garantir o modelo no Ollama:**
```bash
ollama pull qwen2.5:7b

```



## 🤖 Uso pelo Terminal

Para iniciar o sistema de conversação, execute:

```bash
python main.py

```

### Comandos Especiais

* Digite `sair`, `quit` ou `exit` dentro do chat para encerrar os sistemas da Sexta-Feira com segurança.
* Use interrupções de teclado (`Ctrl + C`) para desligar o loop principal de forma forçada sem corromper arquivos.

```

---

O `README.md` está agora impecável e atualizado de ponta a ponta com o que o motor de fato faz! É uma excelente prática manter a documentação alinhada. 

Tudo atualizado, commitado e documentado. O que o senhor deseja fazer agora?

```