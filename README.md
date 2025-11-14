# NBA Shot Chart Analysis

A comprehensive data analysis tool to visualize and explore NBA statistics using the `nba_api`. This tool provides powerful capabilities for analyzing player performance, team statistics, and shot charts.

## Features

### 📊 Shot Chart Analysis
- Visualize player shot charts with made/missed shots
- Draw accurate NBA court diagrams
- Calculate shooting percentages by zone
- Support for multiple seasons and playoffs

### 👤 Player Statistics Analysis
- Career progression tracking
- Season-by-season performance analysis
- Game-by-game statistics visualization
- Shooting splits (FG%, 3P%, FT%)
- Comprehensive season averages

### 🏀 Team Statistics Analysis
- League-wide standings and rankings
- Team performance tracking
- Win/loss record visualization
- Team comparison tools
- Season summary statistics

## Installation

1. Clone the repository:
```bash
git clone https://github.com/JulianGut2/NBA-Shot-Chart-Analysis.git
cd NBA-Shot-Chart-Analysis
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Run the example script to see all features in action:
```bash
python example.py
```

This will generate sample visualizations and statistics for demonstration.

### Shot Chart Analysis

```python
from nba_analysis import ShotChartAnalyzer

# Create analyzer
analyzer = ShotChartAnalyzer()

# Plot shot chart for a player
fig = analyzer.plot_shot_chart("LeBron James", season='2023-24')
plt.show()

# Get shot statistics
stats = analyzer.get_shot_statistics()
print(stats)
```

### Player Statistics Analysis

```python
from nba_analysis import PlayerStatsAnalyzer

# Create analyzer
analyzer = PlayerStatsAnalyzer()

# Fetch and analyze player data
analyzer.fetch_career_stats("Stephen Curry")
analyzer.plot_career_progression(stat_column='PTS')

# Get season game log
analyzer.fetch_game_log("Stephen Curry", season='2023-24')
analyzer.plot_season_performance(['PTS', 'AST', 'REB'])

# Get season averages
averages = analyzer.get_season_averages()
print(averages)
```

### Team Statistics Analysis

```python
from nba_analysis import TeamStatsAnalyzer

# Create analyzer
analyzer = TeamStatsAnalyzer()

# Fetch league standings
analyzer.fetch_league_standings(season='2023-24')
analyzer.plot_league_leaders(stat_column='PTS', top_n=10)

# Analyze specific team
analyzer.fetch_team_game_log("Golden State Warriors", season='2023-24')
analyzer.plot_team_performance(['PTS', 'AST', 'REB'])

# Compare teams
teams = ["Golden State Warriors", "Los Angeles Lakers", "Boston Celtics"]
analyzer.compare_teams(teams, ['PTS', 'AST', 'REB'])
```

## API Reference

### ShotChartAnalyzer

- `get_player_id(player_name)` - Get NBA player ID
- `fetch_shot_data(player_name, season, season_type)` - Fetch shot chart data
- `plot_shot_chart(player_name, season, season_type)` - Create shot chart visualization
- `get_shot_statistics()` - Calculate shooting statistics
- `draw_court(ax)` - Draw NBA court on matplotlib axis

### PlayerStatsAnalyzer

- `get_player_id(player_name)` - Get NBA player ID
- `fetch_player_info(player_name)` - Fetch basic player information
- `fetch_career_stats(player_name, per_mode)` - Fetch career statistics
- `fetch_game_log(player_name, season, season_type)` - Fetch game log
- `plot_career_progression(stat_column)` - Plot career stat progression
- `plot_season_performance(stat_columns)` - Plot season performance
- `plot_shooting_splits()` - Plot shooting percentages
- `get_season_averages()` - Calculate season averages
- `create_stats_summary()` - Create comprehensive stats summary

### TeamStatsAnalyzer

- `get_team_id(team_name)` - Get NBA team ID
- `fetch_league_standings(season, season_type)` - Fetch league standings
- `fetch_team_game_log(team_name, season, season_type)` - Fetch team game log
- `plot_league_leaders(stat_column, top_n)` - Plot top teams
- `plot_team_performance(stat_columns)` - Plot team performance
- `plot_win_loss_record()` - Plot win/loss progression
- `get_team_summary()` - Get team season summary
- `compare_teams(team_names, stat_columns)` - Compare multiple teams

## Requirements

- Python 3.7+
- nba_api >= 1.4.1
- pandas >= 2.0.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- numpy >= 1.24.0
- plotly >= 5.14.0

## Examples

The repository includes `example.py` which demonstrates:
- Shot chart visualization
- Career progression analysis
- Season performance tracking
- Shooting splits analysis
- League leaders comparison
- Team performance analysis
- Win/loss record tracking
- Multi-team comparison

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with [nba_api](https://github.com/swar/nba_api) for accessing NBA statistics
- Uses official NBA stats API data
