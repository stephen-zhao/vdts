from datetime import datetime
from datetime_matcher import DatetimeMatcher
import os
from pathlib import Path
from typing import Dict


def extract_timeseries_from_directory(dir_path: Path, file_pattern: str) -> Dict[datetime, str]:
    # Get list of files in directory
    files = list(file for file in os.listdir(str(dir_path)) if (dir_path / file).is_file())
    
    # Extract the datetimes
    dtmatcher = DatetimeMatcher()
    timepoint_files = list((dtmatcher.extract_datetime(file_pattern, file), file) for file in files)

    # Filter out Nones as those without a datetime cannot be a part of the time series
    timepoint_to_file = dict((timepoint, file) for timepoint, file in timepoint_files if timepoint is not None)

    return timepoint_to_file
