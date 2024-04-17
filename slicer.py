import os
import struct
import librosa
import numpy as np
import webrtcvad
import soundfile as sf


def slice_voice(voice_file_path, max_voice_duration=10, min_voice_duration=1):
    slices_dir = "slices"
    y, sr = librosa.load(voice_file_path, sr=16000)
    y = librosa.to_mono(y)

    if y.dtype.kind == 'f':
        # convert to int16
        y = np.array([int(s * 32768) for s in y])
        # bound
        y[y > 32767] = 32767
        y[y < -32768] = -32768

    raw_samples = struct.pack("%dh" % len(y), *y)

    vad = webrtcvad.Vad()
    vad.set_mode(2)  # 设置VAD的敏感度级别，0-3之间的整数，级别越高，检测到的人声活动越多

    window_duration = 0.03  # duration in seconds
    samples_per_window = int(window_duration * sr + 0.5)
    bytes_per_sample = 2  # for int16

    segments = []
    for i, start in enumerate(np.arange(0, len(y), samples_per_window)):
        stop = min(start + samples_per_window, len(y))
        loc_raw_sample = raw_samples[start * bytes_per_sample: stop * bytes_per_sample]
        try:
            is_speech = vad.is_speech(loc_raw_sample, sample_rate=sr)
            segments.append((start, stop, is_speech))
        except Exception as e:
            print(f"Failed for step {i}, reason: {e}")

    active_segments = []
    current_segment = None
    for start, end, is_speech in segments:
        if is_speech:
            if current_segment is None:
                current_segment = [start, end]
            else:
                current_segment[1] = end
        elif current_segment is not None:
            active_segments.append(tuple(current_segment))
            current_segment = None

    # 如果音频末尾有人声活动，需要将最后一个时间段添加到列表中
    if current_segment is not None:
        active_segments.append(tuple(current_segment))

    # 将每个片段长度限制为最大值
    max_samples = int(max_voice_duration * sr)
    final_segments = []
    for segment in active_segments:
        start, end = segment
        duration = end - start
        if duration <= max_samples:
            final_segments.append(segment)
        else:
            num_sub_segments = int(np.ceil(duration / max_samples))
            sub_segment_size = duration // num_sub_segments
            for i in range(num_sub_segments):
                sub_start = start + i * sub_segment_size
                sub_end = min(sub_start + sub_segment_size, end)
                final_segments.append((sub_start, sub_end))

    # 保存活动部分为.wav文件
    os.makedirs(slices_dir, exist_ok=True)
    num = 0
    for i, segment in enumerate(final_segments):
        start, end = segment
        # Skip short segments
        if end - start < sr * min_voice_duration:
            continue
        num += 1
        segment_audio = y[start:end]
        segment_file = f"{slices_dir}/segment_{num}.wav"
        segment_audio = segment_audio.astype(np.int16)
        sf.write(segment_file, segment_audio, sr)
        print(f"Saved segment {num} as {segment_file}")
