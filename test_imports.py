#!/usr/bin/env python3
"""
Test script to verify all imports and basic functionality
"""

print("Testing rev2 imports...")

print("\n1. Testing config...")
try:
    from config import ModelConfig, APIConfig, verify_setup
    print("   ✓ Config imports successful")
except Exception as e:
    print(f"   ✗ Config import failed: {e}")
    exit(1)

print("\n2. Testing tools...")
try:
    from tools import (
        get_stock_price,
        get_historical_prices,
        calculate_indicators,
        analyze_market_sentiment,
    )
    print("   ✓ Tools imports successful")
except Exception as e:
    print(f"   ✗ Tools import failed: {e}")
    exit(1)

print("\n3. Testing agents...")
try:
    from agents import (
        create_data_fetcher_agent,
        create_market_analyst_agent,
        create_sentiment_agent,
        create_risk_manager_agent,
        create_portfolio_strategist_agent,
    )
    print("   ✓ Agents imports successful")
except Exception as e:
    print(f"   ✗ Agents import failed: {e}")
    exit(1)

print("\n4. Testing crew...")
try:
    from crews import PortfolioAnalysisCrew
    print("   ✓ Crew imports successful")
except Exception as e:
    print(f"   ✗ Crew import failed: {e}")
    exit(1)

print("\n5. Testing agent initialization...")
try:
    data_agent = create_data_fetcher_agent()
    analyst_agent = create_market_analyst_agent()
    sentiment_agent = create_sentiment_agent()
    risk_agent = create_risk_manager_agent()
    strategist_agent = create_portfolio_strategist_agent()
    print("   ✓ All agents initialized successfully")
except Exception as e:
    print(f"   ✗ Agent initialization failed: {e}")
    exit(1)

print("\n6. Testing crew initialization...")
try:
    crew = PortfolioAnalysisCrew(verbose=False)
    print("   ✓ Crew initialized successfully")
except Exception as e:
    print(f"   ✗ Crew initialization failed: {e}")
    exit(1)

print("\n7. Testing tool execution (get_stock_price)...")
try:
    result = get_stock_price("AAPL")
    if "error" in result:
        print(f"   ⚠ Tool executed but returned error: {result['error']}")
    elif "current_price" in result:
        print(f"   ✓ Tool executed successfully (AAPL price: ${result['current_price']:.2f})")
    else:
        print(f"   ⚠ Tool executed but unexpected result: {result}")
except Exception as e:
    print(f"   ✗ Tool execution failed: {e}")

print("\n" + "=" * 60)
print("All import tests passed! ✅")
print("=" * 60)
print("\nSystem is ready to use!")
print("\nQuick start:")
print("  - Run CLI: python main.py")
print("  - Run API: python api/server.py")
print("  - View docs: See README.md")
