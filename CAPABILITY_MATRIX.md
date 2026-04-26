# FRIDAY V2 - CAPABILITY MATRIX
### What Makes Friday a True Assistant

---

## 🧠 1. CONSULTANT (Knowledge-Based Assistant)

### Current Capability ✅
- Can search indexed wiki documents
- Provides context-aware answers using RAG
- Retrieves relevant precedents from past notes

### What's Needed for Excellence ⏳
- [ ] Cross-reference related documents automatically
- [ ] Suggest follow-up questions based on query
- [ ] Track which docs were most helpful
- [ ] Learn from corrections (if user says "that's wrong")
- [ ] Provide confidence scores on answers

### Implementation Strategy
```python
# Future: rag.py enhancements
def smart_search(query, context_window=[]):
    """Search considering previous questions in conversation."""
    related_docs = find_similar_to_previous()
    ranked_docs = rank_by_relevance(related_docs, query)
    return docs_with_confidence_scores(ranked_docs)

def suggest_follow_ups(answer):
    """Generate 2-3 natural follow-up questions."""
    pass
```

---

## 💬 2. CONVERSATION PARTNER (Human-Like Interaction)

### Current Capability ✅
- Basic personality (formal, occasionally sarcastic)
- Maintains 10-message chat history
- Responds in Portuguese (localized)

### What's Needed for Excellence ⏳
- [ ] Detect user mood from text (frustrated, happy, tired, confused)
- [ ] Adapt response tone accordingly
  - Frustrated → More helpful, step-by-step
  - Happy → Enthusiastic, use more humor
  - Tired → Concise, get to point quickly
- [ ] Remember user preferences (communication style)
- [ ] Tell occasional jokes or make cultural references
- [ ] Apologize when wrong
- [ ] Ask clarifying questions when confused
- [ ] Use previous conversations to build context

### Implementation Strategy
```python
# New: agents/personality.py
class PersonalityEngine:
    def detect_mood(self, text: str) -> Mood:
        """Sentiment + linguistic analysis."""
        # Check for: !!! (excited), repeated chars (frustrated), etc.
        pass
    
    def adapt_tone(self, mood: Mood, base_response: str) -> str:
        """Adjust response style."""
        if mood == FRUSTRATED:
            return make_more_helpful(base_response)
        elif mood == HAPPY:
            return inject_enthusiasm(base_response)
        return base_response
    
    def remember_style_preference(self, user_id: str):
        """Learn if user prefers jokes, formality level, etc."""
        pass
```

### Example Flow
```
User: "Ugh, não consigo entender esse código"
      ↓
[Mood Detection] → FRUSTRATED
      ↓
Friday: "Entendo, pode ser confuso. Vou simplificar:
        Passo 1: ... (detailed explanation)
        Passo 2: ... (clear code example)
        
        Ficou claro? Posso expandir alguma parte?"
```

---

## 📝 3. DOCUMENT MANAGER (Creation & Maintenance)

### Current Capability ✅
- Can read documents
- Validates against schema
- Validates path security

### What's Needed for Excellence ⏳
- [ ] **Create new documents**
  - From templates (meeting notes, sprint review, etc.)
  - Auto-populate from chat conversation
  - Format code blocks with syntax highlighting
- [ ] **Edit existing documents**
  - Rewrite for clarity
  - Fix grammar & tone inconsistencies
  - Update outdated sections
  - Add cross-references
- [ ] **Maintain relationships**
  - Update links when docs renamed
  - Track document versions
  - Suggest related documents
- [ ] **Generate from raw data**
  - Create meeting summary from transcript
  - Generate report from data points
  - Create task lists from conversation

### Implementation Strategy
```python
# New: tools/document_manager.py
class DocumentManager:
    def create_from_template(self, template: str, data: dict):
        """Create new doc from template."""
        # Templates: meeting_notes, sprint_review, retrospective, etc.
        pass
    
    def rewrite_for_clarity(self, doc_path: str, aspect: str):
        """Rewrite document section."""
        # aspect: clarity, brevity, formality, examples, structure
        pass
    
    def generate_from_conversation(self, chat_history):
        """Extract key points from chat and create doc."""
        # Use entity extraction + summarization
        pass
    
    def update_cross_references(self, old_path: str, new_path: str):
        """Update all links pointing to renamed doc."""
        pass
    
    def suggest_related_docs(self, doc_path: str):
        """Find related documents using semantic search."""
        pass
```

### Example Flow
```
User: "Cria uma ata da reunião que tivemos"
Friday: [Searching chat history...]
        ✓ Extracted 8 decisions
        ✓ Extracted 12 action items
        ✓ Found 5 related past documents
        
        Criando documento...
        
[Generated: 2026-04-26-reuniao-sprint.md]
- [x] Decision 1
- [ ] Action Item 1 (Assigned: João, Deadline: 2026-05-10)
- [Link] Reunião anterior: link-to-past
```

