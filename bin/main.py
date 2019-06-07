import os
from hotelcuzco.commands import main_command


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(current_dir, "../data")
    main_command(data_dir)
