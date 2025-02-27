import pandas as pd
import os
import re

# Diretórios base
input_dir = "../Data/"
output_base_dir = "../Data_Lake/"

# Processar todos os arquivos CSV
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        # Extrair informações do nome do arquivo
        match = re.match(r'^(.+?)_(\d{4})_(\w+)\.csv$', filename)  # Padrão 1: Campeonato_Ano_Tipo
        if not match:
            match = re.match(r'^(.+?)_(\w+)_(\d{4})\.csv$', filename)  # Padrão 2: Campeonato_Tipo_Ano
        
        if match:
            # Determinar a ordem dos grupos
            if len(match.groups()) == 3:
                if match.re.pattern == r'^(.+?)_(\d{4})_(\w+)\.csv$':
                    championship, year, file_type = match.groups()
                else:
                    championship, file_type, year = match.groups()

                # Processar arquivos de team_stats
                if file_type == "team_stats":
                    # Carregar e transformar dados
                    df = pd.read_csv(os.path.join(input_dir, filename))
                    
                    # Preencher valores nulos
                    cols_to_fill = ['red_cards', 'yellow_cards', 'offsides']
                    for col in cols_to_fill:
                        df[col].fillna(0, inplace=True)
                    
                    # Criar diretório de saída
                    output_dir = os.path.join(output_base_dir, championship, year)
                    os.makedirs(output_dir, exist_ok=True)
                    
                    # Salvar arquivo
                    output_filename = f"{championship}_{year}_team_stats_final.csv"
                    df.to_csv(os.path.join(output_dir, output_filename), index=False)
                    
                    print(f"Arquivo de estatísticas processado: {filename} -> {output_filename}")

                # Processar arquivos de Games
                elif file_type == "Games":
                    # Carregar o arquivo
                    df_games = pd.read_csv(os.path.join(input_dir, filename))

                    # Renomear colunas
                    df_games = df_games.rename(columns={
                        'venue.name': 'Stadium',
                        'home.name': 'Home_Team',
                        'away.name': 'Away_Team',
                        'home': 'Gols_Home',
                        'away': 'Gols_Away',
                        'halftime.home': 'Half_Time_Gols_Home',
                        'halftime.away': 'Half_Time_Gols_Away'
                    })
                
                    # Adicionar coluna de empate
                    df_games['Empate'] = (df_games['Gols_Home'] == df_games['Gols_Away']).astype(int)

                    # Preencher valores nulos
                    df_games['home.winner'] = df_games['home.winner'].fillna(False)

                    # Criar diretório de saída
                    output_dir = os.path.join(output_base_dir, championship, year)
                    os.makedirs(output_dir, exist_ok=True)

                    # Salvar arquivo processado
                    output_filename = f"{championship}_{year}_Games_final.csv"
                    df_games.to_csv(os.path.join(output_dir, output_filename), index=False)

                    print(f"Arquivo processado: {filename} -> {output_filename}")

                # Processar players_stats
                elif file_type == "players_stats":
                    df = pd.read_csv(os.path.join(input_dir, filename))

                    # Preencher todos os valores NA com 0
                    df.fillna(0, inplace=True)

                    # Converter colunas específicas para inteiro
                    for col in ['captain', 'substitute']:
                        if col in df.columns:
                            df[col] = df[col].astype(int)
                        else:
                            print(f"Aviso: Coluna {col} não encontrada em {filename}")

                    # Criar diretório e salvar
                    output_dir = os.path.join(output_base_dir, championship, year)
                    os.makedirs(output_dir, exist_ok=True)
                    output_file = f"{championship}_{year}_players_stats_final.csv"
                    df.to_csv(os.path.join(output_dir, output_file), index=False)
                    print(f"Players stats processado: {filename} -> {output_file}")