import demucs.api


def separate_voice(audio_file_path):
    separator = demucs.api.Separator()

    origin, separated = separator.separate_audio_file(audio_file_path)

    for stem, source in separated.items():
        # drums, bass, other, vocals
        print(f"Saving {stem}")
        demucs.api.save_audio(source, f"stems/{stem}.wav", samplerate=separator.samplerate)
