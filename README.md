# NetflixTMDB: Análise de Popularidade de Filmes e Séries do Netflix

### Projeto final da disciplina de Gerenciamento de Dados do Mestrado em TI do IFPB

## Equipe:
 - Antonio Alves de Sousa Junior
 - Bianca Karla Amorim de Sousa Melo
 - Isleimar de Souza Oliveira
 - Janderson Ferreira Dutra

## Configurações
Orientações para instalação do sistema.
* Requisito para configuração do ambiente virtual no python `python3.8-venv`.
* Baixe e salve o arquivo `netflix_titles.csv` (https://www.kaggle.com/shivamb/netflix-shows?select=netflix_titles.csv) na pasta `import_netflix/data`. Crie a  pasta se não existir.
* Crie o arquivo `.env` na pasta `import_tmdb` com a seguintes informações:
Exemplo:
```bash
#Valores para o MongoDB
mongo_url=<host_mongo>
mongo_port=27017
#Sua chave de acesso a API do TMDB
tmdb_key=<sua_chave_aqui>
```
* Por fim execute o arquivo `start.sh` e veja a mágica acontecer ;) 
