import { useEffect, useState } from "react";
import GameCard from "../components/GameCard";
import DateSelector from "../components/DateSelector";
import { fetchScores } from "../services/ScoresApi";
import ScorePageHeader from "../components/ScorePageHeader";

function ScoresPage() {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const maxDate = yesterday.toISOString().split("T")[0];
    const minDate = '1990-10-10';

    const [games, setGames] = useState([]);
    const [userMessage, setUserMessage] = useState("");
    const [selectedDate, setSelectedDate] = useState(maxDate);

    useEffect(() => {
        fetchScores(selectedDate)
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
    }, [selectedDate]);

    const handleDateChange = (e) => {
        setSelectedDate(e.target.value);
    };

    return (
        <div className="min-h-screen bg-slate-950 overflow-hidden px-4 py-10 text-slate-100 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-6xl space-y-6">
                <ScorePageHeader />
                <DateSelector onDateChange={handleDateChange} selectedDate={selectedDate} minDate={minDate} maxDate={maxDate} />

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

