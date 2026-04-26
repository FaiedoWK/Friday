#!/usr/bin/env python3
"""
Test Script: Curator Ingestion Pipeline
Testa o processo completo de ingestão de arquivo NotebookLM para o Wiki.
"""

import sys
import os
from pathlib import Path

# Adiciona src/ ao path para imports
sys.path.insert(0, str(Path(__file__).parent))

from agents.curator import run_ingest
from dotenv import load_dotenv

load_dotenv()

def test_curator():
    """Executa o teste de ingestão do Curator."""
    
    print("=" * 70)
    print("🎯 TESTE: Curator - Ingestion Pipeline")
    print("=" * 70)
    
    # Configuração do teste
    raw_file = "reuniao_sprint_q2.txt"
    output_topic = "reuniao sprint q2"
    
    print(f"\n📂 Arquivo de entrada: {raw_file}")
    print(f"📝 Tópico: {output_topic}")
    print(f"🏠 Safe Zone: {os.getenv('SAFE_ZONE_PATH')}")
    print(f"📚 Wiki Path: {os.getenv('OBSIDIAN_VAULT_PATH')}")
    
    # Executa a ingestão
    print("\n▶️  Iniciando ingestão...")
    try:
        run_ingest(raw_file, output_topic)
        print("\n✅ Teste concluído com sucesso!")
        
        # Verifica se o arquivo foi criado
        vault_path = Path(os.getenv('OBSIDIAN_VAULT_PATH'))
        wiki_files = list(vault_path.glob("*.md"))
        
        if wiki_files:
            print(f"\n📄 Arquivos no Wiki ({len(wiki_files)}):")
            for wf in sorted(wiki_files):
                print(f"   - {wf.name}")
        else:
            print("\n⚠️  Nenhum arquivo criado no Wiki.")
            
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_curator()
    sys.exit(0 if success else 1)
