# SPEC.md: Jarvis Local Agent (Sexta-Feira) - V2

## 1. Visão Geral
Sexta-Feira é um agente de IA local focado em privacidade e produtividade para o fluxo de trabalho da Quero-Quero. Utiliza uma arquitetura de "LLM Wiki" para transformar dados brutos em conhecimento estruturado e persistente no Obsidian.

## 2. Sandbox e Segurança (Hard Rules)

* **Safe Zone Path:** `C:\Users\980282\dev\Friday\friday_domain`
* **Restrições:**

* Operações de I/O restritas a subpastas: `/raw`, `/wiki` (Obsidian Vault) e `/logs`.
* Validação rigorosa contra escape de diretório (Path Traversal).
* Manipulação exclusiva de extensões seguras: `.md`, `.txt`, `.py`.

## 3. Arquitetura de Motores (Hybrid Brain)
O sistema opera em dois níveis de processamento para otimizar latência e precisão:

### 3.1 Motor Conversacional e Roteamento (Llama 3.2 3B)

* **Função:** Chat de baixa latência, gestão de memória de curto prazo (sliding window) e classificação de intenções.
* **Intenções:** `CHAT`, `RAG_QUERY`, `TOOL_EDIT`, `TOOL_REWIND`.

### 3.2 Motor Operacional e Ferramentas (Llama 3.1 8B-Instruct)

* **Função:** Execução de ferramentas via Zero-Shot Tool Calling.
* **Operações:** Escrita/Leitura de arquivos, Curadoria de Wiki, Edição de código.
* **Isolamento:** Não recebe histórico de chat para evitar falhas sintáticas em chamadas de função.

## 4. Estrutura LLM Wiki (Karpathy Methodology)

1. **Raw Layer (`/raw`):** Ingestão de arquivos brutos (PDFs, notas de reuniões, notebooks).
2. **Wiki Layer (`/wiki`):** O cofre do Obsidian. Arquivos Markdown processados e linkados.
3. **Schema Layer (`schema.md`):** Definições de formatação e regras de extração de pendências.
4. **Maintenance Layer (Lint):** Auditoria semanal (Sextas-feiras) para limpeza e organização da base.

## 5. Interface (CLI)

* Interface construída com `Click` e `Rich`.
* Invocação global via comando `friday` no PowerShell.

## 5.1 Estética

* Definir a paleta de cores e o uso de fontes monoespaçadas para manter o estilo minimalista.