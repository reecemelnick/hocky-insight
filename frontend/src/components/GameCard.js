import React from "react";
import Emoji from "./Emoji";

function GameCard({ game }) {

  let away_result;
  let home_result;
  if (game.winner === game.away_name) {
    away_result = "✅";
    home_result = "❌"
  } else {
    away_result = "❌";
    home_result = "✅"
  }

  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl shadow-sky-950/20 transition-colors duration-150 hover:bg-slate-800/80">
      <div className="flex items-center justify-between gap-6">
        <div className="flex flex-1 items-center gap-4">
          <img src={game.away_logo} alt={game.away_name} width={60} className="rounded-lg" />
          <div className="flex-1">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">Away</p>
            <h3 className="mt-1 text-lg font-bold text-white">{game.away_name}</h3>
            <p className="mt-1 text-sm text-slate-400">ELO: {game.away_elo}</p>
          </div>
          <div className="text-3xl font-bold text-emerald-400">{game.away_score}</div>
          <div className="text-2xl"><Emoji symbol={away_result} /></div>
        </div>

        <div className="border-l border-slate-700"></div>

        <div className="flex flex-1 items-center justify-end gap-4">
          <div className="text-2xl"><Emoji symbol={home_result} /></div>
          <div className="text-3xl font-bold text-emerald-400">{game.home_score}</div>
          <div className="flex-1 text-right">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">Home</p>
            <h3 className="mt-1 text-lg font-bold text-white">{game.home_name}</h3>
            <p className="mt-1 text-sm text-slate-400">ELO: {game.home_elo}</p>
          </div>
          <img src={game.home_logo} alt={game.home_name} width={60} className="rounded-lg" />
        </div>
      </div>
    </div>
  );
}

export default GameCard;
