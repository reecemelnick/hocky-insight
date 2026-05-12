import { useEffect, useState } from "react";
import { fetchPrediction } from "../services/predictionApi";
import GamePredictorHeader from "../components/GamePredictorHeader";
import PredictionTable from "../components/PredictionTable";
import PredictionPaginationControls from "../components/PredictionPaginationControls";
import ErrorCard from "../components/ErrorCard";
import PredictionLoading from "../components/PredictionLoading";

function GamePredictorPage() {
    const [predictions, setPredictions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const [season, setSeason] = useState("20262027");
    const [sortBy, setSortBy] = useState("predicted_ppg");
    const [sortDirection, setSortDirection] = useState("DESC");
    const [position, setPosition] = useState("all");

    useEffect(() => {
        setLoading(true);
        fetchPrediction(currentPage, season, sortBy, sortDirection, position)
            .then((data) => {
                setPredictions(data || []);
                setError("");
            })
            .catch((err) => {
                console.error(err);
                setError("Failed to load predictions.");
            })
            .finally(() => {
                setLoading(false);
            });
    }, [currentPage, season, sortBy, sortDirection, position]);

    const handlePositionChange = (position) => {
        setPosition(position)
    };

    const handleSeasonChange = (e) => {
        setSeason(e.target.value)
    };

    const handleSortChange = (value) => {
        setSortBy(value);
    };

    const toggleDirection = () => {
        setSortDirection(prev => (prev === "ASC" ? "DESC" : "ASC"));
    };

    return (
        <div className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-6xl space-y-6">
                
                <GamePredictorHeader season={season} handleSeasonChange={handleSeasonChange} currentPage={currentPage} position={position} handlePositionChange={handlePositionChange} />

                {loading && <PredictionLoading />}

                {error && <ErrorCard error={error} />}

                {!loading && !error && (
                    <div className="overflow-hidden rounded-3xl border border-slate-800 bg-slate-900/80 shadow-2xl shadow-sky-950/20">
                        <PredictionTable predictions={predictions} season={season} handleSortChange={handleSortChange} toggleDirection={toggleDirection} sortBy={sortBy} sortDirection={sortDirection} />
                        <PredictionPaginationControls currentPage={currentPage} setCurrentPage={setCurrentPage} predictions={predictions} />
                    </div>
                )}
            </div>
        </div>
    )   
}

export default GamePredictorPage;