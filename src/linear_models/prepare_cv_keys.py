import argparse
from collections import defaultdict
import os
import shutil


def make_line(line):
    split = line[:-1].split("\t")
    assert len(split) == 12
    return ",".join(split[:4])


def create_fodler(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)


def save(parts, cv_folder):
    assert isinstance(parts, dict)

    create_fodler(cv_folder)
    for test_folder in parts:
        print("Process folder {}".format(test_folder))
        test_filename = os.path.join(cv_folder, "test_{}".format(test_folder))
        with open(test_filename, 'w') as test_handler:
            test_handler.write(parts[test_folder])


def main(dataset_file, cv_folder):
    parts = defaultdict(list)
    with open(dataset_file, 'r') as handler:
        for i, line in enumerate(handler):
            if i % 100000 == 0:
                print("process", i)
            folder = int(line.strip().split("\t")[0])
            parts[folder].append(make_line(line))
    print("Parts calculated")

    parts = {folder: "\n".join(parts[folder]) for folder in parts}
    print("Parts joined")

    save(parts, cv_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_file", required=True)
    parser.add_argument("--cv_folder", required=True)
    args = parser.parse_args()

    main(args.dataset_file, args.cv_folder)
