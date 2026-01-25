from flaskr.db import get_db
class EloRetriever:

    def get_elo_for_team(self, name):
        db = get_db()

        team = db.execute(
            "SELECT elo FROM elo WHERE team_name = ?", (name,)
        ).fetchone()

        return team
    
    def get_ranked_by_elo(self):
        db = get_db()

        ranked = db.execute(
            "SELECT team_name, elo FROM elo ORDER BY elo DESC;"
        )

        return ranked
    
