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
cp = Albums()