import os
try:
    from pytube import YouTube,Playlist
except:
    os.system("pip install pytube")
    from pytube import YouTube,Playlist
try:
    from moviepy.editor import *
except:
    os.system("pip install moviepy")
    from moviepy.editor import *
import requests
import urllib.parse

try:
    from tqdm import tqdm
except:
    os.system("pip install tqdm")
    from tqdm import tqdm
import json


def get_playlist_video_urls(playlist_url):
    playlist = Playlist(playlist_url)
    video_urls = [video.watch_url for video in playlist.videos]
    return video_urls
def StartYoutube(url):
    video_urls = get_playlist_video_urls(url)
    for url in video_urls:
        yt = YouTube(url)
        title = yt.title
        yt.streams.get_highest_resolution().download()
        VideoFileClip(f'{title}.mp4').audio.write_audiofile(f'{title}.mp3')
        os.remove(f'{title}.mp4')
        
def Spotify(url,start,end):
    headers = {
        "authority":"api-partner.spotify.com",
        "Authorization":f"Bearer {requests.get(url).text.split('accessToken')[1][3:-3]}",
    }
    query = {"uri":f"spotify:playlist:{url.split('/')[-1].split('?')[0]}","offset":start,"limit":end}
    playlistRequest = f'https://api-partner.spotify.com/pathfinder/v1/query?operationName=fetchPlaylist&variables={str(urllib.parse.quote(str(query).replace(" ",""), safe="")).replace("%27","%22")}&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2291d4c2bc3e0cd1bc672281c4f1f59f43ff55ba726ca04a45810d99bd091f3f0e%22%7D%7D'
    dat = requests.get(playlistRequest , headers=headers).text
    SearchonYoutube([[i['itemV2']['data']['name'],[x["profile"]['name'] for x in i['itemV2']['data']['artists']['items']]] for i in json.loads(dat)["data"]["playlistV2"]["content"]["items"]],
                    json.loads(dat)['data']['playlistV2']['name'])
def SearchonYoutube(nameAndURLS,PlaylistTitle):
    YoutubeRequest = "https://www.youtube.com/youtubei/v1/search?prettyPrint=false"
    illegalChars = ['\\','/',':','*','?','"','<','>','|',"'",".",","]
    for i in illegalChars:
        PlaylistTitle = PlaylistTitle.replace(i,'')
    payload = {"context":{
        "client":{
            "hl":"en-GB",
            "gl":"GB",
            "visitorData":"CgtTMWE1NWMzQzI4SSjVyZSyBjIKCgJHQhIEGgAgXQ%3D%3D",
            "clientName":"WEB",
            "clientVersion":"2.20240514.03.00",
            "configInfo":{"appInstallData":"CNXJlLIGEPSp_xIQt6uwBRDM364FEO6irwUQl4OwBRCd0LAFEO_NsAUQ1t2wBRCJ6K4FEPvasAUQ9quwBRDJ17AFEOOt_xIQ77KwBRCmmrAFEPXksAUQ0-GvBRCB7bAFELHcsAUQ2eCwBRD55LAFEPyFsAUQopKwBRDj0bAFEOvo_hIQt--vBRDzobAFEKzqsAUQiOOvBRDeiP8SEOe6rwUQjcywBRDI5rAFEJaVsAUQ_-SwBRC70q8FEPvwsAUQq--wBRCCov8SEJnxsAUQ1KGvBRD14LAFENbnsAUQvoqwBRCX8bAFEPjSsAUQ6sOvBRDDzLAFEIiHsAUQ65OuBRCCorAFEMn3rwUQ8-CwBRC9tq4FENfgsAUQo-2wBRDi1K4FEI_EsAUQoOiwBRD98LAFEM3XsAUQ_eCwBRC36v4SEIvPsAUQooGwBRC9mbAFEPrrsAUQ69uwBRDPqLAFENfprwUQjO6wBRCQsrAFENuvrwUQ0I2wBRCDv7AFEJXxsAUQvvmvBRCM6LAFEN3o_hIQ7rOwBRCK7rAFEJ7ksAUQ9OuwBRDnw7AFENHgsAUQ9KuwBRCK7LAFEMf9tyIQqJqwBRCa8K8FEP_fsAUQ0-CwBRCn47AFEKXC_hIQreOwBRDY3bAFEKzYsAUQlp__EhDViLAFEOavsAUQ__CwBRCq2LAFENnJrwUQ-tCwBRDx2LAFEJis_xIqIENBTVNGQlVYb0wyd0ROSGtCcUNROUF2WkctcXhCQjBI"},
            }},
        "query":""}
    if not os.path.exists(PlaylistTitle):os.makedirs(PlaylistTitle)
    if not os.path.exists("cache"):os.makedirs("cache")
    for x in tqdm(nameAndURLS):
        payload["query"] = f"{x[0]} by {' & '.join(x[1])}"
        for i in json.loads(requests.post(YoutubeRequest, json=payload).text)['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']:
            if "videoRenderer" in i.keys():
                try:
                    yt = YouTube("https://www.youtube.com"+i['videoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url'])
                    title = yt.title
                    for i in illegalChars:
                        title = title.replace(i,'')
                        x[0] = x[0].replace(i,'')
                    yt.streams.get_highest_resolution().download(f"cache/")
                    video = VideoFileClip(f"cache/{title}.mp4", verbose=False)
                    audio = video.audio
                    audio.write_audiofile(f"{PlaylistTitle}/{x[0]} by {' & '.join(x[1])}.mp3")
                    audio.close()
                    video.close()
                    os.remove(f"cache/{title}.mp4")
                    break
                except Exception as e:
                    print(e)
while True:
    while True:
        try:
            choice = int(input("""----------------------------
1. Download Youtube Playlist
2. Download Spotify Playlist
0. Exit
----------------------------
choice: """))
            break
        except:
            print("----------------------------\nInvalid Choice\n----------------------------")
    if choice == 1:
        while True:
            url = input("Enter Youtube Playlist URL: ")
            if "https://www.youtube.com/playlist?" in url:
                break
            else:
                print("Invalid URL, try again.")
        StartYoutube(url)
    elif choice == 2:
        while True:
            url = input("Enter Spotify Playlist URL: ")
            if "https://open.spotify.com/playlist/" in url:
                break
            else:
                print("Invalid URL, try again.")
        while True:
            try:
                start = input("Enter Start Index (default=0): ")
                if start == "":start = 0
                elif int(start) < 0:start = 0
                else:start = int(start)
                break
            except:print("Invalid Number")
        
        while True:
            try:
                end = input("How many songs(default=25): ")
                if end == "":end = 25
                elif int(end) < 1:end = 25
                else:end = int(end)
                break
            except:print("Invalid Number")
        if end == 0:
            print("Invalid Number of Songs")
            continue
        Spotify(url,start,end)
    elif choice == 0:
        break
    else:
        print("----------------------------\nInvalid Choice\n----------------------------")
