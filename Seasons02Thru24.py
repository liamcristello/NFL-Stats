# I'm mostly copying from this video, thank you to Kerry Sports Analyst for the tutorial!
# https://youtu.be/2JDR6jv0fGA?si=54LOUvJ7aeTqA-UD

# Import libraries
#import numpy as np
import pandas as pd
import random
import time

# CONSTS
URL_FRONT = 'https://www.pro-football-reference.com/teams/'
URL_BACK = '/gamelog/'
ATTR_ID = 'id'
ATTR_GAMELOG = 'gamelog'
ATTR_GAMELOG_OPP = 'gamelog_opp'
COL_TEAM = 'Team'
COL_SEASON = 'Season'

# Seasons to download
seasons = [str(season) for season in range(2002, 2025)] #not-inclusive of second param in range
print(f'number of seasons={len(seasons)}')

# Team abbrs
team_abbrs = ['buf','mia','nyj','nwe','rav','cin','cle','pit','htx','clt','jax','oti','den','kan','sdg','rai',
              'dal','nyg','phi','was','chi','det','gnb','min','atl','car','nor','tam','crd','ram','sea','sfo']
print(f'number of team={len(team_abbrs)}')

# Create empty dataframe to append
nfl_df = pd.DataFrame()

# Iterate through seasons
for season in seasons:
    # Iterate through teams
    for team in team_abbrs:
        # STEP 1. Set the  URL
        url = URL_FRONT + team + '/' + season + URL_BACK
        print(url)

        # STEP 2. Get offensive stats (game log table)
        off_df = pd.read_html(url, header=1, attrs={ATTR_ID:ATTR_GAMELOG + season})[0]

        # STEP 3. Get defensive stats (opponent game log table)
        def_df = pd.read_html(url, header=1, attrs={ATTR_ID:ATTR_GAMELOG_OPP + season})[0]

        # STEP 4. Concat two dataframes (offense and defense) (along columns, axis = 1)
        team_df = pd.concat([off_df, def_df], axis=1)

        # Insert the Season column into the dataframe
        team_df.insert(loc=0, column=COL_SEASON, value=season)

        # Insert the Team column into the dataframe
        team_df.insert(loc=2, column=COL_TEAM, value=team.upper())

        # STEP 5. Concatenate the team gamelog to the aggregate dataframe (along rows, axis = 0)
        nfl_df = pd.concat([nfl_df, team_df], ignore_index=True)

        # Pause the program to abide by website rules ("The Dude abides" - Jeff Lebowski)
        # min time is 7 seconds, so will never get more than 8 requests in a minute, well under their 10/min rule
        time.sleep(random.randint(7,8))

# FINAL STEP. Save the downloaded data to a CSV file
nfl_df.to_csv('nfl_gamelogs_2002_to_2024.csv')

# Display aggregate dataframe
print(nfl_df)
