# DeidAudioConsultation

This project provides tools for detecting and masking private information in audio files. It offers two main functionalities:

1. Web Interface for Audio Masking
   - Upload audio files
   - Automatically detect private information
   - Apply audio masking to protect privacy
   - Download the masked audio file

2. CLI Tool for Privacy Information Detection
   - Process audio files to detect private information
   - Export results in Label Studio JSON format for further analysis or annotation


## ENV

### venv 
```
python -m venv .venv
.\.venv\Scripts\activate
```
linux: `source testenv/bin/activate`

#### install requirements
```
pip install -r requirements.txt
```

## Usage

### Web
How to run the web
```
streamlit run .\web.py
```

### CLI

Run the script from the command line with the following syntax:

```
python audio_deid_cli.py <input> <output> [--prefix_path PREFIX_PATH]
```

Arguments:
- `input`: Input file or directory containing .mp3 files
- `output`: Output directory for saving results
- `--prefix_path`: (Optional) Prefix file path for path_info

## Example

Process all .mp3 files in a directory:
```
python audio_deid_cli.py ./data ./output_DIR
```

Use a prefix for path info in json:
```
python audio_deid_cli.py ./data ./output_DIR --prefix_path "/data/upload/6/"
```

## Notes

- The script processes .mp3 files only.
- If the input is a directory, it will recursively search for all .mp3 files within it.
- The output JSON files will have the same name as the input audio files, with the .json extension.


## install log

```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install transformers peft datasets 
pip install git+https://github.com/m-bain/whisperx.git
pip install streamlit pydub

linux: apt-get install ffmpeg

pip freeze > requirements.txt
```






## demo web img
![螢幕擷取畫面 2024-05-25 215646](https://github.com/ISLAB-rui/deidaudioconsultation/assets/56379887/b7cc08a3-ad3a-4de3-b580-963460596ae2)

![螢幕擷取畫面 2024-05-25 215532](https://github.com/ISLAB-rui/deidaudioconsultation/assets/56379887/b1ecbd5d-cd9f-4102-a71d-4589940b1b99)