---

## 📋 4. TASK MASTER (Memory & Accountability)

### Current Capability ⚠️
- Can see tasks in chat history (limited to 10 messages)
- No persistence

### What's Needed for Excellence ⏳
- [ ] **Persistent storage**
  - Store tasks in JSON/YAML with metadata
  - Sync with Obsidian task plugin
  - Query historical tasks
- [ ] **Intelligent reminders**
  - Time-based (every Friday)
  - Context-based (when mentioning related topic)
  - Priority-based (escalate if approaching deadline)
- [ ] **Task dependency tracking**
  - Task B blocked by Task A
  - Generate order of operations
  - Suggest optimizations
- [ ] **Progress tracking**
  - % completion estimations
  - Time spent vs. estimated
  - Burndown charts
- [ ] **Accountability**
  - Weekly summaries
  - Completion rates
  - Patterns (always late on UI? etc.)

### Implementation Strategy
```python
# New: agents/taskmaster.py
class TaskMaster:
    def create_task(self, title: str, deadline: str, priority: int):
        """Create persistent task with metadata."""
        task = {
            "id": uuid(),
            "title": title,
            "deadline": deadline,
            "priority": priority,
            "status": "pending",
            "created_at": now(),
            "tags": extract_tags(title)
        }
        self.persist_task(task)
        return task
    
    def set_reminder(self, task_id: str, trigger_type: str):
        """
        trigger_type: 'time' (deadline), 'context' (when related topic), 
                      'daily', 'weekly', 'milestone'
        """
        pass
    
    def find_blocked_tasks(self):
        """Return tasks waiting on other tasks."""
        pass
    
    def generate_weekly_report(self):
        """Completed, pending, overdue, patterns."""
        pass
```

### Example Flow
```
User: "Preciso refatorar o sistema de auth"
Friday: ✓ Tarefa criada: #1 "Refatorar sistema de auth"
        Deadline? (2026-05-10 é bom?)
        ↓
User: "Sim, dia 10"
Friday: ✓ Adicionado à lista
        
[Later in week]
Friday: 💭 Opa, você tem 1 tarefa vencendo em 3 dias
        
[Friday morning]
Friday: 📋 **RELATÓRIO SEMANAL**
        ✓ 7 tarefas completadas
        ⏳ 3 tarefas em progresso
        ⚠️ 2 tarefas atrasadas
        
        Você está 80% dentro do prazo
        Padrão: atrasado em DevOps (sempre demora +2 dias)
```

---

## 🔍 5. CODE REVIEWER (Quality Assurance)

### Current Capability ⚠️
- Can read code
- No analysis

### What's Needed for Excellence ⏳
- [ ] **Bug detection**
  - Null pointer risks
  - Logic errors
  - Security vulnerabilities
  - Type mismatches
- [ ] **Performance analysis**
  - O(n) complexity detection
  - Memory leaks
  - Inefficient algorithms
  - Suggest optimizations
- [ ] **Code smells**
  - Duplicated code
  - Functions too long
  - Variables poorly named
  - Magic numbers
  - Insufficient error handling
- [ ] **Style enforcement**
  - Consistency with project standards
  - Naming conventions
  - Documentation gaps
  - Test coverage
- [ ] **Architecture review**
  - Suggest design patterns
  - Identify tight coupling
  - Recommend refactoring

### Implementation Strategy
```python
# New: agents/code_reviewer.py
class CodeReviewer:
    def analyze_code(self, code: str, language: str) -> Review:
        """Comprehensive code analysis."""
        return Review(
            bugs=find_bugs(code),
            performance_issues=analyze_performance(code),
            code_smells=detect_smells(code),
            style_issues=check_style(code),
            architecture_suggestions=review_architecture(code)
        )
    
    def suggest_refactoring(self, code: str) -> List[Suggestion]:
        """Specific refactoring proposals."""
        # Return code + explanation of why
        pass
    
    def compare_versions(self, original: str, refactored: str):
        """Show before/after analysis."""
        pass
```

### Example Flow
```
User: "Analisa esse código"
      [pastes 50-line function]

Friday: 🔍 **CODE REVIEW**
        
        ⚠️ 3 Issues Found:
        1. Potential null pointer (line 12)
        2. O(n²) algorithm - could be O(n log n) (line 25)
        3. Function too long - should split into 3 functions
        
        💡 Suggestions:
        - Use Optional type for null-safe access
        - Use HashMap instead of nested loop
        - Extract helper methods for clarity
        
        Would you like the refactored version?
```

---

## ✏️ 6. DOCUMENT EDITOR (Refinement System)

