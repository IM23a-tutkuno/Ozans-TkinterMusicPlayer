# Ozans-TkinterMusicPlayer
This is a  simple MusicPlayer built with Python and Tkinter. The design was created by me with Figma and converted using TkForge.
You can add your own .mp3 files and listen to them. 
All basic music-player features  are available like:<br>
- skip forward/back <br>
- volume control<br>
- play/pause
- .mp3 file playback
- playbar

## Images
![image](https://github.com/user-attachments/assets/ac770eb4-7081-4466-af6b-3df435ec3653)

 ## ❗IMPORTANT❗
<strong>The python script creates two folders in ProgramData: OzansMusicPlayer/AudioFiles</strong><br>
When the user uploads mp3 files from his machine they get copied into that directory. That folder also get scanned for mp3 files everytime the script starts.


## Installation
```bash
pip install -r /path/to/requirements.txt
```

## Module Usage
- pygame: is used for playing audio with pygame mixer music<br>
- mutagen: used for scanning the .mp3 file for the cover<br>
- pillow: used for implementing images into the code<br>
  
## Contributing
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## LICENSE
[LICENSE](/LICENSE)
