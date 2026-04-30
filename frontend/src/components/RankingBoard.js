import Emoji from "./Emoji";

function RankingBoard( {rankings, seeds} ) {

    return (
        <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl shadow-sky-950/20 overflow-hidden">
            <div className="mb-4">
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-400">Elo Ratings</p>
                <h2 className="mt-2 text-xl font-bold text-white">Power Rankings</h2>
            </div>
            <div className="overflow-x-auto">
                <table className="w-full text-sm">
                    <thead>
                        <tr className="border-b border-slate-700">
                            <th className="px-4 py-3 text-left font-semibold text-slate-300">Rank</th>
                            <th className="px-4 py-3 text-left font-semibold text-slate-300">Team</th>
                            <th className="px-4 py-3 text-right font-semibold text-slate-300">Elo</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rankings.map((item, index) => (
                            <tr key={index} className="border-b border-slate-800/50 hover:bg-slate-800/30 transition-colors">
                                <td className="px-4 py-3 font-semibold text-white">
                                    <Emoji symbol={seeds[item.team_name] > (index+1) ? "⬆️" : seeds[item.team_name] < (index+1) ? "🔻" : "🟰"} /> {index + 1}
                                </td>
                                <td className="px-4 py-3 text-white">{item.team_name}</td>
                                <td className="px-4 py-3 text-right font-bold text-cyan-400">{Math.round(item.elo)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    )
}

export default RankingBoard;