### Current Capability ⚠️
- Can read documents
- No editing/improvement suggestions

### What's Needed for Excellence ⏳
- [ ] **Clarity improvement**
  - Simplify complex sentences
  - Break down long paragraphs
  - Add examples where needed
  - Remove jargon or explain it
- [ ] **Tone consistency**
  - Detect tone shifts
  - Align with style guide
  - Maintain voice across document
- [ ] **Structure optimization**
  - Suggest reorganization
  - Improve flow between sections
  - Better headlines
  - Table of contents
- [ ] **Grammar & style**
  - Fix grammar issues
  - Consistency (British vs American English)
  - Remove repetition
  - Improve readability score
- [ ] **Version comparison**
  - Show changes side-by-side
  - Explain why changes were made
  - Allow selective acceptance

### Implementation Strategy
```python
# New: agents/document_editor.py
class DocumentEditor:
    def analyze_clarity(self, text: str) -> ClarityReport:
        """Score clarity and suggest improvements."""
        return {
            "score": 8.5/10,
            "improvements": [
                "Sentence 3 is too long (42 words), break into 2",
                "Line 5 uses jargon, add explanation",
            ]
        }
    
    def simplify_text(self, text: str) -> str:
        """Rewrite for clarity."""
        pass
    
    def check_tone_consistency(self, text: str) -> Report:
        """Detect tone shifts."""
        pass
    
    def improve_structure(self, text: str) -> str:
        """Suggest reorganization."""
        pass
```

### Example Flow
```
User: "Reescreve esse documento para ficar mais claro"

Friday: 📝 **ANÁLISE**
        Clareza: 6.5/10 (abaixo da meta 8.0)
        Tone: Inconsistente (switches entre formal/casual)
        Estrutura: Boa, mas seção 3 é confusa
        
        🔧 **MELHORIAS SUGERIDAS**
        - Parágrafo 1: Muito longo, quebrar em 2
        - Parágrafo 3: Muito jargão, simplificar
        - Seção 2: Reordenar para flow melhor
        
        Versão reescrita:
        [mostra versão melhorada com highlights]
        
        Aceita as mudanças?
```

---

## 🎯 CAPABILITY ROADMAP

### NOW (MVP Phase 1-2) ✅
```
🧠 Consultant: ✅ Search + Context
💬 Conversation: ✅ Basic Personality  
📝 Documents: ✅ Read + Validate
📋 Tasks: ⚠️ Session-only
🔍 Code: ❌ Read-only
✏️ Editor: ❌ Not started
```

### NEXT (Phase 3a - 1-2 weeks) ⏳
```
🧠 Consultant: ✅ + Follow-ups
💬 Conversation: ✅ + Mood Detection
📝 Documents: ✅ + Create + Edit
📋 Tasks: ✅ Persistent Storage
🔍 Code: ✅ Bug Detection
✏️ Editor: ✅ Clarity Analysis
```

### LATER (Phase 3b - Month 2) 🔮
```
🧠 Consultant: ✅ + Learning
💬 Conversation: ✅ + Preferences
📝 Documents: ✅ + Templates
📋 Tasks: ✅ + Dependencies
🔍 Code: ✅ + Architecture
✏️ Editor: ✅ + Tone Sync
```

### FUTURE (Phase 3c - Month 3+) 🚀
```
🧠 Consultant: ✅ + Prediction
💬 Conversation: ✅ + Context Memory
📝 Documents: ✅ + Collaboration
📋 Tasks: ✅ + Analytics
🔍 Code: ✅ + Refactoring
✏️ Editor: ✅ + Full Workflow
```

---

## 🏆 SUCCESS CRITERIA: "Friday is Done When..."

- [x] **Consultant**: Answers any question about your projects using wiki
- [ ] **Partner**: Feels like talking to a real person who knows you
- [ ] **Manager**: Creates & tracks your tasks automatically
- [ ] **Writer**: Helps write, review, and refine all documents
- [ ] **Coder**: Reviews code and catches real bugs
- [ ] **Team**: Remembers everything important across weeks/months

---

## 📈 Time Estimate to Full Capability

| Phase | What | Time | Status |
|-------|------|------|--------|
| 1 | Foundation | 1 day | ✅ |
| 2 | Current Features | 1 day | ⏳ (4h left) |
| 3a | Enhanced Features | 1-2 weeks | 🔮 |
| 3b | Advanced Features | 1-2 weeks | 🔮 |
| 3c | Mastery | 1-2 weeks | 🚀 |

**Total to Full Assistant**: ~4-6 weeks of development

---

**Remember**: Each phase builds on the last. Complete Phase 2 first, then choose which Phase 3 feature to prioritize based on YOUR needs.

