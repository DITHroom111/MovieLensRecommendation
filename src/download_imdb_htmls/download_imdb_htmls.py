import urllib.request
import time
import os
import argparse


SLEEP_SECS = 1
URL_PATERN = "https://www.imdb.com/title/{}"


def save_url(url, filename):
    try:
        html_bytes_file = urllib.request.urlopen(url)
        html_bytes = html_bytes_file.read()
    except:
        html_bytes = b"error"

    with open(filename, 'wb') as handler:
        handler.write(html_bytes)
 

def main(input_file, output_folder):
    os.mkdir(output_folder)
    with open(input_file, 'r') as handler:
        for i, line in enumerate(handler):
            key = line.strip()
            filename = "{}.html".format(key)
            save_url(URL_PATERN.format(key), os.path.join(output_folder, filename))
            print("saved {} file: {}.html".format(i, key))
            time.sleep(SLEEP_SECS)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required=True)
    parser.add_argument("--output_folder", required=True)
    args = parser.parse_args()

    main(args.input_file, args.output_folder)
