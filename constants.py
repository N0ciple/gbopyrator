MBC_TYPES = {
    0x00: "ROM ONLY",
    0x01: "MBC1",
    0x02: "MBC1+RAM",
    0x03: "MBC1+RAM+BATTERY",
    0x05: "MBC2",
    0x06: "MBC2+BATTERY",
    0x08: "ROM+RAM 1",
    0x09: "ROM+RAM+BATTERY 1",
    0x0B: "MMM01",
    0x0C: "MMM01+RAM",
    0x0D: "MMM01+RAM+BATTERY",
    0x0F: "MBC3+TIMER+BATTERY",
    0x10: "MBC3+TIMER+RAM+BATTERY 2",
    0x11: "MBC3",
    0x12: "MBC3+RAM 2",
    0x13: "MBC3+RAM+BATTERY 2",
    0x19: "MBC5",
    0x1A: "MBC5+RAM",
    0x1B: "MBC5+RAM+BATTERY",
    0x1C: "MBC5+RUMBLE",
    0x1D: "MBC5+RUMBLE+RAM",
    0x1E: "MBC5+RUMBLE+RAM+BATTERY",
    0x20: "MBC6",
    0x22: "MBC7+SENSOR+RUMBLE+RAM+BATTERY",
    0xFC: "POCKET CAMERA",
    0xFD: "BANDAI TAMA5",
    0xFE: "HuC3",
    0xFF: "HuC1+RAM+BATTERY",
}

ROM_TYPES = {
    0x00: {"ROM_size_info": "32 KiB", "num_rom_banks": 2},
    0x01: {"ROM_size_info": "64 KiB", "num_rom_banks": 4},
    0x02: {"ROM_size_info": "128 KiB", "num_rom_banks": 8},
    0x03: {"ROM_size_info": "256 KiB", "num_rom_banks": 16},
    0x04: {"ROM_size_info": "512 KiB", "num_rom_banks": 32},
    0x05: {"ROM_size_info": "1 MiB", "num_rom_banks": 64},
    0x06: {"ROM_size_info": "2 MiB", "num_rom_banks": 128},
    0x07: {"ROM_size_info": "4 MiB", "num_rom_banks": 256},
    0x08: {"ROM_size_info": "8 MiB", "num_rom_banks": 512},
}

RAM_TYPES = {
    0x00: {"SRAM_size_info": "0", "info": "No RAM"},
    0x02: {"SRAM_size_info": "8 KiB", "info": "1 bank"},
    0x03: {"SRAM_size_info": "32 KiB", "info": "4 banks of 8 KiB each"},
    0x04: {"SRAM_size_info": "128 KiB", "info": "16 banks of 8 KiB each"},
    0x05: {"SRAM_size_info": "64 KiB", "info": "8 banks of 8 KiB each"},
}

ROM_INFO_SPLIT = "------------------- ROM INFO -------------------"
