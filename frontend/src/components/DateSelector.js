function DateSelector({ onDateChange, selectedDate, minDate, maxDate }) {

    return (
        <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl shadow-sky-950/20">
            <label htmlFor="start" className="block text-sm font-semibold uppercase tracking-[0.2em] text-cyan-400">
                Select Date
            </label>
            <input
                type="date"
                id="start"
                value={selectedDate}
                min={minDate}   
                max={maxDate}  
                onChange={onDateChange}
                className="mt-3 block w-full rounded-lg border border-slate-700 bg-slate-900/60 px-4 py-3 text-white placeholder-slate-500 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
            />
        </div>
    );
}

export default DateSelector;
