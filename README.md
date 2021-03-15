# SGCC (Sega Genesis Checksum Corrector)

A [Sega Genesis] ROM checksum corrector.

## Prerequisites

- [Python](https://www.python.org/downloads/windows)

## Usage

Script can be run on any platform that can run **Python**. By default the ROM
file will not be changed and it will create a new file with `_cc` appended to
the filename. You can supply either `-i` or `--in-place` to have it modify the
ROM in-place or supply `-s` or `--suffix` to change the default appented suffix
to something else.

### Windows

```cmd
python sgcc.py [-i|--in-place] [-s|--suffix] [path to ROM file]
```

### Linux

```bash
./sgcc.py [-i|--in-place] [-s|--suffix] [path to ROM file]
```

<!-- links -->
[Sega Genesis]: https://en.wikipedia.org/wiki/Sega_Genesis
