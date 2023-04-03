# %%
import usb.core
import usb.util
from rich import print
from coms_utils import read_bulk_in, write_save

IN_ENDPOINT = 0x81
OUT_ENDPOINT = 0x01

dev = usb.core.find(idVendor=0x1D50, idProduct=0x6018)

if dev is None:
    raise ValueError("Device not found")

if dev.is_kernel_driver_active(0):
    dev.detach_kernel_driver(0)

dev.set_configuration()

# %%

write_save(dev, "gbcam.sav")
# %%
dev.write(OUT_ENDPOINT, bytearray([0x04]))
# %%
out = read_bulk_in(dev)
print(out)
# %%
with open("output.bin", "wb") as f:
    f.write(bytearray(out))
# %%


# %%
# Free the device
usb.util.dispose_resources(dev)


# %%
interface_idx = 1  # voir 'print(dev)' pour trouver l'interface
usb.util.claim_interface(dev, interface_idx)
# %%
# usb.util.release_interface(dev, interface_idx)
# %%
gbcam_data_string = """
02 00 00 00 10 00 00 00 02 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 4b 84 6b ef
"""

ltk_data_string = """
02 01 00 00 00 01 00 02 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 cc 23 19 5d
"""

default_data_string = """
02 01 00 00 00 01 00 02 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
"""

small_data_string = """
02 01 00 00 00 01 00 02 00 00 00 00 00 00 00 00
"""

ultra_small_data_string = """
02
"""

# Convert string to list of bytes in hexadecimal format
str_bytes_list = small_data_string.replace("\n", " ").strip().split(" ")
# Convert list of bytes in hexadecimal format to list of bytes
bytes_list = [int(b, 16) for b in str_bytes_list]

# 64 null bytes
null_bytes_list = bytearray([0x00] * 64)

# %%
IN_ENDPOINT = 0x81
OUT_ENDPOINT = 0x01

# trigger save dump
dev.write(OUT_ENDPOINT, bytes_list)

# # burn first 64 bytes
# _ = dev.read(IN_ENDPOINT, 64)

# %%
# receive save dump

all_data = []

# Burn first 64 bytes in 2 times
received_data = dev.read(IN_ENDPOINT, 60)
received_data = dev.read(IN_ENDPOINT, 4)

# %%
while True:
    print("While loop")
    for i in range(64):
        print("for loop")
        try:
            received_data = dev.read(IN_ENDPOINT, 60)
            all_data.extend(list(received_data))
            received_data = dev.read(IN_ENDPOINT, 60)
            all_data.extend(list(received_data))
            received_data = dev.read(IN_ENDPOINT, 60)
            all_data.extend(list(received_data))
            received_data = dev.read(IN_ENDPOINT, 60)
            all_data.extend(list(received_data))
            received_data = dev.read(IN_ENDPOINT, 16)
            all_data.extend(list(received_data))
        except usb.core.USBTimeoutError:
            break
    # Break if last cycle was not full
    if i < 63:
        print(i)
        break
    # else:
    # dev.write(OUT_ENDPOINT, null_bytes_list)
# %%

iter = 0
# Read data until GB Operator stops responding
while True:
    print(f"Iteration {iter}")
    iter += 1
    try:
        received_data = dev.read(IN_ENDPOINT, 64)
        all_data.extend(list(received_data))
    except usb.core.USBTimeoutError:
        break

# %%
print(all_data)

# %%
with open("my_dump2.bin", "wb") as f:
    f.write(bytearray(all_data))


# %%

# set the divice in the same state as after the "find".
usb.util.dispose_resources(dev)
# %%
# This scripts sends command to the GB Operator
# to dump a game save file
import usb.core
import usb.util

# Find GB Operator with vendor ID and product ID
# Those values can be found with `lsusb`
dev = usb.core.find(idVendor=0x1D50, idProduct=0x60)

# Detach kernel drivers
dev.detach_kernel_driver(0)

# Activate first configuration
dev.set_configuration()

trigger_bytes = bytearray([0x02, 0x01, 0x00, ..., 0x00])

# Define USB Bulk IN and OUT endpoints
IN_ENDPOINT = 0x81
OUT_ENDPOINT = 0x01

# Send trigger_bytes
dev.write(OUT_ENDPOINT, trigger_bytes)

received_data = []

# Read data until GB Operator stops responding
while True:
    try:
        usbpacket_data = dev.read(IN_ENDPOINT, 64)
        received_data.extend(list(usbpacket_data))
    except usb.core.USBTimeoutError:
        break

# Save dumped data
with open("game.sav", "wb") as f:
    f.write(bytearray(received_data))
# %%
# Free the device
usb.util.dispose_resources(dev)

# %%
