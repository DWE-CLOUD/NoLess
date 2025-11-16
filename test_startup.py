#!/usr/bin/env python3
"""
Quick test script to demonstrate the NoLess startup sequence
"""

import sys
import os

# Add the noless package to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from noless.startup import show_startup_sequence, show_quick_startup, show_service_status
from rich.console import Console
from rich.panel import Panel

console = Console()

def test_full_startup():
    """Test the full startup sequence"""
    console.print("\n[bold cyan]Testing Full Startup Sequence[/bold cyan]\n")
    show_startup_sequence()

def test_quick_startup():
    """Test the quick startup"""
    console.print("\n[bold cyan]Testing Quick Startup[/bold cyan]\n")
    show_quick_startup()

def test_service_status():
    """Test the service status check"""
    show_service_status()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test NoLess startup sequences")
    parser.add_argument("--mode", choices=["full", "quick", "status"], default="full",
                      help="Startup mode to test (default: full)")

    args = parser.parse_args()

    console.print(Panel.fit(
        "[bold white]NoLess Startup Sequence Test[/bold white]\n\n"
        "This script demonstrates the startup sequences:\n"
        "• [cyan]full[/cyan] - Complete startup with all animations\n"
        "• [cyan]quick[/cyan] - Fast startup for non-interactive mode\n"
        "• [cyan]status[/cyan] - Service status check only\n\n"
        "[dim]Use --mode to choose which test to run[/dim]",
        title="[bold cyan]🧪 Test Script[/bold cyan]",
        border_style="cyan"
    ))

    console.print()

    if args.mode == "full":
        test_full_startup()
    elif args.mode == "quick":
        test_quick_startup()
    elif args.mode == "status":
        test_service_status()

    console.print("\n[bold green]✓ Test complete![/bold green]\n")
