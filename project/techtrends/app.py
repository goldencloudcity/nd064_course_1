import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash, g
from werkzeug.exceptions import abort

import logging
import sys
# Function to get a database connection.
# This function connects to database with the name `database.db`
connection_counter=0
def get_db_connection():
    global connection_counter
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    connection_counter+=1
    app.logger.debug(f'connection_counter: {connection_counter}')
    return connection

# Function to get a post using its ID
def get_post(post_id):
    global connection_counter
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    connection_counter-=1
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    global connection_counter
    connection = get_db_connection()
    app.logger.debug(f'connection_counter: {connection_counter}')
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    connection_counter-=1
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.debug(f"404: A non-existent article is retrieved!")
      return render_template('404.html'), 404
    else:
      app.logger.debug(f"""Article "{post['title']}" retrieved!""")
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.debug('The "About Us" page retrieved!')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    global connection_counter
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            app.logger.debug(f'connection_counter: {connection_counter}')
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.debug(f"""New Article "{title}" is created!""")
            connection_counter-=1

            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/healthz')
def healthcheck():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    app.logger.debug('Status request successful')
    app.logger.debug('DEBUG message')
    return response

#   {"status":"success","code":0,"data":{"UserCount":140,"UserCountActive":23}}),
@app.route('/metrics')
def metrics():
    global connection_counter
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    app.logger.debug(f'connection_counter: {connection_counter}')
    #num_connections = len(g._connections) if hasattr(g,'_connections') else 0
    connection.close()
    connection_counter-=1
    response = app.response_class(
            response=json.dumps({"db_connection_count": connection_counter, "post_count": len(posts)}),
            status=200,
            mimetype='application/json'
    )
    app.logger.debug('Metrics request successful')
    return response

# start the application on port 3111
if __name__ == "__main__":
   logging.basicConfig(level=logging.DEBUG,stream=sys.stdout)
   app.run(host='0.0.0.0', port='3111')
