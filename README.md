# gbopyrator: a command line tool and library for the GB Operator

![](imgs/gbopyrator_demo.gif)

## ℹ️ Information

GBOpyrator is a versatile Python package that allows you to manage and control the GB Operator from [Epilogue](https://www.epilogue.co/) via the command line. It currently supports **GameBoy** and **GameBoy Color** games, with GameBoy Advance compatibility in the works!

GBOpyrator is also available as a **library** so that you can integrate it into your own projects!

## ⬇️ Installation

```bash
pip install gbopyrator
```

## 🕹️ Usage

### As a CLI tool

Each flag is optional. Running `gbopyrator` without any flags simply outputs the cartridge info. Here is an example of all the available flags or options.

```bash
gbopyrator \
    --dump-rom rom.gb               # dump the ROM to rom.gb file \
    --dump-save save.sav            # dump the RAM (save) to file \
    --write-save save_backup.sav    # read the file save_backup.sav and upload it to the cartridge RAM (save) \
```

### As a library

For detailed information on utilising GBOpyrator as a **library**, please refer to the [DOC.md](DOC.md) file.
