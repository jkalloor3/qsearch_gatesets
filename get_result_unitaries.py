from __future__ import annotations
import os
import argparse



from extra_gatesets import *
import qsearch
from qsearch.gatesets import *


import pickle
import glob

import pathlib

# Enable logging
import logging
logging.getLogger('bqskit').setLevel(logging.INFO) 
import json

def setup_args():
        # Run setup
    #region setup
    parser = argparse.ArgumentParser(
        description="Get results from qsearch, projects should be in project_files folder"
    )
    # parser.add_argument("qasm_file", type=str, help="file to synthesize")
    parser.add_argument(
        "--folder_name", dest="name", action="store", nargs='?', default="qft_40_mesh_49_blocksize_3_quick",
        type=str, help="folder name in block_files/"
    )
    return parser.parse_args()


if __name__ == '__main__':

    args = setup_args()

    dir = os.path.join("project_files", args.name)
    all_dirs = [os.path.join(dir, x) for x in os.listdir(dir)]

    for d in all_dirs:
        p = qsearch.Project(d)
        # print(p.compilations)
        for com in p.compilations:
            data = p.get_result(com)
            struct = data["structure"]
            unitary = struct.matrix(data["parameters"])
            sub_dir, unitary_name = com.split("-")
            w_dir = os.path.join("final_unitaries", args.name, sub_dir)
            pathlib.Path(w_dir).mkdir(parents=True, exist_ok=True)
            w_path = os.path.join(w_dir, f"{unitary_name}.unitary")
            with open(w_path, "wb") as w_file:
                pickle.dump(unitary,w_file)