import argparse
from collections import defaultdict
import nltk
from nltk.tokenize import word_tokenize
import re
import math
 
# nltk.download('stopwords')
# nltk.download('punkt')
 
 
STOPWORDS = set(nltk.corpus.stopwords.words('english'))
STEMMER = nltk.stem.PorterStemmer()
 

def extract_bag_of_words(doc):
    terms = set()
    for token in word_tokenize(doc):
        if token not in STOPWORDS:
            if not re.search(r'\d', token) and not re.search(r'[^A-Za-z-]', token): #Removing numbers and punctuations
                #(excluding hyphenated words)
                terms.add(STEMMER.stem(token.lower()))
    return terms


def read_texts(texts_file):
    with open(texts_file, 'r') as handler:
        texts = {}
        for line in handler:
            tconst, text = line.strip().split("\t")
            assert tconst not in texts
            texts[tconst] = " ".join(extract_bag_of_words(text))
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
    user_text_ids = defaultdict(list)
    for user_id, movie_id, timestamp, rating in ratings:
        if movie_id not in movie_id_to_text:
            continue

        dataset.append([user_id, movie_id, movie_id_to_text[movie_id], rating, user_text_ids[user_id][:]])

        if (rating < max_rating) and (rating > min_rating):
            user_text_ids[user_id].append(movie_id)

    print("dataset is ready")

    with open(output_file, 'w') as handler:
        for i, obj in enumerate(dataset):
            if i % 10000 == 0:
                print("{} / {}".format(i, len(dataset)))
            user_texts = map(lambda movie_id: movie_id_to_text[movie_id], obj[-1])
            handler.write("\t".join(map(str, obj[:-1])))
            handler.write("\t")
            for text in user_texts:
                handler.write(text)
                handler.write("\n")


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
