# Library

`gbopyrator` can be used as a python library. Here is a quick example of the main functionality:

## Initialising the reader:

You can choose between two options when initialising the reader: *intantaneous* or *blocking*. *Instantaneous* checks if the reader is connected and raises an error if not. *Blocking* waits as long as the timeout for the reader to be connected before raising an error. You only have to use one!
```python
from gbopyrator import CartridgeReader

# Reader Initialisation
# By default, CartridgeReader is not quiet, but you can set `quiet` to True to avoid outputs
cr = CartridgeReader(quiet=True)

# Reader initialisation

# Instantaneous version
cr.initialize_reader()

# Blocking version
cr.initialize_reader(blocking=True,timeout=10)
```

## Identifying the game:
Epilogue uses a custom ID to identify the game. So I recreated the game database (accessible [here](game_data/gb_gbc_roms_info.json)). You can get the game ID and then search for it in the database.
The ROM info is stored as a dict containing the following information:
| key               | description                                         |
| ----------------- | --------------------------------------------------- |
| `full_title`      | Commercial title of the game                        |
| `title`           | title as stored in the ROM                          |
| `CGB_support`     | Boolean (True if the game as GameBoy Color support) |
| `SGB_support`     | Boolean (True if the game as Super GameBoy support) |
| `cartridge_type`  | Memory layout of the cartridge (which MBC if any)   |
| `ROM_size`        | Size of the ROM                                     |
| `RAM_size`        | Size of the RAM (save)                              |
| `destination`     | Region of the game                                  |
| `ROM_version`     | Version of the ROM                                  |
| `header_checksum` | Checksum of the cartridge header                    |
| `global_checksum` | Checksum of the full ROM                            |

```python
from gbopyrator import load_roms_db

# Load roms database
roms_db = load_roms_db()

# Get cartridge ID
rom_epilogue_id = cr.get_epilogue_id()

# Get rom info if the game is found
if rom_epilogue_id in roms_db:
    rom_info = roms_db[rom_epilogue_id]
    for k in rom_info:
            print(f"{k}:\t {rom_info[k]}")
else:
    print("Game not found in database")
```
## Reading and writing the cartridge
Currently `gbopyrator` supports reading the ROM, reading the RAM (save) dans writing a save file to the RAM. Altough writing a game rom to the ROM is technically possible with flashcards it has not been implemented yet.
You can chose the file extension you want (`.gb`,`.gbc`,`.bin`, etc...)

### Read operations
```python
# dumping the ROM
cr.dump_rom("rom_filename.bin")

# dumping the RAM (save)
cr.dump_save("save_filemname.sav")
```
If you don't want to dump files, you can also dump `bytearrays` with the following commands:
```python
# dump the ROM as a bytearray
rom_array = cr.read_rom()

# dump the RAM as a bytearray
ram_array = cr.read_save()
```

### Write operation
You can write a savefile or a `bytearray` to the RAM.
```python
# With a file
cr.write_save_from_file("save_filemname.sav")

# With a bytearray
save_bytes = ...
cr.write_save(save_bytes)
```