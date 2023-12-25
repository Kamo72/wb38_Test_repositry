from Models import Kr2En, En2Kr, T5TextGen
from ppgTranslater import PPGTranslater

class Procedure () :
    def __init__(self) :
        self.isPPGmod = True
        self.ppg = PPGTranslater()
        if(self.isPPGmod == False) :
            self.ppg.available = False
        
        self.kr2en = Kr2En()
        self.en2kr = En2Kr()
        self.t5Gen = T5TextGen()
        self.infoEnText = ""
        
    def SetInfo (self, infoKoTextList) :
        self.infoEnText = ""
        count = 0
        for koText in infoKoTextList:
            print(f'[Process] info translating...{count}/{len(infoKoTextList)}')
            if(self.ppg.available) :
                self.infoEnText += self.ppg.Translate(koText, False)
            else :
                self.infoEnText += self.kr2en.Translate(koText)
            count += 1
        print(f'[Process] info translated!')
        
    def GetAnswer(self, questionKoText) :
        if(self.ppg.available) :
            inputEnText = self.ppg.Translate(questionKoText, False)
        else :
            inputEnText = self.kr2en.Translate(questionKoText)

        outputEnText = self.t5Gen.MakeAnswer(infoEnText=self.infoEnText, inputEnText=inputEnText)
        
        if(self.ppg.available) :
            outputKrText = self.ppg.Translate(outputEnText, True)
        else :
            outputKrText = self.en2kr.Translate(outputEnText)
            
        return outputKrText
