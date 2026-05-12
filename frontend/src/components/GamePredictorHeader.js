import SeasonSelect from "./SeasonSelect";
import PositionPredictionToggle from "./PredictionPositionToggle";

function GamePredictorHeader( { season, handleSeasonChange, currentPage, position, handlePositionChange } ) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl shadow-sky-950/30 backdrop-blur">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
          <div>
              <p className="text-sm font-semibold uppercase tracking-[0.3em] text-cyan-400">Box Pool Helper</p>
              <h1 className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
                  {season} Points Per Game vs Model Projection
              </h1>

              <SeasonSelect season={season} handleSeasonChange={handleSeasonChange} />
              <PositionPredictionToggle position={position} handlePositionChange={handlePositionChange}/> 
              
          </div>
          <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 px-4 py-3 text-sm text-cyan-100">
              Page {currentPage}
          </div>
      </div>
    </div>
  )
} 

export default GamePredictorHeader;