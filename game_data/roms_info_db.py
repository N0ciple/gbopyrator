import re
import json

ROM_INFO_SPLIT = "------------------- ROM INFO -------------------"


def parse_rom(raw_info):
    dict_info = {}
    dict_info["full_title"] = raw_info[1]
    dict_info["title"] = raw_info[4].split("Title                   ")[1].strip()
    if dict_info["title"] == "":
        return None
    else:
        dict_info["CGB_support"] = False if "(No CGB Support)" in raw_info[5] else True
        dict_info["SGB_support"] = False if "(No SGB Support)" in raw_info[6] else True
        dict_info["cartridge_type"] = raw_info[7].split("Cartridge Type          ")[1]
        dict_info["ROM_size"] = raw_info[8].split("ROM Size                ")[1]
        if "None" in raw_info[9]:
            dict_info["RAM_size"] = 0
        else:
            dict_info["RAM_size"] = raw_info[9].split("RAM Size                ")[1]
        dict_info["destination"] = raw_info[10].split("Destination             ")[1]
        dict_info["ROM_version"] = raw_info[12].split("ROM Version             ")[1]
        dict_info["header_checksum"] = (
            raw_info[13].split("Header Checksum         ")[1].split("(")[0].strip()
        )
        dict_info["global_checksum"] = (
            raw_info[14].split("Global Checksum         ")[1].split("(")[0].strip()
        )
    return dict_info


def build_roms_db(roms_list):
    roms_db = {}
    for rom in roms_list:
        rom_id = (
            rom["title"][0] + rom["header_checksum"][2:] + rom["global_checksum"][2:]
        )
        if rom_id not in roms_db:
            roms_db[rom_id] = [rom]
        else:
            roms_db[rom_id].append(rom)

    return clean_roms_db(roms_db)


def clean_roms_db(roms_db):
    for rom_id in roms_db:
        if len(roms_db[rom_id]) > 1:
            first_elem = roms_db[rom_id][0]
            roms_db[rom_id] = [
                rom for rom in roms_db[rom_id] if "[!]" in rom["full_title"]
            ]
            if len(roms_db[rom_id]) == 0:
                first_elem["full_title"] = re.sub(
                    r"\[[^\]]*\]", "", first_elem["full_title"]
                )
                roms_db[rom_id] = first_elem
            else:
                first_elem = roms_db[rom_id][0]
                first_elem["full_title"] = re.sub(
                    r" ?\[[^\]]*\]", "", first_elem["full_title"]
                )
                roms_db[rom_id] = first_elem

        else:
            first_elem = roms_db[rom_id][0]
            first_elem["full_title"] = re.sub(
                r" ?\[[^\]]*\]", "", first_elem["full_title"]
            )
            roms_db[rom_id] = first_elem
    return roms_db


if __name__ == "__main__":
    with open("./originals/gb_gbc_roms_info.txt", "r") as file:
        data = file.read()
    # skip the first line
    data_list = data.split(ROM_INFO_SPLIT)[1:]

    roms_list = [parse_rom(rom.splitlines()) for rom in data_list]
    roms_list = [rom for rom in roms_list if rom is not None]

    roms_db = build_roms_db(roms_list)

    # dump the db as json file
    with open("../gbopyrator/gb_gbc_roms_info.json", "w") as file:
        json.dump(roms_db, file, indent=4)
