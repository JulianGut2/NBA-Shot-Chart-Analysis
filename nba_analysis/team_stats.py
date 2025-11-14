"""
Team Statistics Analyzer Module
Provides functionality to analyze and visualize team statistics
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nba_api.stats.endpoints import leaguedashteamstats, teamgamelog, teamyearbyyearstats
from nba_api.stats.static import teams


class TeamStatsAnalyzer:
    """
    Analyzes and visualizes NBA team statistics
    """
    
    def __init__(self):
        """Initialize the Team Stats Analyzer"""
        self.team_id = None
        self.team_name = None
        self.team_stats = None
        self.game_log = None
        
    def get_team_id(self, team_name):
        """
        Get team ID from team name or abbreviation
        
        Args:
            team_name (str): Name or abbreviation of the team
            
        Returns:
            int: Team ID or None if not found
        """
        # Try full name first
        team_dict = teams.find_teams_by_full_name(team_name)
        if team_dict:
            return team_dict[0]['id']
        
        # Try abbreviation
        team_dict = teams.find_team_by_abbreviation(team_name)
        if team_dict:
            return team_dict['id']
        
        return None
    
    def fetch_league_standings(self, season='2023-24', season_type='Regular Season'):
        """
        Fetch league-wide team statistics (standings)
        
        Args:
            season (str): NBA season (e.g., '2023-24')
            season_type (str): Type of season ('Regular Season', 'Playoffs')
            
        Returns:
            pandas.DataFrame: League standings data
        """
        league_stats = leaguedashteamstats.LeagueDashTeamStats(
            season=season,
            season_type_all_star=season_type,
            per_mode_detailed='PerGame'
        )
        
        self.team_stats = league_stats.get_data_frames()[0]
        return self.team_stats
    
    def fetch_team_game_log(self, team_name, season='2023-24', season_type='Regular Season'):
        """
        Fetch game log for a team's season
        
        Args:
            team_name (str): Name or abbreviation of the team
            season (str): NBA season (e.g., '2023-24')
            season_type (str): Type of season ('Regular Season', 'Playoffs')
            
        Returns:
            pandas.DataFrame: Game log data
        """
        self.team_id = self.get_team_id(team_name)
        self.team_name = team_name
        
        if self.team_id is None:
            raise ValueError(f"Team '{team_name}' not found")
        
        gamelog = teamgamelog.TeamGameLog(
            team_id=self.team_id,
            season=season,
            season_type_all_star=season_type
        )
        
        self.game_log = gamelog.get_data_frames()[0]
        return self.game_log
    
    def plot_league_leaders(self, stat_column='PTS', top_n=10, figsize=(12, 8)):
        """
        Plot top teams for a specific statistic
        
        Args:
            stat_column (str): Statistic to rank by (e.g., 'PTS', 'AST', 'REB')
            top_n (int): Number of top teams to show
            figsize (tuple): Figure size
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        if self.team_stats is None or len(self.team_stats) == 0:
            raise ValueError("No team stats loaded. Call fetch_league_standings first.")
        
        # Sort and get top N teams
        top_teams = self.team_stats.nlargest(top_n, stat_column)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create horizontal bar chart
        y_pos = range(len(top_teams))
        bars = ax.barh(y_pos, top_teams[stat_column], color='#1f77b4', 
                       edgecolor='black', linewidth=1.5)
        
        # Customize the plot
        ax.set_yticks(y_pos)
        ax.set_yticklabels(top_teams['TEAM_NAME'])
        ax.invert_yaxis()  # Highest value at the top
        ax.set_xlabel(stat_column, fontsize=12)
        ax.set_title(f'Top {top_n} Teams - {stat_column}', 
                     fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f'{width:.1f}',
                   ha='left', va='center', fontweight='bold', fontsize=10)
        
        plt.tight_layout()
        return fig
    
    def plot_team_performance(self, stat_columns=['PTS', 'AST', 'REB'], figsize=(14, 6)):
        """
        Plot game-by-game team performance
        
        Args:
            stat_columns (list): List of statistics to plot
            figsize (tuple): Figure size
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        if self.game_log is None or len(self.game_log) == 0:
            raise ValueError("No game log loaded. Call fetch_team_game_log first.")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Reverse the game log to show chronological order
        game_log = self.game_log.iloc[::-1].reset_index(drop=True)
        
        for stat in stat_columns:
            if stat in game_log.columns:
                ax.plot(game_log.index, game_log[stat], marker='o', 
                       label=stat, linewidth=1.5, markersize=4, alpha=0.7)
        
        ax.set_xlabel('Game Number', fontsize=12)
        ax.set_ylabel('Statistics', fontsize=12)
        ax.set_title(f'{self.team_name} Season Performance', 
                     fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_win_loss_record(self, figsize=(10, 6)):
        """
        Plot win/loss record over the season
        
        Args:
            figsize (tuple): Figure size
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        if self.game_log is None or len(self.game_log) == 0:
            raise ValueError("No game log loaded. Call fetch_team_game_log first.")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Reverse the game log to show chronological order
        game_log = self.game_log.iloc[::-1].reset_index(drop=True)
        
        # Calculate cumulative wins
        game_log['IS_WIN'] = game_log['WL'].apply(lambda x: 1 if x == 'W' else 0)
        game_log['CUMULATIVE_WINS'] = game_log['IS_WIN'].cumsum()
        game_log['CUMULATIVE_LOSSES'] = (1 - game_log['IS_WIN']).cumsum()
        
        # Plot cumulative wins and losses
        ax.plot(game_log.index, game_log['CUMULATIVE_WINS'], 
               marker='o', label='Wins', linewidth=2, markersize=4, color='green')
        ax.plot(game_log.index, game_log['CUMULATIVE_LOSSES'], 
               marker='o', label='Losses', linewidth=2, markersize=4, color='red')
        
        ax.set_xlabel('Game Number', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        ax.set_title(f'{self.team_name} Win/Loss Record', 
                     fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def get_team_summary(self):
        """
        Get team season summary statistics
        
        Returns:
            dict: Dictionary containing team summary
        """
        if self.game_log is None or len(self.game_log) == 0:
            return {}
        
        wins = len(self.game_log[self.game_log['WL'] == 'W'])
        losses = len(self.game_log[self.game_log['WL'] == 'L'])
        
        summary = {
            'games_played': len(self.game_log),
            'wins': wins,
            'losses': losses,
            'win_percentage': (wins / len(self.game_log) * 100) if len(self.game_log) > 0 else 0,
            'ppg': self.game_log['PTS'].mean(),
            'opp_ppg': self.game_log.get('OPP_PTS', pd.Series([0])).mean(),
            'fg_pct': self.game_log['FG_PCT'].mean() * 100,
            'fg3_pct': self.game_log['FG3_PCT'].mean() * 100,
            'ft_pct': self.game_log['FT_PCT'].mean() * 100,
            'reb_pg': self.game_log['REB'].mean(),
            'ast_pg': self.game_log['AST'].mean()
        }
        
        return summary
    
    def compare_teams(self, team_names, stat_columns=['PTS', 'AST', 'REB'], figsize=(12, 6)):
        """
        Compare multiple teams across different statistics
        
        Args:
            team_names (list): List of team names to compare
            stat_columns (list): List of statistics to compare
            figsize (tuple): Figure size
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        if self.team_stats is None or len(self.team_stats) == 0:
            raise ValueError("No team stats loaded. Call fetch_league_standings first.")
        
        # Filter teams
        teams_data = self.team_stats[self.team_stats['TEAM_NAME'].isin(team_names)]
        
        if len(teams_data) == 0:
            raise ValueError("No teams found with the given names")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Set up bar positions
        x = range(len(stat_columns))
        width = 0.8 / len(team_names)
        
        # Plot bars for each team
        for i, team in enumerate(team_names):
            team_data = teams_data[teams_data['TEAM_NAME'] == team]
            if len(team_data) > 0:
                values = [team_data[stat].values[0] for stat in stat_columns if stat in team_data.columns]
                positions = [j + (i * width) for j in x]
                ax.bar(positions, values, width, label=team, edgecolor='black', linewidth=1)
        
        ax.set_xlabel('Statistics', fontsize=12)
        ax.set_ylabel('Value', fontsize=12)
        ax.set_title('Team Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks([i + width * (len(team_names) - 1) / 2 for i in x])
        ax.set_xticklabels(stat_columns)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig
