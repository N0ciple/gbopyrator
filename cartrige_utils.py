import binascii
import time
import re
from rich.console import Console
import coms_utils as cu
from printer import Printer


def check_initialized(func):
    def wrapper(*args, **kwargs):
        if args[0].initialized:
            return func(*args, **kwargs)
        else:
            raise Exception(
                "Reader not initialized, call initialize_reader() or initialize_reader_blocking() first"
            )

    return wrapper


def release_device(func):
    def wrapper(*args, **kwargs):
        output = func(*args, **kwargs)
        cu.release_gb_operator(args[0].gbop_device)
        return output

    return wrapper


def get_cartridge_info(func):
    def wrapper(*args, **kwargs):
        cartridge_info = cu.read_cartridge_info(args[0].gbop_device)
        if cartridge_info is None:
            raise Exception(
                "Could not read cartridge info. Make sure a cartridge is inserted."
            )

        return func(*args, cartridge_info=cartridge_info, **kwargs)

    return wrapper


class CartridgeReader(object):
    def __init__(self, quiet=False):
        self.initialized = False
        self.console = Console()
        self.quiet = quiet
        self.printer = Printer(quiet=quiet)

    def initialize_reader(self):
        with self.printer.status("Initializing reader..."):
            dev = cu.find_gb_operator()

        if dev is None:
            raise ValueError(
                """
                GB Operator not found, check it is plugged in or that the appropriate udev rules are set up if you are on linux. See : https://support.epilogue.co/hc/en-us/articles/4403827118738-How-can-I-connect-my-Operator-device-on-Linux-under-a-non-root-user-
                """
            )
        else:
            self.gbop_device = cu.init_gb_operator(dev)
            self.initialized = True
            self.printer.success("[bold green]Reader initialized[/bold green]")

        return

    def initialize_reader_blocking(self, timeout=0):
        with self.printer.status("Initializing reader..."):
            dev = cu.find_gb_operator_blocking(timeout=timeout)
        if dev is None:
            raise ValueError(
                """
                GB Operator not found, check it is plugged in or that the appropriate udev rules are set up if you are on linux. See : https://support.epilogue.co/hc/en-us/articles/4403827118738-How-can-I-connect-my-Operator-device-on-Linux-under-a-non-root-user-
                """
            )
        else:
            self.gbop_device = cu.init_gb_operator(dev)
            self.initialized = True
            self.printer.success("[bold green]Reader initialized[/bold green]")
        return

    @check_initialized
    @release_device
    def read_cartridge_info(self):
        # with self.printer.status("Reading cartridge info..."):
        _cartridge_info = cu.read_cartridge_info(self.gbop_device)
        return _cartridge_info

    @check_initialized
    @release_device
    @get_cartridge_info
    def read_rom(self, cartridge_info=None):
        # with self.printer.status("Reading ROM..."):
        num_bytes = cartridge_info["ROM_size"]
        return cu.read_rom(self.gbop_device, num_bytes, quiet=self.quiet)

    def dump_rom(self, filename):
        rom = self.read_rom()
        with open(filename, "wb") as f:
            f.write(rom)
        self.printer.success(f"ROM dumped to:\t[dark_cyan]{filename}[/dark_cyan]")

    @check_initialized
    @release_device
    @get_cartridge_info
    def read_save(self, cartridge_info=None):
        num_bytes = cartridge_info["RAM_size"]
        if num_bytes == 0:
            self.printer.error("No RAM (save) detected on this cartridge.")
            return None
        else:
            # with self.printer.status("Reading save..."):
            return cu.read_save(self.gbop_device, num_bytes, quiet=self.quiet)

    def dump_save(self, filename):
        save = self.read_save()
        if save is not None:
            with open(filename, "wb") as f:
                f.write(save)
            self.printer.success(f"Save dumped to:\t[dark_cyan]{filename}[/dark_cyan]")

    @check_initialized
    @release_device
    @get_cartridge_info
    def write_save(self, data, cartridge_info=None):
        num_bytes = cartridge_info["RAM_size"]
        if num_bytes == 0:
            self.printer.error(
                "No RAM (save) detected on this cartridge. Impossible to write save."
            )
            return None
        elif num_bytes != len(data):
            self.printer.error(
                f"Save size mismatch. Expected {num_bytes} bytes, got {len(data)} bytes."
            )
            return None
        # with self.printer.status("Writing save..."):
        return cu.write_save(self.gbop_device, data, quiet=self.quiet)

    def write_save_from_file(self, filename):
        with open(filename, "rb") as f:
            data = f.read()
        time.sleep(1)
        out = self.write_save(data)
        if out is not None:
            self.printer.success(
                f"Save written from:\t[dark_cyan]{filename}[/dark_cyan]"
            )

    def close(self):
        self.gbop_device.attach_kernel_driver(0)

    @check_initialized
    @get_cartridge_info
    def get_epilogue_id(self, cartridge_info=None):
        epilogue_id = (
            cartridge_info["title_first_letter"].upper()
            + "{:02x}".format(cartridge_info["heasder_checksum"]).upper()
            + binascii.hexlify(cartridge_info["global_checksum"]).decode().upper()
        )
        return epilogue_id


def file_crc32(filename):
    with open(filename, "rb") as f:
        data = f.read()
    out = binascii.crc32(data) & 0xFFFFFFFF
    return hex(out)


def bytearray_crc32(data):
    out = binascii.crc32(data) & 0xFFFFFFFF
    return hex(out)


def create_crc_db(filename):
    with open(filename, "r") as f:
        content = f.read()
    game_regex = re.compile(
        r'game \(\n\tcomment "(.*)"\n\tpublisher "(.*)"\n\trom \( crc (.*) \)\n\)'
    )
    games = game_regex.findall(content)
    db = {}
    for game in games:
        db[game[2]] = game
    return db


if __name__ == "__main__":
    import time

    from rich.progress import Progress

    with Progress() as progress:
        task1 = progress.add_task("[red]Downloading...", total=1000)
        task2 = progress.add_task("[green]Processing...", total=1000)
        task3 = progress.add_task("[cyan]Cooking...", total=1000)

        while not progress.finished:
            progress.update(task1, advance=0.5)
            progress.update(task2, advance=0.3)
            progress.update(task3, advance=0.9)
            time.sleep(0.02)
    # import time
    # from rich.progress import track

    # for i in track(range(20), description="Processing..."):
    #     time.sleep(1)  # Simulate work being done

    # cr = CartridgeReader()
    # cr.initialize_reader_blocking()
    # print(cr.read_cartridge_info())
    # out = cr.read_rom()
    # print(len(out))
    # # cr.dump_rom("test_dump.rom")
    # # cr.dump_save("test_dump.sav")
    # # cr.dump_save("TESTsave.bin")
    # # cr.write_save_from_file("assets/ltk.sav")
    # cr.close()
