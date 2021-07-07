db.producoes.aggregate([
    //----------Atores
    {$unwind: "$atores"}    
    ,{$lookup:{        
        from: "imdb_name_basics",
        localField: "atores.id",
        foreignField: "_id",
        as: "atores_arr"
    }}    
    ,{$unwind: "$atores_arr"}    
    ,{$addFields:{
        "atores.nome": "$atores_arr.primary_name",
        "atores.ano_nascimento": "$atores_arr.birth_year",
        // "atores.conhecido_por": "$atores_arr.known_for_titles",
        "atores.profissoes": "$atores_arr.primary_profession",
    }}    
    ,{$unset: "atores_arr"}    
    ,{$group:{
        "_id": "$_id",
        "netflix_id" : {"$first":"$netflix_id"},
        "tipo" : {"$first":"$tipo"},
        "titulo" : {"$first":"$titulo"},
        "pais" : {"$first":"$pais"},
        "data_adicao" : {"$first":"$data_adicao"},
        "data_lancamento" : {"$first":"$data_lancamento"},
        "classificacao" : {"$first":"$classificacao"},
        "duracao" : {"$first":"$duracao"},
        "genero" : {"$first":"$genero"},
        "idioma_original" : {"$first":"$idioma_original"},
        "popularidade" : {"$first":"$popularidade"},
        "lista_idiomas" : {"$first":"$lista_idiomas"},
        "total_votos" : {"$first":"$total_votos"},
        "avaliacao" : {"$first":"$avaliacao"},
        "orcamento" : {"$first":"$orcamento"},
        "produtoras" : {"$first":"$produtoras"},
        "atores": {"$push":"$atores"},        
        "direcao" : {"$first":"$direcao"},
    }}
    //---------Direção
    ,{$unwind: "$direcao"}
    ,{$lookup:{        
        from: "imdb_name_basics",
        localField: "direcao.id",
        foreignField: "_id",
        as: "direcao_arr"
    }}
    ,{$unwind: "$direcao_arr"}
    ,{$addFields:{
        "direcao.nome": "$direcao_arr.primary_name",      
        "direcao.ano_nascimento": "$direcao_arr.birth_year",  
        // "direcao.conhecido_por": "$direcao_arr.known_for_titles",
        "direcao.profissoes": "$direcao_arr.primary_profession",
    }}
    ,{$unset: "direcao_arr"}
    ,{$group:{
        "_id": "$_id",
        "netflix_id" : {"$first":"$netflix_id"},
        "tipo" : {"$first":"$tipo"},
        "titulo" : {"$first":"$titulo"},
        "pais" : {"$first":"$pais"},
        "data_adicao" : {"$first":"$data_adicao"},
        "ano_lancamento" : {"$first":"$data_lancamento"},
        "classificacao" : {"$first":"$classificacao"},
        "duracao" : {"$first":"$duracao"},
        "genero" : {"$first":"$genero"},
        "idioma_original" : {"$first":"$idioma_original"},
        "popularidade" : {"$first":"$popularidade"},
        "lista_idiomas" : {"$first":"$lista_idiomas"},
        "total_votos" : {"$first":"$total_votos"},
        "avaliacao" : {"$first":"$avaliacao"},
        "orcamento" : {"$first":"$orcamento"},
        "produtoras" : {"$first":"$produtoras"},     
        "atores" : {"$first":"$atores"},           
        "direcao" : {"$push":"$direcao"}
    }}
    ,{ $out:{db: "movies", coll: "producoes"}}
])