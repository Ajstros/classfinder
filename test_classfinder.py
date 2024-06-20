"""Tests for classfinder script."""

import random
from datetime import datetime, timedelta

import pytest

import classfinder

month_term_dict = {
    1: "j-term",
    2: "spring",
    3: "spring",
    4: "spring",
    5: "spring",
    6: "summer",
    7: "summer",
    8: "summer",
    9: "fall",
    10: "fall",
    11: "fall",
    12: "fall",
}


def test_get_year_term():
    days_prev = 4 * 365
    days_next = 4 * 365
    today = datetime.today()
    date_range = [today - timedelta(days=x) for x in range(days_prev)] + [
        today + timedelta(days=x) for x in range(days_next)
    ]
    for day in date_range:
        assert classfinder.get_year_term(day) == (day.year, month_term_dict[day.month])


@pytest.mark.parametrize(
    "term_str",
    [
        "fall",
        "summer",
        "spring",
        "j-term",
    ],
)
def test_term_str_to_code(term_str):
    term_dict = {
        "fall": 40,
        "summer": 30,
        "spring": 20,
        "j-term": 10,
    }
    term_code = term_dict[term_str]

    # Now randomize capitalization
    num_caps = random.randint(0, len(term_str))
    remaining_chars = list(range(0, len(term_str)))
    for n in range(num_caps):
        char_pos = random.choice(remaining_chars)
        remaining_chars.remove(char_pos)
        term_str = (
            term_str[0:char_pos] + term_str[char_pos].upper() + term_str[char_pos + 1 :]
        )

    assert classfinder.term_str_to_code(term_str) == term_code


@pytest.mark.skip()
def test_get_classes():
    assert False


@pytest.mark.skip()
def test_read_major_classes():
    assert False


@pytest.mark.skip()
def test_read_taken_classes():
    assert False


@pytest.mark.skip()
def test_select_major_classes():
    assert False


@pytest.mark.skip()
def test_select_not_taken_classes():
    assert False


@pytest.mark.skip()
def test_get_major_classes():
    assert False
