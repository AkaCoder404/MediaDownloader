import os
from pytube import YouTube, Playlist
from utils import create_dir, get_output_number

class MediaDownloader():
    def __init__(self, link, on_progress_callback, on_complete_callback, download_location=None):
        self.link = link
        self.on_progress_callback = on_progress_callback
        self.on_complete_callback = on_complete_callback

        self.audio = self.AudioDownloader(link, on_progress_callback, on_complete_callback, download_location)
        self.video = self.VideoDownloader(link, on_progress_callback, on_complete_callback, download_location)

      
    class AudioDownloader:
        def __init__(self, link, on_progress_callback, on_complete_callback, download_location):
            self.link = link
            self.on_progress_callback = on_progress_callback
            self.on_complete_callback = on_complete_callback
            self.audio = YouTube(self.link, on_progress_callback=self.on_progress_callback,
                                 on_complete_callback=self.on_complete_callback)

            if download_location:
                self.download_location = download_location
            else:
                self.download_location = os.getcwd()

        def get_info(self, audio=None):
            if audio is None:
                # To print title
                print("Title :", self.audio.title)
                # To get number of views
                print("Views :", self.audio.views)
                # To get the length of audio
                print("Duration :", self.audio.length)
                # To get description
                # print("Description :", self.audio.description)
                # To get ratings
                print("Ratings :", self.audio.rating)
                return self.audio.title, self.audio.views, self.audio.length, self.audio.description, self.audio.rating
            else:
                # To print title
                print("Title :", audio.title)
                # To get number of views
                print("Views :", audio.views)
                # To get the length of audio
                print("Duration :", audio.length)
                # To get description
                # print("Description :", audio.description)
                # To get ratings
                print("Ratings :", audio.rating)
                return audio.title, audio.views, audio.length, audio.description, audio.rating
                
        def download(self, link=None, outnum=None):
            if link is None:
                print("link is none")
                self.get_info()
                stream = self.audio.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
                create_dir(f"{self.download_location}/audio/")
                stream.download(output_path=f"{self.download_location}/audio/")
            else:
                print("there is link")
                audio = YouTube(link, on_progress_callback=self.on_progress_callback,
                                    on_complete_callback=self.on_complete_callback)
                self.get_info(audio=audio)
                stream = self.audio.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
                
                stream.download(
                        output_path=f"{self.download_location}/playlists/playlist-{outnum}/")
                return audio
                      
    class VideoDownloader:
        def __init__(self, link, on_progress_callback, on_complete_callback, download_location):
            self.link = link
            self.on_progress_callback = on_progress_callback
            self.on_complete_callback = on_complete_callback
            self.video = YouTube(self.link, on_progress_callback=self.on_progress_callback,
                                 on_complete_callback=self.on_complete_callback)
            # self.download_location = download_location

            if download_location:
                self.download_location = download_location
            else:
                self.download_location = os.getcwd()

        def get_info(self, video=None):
            if video is None:
                # To print title
                print("Title :", self.video.title)
                # To get number of views
                print("Views :", self.video.views)
                # To get the length of video
                print("Duration :", self.video.length)
                # To get description
                # print("Description :", self.video.description)
                # To get ratings
                print("Ratings :", self.video.rating)
                return self.video.title, self.video.views, self.video.length, self.video.description, self.video.rating
            else:
                # To print title
                print("Title :", video.title)
                # To get number of views
                print("Views :", video.views)
                # To get the length of video
                print("Duration :", video.length)
                # To get description
                # print("Description :", video.description)
                # To get ratings
                print("Ratings :", video.rating)
                return video.title, video.views, video.length, video.description, video.rating

        def download(self, link=None, outnum=None):
            if link is None:
                print("link is none")
                self.get_info()
                stream = self.video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                create_dir(f"{self.download_location}/videos/")
                stream.download(output_path=f"{self.download_location}/videos/")
            else:
                print("there is link")
                video = YouTube(link, on_progress_callback=self.on_progress_callback,
                                on_complete_callback=self.on_complete_callback)
                self.get_info(video=video)
                # stream options
                # stream = video.streams.get_lowest_resolution()
                stream = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                stream.download(
                    output_path=f"{self.download_location}/playlists/playlist-{outnum}/")

class PlaylistDownloader(MediaDownloader):
    def __init__(self, link, on_progress_callback, on_complete_callback, download_location=None, type=0):
        self.link = link
        self.playlist = Playlist(self.link)
        self.on_progress_callback = on_progress_callback
        self.on_complete_callback = on_complete_callback
        self.type = type

        if download_location:
            self.download_location = download_location
        else:
            self.download_location = os.getcwd()

    def get_all_playlist_links(self):
        print("get_all_playlist_links", self.playlist.video_urls)
        return self.playlist.video_urls

    def get_num_videos(self):
        print("get_num_videos", len(self.playlist.videos))
        return len(self.playlist.videos)

    def download(self):
        links = self.playlist.video_urls
        create_dir(f"{self.download_location}/playlists/")
        outnum = get_output_number(f"{self.download_location}/playlists/") + 1

        for link in links:
            if self.type == 0:
               MediaDownloader(
                    link=link,
                    on_progress_callback=self.on_progress_callback,
                    on_complete_callback=self.on_complete_callback,
                ).audio.download(link, outnum)
            else:
                MediaDownloader(
                    link=link,
                    on_progress_callback=self.on_progress_callback,
                    on_complete_callback=self.on_complete_callback,
                ).video.download(link, outnum)
