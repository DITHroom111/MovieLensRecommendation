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


def cut_one_element_back(line):
    if line[-1] == '"':
        index = line[:-1].rfind('"')
        line = line[:index]
    split = line.split(",")[:-1]
    return ",".join(split)


def get_back_element(line):
    if line[-1] == '"':
        index = line[:-1].rfind('"')
        return line[(index + 1):-1]
    else:
        index = line.rfind(',')
        return line[index:]


def get_tconst_and_movie_id(line):
    split = line.strip().split(",")

    tconst = split[1]

    for i in range(6):
        line = cut_one_element_back(line)
    movie_id = int(line.split(",")[-1])
    
    return tconst, movie_id


def get_title(line):
    for i in range(5):
        line = cut_one_element_back(line)
    return get_back_element(line)


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


def make_movie_id_to_title(imdb_file):
    with open(imdb_file, 'r') as handler:
        next(handler)
        movie_id_to_title = {}
        for line in handler:
            tconst, movie_id = get_tconst_and_movie_id(line)
            title = get_title(line)
            movie_id_to_title[movie_id] = extract_bag_of_words(title)
    return movie_id_to_title


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


def main(sorted_ratings_file, texts_file, imdb_file, output_file, height_rating, low_rating):
    movie_id_to_text = make_movie_id_to_text(texts_file, imdb_file)
    movie_id_to_title = make_movie_id_to_title(imdb_file)
    print("movie_id_to_text map created")
    ratings = read_sorted_ratings(sorted_ratings_file)
    print("Ratings sorted")

    dataset = []
    user_height_rating_words = defaultdict(set)
    user_low_rating_words = defaultdict(set)
    user_height_rating_titles = defaultdict(set)
    user_low_rating_titles = defaultdict(set)
    for i, (fold, user_id, movie_id, timestamp, rating) in enumerate(ratings):
        if i % 100000 == 0:
            print("Calculating intersections {} / {}".format(i, len(ratings)))

        if movie_id in movie_id_to_text:
            movie_text = movie_id_to_text[movie_id]

            height_rating_intersetion_words = " ".join(user_height_rating_words[user_id] & movie_text)
            low_rating_intersetion_words = " ".join(user_low_rating_words[user_id] & movie_text)

            if rating > height_rating:
                user_height_rating_words[user_id].update(movie_text)
            if rating < low_rating:
                user_low_rating_words[user_id].update(movie_text)
        else:
            height_rating_intersetion_words = "HAVE_NO_MOVIE_ID"
            low_rating_intersetion_words = "HAVE_NO_MOVIE_ID"

        if movie_id in movie_id_to_title:
            movie_title = movie_id_to_title[movie_id]

            height_rating_intersetion_title_words = " ".join(user_height_rating_titles[user_id] & movie_title)
            low_rating_intersetion_title_words = " ".join(user_low_rating_titles[user_id] & movie_title)

            if rating > height_rating:
                user_height_rating_titles[user_id].update(movie_text)
            if rating < low_rating:
                user_low_rating_titles[user_id].update(movie_text)
        else:
            movie_title = "HAVE_NO_MOVIE_ID"
            height_rating_intersetion_title_words = "HAVE_NO_MOVIE_ID"
            low_rating_intersetion_title_words = "HAVE_NO_MOVIE_ID"

        dataset.append([
            fold,
            user_id,
            movie_id,
            timestamp,
            rating,
            height_rating_intersetion_words,
            low_rating_intersetion_words,
            height_rating_intersetion_title_words,
            low_rating_intersetion_title_words,
            movie_title,
            user_height_rating_titles[user_id],
            user_low_rating_titles[user_id]
        ])


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
    parser.add_argument("--height_rating", type=float, required=True)
    parser.add_argument("--low_rating", type=float, required=True)
    args = parser.parse_args()

    main(
        args.sorted_ratings_file,
        args.texts_file,
        args.imdb_file,
        args.output_file,
        args.height_rating,
        args.low_rating
    )
