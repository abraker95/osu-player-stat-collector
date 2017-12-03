# osu-player-stat-collector
Scrapes osu! player data in the top 10k off the old website

## Running
```$ python run.py```

## Description
Goes through each player on the leaderboard and gets their

| rank | performance | hitcount | playcount | combo | playtime | ranked score | total score |
------ | ----------- | -------- | --------- | ----- | -------- | ------------ | ----------- |
  
This info is written to a player_stats.csv file
* approximate size: 1.2mb
* approximate time to gather info: 2h
