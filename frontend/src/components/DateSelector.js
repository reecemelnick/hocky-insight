import React, { useState } from "react";

function DateSelector({ onDateChange }) {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const maxDate = yesterday.toISOString().split("T")[0];

    const minDate = "2022-10-07";

    const [selectedDate, setSelectedDate] = useState(maxDate);

    const handleChange = (event) => {
        setSelectedDate(event.target.value);
        if (onDateChange) {
            onDateChange(event.target.value);
        }
    };

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
                onChange={handleChange}
                className="mt-3 block w-full rounded-lg border border-slate-700 bg-slate-900/60 px-4 py-3 text-white placeholder-slate-500 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
            />
        </div>
    );
}

export default DateSelector;
