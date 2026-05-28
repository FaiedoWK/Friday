"""
Curator Agent - Manages document ingestion from /raw to /wiki
Handles formatting, schema validation, and metadata injection
"""
import os
from pathlib import Path
from datetime import datetime
from src.tools.file_ops import read_file, write_file, list_files

FRIDAY_DOMAIN = Path(os.getenv("FRIDAY_DOMAIN_PATH", "./friday_domain")).resolve()
RAW_DIR = FRIDAY_DOMAIN / "raw"
WIKI_DIR = FRIDAY_DOMAIN / "wiki"


def format_obsidian_note(content: str, tags: list = None, source: str = "") -> str:
    """
    Formats raw content into Obsidian-compatible Markdown.
    Injects metadata (source, date, tags) as frontmatter.
    """
    if tags is None:
        tags = ["inbox"]
    
    frontmatter = f"""---
created: {datetime.now().isoformat()}
source: {source}
tags: {' '.join([f'#{tag}' for tag in tags])}
---

"""
    return frontmatter + content


def ingest_raw_file(raw_filename: str, wiki_filename: str = None, tags: list = None) -> str:
    """
    Reads a file from /raw, formats it for Obsidian, and saves to /wiki.
    
    Args:
        raw_filename: filename in raw/ (relative path)
        wiki_filename: output filename in wiki/ (defaults to same name)
        tags: list of tags to add to frontmatter
    
    Returns: success/error message
    """
    try:
        if wiki_filename is None:
            wiki_filename = raw_filename
        
        # Read raw file
        raw_path = f"raw/{raw_filename}"
        content = read_file(raw_path)
        
        if content.startswith("❌"):  # Error
            return content
        
        # Format for Obsidian
        formatted = format_obsidian_note(content, tags=tags or ["inbox"], source=raw_filename)
        
        # Write to wiki
        wiki_path = f"wiki/{wiki_filename}"
        result = write_file(wiki_path, formatted)
        
        if "✅" in result:
            return f"✅ Documento curado: {raw_filename} → {wiki_filename}"
        else:
            return result
    
    except Exception as e:
        return f"❌ Erro ao curar documento: {e}"


def list_pending_ingestion() -> str:
    """
    Lists files in /raw that haven't been processed yet.
    Returns: formatted list of pending files
    """
    return list_files("raw")


def validate_vault_structure() -> str:
    """
    Validates that vault directories exist and are accessible.
    Returns: validation report
    """
    checks = []
    
    # Check raw directory
    raw_exists = RAW_DIR.exists()
    checks.append(f"{'✅' if raw_exists else '❌'} /raw directory: {RAW_DIR}")
    
    # Check wiki directory
    wiki_exists = WIKI_DIR.exists()
    checks.append(f"{'✅' if wiki_exists else '❌'} /wiki directory: {WIKI_DIR}")
    
    # Create if missing
    if not raw_exists:
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        checks.append("  → Criado /raw directory")
    
    if not wiki_exists:
        WIKI_DIR.mkdir(parents=True, exist_ok=True)
        checks.append("  → Criado /wiki directory")
    
    return "\n".join(checks)
