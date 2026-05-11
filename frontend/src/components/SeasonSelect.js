function SeasonSelect( { season, handleSeasonChange} ) {
  return (
    <form className="">
      <label htmlFor="season">Season:</label>
      <select
          id="season"
          value={season}
          onChange={handleSeasonChange}
          className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-slate-100 m-4"
      >
          <option value="20252026">2025-2026</option>
          <option value="20262027">2026-2027</option>
      </select>
    </form>
  )
}

export default SeasonSelect;