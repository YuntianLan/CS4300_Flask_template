cornell_movie_info.json:
    information about movies in the cornell movie dataset
    {movie_id (in cornell movie dataset: {
	Title, Year, Genre, ...,Plot, Poster, imdbID
    }

char_mappings.json:
    maps character ids used in images and *characters.json to character ids in transcripts
    only contains characters in the cornell movie dataset, star wars and marvel movies now
	
all_character_lines.json:
   maps character ids to their lines in transcripts. 
   only contains characters in the cornell movie dataset, star wars and marvel movies now

char_quotes.json:
   maps character ids to their quotes scraped from imdb
   only contains characters in the four franchises, can be used to supplement all_characterlines.json

personality
    all_characters.json:
    	character information for characters in four franchises
    	{char_id: {
    		name: name of the character,
    		series: one of the four series or none,
    		big_five: [a list of big five score],
    		url: link to the character page on fandom,
    		description: description of the character if exists,
    		quote: [a list with first element being the quote, the second element being the speaker],
    		movie: the movie where the quote appears, can be used as main movie for the character if exists}
	}

    cornell_movie_characters.json:
 	character information for characters in the cornell movie dataset
 	same as all_characters.json except that big_five is empty for now, and series field is empty
	This file will be merged with the above later

    big5.csv:
  	435 personality adjectives listed in Saucier and Goldberg’s paper “Evidence for the Big Five in analysis of familiar English personality adjectives” (1996)

    char_big_five:
	big five scores for characters in the four franchises

    other folders:
	original information scraped from Fandom for each character
