import React, { useEffect, useState } from "react";
import GameCard from "./components/GameCard";
import DateSelector from "./components/DateSelector";

function App() {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const formattedDate = yesterday.toISOString().split("T")[0];

    const [games, setGames] = useState([]);
    const [date, setDate] = useState(formattedDate);

    useEffect(() => {
    // function to get yesterday's date in YYYY-MM-DD
    const getYesterday = () => {
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        return yesterday.toISOString().split("T")[0];
    };

    fetch(`http://127.0.0.1:8000/scores?date=${date}`)
        .then((res) => res.json())
        .then((data) => {
            if (!data || data.length === 0) {
                // backend returned nothing → reset date to yesterday
                const yesterdayDate = getYesterday();
                console.log("No games returned, falling back to yesterday:", yesterdayDate);
                setDate(yesterdayDate);
            } else {
                setGames(data);
            }
        })
        .catch((err) => console.error(err));
}, [date]);

    return (
        <div>
            <h1>NHL Games</h1>
            <DateSelector onDateChange={setDate} />
            <p>Selected date: {date}</p>
            {games.map((game, index) => (
                <GameCard key={index} game={game} />
            ))}
        </div>
    );
}

export default App;
