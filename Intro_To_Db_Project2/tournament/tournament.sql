-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--

-- Tournament Database Schema Design
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

\c tournament;

CREATE TABLE player_details (
       player_id    SERIAL	 NOT NULL PRIMARY KEY,
       player_name  varchar(255) NOT NULL
);

CREATE TABLE match_details (
       match_id  SERIAL NOT NULL PRIMARY KEY,
       winner 	 SERIAL NOT NULL REFERENCES player_details(player_id),
       loser 	 SERIAL NOT NULL REFERENCES player_details(player_id)
);

CREATE VIEW player_record AS
       SELECT player_details.player_id as id,
       	      player_details.player_name as name,
	      (SELECT count(*) from match_details
	       WHERE player_details.player_id = match_details.winner) as matches_won,
	      (SELECT count(*) from match_details
	       WHERE player_details.player_id = match_details.winner OR
	       	     player_details.player_id = match_details.loser) as matches_played
	FROM player_details
	ORDER BY matches_won DESC;
