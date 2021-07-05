import csv
import json
import sys
import os
import time

#######################################################################
# Desenvolvido por: Isleimar Oliveira
# Descrição: Converte arquivos CSV para JSON
# Comando: python3 name.basics.py <input_file> <output_file> <options>
# Options:
#   -n --null_value : valor nulo
#   -i --ident_value : espaço da identação
#   -d --delimiter_value : delimitador entre os campos
#   -s --sub_delimiter_value : delimitador dentro dos campos
#   -c --count_limit' : Quantidade limite de itens
#   --remove_file : excluir o arquivo de destino
######################################################################

#Default Values 
null_value = "\\N"
ident_value = 2
delimiter_value = ','
sub_delimiter_value = ','
in_file = ''
out_file = ''
count_limit = 0
remove_file = False

def arguments(args):  
    global null_value, ident_value, delimiter_value, sub_delimiter_value, remove_file, in_file, out_file, count_limit
    files = []  
    try:
        while (len(args) > 0):
            arg = args.pop(0).strip()
            if (arg in ['-n','--null_value']):
                null_value = args.pop(0).strip()
            elif (arg in ['-i','--ident_value']):
                ident_value = int(args.pop(0).strip()) 
            elif (arg in ['-d','--delimiter_value']):
                delimiter_value = args.pop(0).strip() 
            elif (arg in ['-s','--sub_delimiter_value']):
                sub_delimiter_value = args.pop(0).strip() 
            elif (arg in ['-c','--count_limit']):
                count_limit = int(args.pop(0).strip())
            elif (arg in ['--remove_file']):
                remove_file = True                 
            else:
                files.append(arg)
    except:
        print("Invalid arguments")
        raise
    if (len(files) != 2):
        raise "Invalid arguments"    
    in_file, out_file =  files   
    if not (os.path.exists(in_file)):
        raise TypeError("File '{0}' not found. ".format(in_file)) 
    if (os.path.exists(out_file) and not(remove_file)):
        raise TypeError("File '{0}' already exists. ".format(out_file)) 

# Função para extrair os elemtos de um campo 
def extract(s):
    ars = s.split(sub_delimiter_value) 
    ars[:] = [x.strip() for x in ars if x.strip()]
    while (null_value in ars):
        ars.remove(null_value)            
    return ars

def convertToJson():
    all_names = []
    with open(in_file) as c_file:
        reader = csv.reader(c_file, delimiter=delimiter_value)
        headers = reader.__next__()
        i = 0
        for row in reader:
            line = dict(zip(headers, row))
            line["_id"] = line.pop("show_id")
            line["type"] = line.pop("type")

            #director
            director = extract(line.pop("director"))
            if (len(director) > 0):
                line["director"] = director

            #cast
            cast = extract(line.pop("cast"))
            if (len(cast) > 0):
                line["cast"] = cast

            #country
            country = extract(line.pop("country"))
            if (len(country) > 0):
                line["country"] = country
            
            #date_added
            date_added = line.pop("date_added")
            if date_added:
                time_struct = time.strptime(date_added.strip(), "%B %d, %Y")
                iso_date = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time_struct)
                line["date_added"] = {"$date": iso_date}

            #release_year
            release_year = line.pop("release_year")
            if not (release_year == null_value):
                line["release_year"] = int(release_year)

            line["rating"] = line.pop("rating")
            line["duration"] = line.pop("duration")

            #listed_in
            listed_in = extract(line.pop("listed_in"))
            if (len(listed_in) > 0):
                line["listed_in"] = listed_in

            line["description"] = line.pop("description")

            with open(out_file, "a") as j_file:
                if (i == 0):
                    j_file.write("[")
                else:
                    j_file.write(",")
                json.dump(line, j_file, indent=ident_value)
            if (i % 10000 == 0 ):
                print ("Convertendo ", i)
            i += 1
            if ((count_limit > 0) and (i >= count_limit)):
                break
        with open(out_file, "a") as j_file:
            j_file.write("]")
  
def main(args):
    arguments(args)
    if ((remove_file) and (os.path.exists(out_file))):                
        os.remove(out_file)  
    convertToJson()    

if __name__ == "__main__":
    main(sys.argv[1:])