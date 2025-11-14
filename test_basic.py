"""
Simple tests to verify NBA Analysis Tool functionality
Note: These tests do not make actual API calls to avoid network dependencies
"""

import sys
from nba_analysis import ShotChartAnalyzer, PlayerStatsAnalyzer, TeamStatsAnalyzer
from nba_api.stats.static import players, teams


def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    assert ShotChartAnalyzer is not None
    assert PlayerStatsAnalyzer is not None
    assert TeamStatsAnalyzer is not None
    print("✓ All imports successful")


def test_player_lookup():
    """Test player ID lookup functionality"""
    print("\nTesting player lookup...")
    analyzer = PlayerStatsAnalyzer()
    
    # Test valid player
    player_id = analyzer.get_player_id("LeBron James")
    assert player_id is not None
    assert player_id == 2544
    print(f"✓ LeBron James ID: {player_id}")
    
    # Test another valid player
    player_id = analyzer.get_player_id("Stephen Curry")
    assert player_id is not None
    print(f"✓ Stephen Curry ID: {player_id}")
    
    # Test invalid player
    player_id = analyzer.get_player_id("Not A Real Player")
    assert player_id is None
    print("✓ Invalid player returns None")


def test_team_lookup():
    """Test team ID lookup functionality"""
    print("\nTesting team lookup...")
    analyzer = TeamStatsAnalyzer()
    
    # Test valid team by full name
    team_id = analyzer.get_team_id("Los Angeles Lakers")
    assert team_id is not None
    assert team_id == 1610612747
    print(f"✓ Lakers ID: {team_id}")
    
    # Test valid team by abbreviation
    team_id = analyzer.get_team_id("LAL")
    assert team_id is not None
    print(f"✓ LAL abbreviation ID: {team_id}")
    
    # Test another team
    team_id = analyzer.get_team_id("Golden State Warriors")
    assert team_id is not None
    print(f"✓ Warriors ID: {team_id}")
    
    # Test invalid team
    team_id = analyzer.get_team_id("Not A Real Team")
    assert team_id is None
    print("✓ Invalid team returns None")


def test_shot_chart_analyzer():
    """Test ShotChartAnalyzer initialization and methods"""
    print("\nTesting ShotChartAnalyzer...")
    analyzer = ShotChartAnalyzer()
    
    # Test player lookup
    player_id = analyzer.get_player_id("Kevin Durant")
    assert player_id is not None
    print(f"✓ ShotChartAnalyzer player lookup works: KD ID = {player_id}")
    
    # Test team lookup
    team_id = analyzer.get_team_id("Phoenix Suns")
    assert team_id is not None
    print(f"✓ ShotChartAnalyzer team lookup works: Suns ID = {team_id}")


def test_static_data():
    """Test that NBA API static data is accessible"""
    print("\nTesting NBA API static data...")
    
    all_players = players.get_players()
    assert len(all_players) > 0
    print(f"✓ {len(all_players)} players in database")
    
    all_teams = teams.get_teams()
    assert len(all_teams) == 30
    print(f"✓ {len(all_teams)} teams in database")
    
    # Test finding players by full name
    lebron = players.find_players_by_full_name("LeBron James")
    assert len(lebron) > 0
    print(f"✓ Found LeBron James: {lebron[0]['full_name']}")


def test_class_initialization():
    """Test that all analyzer classes initialize correctly"""
    print("\nTesting class initialization...")
    
    shot_analyzer = ShotChartAnalyzer()
    assert shot_analyzer.shot_data is None
    print("✓ ShotChartAnalyzer initialized")
    
    player_analyzer = PlayerStatsAnalyzer()
    assert player_analyzer.player_id is None
    assert player_analyzer.career_stats is None
    assert player_analyzer.game_log is None
    print("✓ PlayerStatsAnalyzer initialized")
    
    team_analyzer = TeamStatsAnalyzer()
    assert team_analyzer.team_id is None
    assert team_analyzer.team_stats is None
    assert team_analyzer.game_log is None
    print("✓ TeamStatsAnalyzer initialized")


def main():
    """Run all tests"""
    print("=" * 60)
    print("NBA ANALYSIS TOOL - FUNCTIONALITY TESTS")
    print("=" * 60)
    
    try:
        test_imports()
        test_player_lookup()
        test_team_lookup()
        test_shot_chart_analyzer()
        test_static_data()
        test_class_initialization()
        
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
