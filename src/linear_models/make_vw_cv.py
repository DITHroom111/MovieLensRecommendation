import argparse
from collections import defaultdict
import os
import shutil


def make_namespace(joined_words, name):
    return " |{} LENGTH:{} {}".format(name, len(joined_words.split()), joined_words)


def make_vw_line(line):
    split = line[:-1].split("\t")

    assert len(split) == 12
    fold, user_id, movie_id, timestamp = map(int, split[:4])
    rating = float(split[4])
    height_rating_intersetion_words, low_rating_intersetion_words = split[5:7]
    height_rating_intersetion_title_words, low_rating_intersetion_title_words = split[7:9]
    movie_title, user_height_rating_titles, user_low_rating_titles = split[9:12]

    vw_line = "{}".format(rating)
    vw_line += make_namespace(height_rating_intersetion_words, "height_rating_intersetion_words")
    vw_line += make_namespace(low_rating_intersetion_words , "low_rating_intersetion_words ")
    vw_line += make_namespace(height_rating_intersetion_title_words, "height_rating_intersetion_title_words")
    vw_line += make_namespace(low_rating_intersetion_title_words, "low_rating_intersetion_title_words")
    vw_line += make_namespace(movie_title, "movie_title")
    vw_line += make_namespace(user_height_rating_titles, "user_height_rating_titles")
    vw_line += make_namespace(user_low_rating_titles, "user_low_rating_titles")

    return vw_line


def create_fodler(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)


def save_cv(parts, cv_folder):
    assert isinstance(parts, dict)

    create_fodler(cv_folder)
    for test_folder in parts:
        print("Process folder {}".format(test_folder))
        test_filename = os.path.join(cv_folder, "test_{}".format(test_folder))
        train_filename = os.path.join(cv_folder, "train_{}".format(test_folder))
        with open(test_filename, 'w') as test_handler:
            test_handler.write(parts[test_folder])
        with open(train_filename, 'w') as train_handler:
            for folder in parts:
                if folder != test_folder:
                    train_handler.write(parts[folder])


def main(dataset_file, cv_folder):
    parts = defaultdict(list)
    with open(dataset_file, 'r') as handler:
        for i, line in enumerate(handler):
            if i % 100000 == 0:
                print("process", i)
            folder = int(line.strip().split("\t")[0])
            parts[folder].append(make_vw_line(line))
    print("Parts calculated")

    parts = {folder: "\n".join(parts[folder]) for folder in parts}
    print("Parts joined")

    save_cv(parts, cv_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_file", required=True)
    parser.add_argument("--cv_folder", required=True)
    args = parser.parse_args()

    main(args.dataset_file, args.cv_folder)
