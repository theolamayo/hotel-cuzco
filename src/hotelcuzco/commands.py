from .cli import ask_full_booking
from .inout import load_reservations, load_rooms, save_reservation


def main_command(data_dir):
    rooms = load_rooms(data_dir)
    reservations = load_reservations(data_dir)
    updated_reservations = ask_full_booking(rooms, reservations)
    save_reservation(updated_reservations, data_dir)
