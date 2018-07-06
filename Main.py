from __future__ import unicode_literals
import sys
import os
import subprocess
import youtube_dl
from datetime import datetime
from threading import Timer
from apscheduler.schedulers.blocking import BlockingScheduler
playlisturl = 'https://www.youtube.com/playlist?list='


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def main():
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


### scheduler ###
scheduler = BlockingScheduler()
scheduler.add_job(main, 'interval', hours=24)
scheduler.start()