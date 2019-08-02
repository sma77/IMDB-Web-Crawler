from requests import get
from bs4 import BeautifulSoup
import csv, sqlite3, re

def inputDataFromCsvToDb():
    crawlDataFromWebToCsv()
    conn = sqlite3.connect('moviesData.db')
    c = conn.cursor()
    c.execute('CREATE TABLE moviesData (title, year, director, actors, imdb_rating);')
    with open('moviesData.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        to_db = [(row['title'], row['director'], row['actors'], row['imdb_rating'], row['year']) for row in reader]
    c.executemany('INSERT INTO moviesData (title, director, actors, imdb_rating, year) VALUES (?, ?, ?, ?, ?);', to_db)
    conn.commit()
    conn.close()

def crawlDataFromWebToCsv():
    with open('moviesData.csv', 'w') as csvfile:
        # initialize csv headers
        fieldnames = ['title', 'director', 'actors', 'imdb_rating', 'year']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        pages = [str(i) for i in range(1, 21)]
        for page in pages:
            url = 'http://www.imdb.com/search/title?groups=top_1000&sort=user_rating&view=simple&page=' + page
            response = get(url)
            # Parse the content of the request with BeautifulSoup
            html_soup = BeautifulSoup(response.text, 'html.parser')
            # Select all the 50 movie containers from a single page
            mv_containers = html_soup.find_all('div', class_ = 'lister-col-wrapper')
            for container in mv_containers:
                header = container.find('span', class_ = 'lister-item-header')
                info = header.find_all('span')[1]
                title = info.a.text
                people = info['title']
                director = people[:people.find('(')].strip()
                actors = people[people.find(')')+2:].strip()
                year = info.find('span', class_ = 'lister-item-year text-muted unbold').text
                match = re.search('([0-9]+)', year)
                year = year[match.start() : match.end()]
                rating = container.strong.text.strip()
                writer.writerow({'title': title, 'director': director, 'actors': actors, 'imdb_rating': rating, 'year': year})


inputDataFromCsvToDb()
