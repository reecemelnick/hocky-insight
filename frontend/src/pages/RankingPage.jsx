import { useEffect, useState } from "react";
import { fetchRankings } from "../services/RankingsApi";
import { fetchStandings } from "../services/StandingsApi";
import RankingBoard from "../components/RankingBoard"
import StandingsBoard from "../components/StandingsBoard";
import '../styles.css';

function RankingPage() {
    const NUMBER_OF_TEAMS = 32;

    const [rank, setRank] = useState([])
    const [standings, setStandings] = useState([])
    const [seeds, setSeed] = useState([])

    useEffect(() => {
         fetchRankings()
            .then((data) => {
                setRank(data)
            })
            .catch((err) => console.log(err))
    }, [])

    // useEffect(() => {
    //     if (standings) {
    //         handleData(standings)
    //     }
    // }, [standings])

    useEffect(() => {
         fetchStandings()
            .then((data) => {
                setStandings(data)
                fillRankDict(data)
            })
            .catch((err) => console.log(err))
    }, [])

    const fillRankDict = (standings) => {
        let tmp_seeds = {};
        if (standings) {
            for (let i = 0; i < NUMBER_OF_TEAMS; i++) {
                tmp_seeds[standings[i]["team_name"]] = (i+1);
            } 
            setSeed(tmp_seeds)
        }   
    }

    return (
        <div>
            <h1>Elo Rating vs NHL Standings</h1>
            <div className="rankings-container">
                <StandingsBoard standings={standings} />
                <RankingBoard rankings={rank} seeds={seeds} />
            </div>
        </div>
    )
}

export default RankingPage;