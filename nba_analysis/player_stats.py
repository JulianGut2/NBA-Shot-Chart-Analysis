"""
Player Statistics Analyzer Module
Provides functionality to analyze and visualize individual player statistics
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nba_api.stats.endpoints import playercareerstats, playergamelog, commonplayerinfo
from nba_api.stats.static import players


class PlayerStatsAnalyzer:
    """
    Analyzes and visualizes NBA player statistics
    """
    
    def __init__(self):
        """Initialize the Player Stats Analyzer"""
        self.player_id = None
        self.player_name = None
        self.career_stats = None
        self.game_log = None
        
    def get_player_id(self, player_name):
        """
        Get player ID from player name
        
        Args:
            player_name (str): Name of the player
            
        Returns:
            int: Player ID or None if not found
        """
        player_dict = players.find_players_by_full_name(player_name)
        if player_dict:
            return player_dict[0]['id']
        return None
    
    def fetch_player_info(self, player_name):
        """
        Fetch basic player information
        
        Args:
            player_name (str): Name of the player
            
        Returns:
            pandas.DataFrame: Player information
        """
        self.player_id = self.get_player_id(player_name)
        self.player_name = player_name
        
        if self.player_id is None:
            raise ValueError(f"Player '{player_name}' not found")
        
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=self.player_id)
        return player_info.get_data_frames()[0]
    
    def fetch_career_stats(self, player_name, per_mode='PerGame'):
        """
        Fetch career statistics for a player
        
        Args:
            player_name (str): Name of the player
            per_mode (str): Statistics mode ('PerGame', 'Totals', 'Per36')
            
        Returns:
            pandas.DataFrame: Career statistics
        """
        self.player_id = self.get_player_id(player_name)
        self.player_name = player_name
        
        if self.player_id is None:
            raise ValueError(f"Player '{player_name}' not found")
        
        career = playercareerstats.PlayerCareerStats(
            player_id=self.player_id,
            per_mode36=per_mode
        )
        
        self.career_stats = career.get_data_frames()[0]
        return self.career_stats
    
    def fetch_game_log(self, player_name, season='2023-24', season_type='Regular Season'):
        """
        Fetch game log for a player's season
        
        Args:
            player_name (str): Name of the player
            season (str): NBA season (e.g., '2023-24')
            season_type (str): Type of season ('Regular Season', 'Playoffs')
            
        Returns:
            pandas.DataFrame: Game log data
        """
        self.player_id = self.get_player_id(player_name)
        self.player_name = player_name
        
        if self.player_id is None:
            raise ValueError(f"Player '{player_name}' not found")
        
        gamelog = playergamelog.PlayerGameLog(
            player_id=self.player_id,
            season=season,
            season_type_all_star=season_type
        )
        
        self.game_log = gamelog.get_data_frames()[0]
        return self.game_log
    
    def plot_career_progression(self, stat_column='PTS', figsize=(12, 6)):
        """
        Plot career progression for a specific statistic
        
        Args:
            stat_column (str): Column to plot (e.g., 'PTS', 'AST', 'REB')
            figsize (tuple): Figure size
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        if self.career_stats is None or len(self.career_stats) == 0:
            raise ValueError("No career stats loaded. Call fetch_career_stats first.")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot the progression
        seasons = self.career_stats['SEASON_ID']
        values = self.career_stats[stat_column]
        
        ax.plot(seasons, values, marker='o', linewidth=2, markersize=8)
        ax.set_xlabel('Season', fontsize=12)
        ax.set_ylabel(stat_column, fontsize=12)
        ax.set_title(f'{self.player_name} Career {stat_column} Progression', 
                     fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        return fig
    
    def plot_season_performance(self, stat_columns=['PTS', 'AST', 'REB'], figsize=(14, 6)):
        """
        Plot game-by-game performance for multiple statistics
        
        Args:
            stat_columns (list): List of statistics to plot
            figsize (tuple): Figure size
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        if self.game_log is None or len(self.game_log) == 0:
            raise ValueError("No game log loaded. Call fetch_game_log first.")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Reverse the game log to show chronological order
        game_log = self.game_log.iloc[::-1].reset_index(drop=True)
        
        for stat in stat_columns:
            if stat in game_log.columns:
                ax.plot(game_log.index, game_log[stat], marker='o', 
                       label=stat, linewidth=1.5, markersize=4, alpha=0.7)
        
        ax.set_xlabel('Game Number', fontsize=12)
        ax.set_ylabel('Statistics', fontsize=12)
        ax.set_title(f'{self.player_name} Season Performance', 
                     fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def get_season_averages(self):
        """
        Calculate season averages from game log
        
        Returns:
            dict: Dictionary containing season averages
        """
        if self.game_log is None or len(self.game_log) == 0:
            return {}
        
        numeric_cols = self.game_log.select_dtypes(include=['float64', 'int64']).columns
        averages = {}
        
        for col in ['PTS', 'AST', 'REB', 'STL', 'BLK', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'MIN']:
            if col in numeric_cols:
                averages[col] = self.game_log[col].mean()
        
        return averages
    
    def plot_shooting_splits(self, figsize=(10, 6)):
        """
        Plot shooting percentages from game log
        
        Args:
            figsize (tuple): Figure size
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        if self.game_log is None or len(self.game_log) == 0:
            raise ValueError("No game log loaded. Call fetch_game_log first.")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Get shooting percentages
        shooting_stats = {
            'FG%': self.game_log['FG_PCT'].mean() * 100,
            '3P%': self.game_log['FG3_PCT'].mean() * 100,
            'FT%': self.game_log['FT_PCT'].mean() * 100
        }
        
        categories = list(shooting_stats.keys())
        values = list(shooting_stats.values())
        
        bars = ax.bar(categories, values, color=['#1f77b4', '#ff7f0e', '#2ca02c'], 
                      edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%',
                   ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Percentage', fontsize=12)
        ax.set_title(f'{self.player_name} Shooting Splits', 
                     fontsize=14, fontweight='bold')
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig
    
    def create_stats_summary(self):
        """
        Create a comprehensive statistics summary
        
        Returns:
            pandas.DataFrame: Summary statistics
        """
        if self.game_log is None or len(self.game_log) == 0:
            return pd.DataFrame()
        
        summary_data = {
            'Statistic': ['Games Played', 'PPG', 'RPG', 'APG', 'SPG', 'BPG', 
                         'FG%', '3P%', 'FT%', 'MPG'],
            'Value': [
                len(self.game_log),
                self.game_log['PTS'].mean(),
                self.game_log['REB'].mean(),
                self.game_log['AST'].mean(),
                self.game_log['STL'].mean(),
                self.game_log['BLK'].mean(),
                self.game_log['FG_PCT'].mean() * 100,
                self.game_log['FG3_PCT'].mean() * 100,
                self.game_log['FT_PCT'].mean() * 100,
                self.game_log['MIN'].mean()
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        summary_df['Value'] = summary_df['Value'].round(2)
        
        return summary_df
