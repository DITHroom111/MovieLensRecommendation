import argparse
import os


def get_key_from_line(line):
    line = line.strip()
    if line.startswith("\""):
        line = line[line.find("\"", 1):]

    return line.split(",")[1]


def main(input_file, downloaded_folder, output_file):
    downloaded_keys = set(map(lambda filename: filename[:filename.find('.')], os.listdir(downloaded_folder)))
    with open(input_file, 'r') as handler:
        keys = list(filter(
            lambda key: (key not in downloaded_keys) and len(key) > 0,
            map(get_key_from_line, handler)
        ))
    with open(output_file, 'w') as handler:
        handler.write('\n'.join(keys))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required=True)
    parser.add_argument("--downloaded_folder", required=True)
    parser.add_argument("--output_file", required=True)
    args = parser.parse_args()

    main(args.input_file, args.downloaded_folder, args.output_file)
