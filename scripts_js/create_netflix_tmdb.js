db.netflix_title.aggregate([
    {
        $lookup: {
            from: "imdb_title_basics",
            let: {                                
                netflix_title: "$title",
                netflix_year: "$release_year",
                netflix_type: {$toLower: "$type"}
            },
            pipeline:[
                {
                    $match:{
                        $expr:{ 
                            $and: [
                                {$eq: ["$$netflix_title", "$primary_title"]},
                                {$eq: ["$$netflix_year",  "$start_year"]},
                                {$eq: ["$$netflix_type",  {$toLower: "$title_type"}]}
                            ]
                        }
                    },
                }
                
             ],
            as: "imdb"
        }
    },
    {$addFields: {count_size: {$size:  "$imdb"}}},
    {$match: {count_size: {$eq:1}}},    
    {$unset: "count_size"},    
    {$unwind:"$imdb"},
    {$addFields: {imdb_id: "$imdb._id"}},
    {$unset: "imdb"},
    {$out: {db: "movies", coll: "netflix_imdb"}}
])