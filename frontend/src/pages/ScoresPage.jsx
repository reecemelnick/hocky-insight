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
        <div>
            <h1>NHL Games</h1>
            <h3>{userMessage}</h3>

            <DateSelector onDateChange={setDate} />
            <p>Selected date: {date}</p>

            {games.map((game, index) => (
                <GameCard key={index} game={game} />
            ))}
        </div>
    );
}

export default ScoresPage;

