# %%
import argparse
from .cartridge_utils import CartridgeReader
from gbopyrator import load_roms_db

# %%
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dump-rom", type=str, default=None, help="Dump ROM to file")
    parser.add_argument("--dump-save", type=str, default=None, help="Dump save to file")
    parser.add_argument(
        "--write-save", type=str, default=None, help="Write save from file"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        default=False,
        help="Do not output anything to stdout",
    )
    args = parser.parse_args()

    # %%

    cr = CartridgeReader(quiet=args.quiet)

    cr.printer.greetings()

    if (args.dump_save is not None) and (args.write_save is not None):
        cr.printer.warning(
            "`dump-save` and `write-save` are both set. GBOpyrator will dump the save first and write it after."
        )
    cr.initialize_reader_blocking()

    rom_epilogue_id = cr.get_epilogue_id()
    roms_db = load_roms_db()

    # Print cartridge info
    if rom_epilogue_id in roms_db:
        rom_info = roms_db[rom_epilogue_id]
        # Center "rom info" text on =80 chars
        cr.printer.print("")
        cr.printer.rule("[blue_violet]CARTRIDGE INFO")
        cr.printer.print(
            f"""Detected game:\t[blue_violet]{rom_info['full_title']}[/blue_violet]"""
        )
        if rom_info["SGB_support"]:
            cr.printer.print(f"""SGB support:\t[blue_violet]Yes[/blue_violet]""")
        if rom_info["CGB_support"]:
            cr.printer.print(f"""CGB support:\t[blue_violet]Yes[/blue_violet]""")
        cr.printer.print(
            f"""ROM size:\t[blue_violet]{rom_info['ROM_size']}[/blue_violet]"""
        )
        if rom_info["RAM_size"] != 0:
            cr.printer.print(
                f"""RAM size:\t[blue_violet]{rom_info['RAM_size']}[/blue_violet]"""
            )
    else:
        cr.printer.warning(
            f"ROM epilogue ID not found in the database. If you know the game, please add it to the database."
        )

    # Print dumping/writing info
    if (
        args.dump_save is not None
        or args.dump_rom is not None
        or args.write_save is not None
    ):
        cr.printer.print("")
        cr.printer.rule("[blue_violet]ROM AND SAVE OPERATIONS")

        if args.dump_save is not None:
            cr.dump_save(args.dump_save)

        if args.dump_rom is not None:
            cr.dump_rom(args.dump_rom)

        if args.write_save is not None:
            cr.write_save_from_file(args.write_save)

        cr.close()

    cr.printer.print("")


# %%

if __name__ == "__main__":
    main()
