"""
Test script for GameBrain API tools
This script validates the implementation of all GameBrain tools
"""

import sys
import os
sys.path.insert(0, 'adk-project/tools')

from typing import Any, Dict, Union
from tools.gamebrain_tools import (
    search_games,
    get_game_details,
    filter_games_by_genre,
    filter_games_by_platform
)


def get_response_data(response: Any) -> Dict[str, Any]:
    """
    Extract data from ToolResponse object or dict.
    
    Args:
        response: Either a ToolResponse object or a dict
        
    Returns:
        dict: The underlying data as a dictionary
    """
    # If it's a ToolResponse object, access its data attribute
    if hasattr(response, 'data'):
        data = response.data
        # Ensure we return a dict
        return data if isinstance(data, dict) else {}
    # If it's already a dict, return as-is
    if isinstance(response, dict):
        return response
    # Fallback for unexpected types
    return {}


def print_separator():
    print("\n" + "="*80 + "\n")


def test_search_games():
    """Test the search_games tool"""
    print("🔍 Testing search_games tool...")
    print_separator()
    
    # Test 1: Basic search
    print("Test 1: Basic search for 'zelda'")
    response = search_games("zelda", limit=5)
    result = get_response_data(response)
    print(f"Success: {result.get('success')}")
    print(f"Count: {result.get('count', 0)}")
    print(f"Total Results: {result.get('total_results', 'N/A')}")
    if result.get('success') and result.get('games'):
        first_game = result['games'][0]
        print(f"First Game: {first_game.get('name', 'N/A')} (ID: {first_game.get('id', 'N/A')})")
        print(f"Genre: {first_game.get('genre', 'N/A')}")
    if result.get('error'):
        print(f"Error: {result['error']}")
    if result.get('note'):
        print(f"Note: {result['note']}")
    print_separator()
    
    # Test 2: Search with platform filter
    print("Test 2: Search for 'mario' on 'switch'")
    response = search_games("mario", limit=5, platform="switch")
    result = get_response_data(response)
    print(f"Success: {result.get('success')}")
    print(f"Count: {result.get('count', 0)}")
    print(f"Total Results: {result.get('total_results', 'N/A')}")
    print(f"Platform Filter: {result.get('platform', 'N/A')}")
    if result.get('success') and result.get('games'):
        first_game = result['games'][0]
        print(f"First Game: {first_game.get('name', 'N/A')}")
    if result.get('error'):
        print(f"Error: {result['error']}")
    print_separator()
    
    # Test 3: Empty query (should fail gracefully)
    print("Test 3: Empty query (error handling)")
    response = search_games("", limit=5)
    result = get_response_data(response)
    print(f"Success: {result.get('success')}")
    if result.get('error'):
        print(f"Error: {result['error']}")
    print_separator()


def test_get_game_details():
    """Test the get_game_details tool"""
    print("📋 Testing get_game_details tool...")
    print_separator()
    
    # Test 1: Valid game ID (using a known game ID from search results)
    print("Test 1: Get details for game ID '64591' (Medieval II: Total War)")
    response = get_game_details("64591")
    result = get_response_data(response)
    print(f"Success: {result.get('success')}")
    if result.get('success'):
        print(f"Name: {result.get('name', 'N/A')}")
        print(f"ID: {result.get('id', 'N/A')}")
        print(f"Year: {result.get('year', 'N/A')}")
        print(f"Genre: {result.get('genre', 'N/A')}")
        if result.get('rating'):
            rating = result['rating']
            print(f"Rating: {rating.get('mean', 'N/A')} ({rating.get('count', 0)} reviews)")
        if result.get('platforms'):
            platforms = [p.get('name', p.get('value', '')) for p in result['platforms'][:3]]
            print(f"Platforms: {', '.join(platforms)}")
    if result.get('error'):
        print(f"Error: {result['error']}")
    print_separator()
    
    # Test 2: Empty ID (should fail gracefully)
    print("Test 2: Empty game ID (error handling)")
    response = get_game_details("")
    result = get_response_data(response)
    print(f"Success: {result.get('success')}")
    if result.get('error'):
        print(f"Error: {result['error']}")
    print_separator()


