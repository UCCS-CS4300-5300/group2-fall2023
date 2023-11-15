#!/usr/bin/env python

### CS 4300 Fall 2023 Group 2
### Harvestly
### Code Quality Summarzation script - uses Radon


import os
import math
import argparse
from radon.raw import analyze
from radon.metrics import mi_visit, mi_rank, h_visit
from radon.complexity import cc_visit, cc_rank

PROJECT_DIRECTORY = "../"

def get_python_file_paths(directory):
    """ Get all python file paths in a directory """
    
    file_paths = []

    for root, _dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and file != "code_quality.py":
                file_paths.append(os.path.join(root, file))
    
    return file_paths


def get_total_LOC(file_paths):
    """ Get the total lines of code in a list of files """

    loc = 0

    for file_path in file_paths:
        with open(file_path, "r") as f:
            content = f.read()

            radon_raw_result = analyze(content)
            loc += radon_raw_result.loc

    return loc


def get_average_mi(file_paths):
    """ Get average maintainability index """

    total_mi = 0

    for file_path in file_paths:
        with open(file_path, "r") as f:
            content = f.read()
            total_mi += mi_visit(content, multi=False)

    return total_mi / len(file_paths)      


def get_average_cc(file_paths):
    """ Get average cyclomatic complexity """

    cc_results = []

    for file_path in file_paths:
        with open(file_path, "r") as f:
            content = f.read()
            cc = cc_visit(content)

            for res in cc:
                cc_results.append(res.complexity)

    return sum(res for res in cc_results) / len(cc_results)


def get_total_halstead(file_paths):
    """ Get total halstead metrics """

    h1, h2 = 0.0, 0.0
    N1, N2 = 0.0, 0.0

    for file_path in file_paths:
        with open(file_path, "r") as f:
            content = f.read()
            halstead = h_visit(content)

            h1 += halstead.total.h1
            h2 += halstead.total.h2
            N1 += halstead.total.N1
            N2 += halstead.total.N2

    vocabulary = h1 + h2
    length = N1 + N2
    calculated_length = (h1 * math.log2(h1)) + (h2 * math.log2(h2))
    volume = length * math.log2(vocabulary)
    difficulty = h1/2 + N2/h2
    effort = difficulty * volume

    return h1, h2, N1, N2, vocabulary, length, calculated_length, volume, difficulty, effort


def main(project_directory=PROJECT_DIRECTORY):
    """ Get summarization of radon metrics """

    file_paths = get_python_file_paths(project_directory)

    loc = get_total_LOC(file_paths)
    mi = get_average_mi(file_paths)
    cc = get_average_cc(file_paths)
    halstead = get_total_halstead(file_paths)

    print("== Code Quality Summarization ===")
    print(f"LOC: {loc}")
    print(f"Average Maintainability Index: ({mi_rank(mi)}) {mi}")
    print(f"Average Cyclomatic Complexity: ({cc_rank(cc)}) {cc}")
    print("Total Halstead Metrics (Entire project):")
    print(f"\th1: {halstead[0]}")
    print(f"\th2: {halstead[1]}")
    print(f"\tN1: {halstead[2]}")
    print(f"\tN2: {halstead[3]}")
    print(f"\tvocabulary: {halstead[4]}")
    print(f"\tlength: {halstead[5]}")
    print(f"\tcalculated_length: {halstead[6]}")
    print(f"\tvolume: {halstead[7]}")
    print(f"\tdifficulty: {halstead[8]}")
    print(f"\teffort {halstead[9]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Code quality summarization.")
    parser.add_argument("--path", help="Path to project directory.")

    args = parser.parse_args()

    if args.path:
        if os.path.exists(args.path):
            main(args.path)
        
        else:
            print(f"Path {args.path} does not exist!")

    else:
        main()
