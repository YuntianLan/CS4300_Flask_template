---------- Files used for generating .json are Character Mapping.ipynb and for generating .csv are Extract Movie Name.ipynb, Name and ID Correspondence.ipynb

---------- Opening json file
# Way to open:
with open("characters_review_other.json", "r") as read_file:
    dict_format = json.loads(json.load(read_file))

---------- Four relevant files
characters_review_cornell.json
Reviews related to characters found in Cornell movie dataset.
(Note: review_content, review_score, review_category are one-to-one (thereby having the same length).
"Unsup" (unsupervised) category automatically yields a score of 0; score label is not given.

characters_review_other.json
Reviews related to characters for the other 4 franchises.
(Note: review_content, review_score, review_category are one-to-one.
"Unsup" (unsupervised) category automatically yields a score of 0 because label is not given.

intersected_script_reviews.csv
reviews for characters in movies found in the Cornell movie dataset. 

intersected_script_reviews_other_franchises.csv
reviews for characters in movies for the other 4 franchises.