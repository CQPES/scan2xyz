import argparse
import os
from typing import Optional

ELEMENTS = [
    "Bq",
    "H ",                                                                                                                                                                                     "He",
    "Li", "Be",                                                                                                                                                 "B ", "C ", "N ", "O ", "F ", "Ne",
    "Na", "Mg",                                                                                                                                                 "Al", "Si", "P ", "S ", "Cl", "Ar",
    "K ", "Ca", "Sc", "Ti", "V ", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",                                                                                     "Ga", "Ge", "As", "Se", "Br", "Kr",
    "Rb", "Sr", "Y ", "Zr", "Nb", "Mo", "Te", "Ru", "Rh", "Pd", "Ag", "Cd",                                                                                     "In", "Sn", "Sb", "Te", "I ", "Xe",
    "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W ", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn",
    "Fr", "Ra", "Ac", "Th", "Pa", "U ", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og",
]


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Convert Gaussian scan log to multi-frame xyz."
    )

    parser.add_argument(
        "-i",
        type=str,
        help="Input Gaussian scan log",
        required=True,
    )

    parser.add_argument(
        "-o",
        type=str,
        help="Output multi-frame xyz",
        default="scan.xyz",
        required=True,
    )

    args = parser.parse_args()

    return args


def scan2xyz(
    log: str,
    xyz: Optional[str] = "scan.xyz"
) -> None:
    with open(log, "r") as f:
        log_contents = f.readlines()
    cur_line_idx = 0
    num_lines = len(log_contents)

    mol_atoms = []
    mol_xyz = []
    energy = 0.0

    while cur_line_idx < num_lines:

        line = log_contents[cur_line_idx]

        if "Z-Matrix orientation" in line:
            mol_atoms = []
            mol_xyz = []

            cur_line_idx += 5
            line = log_contents[cur_line_idx]

            while not line.startswith(" ----"):
                tmp = line.split()

                atom_num = int(tmp[1])
                atom_sym = ELEMENTS[atom_num]
                mol_atoms.append(atom_sym)

                atom_xyz = [float(x) for x in tmp[3:]]
                mol_xyz.append(atom_xyz)

                cur_line_idx += 1
                line = log_contents[cur_line_idx]

        if "SCF Done" in line:
            tmp = line.split()
            energy = float(tmp[4])

            xyz_contents = [
                f"{len(mol_atoms)}\n",
                f"{energy}\n",
            ]

            for (atom_sym, atom_xyz) in zip(mol_atoms, mol_xyz):
                xyz_contents.append(
                    f"{atom_sym}"
                    f"{atom_xyz[0]:13.8f}"
                    f"{atom_xyz[1]:13.8f}"
                    f"{atom_xyz[2]:13.8f}"
                    "\n"
                )

            xyz_contents = "".join(xyz_contents)

            with open(xyz, "a") as f:
                f.write(xyz_contents)

        cur_line_idx += 1


if __name__ == "__main__":
    # parse arg
    args = _parse_args()

    # clear
    if os.path.exists(args.o):
        os.remove(args.o)

    # convert
    scan2xyz(
        log=args.i,
        xyz=args.o,
    )
