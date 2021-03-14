
import logging
from flask import Flask, jsonify, request
import json
from flask_cors import CORS
from argparse import ArgumentParser, RawTextHelpFormatter
import psycopg2
from psycopg2.errors import SerializationFailure


app = Flask(__name__)
CORS(app)

def parse_cmdline():
    parser = ArgumentParser(description=__doc__,
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "dsn",
        help="""database connection string\n\n
             For cockroach demo, use 'postgresql://<username>:<password>@<hostname>:<port>/bank?sslmode=require',\n
             with the username and password created in the demo cluster, and the hostname and port listed in the\n
             (sql/tcp) connection parameters of the demo cluster welcome message.\n\n
             For CockroachCloud Free, use 'postgres://<username>:<password>@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/<cluster-name>.bank?sslmode=verify-full&sslrootcert=<your_certs_directory>/cc-ca.crt'.\n
             If you are using the connection string copied from the Console, your username, password, and cluster name will be pre-populated.\n
             Replace <your_certs_directory> with the path to the cc-ca.cert downloaded from the Console."""
    )

    parser.add_argument("-v", "--verbose",
                        action="store_true", help="print debug info")

    opt = parser.parse_args()
    return opt



def create_movies(conn):
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS movies (id INT PRIMARY KEY, title STRING, run_time STRING, year STRING, imdb_rating STRING, rt_rating STRING, rated STRING, img STRING, description STRING; imdb_votes STRING, genres STRING)"
        )
        # CREATE variable values by looping through movies json, creating list of tuples, and stringifying it
      
        with open("movie_data.json") as json_file:
            data = json.load(movie_data.json)

            str = ""
            genreStr = ""

            for i in data.keys():
                genreStr = ' '.join(sorted(data[i]["genres"]))
                str += ", (" + data[i]["title"] + ", " + data[i]["run_time"] + ", " + data[i]["year"] + ", " + data[i]["imdb_rating"] + ", " + data[i]["rt_rating"] + ", " + data[i]["rated"] + ", " + data[i]["img"] + ", " + data[i]["description"] + ", " + data[i]["imdb_votes"] + ", " + genreStr + ")"

            str = str[2:]

        cur.execute("UPSERT INTO movies (id, title, run_time, year, imdb_rating, rt_rating, rated, img, description, imdb_votes, genres) VALUES " + values)
        logging.debug("create_movies(): status message: %s", cur.statusmessage)
    conn.commit()
        

@app.route('/', methods=['GET'])
def something():
    #content = request.json
    #resp = None
    #return jsonify(response=resp)
    opt = parse_cmdline()
    logging.basicConfig(level=logging.DEBUG if opt.verbose else logging.INFO)
    conn = psycopg2.connect(opt.dsn)
    create_movies(conn)

    conn.close()
    return "Created Movies"

if __name__ == '__main__':
    
    app.run()
