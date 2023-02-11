"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import connect_to_db, db, User, Movie, Rating

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    '''View home page'''

    return render_template('homepage.html')

@app.route('/movies')
def all_movies():
    '''View all movies'''

    movies = Movie.get_movies()

    return render_template('all_movies.html', movies = movies)

@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    '''Show movie with particular ID'''

    movie = Movie.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie = movie)

@app.route('/movies/<movie_id>/rating', methods=['POST'])
def rate_movie(movie_id):
    '''Rate a movie'''
    logged_in = session.get('user_email')
    rating = request.form.get('rating')

    if logged_in is None:
        flash('You need to log in before you can rate!')
        return redirect(url_for('homepage'))
    elif not rating:
        flash('You must select a rating!')
    else:
        user = User.get_user_by_email(logged_in)
        movie = Movie.get_movie_by_id(movie_id)

        rated = Rating.create_rating(user, movie, int(rating))
        db.session.add(rated)
        db.session.commit()

        flash(f'You have rated this movie {rating}!')

    return redirect(f'/movies/{movie_id}') 

@app.route('/users')
def all_users():
    '''View all users'''

    users = User.get_users()

    return render_template('all_users.html', users = users)


@app.route('/users/<user_id>')
def show_user(user_id):
    '''Show user with particular ID'''

    user = User.get_user_by_id(user_id)

    return render_template('user_details.html', user = user)

@app.route('/users', methods=['POST'])
def register_user():
    '''Create a new user'''
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.get_user_by_email(email)

    if user:
        flash('Sorry, that email already exists. Try another.')
    else:
        user = User.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! You can now log in!')
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    '''User Login'''
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.get_user_by_email(email)
    
    if not user or password != password:
        flash('Incorrect email or password, please try again!')
    else:
        session['user_email'] = user.email
        flash(f'Welcome back, { user.email }! You may now rate movies!')
    
    return redirect('/')




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="localhost", port = 4321, debug=True)
