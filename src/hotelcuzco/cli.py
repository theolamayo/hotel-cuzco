from functools import partial

import click
from tabulate import tabulate

from .booker import (
    append_reservation,
    find_available_rooms,
    find_rooms_with_enough_capacity,
)
from .cli_helpers import FORMAT, confirm_date, confirm_room


def ask_full_booking(rooms, reservations):
    nb_guests = ask_number_of_guests()
    adequate_rooms = find_rooms_with_enough_capacity(rooms, nb_guests)

    if adequate_rooms.empty:
        click.echo(f"No adequate room for {nb_guests} guests in our hotel.")
        sys.exit(0)

    checkin_date, checkout_date = ask_dates()

    available_rooms = find_available_rooms(
        reservations, checkin_date, checkout_date, adequate_rooms
    )
    if not available_rooms:
        click.echo(
            f"No available rooms for {nb_guests} guests between {checkin_date}"
            f" and {checkout_date}."
        )
        sys.exit(0)
    else:
        rooms_to_propose = rooms[rooms.room.isin(available_rooms)]
        click.echo("Available rooms:")
        click.echo(tabulate(rooms_to_propose, headers=rooms_to_propose.columns))

    chosen_room = ask_room_to_book(available_rooms)

    updated_reservations = append_reservation(
        reservations, checkin_date, checkout_date, chosen_room
    )
    click.echo(f"{chosen_room} was reserved between {checkin_date} and {checkout_date}")
    return updated_reservations


def ask_dates():
    checkin_date = click.prompt(f"Checkin date ({FORMAT})", value_proc=confirm_date)
    checkout_date = click.prompt(
        f"Checkout date ({FORMAT})",
        value_proc=partial(confirm_date, minimum=checkin_date),
    )
    return checkin_date, checkout_date


def ask_number_of_guests():
    nb_guests = click.prompt("Number of guests", type=int)
    return nb_guests


def ask_room_to_book(available_rooms):
    chosen_room = click.prompt(
        "Enter a room to book",
        type=int,
        value_proc=partial(confirm_room, available_rooms=available_rooms),
    )
    return chosen_room