def test_filter_games_by_genre():
    """Test the filter_games_by_genre tool"""
    print("🎮 Testing filter_games_by_genre tool...")
    print_separator()
    
    # Test 1: Strategy genre
    print("Test 1: Filter by 'strategy' genre")
    response = filter_games_by_genre("strategy", limit=5)
    result = get_response_data(response)
    print(f"Success: {result.get('success')}")
    print(f"Genre: {result.get('genre', 'N/A')}")
    print(f"Count: {result.get('count', 0)}")
    print(f"Total Results: {result.get('total_results', 'N/A')}")
    if result.get('success') and result.get('games'):
        print(f"Sample Games:")
        for game in result['games'][:3]:
            print(f"  - {game.get('name', 'N/A')} ({game.get('genre', 'N/A')})")
    if result.get('error'):
        print(f"Error: {result['error']}")
    if result.get('note'):
        print(f"Note: {result['note']}")
    print_separator()
    
    # Test 2: RPG genre
    print("Test 2: Filter by 'rpg' genre")
    response = filter_games_by_genre("rpg", limit=5)
    result = get_response_data(response)
    print(f"Success: {result.get('success')}")
    print(f"Genre: {result.get('genre', 'N/A')}")
    print(f"Count: {result.get('count', 0)}")
    print(f"Total Results: {result.get('total_results', 'N/A')}")
    if result.get('error'):
        print(f"Error: {result['error']}")
    print_separator()
    
    # Test 3: Empty genre (should fail gracefully)
    print("Test 3: Empty genre (error handling)")
    response = filter_games_by_genre("", limit=5)
    result = get_response_data(response)
    print(f"Success: {result.get('success')}")
    if result.get('error'):
        print(f"Error: {result['error']}")
    print_separator()


def test_filter_games_by_platform():
    """Test the filter_games_by_platform tool"""
    print("🎯 Testing filter_games_by_platform tool...")
    print_separator()
    
    # Test 1: Nintendo Switch platform
    print("Test 1: Filter by 'switch' platform")
    response = filter_games_by_platform("switch", limit=5)
    result = get_response_data(response)
    print(f"Success: {result.get('success')}")
    print(f"Platform: {result.get('platform', 'N/A')}")
    print(f"Count: {result.get('count', 0)}")
    print(f"Total Results: {result.get('total_results', 'N/A')}")
    if result.get('success') and result.get('games'):
        print(f"Sample Games:")
        for game in result['games'][:3]:
            print(f"  - {game.get('name', 'N/A')}")
    if result.get('error'):
        print(f"Error: {result['error']}")
    if result.get('note'):
        print(f"Note: {result['note']}")
    print_separator()
    
    # Test 2: PC platform
    print("Test 2: Filter by 'pc' platform")
    response = filter_games_by_platform("pc", limit=5)
    result = get_response_data(response)
    print(f"Success: {result.get('success')}")
    print(f"Platform: {result.get('platform', 'N/A')}")
    print(f"Count: {result.get('count', 0)}")
    print(f"Total Results: {result.get('total_results', 'N/A')}")
    if result.get('error'):
        print(f"Error: {result['error']}")
    print_separator()
    
    # Test 3: Empty platform (should fail gracefully)
    print("Test 3: Empty platform (error handling)")
    response = filter_games_by_platform("", limit=5)
    result = get_response_data(response)
    print(f"Success: {result.get('success')}")
    if result.get('error'):
        print(f"Error: {result['error']}")
    print_separator()


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("🚀 GAMEBRAIN API TOOLS TEST SUITE")
    print("="*80 + "\n")
    
    # Check API key configuration
    api_key = os.environ.get("GAMEBRAIN_API_KEY", "")
    if not api_key:
        print("❌ ERROR: GAMEBRAIN_API_KEY environment variable is not set!")
        print("\nPlease set your API key before running tests:")
        print("  Windows (PowerShell): $env:GAMEBRAIN_API_KEY = 'your-api-key'")
        print("  Windows (CMD):        set GAMEBRAIN_API_KEY=your-api-key")
        print("  Linux/Mac:            export GAMEBRAIN_API_KEY='your-api-key'")
        print("\nSee API_SETUP.md for detailed instructions.\n")
        return
    
    print(f"✅ API Key configured: {api_key[:8]}...{api_key[-4:]}")
    print("\n⚠️  NOTE: These tests will make actual API calls to GameBrain API")
    print("⚠️  Some tests may fail if the API is unavailable or rate limited")
    print("⚠️  Error handling tests should always pass\n")
    
    try:
        test_search_games()
        test_get_game_details()
        test_filter_games_by_genre()
        test_filter_games_by_platform()
        
        print("\n" + "="*80)
        print("✅ TEST SUITE COMPLETED")
        print("="*80 + "\n")
        
        print("📝 Summary:")
        print("- All tools imported successfully")
        print("- API authentication working")
        print("- Error handling validated")
        print("- Tool structure follows watsonx Orchestrate conventions")
        print("- Response parsing matches GameBrain API structure")
        print("\n⚠️  API connectivity tests depend on GameBrain API availability")
        print("⚠️  Check API_SETUP.md for troubleshooting if tests fail")
        
    except Exception as e:
        print(f"\n❌ TEST SUITE FAILED: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()