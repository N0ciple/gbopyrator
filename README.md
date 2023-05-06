# gbopyrator: a command line tool and library for the GB Operator

![](imgs/gbopyrator_demo.gif)

## ℹ️ Information

GBOpyrator is a versatile Python package that allows you to manage and control the GB Operator from [Epilogue](https://www.epilogue.co/) via the command line. It currently supports **GameBoy** and **GameBoy Color** games, with GameBoy Advance compatibility in the works! 

GBOpyrator can also be integrated into your own projects as a library.

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
For detailed information on utilizing PyGBOperator as a library, please refer to the [DOC.md](DOC.md) file.