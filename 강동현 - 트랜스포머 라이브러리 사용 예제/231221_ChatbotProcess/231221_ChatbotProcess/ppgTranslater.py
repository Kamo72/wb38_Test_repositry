import os
import sys
import urllib.request
import json

class PPGTranslater(object):
    def __init__(self):
        self.client_id = "Vsl7By5p_q7pJCM6WmBI"
        self.client_secret = "3JrGsfsucs"
        self.SetAvailable(self.GetAvailable())
    
    def GetAvailable(self) :
       return self.Translate("a", True) != "[API ERROR : Papago malfunction]"
    
    def SetAvailable(self, isAvailable) :
       self.available = isAvailable
            
        
    def Translate(self, enText, isEntoKo) :
        encText = urllib.parse.quote(enText)
        data = ""
        
        if(isEntoKo) : data ="source=en&target=ko&text=" + encText
        else : data ="source=ko&target=en&text=" + encText
        
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",self.client_id)
        request.add_header("X-Naver-Client-Secret",self.client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            decoded_data = response_body.decode('utf-8')
            json_data = json.loads(decoded_data)
            translated_text = json_data["message"]["result"]["translatedText"]
            self.SetAvailable(True)
            return translated_text
        else:
            self.SetAvailable(False)
            print("Error Code:" + rescode)
            return "[API ERROR : Papago malfunction]"
    pass




