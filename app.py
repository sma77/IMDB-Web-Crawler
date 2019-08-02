from flask import Flask, request, jsonify, render_template
import os, csv, sqlite3

# initialize flask app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'moviesData.db')

# database info
db = 'moviesData.db'
tableName = 'moviesData'
col_title = 'title'
col_year = 'year'
col_director = 'director'
col_actors = 'actors'
col_rating = 'imdb_rating'

# option for using csv besides sqlite3
def get_csv():
    csv_file = open('./moviesData.csv', 'r')
    csv_list = list(csv.DictReader(csv_file))
    return csv_list

# endpoint to display all movies
@app.route('/')
def index():
    csv_list = get_csv()
    return render_template('index.html', object_list=csv_list)

# endpoint to query by title
@app.route('/title=<title>/')
def searchTitle(title):
    return searchAPI(col_title, title)

# endpoint to query by year
@app.route('/year=<year>/')
def searchYear(year):
    return searchAPI(col_year, year)

# endpoint to query by director
@app.route('/director=<director>/')
def searchDirector(director):
    return searchAPI(col_director, director)

# endpoint to query by actors
@app.route('/actors=<actors>/')
def searchactors(actors):
    return searchAPI(col_actors, actors)

# endpoint to query by rating
@app.route('/rating=<rating>/')
def searchRating(rating):
    return searchAPI(col_rating, rating)

def searchAPI(colName, queryValue):
    sqlCmd = None
    print("query value is number %s" % str(is_number(queryValue)))
    if is_number(queryValue):
        sqlCmd = 'SELECT * FROM {} WHERE {}="{}"'
    else:
        sqlCmd = 'SELECT * FROM {} WHERE UPPER({}) LIKE UPPER("%{}%")'

    conn = sqlite3.connect(db)
    c = conn.cursor()
    cmd = sqlCmd.format(tableName, colName, queryValue)
    print('Sql command is %s' % cmd)
    c.execute(cmd)
    rows = c.fetchall()
    c.close()
    return jsonify(rows)

def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True

if __name__=='__main__':
    app.run(debug=True, use_reloader=True)

