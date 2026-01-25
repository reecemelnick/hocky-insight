import { useEffect, useState } from "react";
import { fetchRankings } from "../services/RankingsApi";
import RankingBoard from "../components/RankingBoard"

function RankingPage() {

    const [rank, setRank] = useState([])

    useEffect(() => {
         fetchRankings()
            .then((data) => {
                setRank(data)
            })
            .catch((err) => console.log(err))
    }, [])


    return (
        <div>
            <h1>Elo Rating vs NHL Standings</h1>
            <RankingBoard rankings={rank} />
        </div>
    )
}

export default RankingPage;