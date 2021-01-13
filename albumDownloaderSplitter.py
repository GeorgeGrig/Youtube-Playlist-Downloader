import youtube_dl
import os,json
#playlisturl = input("Enter your album url: ") 
playlisturl = 'https://www.youtube.com/watch?v=td6yY7_zdE8'

command = f'cmd /c "youtube-dl.exe -x -f bestaudio --audio-format mp3 -o Downloads\%(title)s-%(id)s.%(ext)s --embed-thumbnail --add-metadata --write-info-json {playlisturl}"'
os.system(command)
json_file = f'./Downloads/{[f for f in os.listdir("./Downloads/") if f.endswith(".json")][0]}'
with open(json_file, "r") as read_file:
    data = json.load(read_file)
print(json_file)
input_file = f'./Downloads/{[f for f in os.listdir("./Downloads/") if f.endswith(".mp3")][0]}'
for chapter in data["chapters"]:
    command = f'ffmpeg.exe -i "{input_file}" -ss {chapter["start_time"]} -to {chapter["end_time"]} "./Downloads/{chapter["title"]}.mp3"'
    os.system(command)
os.remove(input_file)
os.remove(json_file)