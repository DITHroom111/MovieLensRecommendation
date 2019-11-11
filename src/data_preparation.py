from pyspark.sql import functions as f

import os

common_path = '/data/MobodMovieLens/train'

ratings = spark.read.csv(os.path.join(common_path, 'ratings.csv'), header=True).cache()
movies = spark.read.csv(os.path.join(common_path, 'movies.csv'), header=True).cache()

ratings_tmp = (
    ratings
    .withColumn(
        'order',
        f.row_number().over(Window.partitionBy('userId').orderBy('timestamp')) /
        f.count('*').over(Window.partitionBy('userId'))
    )
    .withColumn('hash', f.abs(f.hash('userId')) % 211)
)
ratings_train_A = (
    ratings_tmp
    .filter((f.col('hash') > 0) & (f.col('hash') <= 105) & (f.col('order') < 0.905))
    .drop('order', 'hash')
    .cache()
)
ratings_train_B = (
    ratings_tmp
    .filter((f.col('hash') > 106) & (f.col('order') < 0.905))
    .drop('order', 'hash')
    .cache()
)
ratings_dev = (
    ratings_tmp
    .filter((f.col('hash') == 0) | (f.col('order') >= 0.905))
    .drop('order', 'hash')
    .cache()
)

ratings_train_A.repartition(1).write.csv('ratings_train_A.csv', header=True, mode='overwrite')
ratings_train_B.repartition(1).write.csv('ratings_train_B.csv', header=True, mode='overwrite')
ratings_dev.repartition(1).write.csv('ratings_dev.csv', header=True, mode='overwrite')

print('movies count in movie table: ', movies.count())
print('ratings in train:', ratings_train.count())
print('ratings in dev:', ratings_dev.count())
print('users in train: ', ratings_train.agg(f.countDistinct('userId').alias('user_cnt')).collect()[0].user_cnt)
print('users in dev: ', ratings_dev.agg(f.countDistinct('userId').alias('user_cnt')).collect()[0].user_cnt)
print(
    'movies in train: ',
    ratings_train.agg(f.countDistinct('movieId').alias('movie_cnt')).collect()[0].movie_cnt
)
print(
    'movies in dev: ',
    ratings_dev.agg(f.countDistinct('movieId').alias('movie_cnt')).collect()[0].movie_cnt
)
