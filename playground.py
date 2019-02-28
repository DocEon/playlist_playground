# -*- coding: utf-8 -*-
"""
"""
import os
import csv
# todo: get list of top-played artists for each season / month
# todo: get list of top-played tracks for each season / month

# todo: hook up with Echo Nest for BPM info
# todo: export new spotify playlists

directory = r"jpmb_playlists"
playground_dict = {}
all_songs = []
all_playlists = []

summer_months = ["june", "july", "august"]
fall_months = ["september", "october", "november"]
winter_months = ["december", "january", "february"]
spring_months = ["march", "april", "may"]

class Playlist:
    
    def __init__(self, month, year):
        self.month = month
        self.year = year
        self.song_list = []
        self.name = month + " " + year
        
    def addSong(self, song):
        self.song_list.append(song)
    
class Song:
    
    def __init__(self, uri, added_by, album, artist, duration, title, track_number, added_at):
        self.title = title
        self.artist = artist
        self.uri = uri
        self.added_by = added_by
        self.duration = duration
        self.track_number = track_number
        self.added_at = added_at
        self.album = album
        self.playlists = []
        self.plays = 0
        
    def description(self):
        return "{} : {} plays {} times.".format(self.title, self.artist, self.plays)
    
    def onPlaylist(self, playlist_name):
        self.playlists.append(playlist_name)
        self.plays = len(self.playlists)
        
    def playsWhere(self):
        outputString = "\n{} by {} plays on the following {} playlists:".format(self.title, self.artist, self.plays)
        for playlist in self.playlists:
            outputString += "\n\t{}".format(playlist)
        return outputString
        
def makeDictIntoSong(song_dict):
    uri = song_dict['\ufeff\ufeffSpotify URI']
    track_number = song_dict['Track Number']
    title = song_dict['Track Name']
    duration = song_dict['Track Duration (ms)']
    artist = song_dict['Artist Name']
    added_by = song_dict['Added By']
    added_at = song_dict['Added At']
    album = song_dict['Album Name']
    newSong = Song(uri, added_by, album, artist, duration, title, track_number, added_at)
    return newSong

def initialize_objects(playground_dict):
    playlist_list = list(playground_dict.keys())
    for x in range(0, len(playlist_list)):
        playlist = playground_dict[playlist_list[x]]
        playlist_name = playlist_list[x]
        playlist_month = playlist_name.split('_')[0]
        playlist_year = playlist_name.split('_')[1]
        newPlaylist = Playlist(playlist_month, playlist_year)
        song_list = []
        for song in playlist.keys():
            song_from_dict = playlist[song]
            currentSong = next((track for track in all_songs if track.uri == song_from_dict['\ufeff\ufeffSpotify URI']), None)
            if currentSong == None:
                currentSong = makeDictIntoSong(song_from_dict)
                all_songs.append(currentSong)
            currentSong.onPlaylist(playlist_name)
            song_list.append(currentSong)
            newPlaylist.addSong(currentSong)
        all_playlists.append(newPlaylist)


            
def getFileNames(directory):
  path_list = []
  for root, dirs, files in os.walk(directory, topdown=False):
    for name in files:
      f = os.path.join(root, name)
      path_list.append(f)
  return path_list

def makePlaylistDict(csvPath):
    headerList = []
    playlist_dict = {}
    with open(csvPath, encoding = 'utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                for entry in row:
                    headerList.append(entry)
                line_count += 1
            else:
                playlist_dict[row[0]] = {}
                for x in range(0, len(headerList)):
                    playlist_dict[row[0]][headerList[x]] = row[x]
    return playlist_dict

def initialize(path_list):
    playground_dict = {}
    for path in path_list:
        playground_dict[path.split("/")[1].split(".")[0]] = makePlaylistDict(path)
    return playground_dict


def prettyPrintPlaylist(playlist_dict):
    track_number = 1
    for key in playlist_dict:
        print("Track " + str(track_number) + ": " + playlist_dict[key]["Track Name"] + " || " + playlist_dict[key]["Artist Name"])
        track_number += 1
        
def getListOfAllTracks(playground_dict):
    list_of_songs = []
    for playlist in playground_dict:
        for song in playground_dict[playlist]:
            list_of_songs.append(playground_dict[playlist][song]["Track Name"] + ", " + playground_dict[playlist][song]["Artist Name"])
    return list_of_songs

def getNumberedList(list_of_songs):
    numbered_list = []
    for song in list_of_songs:
        if list_of_songs.count(song) > 1:
            count_list = [list_of_songs.count(song), song]
            numbered_list.append(count_list)
    return numbered_list

def getSeasonDict(season_months):
    season_dict = {}
    playlists_list = playground_dict.keys()
    for playlist in playlists_list:
        for month in season_months:
            if month in playlist:
                season_dict[playlist] = playground_dict[playlist]
    return season_dict
        


path_list = getFileNames(directory)
playground_dict = initialize(path_list)
list_of_songs = getListOfAllTracks(playground_dict)
initialize_objects(playground_dict)

oneplays = [song for song in all_songs if song.plays == 1]
twoplays = [song for song in all_songs if song.plays == 2]
threeplays = [song for song in all_songs if song.plays == 3]
fourplays = [song for song in all_songs if song.plays == 4]
fiveplays = [song for song in all_songs if song.plays == 5]
sixplays = [song for song in all_songs if song.plays == 6]