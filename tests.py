
import pychromecast
from pychromecast.controllers.youtube import YouTubeController
import urllib.error
import urllib.parse
import urllib.request
import re


# extract the youtube links from the provided search_list
def get_youtube_links(search_list):
    search_text = str(search_list)
    query = urllib.parse.quote(search_text)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    # Get all video links from page
    temp_links = []
    all_video_links = re.findall(r'href=\"\/watch\?v=(.{11})', html.decode())
    for each_video in all_video_links:
        if each_video not in temp_links:
            temp_links.append(each_video)
    video_links = temp_links
    # Get all playlist links from page
    temp_links = []
    all_playlist_results = re.findall(r'href=\"\/playlist\?list\=(.{34})', html.decode())
    sep = '"'
    for each_playlist in all_playlist_results:
        if each_playlist not in temp_links:
            cleaned_pl = each_playlist.split(sep, 1)[0]  # clean up dirty playlists
            temp_links.append(cleaned_pl)
    playlist_links = temp_links
    yt_links = []
    if video_links:
        yt_links.append(video_links[0])
        print("Found Single Links: " + str(video_links))
    if playlist_links:
        yt_links.append(playlist_links[0])
        print("Found Playlist Links: " + str(playlist_links))
    return yt_links


def begin_cast():
    cast = pychromecast.Chromecast('192.168.0.37')
    cast.wait()
    mc = cast.media_controller
    #mc.play_media('http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4', 'video/mp4')
    #mc.block_until_active()
    #mc.play()
    mc.stop()

def cast_youtube(videoID):
    cast = pychromecast.Chromecast('192.168.0.37')
    cast.wait()
    yt = YouTubeController()
    cast.register_handler(yt)
    yt.play_video(videoID)

newID = get_youtube_links('captain marvel trailer')[0]
print(newID)
cast_youtube(newID)

