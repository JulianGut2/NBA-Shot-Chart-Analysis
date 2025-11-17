"""
NBA Data Analysis Tool - Example Usage
Demonstrates the capabilities of the NBA analysis tool
"""

import matplotlib.pyplot as plt
from nba_analysis import ShotChartAnalyzer, PlayerStatsAnalyzer, TeamStatsAnalyzer


def demo_shot_chart():
    """Demonstrate shot chart functionality"""
    print("=" * 60)
    print("DEMO: Shot Chart Analysis")
    print("=" * 60)
    
    analyzer = ShotChartAnalyzer()
    
    # Example: LeBron James shot chart
    player_name = "LeBron James"
    print(f"\nFetching shot chart data for {player_name}...")
    
    try:
        # Fetch and plot shot chart
        fig = analyzer.plot_shot_chart(player_name, season='2023-24')
        plt.savefig('shot_chart_example.png', dpi=150, bbox_inches='tight')
        print(f"✓ Shot chart saved as 'shot_chart_example.png'")
        
        # Get shot statistics
        stats = analyzer.get_shot_statistics()
        print(f"\nShot Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value:.2f}" if isinstance(value, float) else f"  {key}: {value}")
        
        plt.close()
        
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print()


def demo_player_stats():
    """Demonstrate player statistics functionality"""
    print("=" * 60)
    print("DEMO: Player Statistics Analysis")
    print("=" * 60)
    
    analyzer = PlayerStatsAnalyzer()
    
    # Example: Stephen Curry statistics
    player_name = "Stephen Curry"
    print(f"\nAnalyzing {player_name}...")
    
    try:
        # Fetch career stats
        print("Fetching career statistics...")
        career_stats = analyzer.fetch_career_stats(player_name)
        print(f"✓ Career stats loaded ({len(career_stats)} seasons)")
        
        # Plot career progression
        fig = analyzer.plot_career_progression(stat_column='PTS')
        plt.savefig('career_progression_example.png', dpi=150, bbox_inches='tight')
        print(f"✓ Career progression chart saved as 'career_progression_example.png'")
        plt.close()
        
        # Fetch game log
        print("\nFetching season game log...")
        game_log = analyzer.fetch_game_log(player_name, season='2023-24')
        print(f"✓ Game log loaded ({len(game_log)} games)")
        
        # Plot season performance
        fig = analyzer.plot_season_performance(['PTS', 'AST', 'REB'])
        plt.savefig('season_performance_example.png', dpi=150, bbox_inches='tight')
        print(f"✓ Season performance chart saved as 'season_performance_example.png'")
        plt.close()
        
        # Plot shooting splits
        fig = analyzer.plot_shooting_splits()
        plt.savefig('shooting_splits_example.png', dpi=150, bbox_inches='tight')
        print(f"✓ Shooting splits chart saved as 'shooting_splits_example.png'")
        plt.close()
        
        # Get season averages
        print("\nSeason Averages:")
        averages = analyzer.get_season_averages()
        for key, value in averages.items():
            print(f"  {key}: {value:.2f}")
        
        # Create stats summary
        summary = analyzer.create_stats_summary()
        print("\nStats Summary:")
        print(summary.to_string(index=False))
        
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print()


def demo_team_stats():
    """Demonstrate team statistics functionality"""
    print("=" * 60)
    print("DEMO: Team Statistics Analysis")
    print("=" * 60)
    
    analyzer = TeamStatsAnalyzer()
    
    try:
        # Fetch league standings
        print("\nFetching league standings...")
        standings = analyzer.fetch_league_standings(season='2023-24')
        print(f"✓ League standings loaded ({len(standings)} teams)")
        
        # Plot league leaders
        fig = analyzer.plot_league_leaders(stat_column='PTS', top_n=10)
        plt.savefig('league_leaders_example.png', dpi=150, bbox_inches='tight')
        print(f"✓ League leaders chart saved as 'league_leaders_example.png'")
        plt.close()
        
        # Analyze specific team
        team_name = "Golden State Warriors"
        print(f"\nAnalyzing {team_name}...")
        
        # Fetch team game log
        game_log = analyzer.fetch_team_game_log(team_name, season='2023-24')
        print(f"✓ Team game log loaded ({len(game_log)} games)")
        
        # Plot team performance
        fig = analyzer.plot_team_performance(['PTS', 'AST', 'REB'])
        plt.savefig('team_performance_example.png', dpi=150, bbox_inches='tight')
        print(f"✓ Team performance chart saved as 'team_performance_example.png'")
        plt.close()
        
        # Plot win/loss record
        fig = analyzer.plot_win_loss_record()
        plt.savefig('win_loss_record_example.png', dpi=150, bbox_inches='tight')
        print(f"✓ Win/loss record chart saved as 'win_loss_record_example.png'")
        plt.close()
        
        # Get team summary
        summary = analyzer.get_team_summary()
        print(f"\n{team_name} Season Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value:.2f}" if isinstance(value, float) else f"  {key}: {value}")
        
        # Compare teams
        print("\nComparing multiple teams...")
        analyzer.fetch_league_standings(season='2023-24')
        teams_to_compare = ["Golden State Warriors", "Los Angeles Lakers", "Boston Celtics"]
        fig = analyzer.compare_teams(teams_to_compare, ['PTS', 'AST', 'REB'])
        plt.savefig('team_comparison_example.png', dpi=150, bbox_inches='tight')
        print(f"✓ Team comparison chart saved as 'team_comparison_example.png'")
        plt.close()
        
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print()


def main():
    """Run all demonstrations"""
    print("\n" + "=" * 60)
    print("NBA DATA ANALYSIS TOOL - DEMONSTRATION")
    print("=" * 60)
    print("\nThis script demonstrates the capabilities of the NBA analysis tool.")
    print("It will generate several visualizations and statistics.\n")
    
    # Run demonstrations
    demo_shot_chart()
    demo_player_stats()
    demo_team_stats()
    
    print("=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - shot_chart_example.png")
    print("  - career_progression_example.png")
    print("  - season_performance_example.png")
    print("  - shooting_splits_example.png")
    print("  - league_leaders_example.png")
    print("  - team_performance_example.png")
    print("  - win_loss_record_example.png")
    print("  - team_comparison_example.png")
    print("\nCheck these files to see the visualizations!")
    print()


if __name__ == "__main__":
    main()
