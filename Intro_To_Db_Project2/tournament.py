#!/usr/bin/env python# 
# tournament.py -- implementation of a Swiss-system tournament

import psycopg2
import traceback
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.disabled = True

"""
Table Names in the tournament schema.
"""
MATCH_TABLE = "match_details"
PLAYER_TABLE = "player_details"
PLAYER_RECORD_VIEW = "player_record"

"""
Helpler Functions
"""
def queryExecutor(query, 
                  qry_params = None, 
                  fetch_result = False):
    try:
        db_connection = connect()

        if db_connection is None:
            logger.info ("Error in connecting to DB")
        
        logger.info ("Executing Query: " + query)    
        if (qry_params):
            logger.info ("Query Parameters: " + str(qry_params))

        cursor = db_connection.cursor()
        cursor.execute(query, qry_params);        
        db_connection.commit()        
        logger.info ("Total number of rows affected: " + str(cursor.rowcount))

        if(fetch_result):
            return cursor.fetchall()

    except psycopg2.Error as ex:
        logger.error ("\nPostgres Exception caught: \nException Details: " + str(ex)) 
    except Exception as ex:
        logger.error ("\nPython Exception caught: \n" + traceback.format_exc())

    db_connection.close()
    

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""   
    queryExecutor("DELETE FROM " + MATCH_TABLE) 

def deletePlayers():
    """Remove all the player records from the database."""
    queryExecutor("DELETE FROM " + PLAYER_TABLE)

def countPlayers():
    """Returns the number of players currently registered."""
    query = ("SELECT count(*) FROM " + PLAYER_TABLE)
    qry_results = queryExecutor(query, 
                                fetch_result = True)    
    logger.debug ("Player Count: " + str(qry_results[0][0]))
    return qry_results[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    query = ("INSERT INTO " + PLAYER_TABLE + " (player_name) VALUES (%s)")
    qry_params = (name, )
    queryExecutor(query, qry_params)

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
    query = ("SELECT * FROM " + PLAYER_RECORD_VIEW)    
    return queryExecutor(query, 
                         fetch_result = True)    

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """ 
    query = ("INSERT INTO " + MATCH_TABLE + " (winner, loser) VALUES (%s, %s)")
    qry_params = (winner, loser, )
    queryExecutor(query, qry_params)

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

    player_standings = playerStandings()
    swiss_pairs = list()

    for players_idx in xrange(0, len(player_standings)/2):
        player_1 = player_standings[players_idx * 2]
        player_2 = player_standings[(players_idx * 2) + 1]
        swiss_pairs.append((player_1[0], player_1[1], player_2[0], player_2[1]))

    return swiss_pairs