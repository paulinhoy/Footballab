import sqlite3
import os

# Definir o caminho para o banco de dados
# Nota: Como não temos o caminho real, vamos assumir que está no diretório atual
db_path = "Football.db"

# Verificar se o banco de dados existe
if not os.path.exists(db_path):
    print(f"Erro: Banco de dados '{db_path}' não encontrado.")
    print("Este script precisa ser executado no mesmo diretório do arquivo Football.db")
    print("ou o caminho precisa ser ajustado no código.")
else:
    # Conectar ao banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verificar se as tabelas para cada ano existem
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [table[0] for table in cursor.fetchall()]
    
    # Lista para armazenar os anos disponíveis
    available_years = []
    
    # Verificar quais anos estão disponíveis (2017-2024)
    for year in range(2017, 2025):
        table_name = f"Camp_Brasileiro_teams_{year}"
        if table_name in tables:
            available_years.append(year)
    
    if not available_years:
        print("Nenhuma tabela de dados de jogadores do Campeonato Brasileiro encontrada para os anos 2017-2024.")
    else:
        print(f"Anos disponíveis: {available_years}")
        
        # Criar tabela final se não existir
        cursor.execute("DROP TABLE IF EXISTS team_stats_all")
        
        # Processar cada ano disponível
        for year in available_years:
            print(f"Processando dados de {year}...")
            
            # Adaptar a query para o ano específico
            query = f"""
            -- Tabela temporária para o ano {year}
            CREATE TEMPORARY TABLE temp_team_stats_{year} AS
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
                ROW_NUMBER() OVER (PARTITION BY team_name ORDER BY fixture_id) AS row_num
            FROM Camp_Brasileiro_teams_{year} 
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
            FROM Camp_Brasileiro_games_{year} as gm
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
                AVG(r.passes_accurate) as avg_passes_accurate
            FROM ranked_games_stats t
            LEFT JOIN ranked_games_stats r ON t.team_name = r.team_name AND r.row_num BETWEEN t.row_num - 3 AND t.row_num - 1
            GROUP BY t.fixture_id, t.team_name
        )
        SELECT
            fixture_id,
            team_name,
            {year} as year,
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
            avg_passes_accurate
        FROM previous_three_games
        ORDER BY fixture_id, team_name;
            """
            
            try:
                # Executar a query para criar a tabela temporária
                cursor.execute(query)
                
                # Se for o primeiro ano, criar a tabela final
                if year == available_years[0]:
                    cursor.execute(f"""
                    CREATE TABLE team_stats_all AS
                    SELECT * FROM temp_team_stats_{year}
                    """)
                else:
                    # Para os anos seguintes, inserir na tabela final
                    cursor.execute(f"""
                    INSERT INTO team_stats_all
                    SELECT * FROM temp_team_stats_{year}
                    """)
                
                # Remover a tabela temporária
                cursor.execute(f"DROP TABLE temp_team_stats_{year}")
                
                # Commit para salvar as alterações
                conn.commit()
                print(f"Dados de {year} processados com sucesso!")
                
            except sqlite3.Error as e:
                print(f"Erro ao processar dados de {year}: {e}")
                conn.rollback()
        
        # Verificar quantos registros foram inseridos na tabela final
        cursor.execute("SELECT COUNT(*) FROM team_stats_all")
        count = cursor.fetchone()[0]
        print(f"\nProcessamento concluído! Total de {count} registros na tabela team_stats_all")
        
        # Mostrar alguns registros de exemplo
        cursor.execute("SELECT year, COUNT(*) FROM team_stats_all GROUP BY year")
        year_counts = cursor.fetchall()
        print("\nDistribuição por ano:")
        for year, count in year_counts:
            print(f"  {year}: {count} registros")
        
    # Fechar a conexão
    conn.close()