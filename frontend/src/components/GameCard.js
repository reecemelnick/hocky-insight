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
    <div style={{ marginBottom: "20px" }}>
      <img src={game.away_logo} alt={game.away_name} width={50} />
      <strong>({game.away_elo}){game.away_name}</strong>: {game.away_score} <Emoji symbol={away_result} /> vs
      <img src={game.home_logo} alt={game.home_name} width={50} />
      <strong>({game.home_elo}){game.home_name}</strong>: {game.home_score} <Emoji symbol={home_result} />
    </div>
  );
}

export default GameCard;
