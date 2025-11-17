"""
Shot Chart Analyzer Module
Provides functionality to visualize NBA player shot charts
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import players, teams


class ShotChartAnalyzer:
    """
    Analyzes and visualizes NBA player shot charts
    """
    
    def __init__(self):
        """Initialize the Shot Chart Analyzer"""
        self.shot_data = None
        
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
    
    def get_team_id(self, team_name):
        """
        Get team ID from team name
        
        Args:
            team_name (str): Name of the team
            
        Returns:
            int: Team ID or None if not found
        """
        team_dict = teams.find_teams_by_full_name(team_name)
        if team_dict:
            return team_dict[0]['id']
        return None
    
    def fetch_shot_data(self, player_name, season='2023-24', season_type='Regular Season'):
        """
        Fetch shot chart data for a player
        
        Args:
            player_name (str): Name of the player
            season (str): NBA season (e.g., '2023-24')
            season_type (str): Type of season ('Regular Season', 'Playoffs')
            
        Returns:
            pandas.DataFrame: Shot chart data
        """
        player_id = self.get_player_id(player_name)
        
        if player_id is None:
            raise ValueError(f"Player '{player_name}' not found")
        
        # Fetch shot chart data
        shot_chart = shotchartdetail.ShotChartDetail(
            team_id=0,
            player_id=player_id,
            season_nullable=season,
            season_type_all_star=season_type,
            context_measure_simple='FGA'
        )
        
        self.shot_data = shot_chart.get_data_frames()[0]
        return self.shot_data
    
    def draw_court(self, ax=None, color='black', lw=2, outer_lines=False):
        """
        Draw NBA court on matplotlib axis
        
        Args:
            ax: Matplotlib axis object
            color: Line color
            lw: Line width
            outer_lines: Whether to draw outer court lines
            
        Returns:
            matplotlib.axes.Axes: The axis with court drawn
        """
        if ax is None:
            ax = plt.gca()
        
        # Create the basketball hoop
        hoop = patches.Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)
        
        # Create backboard
        backboard = patches.Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)
        
        # The paint (restricted area)
        outer_box = patches.Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
        inner_box = patches.Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)
        
        # Free throw top arc
        top_free_throw = patches.Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                                      linewidth=lw, color=color, fill=False)
        
        # Free throw bottom arc
        bottom_free_throw = patches.Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                                         linewidth=lw, color=color, linestyle='dashed', fill=False)
        
        # Restricted Zone
        restricted = patches.Arc((0, 0), 80, 80, theta1=0, theta2=180,
                                 linewidth=lw, color=color, fill=False)
        
        # Three point line
        corner_three_a = patches.Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
        corner_three_b = patches.Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
        three_arc = patches.Arc((0, 0), 475, 475, theta1=22, theta2=158,
                                linewidth=lw, color=color, fill=False)
        
        # Center Court
        center_outer_arc = patches.Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                                        linewidth=lw, color=color, fill=False)
        center_inner_arc = patches.Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                                        linewidth=lw, color=color, fill=False)
        
        # List of court shapes
        court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                          bottom_free_throw, restricted, corner_three_a,
                          corner_three_b, three_arc, center_outer_arc,
                          center_inner_arc]
        
        # Add outer lines
        if outer_lines:
            outer_lines_shape = patches.Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                                   color=color, fill=False)
            court_elements.append(outer_lines_shape)
        
        # Add all elements to the plot
        for element in court_elements:
            ax.add_patch(element)
        
        return ax
    
    def plot_shot_chart(self, player_name, season='2023-24', season_type='Regular Season',
                        title=None, figsize=(12, 11), cmap='coolwarm'):
        """
        Create a shot chart visualization for a player
        
        Args:
            player_name (str): Name of the player
            season (str): NBA season
            season_type (str): Type of season
            title (str): Custom title for the chart
            figsize (tuple): Figure size
            cmap (str): Colormap for the shots
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        # Fetch data if not already loaded
        if self.shot_data is None:
            self.fetch_shot_data(player_name, season, season_type)
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=figsize)
        
        # Draw the court
        self.draw_court(ax, outer_lines=True)
        
        # Plot made and missed shots
        made_shots = self.shot_data[self.shot_data['SHOT_MADE_FLAG'] == 1]
        missed_shots = self.shot_data[self.shot_data['SHOT_MADE_FLAG'] == 0]
        
        ax.scatter(missed_shots['LOC_X'], missed_shots['LOC_Y'], 
                   c='red', marker='x', s=50, linewidths=2, alpha=0.5, label='Missed')
        ax.scatter(made_shots['LOC_X'], made_shots['LOC_Y'], 
                   c='green', marker='o', s=50, alpha=0.5, label='Made')
        
        # Set plot limits and properties
        ax.set_xlim(-250, 250)
        ax.set_ylim(-47.5, 422.5)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Add title
        if title is None:
            fg_pct = (len(made_shots) / len(self.shot_data) * 100) if len(self.shot_data) > 0 else 0
            title = f"{player_name} Shot Chart\n{season} {season_type}\nFG%: {fg_pct:.1f}%"
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.legend(loc='upper right')
        plt.tight_layout()
        
        return fig
    
    def get_shot_statistics(self):
        """
        Calculate shot statistics from loaded data
        
        Returns:
            dict: Dictionary containing various shot statistics
        """
        if self.shot_data is None or len(self.shot_data) == 0:
            return {}
        
        total_shots = len(self.shot_data)
        made_shots = len(self.shot_data[self.shot_data['SHOT_MADE_FLAG'] == 1])
        
        stats = {
            'total_shots': total_shots,
            'made_shots': made_shots,
            'missed_shots': total_shots - made_shots,
            'fg_percentage': (made_shots / total_shots * 100) if total_shots > 0 else 0
        }
        
        # Three-point statistics
        three_pointers = self.shot_data[self.shot_data['SHOT_TYPE'] == '3PT Field Goal']
        if len(three_pointers) > 0:
            made_3pt = len(three_pointers[three_pointers['SHOT_MADE_FLAG'] == 1])
            stats['three_pt_attempts'] = len(three_pointers)
            stats['three_pt_made'] = made_3pt
            stats['three_pt_percentage'] = (made_3pt / len(three_pointers) * 100)
        
        # Two-point statistics
        two_pointers = self.shot_data[self.shot_data['SHOT_TYPE'] == '2PT Field Goal']
        if len(two_pointers) > 0:
            made_2pt = len(two_pointers[two_pointers['SHOT_MADE_FLAG'] == 1])
            stats['two_pt_attempts'] = len(two_pointers)
            stats['two_pt_made'] = made_2pt
            stats['two_pt_percentage'] = (made_2pt / len(two_pointers) * 100)
        
        return stats
