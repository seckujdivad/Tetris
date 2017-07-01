def music_player(): #added by jack, work in progress, only plays one song for now
##    winsound.PlaySound("assets/sounds/level 1.WAV", winsound.SND_FILENAME | winsound.SND_ASYNC)
##    if music_number > 180:
    winsound.PlaySound("assets/sounds/level 5.WAV", winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
##    elif music_number > 120:
##        winsound.PlaySound("assets/sounds/level 3.WAV", winsound.SND_FILENAME | winsound.SND_ASYNC)
##    elif music_number > 60:
##        winsound.PlaySound("assets/sounds/level 2.WAV", winsound.SND_FILENAME | winsound.SND_ASYNC)