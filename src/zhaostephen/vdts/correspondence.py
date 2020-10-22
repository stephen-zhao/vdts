from dataclasses import dataclass
from datetime import datetime
from typing import Generator, Generic, Iterable, Optional, TypeVar
from zhaostephen.vdts.fuzzytimedelta import FuzzyTimeDelta


CORRESPONDENCE_KINDS = [
    'okay', 'missing', 'extra'
]


TData = TypeVar('TData')
@dataclass
class Correspondence(Generic[TData]):
    correspondence_kind: str
    data: TData


def create_okay_correspondence(data: TData):
    return Correspondence(
        correspondence_kind='okay',
        data=data
    )

def create_missing_correspondence(data: TData):
    return Correspondence(
        correspondence_kind='missing',
        data=data
    )

def create_extra_correspondence(data: TData):
    return Correspondence(
        correspondence_kind='extra',
        data=data
    )


def get_correspondence_with_fuzzy_regular_timeseries(
    maybe_timeseries: Iterable[datetime],
    expected_interval: FuzzyTimeDelta,
    start_timepoint: Optional[datetime] = None,
    end_timepoint: Optional[datetime] = None,
) -> Generator[Correspondence[datetime], None, Optional[datetime]]:

    if start_timepoint is not None and end_timepoint is not None and start_timepoint > end_timepoint:
        raise ValueError('end_timepoint must be in the future of start_timepoint.')

    # Begin the time series at the time point of the oldest timepoint or the start timepoint if provided
    subject_ts = iter(maybe_timeseries)
    try:
        subject_ts_curr_point = next(subject_ts)
    except StopIteration:  # Empty subject
        # If either time range point is not given, then there is
        # no way to check the empty time series, because there is no
        # good way to determine when it starts/ends without at least one
        # subject timepoint.
        if start_timepoint is None or end_timepoint is None:
            return None
        # Otherwise we just return "missing" files for all timepoints between
        # start and end.
        else:
            subject_ts_curr_point = None

    expected_ts_curr_point = start_timepoint if start_timepoint is not None else subject_ts_curr_point
    latest_reported_point = None

    # If subjects exist, then gradually step through time to determine whether subjects are okay/extra/missing
    if subject_ts_curr_point is not None:
        while True:
            try:
                if end_timepoint is not None and (expected_ts_curr_point > end_timepoint or subject_ts_curr_point > end_timepoint):
                    return latest_reported_point
                if expected_ts_curr_point - expected_interval.margin <= subject_ts_curr_point <= expected_ts_curr_point + expected_interval.margin:
                    latest_reported_point = subject_ts_curr_point
                    yield create_okay_correspondence(subject_ts_curr_point)
                    expected_ts_curr_point = subject_ts_curr_point + expected_interval.delta
                    subject_ts_curr_point = next(subject_ts)
                elif expected_ts_curr_point + expected_interval.margin < subject_ts_curr_point:
                    latest_reported_point = expected_ts_curr_point
                    yield create_missing_correspondence(expected_ts_curr_point)
                    expected_ts_curr_point += expected_interval.delta
                elif subject_ts_curr_point < expected_ts_curr_point - expected_interval.margin:
                    latest_reported_point = subject_ts_curr_point
                    yield create_extra_correspondence(subject_ts_curr_point)
                    subject_ts_curr_point = next(subject_ts)
                else:
                    raise ValueError('Invalid expected_ts_curr_point or subject_ts_curr_point')
            except StopIteration:
                break
        # If end time is not provided, we finish after the last subject (or missing subject) is processed
        if end_timepoint is None:
            return latest_reported_point
        # Otherwise, we continue on, starting from the next expected timepoint
        else:
            expected_ts_curr_point += expected_interval.delta

    # We process until we reach the end timepoint
    if end_timepoint is not None:
        while expected_ts_curr_point + expected_interval.margin < end_timepoint:
            latest_reported_point = expected_ts_curr_point
            yield create_missing_correspondence(expected_ts_curr_point)
            expected_ts_curr_point += expected_interval.delta
    
    return latest_reported_point