import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
from zhaostephen.vdts._internal.exceptions import CliInvalidArgumentError
from zhaostephen.vdts.fuzzytimedelta import TIME_INTERVAL_CODES


@dataclass
class CliMainArgs:
    in_dir_path: Path
    interval_code: str
    is_end_now: bool
    file_pattern: str


def _create_invalid_arguments_msg(argparser: argparse.ArgumentParser, argument_dict: Dict[str, str], details: Optional[str]) -> str:
    msg = []

    if len(argument_dict) == 0:
        pass
    elif len(argument_dict) == 1:
        for arg_name, arg_val in argument_dict.items():
            msg.append(f'Invalid argument: {arg_name} = {arg_val}')
    else:
        msg.append('Invalid arguments:')
        for arg_name, arg_val in argument_dict.items():
            msg.append(f'    {arg_name} = {arg_val}')

    if len(argument_dict) > 0:
        msg.append('')

    if details is not None:
        msg.append(details)
        msg.append('')

    msg.append(argparser.format_usage())

    return '\n'.join(msg)


def _create_argparser(program_name: str) -> argparse.ArgumentParser:
    argparser = argparse.ArgumentParser(
        prog=program_name,
        description="Check for missing files by datetime in a time-series.",
    )
    argparser.add_argument('-i', '--interval', nargs='?', choices=TIME_INTERVAL_CODES, default='m', help='The interval at which points should occur in the time series. Defaults to monthly (m).')
    argparser.add_argument('-n', '--end-now', action='store_true', help='Use the current time as the endpoint of the time series.')
    argparser.add_argument('in_dir', help='The input directory to verify as a time series.')
    argparser.add_argument('file_pattern', help='A dfregex which determines relevent files and extracts the necessary datetimes from the file names.')
    return argparser


def parse_args(program_name: str, args: List[str]) -> CliMainArgs:
    argparser = _create_argparser(program_name)
    parsed_args = argparser.parse_args(args)

    # Validate in_dir
    in_dir_path = Path(parsed_args.in_dir)
    if in_dir_path.is_file():
        raise CliInvalidArgumentError(_create_invalid_arguments_msg(
            argparser,
            {'in_dir': parsed_args.in_dir},
            'Input directory cannot be a file.',
        ))
    if not in_dir_path.is_dir():
        raise CliInvalidArgumentError(_create_invalid_arguments_msg(
            argparser,
            {'in_dir': parsed_args.in_dir},
            'Input directory is not a valid directory.',
        ))

    return CliMainArgs(
        in_dir_path=in_dir_path,
        interval_code=parsed_args.interval,
        is_end_now=parsed_args.end_now,
        file_pattern=parsed_args.file_pattern
    )
