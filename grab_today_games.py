# General Imports
import os 
from nba_api.stats.endpoints import LeagueGameFinder
from datetime import date, timedelta

# Creating our function to grab yesterdays game
def get_yesterdays_games():
    
    # Using datetime to grab yesterdays date and correcting format
    # based on nba_api requirements
 
    yesterday = date.today() - timedelta(days = 1)

    fmt_correction = yesterday.strftime('%m/%d/%Y')

    # Getting the game information specifically for the regular season
    gamefinder = LeagueGameFinder(
        league_id_nullable = "00",
        date_from_nullable = fmt_correction,
        date_to_nullable = fmt_correction,
        season_type_nullable = "Regular Season"
    )

    games_df = gamefinder.get_data_frames()[0]
    # Ran these in order to see column names and data, dont need them anymore
    # but will keep them here for reference incase of debugging
    #print(games_df.columns)
    #print(games_df.head())

    game_ids = games_df["GAME_ID"].unique().tolist()

    # This will return yesterdays date as well as all games that were played
    return yesterday, game_ids

def write_to_text(filename = "yesterdays_games.txt"):
    yday, game_ids = get_yesterdays_games()
    
    if not game_ids:
        print(f"No games found for {yday}. Nothing was written.")
        return

    with open(filename, "w") as f:
        for gid in game_ids:
            f.write(f"{gid}\n")

    print(f"Wrote {len(game_ids)} game IDs for {yday} to {filename}")
    print("Game IDs: ", game_ids)

if __name__ == "__main__":
    write_to_text()