import helpers.scrape_nba_schedule as pull_games

weekly_games = pull_games.run()

print(weekly_games)