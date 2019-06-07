import pandas as pd

from hotelcuzco.inout import load_reservations, load_rooms

from .conftest import ASSETS_DIR


def test_load_rooms(get_rooms_clean):
    loaded_rooms = load_rooms(ASSETS_DIR, filename="rooms_raw.csv")
    pd.testing.assert_frame_equal(loaded_rooms, get_rooms_clean)


def test_load_reservations(get_reservations):
    loaded_reservations = load_reservations(ASSETS_DIR, filename="reservations.csv")
    pd.testing.assert_frame_equal(loaded_reservations, get_reservations)
