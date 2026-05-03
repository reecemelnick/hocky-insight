import { useEffect, useState } from "react";
import { fetchPrediction } from "../services/predictionApi";

function GamePredictorPage() {
    const [predictions, setPredictions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const playersPerPage = 10;

    useEffect(() => {
        fetchPrediction()
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
    }, []);

    const startIndex = (currentPage - 1) * playersPerPage;
    const endIndex = startIndex + playersPerPage;
    const displayedPlayers = predictions.slice(startIndex, endIndex);
    const totalPages = Math.ceil(predictions.length / playersPerPage);

    return (
        <div className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-6xl space-y-6">
                <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl shadow-sky-950/30 backdrop-blur">
                    <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
                        <div>
                            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-cyan-400">Box Pool Helper</p>
                            <h1 className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
                                2025 Points Per Game vs Model Projection
                            </h1>
                        </div>
                        <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 px-4 py-3 text-sm text-cyan-100">
                            {predictions.length} players ({currentPage} of {totalPages})
                        </div>
                    </div>
                </div>

                {loading && (
                    <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-8 text-center text-slate-300 shadow-xl shadow-sky-950/20">
                        Loading predictions...
                    </div>
                )}

                {error && (
                    <div className="rounded-3xl border border-rose-500/30 bg-rose-500/10 p-6 text-rose-100 shadow-xl shadow-rose-950/20">
                        {error}
                    </div>
                )}

                {!loading && !error && (
                    <div className="overflow-hidden rounded-3xl border border-slate-800 bg-slate-900/80 shadow-2xl shadow-sky-950/20">
                        <div className="overflow-x-auto">
                            <table className="min-w-full divide-y divide-slate-800 text-left">
                                <thead className="bg-slate-950/60">
                                    <tr>
                                        <th className="px-6 py-4 text-xs font-semibold uppercase tracking-[0.25em] text-slate-400">Name</th>
                                        <th className="px-6 py-4 text-xs font-semibold uppercase tracking-[0.25em] text-slate-400">2025 PPG</th>
                                        <th className="px-6 py-4 text-xs font-semibold uppercase tracking-[0.25em] text-slate-400">Predicted PPG</th>
                                        <th className="px-6 py-4 text-xs font-semibold uppercase tracking-[0.25em] text-slate-400">Games Played</th>
                                        <th className="px-6 py-4 text-xs font-semibold uppercase tracking-[0.25em] text-slate-400">Delta</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-800">
                                    {displayedPlayers.map((player, index) => {
                                        const actualPpg = player.ppg == null ? null : Number(player.ppg);
                                        const predictedPpg = player.predicted_ppg == null ? null : Number(player.predicted_ppg);
                                        const delta = actualPpg == null || predictedPpg == null ? null : actualPpg - predictedPpg;

                                        return (
                                            <tr
                                                key={`${player.name}-${index}`}
                                                className="transition-colors duration-150 hover:bg-slate-800/60"
                                            >
                                                <td className="px-6 py-4 font-medium text-white">{player.name}</td>
                                                <td className="px-6 py-4 text-slate-300">{actualPpg == null ? "-" : actualPpg.toFixed(3)}</td>
                                                <td className="px-6 py-4 text-slate-300">{predictedPpg == null ? "-" : predictedPpg.toFixed(3)}</td>
                                                <td className="px-6 py-4 text-slate-300">{player.games_played == null ? "-" : player.games_played}</td>
                                                <td className={`px-6 py-4 font-semibold ${delta == null ? "text-slate-400" : delta >= 0 ? "text-emerald-400" : "text-rose-400"}`}>
                                                    {delta == null ? "-" : delta.toFixed(3)}
                                                </td>
                                            </tr>
                                        );
                                    })}
                                </tbody>
                            </table>
                        </div>

                        <div className="flex items-center justify-between border-t border-slate-800 bg-slate-950/60 px-6 py-4">
                            <button
                                onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                                disabled={currentPage === 1}
                                className="rounded-lg border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-medium text-slate-300 transition-colors hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                Previous
                            </button>
                            <span className="text-sm text-slate-400">Page {currentPage} of {totalPages}</span>
                            <button
                                onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                                disabled={currentPage === totalPages || totalPages === 0}
                                className="rounded-lg border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-medium text-slate-300 transition-colors hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                Next
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )   
}

export default GamePredictorPage;