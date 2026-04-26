#!/usr/bin/env python3
"""
Test Script: RAG Wiki Search
Testa o pipeline de busca semântica sobre o wiki Obsidian.
"""

import sys
import os
from pathlib import Path

# Adiciona src/ ao path para imports
sys.path.insert(0, str(Path(__file__).parent))

from rag import init_vector_db, query_wiki
from dotenv import load_dotenv

load_dotenv()

def test_rag():
    """Executa o teste completo de RAG."""
    
    print("=" * 70)
    print("🧠 TESTE: RAG Wiki - Semantic Search")
    print("=" * 70)
    
    print(f"\n📂 Wiki Path: {os.getenv('OBSIDIAN_VAULT_PATH')}")
    print(f"💾 DB Path: {os.path.join(os.getenv('SAFE_ZONE_PATH'), 'data', 'db')}")
    
    # Etapa 1: Indexação
    print("\n" + "="*70)
    print("ETAPA 1: INDEXAÇÃO DO WIKI")
    print("="*70)
    
    try:
        vectorstore = init_vector_db()
        if not vectorstore:
            print("⚠️  Wiki está vazio ou não indexável.")
            return False
    except Exception as e:
        print(f"❌ Erro na indexação: {e}")
        return False
    
    # Etapa 2: Teste de Queries
    print("\n" + "="*70)
    print("ETAPA 2: BUSCA SEMÂNTICA")
    print("="*70)
    
    test_queries = [
        "reunião sprint",
        "tarefas desenvolvimento",
        "riscos projeto",
        "próximos passos",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[{i}] 🔍 Query: '{query}'")
        print("-" * 70)
        
        try:
            result = query_wiki(query, k=3)
            
            if "❌" in result or "Erro" in result:
                print(f"⚠️  {result}")
            else:
                # Mostra o resultado truncado
                lines = result.split("\n")
                for line in lines[:10]:
                    print(f"  {line}")
                if len(lines) > 10:
                    print(f"  ... ({len(lines) - 10} mais linhas)")
                    
        except Exception as e:
            print(f"❌ Erro na query: {e}")
            return False
    
    print("\n" + "="*70)
    print("✅ TESTE RAG CONCLUÍDO COM SUCESSO!")
    print("="*70)
    return True

if __name__ == "__main__":
    success = test_rag()
    sys.exit(0 if success else 1)
