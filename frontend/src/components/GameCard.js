import React from "react";

function GameCard({ game }) {
  return (
    <div style={{ marginBottom: "20px" }}>
      <img src={game.away_logo} alt={game.away_name} width={50} />
      <strong>({game.away_elo}){game.away_name}</strong>: {game.away_score} vs
      <img src={game.home_logo} alt={game.home_name} width={50} />
      <strong>({game.home_elo}){game.home_name}</strong>: {game.home_score}
    </div>
  );
}

export default GameCard;
