from datetime import datetime

import pytest

from zhaostephen.vdts.printer import get_string_from_time_interval_code


@pytest.mark.parametrize(
    ("month", "expected_quarter"),
    [
        (1, 1), (2, 1), (3, 1),
        (4, 2), (5, 2), (6, 2),
        (7, 3), (8, 3), (9, 3),
        (10, 4), (11, 4), (12, 4),
    ],
)
def test_quarter_label(month: int, expected_quarter: int) -> None:
    t = datetime(2024, month, 15)
    assert get_string_from_time_interval_code('q', t) == f"2024-Q{expected_quarter}"
