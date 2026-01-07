import React, { useState } from "react";

function DateSelector({ onDateChange }) {
    // Max = yesterday
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const maxDate = yesterday.toISOString().split("T")[0];

    // Min = NHL season start (example)
    const minDate = "2025-10-07"; // adjust to your needs

    const [selectedDate, setSelectedDate] = useState(maxDate);

    const handleChange = (event) => {
        setSelectedDate(event.target.value);
        if (onDateChange) {
            onDateChange(event.target.value);
        }
    };

    return (
        <div>
            <label htmlFor="start">Select Date:</label>
            <input
                type="date"
                id="start"
                value={selectedDate}
                min={minDate}   
                max={maxDate}  
                onChange={handleChange}
            />
        </div>
    );
}

export default DateSelector;
