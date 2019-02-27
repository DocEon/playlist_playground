# -*- coding: utf-8 -*-
"""
"""
import os
import csv

directory = r"jpmb_playlists"
playground_dict = {}

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
        playground_dict[path.split("\\")[1].split(".")[0]] = makePlaylistDict(path)
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
            

def main():
    path_list = getFileNames(directory)
    playground_dict = initialize(path_list)
    list_of_songs = getListOfAllTracks