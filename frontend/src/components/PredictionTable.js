import PredictionTableRow from "./PredictionTableRow";

function PredictionTable( { predictions, season, handleSortChange, toggleDirection, sortBy} ) {

  const handleHeaderClick = (field) => {
    if (sortBy === field) {
      toggleDirection()
    } else {
      handleSortChange(field)
    }
  } 

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-slate-800 text-left">
          <thead className="bg-slate-950/60">
              <tr>
                  <th onClick={() => handleHeaderClick("name")} className="cursor-pointer hover:text-white px-6 py-4 text-xs font-semibold uppercase tracking-[0.25em] text-slate-400">Name</th>
                  <th className="px-6 py-4 text-xs font-semibold uppercase tracking-[0.25em] text-slate-400">{season} PPG</th>
                  <th className="px-6 py-4 text-xs font-semibold uppercase tracking-[0.25em] text-slate-400">Predicted PPG</th>
                  <th className="px-6 py-4 text-xs font-semibold uppercase tracking-[0.25em] text-slate-400">Games Played</th>
                  <th className="px-6 py-4 text-xs font-semibold uppercase tracking-[0.25em] text-slate-400">Delta</th>
              </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
              {predictions.map((player, index) => {
                  return (
                    <PredictionTableRow player={player} key={index} />
                  );
              })}
          </tbody>
      </table>
    </div>
  )
}

export default PredictionTable;