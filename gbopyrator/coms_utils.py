import usb.core
import time
from crccheck.crc import Crc32Mpeg2
from .constants import MBC_TYPES, RAM_TYPES, ROM_TYPES
from rich.progress import Progress


# Endpoints definitiions for USB Bulk IN and OUT
IN_ENDPOINT = 0x81
OUT_ENDPOINT = 0x01

# GB Operator Vendor and Product IDs
GB_OPERATOR_VENDOR_ID = 0x1D50
GB_OPERATOR_PRODUCT_ID = 0x6018

# Trigger sequence
TRIGGER_CARTRIDGE_INFO = bytearray(
    [
        0x04,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    ]
)
TRIGGER_SAVE_READ = bytearray(
    [
        0x02,
        0x01,
        0x00,
        0x00,
        0x00,
        0x01,
        0x00,
        0x02,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    ]
)


def _craft_save_write_trigger(save_size):
    """
    Craft a save write trigger

    Parameters
    ----------
    save_size : int

    Returns
    -------
    bytearray
    """

    save_size_bytearray = save_size.to_bytes(
        (save_size.bit_length() + 7) // 8, byteorder="little"
    )
    trigger_save_write = bytearray([0x03, 0x00, 0x00, 0x00, 0x00, 0x00])
    trigger_save_write += save_size_bytearray

    # Add 0x00 to reach 60 bytes
    pad_legnth = 60 - len(trigger_save_write)
    trigger_save_write += bytearray([0x00] * pad_legnth)
    # Add CRC32
    trigger_save_write = add_crc32(trigger_save_write)
    return trigger_save_write


def _craft_rom_read_trigger(rom_size):
    """
    Craft a rom read trigger

    Parameters
    ----------
    rom_size : int

    Returns
    -------
    bytearray
    """

    rom_size_bytearray = rom_size.to_bytes(
        (rom_size.bit_length() + 7) // 8, byteorder="little"
    )
    trigger_rom_read = bytearray([0x00, 0x00])
    trigger_rom_read += rom_size_bytearray

    # Add 0x00 to reach 60 bytes
    pad_legnth = 60 - len(trigger_rom_read)
    trigger_rom_read += bytearray([0x00] * pad_legnth)
    # Add CRC32
    trigger_rom_read = add_crc32(trigger_rom_read)
    return trigger_rom_read


def _craft_save_read_trigger(save_size):
    """
    Craft a save read trigger

    Parameters
    ----------
    save_size : int

    Returns
    -------
    bytearray
    """

    save_size_bytearray = save_size.to_bytes(
        (save_size.bit_length() + 7) // 8, byteorder="little"
    )
    trigger_save_read = bytearray([0x02, 0x00, 0x00, 0x00, 0x00])
    trigger_save_read += save_size_bytearray

    # Add 0x00 to reach 60 bytes
    pad_legnth = 60 - len(trigger_save_read)
    trigger_save_read += bytearray([0x00] * pad_legnth)
    # Add CRC32
    trigger_save_read = add_crc32(trigger_save_read)
    return trigger_save_read


