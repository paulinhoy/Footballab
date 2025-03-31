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
        table_name = f"Camp_Brasileiro_games_{year}"    #Colocar Camp_Brasileiro_players_{year} para verficar tbm
        if table_name in tables:
            available_years.append(year)
    
    if not available_years:
        print("Nenhuma tabela de dados de jogadores do Campeonato Brasileiro encontrada para os anos 2017-2024.")
    else:
        print(f"Anos disponíveis: {available_years}")
        
        # Criar tabela final se não existir
        cursor.execute("DROP TABLE IF EXISTS player_last5_avg_stats_br_25min_final")
        
        # Processar cada ano disponível
        for year in available_years:
            print(f"Processando dados de {year}...")
            
            # Adaptar a query para o ano específico
            query = f"""
            -- Tabela temporária para o ano {year}
            CREATE TEMPORARY TABLE temp_player_stats_final_{year} AS
            WITH 

            situation_games as (
            select pl.fixture_id,
                   pl.player_id,
                   pl.team_name,
                   case 
                    when pl.team_name = gm.Home_Team then 1
                    else 0
                   end as if_home_team -- Nome da coluna que identifica se o time é mandante 
            from Camp_Brasileiro_players_{year} as pl
            inner join Camp_Brasileiro_games_{year} as gm
                on pl.fixture_id = gm.fixture_id
            ),

            stats_players as (
            select ls.*,
                   st.team_name,
                   if_home_team
            from player_last5_avg_stats_br_25min as ls
                inner join situation_games as st
                    on st.player_id = ls.player_id and st.fixture_id = ls.fixture_id
            )

            select  team_name, 
                    if_home_team,
                    fixture_id,
                    year,
                    AVG(avg_minutes) as avg_minutes_team,      -- Se eu for criar novas features tenho que adicionar aqui 
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
                        """

            try:
                # Executar a query para criar a tabela temporária
                cursor.execute(query)
                
                # Se for o primeiro ano, criar a tabela final
                if year == available_years[0]:
                    cursor.execute(f"""
                    CREATE TABLE player_last5_avg_stats_br_25min_final AS
                    SELECT * FROM temp_player_stats_final_{year}
                    """)
                else:
                    # Para os anos seguintes, inserir na tabela final
                    cursor.execute(f"""
                    INSERT INTO player_last5_avg_stats_br_25min_final
                    SELECT * FROM temp_player_stats_final_{year}
                    """)
                
                # Remover a tabela temporária
                cursor.execute(f"DROP TABLE temp_player_stats_final_{year}")
                
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