# Tournament Project
The second project for the Fullstack Web Developer Nanodegree: 
Basic SQL implementation for Swiss Style Tournament
 
## Pre-Requisites
**Python 2** and **PostgreSQL**. I use Python 2.7 and PostgreSQL 9

## Setup & Testing
Having created a suitable database run the following command
from within psql to prepare the database:
```
$ \i tournament.sql
```
In order to test the project run
```
$ python tournament_test.py
```

# Tables
## player
Includes **id** and **uname** (user name)
 
## match_result
Records match results referencing the player.id in 
columns **winner** and **loser**

# Views
## win_count
Displays **player_id** and number of **wins**

## match_count
Displayes **player_id** and number of **matches**

# Using the Project
The following steps are recommended:
1. Register all players using the registerPlayer(name) method
2. User countPlayers() to verify the number of registered players
3. Run swissPairings() to get players grouped into matches for the next round
4. Run reportMatchWinner(winner, loser) to record results for each match
5. Run playerStandings() to view current standings

Steps 3. to 5. can obviously be run repeatedly.
