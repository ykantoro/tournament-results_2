#Overview
In this project contains a Python module that uses the PostgreSQL database to keep track of players and matches in a Swiss system pairing game tournament.
In the Swiss pairing game, players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.
In addition to the basic requirements, I implemented an additional feature:
*   Support games where a tied game is possible.

#Usage
1.	Install Vagrant and VirtualBox
2.	Download the source code and unzip it
3.	Launch the Vagrant VM and log in  
	`$ vagrant up`  
	`$ vagrant ssh`  
	`$ cd user/vagrant/fullstack/tournament/`  
4.	Initialize database  
	`$ psql`
5.	Database tournament and tables will be created by running tournament.sql file:  
	`=> \i tournament.sql`  
	`=> \q`
6.	Run test script  
    `$ python tournament_test.py`

#File Descriptions
###Tournament.py
**def connect()**  
Function used to connect to the PostreSQL database, returns a database connection.  
**def deleteMatches()**  
Function used for removal of all match records from the game table.  
**def deletePlayers()**  
Function used for removal of registered players from the players table.  
**def countPlayers()**  
Function used for counting all players registered in players table. Returns integer result.  
**def registerPlayer()**  
Function used for adding players to the players table, by inserting a players name. A serial id will be auto-generated when player name is registered in the players table.  
**def playerStandings()**  
Function queries players standings from players_standings view. Results are then parsed into tuple format (int, str, float, int) and returned. Float is used instead of integer because a match can result in a tie.  
**def reportMatch()**  
Function takes in 3 parameters, which are passed in once a match has completed. A winner player ID, a loser player ID (optional), and a winner2 player ID (optional). A winner parameter must always be passed in. If the match does not result in a tie, only a winner and a loser parameter will be passed. If the match results in a tie a winner and winner2 parameter will be passed in, loser parameter will default to 0. Depending on the results, player IDs are inserted into the winner column, loser column or winner2 column in the game table. These proper insertions are then used to score the game.  
**def swissPairings()**  
Query is fetched to get current player standings (from highest to lowest score). The query is then parsed and returned in a tuple format, each which contains (id1, name1, id2, name2).  
###Tournament.sql
**Table Players**  
Holds information on the registered players, such as id and name.  
**Table game**  
Holds information on the matches played, including winners, losers, ties, as well as player ids.  
**View player_count**  
This view is used to use count the number of players registered.  
**View num_matches**  
This view is used to determine the number of matches played by each player (id and name).  
**View scores**  
This view adds scores to each player depending on the outcome of their matches. 1 point is given if the match has a single winner, 0 points are given if the player lost the match. Half (0.5) points are given if the match ends in a tie.  
**View num_wins**  
This view sums up the score for each player for every match and orders the players by highest to lowest score.  
**View player_standings**  
This view joins view num_wins and view num_matches to return a snapshot of the current players names and ids, their current score and how many matches they have played.
