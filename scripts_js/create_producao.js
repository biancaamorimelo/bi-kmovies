db.netflix_imdb.aggregate([
    {$project:{
        _id: "$imdb_id",
        netflix_id: "$_id",
        tipo: "$type",
        titulo: "$title",
        pais: "$country",
        data_adicao: "$date_added",
        data_lancamento: "$release_year",
        classificacao: "$rating",
        duracao: "$duration",
        genero: "$listed_in",
        sinopse: "$desciption"        
    }}
    //---lookup tmdb--------------------------------------
    ,{$lookup: {
        from: "tmdb_titles",
        localField: "_id",
        foreignField: "_id",
        as: "tmdb"
    }}
    ,{$unwind: "$tmdb"}
    ,{$addFields:{
        idioma_original: "$tmdb.original_language",
        popularidade: "$tmdb.popularity",
        lista_idiomas: "$tmdb.spoken_languages",
        total_votos: "$tmdb.vote_count",
        avaliacao: "$tmdb.vote_average",
        orcamento: "$tmdb.budget",
        produtoras: "$tmdb.production_companies"

    }}
    ,{$unset: "tmdb"}    
    //--------Ator---------------------------------------
    ,{$lookup: {
        from: "imdb_title_principals",
        let:{
            id: "$_id"
        },
        pipeline:[
            {$match: {                
                $expr:{
                    $and: [
                        {$eq:["$$id", "$tconst"]},                        
                        {$in: ["$category", ["actor", "actress"]]}
                    ]
                }
            }}            
            ,{$project:{
                id: "$nconst",  
                _id: 0,
                categoria: "$category",
                papeis: "$characters"
            }}
        ],
        as: "atores"
    }}
    //--------Direção---------------------------------------
    ,{$lookup: {
        from: "imdb_title_principals",
        let:{
            id: "$_id"
        },
        pipeline:[
            {$match: {                
                $expr:{
                    $and: [
                        {$eq:["$$id", "$tconst"]},
                        {$not: {$in: ["$category", ["actor", "actress"]]}}
                    ]
                }
            }}            
            ,{$project:{
                id: "$nconst",  
                _id: 0,
                categoria: "$category",
                papeis: "$characters"
            }}
        ],
        as: "direcao"
    }}
    ,{$out: {db: "movies", coll: "producoes"}}
    
]).pretty()