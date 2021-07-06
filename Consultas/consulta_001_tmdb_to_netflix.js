db.tmdb_titles.aggregate([
    {
        $lookup: {
            from: "netflix_title",
            localField: "original_title",
            foreignField: "title",
            as: "netflix"
        }
    },
    {
        $addFields:{
            release_date: { 
                $cond:  { 
                    if: {$gte: [{$strLenCP:"$release_date"}, 9]},
                    then: {$dateFromString:{dateString:"$release_date"}},
                    else: ISODate("1800-01-01")
                }
            },
            netflix_count: {
                $size: "$netflix"
            },
            netflix_release_year: {                 
                $arrayElemAt:["$netflix.release_year", 0]                
            },                        
            netflix: {
                $arrayElemAt:["$netflix", 0]            
            }
        }
    },
    // {
    //     $project:{
    //         release_date: { 
    //             $cond:  { 
    //                 if: {$gte: [{$strLenCP:"$release_date"}, 9]},
    //                 then: {$dateFromString:{dateString:"$release_date"}},
    //                 else: ISODate("1900-01-01")
    //             }
    //         },            
    //         title: "$title",
    //         original_title: "$original_title",
    //         netflix_count: {$size: "$netflix"},
    //         netflix_release_year: {                 
    //             $arrayElemAt:["$netflix.release_year", 0]                
    //         },                        
    //         netflix: {
    //             $arrayElemAt:["$netflix", 0]
    //         }
    //     }
    // },
    {
            $addFields:{
                release_year: {
                        $year: "$release_date"
                },
                dif_date: {
                    $abs: {
                        $subtract: [{$year: "$release_date"} , "$netflix_release_year"]
                    }
                }
            }
    },{
        $match: {            
            netflix_count: {$eq:1},
            dif_date: {$lt: 3}
            
        }
    }
//     ,{
//         $count: "count"
//     }
 ])
            
