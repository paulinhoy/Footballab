--SELECT name FROM sqlite_schema 
--WHERE type='table'

-- Essa query identifica/realiza:
-- qual o time com mando de campo, agrupa a media de estatisticas dos jogadores de cada time, cria uma única linha com estatítisca dos time mandante e do time visitante 

WITH 

situation_games as (
select pl.fixture_id,
       pl.player_id,
       pl.team_name,
       case 
        when pl.team_name = gm.Home_Team then 1
        else 0
       end as if_home_team -- Nome da coluna que identifica se o time é mandante 
from Camp_Brasileiro_players_2024 as pl
inner join Camp_Brasileiro_games_2024 as gm
    on pl.fixture_id = gm.fixture_id
),

stats_players as (
select ls.*,
       st.team_name,
       if_home_team
from player_last5_avg_stats_br_2024_45min as ls
    inner join situation_games as st
        on st.player_id = ls.player_id and st.fixture_id = ls.fixture_id
),

stats_team as (              
select  team_name, 
        if_home_team,
        fixture_id,
        AVG(avg_minutes) as avg_minutes_team,      -- Se criar novas features tenho que adicionar aqui 
        AVG(avg_rating) as avg_rating_team,
        AVG(avg_offsides) as avg_offsides_team,
        AVG(avg_shots_total) as avg_shots_total_team,
        AVG(avg_shots_on) as avg_shots_on_team,
        AVG(avg_goals_total) as avg_goals_total_team,
        AVG(avg_goals_conceded) as avg_goals_conceded_team,
        AVG(avg_assists) as avg_assists_team,
        AVG(avg_saves) as avg_saves_team,
        AVG(avg_passes_total) as avg_passes_total_team,
        AVG(avg_passes_key) as avg_passes_key_team,
        AVG(avg_passes_accuracy) as avg_passes_accuracy_team,
        AVG(avg_tackles_total) as avg_tackles_total_team,
        AVG(avg_tackles_blocks) as avg_tackles_blocks_team,
        AVG(avg_tackles_interceptions) as avg_tackles_interceptions_team,
        AVG(avg_duels_total) as avg_duels_total_team,
        AVG(avg_duels_won) as avg_duels_won_team,
        AVG(avg_dribbles_attempts) as avg_dribbles_attempts_team,
        AVG(avg_dribbles_success) as avg_dribbles_success_team,
        AVG(avg_dribbles_past) as avg_dribbles_past_team,
        AVG(avg_fouls_drawn) as avg_fouls_drawn_team,
        AVG(avg_fouls_committed) as avg_fouls_committed_team,
        AVG(avg_cards_yellow) as avg_cards_yellow_team,
        AVG(avg_cards_red) as avg_cards_red_team,
        AVG(avg_penalty_won) as avg_penalty_won_team,
        AVG(avg_penalty_committed) as avg_penalty_committed_team,
        AVG(avg_penalty_scored) as avg_penalty_scored_team,
        AVG(avg_penalty_missed) as avg_penalty_missed_team,
        AVG(avg_penalty_saved) as avg_penalty_saved_team
from stats_players
group by fixture_id, team_name
)

SELECT
    fixture_id,
    -- Para cada variável, crie colunas home (1) e away (0)         Se criar novas variaveis tenho que adicionar aqui 
    MAX(CASE WHEN if_home_team = 1 THEN avg_minutes_team END) AS avg_minutes_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_minutes_team END) AS avg_minutes_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_rating_team END) AS avg_rating_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_rating_team END) AS avg_rating_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_offsides_team END) AS avg_offsides_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_offsides_team END) AS avg_offsides_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_shots_total_team END) AS avg_shots_total_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_shots_total_team END) AS avg_shots_total_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_shots_on_team END) AS avg_shots_on_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_shots_on_team END) AS avg_shots_on_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_goals_total_team END) AS avg_goals_total_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_goals_total_team END) AS avg_goals_total_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_goals_conceded_team END) AS avg_goals_conceded_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_goals_conceded_team END) AS avg_goals_conceded_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_assists_team END) AS avg_assists_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_assists_team END) AS avg_assists_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_saves_team END) AS avg_saves_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_saves_team END) AS avg_saves_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_passes_total_team END) AS avg_passes_total_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_passes_total_team END) AS avg_passes_total_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_passes_key_team END) AS avg_passes_key_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_passes_key_team END) AS avg_passes_key_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_passes_accuracy_team END) AS avg_passes_accuracy_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_passes_accuracy_team END) AS avg_passes_accuracy_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_tackles_total_team END) AS avg_tackles_total_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_tackles_total_team END) AS avg_tackles_total_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_tackles_blocks_team END) AS avg_tackles_blocks_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_tackles_blocks_team END) AS avg_tackles_blocks_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_tackles_interceptions_team END) AS avg_tackles_interceptions_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_tackles_interceptions_team END) AS avg_tackles_interceptions_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_duels_total_team END) AS avg_duels_total_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_duels_total_team END) AS avg_duels_total_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_duels_won_team END) AS avg_duels_won_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_duels_won_team END) AS avg_duels_won_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_dribbles_attempts_team END) AS avg_dribbles_attempts_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_dribbles_attempts_team END) AS avg_dribbles_attempts_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_dribbles_success_team END) AS avg_dribbles_success_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_dribbles_success_team END) AS avg_dribbles_success_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_dribbles_past_team END) AS avg_dribbles_past_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_dribbles_past_team END) AS avg_dribbles_past_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_fouls_drawn_team END) AS avg_fouls_drawn_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_fouls_drawn_team END) AS avg_fouls_drawn_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_fouls_committed_team END) AS avg_fouls_committed_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_fouls_committed_team END) AS avg_fouls_committed_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_cards_yellow_team END) AS avg_cards_yellow_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_cards_yellow_team END) AS avg_cards_yellow_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_cards_red_team END) AS avg_cards_red_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_cards_red_team END) AS avg_cards_red_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_penalty_won_team END) AS avg_penalty_won_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_penalty_won_team END) AS avg_penalty_won_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_penalty_committed_team END) AS avg_penalty_committed_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_penalty_committed_team END) AS avg_penalty_committed_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_penalty_scored_team END) AS avg_penalty_scored_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_penalty_scored_team END) AS avg_penalty_scored_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_penalty_missed_team END) AS avg_penalty_missed_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_penalty_missed_team END) AS avg_penalty_missed_team_away,
    MAX(CASE WHEN if_home_team = 1 THEN avg_penalty_saved_team END) AS avg_penalty_saved_team_home,
    MAX(CASE WHEN if_home_team = 0 THEN avg_penalty_saved_team END) AS avg_penalty_saved_team_away
FROM stats_team
GROUP BY fixture_id;

-- Construção de variável respota em outa query ? 
