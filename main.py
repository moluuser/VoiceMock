import shutil
from asr import execute_asr
from separator import separate_voice
from slicer import slice_voice

voice_file_path = "song.mp3"
output_folder = "output"

if __name__ == '__main__':
    # Clean
    try:
        shutil.rmtree(output_folder)
    except:
        pass

    # Prepare
    separate_voice(voice_file_path, output_folder)
    slice_voice(f"{output_folder}/stems/vocals.wav", output_folder)
    execute_asr(f"{output_folder}/slices", output_folder, "zh")

    # Train

    # Inference
