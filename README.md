# Projeto: Ciência de Dados Aplicada ao Futebol

Este projeto tem como objetivo estudar conceitos de ciência de dados aplicados ao futebol. A ideia é explorar até onde é possível chegar utilizando modelos de machine learning para prever probabilidades de vitória, derrota, gols, escanteios e outros aspectos interessantes relacionados ao esporte.

---

## Estrutura do Projeto

Atualmente, o projeto está dividido em três etapas principais, organizadas em diferentes pastas:

### 1. Coleta de Dados

A pasta **`Coleta`** contém todo o código utilizado para realizar a coleta de dados a partir da API **`API-FOOTBALL`**. Os dados coletados incluem:

- Resultados das partidas.
- Estatísticas dos times durante os jogos.
- Estatísticas dos jogadores minuto a minuto.
- Informações sobre escalações.

Os dados coletados são salvos na pasta **`data`** seguindo o formato de nomeação:  
`{Nome_Da_Liga}_{Season}_{TipoDeDado}.csv`.

---

### 2. Limpeza e Formatação de Dados

A pasta **`Cleaning`** contém scripts e notebooks para realizar a formatação e limpeza dos dados. Apesar de a coleta já fornecer uma boa estrutura, algumas melhorias foram feitas para facilitar o entendimento e a análise:

- Renomeação de colunas.
- Tratamento de valores faltantes.
- Ajuste de colunas categóricas.

#### Arquivos principais:

- **`Clean_Data.ipynb`**: Contém as alterações realizadas para fins de visualização.
- **`Data_Preparation.py`**: Automatiza as modificações realizadas no notebook e organiza os dados na pasta **`Data_Lake`**.

#### Organização dos dados:

O script **`Data_Preparation.py`** cria automaticamente uma estrutura organizada na pasta **`Data_Lake`**, onde:

- Cada campeonato possui sua própria pasta.
- Dentro de cada pasta de campeonato, há subpastas para cada ano disponível.

Essa organização facilita o acesso e a manipulação dos dados.

---

### 3. Preparação Inicial dos Dados

Nesta etapa, o objetivo é organizar os dados de forma que possam ser utilizados em modelos de machine learning. As principais ações realizadas incluem:

- Criação de uma tabela onde:
- Cada linha representa um jogo.
- As colunas contêm estatísticas acumuladas dos times em jogos anteriores, separadas entre time mandante e time visitante.
- Definição de variáveis-alvo para os modelos de classificação, como:
- Previsão de mais de 2.5 gols (1 para mais de 2.5 gols, 0 caso contrário).
- Previsão de escanteios, cartões, entre outros.

#### Banco de Dados

Utilizando **SQLite**, foi criado um banco de dados chamado **`Football.db`**. O script **`BancoSQL.py`**:

- Varre automaticamente a pasta **`Data_Lake`**.
- Insere todos os arquivos CSV disponíveis no banco de dados.

---

## Status do Projeto

A construção e organização dos dados ainda estão em andamento. O próximo passo será refinar os dados e iniciar a aplicação de modelos de machine learning para realizar as previsões.
