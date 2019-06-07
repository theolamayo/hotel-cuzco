import click
import pandas as pd

from .booker import check_hotel_open_this_date, START_ANNUAL_CLOSING, END_ANNUAL_CLOSING

FORMAT = "%d/%m/%Y"


def confirm_date(date, minimum=None):
    try:
        date = pd.to_datetime(date, format=FORMAT).date()
    except ValueError:
        raise click.BadParameter("Date format incorrect", param=date)

    if minimum is not None and date <= minimum:
        raise click.BadParameter(
            f"date should be strictly higher than {minimum}", param=date
        )

    if not check_hotel_open_this_date(date):
        raise click.BadParameter(
            f"hotel is closed between {START_ANNUAL_CLOSING.replace(year=date.year)}"
            f" and {END_ANNUAL_CLOSING.replace(year=date.year)}",
            param=date,
        )

    return date


def confirm_room(room, available_rooms):
    try:
        assert int(room) in available_rooms
    except (AssertionError, ValueError):
        raise click.BadParameter(
            f"Please choose an available room {available_rooms}", param=room
        )
    return room
