import argparse
from tqdm import tqdm
from pathlib import Path
import json
import os

from utils.pipeline import Deid_audio

from utils.json_converter import convert_to_label_studio


def main():
    parser = argparse.ArgumentParser(description="Process audio files to detect private information and export results in Label Studio JSON format.")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("output", help="Output directory for saving results")

    # prefix path 
    parser.add_argument("--prefix_path", help="Prefix file path for path_info", default="")

    args = parser.parse_args()

    input_path = args.input
    output_dir = args.output

    # check is exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input path {input_path} does not exist")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # check if input is file or directory
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input path {input_path} does not exist")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    if os.path.isfile(input_path):
        files = [input_path]
    else:
        files = []
        for root, _, filenames in os.walk(input_path):
            for filename in filenames:
                if filename.endswith(".mp3"):
                    files.append(os.path.join(root, filename))

    for file in tqdm(files, desc="Processing files"):
        deid = Deid_audio(file)
        deid.wisperx()
        deid.model('zhaorui-nb/aicup-pythia-160m')

        with open(deid.get_masked_json()) as f:
            mask_json = json.load(f)

        path_info = args.prefix_path + os.path.basename(file)
        save_path = os.path.join(output_dir, os.path.basename(file).replace(".mp3", ".json"))
        # get file name and extension
        convert_to_label_studio(path_info, mask_json, save_path=save_path)

        print(f"Processed {file} and saved result to {save_path}")


        # except Exception as e:
        #     print(f"Error processing {file}: {str(e)}")

if __name__ == "__main__":
    main()