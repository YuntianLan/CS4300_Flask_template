---------- Opening json file
# Way to open:
with open("characters_review_other.json", "r") as read_file:
    dict_format = json.loads(json.load(read_file))

---------- Four relevant files
characters_review_cornell.json
Reviews related to characters found in Cornell movie dataset.
review_content, review_score, review_category are one-to-one (thereby having the same length)
review_count counts the total number of reviews; rating_count counts the total number of reviews that *also give a rating*
"Unsup" (unsupervised) category automatically yields a score of 0 as score is given, and is therefore excluded from calculating average rating or counting the number of ratings (thought including in total review count)

characters_review_other.json
Reviews related to characters for the other 4 franchises.
Note: review_content, review_score, review_category are one-to-one (thereby having the same length
review_count counts the total number of reviews; rating_count counts the total number of reviews that also *give a rating*
"Unsup" (unsupervised) category automatically yields a score of 0 as score is given, and is therefore excluded from calculating average rating (thought including in total review count)

movie_cornell_review_info.json
Reviews related to movie found in Cornell movie dataset.
Same explanations except that this is movie-specific.

movie_other_review_info.json
Reviews related to movie found in other franchise movie dataset.
Same explanations except that this is movie-specific.

