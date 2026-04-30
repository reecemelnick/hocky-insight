import { useEffect, useState } from "react";
import GameCard from "../components/GameCard";
import DateSelector from "../components/DateSelector";
import { fetchScores } from "../services/ScoresApi";

function ScoresPage() {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const formattedDate = yesterday.toISOString().split("T")[0];

    const [games, setGames] = useState([]);
    const [date, setDate] = useState(formattedDate);
    const [userMessage, setUserMessage] = useState("");

    useEffect(() => {
        fetchScores(date)
            .then((data) => {
                if (!data || data.length === 0) {
                    setUserMessage("No games today")
                    setGames(data)
                } else {
                    setUserMessage("")
                    setGames(data);
                }
            })
            .catch((err) => console.error(err));
    }, [date]);

    return (
        <div className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-6xl space-y-6">
                <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl shadow-sky-950/30 backdrop-blur">
                    <div>
                        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-cyan-400">NHL Scores</p>
                        <h1 className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
                            Game Results
                        </h1>
                        <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-400">
                            View scores and results for NHL games
                        </p>
                    </div>
                </div>

                <DateSelector onDateChange={setDate} />

                {userMessage && (
                    <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 text-center text-slate-300 shadow-xl shadow-sky-950/20">
                        {userMessage}
                    </div>
                )}

                <div className="space-y-4">
                    {games.map((game, index) => (
                        <GameCard key={index} game={game} />
                    ))}
                </div>
            </div>
        </div>
    );
}

export default ScoresPage;

