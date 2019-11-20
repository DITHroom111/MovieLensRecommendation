# MovieLensRecommendation
Recommendation system built on MovieLens dataset for MIPT ML on Big Data course

Task: https://piazza.com/class/jz6qr7iba4i6no?cid=11

How to work with spark in MIPT cluster: https://docs.google.com/document/d/1dmb8o3M2ZCsjPq3rJQqd-jNLQhiBXWbWZcTn9aYUAp8

Train and dev data: https://yadi.sk/d/Am3QOOka1OcpcA

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
files corespondance: predictions_0 -> u_0_m_0
                     predictions_1 -> u_0_m_1
                     predictions_2 -> u_0_m_2
                     predictions_3 -> u_0_m_0
                     predictions_4 -> u_0_m_1
                     predictions_5 -> u_0_m_2
                     predictions_6 -> u_0_m_0
                     predictions_7 -> u_0_m_1
                     predictions_8 -> u_0_m_2
the scheme is: fold,user_id,movie_id,timestamp,prediction
