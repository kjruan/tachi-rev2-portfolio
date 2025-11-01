#!/usr/bin/env python3
"""
Rev2 Portfolio Management CLI
Main interface for multi-agent portfolio analysis
"""

import sys
from typing import Dict
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

from config import verify_setup
from crews.portfolio_crew import PortfolioAnalysisCrew


console = Console()


def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║         Rev2 - AI Portfolio Management System            ║
    ║         Powered by Claude AI & Multi-Agent CrewAI        ║
    ╚══════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


def print_menu():
    """Print main menu"""
    table = Table(title="Main Menu", show_header=True, header_style="bold magenta")
    table.add_column("Option", style="cyan", width=8)
    table.add_column("Action", style="green")

    table.add_row("1", "Analyze Portfolio (Multiple Stocks)")
    table.add_row("2", "Quick Stock Analysis (Single Stock)")
    table.add_row("3", "Example: Analyze Tech Portfolio")
    table.add_row("4", "Example: Analyze Single Stock (AAPL)")
    table.add_row("5", "Configuration Check")
    table.add_row("q", "Quit")

    console.print(table)


def get_portfolio_input() -> Dict[str, float]:
    """Get portfolio input from user"""
    console.print("\n[bold]Enter your portfolio:[/bold]", style="yellow")
    console.print("Format: TICKER:SHARES (e.g., AAPL:10)")
    console.print("Enter 'done' when finished\n")

    portfolio = {}

    while True:
        entry = input("Stock (TICKER:SHARES) or 'done': ").strip()

        if entry.lower() == "done":
            break

        try:
            ticker, shares = entry.split(":")
            ticker = ticker.upper().strip()
            shares = float(shares.strip())

            if shares <= 0:
                console.print("[red]Error: Shares must be positive[/red]")
                continue

            portfolio[ticker] = shares
            console.print(f"[green]Added {ticker}: {shares} shares[/green]")

        except ValueError:
            console.print("[red]Error: Invalid format. Use TICKER:SHARES[/red]")

    return portfolio


def analyze_portfolio(crew: PortfolioAnalysisCrew):
    """Analyze a portfolio"""
    portfolio = get_portfolio_input()

    if not portfolio:
        console.print("[red]No portfolio entered![/red]")
        return

    console.print(f"\n[bold green]Analyzing portfolio with {len(portfolio)} positions...[/bold green]\n")

    try:
        with console.status("[bold green]Running multi-agent analysis...", spinner="dots"):
            result = crew.analyze_portfolio(portfolio)

        # Display results
        console.print("\n" + "=" * 80)
        console.print(Panel(result["analysis"], title="Portfolio Analysis Results", border_style="green"))
        console.print("=" * 80 + "\n")

    except Exception as e:
        console.print(f"[red]Error during analysis: {e}[/red]")


def quick_stock_analysis(crew: PortfolioAnalysisCrew):
    """Quick analysis of a single stock"""
    ticker = input("\nEnter stock ticker: ").strip().upper()

    if not ticker:
        console.print("[red]No ticker entered![/red]")
        return

    console.print(f"\n[bold green]Analyzing {ticker}...[/bold green]\n")

    try:
        with console.status(f"[bold green]Analyzing {ticker}...", spinner="dots"):
            result = crew.quick_analysis(ticker)

        # Display results
        console.print("\n" + "=" * 80)
        console.print(Panel(result["analysis"], title=f"{ticker} Analysis", border_style="blue"))
        console.print("=" * 80 + "\n")

    except Exception as e:
        console.print(f"[red]Error during analysis: {e}[/red]")


def example_tech_portfolio(crew: PortfolioAnalysisCrew):
    """Run example analysis on a tech portfolio"""
    portfolio = {
        "AAPL": 10,
        "MSFT": 15,
        "GOOGL": 5,
        "NVDA": 8,
    }

    console.print("\n[bold]Example Tech Portfolio:[/bold]")
    for ticker, shares in portfolio.items():
        console.print(f"  {ticker}: {shares} shares")

    console.print(f"\n[bold green]Analyzing portfolio...[/bold green]\n")

    try:
        with console.status("[bold green]Running multi-agent analysis...", spinner="dots"):
            result = crew.analyze_portfolio(portfolio)

        console.print("\n" + "=" * 80)
        console.print(Panel(result["analysis"], title="Tech Portfolio Analysis", border_style="green"))
        console.print("=" * 80 + "\n")

    except Exception as e:
        console.print(f"[red]Error during analysis: {e}[/red]")


def example_single_stock(crew: PortfolioAnalysisCrew):
    """Run example analysis on Apple stock"""
    ticker = "AAPL"

    console.print(f"\n[bold]Example: Analyzing {ticker}[/bold]\n")

    try:
        with console.status(f"[bold green]Analyzing {ticker}...", spinner="dots"):
            result = crew.quick_analysis(ticker)

        console.print("\n" + "=" * 80)
        console.print(Panel(result["analysis"], title=f"{ticker} Analysis", border_style="blue"))
        console.print("=" * 80 + "\n")

    except Exception as e:
        console.print(f"[red]Error during analysis: {e}[/red]")


def check_configuration():
    """Check system configuration"""
    console.print("\n[bold]Checking configuration...[/bold]\n")

    if verify_setup():
        console.print("[green]✓ Configuration is valid![/green]")
        console.print("\n[bold]System Ready:[/bold]")
        console.print("  - Claude API configured")
        console.print("  - All agents initialized")
        console.print("  - Tools available")
    else:
        console.print("[red]✗ Configuration failed![/red]")
        console.print("\nPlease check your .env file and ensure ANTHROPIC_API_KEY is set.")


def main():
    """Main application loop"""
    print_banner()

    # Verify setup
    console.print("[bold]Verifying configuration...[/bold]")
    if not verify_setup():
        console.print("\n[red]Configuration error! Please fix before continuing.[/red]")
        console.print("Check your .env file and ensure ANTHROPIC_API_KEY is set.")
        sys.exit(1)

    console.print("[green]✓ Configuration verified![/green]\n")

    # Initialize crew
    console.print("[bold]Initializing AI agents...[/bold]")
    try:
        crew = PortfolioAnalysisCrew(verbose=False)
        console.print("[green]✓ Agents ready![/green]\n")
    except Exception as e:
        console.print(f"[red]Failed to initialize agents: {e}[/red]")
        sys.exit(1)

    # Main loop
    while True:
        print_menu()

        choice = input("\nSelect an option: ").strip().lower()

        if choice == "1":
            analyze_portfolio(crew)
        elif choice == "2":
            quick_stock_analysis(crew)
        elif choice == "3":
            example_tech_portfolio(crew)
        elif choice == "4":
            example_single_stock(crew)
        elif choice == "5":
            check_configuration()
        elif choice == "q":
            console.print("\n[cyan]Thank you for using Rev2! Goodbye.[/cyan]\n")
            break
        else:
            console.print("[red]Invalid option. Please try again.[/red]")

        input("\nPress Enter to continue...")
        console.clear()
        print_banner()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted by user. Exiting...[/yellow]\n")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Unexpected error: {e}[/red]\n")
        sys.exit(1)
