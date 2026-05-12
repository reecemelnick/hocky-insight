import PredictionTableRow from "./PredictionTableRow";

function PredictionTable( { predictions, season, handleSortChange, toggleDirection, sortBy, sortDirection} ) {

  const handleHeaderClick = (field) => {
    if (sortBy === field) {
      toggleDirection()
    } else {
      handleSortChange(field)
    }
  } 

  const renderSortArrow = (field) => {
    if (sortBy !== field) return null;

    return sortDirection === "ASC" ? " ▲" : " ▼";
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-slate-800 text-left">
          <thead className="bg-slate-950/60">
              <tr>
                  <th onClick={() => handleHeaderClick("name")} className={`cursor-pointer hover:text-white px-6 py-4 text-xs font-semibold uppercase tracking-[0.25em] text-slate-400 ${sortBy === 'name' ? "bg-slate-800 text-white" : "text-slate-400"}`}>Name {renderSortArrow("name")}</th>
                  <th onClick={() => handleHeaderClick("ppg")} className={`cursor-pointer hover:text-white px-6 py-4 text-xs font-semibold uppercase tracking-[0.25em] text-slate-400 ${sortBy === 'ppg' ? "bg-slate-800 text-white" : "text-slate-400"}`}>{season} PPG {renderSortArrow("ppg")}</th>
                  <th onClick={() => handleHeaderClick("predicted_ppg")} className={`cursor-pointer hover:text-white px-6 py-4 text-xs font-semibold uppercase tracking-[0.25em] text-slate-400 ${sortBy === 'predicted_ppg' ? "bg-slate-800 text-white" : "text-slate-400"}`}>Predicted PPG {renderSortArrow("predicted_ppg")}</th>
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