import mysql.connector
from fastapi import FastAPI
from typing import Optional 
import json
from mysql.connector import Error
from pydantic import BaseModel
import os 

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB = "kfm8nx"

db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur=db.cursor()




@app.get('/genres')
def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}



@app.get('/songs')
def get_songs():
    query = """
    SELECT 
        songs.title,
        songs.album,
        songs.artist,
        songs.year,
        songs.file AS song_file,
        songs.image AS song_image,
        genres.genre
    FROM songs
    JOIN genres ON songs.genre = genres.genreid;
    """
    try:
        cur.execute(query)
        headers = [x[0] for x in cur.description]
        results = cur.fetchall()
        json_data = []
        for result in results:
            json_data.append(dict(zip(headers, result)))
        return json_data
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}

