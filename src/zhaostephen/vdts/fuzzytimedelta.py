from dataclasses import dataclass
from dateutil.relativedelta import relativedelta


TIME_INTERVAL_CODES = [
    'y', 'q', 'm', 'w', 'd'
]


@dataclass
class FuzzyTimeDelta:
    delta: relativedelta
    margin: relativedelta


_timeIntervalCodeToFuzzyTimeDelta = {
    'y': FuzzyTimeDelta(relativedelta(years=1), relativedelta(months=1)),
    'q': FuzzyTimeDelta(relativedelta(months=3), relativedelta(months=1)),
    'm': FuzzyTimeDelta(relativedelta(months=1), relativedelta(weeks=1)),
    'w': FuzzyTimeDelta(relativedelta(weeks=1), relativedelta(days=3)),
    'd': FuzzyTimeDelta(relativedelta(days=1), relativedelta(hours=10)),
}


def get_fuzzy_time_delta_from_time_interval_code(time_interval_code: str) -> FuzzyTimeDelta:
    if time_interval_code not in TIME_INTERVAL_CODES:
        raise ValueError('time_interval_code must be in TIME_INTERVAL_CODES')
    try:
        return _timeIntervalCodeToFuzzyTimeDelta[time_interval_code]
    except:
        raise NotImplementedError('time_interval_code is in TIME_INTERVAL_CODES, but not implemented')
