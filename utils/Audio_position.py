import json

# input json format
'''
asr
|-- language
|-- segments[]
    |-- start
    |-- end
    |-- text
    |-- words[]
        |-- word
        |-- start
        |-- end
        |-- score
|-- word_segments[]
    |-- word
    |-- start
    |-- end
    |-- score
'''


class Audio_position:
    def __init__(self, json_data):
        self.segments = json_data['segments']
        for seg in self.segments:
            for word in seg['words']:
                word['mask'] = False

        # add mask type
        for seg in self.segments:
            for word in seg['words']:
                word['mask_type'] = ''
    
        '''
        |-- segments[]
            |-- start
            |-- end
            |-- text
            |-- words[]
                |-- word
                |-- start
                |-- end
                |-- score
                |-- mask 
        '''

        self.mask = []
        '''
        |-- mask[]
            |-- str
            |-- start
            |-- end

        '''
    def __len__(self): 
        return len(self.segments)

    def remove_end_punctuation(self, word):
        punctuation = ['.', ',','?' , '!' , ':' , ';']
        while word[-1] in punctuation:
            word = word[:-1]
        return word

    def compare_str(self, str1, str2):
        if str1 == None or str2 == None:
            return False
        w1 = str1.strip()
        w2 = str2.strip()
        w1 = self.remove_end_punctuation(w1)
        w2 = self.remove_end_punctuation(w2)
        return w1 == w2
    
    def word_2_word_index(self, sentence_index, word , start = 0):
        for i in range(start, len(self.segments[sentence_index]['words'])):
            if self.compare_str(self.segments[sentence_index]['words'][i]['word'], word):
                return i
        return None
    

    def get_sentence(self, sentence_index):
        if sentence_index==None:
            return None
        if sentence_index < len(self.segments):
            return self.segments[sentence_index]['text']
    def get_word(self, sentence_index, word_index):
        if sentence_index==None or word_index==None:
            return None
        if sentence_index < len(self.segments) and word_index < len(self.segments[sentence_index]['words']):
            return self.segments[sentence_index]['words'][word_index]['word']

    

    def search_continuous_word_index(self, sentence_index, str):
        """
        Search for the continuous index of a word in the sentence.
        """
        start_w_index = 0
        # sentence = self.get_sentence(sentence_index)
        query = str.split()
        while start_w_index < len(self.segments[sentence_index]['words']):
            still_continuous = True
            for i in range(len(query)):
                if not self.compare_str(query[i], self.get_word(sentence_index, start_w_index + i)):
                    still_continuous = False
                    break
            if still_continuous:
                return start_w_index , start_w_index + len(query)
            start_w_index += 1
        return None

    def set_mask(self, sentence_index,  mask_range, mask_type='<MASK>' ,mask_value=True):
        """
        Set the mask attribute of a word.
        """
        if mask_range == None:
            return
        assert mask_range[0] <= mask_range[1]
        assert sentence_index < len(self.segments)
        assert mask_range[1] <= len(self.segments[sentence_index]['words']) 
        assert mask_value == True or mask_value == False

        for i in range(mask_range[0], mask_range[1]):
            self.segments[sentence_index]['words'][i]['mask'] = mask_value
            self.segments[sentence_index]['words'][i]['mask_type'] = mask_type

    def print_segments(self , s , e):
        print(json.dumps(self.segments[s:e], indent=4))

    def generate_mask(self):
        # if the mask in the same sentence, then it is continuous , it will be merged(time and word). 
        
        for seg in self.segments:
            last_mask = False
            words = []
            start_t = None
            end_t = None

            start_type = ''

            # some word dont start or end time, will use last word's time
            # last_start = 0
            # last_end = 0

            # some segment only have one not start and end time word, will use segment's start and end time
            seg_start = seg['start']
            seg_end = seg['end']
            
            # print(json.dumps(seg, indent=4))
            for word in seg['words']:
                if last_mask == False and word['mask'] == True:
                    # if word['start'] exit
                    start_t = word['start'] if 'start' in word.keys() else seg_start
                    end_t = word['end'] if 'end' in word.keys() else seg_end
                    words.append(word['word'])
                    start_type = word['mask_type']
                elif last_mask == True and word['mask'] == True:
                    end_t = word['end'] if 'end' in word.keys() and end_t < word['end'] else seg_end
                    #if end_t < word['end'] else end_t
                    words.append(word['word'])
                elif last_mask == True and word['mask'] == False:
                    if len(words)>0 and start_t != None and end_t != None:
                        # self.mask.append({'str': ' '.join(words), 'start': start_t, 'end': end_t})
                        self.mask.append({'str': ' '.join(words), 'type': start_type, 'start': start_t, 'end': end_t})                                           
                        
                    words = []
                    start_t = None
                    end_t = None
                else:
                    pass
                last_mask = word['mask']
                # last_start = word['start'] if 'start' in word.keys() else last_start
                # last_end = word['end'] if 'end' in word.keys() else last_end
            if last_mask == True:
                if len(words)>0 and start_t != None and end_t != None:
                    # whispex some end will smaller than start
                    # if start_t > end_t:
                    #     start_t, end_t = end_t, start_t
                    if start_t < end_t:
                        mask_type = word['mask_type']
                        # self.mask.append({'str': ' '.join(words), 'start': start_t, 'end': end_t})
                        self.mask.append({'str': ' '.join(words), 'type': start_type, 'start': start_t, 'end': end_t})                                           

                words = []
        return self.mask
    
    def get_mask(self):
        return self.mask
    def get_mask_time(self):
        times = []
        for m in self.mask:
            times.append([m['start'], m['end']])
        return times



if __name__ == '__main__':
    
    json_data = None
    with open('./.output/Sample2.json') as f:
        json_data = json.load(f)
    apos = Audio_position(json_data)
    
    print(apos.get_sentence(2))
    res = apos.search_continuous_word_index(2, 'you going')


    print(res)

    apos.set_mask(2, res)

    apos.print_segments(0, 3)


    apos.generate_mask()
    print(json.dumps(apos.mask[:6], indent=4))

    print("times : " , apos.get_mask_time() ) 

