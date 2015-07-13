-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

drop database if exists tournament;
create database tournament;
\CONNECT tournament;

CREATE TABLE player (id serial primary key, uname text);

CREATE TABLE match_result (winner serial REFERENCES player (id),
             loser serial REFERENCES player (id));

CREATE VIEW win_count AS
  SELECT player.id as player_id, count(match_result.winner) AS wins
  FROM player
  LEFT JOIN match_result
    ON player.id = match_result.winner
  GROUP BY player.id, match_result.winner;

CREATE VIEW match_count AS
  SELECT player.id as player_id, count(match_result) AS matches
  FROM player
  LEFT JOIN match_result
    ON (player.id = match_result.winner OR player.id = match_result.loser)
  GROUP BY player.id;