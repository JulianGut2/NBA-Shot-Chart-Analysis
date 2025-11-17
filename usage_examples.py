"""
NBA Analysis Tool - Usage Examples
This file contains practical examples of how to use the NBA Analysis Tool
"""

# Example 1: Analyzing a player's shot chart
def example_shot_chart():
    from nba_analysis import ShotChartAnalyzer
    import matplotlib.pyplot as plt
    
    analyzer = ShotChartAnalyzer()
    
    # Create shot chart for a player
    fig = analyzer.plot_shot_chart("LeBron James", season='2023-24')
    plt.savefig('lebron_shots.png')
    
    # Get shooting statistics
    stats = analyzer.get_shot_statistics()
    print(f"Total Shots: {stats['total_shots']}")
    print(f"FG%: {stats['fg_percentage']:.1f}%")


# Example 2: Analyzing player career progression
def example_player_career():
    from nba_analysis import PlayerStatsAnalyzer
    import matplotlib.pyplot as plt
    
    analyzer = PlayerStatsAnalyzer()
    
    # Fetch career stats
    career_stats = analyzer.fetch_career_stats("Stephen Curry")
    
    # Plot points per game over career
    fig = analyzer.plot_career_progression(stat_column='PTS')
    plt.savefig('curry_career.png')
    
    # Get season averages
    analyzer.fetch_game_log("Stephen Curry", season='2023-24')
    averages = analyzer.get_season_averages()
    print(f"PPG: {averages['PTS']:.1f}")
    print(f"APG: {averages['AST']:.1f}")
    print(f"RPG: {averages['REB']:.1f}")


# Example 3: Comparing multiple players
def example_player_comparison():
    from nba_analysis import PlayerStatsAnalyzer
    import pandas as pd
    
    players = ["LeBron James", "Kevin Durant", "Stephen Curry"]
    stats_list = []
    
    for player in players:
        analyzer = PlayerStatsAnalyzer()
        analyzer.fetch_game_log(player, season='2023-24')
        averages = analyzer.get_season_averages()
        averages['Player'] = player
        stats_list.append(averages)
    
    comparison_df = pd.DataFrame(stats_list)
    print(comparison_df[['Player', 'PTS', 'AST', 'REB']])


# Example 4: Team analysis
def example_team_analysis():
    from nba_analysis import TeamStatsAnalyzer
    import matplotlib.pyplot as plt
    
    analyzer = TeamStatsAnalyzer()
    
    # Get league standings
    standings = analyzer.fetch_league_standings(season='2023-24')
    
    # Plot top scorers
    fig = analyzer.plot_league_leaders(stat_column='PTS', top_n=10)
    plt.savefig('top_scoring_teams.png')
    
    # Analyze specific team
    analyzer.fetch_team_game_log("Los Angeles Lakers", season='2023-24')
    summary = analyzer.get_team_summary()
    print(f"Record: {summary['wins']}-{summary['losses']}")
    print(f"Win%: {summary['win_percentage']:.1f}%")
    print(f"PPG: {summary['ppg']:.1f}")


# Example 5: Team comparison
def example_team_comparison():
    from nba_analysis import TeamStatsAnalyzer
    import matplotlib.pyplot as plt
    
    analyzer = TeamStatsAnalyzer()
    analyzer.fetch_league_standings(season='2023-24')
    
    # Compare multiple teams
    teams = ["Los Angeles Lakers", "Boston Celtics", "Golden State Warriors"]
    fig = analyzer.compare_teams(teams, ['PTS', 'AST', 'REB', 'FG_PCT'])
    plt.savefig('team_comparison.png')


if __name__ == "__main__":
    print("NBA Analysis Tool - Usage Examples")
    print("=" * 50)
    print("\nNote: These examples require internet access to fetch")
    print("data from the NBA API. Uncomment and run individual")
    print("examples as needed.")
    print("\nAvailable examples:")
    print("  1. example_shot_chart() - Shot chart analysis")
    print("  2. example_player_career() - Career progression")
    print("  3. example_player_comparison() - Compare players")
    print("  4. example_team_analysis() - Team statistics")
    print("  5. example_team_comparison() - Compare teams")
