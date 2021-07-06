import os
import pymongo
import requests
import json

file_name_env=".env"
comment_char="#"
equalit_char="="

# É possível criar um arquivo de configuração para definir os valores.
# O arquivo de configuração será '.env' e deve está na mesma pasta.
# Os valores serão substituídos pelos valores constantes no arquivos de configuração.
# A chave "mongo_string=<string de acesso>" poderá ser definida no arquivo de configuração.
# A presença da chava "mongo_string" sobscreverá qualquer configuração de conexão
vars={
    "mongo_url":"localhost",
    "mongo_port":"27017",
    "mongo_db_name":"movies",
    "mongo_collection_name":"imdb_title_basics",
    "mongo_collection_tmdb":"tmdb_titles",
    "page_size":50,
    "tmdb_api_url":"https://api.themoviedb.org/3/movie/{0}?api_key={1}&language=pt-BR",
    "start_year":2000,
    "final_year":2030,
    "tmp_file_name":"movies.json",
    "ident_value":2
}

mongo_client={}
mongo_db={}
page_index=0
total=0

#Carregar variável do arquivo de configuração
def get_key_values():
    global vars
    if not os.path.isfile(file_name_env):
        return
    with open(file_name_env) as file:
        for row in file:
            if (row.find(comment_char)!=-1):
                row = row[:row.index(comment_char)]
            v = [x.strip() for x in row.partition(equalit_char)[::2] if x.strip()]
            if (len(v)==2):
                vars[v[0]]=v[1]
            elif (len(v)!=0):
                raise TypeError("Formato inválida para '{0}'".format(row.strip()))

#Conectar ao servidor do MongoDB
def conect_mongo():
    global vars,mongo_client,mongo_db
    if not ("mongo_string" in vars):
        mongo_url = vars["mongo_url"]
        mongo_port = vars["mongo_port"]
        vars["mongo_string"] = "mongodb://{0}:{1}".format(mongo_url,mongo_port)

    mongo_client = pymongo.MongoClient(vars["mongo_string"])
    mongo_db = mongo_client[vars["mongo_db_name"]]

#Busca no mongoDB
def get_movie_tmd_db(id):
    global vars, mongo_db
    collection = mongo_db[vars["mongo_collection_tmdb"]]    
    query={
        "_id" : {"$eq": id}
    }
    doc = collection.find_one(query)    
    if (doc is None):
        return    
    return doc


def get_movie_tmdb(id):
    global vars
    doc = get_movie_tmd_db(id)
    if not(doc is None):
        return doc    
    key = vars["tmdb_key"]
    url = vars["tmdb_api_url"].format(id,key)
    rsp = requests.get(url)
    if (rsp.status_code != 200):
        return
    return rsp.json()

def get_page_movie():
    global vars, page_index,total
    movies=[]
    page_size = vars["page_size"]
    offset = page_size * page_index
    mongo_collection = mongo_db[vars["mongo_collection_name"]]
    myquery ={
        "start_year" : {
            "$gte": int(vars["start_year"]),
            "$lt": int(vars["final_year"]) +1
        }
    }    
    docs = mongo_collection.find(myquery,{"_id": 1}).sort([("start_year", -1),( "_id",1)]).skip(offset).limit(page_size)
    if (docs.count(True) == 0):
        return
    page_index +=1
    for doc in docs:
        total += 1        
        try:
            movie = get_movie_tmdb(doc["_id"])
        except:
            print ("Falha na conexão")
        if (movie):
            movie["_id"] = doc["_id"]
            movies.append(movie)
    return movies

get_key_values()
conect_mongo()

keep=True
cont=0
file_name="data/{0}".format(vars["tmp_file_name"])
if (os.path.exists(file_name)):
    os.remove(file_name)
while(keep):
    movies = get_page_movie()
    keep = not (movies is None)
    if keep:
        with open(file_name,"a") as file:
            for movie in movies:
                if (cont == 0):
                    file.write("[")
                else:
                    file.write(",")
                json.dump(movie, file, indent=vars["ident_value"])
                cont +=1
            print("Gravando {0} -> Total testado {1}".format(cont, total))
with open(file_name,"a") as file:
    file.write("]")

