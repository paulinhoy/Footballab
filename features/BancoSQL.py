import os
import pandas as pd
import sqlite3

# Diretório base
Data = '../Data_Lake/'

# Criando banco de dados
conn = sqlite3.connect('Football.db')
cursor = conn.cursor()

# Loop para percorrer as ligas e as seasons
for liga in os.listdir(Data):
    for ano in os.listdir(f'{Data}{liga}'):
        # Caminho base para os arquivos CSV
        base_path = f"{Data}{liga}/{ano}/{liga}_{ano}"

        # Importar arquivo de jogos (Games)
        games_file = f"{base_path}_Games_final.csv"
        if os.path.exists(games_file):
            df = pd.read_csv(games_file)
            df.to_sql(f"{liga}_games_{ano}", conn, if_exists='replace', index=False)
        else:
            print(f"Arquivo não encontrado: {games_file}")

        # Importar arquivo de estatísticas dos jogadores (Players)
        players_file = f"{base_path}_players_stats_final.csv"
        if os.path.exists(players_file):
            df = pd.read_csv(players_file)
            df.to_sql(f"{liga}_players_{ano}", conn, if_exists='replace', index=False)
        else:
            print(f"Arquivo não encontrado: {players_file}")

        # Importar arquivo de estatísticas dos times (Events)
        events_file = f"{base_path}_team_stats_final.csv"
        if os.path.exists(events_file):
            df = pd.read_csv(events_file)
            df.to_sql(f"{liga}_teams_{ano}", conn, if_exists='replace', index=False)
        else:
            print(f"Arquivo não encontrado: {events_file}")

# Fechando conexão com o banco de dados
conn.close()