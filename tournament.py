#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except:
        print("Not able to connect with database")



def deleteMatches():
    """Remove all the match records from the database."""
    db, c = connect()
    # Removes all match results in game table
    query = "TRUNCATE TABLE game;"
    c.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, c = connect()
    # Removes all registered players
    query = "TRUNCATE TABLE players CASCADE;"
    c.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, c = connect()
    # Fetched query from player_count view - counts numer of players registered
    query = "SELECT * FROM player_count;"
    c.execute(query)
    # fetchone() returns a tuple (row)
    # To extract the value, query_result[0] is used
    query_restult = c.fetchone()
    db.close()
    return query_restult[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, c = connect()
    # Insert name parameter provided for player into players table
    # A unique player id will be generated for ever new player
    query = "INSERT INTO players (player_name) VALUES (%s)"
    # Use c.execute to format query command instead of directly string
    # formatting to prevent SQL injection
    c.execute(query, (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, c = connect()
    # Fetched query to get current player standings by highest score
    query = "SELECT * FROM player_standing"
    c.execute(query)
    # Returns a list tuples (rows) from query (int, str, float, int)
    standings = [[int(row[0]), str(row[1]),
                 float(row[2]), int(row[3])]
                 for row in c.fetchall()]
    db.close()
    return standings


def reportMatch(winner, loser=0, winner2=0):
    # Defaul properties are used in the case of a tied game
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, c = connect()
    # In the result of a tie (2 winners), a winner2 ID value will be passed in
    # to the winner2 optional parameter.
    # IF statement is used to determine logic needed for 2 scenarios:
    #   - A tie (if loser=0 - or keeps the default value)
    #   - A Win (if loser param is > 0 and winner2=0)
    if winner2 != 0:
        # If result is a tie, add player ids to correct columns in game table
        query = "INSERT INTO game (winner, tie) VALUES (%s,%s)"
        c.execute(query, (winner, winner2,))
    else:
        # If result is not a tie, add player ids to correct winner and loser
        # columns in game table
        query = "INSERT INTO game (winner, loser) VALUES (%s,%s)"
        c.execute(query, (winner, loser,))
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
    db, c = connect()
    # Get players standing (most to least points), including
    # name and unique ID
    query = "SELECT * FROM player_standing"
    c.execute(query)

    # Player standing query results represented in row
    # To extract results, a loop is used to capture row results
    # from c.fetchall()
    standings = [[int(row[0]), str(row[1])]
                 for row in c.fetchall()]

    # Create array to store tuple pairs from standings to be returned
    pairs = []
    i = 0
    # Loop through standings (rows) to create a tuple of pairs
    while i < len(standings):
        #pairs.append(zip(standings[i]))
        pairs.append([standings[i][0], standings[i][1],
                     standings[i+1][0], standings[i+1][1]])
        # Skip players by 2 to prevent incorrect matching.
        i = i+2
    db.close()
    return pairs
