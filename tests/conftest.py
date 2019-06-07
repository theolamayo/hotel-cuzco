import os
import pytest

import pandas as pd

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
ASSETS_DIR = os.path.join(CURR_DIR, "assets")


@pytest.fixture
def get_rooms_clean():
    rooms = pd.read_csv(os.path.join(ASSETS_DIR, "rooms_clean.csv"))
    return rooms


@pytest.fixture
def get_reservations():
    reservations = pd.read_csv(
        os.path.join(ASSETS_DIR, "reservations.csv"),
        parse_dates=["checkin_date", "checkout_date"],
    )
    reservations.loc[:, "checkin_date"] = reservations.checkin_date.dt.date
    reservations.loc[:, "checkout_date"] = reservations.checkout_date.dt.date
    return reservations
