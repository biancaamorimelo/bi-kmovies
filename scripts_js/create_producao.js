db.netflix_title.aggregate([
    {$project:{
        imdb_id: "$imdb_id",
        tipo: "$type",
        titulo: "title",
        pais: "$country",
        data_adicao: "$date_added",
        data_lancamento: "$release_year",
        classificacao: "$rating",
        duracao: "$duration",
        genero: "$listed_in",
        sinopse: "$desciption"        
    }},
    {$out: {
        db: "movies", coll: "producoes"
    }}
])