import json
import os

import requests

from exceptions import ResponseException
from secrets import spotify_token, spotify_user_id
from albums import Albums
import openpyxl

 #Create A New Playlist
class Library:
    def __init__(self):
        self.trackids = []
        self.tracknames = []
        self.albumids = []
        self.ninetysalbums = []
        self.eightysalbums = []
        self.seventysalbums =[]
        self.canyougetanyolder = []
        self.wb = openpyxl.Workbook()
    def getTracks(self):
        
        # Initial Query
        query = "https://api.spotify.com/v1/me/tracks?limit=50&offset=0"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        # Initial Response
        json_response = response.json()
        items = json_response["items"]
        totalsongs = json_response["total"]
        print(totalsongs)
        runtimes = int(totalsongs/50)
        print(runtimes)
        count = 0
        i=0
        row=0
        #Loop
        while count < runtimes:
            while i < 49: 
                trackname = items[i]['track']['name']
                trackid = items[i]['track']['uri']
                albumid = items[i]['track']['album']['id']
                print(trackname+ " " + albumid)
                self.tracknames.append(trackname)
                self.trackids.append(trackid)
                self.albumids.append(albumid)
                ws = self.wb.active
                ws.cell(row=row+1, column=1).value = trackname
                ws.cell(row=row+1, column=2).value = trackid
                ws.cell(row=row+1, column=3).value = albumid
                row = row +1
                i = i + 1
        #New Query
            i=0
            print(json_response['next'])
            query = json_response['next']
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(spotify_token)
            })
            json_response = response.json()
            items = json_response["items"]
            self.wb.save("Spotify Library.xlsx")
            print(str(count+1) + " out of " + str(runtimes) + " Done")
            count = count + 1
    def whatdecade(self):
        count = 1
        for i in range(len(self.albumids)):
            cp = Albums()
            if cp.isEightys(self.albumids[i]):
                self.eightysalbums.append(self.trackids[i])
            if count % 100 == 0:
                print(count)
            count = count + 1
        print(self.eightysalbums)
        print("Decades Done")
    def create90s_playlist(self):
        request_body = json.dumps({
            "name": "That's So 90s",
            "description": "Songs from the 90s",
            "public": False
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        # playlist id
        print(response_json["id"])
        return response_json["id"]    
    def add90ssong_to_playlist(self):

        # collect all of uri
        uris = self.ninetysalbums
        # uri limit is 100 per request       
        request_len = round(len(uris)/100) #4
        # create a new playlist
        playlist_id = self.create90s_playlist()
        print(playlist_id)
        # add all songs into new playlist
        i = 0
        begin = 0
        end = 99
        while i < request_len:
            thisuris = uris[begin:end]
            request_data = json.dumps(thisuris)

            query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

            response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        # check for valid response status
            if response.status_code != 201:
                raise ResponseException(response.status_code)
            response_json = response.json()
            print("Successful Upload")
            print(response_json)
            i = i+1
            begin = begin + 100
            if i == request_len-1:
               end = len(uris)-1
            else:
                end = end + 100
        return response_json
    def create80s_playlist(self):
        request_body = json.dumps({
            "name": "That's So 80s",
            "description": "Songs from the 80s",
            "public": False
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        # playlist id
        print("Playlist Created. You may now add your songs with the id below")
        print(response_json["id"])
        return response_json["id"]
    def add80ssong_to_playlist(self):

        # collect all of uri
        uris = self.eightysalbums
        print(self.albumids)
        # uri limit is 100 per request       
        request_len = round(len(uris)/100) #4
        # create a new playlist
        playlist_id = self.create80s_playlist()
        print(playlist_id)
        # add all songs into new playlist
        i = 0
        begin = 0
        end = 99
        while i < request_len:
            thisuris = uris[begin:end]
            request_data = json.dumps(thisuris)

            query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

            response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        # check for valid response status
            if response.status_code != 201:
                raise ResponseException(response.status_code)
            print(response.json())
            response_json = response.json()
            print("Successful Upload")
            i = i+1
            begin = begin + 100
            if i == request_len-1:
               end = len(uris)-1
            else:
                end = end + 100
        return response_json
    def create70s_playlist(self):
        request_body = json.dumps({
            "name": "That's So 70s",
            "description": "Songs from the 70s",
            "public": False
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        # playlist id
        print(response_json["id"])
        return response_json["id"]    
    def add70ssong_to_playlist(self):

        # collect all of uri
        uris = self.seventysalbums
        # uri limit is 100 per request       
        request_len = round(len(uris)/100) #4
        # create a new playlist
        playlist_id = self.create70s_playlist()
        print(playlist_id)
        # add all songs into new playlist
        i = 0
        begin = 0
        end = 99
        while i < request_len:
            thisuris = uris[begin:end]
            request_data = json.dumps(thisuris)

            query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

            response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        # check for valid response status
            if response.status_code != 201:
                raise ResponseException(response.status_code)
            response_json = response.json()
            print("Successful Upload")
            print(response_json)
            i = i+1
            begin = begin + 100
            if i == request_len-1:
               end = len(uris)-1
            else:
                end = end + 100
        return response_json
    def createoldies_playlist(self):
        request_body = json.dumps({
            "name": "That's So Ancient",
            "description": "Songs from 1969 and before",
            "public": False
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        # playlist id
        print(response_json["id"])
        return response_json["id"]      
    def addoldsong_to_playlist(self):

        # collect all of uri
        uris = self.canyougetanyolder
        # uri limit is 100 per request       
        request_len = round(len(uris)/100) #4
        # create a new playlist
        playlist_id = self.createoldies_playlist()
        print(playlist_id)
        # add all songs into new playlist
        i = 0
        begin = 0
        end = 99
        while i < request_len:
            thisuris = uris[begin:end]
            request_data = json.dumps(thisuris)

            query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

            response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        # check for valid response status
            if response.status_code != 201:
                raise ResponseException(response.status_code)
            response_json = response.json()
            print("Successful Upload")
            print(response_json)
            i = i+1
            begin = begin + 100
            if i == request_len-1:
               end = len(uris)-1
            else:
                end = end + 100
        return response_json
    def openLibrary(self):
        wb = openpyxl.load_workbook("Spotify Library.xlsx")
        ws = wb.worksheets[0]
        i=0
        yearsadded = 0
        totalrows = ws.max_row
        while i < totalrows and yearsadded < 1000:
            cp = Albums()
            albumid = ws.cell(row=i+1,column=3).value
            if ws.cell(row=i+1, column=4).value is None: 
                ws.cell(row=i+1, column=4).value = cp.getreleasedate(albumid)
                yearsadded = yearsadded + 1
                print(str(yearsadded) + " have been added.")
                wb.save("Spotify Library Years.xlsx")
            i=i+1
        
cp = Library()
#cp.getTracks()
#cp.whatdecade() 
cp.openLibrary()
#cp.create80s_playlist()
#cp.add80ssong_to_playlist()
#cp.add90ssong_to_playlist()
