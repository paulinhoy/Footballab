-- Ver nome das tabelas: Automatizar com python para ter estatística para todos campeonatos
SELECT name FROM sqlite_schema 
WHERE type='table'


select *
from player_last5_avg_stats_br_25min

CREATE TABLE player_last5_avg_stats_br_25min as
-- Tabela de Medias dos stats dos ultimos jogos
WITH 
-- Lista de todos os players para cada fixture_id
current_fixtures AS (
  SELECT DISTINCT fixture_id, player_id 
  FROM Camp_Brasileiro_players_2024
),

-- Jogos anteriores de cada jogador, com ranking para pegar os últimos 3
ranked_previous_games AS (
  SELECT 
    cf.fixture_id AS current_fixture,
    cf.player_id AS current_player_id,
    prev.*,
    ROW_NUMBER() OVER (
      PARTITION BY cf.fixture_id, cf.player_id 
      ORDER BY prev.fixture_id DESC
    ) AS rn
  FROM current_fixtures cf
  INNER JOIN Camp_Brasileiro_players_2024 prev
    ON cf.player_id = prev.player_id
    AND prev.fixture_id < cf.fixture_id
),

-- Cálculo das médias dos últimos 3 jogos por jogador e time
aggregated_stats AS (
  SELECT 
    current_fixture,
    current_player_id,
    team_id,
    AVG(rating) AS avg_rating,
    AVG(minutes) AS avg_minutes,
    AVG(offsides) AS avg_offsides,
    AVG(shots_total) AS avg_shots_total,
    AVG(shots_on) AS avg_shots_on,
    AVG(goals_total) AS avg_goals_total,
    AVG(goals_conceded) AS avg_goals_conceded,
    AVG(assists) AS avg_assists,
    AVG(saves) AS avg_saves,
    AVG(passes_total) AS avg_passes_total,
    AVG(passes_key) AS avg_passes_key,
    AVG(passes_accuracy) AS avg_passes_accuracy,
    AVG(tackles_total) AS avg_tackles_total,
    AVG(tackles_blocks) AS avg_tackles_blocks,
    AVG(tackles_interceptions) AS avg_tackles_interceptions,
    AVG(duels_total) AS avg_duels_total,
    AVG(duels_won) AS avg_duels_won,
    AVG(dribbles_attempts) AS avg_dribbles_attempts,
    AVG(dribbles_success) AS avg_dribbles_success,
    AVG(dribbles_past) AS avg_dribbles_past,
    AVG(fouls_drawn) AS avg_fouls_drawn,
    AVG(fouls_committed) AS avg_fouls_committed,
    AVG(cards_yellow) AS avg_cards_yellow,
    AVG(cards_red) AS avg_cards_red,
    AVG(penalty_won) AS avg_penalty_won,
    AVG(penalty_committed) AS avg_penalty_committed
  FROM ranked_previous_games
  WHERE rn <= 3  -- quantos jogos anteriores devem ser computados para fazer a media
  GROUP BY current_fixture, current_player_id, team_id
)

-- Resultado final com todos os jogadores, mesmo sem estatísticas anteriores
SELECT 
  cf.fixture_id,
  cf.player_id,
  a.team_id,
  a.avg_minutes,
  a.avg_rating,
  a.avg_offsides,
  a.avg_shots_total,
  a.avg_shots_on,
  a.avg_goals_total,
  a.avg_goals_conceded,
  a.avg_assists,
  a.avg_saves,
  a.avg_passes_total,
  a.avg_passes_key,
  a.avg_passes_accuracy,
  a.avg_tackles_total,
  a.avg_tackles_blocks,
  a.avg_tackles_interceptions,
  a.avg_duels_total,
  a.avg_duels_won,
  a.avg_dribbles_attempts,
  a.avg_dribbles_success,
  a.avg_dribbles_past,
  a.avg_fouls_drawn,
  a.avg_fouls_committed,
  a.avg_cards_yellow,
  a.avg_cards_red,
  a.avg_penalty_won,
  a.avg_penalty_committed
FROM current_fixtures cf
LEFT JOIN aggregated_stats a
  ON cf.fixture_id = a.current_fixture
  AND cf.player_id = a.current_player_id
where a.avg_minutes >25;          -- Pegando jogadores que nos ultimos 5 jogos jogou na media mais de 25 minutos 