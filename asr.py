import os
import traceback
from tqdm import tqdm
from funasr import AutoModel

path_asr = "iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
path_vad = "iic/speech_fsmn_vad_zh-cn-16k-common-pytorch"
path_punc = "iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch"

model = AutoModel(
    model=path_asr,
    vad_model=path_vad,
    punc_model=path_punc,
)


def execute_asr(input_folder, output_folder, language):
    print(f"Executing ASR on {input_folder}")
    input_file_names = os.listdir(input_folder)
    input_file_names.sort()

    output = []
    output_file_name = os.path.basename(input_folder)

    for file_name in tqdm(input_file_names):
        try:
            file_path = os.path.join(input_folder, file_name)
            text = model.generate(input=file_path)[0]["text"]
            output.append(f"{file_path}|{output_file_name}|{language.upper()}|{text}")
        except:
            print(traceback.format_exc())

    output_folder = f"{output_folder}/asr"
    os.makedirs(output_folder, exist_ok=True)
    output_file_path = os.path.abspath(f'{output_folder}/{output_file_name}.list')

    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output))
        print(f"ASR output saved to {output_file_path}")
    return output_file_path
