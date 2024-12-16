import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from youtube_transcript_api import YouTubeTranscriptApi

# Function to fetch transcript
def fetch_transcript():
    video_url = url_entry.get()
    try:
        # Extract video ID
        if 'youtu.be' in video_url:
            video_id = video_url.split('/')[-1]
        elif 'youtube.com/watch?v=' in video_url:
            video_id = video_url.split('v=')[1].split('&')[0]
        else:
            raise ValueError("Invalid YouTube URL")

        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Process the transcript
        text_only_lines = [entry['text'] for entry in transcript]
        last_time = transcript[-1]['start']

        # Combine lines into a formatted transcript
        formatted_transcript = "\n".join(text_only_lines) + f"\n\n(Last Timestamp: {last_time}s)"

        # Display the transcript in the GUI
        transcript_text.delete("1.0", tk.END)
        transcript_text.insert(tk.END, formatted_transcript)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch transcript: {e}")

# Function to save the transcript
def save_transcript():
    content = transcript_text.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Warning", "No transcript to save.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        title="Save Transcript"
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

# Function to copy transcript to clipboard
def copy_transcript():
    content = transcript_text.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Warning", "No transcript to copy.")
        return

    root.clipboard_clear()
    root.clipboard_append(content)
    root.update()  # Keeps the clipboard updated

# Function to toggle between Light and Dark Modes
def toggle_dark_mode():
    global dark_mode
    if dark_mode:
        # Switch to Light Mode
        style.theme_use("default")
        root.configure(bg="white")
        frame.configure(bg="white")
        transcript_frame.configure(bg="white")
        button_frame.configure(bg="white")
        dark_mode_button.configure(text="Dark Mode")
        transcript_text.configure(bg="white", fg="black", insertbackground="black")
    else:
        # Switch to Dark Mode
        style.theme_use("clam")
        root.configure(bg="#2e2e2e")
        frame.configure(bg="#2e2e2e")
        transcript_frame.configure(bg="#2e2e2e")
        button_frame.configure(bg="#2e2e2e")
        dark_mode_button.configure(text="Light Mode")
        transcript_text.configure(bg="#3c3f41", fg="white", insertbackground="white")
    dark_mode = not dark_mode

# Initialize Dark Mode state
dark_mode = False

# Create the GUI window
root = tk.Tk()
root.title("YouTube Transcript Fetcher")

# Apply a style for consistent theme switching
style = ttk.Style()

# URL Input
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky="EW")
ttk.Label(frame, text="YouTube URL:").grid(row=0, column=0, sticky="W")
url_entry = ttk.Entry(frame, width=50)
url_entry.grid(row=0, column=1, sticky="EW")
ttk.Button(frame, text="Fetch Transcript", command=fetch_transcript).grid(row=0, column=2, sticky="E")
frame.columnconfigure(1, weight=1)

# Transcript Display
transcript_frame = ttk.Frame(root, padding="10")
transcript_frame.grid(row=1, column=0, sticky="NSEW")
ttk.Label(transcript_frame, text="Transcript:").grid(row=0, column=0, sticky="W")
transcript_text = tk.Text(transcript_frame, wrap="word", height=20, width=80)
transcript_text.grid(row=1, column=0, sticky="NSEW")
scrollbar = ttk.Scrollbar(transcript_frame, orient="vertical", command=transcript_text.yview)
scrollbar.grid(row=1, column=1, sticky="NS")
transcript_text["yscrollcommand"] = scrollbar.set

# Action Buttons
button_frame = ttk.Frame(root, padding="10")
button_frame.grid(row=2, column=0, sticky="EW")
ttk.Button(button_frame, text="Copy Transcript", command=copy_transcript).grid(row=0, column=0, padx=5)
ttk.Button(button_frame, text="Save Transcript", command=save_transcript).grid(row=0, column=1, padx=5)
dark_mode_button = ttk.Button(button_frame, text="Dark Mode", command=toggle_dark_mode)
dark_mode_button.grid(row=0, column=2, padx=5)

# Adjust layout
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Run the GUI event loop
root.mainloop()
