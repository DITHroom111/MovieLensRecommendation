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


def main(htmls_folder, output_file):
    html_filenames = os.listdir(htmls_folder)
    with open(output_file, 'w') as handler:
        for i, html_filename in enumerate(html_filenames):
            print("{} / {}".format(i, len(html_filenames)))
            try:
                text = get_text_from_html(os.path.join(htmls_folder, html_filename))
                key = html_filename[:html_filename.find(".")]
                handler.write("{}\t{}\n".format(key, text))
            except:
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--htmls_folder", required=True)
    parser.add_argument("--output_file", required=True)
    args = parser.parse_args()

    main(args.htmls_folder, args.output_file)
