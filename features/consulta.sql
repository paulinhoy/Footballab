-- SELECT name FROM sqlite_schema 
-- WHERE type='table'

-- Essa query identifica/realiza:
-- qual o time com mando de campo, agrupa a media de estatisticas dos jogadores de cada time, cria uma única linha com estatítisca dos time mandante e do time visitante 
-- Consulta com estatisticas corrigidas, mas não juntei as estatisticas de time mandante e visitante. 
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
from player_last5_avg_stats_br_2024_25min as ls
    inner join situation_games as st
        on st.player_id = ls.player_id and st.fixture_id = ls.fixture_id
)
              
select  team_name, 
        if_home_team,
        fixture_id,
        AVG(avg_minutes) as avg_minutes_team,      -- Se criar novas features tenho que adicionar aqui 
        AVG(avg_rating) as avg_rating_team,
        SUM(avg_offsides) as avg_offsides_team,
        SUM(avg_shots_total) as avg_shots_total_team,
        SUM(avg_shots_on) as avg_shots_on_team,
        SUM(avg_goals_total) as avg_goals_total_team,
        SUM(avg_goals_conceded) as avg_goals_conceded_team,
        SUM(avg_assists) as avg_assists_team,
        SUM(avg_saves) as avg_saves_team,
        SUM(avg_passes_total) as avg_passes_total_team,
        SUM(avg_passes_key) as avg_passes_key_team,
        SUM(avg_passes_accuracy) as avg_passes_accuracy_team,
        SUM(avg_tackles_total) as avg_tackles_total_team,
        SUM(avg_tackles_blocks) as avg_tackles_blocks_team,
        SUM(avg_tackles_interceptions) as avg_tackles_interceptions_team,
        SUM(avg_duels_total) as avg_duels_total_team,
        SUM(avg_duels_won) as avg_duels_won_team,
        SUM(avg_dribbles_attempts) as avg_dribbles_attempts_team,
        SUM(avg_dribbles_success) as avg_dribbles_success_team,
        SUM(avg_dribbles_past) as avg_dribbles_past_team,
        SUM(avg_fouls_drawn) as avg_fouls_drawn_team,
        SUM(avg_fouls_committed) as avg_fouls_committed_team,
        SUM(avg_cards_yellow) as avg_cards_yellow_team,
        SUM(avg_cards_red) as avg_cards_red_team,
        SUM(avg_penalty_won) as avg_penalty_won_team,
        SUM(avg_penalty_committed) as avg_penalty_committed_team
from stats_players
group by fixture_id, team_name
