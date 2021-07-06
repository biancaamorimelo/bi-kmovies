db.imdb_title_basics.aggregate([
    {
        $lookup: {
            from: "imdb_title_crew",
            localField: "_id",
            foreignField: "_id",
            as: "crew_arr"
        }
    },
    {
        $addFields:{
            directors: {                 
                $arrayElemAt:["$crew_arr.directors", 0]
            },
            writers: {                 
                $arrayElemAt:["$crew_arr.writers", 0]
            },
        }
    },
    {$unset:["crew_arr"]},
    {
        $out: {
            db: "movies", coll: "tmp_imdb"
        }
    }
])