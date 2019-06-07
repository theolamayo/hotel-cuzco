import click
import pytest
import datetime

from hotelcuzco.cli_helpers import confirm_date, confirm_room


def test_confirm_single_date():
    assert confirm_date("12/09/2019")
    with pytest.raises(click.BadParameter):
        confirm_date("21-09-2019")
        confirm_date("09/21/2019")
        confirm_date("2019")
        confirm_date("ask")
        confirm_date(2019)


def test_confirm_date_with_minimum():
    assert confirm_date("12/09/2019", datetime.date(2019, 9, 11))
    with pytest.raises(click.BadParameter):
        confirm_date("12/09/2019", datetime.date(2019, 9, 12))
        confirm_date("12/09/2019", datetime.date(2019, 9, 13))


def test_confirm_room():
    assert confirm_room(101, set([101, 102]))
    assert confirm_room("101", set([101, 102]))
    with pytest.raises(click.BadParameter):
        confirm_room("ask", set([101, 102]))
        confirm_room(103, set([101, 102]))
