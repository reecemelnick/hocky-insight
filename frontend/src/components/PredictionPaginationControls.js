function PredictionPaginationControls( {currentPage, setCurrentPage, predictions} ) {
  return (
    <div className="flex items-center justify-between border-t border-slate-800 bg-slate-950/60 px-6 py-4">
      <button
          onClick={() => setCurrentPage((prev) => Math.max(1, prev - 1))}
          disabled={currentPage === 1}
          className="rounded-lg border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-medium text-slate-300 transition-colors hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed"
      >
          Previous
      </button>
      <span className="text-sm text-slate-400">Page {currentPage}</span>
      <button
          onClick={() => setCurrentPage((prev) => prev + 1)}
          disabled={predictions.length < 10}
          className="rounded-lg border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-medium text-slate-300 transition-colors hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed"
      >
          Next
      </button>
    </div>
  );
}

export default PredictionPaginationControls;