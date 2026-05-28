"""
Safe File Operations - Strictly limited to .md, .txt, .py files within friday_domain
"""
import os
import pathlib
from pathlib import Path
from typing import Optional

# Security boundary - all operations must be within this directory
FRIDAY_DOMAIN = Path(os.getenv("FRIDAY_DOMAIN_PATH", "./friday_domain")).resolve()

ALLOWED_EXTENSIONS = {".md", ".txt", ".py"}


def _validate_path(file_path: str) -> Path:
    """
    Validates that file_path is within friday_domain and has allowed extension.
    Raises ValueError if path is invalid or outside boundaries.
    """
    # Resolve to absolute path
    resolved = (FRIDAY_DOMAIN / file_path).resolve()
    
    # Security check: must be within FRIDAY_DOMAIN
    try:
        resolved.relative_to(FRIDAY_DOMAIN)
    except ValueError:
        raise ValueError(f"❌ Acesso negado: caminho fora de friday_domain")
    
    # Check extension
    if resolved.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError(f"❌ Extensão não permitida: {resolved.suffix}. Permitidas: {ALLOWED_EXTENSIONS}")
    
    return resolved


def read_file(file_path: str) -> str:
    """
    Safely reads a file from friday_domain.
    Returns: file content or error message
    """
    try:
        resolved = _validate_path(file_path)
        
        if not resolved.exists():
            return f"❌ Arquivo não encontrado: {file_path}"
        
        if not resolved.is_file():
            return f"❌ Não é um arquivo: {file_path}"
        
        with open(resolved, "r", encoding="utf-8") as f:
            return f.read()
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"❌ Erro ao ler arquivo: {e}"


def write_file(file_path: str, content: str) -> str:
    """
    Safely writes content to a file in friday_domain.
    Creates parent directories if needed.
    Returns: success or error message
    """
    try:
        resolved = _validate_path(file_path)
        
        # Create parent directories if they don't exist
        resolved.parent.mkdir(parents=True, exist_ok=True)
        
        with open(resolved, "w", encoding="utf-8") as f:
            f.write(content)
        
        return f"✅ Arquivo salvo: {file_path}"
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"❌ Erro ao salvar arquivo: {e}"


def append_file(file_path: str, content: str) -> str:
    """
    Safely appends content to a file in friday_domain.
    Creates the file if it doesn't exist.
    Returns: success or error message
    """
    try:
        resolved = _validate_path(file_path)
        
        # Create parent directories if they don't exist
        resolved.parent.mkdir(parents=True, exist_ok=True)
        
        with open(resolved, "a", encoding="utf-8") as f:
            f.write(content)
        
        return f"✅ Conteúdo adicionado: {file_path}"
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"❌ Erro ao adicionar conteúdo: {e}"


def list_files(dir_path: str = "") -> str:
    """
    Lists files in a directory within friday_domain.
    Returns: formatted file list or error message
    """
    try:
        dir_resolved = (FRIDAY_DOMAIN / dir_path).resolve()
        
        # Validate directory is within bounds
        try:
            dir_resolved.relative_to(FRIDAY_DOMAIN)
        except ValueError:
            return f"❌ Acesso negado: diretório fora de friday_domain"
        
        if not dir_resolved.exists():
            return f"❌ Diretório não encontrado: {dir_path}"
        
        if not dir_resolved.is_dir():
            return f"❌ Não é um diretório: {dir_path}"
        
        # List files with allowed extensions
        items = []
        for item in sorted(dir_resolved.iterdir()):
            rel_path = item.relative_to(FRIDAY_DOMAIN)
            if item.is_dir():
                items.append(f"📁 {rel_path}/")
            elif item.suffix.lower() in ALLOWED_EXTENSIONS:
                items.append(f"📄 {rel_path}")
        
        if not items:
            return f"Diretório vazio: {dir_path}"
        
        return "\n".join(items)
    except Exception as e:
        return f"❌ Erro ao listar diretório: {e}"


def delete_file(file_path: str) -> str:
    """
    Safely deletes a file from friday_domain.
    Returns: success or error message
    """
    try:
        resolved = _validate_path(file_path)
        
        if not resolved.exists():
            return f"❌ Arquivo não encontrado: {file_path}"
        
        if not resolved.is_file():
            return f"❌ Não é um arquivo: {file_path}"
        
        resolved.unlink()
        return f"✅ Arquivo deletado: {file_path}"
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"❌ Erro ao deletar arquivo: {e}"
