function StandingsBoard( {standings} ) {

    return (
        <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl shadow-sky-950/20 overflow-hidden">
            <div className="mb-4">
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-400">NHL Standings</p>
                <h2 className="mt-2 text-xl font-bold text-white">Official Standings</h2>
            </div>
            <div className="overflow-x-auto">
                <table className="w-full text-sm">
                    <thead>
                        <tr className="border-b border-slate-700">
                            <th className="px-4 py-3 text-left font-semibold text-slate-300">Rank</th>
                            <th className="px-4 py-3 text-left font-semibold text-slate-300">Team</th>
                            <th className="px-4 py-3 text-center font-semibold text-slate-300">W</th>
                            <th className="px-4 py-3 text-center font-semibold text-slate-300">L</th>
                            <th className="px-4 py-3 text-center font-semibold text-slate-300">OTL</th>
                            <th className="px-4 py-3 text-right font-semibold text-slate-300">Points</th>
                        </tr>
                    </thead>
                    <tbody>
                        {standings.map((item, index) => (
                            <tr key={index} className="border-b border-slate-800/50 hover:bg-slate-800/30 transition-colors">
                                <td className="px-4 py-3 font-semibold text-cyan-400">{index + 1}</td>
                                <td className="px-4 py-3 font-semibold text-white">{item.team_name}</td>
                                <td className="px-4 py-3 text-center text-emerald-400 font-bold">{item.wins}</td>
                                <td className="px-4 py-3 text-center text-red-400 font-bold">{item.loss}</td>
                                <td className="px-4 py-3 text-center text-slate-400 font-bold">{item.otLoss}</td>
                                <td className="px-4 py-3 text-right font-bold text-sky-400">{item.points}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    )
}

export default StandingsBoard;