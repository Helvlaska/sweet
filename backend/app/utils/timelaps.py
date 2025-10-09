from datetime import date, timedelta
from flask import current_app as app

def get_time_range(range_type: str, target_date: date | None = None):
    """
    Retourne un tuple (start_date, end_date) selon le type de période demandé.
    - range_type: "day", "week", "month", "3months"
    - target_date: optionnelle, utilisée pour "day"
    """
    today = date.today()

    if range_type == "day":
        if not target_date:
            target_date = today
        app.logger.info("[BACK][utils/timelaps.py][get_time_range()] Plage horaire sur une journée")
        return target_date, target_date

    elif range_type == "week":
        app.logger.info("[BACK][utils/timelaps.py][get_time_range()] Plage horaire sur une semaine")
        return today - timedelta(days=7), today

    elif range_type == "month":
        app.logger.info("[BACK][utils/timelaps.py][get_time_range()] Plage horaire sur un mois")
        return today - timedelta(days=30), today

    elif range_type == "3months":
        app.logger.info("[BACK][utils/timelaps.py][get_time_range()] Plage horaire sur trois mois")
        return today - timedelta(days=90), today

    elif range_type == "6months":
        app.logger.info("[BACK][utils/timelaps.py][get_time_range()] Plage horaire sur six mois")
        return today - timedelta(days=180), today

    elif range_type == "years":
        app.logger.info("[BACK][utils/timelaps.py][get_time_range()] Plage horaire sur 1 an")
        return today - timedelta(days=365), today

    else:
        raise ValueError(f"Type de période invalide : {range_type}")
