import argparse


def main(file_1, file_2, output_file):
    lines = []
    with open(file_1, 'r') as handler_1, open(file_2, 'r') as handler_2:
        for line_1, line_2 in zip(handler_1, handler_2):
            lines.append(",".join([line_1.strip(), line_2.strip()]))
    with open(output_file, 'w') as handler:
        for line in lines:
            handler.write(line + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_1", required=True)
    parser.add_argument("--file_2", required=True)
    parser.add_argument("--output_file", required=True)
    args = parser.parse_args()

    main(args.file_1, args.file_2, args.output_file)
