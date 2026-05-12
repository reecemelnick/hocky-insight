function PositionPredictionToggle( { position, handlePositionChange } ) {
  
  const positions = [
    { label: "All", value: "all" },
    { label: "Forwards", value: "forwards" },
    { label: "Defencemen", value: "defencemen" },
  ];

  return (
    <div className="inline-flex rounded-xl border border-slate-700 bg-slate-900 p-1">
      {positions.map((pos) => (
        <button
          key={pos.value}
          onClick={() => handlePositionChange(pos.value)}
          className={`rounded-lg px-4 py-2 text-sm font-medium transition-colors duration-150 ${
            position === pos.value
              ? "bg-cyan-500 text-white"
              : "text-slate-300 hover:bg-slate-800"
          }`}
        >
          {pos.label}
        </button>
      ))}
    </div>
  );
}

export default PositionPredictionToggle;