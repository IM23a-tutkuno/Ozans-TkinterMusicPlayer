import os
directory_path = os.path.join(os.environ['USERPROFILE'],'Desktop','Script')
print(directory_path)


music_directory = os.path.join(os.getenv("ProgramData"), "OzansMusicPlayer", "Music")

# Ensure the music directory exists
if not os.path.exists(music_directory):
    os.makedirs(music_directory)