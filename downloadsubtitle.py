from youtube_transcript_api import YouTubeTranscriptApi
import re
from pytube import YouTube

def download_subtitles(url, filename):
    try:
        # Get the transcript for the video
        transcript = YouTubeTranscriptApi.get_transcript(url)

        # Build the SRT string
        srt = ''
        for i, line in enumerate(transcript):
            start = line['start']
            end = line['start'] + line['duration']
            text = line['text']
            srt += f"{i+1}\n{convert_to_srt_timestamp(start)} --> {convert_to_srt_timestamp(end)}\n{text}\n\n"

        # Save the SRT file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(srt)

        print(f"Subtitles downloaded and saved as '{filename}'.")
    except Exception as e:
        print(f"Error downloading subtitles: {str(e)}")

def convert_to_srt_timestamp(seconds):
    h = int(seconds / 3600)
    m = int(seconds / 60 % 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def cut_Youtube_url(url):
        match = re.search(r'(?<=\?v=)[\w-]+', url)
        if match:
            video_id = match.group(0)
            print(video_id)  # Output: -GwBNwZOPUs
            return video_id
        else:
            print('No match found')
            return ""
def get_video_name (link) : 
    yt = YouTube(link)
    stream = yt.streams.get_highest_resolution()
    video_title = stream.title.replace('\\', '').replace('/', '').replace(':', '').replace(
                        '*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '') 
    return video_title
               
                    
# url = "-GwBNwZOPUs" 


# url = "https://www.youtube.com/watch?v=yvaR4MW5u4k&list=PLEWFSKHjyrwyyYTnBXYHmIbm-2vVP5Wfg&index=3"
# url = "https://www.youtube.com/watch?v=FloKO5sSHTg&list=PLEWFSKHjyrwyyYTnBXYHmIbm-2vVP5Wfg&index=4"
url = "https://www.youtube.com/watch?v=IOnVV7Fbv5g&t=3s"
download_subtitles(cut_Youtube_url(url), get_video_name(url) + '.srt')
