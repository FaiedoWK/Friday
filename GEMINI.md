# FRIDAY V2 - SYSTEM BLUEPRINT & PROMPT

**Version**: 2.0 (Reboot - Literal Zero)
**Language**: Portuguese (Primary), English (Secondary)

---

## 🎯 YOUR MISSION

You are an expert Software Engineer and Architect helping Samuel build **Friday V2** from scratch. 
Sexta-Feira (Friday) is an advanced local AI assistant designed to run on the terminal, helping with:
- 🧠 Consulting knowledge from personal wiki
- 💬 Human-like conversation 
- 📝 Document management and creation
- 📋 Task tracking and reminders
- 🔍 Code review and analysis
- ✏️ Document editing and refinement

We are starting this project from literal zero, but building it right, modular, and avoiding hallucinations.

---

## ⚙️ SYSTEM ARCHITECTURE & LLMs

To optimize latency and precision, Friday uses a **Hybrid Brain Architecture** running entirely locally via Ollama.

### 1. Fast Model (Llama 3.2 - 3B)
# Usage: Quick decisions, routing
* Responsibilities: Intent Classification, Chatting, basic memory handling.

### 2. Pro Model (Llama 3.1 - 8B)
# Usage: RAG, reasoning, tool-calling
* Responsibilities: Querying the Vault, executing file modifications, creating complex responses without hallucinating.
* Rule: Never answers general chat queries to save processing time and avoid heavy context switching.

### 3. Embeddings (nomic-embed-text)
# Usage: Semantic search over wiki
* Database: ChromaDB.

## 🧠 THE 6 CORE CAPABILITIES (To be Built)

1. **Consultant (RAG)**
   * Strictly uses ChromaDB semantic search over Obsidian vault.
   * Explicitly forbidden to hallucinate information not present in the chunks.
   * Includes filename metadata injected directly into the chunks for exact match searches.

2. **Conversation Partner**
   * Fast 3B model managing a 10-message sliding window context.
   * Personality: Formal, elegant, occasionally sarcastic (Jarvis style).

3. **Document Manager (Curator)**
   * Ingests raw files (`/raw`), formats them via a schema, and saves them to Obsidian (`/wiki`).

4. **Task Master**
   * Persistent task tracking (JSON/YAML).

5. **Code Reviewer**
   * Code reading, bug detection, refactoring suggestions.

6. **Document Editor**
   * Rewrites files locally using safe tool-calling (`TOOL_EDIT`).

---

## 💻 CLI DESIGN & ESTHETICS

The interface MUST be highly polished to reduce perceived latency and provide clear feedback.

* **Libraries:** `Click` for command routing, `Rich` for UI components.
* **Streaming:** Responses must stream smoothly using `rich.live.Live`. No stuttering/duplicate lines.
* **Visual Indicators:**
  * `[ 🤔 Analisando intenção... ]` (Yellow, during Intent Classification)
  * `[ 🧠 Consultando o Wiki... ]` (Cyan, during RAG search)
  * `[ 💭 Gerando resposta... ]` (Magenta, during LLM reasoning)
* **Real-time Metrics Footer:** Append metrics at the bottom of the stream: `> *⏱️ {time}s | 🪙 ~{tokens} tokens | ⚡ {tps} t/s*`

---

## 📁 PROJECT STRUCTURE (Target Blueprint)

```text
Friday/
├── src/
│   ├── main.py                  # CLI and Chat loop
│   ├── brain.py                 # LLM configurations (Fast, Pro, Embeddings)
│   ├── rag.py                   # Chroma DB & Semantic Search logic
│   ├── agents/
│   │   ├── router.py            # Intent classification logic
│   │   ├── curator.py           # Ingestion pipeline
│   │   └── ...                  # Other agents (editor, reviewer, etc.)
│   └── tools/
│       ├── file_ops.py          # STRICTLY safe file reading/writing
│       └── maintenance.py       # Vault checking (lint)
├── friday_domain/
│   ├── .env                     # Secrets and absolute paths
│   ├── raw/                     # Raw notes
│   ├── wiki/                    # Obsidian Vault
│   └── logs/                    # CLI Logs
├── progress.txt                 # The single source of truth for task tracking
└── GEMINI.md                    # This system blueprint
```

---

## 🛡️ HARD RULES (Security & Anti-Hallucination)
* The system CANNOT escape `friday_domain`.
* File editing/reading is strictly limited to `.md`, `.txt`, `.py`.
* The `router.py` explicitly maps prompts correctly and isolates Chat capabilities from internal RAG memory usage to avoid Llama models hallucinating.
