from flaskr.db import get_db

class PpgPredictRetriever:

    def get_ppg_predictions(self, page, page_size=10):
        # Hard cap: never fetch more than 10 players at a time
        page_size = min(page_size, 10)
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                pp.player_id,
                pp.name,
                pp.predicted_ppg,
                ps.goals,
                ps.assists,
                ps.games_played
            FROM player_predictions pp
            LEFT JOIN player_seasons ps
                ON pp.player_id = ps.player_id
                AND ps.season = '20242025'
            ORDER BY pp.predicted_ppg DESC
            LIMIT ? OFFSET ?
        """, (page_size, (page - 1) * page_size))

        rows = cursor.fetchall()

        result = []
        for row in rows:
            result.append({
                "player_id": row["player_id"],
                "name": row["name"],
                "ppg": (row["goals"] + row["assists"]) / row["games_played"] if row["games_played"] else None,
                "predicted_ppg": row["predicted_ppg"],
                "games_played": row["games_played"],
            })
        
        return result