"""Tests for classfinder script."""

import pytest
from datetime import datetime, timedelta
import classfinder

month_term_dict = {
    1 : 'j-term',
    2 : 'spring',
    3 : 'spring',
    4 : 'spring',
    5 : 'spring',
    6 : 'summer',
    7 : 'summer',
    8 : 'summer',
    9 : 'fall',
    10 : 'fall',
    11 : 'fall',
    12 : 'fall',
}

def test_get_year_term():
    days_prev = 4 * 365
    days_next = 4 * 365
    today = datetime.today()
    date_range = [today - timedelta(days=x) for x in range(days_prev)] + [today + timedelta(days=x) for x in range(days_next)]
    for day in date_range:
        assert classfinder.get_year_term(day) == (day.year, month_term_dict[day.month])

@pytest.mark.parametrize('term_str', [
    'fall', 'summer', 'spring', 'j-term',
    'FALL', 'SUMMER', 'SPRING', 'J-TERM',
    'Fall', 'Summer', 'Spring', 'J-term',
    'J-Term',
])
def test_term_str_to_code(term_str):
    term_dict = {
        'fall' : 40,
        'summer' : 30,
        'spring' : 20,
        'j-term' : 10,
    }
    assert classfinder.term_str_to_code(term_str) == term_dict[term_str.lower()]

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

