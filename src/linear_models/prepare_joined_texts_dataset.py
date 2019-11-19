import argparse
from collections import defaultdict


def read_texts(texts_file):
    with open(texts_file, 'r') as handler:
        texts = {}
        for line in handler:
            tconst, text = line.split("\t")
            assert tconst not in texts
            texts[tconst] = text
        return texts


def map_ratings_line(line):
    user_id, movie_id, timestamp = list(map(int, line.strip().split(",")[:3]))
    rating = float(line.strip().split(",")[3])
    return user_id, movie_id, timestamp, rating


def read_sorted_ratings(ratings_file):
    with open(ratings_file, 'r') as handler:
        next(handler)
        data = map(map_ratings_line, handler)
        return sorted(data, key=lambda obj: obj[3])


def get_tconst_and_movie_id(line):
    line = line.strip()
    if line.startswith("\""):
        line = line[line.find("\"", 1):]

    tconst = line.split(",")[1]
    movie_id = int(line.split(",")[-5])
    return tconst, movie_id


def make_movie_id_to_tconst(imdb_file):
    with open(imdb_file, 'r') as handler:
        next(handler)
        movie_id_to_tconst = {}
        for line in handler:
            tconst, movie_id = get_tconst_and_movie_id(line)
            #assert movie_id not in movie_id_to_tconst 
            if len(tconst) > 0:
                movie_id_to_tconst[movie_id] = tconst
    return movie_id_to_tconst


def make_movie_id_to_text(texts_file, imdb_file):
    tconst_to_texts = read_texts(texts_file)
    movie_id_to_tconst = make_movie_id_to_tconst(imdb_file)
    movie_id_to_text = {}
    for movie_id in movie_id_to_tconst:
        if movie_id in movie_id_to_tconst:
            tconst = movie_id_to_tconst[movie_id]
            if tconst in tconst_to_texts:
                movie_id_to_text[movie_id] = tconst_to_texts[tconst]
    return movie_id_to_text


def main(ratings_file, texts_file, imdb_file, output_file, min_rating, max_rating):
    movie_id_to_text = make_movie_id_to_text(texts_file, imdb_file)
    print("movie_id_to_text map created")
    ratings = read_sorted_ratings(ratings_file)
    print("Ratings sorted")

    dataset = []
    user_texts = defaultdict(lambda: "")
    for user_id, movie_id, timestamp, rating in ratings:
        if movie_id not in movie_id_to_text:
            continue

        dataset.append((user_id, movie_id, user_texts[user_id], movie_id_to_text[movie_id], rating))

        if (rating < max_rating) and (rating > min_rating):
            user_texts[user_id] += "\n" + movie_id_to_text[movie_id]

    print("dataset is ready")

    with open(output_file, 'w') as handler:
        for obj in dataset:
            handler.write("\t".join(map(str, obj)) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ratings_file", required=True)
    parser.add_argument("--texts_file", required=True)
    parser.add_argument("--imdb_file", required=True)
    parser.add_argument("--output_file", required=True)
    parser.add_argument("--min_rating", type=float, required=True)
    parser.add_argument("--max_rating", type=float, required=True)
    args = parser.parse_args()

    main(
        args.ratings_file,
        args.texts_file,
        args.imdb_file,
        args.output_file,
        args.min_rating,
        args.max_rating
    )
