import os

import pandas as pd


def load_rooms(data_dir, filename="hotel_cuzco_rooms.csv"):
    hotel_rooms = pd.read_csv(os.path.join(data_dir, filename))
    hotel_rooms.loc[:, "capacity"] = (
        hotel_rooms.capacity.str.split().str.get(0).astype(int)
    )
    return hotel_rooms


def load_reservations(data_dir, filename="reservations.csv"):
    reservations = pd.read_csv(
        os.path.join(data_dir, filename), parse_dates=["checkin_date", "checkout_date"]
    )
    reservations.loc[:, "checkin_date"] = reservations.checkin_date.dt.date
    reservations.loc[:, "checkout_date"] = reservations.checkout_date.dt.date

    return reservations


def save_reservation(reservations, data_dir, filename="reservations.csv"):
    reservations.to_csv(os.path.join(data_dir, filename), index=False)
