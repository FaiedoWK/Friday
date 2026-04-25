import os
from langchain.tools import tool
from dotenv import load_dotenv
from tools.validator import validate_path

load_dotenv()
SAFE_ZONE = os.getenv("SAFE_ZONE_PATH")

@tool
def write_file(relative_path: str, content: str) -> str:
    """
    Cria ou sobrescreve um arquivo de texto com o conteúdo fornecido.
    Use esta ferramenta para salvar logs diários ou criar novos arquivos de código.
    """
    try:
        # Resolve o caminho baseado na safe zone
        full_path = os.path.join(SAFE_ZONE, relative_path)
        
        # Garante que não vamos escapar da área permitida
        valid_path = validate_path(full_path)
        
        # Garante que o diretório alvo (ex: logs/) existe
        os.makedirs(os.path.dirname(valid_path), exist_ok=True)
        
        with open(valid_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return f"Sucesso: Arquivo salvo em {valid_path}"
    except Exception as e:
        return f"Erro de I/O ao salvar arquivo: {str(e)}"
    
@tool
def read_file(relative_path: str) -> str:
    """
    Lê e retorna o conteúdo completo de um arquivo de texto.
    """
    try:
        # REsolve o caminho baseado na safe zone
        full_path = os.path.join(SAFE_ZONE, relative_path)

        # Validação de segurança rigorosa
        valid_path = validate_path(full_path)

        if not os.path.exists(valid_path):
            return f"Erro: O arquivo {relative_path} não foi encontrado."
        
        with open(valid_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    except Exception as e:
        return f"Erro de I/O ao ler arquivo: {str(e)}"