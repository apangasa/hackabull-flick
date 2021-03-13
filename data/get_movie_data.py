import csv
import json
import requests


def get_movie_data():
    movies = {}
    direc = 'data/IMDb movies.csv'
    with open(direc, 'r', encoding='utf8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')

        for idx, row in enumerate(reader):
            # if len(movies.keys()) >= 750:
            #     # Prevent more than 750 API requests
            #     break

            # if idx % 50 != 0:
            #     # only take every 100 movies from the csv (otherwise we hit API request limit)
            #     # periodically dump movie info into file
            #     continue

            try:
                film_id = row[0]
                if film_id == 'imdb_title':
                    # Skip Headers
                    continue

                # Movie Database API Request
                url = "https://movie-database-imdb-alternative.p.rapidapi.com/"
                querystring = {"i": str(film_id), "r": "json"}
                headers = {
                    'x-rapidapi-key': "48460a9c8fmsh83f511fa2efe743p160b5cjsnfa3e1c5a02ee",
                    'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com"
                }
                response = requests.request(
                    "GET", url, headers=headers, params=querystring)
                data = json.loads(response.text)
                title = data['Title']
                run_time = data['Runtime'].split(' ')[0]
                year = data['Year']
                rated = data['Rated']
                genres = data['Genre'].split(',')
                imdb_rating = data['imdbRating']
                rt_rating = data['Ratings'][1]['Value']
                imdb_votes = data['imdbVotes']
                description = data['Plot']
                img = data['Poster']

                # # IMDB API Request
                # url = "https://imdb8.p.rapidapi.com/title/get-overview-details"
                # querystring = {"tconst": str(film_id), "currentCountry": "US"}
                # headers = {
                #     'x-rapidapi-key': "48460a9c8fmsh83f511fa2efe743p160b5cjsnfa3e1c5a02ee",
                #     'x-rapidapi-host': "imdb8.p.rapidapi.com"
                # }
                # response = requests.request(
                #     "GET", url, headers=headers, params=querystring)
                # data = json.loads(response.text)
                # title = data['title']['title']
                # run_time = data['title']['runningTimeInMinutes']
                # year = data['title']['year']
                # rating = data['ratings']['rating']
                # rating_count = data['ratings']['ratingCount']
                # genres = data['genres']

                # Utelly API Request (identify streaming services)
                # url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/idlookup"
                # querystring = {"source_id": str(
                #     film_id), "source": "imdb", "country": "us"}
                # headers = {
                #     'x-rapidapi-key': "48460a9c8fmsh83f511fa2efe743p160b5cjsnfa3e1c5a02ee",
                #     'x-rapidapi-host': "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com"
                # }
                # response = requests.request(
                #     "GET", url, headers=headers, params=querystring)
                # data = json.loads(response.text)

                # services = []

                # for location in data['collection']['locations']:
                #     services.append(location['display_name'])

                movies[film_id] = {
                    'title': title,
                    'run_time': run_time,
                    'year': year,
                    'imdb_rating': imdb_rating,
                    'rt_rating': rt_rating,
                    'rated': rated,
                    'img': img,
                    'description': description,
                    'imdb_votes': imdb_votes,
                    'genres': genres
                }

                if len(movies.keys()) % 10 == 0:
                    print('Adding movies...')
                    print(len(movies.keys()))
                    with open('data/movie_data.json', 'w') as movie_data:
                        json.dump(movies, movie_data)
            except:
                continue

        print('Final dump!')
        with open('data/movie_data.json', 'w') as movie_data:
            json.dump(movies, movie_data)


get_movie_data()
