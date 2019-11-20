# MovieLensRecommendation
Recommendation system built on MovieLens dataset for MIPT ML on Big Data course

Task: https://piazza.com/class/jz6qr7iba4i6no?cid=11

## What did we build?
Main idea: create several strong independent features and train CatBoost using them. Also, we pick imdb dataset to get actors and some other features, and we get movie's descriptions from imdb web-site. CatBoost was trained on following features:
- user - movie ALS
- user - genre ALS
- user - actor ALS
- linear model, trained on movies descriptions and descriptions of movies which got high rating from this user
- BERT model trained in similar way
- features from imdb: averageRating, isAdult, runtimeMinutes, numVotes, year, titleType (movie or series), genres
- current month, difference between current year and movie year
Also, for cold movie we have all features except ALS which is pretty strong one. Hence, we trained separate model for cold movies without ALS. For cold user we can say pretty much nothing, so we predict simply average rating for this movie.

## For developers

How to work with spark in MIPT cluster: https://docs.google.com/document/d/1dmb8o3M2ZCsjPq3rJQqd-jNLQhiBXWbWZcTn9aYUAp8

Part of train with bert, dev and test data with ALS: https://yadi.sk/d/Am3QOOka1OcpcA
All train examples with ALS: https://drive.google.com/open?id=1enPhlNYNvm6kFWSK-4IqduYAHvNi_T5H

Some data stats:
- movies count in movie table:  27278
- ratings in train: 14519043
- ratings in dev: 1690360
- users in train:  133929
- users in dev:  134597
- movies in train:  20707
- movies in dev:  16907


imdb texts: https://yadi.sk/d/hUegPQkYorJctQ

linear models 9 train parts predictions: https://yadi.sk/d/QAf6UewAefN1dg
files corespondance:
- predictions_0 -> u_0_m_0
- predictions_1 -> u_0_m_1
- predictions_2 -> u_0_m_2
- predictions_3 -> u_0_m_0
- predictions_4 -> u_0_m_1
- predictions_5 -> u_0_m_2
- predictions_6 -> u_0_m_0
- predictions_7 -> u_0_m_1
- predictions_8 -> u_0_m_2
the scheme is: fold,user_id,movie_id,timestamp,prediction
