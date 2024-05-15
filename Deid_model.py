from typing import Any
from transformers import AutoTokenizer, AutoModelForCausalLM

class Deid_model:
    def __init__(self, model_path , device = 'cuda'):
        self.model_path = model_path
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path , device_map = device)        
        

        self.model.eval()
        self.bos = '<|endoftext|>'
        self.eos = '<|END|>'
        self.pad = '<|pad|>'
        self.sep ='\n\n####\n\n'
        self.eos_id = self.tokenizer.convert_tokens_to_ids(self.eos)
        self.pad_id = self.tokenizer.convert_tokens_to_ids(self.tokenizer.pad_token)      
    
    def input_template(self, text):
        if type(text) == list:
            input_text = [f"{self.bos} {s} {self.sep}" for s in text]
        else:
            input_text = f"{self.bos} {text} {self.sep}"
        return input_text 

    def get_labels(self, model_output):
        label_start = model_output.index(self.sep) + len(self.sep)
        pred = model_output[label_start:].replace(self.eos, '')
        pred = pred.replace(self.pad, '')
        pred = pred.strip() 
        labels = []
        for l in pred.split('\n'):
            if l != '' and l != 'PHI: NULL' and ':' in l:
                label = l.split(':')[0].strip()
                content = l.split(':')[1].strip()
                if '=>' in content:
                    content = content.split('=>')[0].strip()
                if content != '':
                    labels.append([label, content])
        return labels

    def __call__(self , text):
        input_text = self.input_template(text)
        input_tensor = self.tokenizer(input_text, return_tensors="pt").to(self.device) # padding=True
        output_tokens = self.model.generate(
                            **input_tensor,
                            max_new_tokens=400, 
                            pad_token_id = self.pad_id,
                            eos_token_id=self.eos_id
                        )
        output_text = self.tokenizer.batch_decode(output_tokens)

        # [ [label , content]*n ]
        labels = [self.get_labels(o) for o in output_text]        
        return labels


    



if __name__ == '__main__':
    

    # model = Deid_model('model/pythia/model_v5_EP8_2023_1130_1450_10')


    # test islab model
    # ISLabResearch/opendeid-70m-ft-full
    # ISLabResearch/opendeid-160m-ft-full
    # ISLabResearch/opendeid-410m-ft-full
    # ISLabResearch/opendeid-1b-ft-full
    # ISLabResearch/opendeid-2.8b-ft-full
    # ISLabResearch/opendeid-6.9b-ft-full
    # ISLabResearch/opendeid-12b-ft-full

    model = Deid_model('ISLabResearch/opendeid-410m-ft-full')

    # test __call__
    s = 'Hi, Doctor Rhee. I am a 23'
    ss = [s,s]
    print('s : ' , model(s))
    print('ss : ' , model(ss))



