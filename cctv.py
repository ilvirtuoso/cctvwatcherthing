import tkinter as tk
from tkinter import ttk
import vlc

class MultiStreamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi VLC Stream Viewer")
        self.root.geometry("800x600")  # Adjusted window size to match the grid layout

        # Define stream links
        self.stream_links = {
            "stream1": "http://kamera.wseip.edu.pl/mjpg/video.mjpg",
            "stream2": "http://85.196.146.82:3337/mjpg/video.mjpg",
            "stream3": "http://109.247.15.178:6001/mjpg/video.mjpg",
            "stream4": "http://77.110.203.114:82/mjpg/video.mjpg",
            "stream5": "http://213.236.250.78/mjpg/video.mjpg",
            "stream6": "http://kamera.mikulov.cz:8888/mjpg/video.mjpg",
            "stream7": "http://webcam.schwaebischhall.de/mjpg/video.mjpg",
            "stream8": "http://myrafjell.sodvin.no/mjpg/video.mjpg",
            "stream9": "http://e1480d3b88f7.sn.mynetname.net:90/mjpg/video.mjpg",
            "stream10": "http://67.53.46.161:65123/mjpg/video.mjpg",
            "stream11": "http://webcam.thealgonquin.com:8080/mjpg/video.mjpg",
            "stream12": "http://63.142.183.154:6103/mjpg/video.mjpg",
            "stream13": "http://webcam.moss-havn.no:55111/mjpg/video.mjpg",
            "stream14": "http://109.164.255.227:15000/mjpg/video.mjpg",
            "stream15": "http://92.247.13.209/mjpg/video.mjpg",
            "stream16": "http://mfc.istmein.de:8033/mjpg/video.mjpg", 
            "stream17": "http://220.233.144.165:8888/mjpg/video.mjpg?timestamp=1234567890123",
            "stream18": "http://nauticaantonio.telecablesantapola.es:8088/mjpg/video.mjpg",
            "stream19": "http://brandts.mine.nu:84/mjpg/video.mjpg",
            "stream20": "https://webcam1.lpl.org/mjpg/video.mjpg",
            "stream21": "http://ca1-camera.desco.com:8082/mjpg/video.mjpg",
            "stream22": "http://299jkb1.257.cz/mjpg/video.mjpg",
            "stream23": "http://129.2.146.15/mjpg/video.mjpg",
        }

        # Create a single VLC instance with hardware acceleration enabled for both NVIDIA and AMD
        # '--avcodec-hw=any' lets VLC auto-detect and use available GPU hardware (CUDA/VDPAU for NVIDIA, VAAPI for AMD/Intel)
        # '--no-audio' disables audio processing since streams are video-only
        # '--network-caching=300' adds some buffering to smooth network streams
        self.instance = vlc.Instance('--avcodec-hw=any', '--no-audio', '--network-caching=300')

        # Create a frame for the video streams
        self.video_frame = tk.Frame(self.root)
        self.video_frame.pack(fill=tk.BOTH, expand=True)

        # Initialize players and video panels
        self.players = {}
        self.video_panels = {}

        # Create video panels for each stream in a grid layout
        total_streams = len(self.stream_links)
        rows = int(total_streams ** 0.5)  # Calculate rows based on square root of total streams
        cols = (total_streams + rows - 1) // rows  # Calculate columns to fit all streams

        for index, (stream_name, stream_url) in enumerate(self.stream_links.items()):
            row = index // cols
            col = index % cols
            self.add_stream(stream_name, stream_url, row, col)

    def add_stream(self, stream_name, stream_url, row, col):
        # Create a VLC player from the shared instance
        player = self.instance.media_player_new()

        # Create a video panel using tk.Label
        video_panel = tk.Label(self.video_frame, bg="black")
        video_panel.grid(row=row, column=col, sticky="nsew")  # Ensure full space utilization

        # Set the media for the player
        media = self.instance.media_new(stream_url)
        player.set_media(media)

        # Assign the video output to the panel
        player.set_hwnd(video_panel.winfo_id())

        # Store the player and panel
        self.players[stream_name] = player
        self.video_panels[stream_name] = video_panel

        # Play the stream
        player.play()

        # Configure grid weights for resizing
        self.video_frame.grid_rowconfigure(row, weight=1)
        self.video_frame.grid_columnconfigure(col, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiStreamApp(root)
    root.mainloop()