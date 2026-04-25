# Sexta-Feira (Friday) - AI Agent System

An intelligent AI agent system powered by local LLMs, built with LangChain and designed for advanced task management, knowledge retrieval, and conversational intelligence.

## Overview

**Sexta-Feira** is a sophisticated CLI-based AI assistant that brings together multiple specialized agents to handle different types of requests. The system runs locally using Ollama with Llama 3.2, ensuring privacy and control over your AI interactions.

### Key Features

- 🤖 **Intent Router**: Intelligently classifies user requests and routes them to appropriate agents
- 💾 **Session Memory**: Maintains context with 10-message short-term memory for coherent conversations
- 📚 **RAG System**: Semantic search capabilities over your knowledge base using ChromaDB
- 🔗 **Obsidian Vault Integration**: Seamlessly connects to your Obsidian vault for note curation
- 🎨 **Rich CLI Interface**: Beautiful, responsive terminal UI with streaming responses
- 🚀 **Local-First**: Runs entirely on your machine using Ollama—no external API calls needed

## Project Structure

```
Friday/
├── src/
│   ├── main.py              # Entry point with chat loop
│   ├── brain.py             # LLM initialization and configuration
│   ├── rag.py               # Vector database and semantic search
│   ├── agents/
│   │   ├── router.py        # Intent classification & routing
│   │   ├── chronicler.py    # Task recording & history
│   │   └── curator.py       # Obsidian vault curation
│   └── tools/
│       ├── editor.py        # File editing utilities
│       ├── file_ops.py      # File operations
│       └── validator.py     # Data validation
├── friday_domain/
│   ├── schema.md            # Data structure definitions
│   ├── wiki/                # Knowledge base (synced with Obsidian)
│   ├── raw/                 # Raw ingestion data
│   ├── vault/               # Obsidian vault reference
│   └── logs/                # Domain-specific logs
├── data/
│   └── db/                  # Vector DB storage (ChromaDB)
├── requirements.txt         # Python dependencies
└── progress.txt             # Development progress tracking
```

## Components

### Router (`agents/router.py`)
Classifies user intentions and routes requests to the appropriate agent. Supports intents like:
- `CHAT`: General conversation
- `TOOL_*`: Tool-specific operations
- `RAG_SEARCH`: Knowledge base queries
- `CURATION`: Vault management

### Chronicler (`agents/chronicler.py`)
Records conversations, maintains history, and manages session context.

### Curator (`agents/curator.py`)
Handles Obsidian vault integration and note management. Features:
- Automatic note ingestion
- Tag-based organization
- Task extraction to "Pendências" sections

### RAG System (`src/rag.py`)
Provides semantic search over your wiki and knowledge base using ChromaDB embeddings.

## Requirements

- **Python**: 3.9+
- **Ollama**: Running with Llama 3.2 for conversation mode and Llama 3.1 Instruct for tool-calling mode
- **Memory**: 4GB+ recommended

## Installation

1. **Clone or navigate to the project**:
   ```bash
   cd Friday
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment** (create `.env` file):
   ```env
   OBSIDIAN_VAULT_PATH=/path/to/your/vault
   OLLAMA_MODEL=llama2
   OLLAMA_BASE_URL=http://localhost:11434
   ```

4. **Ensure Ollama is running**:
   ```bash
   ollama serve
   ```

## Usage

### Start the chat interface
```bash
python src/main.py
```

Or use the global alias (if configured):
```bash
friday
```

### Example interactions

```
User: What's the status of my projects?
Sexta-Feira: [Returns categorized task list with dates and priorities]

User: Search my wiki for async patterns
Sexta-Feira: [Retrieves semantically similar notes using RAG]

User: Add a reminder to review the architecture
Sexta-Feira: [Creates note in Obsidian vault with proper tagging]
```

## Technology Stack

- **LLM Framework**: LangChain 0.3.0+
- **Local LLM**: Ollama + Llama 3.2
- **Vector DB**: ChromaDB 0.5.15+ (semantic search)
- **Document Processing**: PyPDF 4.2.0+
- **CLI UI**: Rich 13.7.1 (beautiful terminal formatting)
- **Configuration**: python-dotenv 1.0.1
- **CLI Framework**: Click 8.1.7

## Development Status

### Completed ✅
- Intent classification router
- Session memory management (10-message history)
- Basic chat interface with Rich formatting
- Global CLI alias setup

### In Progress 🔄
- CLI streaming responses (latency reduction)
- Obsidian vault integration with real file testing
- Rich Live displays for better UX

### Planned 📋
- Semantic search over wiki directory
- Advanced task management (Taskmaster agent)
- Maintenance commands (`friday lint`)
- Performance optimizations

## Wiki Formatting Rules

All notes in the wiki follow these conventions:

1. **Tags**: Start with relevant tags (e.g., `#dev-container`, `#reuniao`)
2. **Tasks**: Extract to a final "## Pendências" section with checkboxes
3. **Structure**: Use bullet points for scannability
4. **Tone**: Maintain professional language

Example:
```markdown
# Projeto X

#dev #importante

- Ponto principal 1
- Ponto principal 2

## Pendências
- [ ] Implementar feature A
- [ ] Revisar PR #42
```

## Commands

| Command | Purpose |
|---------|---------|
| `exit` / `quit` / `sair` | Exit the chat |
| `friday lint` | Audit system integrity (planned) |

## Configuration

All configuration is stored in `.env`. Key variables:

- `OBSIDIAN_VAULT_PATH`: Path to your Obsidian vault root
- `OLLAMA_MODEL`: Which model to use (default: llama2)
- `OLLAMA_BASE_URL`: Ollama server address (default: http://localhost:11434)

## Troubleshooting

### Ollama connection issues
- Verify Ollama is running: `ollama serve`
- Check `.env` has correct `OLLAMA_BASE_URL`
- Ensure port 11434 is accessible

### Vault integration not working
- Verify `OBSIDIAN_VAULT_PATH` points to the correct vault root
- Ensure the path exists and is readable
- Check that the `wiki/` directory is writable

### Low response quality
- Ensure Llama 3.2 model is downloaded: `ollama pull llama2`
- Provide more context in your queries
- Review session history for conversation coherence

## Contributing

Development guidelines:

1. Keep chat loop responsive—use Rich streaming for long outputs
2. Maintain clear intent classification in the router
3. Document new agents in `agents/` with clear docstrings
4. Update `progress.txt` with completed tasks
5. Follow wiki formatting rules in documentation

## License

[Add your license here]

## Author

My Friday AI Assistant

---

**Status**: Phase 2 - CLI Plus Development  
**Last Updated**: April 2026
