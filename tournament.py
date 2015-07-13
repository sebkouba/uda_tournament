#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(dbname="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        # this allows you to parameterise variables, right?!?
        db = psycopg2.connect("dbname={}".format(dbname))
        cursor = db.cursor()
        return db, cursor
    except:
        print("db is messed up somehow")


def deleteMatches():
    """Remove all the match records from the database."""
    db, c = connect()

    c.execute("TRUNCATE match_result;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, c = connect()
    c.execute("TRUNCATE player;")
    db.commit()
    db.close


def countPlayers():
    """Returns the number of players currently registered."""
    db, c = connect()
    query = "SELECT count(*) FROM player"

    c.execute(query)
    result = c.fetchall()
    db.close
    return int(result[0][0])


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db, c = connect()
    query = "INSERT INTO player (uname) VALUES (%s)"
    param = (name,)

    c.execute(query, param)
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, c = connect()
    query = """
              SELECT player.id, uname, wins, matches
              FROM player
              LEFT JOIN match_count ON player.id = match_count.player_id
              LEFT JOIN win_count ON player.id = win_count.player_id
              GROUP BY player.id, win_count.wins, match_count.matches
              ORDER BY wins DESC;
              """
    c.execute(query)

    standings = c.fetchall()

    db.close
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, c = connect()

    query = "INSERT INTO match_result (winner, loser) VALUES (%s, %s)"
    param = (winner, loser)

    c.execute(query, param)
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # use existing "standings" as starting point
    standings = playerStandings()

    pairs = []

    # loop through "standings" in steps of two & add pairs to list
    for i in range(0, len(standings), 2):
        # make sure we have enough players for the i'th pair
        if len(standings) >= i+2:
            # not sure if this makes the code more readable or just longer...
            first_id = standings[i][0]
            first_name = standings[i][1]
            second_id = standings[i+1][0]
            second_name = standings[i+1][1]

            pairs.append((first_id, first_name, second_id, second_name))

    return pairs
