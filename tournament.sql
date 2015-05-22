-- Table definitions for the tournament project. 
-- Drop database if it already exists
-- Create tournament database and connect to it.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament; 
-- Columns: 
--   player_id:    id of players, auto-generated when player_name is registered. 
--   player_name:  name of player reistered.
CREATE TABLE players 
             ( 
             player_id SERIAL PRIMARY KEY, 
             player_name TEXT 
             ); 

-- Columns: 
--   winner: id of winner 
--   loser: id of loser (if not tied, can be null) 
--   tie: id of additional winner in the event of a tie
CREATE TABLE game 
             ( 
             winner SERIAL REFERENCES players, 
             loser INTEGER, 
             tie   INTEGER 
             ); 

-- Columns: 
--   num_players: counts the number of registered players via aggregate
CREATE VIEW player_count AS
SELECT Count(*)	AS num_players 
FROM   players; 

-- Columns: 
--   players.player_id:  ids of players in game 
--   players.player_name: name of players in game 
--   num_matches:    count of the number of matches played
CREATE VIEW num_matches AS 
SELECT    players.player_id, 
          players.player_name, 
          Count (winner) AS num_matches 
FROM      players 
LEFT JOIN game 
ON        players.player_id = winner 
OR        players.player_id = loser 
OR        players.player_id = tie 
GROUP BY  players.player_id 
ORDER BY  num_matches DESC; 

-- Columns: 
--   players.player_id:  ids of players in game 
--   players.player_name:  name of players in game 
--   scores:     scores recieved for every match played. 
--         lose:0 win:1 tie:0.5
CREATE VIEW score AS 
SELECT    players.player_id, 
          players.player_name, 
          CASE 
                    WHEN game.tie != 0 THEN 0.5 
                    WHEN game.winner = players.player_id THEN 1 
                    ELSE 0 
          END AS scores 
FROM      players 
LEFT JOIN game 
ON        players.player_id = winner 
OR        players.player_id = loser 
OR        players.player_id = tie 
GROUP BY  players.player_id, 
          game.winner, 
          game.tie 
ORDER BY  scores DESC; 

-- Columns: 
--   players.player_id:  id of players 
--   players.player_name: name of players 
--   num_wins:    number of matches that player won, 
--         summed from score view
CREATE VIEW num_wins AS 
SELECT    players.player_id, 
          players.player_name, 
          Sum(scores) AS num_wins 
FROM      players 
LEFT JOIN score 
ON        score.player_id = players.player_id 
GROUP BY  players.player_id, 
          players.player_name 
ORDER BY  num_wins DESC; 

-- Columns: 
--   num_wins.player_id:      id of players 
--   num_wins.player_name:   name of players 
--   num_wins.num_wins:   number of matches the player has won. Summed from score view 
--   num_matches.num_matches: number of matches the player has played.
CREATE VIEW player_standing AS
SELECT   num_wins.player_id, 
         num_wins.player_name, 
         num_wins.num_wins, 
         num_matches.num_matches 
FROM     num_wins, 
         num_matches 
WHERE    num_wins.player_id = num_matches.player_id 
ORDER BY num_wins.num_wins DESC, 
         num_matches.num_matches DESC;