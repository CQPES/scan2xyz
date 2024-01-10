# scan2xyz

Gaussian scan log to multi-frame xyz

## Requirements

- Python 3.8 and above

## Usage

```bash
$ python3 scan2xyz.py -h
usage: scan2xyz.py [-h] -i I -o O

Convert Gaussian scan log to multi-frame xyz.

optional arguments:
  -h, --help  show this help message and exit
  -i I        Input Gaussian scan log
  -o O        Output multi-frame xyz
```

## Example

In folder `example/`, there is a dihedral scan tasks of methanol.

- `methanol_scan.gjf`: Gaussian scan input
- `methanol_scan.out`: Gaussian scan log
- `methanol_scan.xyz`: Converted xyz file

Run the following command, then `methanol_scan.xyz` will be created.

```bash
$ python3 ../src/scan2xyz.py -i methanol_scan.out -o methanol_scan.xyz
```
