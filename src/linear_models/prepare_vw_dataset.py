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
                terms.add(STEMMER.stem(token.lower()))
    return terms


def read_texts(texts_file):
    with open(texts_file, 'r') as handler:
        texts = {}
        for line in handler:
            tconst, text = line.strip().split("\t")
            assert tconst not in texts
            texts[tconst] = extract_bag_of_words(text)
        return texts


def map_ratings_line(line):
    # [fold, user_id, movie_id, timestamp, rating]
    types = [int, int, int, int, float]
    values = line.strip().split("\t")
    return list(map(lambda pair: pair[0](pair[1]), zip(types, values)))


def read_sorted_ratings(sorted_ratings_file):
    with open(sorted_ratings_file, 'r') as handler:
        return list(map(map_ratings_line, handler))


def step_one_element_back(line):
    if line[-1] == '"':
        index = line[:-1].rfind('"')
        line = line[:index]
    split = line.split(",")[:-1]
    return ",".join(split)


def get_tconst_and_movie_id(line):
    split = line.strip().split(",")

    tconst = split[1]

    for i in range(6):
        line = step_one_element_back(line)
    movie_id = int(line.split(",")[-1])
    
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


def main(sorted_ratings_file, texts_file, imdb_file, output_file, min_rating, max_rating):
    movie_id_to_text = make_movie_id_to_text(texts_file, imdb_file)
    print("movie_id_to_text map created")
    ratings = read_sorted_ratings(sorted_ratings_file)
    print("Ratings sorted")

    dataset = []
    user_words = defaultdict(set)
    for i, (fold, user_id, movie_id, timestamp, rating) in enumerate(ratings):
        if i % 100000 == 0:
            print("Calculating intersections {} / {}".format(i, len(ratings)))

        if movie_id not in movie_id_to_text:
            dataset.append([fold, user_id, movie_id, timestamp, rating])
            continue
        
        intersetion_words = movie_id_to_text[movie_id] & user_words[user_id]
        dataset.append([fold, user_id, movie_id, timestamp, rating, " ".join(intersetion_words)])

        if (rating < max_rating) and (rating > min_rating):
            user_words[user_id].update(movie_id_to_text[movie_id])

    print("dataset is ready")

    with open(output_file, 'w') as handler:
        for i, obj in enumerate(dataset):
            if i % 100000 == 0:
                print("Writing output {} / {}".format(i, len(dataset)))
            for i, string in enumerate(map(str, obj)):
                if i != 0:
                    handler.write("\t")
                handler.write(string)
            handler.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sorted_ratings_file", required=True)
    parser.add_argument("--texts_file", required=True)
    parser.add_argument("--imdb_file", required=True)
    parser.add_argument("--output_file", required=True)
    parser.add_argument("--min_rating", type=float, required=True)
    parser.add_argument("--max_rating", type=float, required=True)
    args = parser.parse_args()

    main(
        args.sorted_ratings_file,
        args.texts_file,
        args.imdb_file,
        args.output_file,
        args.min_rating,
        args.max_rating
    )
