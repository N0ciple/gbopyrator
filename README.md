# gbopyrator: manage your GB Operator with Python🐍

![](imgs/gbopyrator_demo.gif)

## ℹ️ Information

GBOopyrator is a Python package that enables you to control the GB Operator from [Epilogue](https://www.epilogue.co/) via the command line.
Currently, `gbopyrator` is only compatible with **GameBoy** and **GameBoy Color** games. Support for GameBoy Advance is in development!
GBOpyrator can also be utilised as a library in your own projects.

## ⬇️ Installation
```bash
pip install gbopyrator
```
## 🕹️ Usage
### As a CLI tool
```bash
gbopyrator \
    --dump-rom rom.gb               # dump the ROM to rom.gb file \
    --dump-save save.sav            # dump the RAM (save) to file \
    --write-save save_backup.sav    # read the file save_backup.sav and upload it to the cartridge RAM (save) \
```
### As a library
Refer to the [DOC.md](DOC.md) file for information on using GBOpyrator as a library.