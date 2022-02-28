import pandas as pd
import requests
import psycopg2
from sqlalchemy import create_engine

TOKEN = "BQA9kX7H78kJBwy6LxRe1CL48VeUb2juWZvQsghPZeg1E_4pDF-kxohgFrYKqnYOP46lkbDb6aBZbkmQu7O2aSjx_iLQ4ciiBqVErTRpyAtSh8D3_CLH2w8OxaRrdq0yYxhsksBmIDJ4ADva0SgTq0jPpjAGn4InDvJhpKkyu1ZB"

if __name__ == "__main__":
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played", headers=headers)

    data = r.json()

song_names = []
popularity = []
artist_names = []
played_at_list = []
timestamps = []

for song in data["items"]:
    song_names.append(song["track"]["name"])
    popularity.append(song["track"]["popularity"])
    artist_names.append(song["track"]["album"]["artists"][0]["name"])
    played_at_list.append(song["played_at"])
    timestamps.append(song["played_at"][0:10])

song_dict = {
    "song_name": song_names,
    "popularity": popularity,
    "artist_name": artist_names,
    "played_at": played_at_list,
    "timestamps": timestamps
}

song_df = pd.DataFrame(song_dict, columns=["song_name", "popularity", "artist_name", "played_at", "timestamps"])


# print(song_df)

def create_tables():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS get_recently_played_track (
            ID SERIAL PRIMARY KEY,
            song_name VARCHAR(255),
            popularity SMALLINT,
            artist_name VARCHAR(255),
            played_at timestamp,
            timestamps date
        )
        """)
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="spotifydb",
            user="postgres",
            password="Pa55w.rd"
        )
        cur = conn.cursor()
        cur.execute(commands)
        cur.close()
        conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


create_tables()
engine = create_engine('postgresql+psycopg2://postgres:Pa55w.rd@localhost:5432/spotifydb')
song_df.to_sql('get_recently_played_track', con=engine, if_exists='append', index=False)
