from flaskr.db import get_db

class PpgPredictRetriever:

    ALLOWED_SORT_COLUMNS = {
        "name": "pp.name",
        "ppg": "ppg",
        "predicted_ppg": "pp.predicted_ppg",
    }

    ALLOWED_ORDERS = ["ASC", "DESC"]

    def get_ppg_predictions(self, page, season, sort_by, order,page_size=10):
        # Hard cap: never fetch more than 10 players at a time
        page_size = min(page_size, 10)

        conn = get_db()
        cursor = conn.cursor()

        query = self.get_prediction_query(season, sort_by, order)

        rows = self.get_prediction_rows(query, cursor, season, page_size, page)

        result = self.build_result(rows)

        return result
    
    def build_result(self, rows):
        result = []

        for row in rows:
            goals = row["goals"] or 0
            assists = row["assists"] or 0
            games_played = row["games_played"]

            ppg = (
                (goals + assists) / games_played
                if games_played and games_played > 0
                else None
            )

            result.append({
                "player_id": row["player_id"],
                "name": row["name"],
                "ppg": ppg,
                "predicted_ppg": row["predicted_ppg"],
                "games_played": games_played,
            })

        return result
    
    def get_prediction_rows(self, query, cursor, season, page_size, page):
        cursor.execute(
            query, 
            (season, page_size, (page - 1) * page_size)
        )
        rows = cursor.fetchall()
        return rows
    

    def get_prediction_query(self, season, sort_by, order):
        prediction_table_name = "player_predictions_" + season

        sort_column = self.ALLOWED_SORT_COLUMNS.get(
            sort_by,
            "pp.predicted_ppg"
        )

        order = order.upper()
        if order not in self.ALLOWED_ORDERS:
            order = "DESC"

        query = f"""
            SELECT
                pp.player_id,
                pp.name,
                pp.predicted_ppg,
                ps.goals,
                ps.assists,
                ps.games_played,

                CASE
                    WHEN ps.games_played > 0
                    THEN CAST(ps.goals + ps.assists AS FLOAT) / ps.games_played
                    ELSE NULL
                END AS ppg

            FROM {prediction_table_name} pp

            LEFT JOIN player_seasons ps
                ON pp.player_id = ps.player_id
                AND ps.season = ?

            ORDER BY {sort_column} {order}

            LIMIT ? OFFSET ?
        """

        return query