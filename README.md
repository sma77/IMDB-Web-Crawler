Use Python and BeautifulSoup as web crawler for top 1000 IMDB movies.

### Install
Script needs to install "beautifulsoup4" and "flask".
```
pip3 install beautifulsoup
pip3 install flask
```

### How to Run
First run `crawler.py` to generate `moviesData.csv` and `moviesData.db`.
```
python crawler.py
```
Then run `app.py` and visit `localhost:5000` in your web browser.
```
python app.py
```

Try to query the database with
* full/partial title: `localhost:5000/title=?`
* year: `localhost:5000/year=?`
* full/partial director's name: `localhost:5000/director=?`
* full/partial actor's name: `localhost:5000/actors=?`
* IMDB rating: `localhost:5000/rating=?`


Improvements:
* Add access control to the search API
* Add max number of threads allowed to use the API at the same time
* Try to use NoSql db to store the movies' info
* Add NLP to analyze the search item and support for complex search 
