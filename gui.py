# importing tkinter for gui
import tkinter as tk
from tkinter.ttk import Progressbar
from downloader import MediaDownloader, PlaylistDownloader

# threading 



class GUI():
    def __init__(self):
        self.is_playlist = False
        self.is_audio = False
        # creating window
        self.window = tk.Tk()
        # getting screen width and height of display
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        # setting tkinter window size
        self.window.geometry("%dx%d" % (self.width // 4, self.height // 2.5))
        self.window.title('YTDownloader')
        self.label = tk.Label(
            self.window,
            text="Paste a YouTube video link or a Playlist link to download!",
            wraplength=(self.width // 4) - 20
        )
        # textbox for link
        self.textbox = tk.Text(
            self.window,
            height=5,
            width=50
        )
        # textbox for results
        self.textbox2 = tk.Text(
            self.window,
            height=3,
            width=50,
            state="disabled"
        )
        # label for results
        self.label1 = tk.Label(
            self.window,
            text="Results",
            wraplength=(self.width // 4) - 20
        )

        self.var1 = tk.IntVar() # playlist
        self.var2 = tk.IntVar() # audio

        self.playlist_checkbox = tk.Checkbutton(
            self.window,
            text='Playlist',
            variable=self.var1,
            onvalue=1,
            offvalue=0,
            command=self.update_is_playlist
        )

        self.audio_checkbox = tk.Checkbutton(
            self.window,
            text='Audio',
            variable=self.var2,
            onvalue=1,
            offvalue=0,
            command=self.update_is_audio
        )

        self.video_info_label = tk.Label(
            self.window,
            text="",
            wraplength=(self.width // 4) - 20
        )
        self.progress = Progressbar(
            self.window,
            orient=tk.HORIZONTAL,
            length=100,
            mode='determinate'
        )
        self.button = tk.Button(
            self.window,
            text='Download',
            width=25,
            command=self.download
        )
        self.completion_label = tk.Label(
            self.window,
            text="",
            wraplength=(self.width // 4) - 20
        )
        self.build()

    def build(self):
        self.label.pack()
        self.textbox.pack()
        self.label1.pack()
        self.textbox2.pack()
        self.playlist_checkbox.pack()
        self.audio_checkbox.pack()
        self.progress.pack()
        self.video_info_label.pack()
        self.button.pack()
        self.completion_label.pack()
        self.window.mainloop()

    def on_progress_callback(self, stream, data_chunk, rem_bytes):
        # print(stream.filesize, rem_bytes)
        percent_remaining = int(
            ((stream.filesize - rem_bytes) / stream.filesize) * 100)
        print("percent remaining", percent_remaining)
        self.progress['value'] = percent_remaining
        self.video_info_label['text'] = stream.title
        self.window.update()
        # self.window.update_idletasks()

    def on_complete_callback(self, stream, file_path):
        print("file_path", file_path)
        self.completion_label['text'] = f"Downloaded at location: {file_path}"
        self.window.update_idletasks()

    def download(self):
        self.progress['value'] = 0 # reset progress bar
        self.textbox2.delete('1.0', 'end')
        link = self.textbox.get("1.0", 'end-1c')
        try:
            if self.is_playlist:
                if self.is_audio:
                    downloader = PlaylistDownloader(
                        link=link,
                        on_progress_callback=self.on_progress_callback,
                        on_complete_callback=self.on_complete_callback,
                        type = 0
                    )
                else:
                    downloader = PlaylistDownloader(
                        link=link,
                        on_progress_callback=self.on_progress_callback,
                        on_complete_callback=self.on_complete_callback,
                        type = 1
                    )
            else:
                if self.is_audio:
                    downloader = MediaDownloader(
                        link=link,
                        on_progress_callback=self.on_progress_callback,
                        on_complete_callback=self.on_complete_callback,
                    ).audio
                else:
                    downloader = MediaDownloader(
                        link=link,
                        on_progress_callback=self.on_progress_callback,
                        on_complete_callback=self.on_complete_callback,
                    ).video
            downloader.download()
            self.update_result("finished")

        except Exception as e:
            self.update_result(str(e))
            print(str(e))

    def update_is_playlist(self):
        val = self.var1.get()
        if val == 0:
            self.is_playlist = False
        else:
            self.is_playlist = True

    def update_is_audio(self):
        val = self.var2.get()
        if val == 0:
            self.is_audio = False
        else:
            self.is_audio = True

    def update_result(self, message):
        self.textbox2.config(state="normal")
        self.textbox2.insert('end', message)
        self.textbox2.config(state="disabled")

GUI()
