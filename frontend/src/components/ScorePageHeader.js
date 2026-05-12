function ScorePageHeader() {
  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl shadow-sky-950/30 backdrop-blur">
      <div>
          <p className="text-sm font-semibold uppercase tracking-[0.3em] text-cyan-400">NHL Scores</p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
              Game Results
          </h1>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-400">
              View scores and results for NHL games
          </p>
      </div>
    </div>
  );
};

export default ScorePageHeader;