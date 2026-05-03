from flaskr.db import get_db
from datetime import date, timedelta
from .eloManager import EloManager

class UpdateManager():
    
    def run_daily_tasks_if_needed(self):
        
        # get last time update was run and compare to todays date
        last_data_updated = self.get_last_date()
        todays_date_string = date.today().isoformat()

        # if update needed
        if last_data_updated is None or todays_date_string > last_data_updated:
            
            self.update_elo() # update elo for all games from yesterday

            self.save_last_update_date(todays_date_string) # save last update date as today
    
    def update_elo(self):
        elo = EloManager()
        yesterday = date.today() - timedelta(days=1)
        elo.run_though_day(yesterday)

    # get last time update was run
    def get_last_date(self):
        db = get_db()
        date_row = db.execute(
            "SELECT * FROM updates ORDER BY id DESC LIMIT 1"
        ).fetchone()
        
        last_run = date_row["last_update"] if date_row else None # ISO format

        return last_run # last date update was run. None if first time running

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
