from datetime import datetime

import pytest
from dateutil.relativedelta import relativedelta

from zhaostephen.vdts._internal.cli.main import main
from zhaostephen.vdts.fuzzytimedelta import (
    TIME_INTERVAL_CODES,
    get_fuzzy_time_delta_from_time_interval_code,
)
from zhaostephen.vdts.printer import get_string_from_time_interval_code


def test_cli_help_exits_cleanly(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0
    assert "usage" in capsys.readouterr().out.lower()


@pytest.mark.parametrize("code", TIME_INTERVAL_CODES)
def test_every_interval_code_has_a_fuzzy_delta(code):
    fuzzy = get_fuzzy_time_delta_from_time_interval_code(code)
    assert isinstance(fuzzy.delta, relativedelta)
    assert isinstance(fuzzy.margin, relativedelta)


def test_unknown_interval_code_is_rejected():
    with pytest.raises(ValueError):
        get_fuzzy_time_delta_from_time_interval_code("x")
    with pytest.raises(ValueError):
        get_string_from_time_interval_code("x", datetime(2024, 1, 1))


@pytest.mark.parametrize(
    ("code", "expected"),
    [
        ("y", "2024"),
        ("m", "2024-07 (July 2024)"),
        ("d", "2024-07-15"),
    ],
)
def test_interval_labels(code, expected):
    assert get_string_from_time_interval_code(code, datetime(2024, 7, 15)) == expected
