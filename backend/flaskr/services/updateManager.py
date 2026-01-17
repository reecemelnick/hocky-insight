from flaskr.db import get_db
from datetime import date, timedelta
from .eloManager import EloManager

class UpdateManager():
    
    def run_daily_tasks_if_needed(self):

        last_row = self.get_last_date()
        last_run = last_row["last_update"] if last_row else None
        todays_date_string = date.today().isoformat()

        if last_run is None or todays_date_string > last_run:
            
            # basically run proccess_day on yesterday
            elo = EloManager()
            yesterday = date.today() - timedelta(days=1)
            elo.run_though_day(yesterday)

            print("Updating last date")
            self.save_last_update_date(todays_date_string)

    # get last time elo was updated
    def get_last_date(self):
        db = get_db()
        date = db.execute(
            "SELECT * FROM updates ORDER BY id DESC LIMIT 1"
        ).fetchone()

        return date

    # save last date updated 
    def save_last_update_date(self, date):
        db = get_db()
        db.execute(
            """
            INSERT INTO updates (last_update)
            VALUES (?)       
            """,
            (date,)
        )
        db.commit()
