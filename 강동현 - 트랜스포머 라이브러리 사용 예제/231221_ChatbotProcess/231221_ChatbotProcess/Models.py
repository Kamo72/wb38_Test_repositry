# -*- coding: cp949 -*-
import torch
from transformers import GenerationConfig, pipeline
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class T5TextGen():
    
    def __init__ (self):
        print('[Process] Loading T5...')
        modelname = "google/flan-t5-large"
        self.tokenizer = T5Tokenizer.from_pretrained(modelname)
        self.model = T5ForConditionalGeneration.from_pretrained(modelname).to("cuda")
        print('[Process] Loaded T5!')
    
    def MakeAnswer (self, infoEnText, inputEnText) :
        print('[Process] Answer generating...')
        input_ids = self.tokenizer(infoEnText + "Question : Please write about 50 characters,  " +inputEnText + "?", return_tensors="pt").input_ids.to("cuda")
        genConfig = GenerationConfig(
            # num_beams = 2,
            # length_penalty=0.1,
            do_sample=True,
            # temperature  = 1,
            repetition_penalty = 10.0,
            max_length = 500
            )
        
        outputEnData = self.model.generate(input_ids, generation_config=genConfig)
        outputEnText = self.tokenizer.decode(outputEnData[0], skip_special_tokens=True)
        print('[Process] Answer generated! - ' + outputEnText)
        return outputEnText


class En2Kr ():
    
    def __init__(self) :
        print('[Process] Loading en2krTrs...')
        
        modelname = "hyerin/m2m100_418M-finetuned-en-to-ko"
        self.tokenizer = AutoTokenizer.from_pretrained(modelname)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(modelname).to("cuda")

        print('[Process] Loaded en2krTrs!')
        
    def Translate(self, text) : 
        print('[Process] en2krTrs translating...')
        input_ids = self.tokenizer.encode(text, return_tensors="pt").to("cuda")
        
        genConfig = GenerationConfig(
            # num_beams = 2,
            # length_penalty=0.1,
            # do_sample=True,
            # temperature  = 0.1,
            # repetition_penalty = 10.0,
            max_length = 500
            )                

        output_ids = self.model.generate(input_ids, genConfig)
        translated_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=False)
        translated_text = translated_text.replace("</s>", "")
        translated_text = translated_text.replace("__ko__ ", "")
        print('[Process] en2krTrs translated! - ' + translated_text)
        return translated_text
    

class Kr2En ():

    def __init__(self) :
        print('[Process] Loading kr2enTrs...')
        
        modelname = "hcho22/opus-mt-ko-en-finetuned-kr-to-en"
        self.tokenizer = AutoTokenizer.from_pretrained(modelname)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(modelname, from_tf=True).to("cuda")
        
        print('[Process] Loaded kr2enTrs!')
        
    def Translate(self, text) : 
        print('[Process] kr2enTrs translating...')
        input_ids = self.tokenizer.encode(text, return_tensors="pt").to("cuda")
        genConfig = GenerationConfig(
            # num_beams = 2,
            # length_penalty=0.1,
            do_sample=True,
            temperature  = 0.1,
            # repetition_penalty = 10.0,
            max_length = 500
            )        

        output_ids = self.model.generate(input_ids,genConfig)
        translated_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        print('[Process] kr2enTrs translated! - ' + translated_text)
        return translated_text