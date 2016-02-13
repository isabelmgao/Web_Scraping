Data_Manipulation_Web_Scraping
Web scraping IMDB.com and comparing it to TMDB's dataset (provided by their API)

Fetched the top 200 Sci-Fi movies based on user ratings from IMDB starting from this URL

Parsed the HTML pages from Step 1 with BeautifulSoup, extracted movie information for top 200 Sci-Fi movies and saved the result in a tsv file

Used the Web service http://www.themoviedb.org/documentation/api to get themoviedb.org rating for each of the top 200 movies using the IMDB ID you collected in Step 2.

With the data from step 3, I loaded the JSON string on each line into a variable, extracted just the ‘vote_average’ numbers, and then joined it with the IMDB data based on the IMDB IDs

Visualization: created a scatter plot graphic to visualize the results
