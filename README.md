# gbopyrator: a Python module to control the GB Operator

⚠️ Under development

## Information

`gbopyrator` is a Python package that enables you to control the GB Operator from [Epilogue](https://www.epilogue.co/) via the command line.
Currently, `gbopyrator` is only compatible with **GameBoy** and **GameBoy Color** games. Support for GameBoy Advance is in development!
## Installation
```bash
pip install gbopyrator
```
## Usage
```bash
gbopyrator \
    --dump-rom rom.gb               # dump the ROM to rom.gb file \
    --dump-save save.sav            # dump the RAM (save) to file \
    --write-save save_backup.sav    # read the file save_backup.sav and upload it to the cartridge RAM (save) \
```