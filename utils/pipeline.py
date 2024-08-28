from tqdm import tqdm
import subprocess
import json
from pydub import AudioSegment
import os
import sys

from .Deid_model import Deid_model
from .Audio_position import Audio_position

class Deid_audio:

    def __init__(self, input_file):
        self.input_file = input_file
        # self.file_name = self.input_file.split('/')[-1].replace('.mp3', '')
        self.file_name = os.path.basename(self.input_file).replace('.mp3', '')
        self.asr = None #json
        self.mask_time = None #list [[start, end], [start, end]...]
        self.model_save_path = f'./.output/{self.file_name}_mask.json'
        self.masked_file = f'./.output/{self.file_name}_masked.mp3'


    def wisperx(self):
        # args = ['whisperx', '--language', 'en', '--output_dir', './.output', self.input_file]
        # process = subprocess.Popen(args, stdout=subprocess.PIPE, text=True)
        # while True:
        #     output = process.stdout.readline()
        #     if output == '' and process.poll() is not None:
        #         break
        #     if output:
        #         print(output.strip())

        command = f'whisperx --language en --output_dir ./.output {self.input_file}'
        os.system(command)


        # file_name = self.input_file.split('/')[-1]
        # with open(f"./.output/{file_name.replace('.mp3', '.json')}") as f:
        with open(f"./.output/{self.file_name}.json") as f:
            self.asr = json.load(f)
        return self.asr

    def model(self, model_path):
        apos = Audio_position(self.asr)
        # model = Deid_model('model/pythia/model_v5_EP8_2023_1130_1450_10')
        model = Deid_model(model_path)
        for i in tqdm(range(len(apos))):
            labels = model(apos.get_sentence(i))[0]
            for label in labels: # [label, content]
                m_index = apos.search_continuous_word_index(i , label[1])
                apos.set_mask(i, m_index, mask_type=label[0])   
        apos.generate_mask()
        mask = apos.get_mask()

        with open(self.model_save_path, 'w') as f:
            j = json.dumps(mask, indent=4)
            f.write(j)
            print(j)
        self.mask_time = apos.get_mask_time()

    def mask_audio(self):
        audio = AudioSegment.from_file(self.input_file)
        for start, end in self.mask_time:
            start = start * 1000
            end = end * 1000
            sl = AudioSegment.silent(duration=end - start)
            audio = audio[:start] + sl + audio[end:]
        audio.export(self.masked_file, format="mp3")

    def get_masked_file_path(self):
        return self.masked_file
    def get_mask_time(self):  
        return self.mask_time
    def get_masked_json(self):
        return self.model_save_path
    def get_model_save_path(self):
        return self.model_save_path


    # def pipeline(input_file):
    #     # if file is exit and is mp3
    #     if not os.path.exists(input_file):
    #         print("File not found")
    #         return None
    #     if not input_file.endswith('.mp3'):
    #         print("File is not mp3")
    #         return None
        
    #     file_name = input_file.split('/')[-1].replace('.mp3', '')
    #     masked_file = f'./.output/{file_name}_masked.mp3'

    #     asr = wisperx(input_file)
    #     mask_time = model(asr , save_path=f'./.output/{file_name}.json')
    #     mask_audio(input_file, mask_time, output_file=masked_file)

    #     if not os.path.exists(masked_file):
    #         print("Error in masking audio")
    #         return None
                        
    #     return masked_file


    def pipeline(self):
        if not os.path.exists(self.input_file):
            print("File not found")
            return None
        if not self.input_file.endswith('.mp3'):
            print("File is not mp3")
            return None

        self.wisperx()
        self.model()
        self.mask_audio()

if __name__ == '__main__':
    INPUT_FILE = './data/Sample1.mp3'


    # deid = Deid_audio(INPUT_FILE)
    # deid.pipeline()
    # print(deid.get_masked_file_path())


    deid = Deid_audio(INPUT_FILE)
    deid.wisperx()
    # deid.model()
    # deid.mask_audio()
    # print(deid.get_masked_file_path())




