import xml.etree.ElementTree as ET
import shutil
import urllib.parse
import os
import sys
from pathlib import Path


def main():
    root = get_sys_arg('iml_path=')
    if root is None:
        print("You need to provide the path to your itunes music library. "
              "(iml_path=\"X:\path\\to\library\iTunes Music Library.xml\")")
        exit()

    playlist_name = get_sys_arg('p_name=')
    if playlist_name is None:
        print("You need to provide the name of a playlist. (p_name=\"playlist name\")")
        exit()

    root = ET.parse(root).getroot()
    playlists_root = get_playlists_root(root)
    tracks_root = get_tracks_root(root)

    playlist = find_playlist_tracks(playlists_root, playlist_name)
    if playlist is None:
        print("Playlist couldn't be found. Please check for typos.")
    else:
        track_ids = get_track_ids(playlist)
        track_locations = get_track_locations(track_ids, tracks_root)
        copy_tracks_to(track_locations)


def get_sys_arg(arg_name):
    for arg in sys.argv:
        if arg.startswith(arg_name):
            return arg[len(arg_name):]
    return None


def copy_tracks_to(track_locations):
    dst = get_sys_arg('dst=')
    if dst is None:
        dst = os.path.realpath(__file__).rpartition('\\')[0]
        dst = os.path.join(dst, 'dst')
        if not os.path.exists(dst):
            Path(dst).mkdir(parents=True, exist_ok=True)

    if not os.path.exists(dst):
        print("The given output folder does not exist.")
        exit()

    tracks_len = len(track_locations)
    for i in range(tracks_len):
        track_location = urllib.parse.unquote(track_locations[i][17:])
        shutil.copy2(track_location, dst)
        print("Copying track {} of {}.".format(i+1, tracks_len), end='\r', flush=True)


def get_track_locations(track_ids, tracks_root):
    track_locations = []
    for track_id in track_ids:
        track_locations.append(find_track_location_by_id(tracks_root, track_id))
    return track_locations


def find_track_location_by_id(tracks_root, track_id):
    track_found = False
    location_found = False

    for track in tracks_root:
        if track_found:
            for data in track:
                if location_found:
                    return data.text
                if data.text == 'Location':
                    location_found = True
            track_found = False
        if track.tag == 'key' and track.text == track_id:
            track_found = True


def get_tracks_root(root):
    tracks_tag_found = False

    for dicti in root:
        for element in dicti:
            if tracks_tag_found:
                return element
            if element.text == 'Tracks':
                tracks_tag_found = True


def get_playlists_root(root):
    playlist_tag_found = False
    for dicti in root.findall('dict'):
        for key in dicti:
            if playlist_tag_found:
                return key
            if key.text == 'Playlists':
                playlist_tag_found = True


def find_playlist_tracks(playlists, p_name):
    for playlist in playlists.findall('dict'):
        correct_playlist_found = False
        for element in playlist:
            if correct_playlist_found and element.tag == 'array':
                return element
            if element.text == p_name:
                correct_playlist_found = True


def get_track_ids(playlist):
    track_ids = []
    for track in playlist:
        for element in track:
            if element.tag == 'integer':
                track_ids.append(element.text)
    return track_ids


if __name__ == '__main__':
    main()
