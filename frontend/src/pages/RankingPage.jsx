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
        <div className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-7xl space-y-6">
                <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl shadow-sky-950/30 backdrop-blur">
                    <div>
                        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-cyan-400">NHL Rankings</p>
                        <h1 className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
                            Elo Rating vs NHL Standings
                        </h1>
                        <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-400">
                            Compare team power rankings with official NHL standings
                        </p>
                    </div>
                </div>

                <div className="grid gap-6 lg:grid-cols-2">
                    <StandingsBoard standings={standings} />
                    <RankingBoard rankings={rank} seeds={seeds} />
                </div>
            </div>
        </div>
    )
}

export default RankingPage;