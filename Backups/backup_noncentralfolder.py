import os
import sys
import tkinter as tk
from tkinter import filedialog, Listbox, END, ACTIVE, NW, ttk
from pygame import mixer
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from PIL import Image, ImageTk, ImageDraw
from io import BytesIO

def load_asset(path):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    assets = os.path.join(base, "assets")
    return os.path.join(assets, path)


window = tk.Tk()
window.geometry("960x540")
window.configure(bg="#000000")
window.title("Ozan's Music Player")
mixer.init()
is_paused = False
song_index = 0
volume = 0.5
length = 0
current_progress = 0


canvas = tk.Canvas(
    window,
    bg="#23e340",
    width=960,
    height=540,
    bd=0,
    borderwidth=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

# background
canvas.create_rectangle(0, 0, 960, 540, fill='#486664', outline="")

bg_image = ImageTk.PhotoImage(Image.open("../assets/gradient.png"))

canvas.create_image(0, 0, anchor=NW, image=bg_image)

# lower box with all buttons
canvas.create_rectangle(18, 411, 941, 520, fill='', width="1.0", outline='')

lower_bar_image = ImageTk.PhotoImage(Image.open("../assets/lower_bar.png"))

canvas.create_image(20, 411, anchor=NW, image=lower_bar_image)

# cover place
canvas.create_rectangle(286, 42, 657, 375, fill='#7ea8a5', outline="#ffffff", width="1.0")



# album art
album_art_label = tk.Label(window)
album_art_label.config(bg='#486664', borderwidth=0)
album_art_label.place(x=286, y=42, width=372, height=334)


#play bar
progress = ttk.Progressbar(window, orient="horizontal", length=350, mode="determinate", style='success.Striped.Horizontal.TProgressbar')
progress.configure(maximum=length)
progress.place(x=306, y=490, width=348, height=16)






# play button

def playMusic():
    global is_paused
    global percent_p_second
    if is_paused:
        mixer.music.unpause()
        is_paused = False
        progress.start(1000)
    else:
        music_name = playlist.get(ACTIVE)
        print(music_name[0:-4])
        path = os.path.join(os.getcwd(), music_name)
        get_album_cover(path)
        mixer.music.load(playlist.get(ACTIVE))
        progress["value"] = 0
        mixer.music.play()
        progress.start(1000)
        is_paused = False


def get_album_cover(music_path):
    global length
    try:
        audio = MP3(music_path, ID3=ID3)
        album_art = None
        length = audio.info.length
        progress.configure(maximum=length)
        for tag in audio.tags.values():
            if isinstance(tag, APIC):
                album_art = tag.data
                break
        if album_art:
            image = Image.open(BytesIO(album_art))
            image = image.resize((371, 333), Image.Resampling.LANCZOS)
            album_art_tk = ImageTk.PhotoImage(image)
            album_art_label.config(image=album_art_tk)
            album_art_label.image = album_art_tk
        else:
            album_art_label.config(image="", text="No album art found", bg="#7ea8a5")
    except Exception as e:
        print(f"Error extracting album art: {e}")
        album_art_label.config(image="", text="Error loading album art", bg="#7ea8a5")


"""Rounded Corners Function"""


def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


button_1_image = tk.PhotoImage(file=load_asset("1.png"))

button_1 = tk.Button(
    image=button_1_image,
    relief="flat",
    bg='#476C74',
    borderwidth=0,
    highlightthickness=0,
    command=playMusic)

button_1.place(x=418, y=423, width=60, height=60)


# pause button


def stopMusic():
    global is_paused
    global current_progress
    mixer.music.pause()
    current_progress = progress["value"]
    progress.stop()
    progress['value'] = current_progress
    is_paused = True


button_2_image = tk.PhotoImage(file=load_asset("2.png"))

button_2 = tk.Button(
    image=button_2_image,
    relief="flat",
    bg='#476C74',
    borderwidth=0,
    highlightthickness=0,
    command=stopMusic
)

button_2.place(x=482, y=423, width=60, height=60)

# upload button
button_3_image = tk.PhotoImage(file=load_asset("3.png"))

playlist = Listbox(window, width=20, height=14, font=("Arial,bold ", 15))
playlist.place(x=20, y=43)


def addMusic():
    print('hello')
    path = filedialog.askdirectory()
    if path:
        os.chdir(path)
        songs = os.listdir(path)

        for song in songs:
            print(song)
            if song.endswith(".mp3"):
                playlist.insert(END, song)


button_3 = tk.Button(
    image=button_3_image,
    relief="flat",
    bg='#476C74',
    borderwidth=0,
    highlightthickness=0,
    command=addMusic)

button_3.place(x=42, y=428, width=239, height=78)


# skip forward

def skipForward():
    global song_index
    song_index += 1
    if song_index >= playlist.size():  # Loop back to the first song if at the end
        song_index = 0
    next_song = playlist.get(song_index)
    path = os.path.join(os.getcwd(), next_song)
    get_album_cover(path)
    mixer.music.load(next_song)
    progress["value"] = 0
    mixer.music.play()
    playlist.selection_clear(0, END)
    playlist.activate(song_index)
    playlist.selection_set(song_index)


button_5_image = tk.PhotoImage(file=load_asset("5.png"))

button_5 = tk.Button(
    image=button_5_image,
    relief="flat",
    borderwidth=0,
    bg='#476C74',
    highlightthickness=0,
    command=skipForward
)

button_5.place(x=547, y=429, width=107, height=49)


# skip back

def skipBack():
    global song_index
    song_index -= 1
    if song_index < 0:
        song_index = 0
    next_song = playlist.get(song_index)
    path = os.path.join(os.getcwd(), next_song)
    get_album_cover(path)
    mixer.music.load(next_song)
    mixer.music.play()
    progress["value"] = 0
    playlist.selection_clear(0, END)
    playlist.activate(song_index)
    playlist.selection_set(song_index)


button_6_image = tk.PhotoImage(file=load_asset("6.png"))

button_6 = tk.Button(
    image=button_6_image,
    relief="flat",
    bg='#476C74',
    borderwidth=0,
    highlightthickness=0,
    command=skipBack
)

button_6.place(x=306, y=429, width=107, height=49)


# volume up


def volume_up():
    global volume
    volume += 0.1
    if volume > 1:
        volume = 1
    mixer.music.set_volume(volume)


button_4_image = tk.PhotoImage(file=load_asset("4.png"))

button_4 = tk.Button(
    image=button_4_image,
    relief="flat",
    bg='#476C74',
    borderwidth=0,
    highlightthickness=0,
    command=volume_up
)

button_4.place(x=679, y=429, width=239, height=37)


# volume down

def volume_down():
    global volume
    volume -= 0.1
    if volume < 0:
        volume = 0
    mixer.music.set_volume(volume)


button_7_image = tk.PhotoImage(file=load_asset("7.png"))

button_7 = tk.Button(
    image=button_7_image,
    relief="flat",
    bg='#476C74',
    borderwidth=0,
    highlightthickness=0,
    command=volume_down
)

button_7.place(x=679, y=474, width=239, height=37)

window.resizable(False, False)
window.mainloop()
