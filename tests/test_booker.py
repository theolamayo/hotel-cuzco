import datetime

import numpy as np
import pandas as pd

from hotelcuzco.booker import (
    find_rooms_with_enough_capacity,
    find_available_rooms,
    append_reservation,
    check_hotel_open_this_date,
    adapt_date_year_to_reference_date,
    check_hotel_open_between_two_dates,
)


def test_find_rooms_with_enough_capacity(get_rooms_clean):
    adequate_rooms = find_rooms_with_enough_capacity(get_rooms_clean, 3)
    np.testing.assert_array_equal(adequate_rooms.values, np.array([102, 103, 203, 303]))

    adequate_rooms = find_rooms_with_enough_capacity(get_rooms_clean, 1)
    np.testing.assert_array_equal(adequate_rooms.values, get_rooms_clean.room.values)

    adequate_rooms = find_rooms_with_enough_capacity(get_rooms_clean, 15)
    np.testing.assert_array_equal(adequate_rooms.values, np.array([]))


def test_find_available_rooms(get_reservations):
    unknown_rooms = set([2876])
    available_rooms = find_available_rooms(
        get_reservations,
        datetime.date(2018, 10, 21),
        datetime.date(2018, 10, 22),
        unknown_rooms,
    )
    assert available_rooms == unknown_rooms

    booked_rooms = set([101, 102])
    available_rooms = find_available_rooms(
        get_reservations,
        datetime.date(2018, 10, 21),
        datetime.date(2018, 10, 22),
        booked_rooms,
    )
    assert available_rooms == set()

    really_available_room = set([203])
    available_rooms = find_available_rooms(
        get_reservations,
        datetime.date(2018, 10, 21),
        datetime.date(2018, 10, 22),
        really_available_room,
    )
    assert available_rooms == really_available_room


def test_append_reservation():
    initial_reservations = pd.DataFrame(
        {
            "checkin_date": [datetime.date(2018, 10, 21)],
            "checkout_date": [datetime.date(2018, 10, 22)],
            "room": [101],
        }
    )
    expected_reservations = pd.DataFrame(
        {
            "checkin_date": [datetime.date(2018, 10, 21), datetime.date(2018, 10, 31)],
            "checkout_date": [datetime.date(2018, 10, 22), datetime.date(2018, 11, 19)],
            "room": [101, 203],
        }
    )
    returned_reservations = append_reservation(
        initial_reservations,
        datetime.date(2018, 10, 31),
        datetime.date(2018, 11, 19),
        203,
    )
    pd.testing.assert_frame_equal(returned_reservations, expected_reservations)


def test_adapt_date_year_to_reference_date():
    date = datetime.date(1900, 11, 21)
    reference_date = datetime.date(2018, 8, 21)
    expected_date = datetime.date(2018, 11, 21)
    returned_date = adapt_date_year_to_reference_date(date, reference_date)
    assert returned_date == expected_date


def test_check_hotel_open_this_date():
    for day in range(18, 29):
        assert not check_hotel_open_this_date(datetime.date(2018, 10, day))

    assert check_hotel_open_this_date(datetime.date(2019, 3, 21))


def test_check_hotel_open_between_two_dates():
    assert check_hotel_open_between_two_dates(
        datetime.date(2019, 3, 21), datetime.date(2019, 3, 25)
    )
    assert not check_hotel_open_between_two_dates(
        datetime.date(2018, 10, 15), datetime.date(2018, 11, 25)
    )
