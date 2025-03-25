import customtkinter as ctk
import yt_dlp
import threading
import os
import subprocess

# Initialize the app
app = ctk.CTk()
app.title("YouTube Video Downloader")
app.geometry("550x450")
ctk.set_appearance_mode("dark")  # Dark Mode
ctk.set_default_color_theme("blue")

# Function to download video
def download_video():
    url = url_entry.get()
    resolution = resolution_var.get()

    if not url:
        status_label.configure(text="❌ Please enter a URL!", text_color="red")
        return

    ydl_opts = {
        'format': f'bestvideo[height<={resolution}]+bestaudio/best',
        'outtmpl': 'Downloads/%(title)s.%(ext)s',
        'progress_hooks': [update_progress]
    }

    def run_download():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                status_label.configure(text="Downloading...", text_color="orange")
                info_dict = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info_dict)
                status_label.configure(text="✅ Download Complete!", text_color="green")
                progress_bar.set(1.0)
                
                # Open the video after download
                subprocess.run(["open", filename])  # macOS command to open files
        except Exception as e:
            status_label.configure(text=f"Error: {e}", text_color="red")

    threading.Thread(target=run_download, daemon=True).start()

# Function to update progress
def update_progress(d):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 1)
        progress = downloaded / total
        progress_bar.set(progress)

# Function to watch the last downloaded video
def watch_video():
    try:
        files = os.listdir("Downloads")
        if not files:
            status_label.configure(text="❌ No videos found!", text_color="red")
            return

        latest_file = max(files, key=lambda f: os.path.getctime(os.path.join("Downloads", f)))
        file_path = os.path.join("Downloads", latest_file)

        # Open the last downloaded file
        subprocess.run(["open", file_path])  # macOS command
    except Exception as e:
        status_label.configure(text=f"Error: {e}", text_color="red")

# UI Elements
ctk.CTkLabel(app, text="YouTube Video URL:", font=("Arial", 14)).pack(pady=10)
url_entry = ctk.CTkEntry(app, width=400)
url_entry.pack(pady=5)

# Resolution selection
ctk.CTkLabel(app, text="Select Resolution:", font=("Arial", 14)).pack(pady=10)
resolution_var = ctk.StringVar(value="1080")
resolution_dropdown = ctk.CTkComboBox(app, values=["144", "240", "360", "480", "720", "1080"], variable=resolution_var)
resolution_dropdown.pack(pady=5)

# Download button
download_button = ctk.CTkButton(app, text="Download", command=download_video)
download_button.pack(pady=20)

# Progress bar
progress_bar = ctk.CTkProgressBar(app, width=400)
progress_bar.set(0)
progress_bar.pack(pady=10)

# Status label
status_label = ctk.CTkLabel(app, text="")
status_label.pack()

# Watch Video button
watch_button = ctk.CTkButton(app, text="Watch Video", command=watch_video)
watch_button.pack(pady=10)

# Run the app
app.mainloop()
