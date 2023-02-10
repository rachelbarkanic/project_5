'''Script to seed database'''

import os
import json
from random import choice, randint
from datetime import datetime

import model

from model import connect_to_db, db, User, Movie, Rating
import server

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())


'''Create movies, store them in a list so we can use them
to create fake ratings later'''

movies_in_db = []
for movie in movie_data:
    title, overview, poster_path = (
        movie['title'],
        movie['overview'],
        movie['poster_path']
    )

    release_date = datetime.strptime(movie['release_date'], '%Y-%m-%d')

    db_movie = Movie.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(db_movie)

model.db.session.add_all(movies_in_db)
model.db.session.commit()
    #TO DO: get the title, overview, poster_path from movie dict
    #Get release_date and convert to datettime object with datetime.strptime

    #TO DO: create a movie here and append it to movies_in_db


for n in range(10):
    email = f'user{n}@test.com'
    password = 'test'

    user = User.create_user(email, password)
    model.db.session.add(user)

    for _ in range(10):
        random_movie = choice(movies_in_db)
        score = randint(1, 5)

        rating = Rating.create_rating(user, random_movie, score)
        model.db.session.add(rating)

model.db.session.commit()