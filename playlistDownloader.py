import youtube_dl
import os,time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def youtubedl():
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '/%(playlist_title)s/%(title)s.%(ext)s',  #downloads playlist in the folder of the same name
        'download_archive': 'archive.txt',
        'writethumbnail': True,
        'ignoreerrors' : True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320'},
            {
        'key': 'EmbedThumbnail',
    },],
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlisturl])

def main(deezer,sponsorblock):
    if not deezer:
        if sponsorblock:
            command = f'cmd /c "yt-dlp -i -x --audio-format "mp3" -o "/Downloads/%(playlist_title)s/%(title)s.%(ext)s" --audio-quality 0 --no-keep-video --sponskrub-cut {playlisturl}"'
        else:
            command = f'cmd /c "yt-dlp -i -x --audio-format "mp3" -o "/Downloads/%(playlist_title)s/%(title)s.%(ext)s" --audio-quality 0 --no-keep-video {playlisturl}"'
        os.system(command)
    else:
        titles, urls = getPlaylistLinks(playlisturl)
        k = 0
        for title in titles:
            #Search title in deezer
            try:
                deezerLink = deezerSearch(title)
                command = f'cmd /c "deemix -b flac {deezerLink}"'
            except:
                print('Deemix failed, falling back to youtube')
                command = f'cmd /c "yt-dlp -i -x --audio-format "mp3" -o "/Downloads/%(playlist_title)s/%(title)s.%(ext)s" --audio-quality 0 --no-keep-video --sponskrub-cut {urls[k]}"' 
            k += 1
            os.system(command)

def getPlaylistLinks(playlist):
    ydl_opts = {
    'ignoreerrors': True,
    'quiet': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        playlist_dict = ydl.extract_info(playlist, download=False)
        urls = []
        titles = []
        for video in playlist_dict['entries']:
            if not video:
                print('ERROR: Unable to get info. Continuing...')
                continue
            urls.append('https://www.youtube.com/watch?v='+ video.get('id'))
            titles.append(video.get('title'))
        return titles, urls

def deezerSearch(title):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    try:
        stopwords = ['1.','2.','3.','6.','4.','5.','7.','8.','9.','10.','[',']','(',')','lyric video','lyrics video','high quality','music video',' video','hq','Extented','soundtrack','official','remix','ᴴᴰ','- Lyrics','Official Audio','VÍDEO','HD','Audio','audioΑ','with lyrics','Explicit','OFFICIAL VIDEO','Official Audio','official video','Official Video','Official Video', 'with lyrics', 'lyrics','official music video','Official Music Video','Official music Video','Official Music video','Official Video','ost']
        title = title.lower()
        for word in stopwords:
            title = title.replace(word.lower(),"")
        driver.get('https://www.deezer.com/search/'+title)
        time.sleep(5)
        link = 'https://www.deezer.com/' + driver.find_element_by_css_selector('div.datagrid-row:nth-child(1) > div:nth-child(3) > div:nth-child(1) > a:nth-child(1)').get_attribute('href')
        driver.close()
    except:
        driver.close()
    return link

#To change deemix download path go to%AppData%\Roaming\deemix\config.json
playlisturl = input("Enter your playlist url: ") 
deezer = True
sponsorblock = True
deezer = input('Use deezer API when possible? (True or False): ')
sponsorblock = input('Use sponsorblock API when possible? (True or False): ')
main(deezer,sponsorblock)