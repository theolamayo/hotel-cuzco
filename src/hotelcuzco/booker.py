import datetime

import pandas as pd

START_ANNUAL_CLOSING = datetime.date(1900, 10, 18)
END_ANNUAL_CLOSING = datetime.date(1900, 10, 28)


def find_rooms_with_enough_capacity(rooms, nb_guests):
    adequate_rooms = rooms.loc[rooms.capacity >= nb_guests, "room"]
    return adequate_rooms


def find_available_rooms(reservations, checkin_date, checkout_date, adequate_rooms):
    checking_condition = checkin_date >= reservations.checkout_date
    checkout_condition = checkout_date <= reservations.checkin_date

    unavailable_rooms = reservations.loc[
        ~(checking_condition | checkout_condition), "room"
    ]

    available_rooms = set(adequate_rooms) - set(unavailable_rooms)
    return available_rooms


def append_reservation(reservations, checkin_date, checkout_date, room):
    updated_reservations = reservations.append(
        {"checkin_date": checkin_date, "checkout_date": checkout_date, "room": room},
        ignore_index=True,
    )
    return updated_reservations


def adapt_date_year_to_reference_date(date, reference_date):
    adapted_date = date.replace(year=reference_date.year)
    return adapted_date


def check_hotel_open_this_date(date):
    start_annual_closing = adapt_date_year_to_reference_date(START_ANNUAL_CLOSING, date)
    end_annual_closing = adapt_date_year_to_reference_date(END_ANNUAL_CLOSING, date)

    hotel_is_open = date not in pd.date_range(
        start=start_annual_closing, end=end_annual_closing, freq="D"
    )
    return hotel_is_open


def check_hotel_open_between_two_dates(checkin_date, checkout_date):
    start_annual_closing = adapt_date_year_to_reference_date(
        START_ANNUAL_CLOSING, checkin_date
    )
    end_annual_closing = adapt_date_year_to_reference_date(
        END_ANNUAL_CLOSING, checkout_date
    )
    return not (
        (checkin_date < start_annual_closing) and (checkout_date > end_annual_closing)
    )
