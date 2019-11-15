import argparse
import os

def is_html_valid(filename):
    try:
        return "<h2>Storyline</h2>" in open(filename,'r').read()
    except:
        return False


def main(htmls_folder, output_file):
    non_valid_filenames = filter(is_html_valid, os.listdir(htmls_folder))
    with open(output_file, 'w') as handler:
        handler.write('\n'.join(non_valid_filenames))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--htmls_folder", required=True)
    parser.add_argument("--output_file", required=True)
    args = parser.parse_args()

    main(args.htmls_folder, args.output_file)
