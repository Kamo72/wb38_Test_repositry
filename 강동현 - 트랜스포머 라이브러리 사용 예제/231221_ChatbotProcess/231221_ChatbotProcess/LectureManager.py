# -*- coding: cp949 -*-
import os
from asyncio.windows_events import NULL
from re import I

class LectureManager(object):
    def __init__(self):
        user_documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
        self.filePath = f"{user_documents_path}\WB38Test"
        self.lecturePath = ""
        self.partPath = ""
    

    def LoadLecture(self, lectureName) :
        dirPath = f"{self.filePath}\{lectureName}"
        
        if os.path.exists(dirPath):       
            self.lecturePath = dirPath
            print(f"[SUCCEED] lecture is found : {dirPath}")
            return True
        else :
            print(f"[ERROR] failed to find directory : {dirPath} it's not exists already.")
            return False
    
    def MakeLecture(self, lectureName, ):
        dirPath = f"{self.filePath}\{lectureName}"
        
        if os.path.exists(dirPath):
            print(f"[WARNING] failed to make directory : {dirPath}, it exists already.")
            return False
        else :
            os.makedirs(dirPath)
            print(f"[SUCCEED] succeed to make directory at : {dirPath}")
            return True
        
    def ListLecture(self):
        folders = [f for f in os.listdir(self.filePath) if os.path.isdir(os.path.join(self.filePath, f))]
        
        print('[SUCCEED] all lectures in disk found : ')
        
        for folder in folders:
            print(folder)
        return folders
    
    def DeleteLecture(self, lecture) :
        ditToDel = f"{self.filePath}\{lecture}.txt"
        
        try:
            if os.path.exists(ditToDel):
                print(f"[WARNING] failed to delete directory : {ditToDel}, it's not exists already.")
                return False
            
            os.rmdir(ditToDel)
            
            if(self.lecturePath == ditToDel) :
                self.partPath = ""
                self.lecturePath = ""
                
            print(f'[SUCCEED] success to delete : {ditToDel}')
            return True
        
        except OSError as e:
            print(f'[ERROR] failed to delete : {ditToDel}')
            return False



    def LoadPart(self, partName):
        dirToLoad = f"{self.lecturePath}\{partName}.txt"
        if self.lecturePath == "" :
            print(f"[ERROR] to load part, you must load lecture first.")
            return False
        
        if not os.path.exists(dirToLoad):
            print(f"[ERROR] failed to load file at : {dirToLoad}, it isn't exists.")
            return False   
        
        self.partPath = f"{dirToLoad}"
        print(f"[SUCCEED] succesfully file is created at : {self.partPath}")
        
        return False
    
    def MakePart(self, partName):
        dirToMake = f"{self.lecturePath}/{partName}.txt"

        if self.lecturePath == "" :
            print(f"[ERROR] to make part, you must load lecture first.")
            return False
        
        if os.path.exists(dirToMake):
            print(f"[WARNING] failed to make file at : {dirToMake}, it exists already.")
            return False            

        with open(dirToMake, 'w') as file:
            file.write('')
        print(f"[SUCCEED] succesfully file is created at : {dirToMake}")
        return True        

    def ListPart(self):
        if self.lecturePath == "" :
            print(f"[ERROR] to List parts, you must load lecture first.")
            return []
        
        files = [f for f in os.listdir(self.lecturePath) if os.path.isfile(os.path.join(self.lecturePath, f))]
        print(f'[SUCCEED] all parts in lecture ({self.lecturePath}) found : ')
        
        for file in files :
            print(file)
        return files
    
    def DeletePart(self, partName) :
        dirToDel = f"{self.lecturePath}/{partName}.txt"
        try:
            if self.lecturePath == "" :
                print(f"[ERROR] to delete part, you must load lecture first.")
                return False
        
            if not os.path.exists(dirToDel):
                print(f"[ERROR] failed to delete file at : toDelDir, it isn't exists .")
                return False  
        
            os.remove(dirToDel)
            print(f"[SUCCEED] succesfully file is deleted at : {dirToDel}")
            if(self.partPath == dirToDel) : 
                self.partPath = ""
            return True
        
        except OSError as e:
            print(f'[ERROR] failed to delete : {dirToDel}')
            return False
        
        

    def WriteContext(self, context):
        if self.partPath == "" :
            print(f"[ERROR] to write context, you must load lecture's part first.")
            return False
        
        if not os.path.exists(self.partPath):
            print(f"[ERROR] failed to find file at : {self.partPath}, it isn't exists.")
            return False   
            
        with open(self.partPath, 'a') as file:
            file.write(context)
            print(f"[SUCCEED] succesfully contexts is appended")
        return True
            
    def ReadContext(self):
        if self.partPath == "" :
            print(f"[ERROR] to read context, you must load lecture's part first.")
            return []
        
        if not os.path.exists(self.partPath):
            print(f"[ERROR] failed to find file at : {self.partPath}, it isn't exists.")
            return []   
        
        with open(self.partPath, 'r') as file:
            lines = file.readlines()

        # 줄바꿈에 따라 3줄씩 끊어서 배열로 저장
        lines_array = [lines[i:i+3] for i in range(0, len(lines), 3)]

        if(len(lines_array) != 0) :
            lines_array = lines_array[0]

        # for lineSet in lines_array :
        #     lineSet.replace("    ","")
            
        print(f"[SUCCEED] succesfully contexts is read")
        return lines_array
    
    def ResetContext(self) :
        if self.partPath == "" :
            print(f"[ERROR] to clear context, you must load lecture's part first.")
            return False
        
        if not os.path.exists(self.partPath):
            print(f"[ERROR] failed to find file at : {self.partPath}, it isn't exists.")
            return False   
            
        with open(self.partPath, 'w') as file:
            file.write('')
        
        print(f"[SUCCEED] succesfully contexts is cleared")
        return False

