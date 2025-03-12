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
        table_name = f"Camp_Brasileiro_players_{year}"
        if table_name in tables:
            available_years.append(year)
    
    if not available_years:
        print("Nenhuma tabela de dados de jogadores do Campeonato Brasileiro encontrada para os anos 2017-2024.")
    else:
        print(f"Anos disponíveis: {available_years}")
        
        # Criar tabela final se não existir
        cursor.execute("DROP TABLE IF EXISTS player_last5_avg_stats_br_25min")
        
        # Processar cada ano disponível
        for year in available_years:
            print(f"Processando dados de {year}...")
            
            # Adaptar a query para o ano específico
            query = f"""
            -- Tabela temporária para o ano {year}
            CREATE TEMPORARY TABLE temp_player_stats_{year} AS
            WITH 
            -- Lista de todos os players para cada fixture_id
            current_fixtures AS (
              SELECT DISTINCT fixture_id, player_id 
              FROM Camp_Brasileiro_players_{year}
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
              INNER JOIN Camp_Brasileiro_players_{year} prev
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
              WHERE rn <= 3
              GROUP BY current_fixture, current_player_id, team_id
            )

            -- Resultado final com todos os jogadores, mesmo sem estatísticas anteriores
            SELECT 
              cf.fixture_id,
              cf.player_id,
              a.team_id,
              {year} AS year,
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
            WHERE a.avg_minutes > 25;
            """
            
            try:
                # Executar a query para criar a tabela temporária
                cursor.execute(query)
                
                # Se for o primeiro ano, criar a tabela final
                if year == available_years[0]:
                    cursor.execute(f"""
                    CREATE TABLE player_last5_avg_stats_br_25min AS
                    SELECT * FROM temp_player_stats_{year}
                    """)
                else:
                    # Para os anos seguintes, inserir na tabela final
                    cursor.execute(f"""
                    INSERT INTO player_last5_avg_stats_br_25min
                    SELECT * FROM temp_player_stats_{year}
                    """)
                
                # Remover a tabela temporária
                cursor.execute(f"DROP TABLE temp_player_stats_{year}")
                
                # Commit para salvar as alterações
                conn.commit()
                print(f"Dados de {year} processados com sucesso!")
                
            except sqlite3.Error as e:
                print(f"Erro ao processar dados de {year}: {e}")
                conn.rollback()
        
        # Verificar quantos registros foram inseridos na tabela final
        cursor.execute("SELECT COUNT(*) FROM player_last5_avg_stats_br_25min")
        count = cursor.fetchone()[0]
        print(f"\nProcessamento concluído! Total de {count} registros na tabela player_last5_avg_stats_br_25min")
        
        # Mostrar alguns registros de exemplo
        cursor.execute("SELECT year, COUNT(*) FROM player_last5_avg_stats_br_25min GROUP BY year")
        year_counts = cursor.fetchall()
        print("\nDistribuição por ano:")
        for year, count in year_counts:
            print(f"  {year}: {count} registros")
        
    # Fechar a conexão
    conn.close()