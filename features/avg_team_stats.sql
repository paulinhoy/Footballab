WITH ranked_games AS (
    SELECT 
        fixture_id,
        team_name,
        "passes_%",
        shots_on_goal,
        shots_off_goal,
        total_shots,
        blocked_shots,
        shots_insidebox,
        shots_outsidebox,
        fouls,
        corner_kicks,
        offsides,
        ball_possession,
        yellow_cards,
        red_cards,
        goalkeeper_saves,
        total_passes,
        passes_accurate,
        expected_goals,
        goals_prevented,
        ROW_NUMBER() OVER (PARTITION BY team_name ORDER BY fixture_id) AS row_num
    FROM Camp_Brasileiro_teams_2024 
),
ranked_games_stats AS (   
    SELECT 
        gm.fixture_id,
        gm.Home_Team,
        (gm.Gols_Home + gm.Gols_Away) as Total_Gols,
        CASE 
            WHEN gm.Home_Team = rk.team_name THEN gm.Gols_Home 
            ELSE gm.Gols_Away 
        END as Gols,
        rk.*
    FROM Camp_Brasileiro_games_2024 as gm
    INNER JOIN ranked_games as rk ON gm.fixture_id = rk.fixture_id
),
previous_three_games AS (
    SELECT 
        t.fixture_id,
        t.team_name,
        AVG(r.Gols) as avg_Gols,
        AVG(r.Total_Gols) AS avg_Total_Gols,
        AVG(r."passes_%") as "avg_passes_%",
        AVG(r.shots_on_goal) as avg_shots_on_goal,
        AVG(r.shots_off_goal) as avg_shots_off_goal,
        AVG(r.total_shots) as avg_total_shots,
        AVG(r.blocked_shots) as avg_blocked_shots,
        AVG(r.shots_insidebox) as avg_shots_insidebox,
        AVG(r.shots_outsidebox) as avg_shots_outsidebox,
        AVG(r.fouls) as avg_fouls,
        AVG(r.corner_kicks) as avg_corner_kicks,
        AVG(r.offsides) as avg_offsides,
        AVG(r.ball_possession) as avg_ball_possession,
        AVG(r.yellow_cards) as avg_yellow_cards,
        AVG(r.red_cards) as avg_red_cards,
        AVG(r.goalkeeper_saves) as avg_goalkeeper_saves,
        AVG(r.total_passes) as avg_total_passes,
        AVG(r.passes_accurate) as avg_passes_accurate,
        AVG(r.expected_goals) as avg_expected_goals,
        AVG(r.goals_prevented) as avg_goals_prevented
    FROM ranked_games_stats t
    LEFT JOIN ranked_games_stats r ON t.team_name = r.team_name AND r.row_num BETWEEN t.row_num - 3 AND t.row_num - 1
    GROUP BY t.fixture_id, t.team_name
)
SELECT
    fixture_id,
    team_name,
    avg_Gols,
    avg_Total_Gols,
    "avg_passes_%",
    avg_shots_on_goal,
    avg_shots_off_goal,
    avg_total_shots,
    avg_blocked_shots,
    avg_shots_insidebox,
    avg_shots_outsidebox,
    avg_fouls,
    avg_corner_kicks,
    avg_offsides,
    avg_ball_possession,
    avg_goalkeeper_saves,
    avg_total_passes,
    avg_passes_accurate,
    avg_expected_goals,
    avg_goals_prevented
FROM previous_three_games
ORDER BY fixture_id, team_name;