import argparse


def get_key_from_line(line):
    line = line.strip()
    if line.startswith("\""):
        line = line[line.find("\"", 1):]

    return line.split(",")[1]


def main(input_file, output_file):
    with open(input_file, 'r') as  handler:
        next(handler)
        keys = list(filter(lambda key: len(key) > 0, map(get_key_from_line, handler)))
    with open(output_file, 'w') as handler:
        handler.write('\n'.join(keys))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required=True)
    parser.add_argument("--output_file", required=True)
    args = parser.parse_args()

    main(args.input_file, args.output_file)
