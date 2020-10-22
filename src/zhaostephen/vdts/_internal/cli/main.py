from datetime import datetime
import os
import sys
from typing import List, Optional
from zhaostephen.vdts._internal.cli.main_parser import parse_args
from zhaostephen.vdts._internal.exceptions import CliInvalidArgumentError
from zhaostephen.vdts.correspondence import get_correspondence_with_fuzzy_regular_timeseries
from zhaostephen.vdts.filesystem import extract_timeseries_from_directory
from zhaostephen.vdts.fuzzytimedelta import get_fuzzy_time_delta_from_time_interval_code
from zhaostephen.vdts.printer import get_string_from_time_interval_code


PROGRAM_NAME = 'vdts'


def main(argv: Optional[List[str]] = None) -> int:
    program_name = PROGRAM_NAME if os.path.basename(sys.argv[0]) == '__main__.py' else None
    if argv is None:
        argv = sys.argv[1:]

    # Parse args
    try:
        args = parse_args(program_name, argv)
    except CliInvalidArgumentError as e:
        sys.stderr.write('{}'.format(e))
        exit(1)

    # Get the time delta
    fuzzy_interval = get_fuzzy_time_delta_from_time_interval_code(args.interval_code)
    # Get the time series
    timeseries_files = extract_timeseries_from_directory(args.in_dir_path, args.file_pattern)

    # Check if there are any files left
    if len(timeseries_files) == 0:
        print("No files from which a time series could be inferred exist in the provided directory.")
        exit(0)

    end_time = datetime.now() if args.is_end_now else None
    for correspondence in get_correspondence_with_fuzzy_regular_timeseries(sorted(timeseries_files.keys()), fuzzy_interval, end_timepoint=end_time):
        # Display results to user as they come up
        timepoint = correspondence.data
        if correspondence.correspondence_kind == 'missing':
            print(f">>> Missing file for timepoint {get_string_from_time_interval_code(args.interval_code, timepoint)} <<< ❌")
        elif correspondence.correspondence_kind == 'extra':
            print(f">>> Extra file for timepoint {timepoint.isoformat()} <<< ❗")
        else:
            filename = timeseries_files.get(correspondence.data)
            print(f"{filename} <<< ✅")
