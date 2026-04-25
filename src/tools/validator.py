import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SAFE_ZONE = os.getenv("SAFE_ZONE_PATH")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", ".md,.txt,.py").split(",")

def validate_path(target_path: str) -> str:
    """
    Valida se o caminho solicitado está dentro da Safe Zone e possui extensão permitida.
    Retorna o caminho absoluto se válido, caso contrário, levanta um erro de segurança.
    """
    # 1. Resolve para o caminho absoluto (previne bypass com ../)
    abs_safe_zone = Path(SAFE_ZONE).resolve()
    abs_target = Path(target_path).resolve()

    # 2. Verifica se o target começa com o path da Safe Zone
    if not str(abs_target).startswith(str(abs_safe_zone)):
        raise PermissionError(f"Acesso negado: O caminho {target_path} está fora da Safe Zone!")

    # 3. Restrição de Extensões (apenas para arquivos)
    if abs_target.suffix and abs_target.suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Extensão {abs_target.suffix} não permitida!")

    return str(abs_target)