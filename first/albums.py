import json
import os

import requests

from exceptions import ResponseException
from secrets import spotify_token, spotify_user_id

 #Create A New Playlist
class Albums:
    def __init__(self):
        self.id = spotify_user_id
        self.albums = []
        self.genres = []
    def getreleasedate(self,albumid):

        # Initial Query
        query = "https://api.spotify.com/v1/albums/{}".format(albumid)
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        # Initial Response
        json_response = response.json()
        release_date = json_response["release_date"]
        year = int(release_date[0:4])
        return(year)
    def getreleasedates(self,albums):
        # Initial Query
        albums =list(filter(None, albums))
        s = ","
        s = s.join(albums)
        query = "https://api.spotify.com/v1/tracks/?ids={}".format(s)
        print(query)
        response = requests.get(
        query,
        headers={
             "Content-Type": "application/json",
             "Authorization": "Bearer {}".format(spotify_token)
        }
        )
        # Initial Response
        json_response = response.json()
        print(json_response)
        resalbums = json_response["tracks"]
        years =[]
        i =0
        for i in range(0,len(albums)):
            release_date = resalbums[i]["album"]['release_date']
            years.append(int(release_date[0:4]))
        return(years)
    def isNinetys(self,albumid): 
        year =self.getreleasedate(albumid)
        if(1990 <= year and year <= 1999):
            return True
        else:
            return False
    def isEightys(self,albumid): 
        year =self.getreleasedate(albumid)
        if(1980 <= year and year <= 1989):
            return True
        else:
            return False 
        year =self.getreleasedate(albumid)
        if(1970 <= year and year <= 1979):
            return True
        else:
            return False
    def canyougetanyolder(self,albumid): 
        year =self.getreleasedate(albumid)
        if(year <= 1969):
            return True
        else:
            return False
    def getgenres(self,artistids):
        self.genres = []
        s = ","
        s = s.join(artistids)
        query = "https://api.spotify.com/v1/artists/?ids={}".format(s)
        print(query)
        response = requests.get(
        query,
        headers={
             "Content-Type": "application/json",
             "Authorization": "Bearer {}".format(spotify_token)
        }
        )
        # Initial Response
        json_response = response.json()
        genalbums = json_response["artists"]
        i =0
        for i in range(0,len(genalbums)):
            genre = genalbums[i]["genres"]
            if len(genre)>0:
                s =  ","
                s = s.join(genre)
                self.genres.append(s)
            else:
                self.genres.append("No genre available")
        print(len(self.genres))
        return(self.genres)
cp = Albums()