import os
import re
import tkinter as tk
from tkinter import filedialog
from pytube import YouTube
# Adding progress bar
import tkinter.ttk as ttk
from youtube_transcript_api import YouTubeTranscriptApi


class YouTubeDownloader:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Downloader")

        # Create and place add link button and text box
        self.link_text = tk.StringVar()
        self.link_label = tk.Label(master, text="Enter YouTube Link:")
        self.link_label.grid(row=0, column=0, pady=10)
        self.link_entry = tk.Entry(
            master, textvariable=self.link_text, width=40)
        self.link_entry.grid(row=0, column=1, padx=5, pady=10)
        self.add_link_button = tk.Button(
            master, text="Add Link", command=self.add_link)
        self.add_link_button.grid(row=0, column=2, padx=5, pady=10)

        # Create and place output folder button and text box
        self.folder_path = tk.StringVar()
        self.folder_label = tk.Label(master, text="Select Output Folder:")
        self.folder_label.grid(row=1, column=0, pady=10)
        self.folder_entry = tk.Entry(
            master, textvariable=self.folder_path, width=40)
        self.folder_entry.grid(row=1, column=1, padx=5, pady=10)
        self.folder_button = tk.Button(
            master, text="Choose Folder", command=self.choose_folder)
        self.folder_button.grid(row=1, column=2, padx=5, pady=10)

        # Create and place filename pattern checkbox
        self.filename_var = tk.IntVar()
        self.filename_checkbox = tk.Checkbutton(
            master, text="Use video title as filename", variable=self.filename_var)
        self.filename_checkbox.grid(row=2, column=1, pady=10)

        # To add a checkbox to let the user check whether the file exists or not,
        self.check_var = tk.IntVar()
        self.check_button = tk.Checkbutton(
            master, text="SKip if file existence", variable=self.check_var)
        self.check_button.grid(row=2, column=2, pady=10)

        # add download subtitle.
        self.subtitle_checkbox_var = tk.IntVar()
        self.subtitle_checkbox_button = tk.Checkbutton(
            master, text="Download subtitle", variable=self.subtitle_checkbox_var)
        self.subtitle_checkbox_button.grid(row=2, column=3, pady=10)

        # Create and place list box and start button
        self.listbox_label = tk.Label(master, text="YouTube Video Links:")
        self.listbox_label.grid(row=3, column=0, pady=10)
        self.listbox = tk.Listbox(master, height=10, width=60)
        self.listbox.grid(row=4, column=0, columnspan=3, padx=5, pady=10)
        self.start_button = tk.Button(
            master, text="Start Download", command=self.start_download)
        self.start_button.grid(row=5, column=1, padx=5, pady=2)

        # Create and place delete button
        self.delete_button = tk.Button(
            master, text="Delete Link", command=self.delete_link)
        self.delete_button.grid(row=5, column=2, padx=5, pady=2)

        # load data button.
        self.load_data_button = tk.Button(
            master, text="Load Data", command=self.load_data)
        self.load_data_button.grid(row=5, column=3, padx=5, pady=2)

        # Create and place progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            master, variable=self.progress_var, length=200)
        self.progress_bar.grid(row=6, column=1, pady=10)

        # Initialize output folder path and list of links
        self.output_folder = ""
        self.links = []

    def update_progress_bar(self, stream, chunk, bytes_remaining):
        # Calculate the percentage of the video that has been downloaded
        percent = (100 * ((stream.filesize - bytes_remaining) / stream.filesize))
        # Update the progress bar
        self.progress_var.set(percent)
        self.master.update_idletasks()

    def add_link(self):
        # Add the link to the list box and clear the link entry text box
        link = self.link_text.get()
        if link:
            self.links.append(link)
            self.listbox.insert(tk.END, link)
            self.link_text.set("")

    def choose_folder(self):
        # Open a folder dialog and set the output folder path
        self.output_folder = filedialog.askdirectory()
        self.folder_path.set(self.output_folder)

    # Adding a button to load data for list box from select a file in dialog box.
    def load_data(self):
        # Open a file dialog and set the output folder path
        self.output_folder = filedialog.askopenfilename()
        # self.folder_path.set(self.output_folder)
        # Read the file and add the links to the list box and links list
        with open(self.output_folder, 'r') as f:
            for line in f:
                link = line.strip()
                self.links.append(link)
                self.listbox.insert(tk.END, link)

    def start_download(self):
        # Loop through the links and start downloading the videos
        for link in self.links:
            try:
                yt = YouTube(link, on_progress_callback=self.update_progress_bar)
                stream = yt.streams.get_highest_resolution()
                if self.filename_var.get():
                    video_title = stream.title.replace('\\', '').replace('/', '').replace(':', '').replace(
                        '*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
                    filename = video_title + ".mp4"
                else:
                    filename = str(int(yt.publish_date.timestamp())) + ".mp4"
                filepath = os.path.join(self.output_folder, filename)
                # yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(filepath)
                stream.download(output_path=self.output_folder,
                                filename=filename, skip_existing=self.check_var.get())
                # Download video
                if self.subtitle_checkbox_var.get() :
                    self.download_subtitles(link, os.path.join(self.output_folder, filename + ".srt"))
                

            except Exception as e:
                print(f"Error downloading {link}: {e}")
                tk.messagebox.showerror("Error", str(e))
                continue

        # Clear the list box and reset the links and output folder variables
        self.show_success_message("Finished all files")
        self.listbox.delete
        self.links.clear()
        self.master.update_idletasks()


    def delete_link(self):
        # Get the selected item from the list box
        selected_item = self.listbox.curselection()
        # Delete the selected item from the list box
        self.listbox.delete(selected_item)
        # Delete the selected item from the links list
        del self.links[selected_item[0]]

    def download_subtitles(self, url, filename):
        try:
            # Get the transcript for the video
            transcript = YouTubeTranscriptApi.get_transcript(self.cut_Youtube_url(url))

            # Build the SRT string
            srt = ''
            for i, line in enumerate(transcript):
                start = line['start']
                end = line['start'] + line['duration']
                text = line['text']
                srt += f"{i+1}\n{self.convert_to_srt_timestamp(start)} --> {self.convert_to_srt_timestamp(end)}\n{text}\n\n"

            # Save the SRT file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(srt)

            print(f"Subtitles downloaded and saved as '{filename}'.")
        except Exception as e:
            print(f"Error downloading subtitles: {str(e)}")

    def convert_to_srt_timestamp(self, seconds):
        h = int(seconds / 3600)
        m = int(seconds / 60 % 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    def cut_Youtube_url(self, url):
        match = re.search(r'(?<=\?v=)[\w-]+', url)
        if match:
            video_id = match.group(0)
            print(video_id)  # Output: -GwBNwZOPUs
            return video_id
        else:
            print('No match found')
            return ""

    # Create a function to display the success message
    def show_success_message(self, msg : str):
        tk.messagebox.showinfo("Success", msg)
