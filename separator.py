import os

import demucs.api


def separate_voice(audio_file_path, output_folder="output"):
    print(f"Separating voice from {audio_file_path}")
    separator = demucs.api.Separator()

    origin, separated = separator.separate_audio_file(audio_file_path)

    os.makedirs(f"{output_folder}/stems", exist_ok=True)
    for stem, source in separated.items():
        # drums, bass, other, vocals
        print(f"Saving {stem}")
        demucs.api.save_audio(source, f"{output_folder}/stems/{stem}.wav", samplerate=separator.samplerate)
