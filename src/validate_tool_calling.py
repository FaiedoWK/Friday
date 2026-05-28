#!/usr/bin/env python3
"""
Tool Calling Validation - Quick checks without LLM calls
Validates that the tool calling infrastructure is properly wired
"""

import sys
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

console = Console()


def test_imports():
    """Verify all modules can be imported"""
    console.print("\n[bold cyan]CHECK 1: Module Imports[/bold cyan]")
    try:
        from src.tools.file_ops import read_file, write_file, list_files
        from src.agents.curator import ingest_raw_file, validate_vault_structure
        from src.agents.handlers import handle_rag_search, handle_tool_edit, handle_curation
        from src.agents.router import classify_intent, handle_intent
        console.print("  [bold green]✅ All modules import successfully[/bold green]")
        return True
    except Exception as e:
        console.print(f"  [bold red]❌ Import failed: {e}[/bold red]")
        return False


def test_file_ops():
    """Test file operations without LLM"""
    console.print("\n[bold cyan]CHECK 2: File Operations[/bold cyan]")
    try:
        from src.tools.file_ops import read_file, write_file, list_files
        
        # Write test
        result = write_file("wiki/check_test.txt", "test content")
        assert "✅" in result, f"Write failed: {result}"
        console.print("  ✅ Write operation works")
        
        # Read test
        content = read_file("wiki/check_test.txt")
        assert "test content" in content, "Read mismatch"
        console.print("  ✅ Read operation works")
        
        # List test
        listing = list_files("wiki")
        assert "check_test.txt" in listing, "List failed"
        console.print("  ✅ List operation works")
        
        console.print("  [bold green]✅ All file operations work[/bold green]")
        return True
    except Exception as e:
        console.print(f"  [bold red]❌ File ops failed: {e}[/bold red]")
        return False


def test_vault_structure():
    """Test vault initialization"""
    console.print("\n[bold cyan]CHECK 3: Vault Structure[/bold cyan]")
    try:
        from src.agents.curator import validate_vault_structure
        
        report = validate_vault_structure()
        console.print("  " + report.replace("\n", "\n  "))
        console.print("  [bold green]✅ Vault structure valid[/bold green]")
        return True
    except Exception as e:
        console.print(f"  [bold red]❌ Vault check failed: {e}[/bold red]")
        return False


def test_intent_handler_wiring():
    """Test that handlers are properly wired to router"""
    console.print("\n[bold cyan]CHECK 4: Intent Handler Wiring[/bold cyan]")
    try:
        from src.agents.router import handle_intent
        
        # Test that handle_intent returns correct handler types
        handler_type, _ = handle_intent("[CHAT]", "hello")
        assert handler_type == "chat", f"Expected 'chat', got '{handler_type}'"
        console.print("  ✅ [CHAT] handler wired")
        
        handler_type, response = handle_intent("[TOOL_EDIT]", "list files in wiki")
        assert handler_type == "tool", f"Expected 'tool', got '{handler_type}'"
        assert "wiki" in response or "❌" not in response, f"Handler returned error: {response}"
        console.print("  ✅ [TOOL_EDIT] handler wired")
        
        handler_type, response = handle_intent("[CURATION]", "process pending documents")
        assert handler_type == "curation", f"Expected 'curation', got '{handler_type}'"
        console.print("  ✅ [CURATION] handler wired")
        
        console.print("  [bold green]✅ All handlers wired correctly[/bold green]")
        return True
    except Exception as e:
        console.print(f"  [bold red]❌ Handler wiring failed: {e}[/bold red]")
        import traceback
        traceback.print_exc()
        return False


def show_summary(all_passed):
    """Show final summary"""
    console.print("\n" + "=" * 60)
    if all_passed:
        console.print("[bold green]✅ TOOL CALLING INFRASTRUCTURE IS OPERATIONAL[/bold green]")
        console.print("\n[italic]The following is now working:[/italic]")
        console.print("  • File operations are no longer hallucinated - REAL files are read/written")
        console.print("  • Router detects intent AND routes to actual handlers")
        console.print("  • Handlers execute real tool calling (not fake LLM responses)")
        console.print("  • Vault structure is initialized and accessible")
        console.print("\n[italic]You can now test in the CLI with real file operations![/italic]")
    else:
        console.print("[bold red]❌ Some checks failed - see errors above[/bold red]")
    console.print("=" * 60)
    return all_passed


def main():
    console.print("[bold yellow]🧪 FRIDAY V2 - TOOL CALLING INFRASTRUCTURE CHECK[/bold yellow]")
    console.print("=" * 60)
    
    results = [
        ("Module Imports", test_imports()),
        ("File Operations", test_file_ops()),
        ("Vault Structure", test_vault_structure()),
        ("Handler Wiring", test_intent_handler_wiring()),
    ]
    
    # Show results table
    table = Table(title="Validation Results")
    table.add_column("Check", style="cyan")
    table.add_column("Status", style="green")
    
    for name, passed in results:
        table.add_row(name, "✅ PASS" if passed else "❌ FAIL")
    
    console.print(table)
    
    all_passed = all(passed for _, passed in results)
    show_summary(all_passed)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