def add_crc32(data):
    """
    Add CRC32 to data

    Parameters
    ----------
    data : bytearray

    Returns
    -------
    bytearray
    """
    crc = Crc32Mpeg2.calc(data)
    bytes_crc = crc.to_bytes((crc.bit_length() + 7) // 8, byteorder="little")
    return data + bytes_crc


def find_gb_operator():
    """
    Find GB Operator device

    Returns
    -------
    usb.core.Device
    """
    # Find GB Operator with vendor ID and product ID
    # Those values can be found with `lsusb`
    return usb.core.find(
        idVendor=GB_OPERATOR_VENDOR_ID, idProduct=GB_OPERATOR_PRODUCT_ID
    )


def find_gb_operator_blocking(timeout=0):
    """
    Block while GB Operator device if not found

    Parameters
    ----------
    timeout : int, optional. If timeout = 0, will nerver timeout

    Returns
    -------
    usb.core.Device
    """

    if timeout == 0:
        while True:
            gbop_device = find_gb_operator()
            if gbop_device is not None:
                return gbop_device
            time.sleep(1)
    else:
        start = time.time()
        while True:
            gbop_device = find_gb_operator()
            if gbop_device is not None:
                return gbop_device
            time.sleep(1)
            if time.time() - start > timeout:
                raise TimeoutError("Unable to find GB Operator device")


def init_gb_operator(gbop_device):
    """
    Initialize GB Operator device

    Parameters
    ----------
    gbop_device : usb.core.Device
    """

    # Check if device is None
    if gbop_device is None:
        raise ValueError("Device not found, you passed a device that is None")

    # Detack kernel driver
    if gbop_device.is_kernel_driver_active(0):
        gbop_device.detach_kernel_driver(0)

    # Activate first configuration
    gbop_device.set_configuration()

    # return device
    return gbop_device


def read_bulk_in(gbop_device, num_bytes=0, with_ack=False, quiet=False):
    """
    Read data from GB Operator device

    Parameters
    ----------
    gbop_device : usb.core.Device
    num_bytes : int, optional

    Returns
    -------
    bytearray
    """
    received_data = bytearray([])

    # Read data until GB Operator stops responding
    iteration = 0

    with Progress(disable=quiet, transient=True) as progress:
        task = progress.add_task("Reading...", total=num_bytes)

        while len(received_data) < num_bytes:
            progress.update(task, advance=64)
            try:
                usbpacket_data = gbop_device.read(IN_ENDPOINT, 64)
                received_data += bytearray(usbpacket_data)
                iteration += 1
            except usb.core.USBTimeoutError:
                print("USBTimeoutError")
                return received_data
            if with_ack and (iteration % 320 == 0):
                # send ACK
                gbop_device.write(OUT_ENDPOINT, bytearray([0x00] * 64))
                # read ACK
                _ = gbop_device.read(IN_ENDPOINT, 60)
                _ = gbop_device.read(IN_ENDPOINT, 4)

    return received_data


def write_bulk_out(gbop_device, data, qiuet=False):
    """
    Write data to GB Operator device

    Parameters
    ----------
    gbop_device : usb.core.Device
    data : bytearray
    """
    with Progress(disable=qiuet, transient=True) as progress:
        task = progress.add_task("Writing...", total=len(data))

        # Write data to GB Operator in chunks of 64 bytes
        for sequence in range(0, len(data), 64):
            progress.update(task, advance=64)
            gbop_device.write(OUT_ENDPOINT, data[sequence : sequence + 64])
            time.sleep(0.0001)
            # Read 64 bytes from GB Operator
            _ = gbop_device.read(IN_ENDPOINT, 60)
            _ = gbop_device.read(IN_ENDPOINT, 4)


def read_cartridge_info(gbop_device):
    """
    Read cartridge info from GB Operator device

    Parameters
    ----------
    gbop_device : usb.core.Device

    Returns
    -------
    dict
    """
    # Send trigger_bytes
    gbop_device.write(OUT_ENDPOINT, TRIGGER_CARTRIDGE_INFO)

    # Burn the ACK
    _ = gbop_device.read(IN_ENDPOINT, 60)
    _ = gbop_device.read(IN_ENDPOINT, 4)

    # Read card data from GB Operator
    received_data = read_bulk_in(gbop_device, num_bytes=256, quiet=True)

    # Extract card info only
    received_data = received_data[:60]

    # check if received_data is all null bytes
    if not (received_data[3] or received_data[4]):
        return None

    if received_data[2] == 0x20:
        # Parse data
        cartridge_info = {
            "cartridge_type": "GB/GBC",
            "ROM_size": int.from_bytes(received_data[5:8], byteorder="little"),
            "RAM_size": int.from_bytes(received_data[9:12], byteorder="little"),
            "title_first_letter": chr(received_data[13]),
            "MBC_type": MBC_TYPES[received_data[14]],
            "ROM_type": ROM_TYPES[received_data[15]],
            "RAM_type": RAM_TYPES[received_data[16]],
            "heasder_checksum": received_data[17],
            "global_checksum": received_data[18:20],
        }
    else:
        cartridge_info = {
            "cartridge_type": "GBA",
            # "ROM_size": int.from_bytes(received_data[5:8], byteorder="little"),
            # "RAM_size": int.from_bytes(received_data[9:12], byteorder="little"),
        }
        raise NotImplementedError("GBA cartridge support not implemented yet")

    return cartridge_info


def read_save(gbop_device, num_bytes, quiet=False):
    """
    Dump save file from GB Operator device

    Parameters
    ----------
    gbop_device : usb.core.Device
    filename : str
    """
    # craft trigger bytes
    trigger_save_read = _craft_save_read_trigger(num_bytes)

    # Send trigger_bytes
    gbop_device.write(OUT_ENDPOINT, trigger_save_read)

    # Burn the first 64 bytes
    # Burn first 64 bytes in 2 times
    _ = gbop_device.read(IN_ENDPOINT, 60)
    _ = gbop_device.read(IN_ENDPOINT, 4)

    # Read data from GB Operator
    received_data = read_bulk_in(gbop_device, num_bytes=num_bytes, quiet=quiet)

    return bytearray(received_data)


def write_save(gbop_device, bytearray_data, quiet=False):
    """
    Write save file to GB Operator device

    Parameters
    ----------
    gbop_device : usb.core.Device
    filename : str
    """
    # craft trigger bytes
    trigger_save_write = _craft_save_write_trigger(len(bytearray_data))

    # Send trigger_bytes
    gbop_device.write(OUT_ENDPOINT, trigger_save_write)

    # Burn the first 64 bytes
    # Burn first 64 bytes in 2 times
    _ = gbop_device.read(IN_ENDPOINT, 60)
    _ = gbop_device.read(IN_ENDPOINT, 4)

    # Write data to GB Operator
    write_bulk_out(gbop_device, bytearray_data, qiuet=quiet)

    return True


def read_rom(gbop_device, num_bytes, quiet=False):
    """
    Dump ROM from GB Operator device

    Parameters
    ----------
    gbop_device : usb.core.Device
    filename : str
    """
    # craft trigger bytes
    trigger_rom_read = _craft_rom_read_trigger(num_bytes)

    # Send trigger_bytes
    gbop_device.write(OUT_ENDPOINT, trigger_rom_read)

    # Burn first 64 bytes in 2 times
    _ = gbop_device.read(IN_ENDPOINT, 60)
    _ = gbop_device.read(IN_ENDPOINT, 4)

    # Send "ACK" to GB Operator
    gbop_device.write(OUT_ENDPOINT, bytearray([0x00] * 64))

    # Burn first 64 bytes a second time
    _ = gbop_device.read(IN_ENDPOINT, 60)
    _ = gbop_device.read(IN_ENDPOINT, 4)

    # Read data from GB Operator
    received_data = read_bulk_in(
        gbop_device, num_bytes=num_bytes, with_ack=True, quiet=quiet
    )

    return bytearray(received_data)


def release_gb_operator(gbop_device):
    """
    Release GB Operator device

    Parameters
    ----------
    gbop_device : usb.core.Device
    """
    # Release device
    usb.util.dispose_resources(gbop_device)
