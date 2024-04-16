from separator import separate_voice
from slicer import slice_voice

if __name__ == '__main__':
    separate_voice("song.mp3")
    slice_voice("stems/vocals.wav")
