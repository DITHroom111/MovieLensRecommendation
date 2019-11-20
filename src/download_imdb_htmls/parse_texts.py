import argparse
import os
from bs4 import BeautifulSoup


def get_text_from_html(html_filename):
    with open(html_filename, 'r') as handler:
        soup = BeautifulSoup(handler.read(), 'html')
        h2s = list(filter(lambda h2: h2.text == "Storyline", soup.find_all('h2')))
        assert len(h2s) == 1
        storyline = h2s[0]
        text = list(list(storyline.fetchNextSiblings()[0].children)[1].children)[1].text.strip()
        return text


def read_skip_keys(already_parsed_texts_file):
    with open(already_parsed_texts_file, 'r') as handler:
        return {line.strip().split("\t")[0] for line in handler}


def main(htmls_folder, output_file, already_parsed_texts_file):
    skip_keys = read_skip_keys(already_parsed_texts_file)
    html_filenames = os.listdir(htmls_folder)
    with open(output_file, 'w') as handler:
        for i, html_filename in enumerate(html_filenames):
            print("{} / {}".format(i, len(html_filenames)))
            key = html_filename[:html_filename.find(".")]
            if key in skip_keys:
                continue
            try:
                text = get_text_from_html(os.path.join(htmls_folder, html_filename))
                handler.write("{}\t{}\n".format(key, text))
            except:
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--htmls_folder", required=True)
    parser.add_argument("--already_parsed_texts_file", required=True)
    parser.add_argument("--output_file", required=True)
    args = parser.parse_args()

    main(args.htmls_folder, args.output_file, args.already_parsed_texts_file)
