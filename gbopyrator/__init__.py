from .cartridge_utils import CartridgeReader
from pkg_resources import resource_filename
import json

__version__ = "0.3"

def load_roms_db(filename=resource_filename(__name__, "gb_gbc_roms_info.json")):
    with open(filename, "r") as file:
        roms_db = json.load(file)
    return roms_db
