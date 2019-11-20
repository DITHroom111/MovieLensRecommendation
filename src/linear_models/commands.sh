python3 make_sorted_ratings.py --output_file sorted_ratings.tsv --ratings_files MovieLensDataToZomb/ratings_train_with_ALS_predictions_u_*
python3 prepare_vw_dataset.py --sorted_ratings_file sorted_ratings.tsv --texts_file texts.tsv --imdb_file MovieLensDataToZomb/movies_imdb.csv --min_rating 3.5 --max_rating 10 --output_file vw_dataset_3.5_10.tsv
python3 make_vw_cv.py --dataset_file vw_dataset_3.5_10.tsv --cv_folder vw_cv
vw train_0 -f model_0 --loss_function squared --passes 5 -c --adaptive --normalized --l1 0.00000001 --l2 0.0000001 -b 24
