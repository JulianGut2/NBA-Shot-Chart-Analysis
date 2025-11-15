# Retrieve general imports
from nba_api.stats.endpoints import ShotChartDetail, BoxScoreSummaryV2
from nba_api.live.nba.endpoints import scoreboard
import pandas as pd
import datetime

# Create a list that contains all of the games in the data
# Right now I'm gonna just establish the list
games = []

# Open and read the file then I'll just stuff it all into
# the games list
with open("yesterdays_games.txt", "r") as f:
    for line in f:
        games.append(line.strip())

# Gonna keep this here for testing purposes
# print(games)
