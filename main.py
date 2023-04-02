import tkinter as tk
from tkinter import filedialog
import os
from pytube import YouTube

def choose_folder():
    # Function to allow user to choose the output folder
    output_folder = filedialog.askdirectory()
    output_folder_text.set(output_folder)
    return output_folder

def download_video(url, output_folder, use_timestamp=False):
    try:
        yt = YouTube(url)
        # Get the video title
        title = yt.title
        # Create the filename based on the chosen pattern
        if use_timestamp:
            filename = str(int(yt.publish_date.timestamp())) + ".mp4"
        else:
            filename = title + ".mp4"
        # Download the video to the chosen output folder
        yt.streams.first().download(output_folder, filename=filename)
        print("Downloaded:", title)
        return True
    except Exception as e:
        print("Failed to download:", url)
        print(e)
        return False

def process_links():
    # Function to process links added to the list box
    output_folder = output_folder_text.get()
    use_timestamp = use_timestamp_var.get()
    for url in links_listbox.get(0, tk.END):
        success = download_video(url, output_folder, use_timestamp)
        if not success:
            continue

# root = tk.Tk()

# # Create the text box for the output folder
# output_folder_text = tk.StringVar()
# output_folder_textbox = tk.Entry(root, textvariable=output_folder_text)
# output_folder_textbox.pack()

# # Add a button to choose the output folder
# choose_folder_button = tk.Button(root, text="Choose Folder", command=choose_folder)
# choose_folder_button.pack()

# # Add a checkbox to choose the filename pattern
# use_timestamp_var = tk.BooleanVar()
# use_timestamp_checkbox = tk.Checkbutton(root, text="Use Timestamp", variable=use_timestamp_var)
# use_timestamp_checkbox.pack()

# # Create the list box for adding video links
# links_listbox = tk.Listbox(root)
# root.mainloop()


def download_video(url, output_path):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    video_title = stream.title.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
    filename = f"{video_title}.mp4"
    output_file = os.path.join(output_path, filename)
    stream.download(output_path=output_path, filename=filename)
    print(f"Downloaded video from {url} to {output_file}")

url = "https://www.youtube.com/watch?v=vfg8pwjJVIc&t=60s"
folder = "D:/tmp"

import sys

def download_video(url):
    try:
        yt = YouTube(url)
    except:
        print("Invalid URL, please try again!")
        sys.exit(1)
    
    print(f"Downloading {yt.title}...")
    stream = yt.streams.get_highest_resolution()
    filesize = stream.filesize
    print(f"Filesize: {filesize / (1024*1024):.2f} MB")

    # Show download progress
    def show_progress_bar(stream, chunk, file_handle, bytes_remaining):
        remaining = round(100 * bytes_remaining / filesize)
        completed = 100 - remaining
        progress_bar = "#" * completed + "-" * remaining
        sys.stdout.write(f"\r{progress_bar} {completed}%")
        sys.stdout.flush()

    stream.download(output_path="./downloads", filename=yt.title, on_progress_callback=show_progress_bar)
    print(f"\n{yt.title} has been downloaded to ./downloads!")


def download_srt(video_url, output_path):
    # Create a YouTube object and get the video's captions
    youtube = YouTube(video_url)
    captions = youtube.captions

    # Select the first available caption (usually in English)
    caption = captions.get_by_language_code('en')

    # Download the caption and save it to the output path
    if caption:
        srt_file = caption.generate_srt_captions()
        with open(os.path.join(output_path, f'{youtube.title}.srt'), 'w') as f:
            f.write(srt_file)
        print('SRT file downloaded successfully!')
    else:
        print('No caption available for this video.')

if __name__ == "__main__":
    # url = input("Please enter a YouTube URL: ")
    url = "https://www.youtube.com/watch?v=yvaR4MW5u4k"
    download_srt(url, folder)
