import os
import pymongo
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
    "mongo_db_name":"tmdb",
    "mongo_collection_name":"movies",
    "page_size":50,
}

mongo_client={}
mongo_db={}
page_index=0

myquery ={}

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


def get_page_movie():    
    global vars, myquery, page_index    
    page_size = vars["page_size"]
    movies=[]
    offset = page_size * page_index
    mongo_collection = mongo_db[ vars["mongo_collection_name"]]
    docs = mongo_collection.find(myquery,{
        "_id": 1,
        "original_title":1,
        "release_date":1
    }).sort("_id",1).skip(offset).limit(page_size)
    page_index +=1
    for doc in docs:
        movies.append(doc)
    return movies
    
              
    

get_key_values()
conect_mongo()

keep=True
cont=0
while(keep):
    movies = get_page_movie()
    print(movies)
    keep = (len(movies) > 0)    
        
