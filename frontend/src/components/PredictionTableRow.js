function PredictionTableRow( { player, index } ) {

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
  )
}

export default PredictionTableRow;