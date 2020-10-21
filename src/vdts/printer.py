from datetime import datetime
from vdts.fuzzytimedelta import TIME_INTERVAL_CODES


def get_string_from_time_interval_code(time_interval_code: str, t: datetime) -> str:
    if time_interval_code not in TIME_INTERVAL_CODES:
        raise ValueError(f'time_interval_code "{time_interval_code}"" must be in TIME_INTERVAL_CODES')
    elif time_interval_code == 'y':
        return t.strftime('%Y')
    elif time_interval_code == 'q':
        return f"{t.strftime('%Y')}-Q{t.month // 3 + 1}"
    elif time_interval_code == 'm':
        return t.strftime('%Y-%m (%B %Y)')
    elif time_interval_code == 'w':
        return t.strftime('Week of %Y-%m-%d (week #%U)')
    elif time_interval_code == 'd':
        return t.strftime('%Y-%m-%d')
    else:
        raise NotImplementedError(f'time_interval_code "{time_interval_code}"is in TIME_INTERVAL_CODES, but not implemented')
