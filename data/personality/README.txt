This dataset includes a list of personality adjectives and personality descriptions of 270 characters in four franchises scraped from Fandom.

all_characters.json:
  char_id:
    name: name of the character
    series: one of the four series or none
    big_five: a list of big five score
    url: link to the character page on fandom
    description: description of the character if exists
    quote: a list with first element being the quote, the second element being the speaker
    movie: the movie where the quote appears, can be used as main movie for the character

big5.csv:
  435 personality adjectives listed in Saucier and Goldberg’s paper “Evidence for the Big Five in analysis of familiar English personality adjectives” (1996)

Original personality descriptions in each folder:
  Each json file has the below fields:
    id: id of the character
    name: name of the character
    fandom: fandom the character belongs to
    url: link to the fandom wiki page
    personality: a list of paragraphs, main description under the "Personality" section in the wiki page
    figure_captions: a list of figure captions of figures under the "Personality" section
    quotes: a list of quotes under the "Personality" section
