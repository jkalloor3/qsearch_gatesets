from __future__ import annotations
import os
import argparse

from bqskit.ir import Circuit

import pathlib

from extra_gatesets import *
import qsearch
from qsearch.gatesets import *

from qsearch import leap_compiler, multistart_solvers, parallelizers


import pickle
import glob

# Enable logging
import logging
logging.getLogger('bqskit').setLevel(logging.INFO) 

import sys

def my_print(text):
    sys.stdout.write(str(text))
    sys.stdout.flush()

def setup_args():
        # Run setup
    #region setup
    parser = argparse.ArgumentParser(
        description="Run qsearch on a given folder, optionally specify a range of blocks with start_num and stride"
    )
    # parser.add_argument("qasm_file", type=str, help="file to synthesize")
    parser.add_argument(
        "--folder_name", dest="name", action="store", nargs='?', default="qft_40_mesh_49_blocksize_3_quick",
        type=str, help="folder name in unitaries/"
    )
    parser.add_argument(
        "--start_num", dest="start_num", action="store", nargs="?", 
        default=0, type=int, help="which block num to start with"
    )
    parser.add_argument(
        "--stride", dest="stride", action="store", nargs="?", 
        default=-1, type=int, help="how many blocks to run on, default run on all blocks [start_num:]"
    )
    parser.add_argument(
        "--gates", dest="gates", action="store", 
        default="ISWAP,CNOT,sqrt(ISWAP),sqrt(CNOT)", type=str, help="Which gates to use as a comma separated list"
    )
    return parser.parse_args()


if __name__ == '__main__':

    args = setup_args()

    if args.stride != -1:
        path = os.path.join("project_files", args.name, f"{args.name}_{args.start_num}_{args.stride}")
        files = sorted(glob.glob(f"unitaries/{args.name}/*.unitary")[args.start_num:args.start_num + args.stride])
    else:
        path = os.path.join("project_files", args.name, f"{args.name}_{args.start_num}")
        files = sorted(glob.glob(f"unitaries/{args.name}/*.unitary")[args.start_num:])

    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    p = qsearch.Project(path)
    p.clear()
    p["solver"] = multistart_solvers.NaiveMultiStart_Solver(16)
    p["inner_solver"] = qsearch.solvers.LeastSquares_Jac_SolverNative()
    p["parallelizer"] = parallelizers.ProcessPoolParallelizer
    p["backend"] = qsearch.backends.NativeBackend()
    p["min_depth"] = 4
    p["compiler_class"] = leap_compiler.LeapCompiler
    p["verbosity"] = 1

    accepted_gatesets = args.gates.split(",")

    print("Here")
    print(len(files))
    print(len(demo_gatesets))
    for name, gateset in demo_gatesets:
        if name in accepted_gatesets:
            my_print("|")
            for f in files:
                my_print(".")
                bench_name = os.path.basename(f).split(".")[0]
                with open(f, "rb") as unit_file:
                    bench = pickle.load(unit_file)
                p.add_compilation(f"{name}-{bench_name}", bench.numpy, gateset=gateset, verbosity=0)

    print(p.compilations)
    p.run()