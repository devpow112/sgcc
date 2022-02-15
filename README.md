# SGCC (Sega Genesis Checksum Corrector)

A [Sega Genesis] ROM checksum corrector.

## Prerequisites

- [Python]

## Usage

Script can be run on any platform that can run **Python**. By default the ROM
file will not be changed and it will create a new file with `_cc` appended to
the filename. You can supply either `-i` or `--in-place` to have it modify the
ROM in-place or supply `-s` or `--suffix` to change the default appended suffix
to something else.

```console
usage: [python] sgcc.py [-h] [-i] [-s SUFFIX] path

Compares and corrects the checksum for a Sega Genesis ROM.

positional arguments:
  path                  Relative path to the Sega Genesis ROM file.

optional arguments:
  -h, --help            show this help message and exit
  -i, --in-place        Make header change in-place, otherwise make another file
  -s SUFFIX, --suffix SUFFIX
                        Custom suffix to use when not doing in-place fixing
```

<!-- links -->
[Sega Genesis]: https://en.wikipedia.org/wiki/Sega_Genesis
[Python]: https://www.python.org/downloads/windows
