import argparse
from collections import defaultdict


def map_ratings_line(line):
    user_id, movie_id, timestamp = list(map(int, line.strip().split(",")[:3]))
    rating = float(line.strip().split(",")[3])
    return user_id, movie_id, timestamp, rating


def read_sorted_ratings(ratings_files):
    data = []
    for i, ratings_file in enumerate(ratings_files):
        with open(ratings_file, 'r') as handler:
            next(handler)
            for line in handler:
                user_id, movie_id, timestamp, rating = map_ratings_line(line)
                data.append((i, user_id, movie_id, timestamp, rating))
    return sorted(data, key=lambda obj: obj[3])


def main(ratings_files, output_file):
    for i, filename in enumerate(ratings_files):
        print(i, filename)
    ratings = read_sorted_ratings(ratings_files)
    print("Sorted ratings ready")

    with open(output_file, 'w') as handler:
        for obj in ratings:
            handler.write("\t".join(map(str, obj)) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ratings_files", nargs='+', help='<Required> Set flag', required=True)
    parser.add_argument("--output_file", required=True)
    args = parser.parse_args()

    main(args.ratings_files, args.output_file)
