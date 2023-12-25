# -*- coding: cp949 -*-
from asyncio.windows_events import NULL
from re import split
import torch
from transformers import GenerationConfig, pipeline
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from Models import T5TextGen, En2Kr, Kr2En
from Procedure import Procedure
from LectureManager import LectureManager
from ServerAndClient import Server,Client
import socket, time

def MainProcess() :
    server = NULL
    client = NULL
    lm = LectureManager()
    proc = Procedure()

    def ServerDel (client_socket, msg) :
        print(msg),
        sp = msg.split("#")
        flag = sp[0]
        match flag:
            case "CreateLecture" : pass
            case "DeleteLecture" : pass
            case "ListLecture" : pass
            case "CreatePart" : pass
            case "DeletePart" : pass
            case "Listpart" : pass
            case "AppendContext" : pass
            case "ResetContext" : pass
            case "ListContext" : pass
            case "LoadContext" : pass
            case "GetAnswer" : pass
            case "StopProcess" : pass
    
    def ClientDel (msg) :
        print(msg),
        sp = msg.split("#")
        flag = sp[0]
        match flag:
            case "CreateLecture" :
                res = lm.MakeLecture(sp[1])
                client.Send("CreateLecture#" + str(res))
                
            case "DeleteLecture" : 
                res = lm.DeleteLecture(sp[1])
                client.Send("DeleteLecture#" + str(res))
                
            case "ListLecture" : 
                res = lm.ListLecture()
                pac = "ListLecture#"
                for lec in res : pac += lec + "@"
                client.Send(pac)
                
            case "CreatePart" : 
                ssp = sp[1].split("@")
                lm.LoadLecture(ssp[0])
                res = lm.MakePart(ssp[1])
                client.Send("CreatePart#" + str(res))
                
            case "DeletePart" :
                ssp = sp[1].split("@")
                lm.LoadLecture(ssp[0])
                res = lm.DeletePart(ssp[1])
                client.Send("DeletePart#" + str(res))
                
            case "Listpart" : 
                lm.LoadLecture(sp[1])
                res = lm.ListPart()
                pac = "Listpart#"
                for part in res : pac += part + "@"
                client.Send(pac)
                
            case "AppendContext" : 
                ssp = sp[1].split("@")
                lm.LoadLecture(ssp[0])
                lm.LoadPart(ssp[1])
                res = lm.WriteContext(ssp[2])
                client.Send("AppendContext#" + str(res))
                
            case "ResetContext" :
                ssp = sp[1].split("@")
                lm.LoadLecture(ssp[0])
                lm.LoadPart(ssp[1])
                res = lm.ResetContext()
                client.Send("ResetContext#" + str(res))
                
            case "ListContext" :
                ssp = sp[1].split("@")
                lm.LoadLecture(ssp[0])
                lm.LoadPart(ssp[1])
                res = lm.ReadContext()
                pac = "ListContext#"
                for part in res : pac += part + "@"
                client.Send(pac)
            
            case "LoadContext" :
                ssp = sp[1].split("@")
                lm.LoadLecture(ssp[0])
                lm.LoadPart(ssp[1])
                res = lm.ReadContext()
                proc.SetInfo(res)
                client.Send("LoadContext#" + str(True))
                
            case "GetAnswer" :
                ssp = sp[1].split("@")
                idx = ssp[0]
                res = proc.GetAnswer(ssp[1])
                client.Send("GetAnswer#" +ssp[0]+"#"+ res)
                
            case "StopProcess" :
                exit()

    server = Server('127.0.0.1', 4090, ServerDel)
    client = Client('127.0.0.1', 4090, ClientDel)
    
    server.Deploy()
    client.Connect()
    
    
    time.sleep(1)
    server.Send("CreateLecture#�ڻ����� �ɷη���")
    time.sleep(1)
    server.Send("DeleteLecture#�ڻ����� �ɷη���")
    time.sleep(1)
    server.Send("CreateLecture#�ڻ����� �ɷη���")
    time.sleep(1)
    server.Send("ListLecture#")
    time.sleep(1)
    server.Send("CreatePart#�ڻ����� �ɷη���@�ɷ��ɷθ�")
    time.sleep(1)
    server.Send("DeletePart#�ڻ����� �ɷη���@�ɷ��ɷθ�")
    time.sleep(1)
    server.Send("CreatePart#�ڻ����� �ɷη���@�ɷ��ɷθ�")
    time.sleep(1)
    server.Send("CreatePart#�ڻ����� �ɷη���@�Ƹ��ٵ� õ���� ��")
    time.sleep(1)
    server.Send("Listpart#�ڻ����� �ɷη���")
    time.sleep(1)
    server.Send("ResetContext#�ڻ����� �ɷη���@�ɷ��ɷθ�")
    time.sleep(1)
    server.Send("AppendContext#�ڻ����� �ɷη���@�ɷ��ɷθ�@�ڻ����� ���� 1���� �л��̴�. �ڻ��� �л��� �ſ� �ȶ��ϸ�, �ΰ����� �о߿��� ū �ɷ��� �����Ѵ�. �ڻ��� �л��� ���� ������ ������ �ִ� �л��̴�.")
    time.sleep(1)
    server.Send("ResetContext#�ڻ����� �ɷη���@�Ƹ��ٵ� õ���� ��")
    time.sleep(1)
    server.Send("AppendContext#�ڻ����� �ɷη���@�Ƹ��ٵ� õ���� ��@�ڻ����� ��۴뿡�� Ż���� �л��̴�. �ڻ��� �л��� ��۴뿡 ������ ������ �־���. �ڻ��� �л��� ��۴븦 �Ⱦ��Ѵ�. �ڻ��� �л��� ��۴뿡�� �����ƴ�.")
    time.sleep(1)
    server.Send("LoadContext#�ڻ����� �ɷη���@�Ƹ��ٵ� õ���� ��")
    time.sleep(10)
    server.Send("GetAnswer#1@�ڻ��� �л��� ���� �������ٷ�?")
    time.sleep(1)
    server.Send("LoadContext#�ڻ����� �ɷη���@�ɷ��ɷθ�")
    time.sleep(10)
    server.Send("GetAnswer#2@�ڻ��� �л��� ���� �������ٷ�?")

    a = input("insert any")
    exit()





    
    # lm.LoadLecture("�̵���_�˾��̰���")
    # lm.LoadPart("���־� ��Ʃ��� ������ �ȸ³׿�")
    # print(lm.ReadContext())
    # lm.WriteContext("sadsadasdsadsadsa")
    # print(lm.ReadContext())
    
    # a = input("insert any")
    # exit()



    # lm.MakeLecture("�̵���_�˾��̰���")
    # lm.ListLecture()
    # lm.LoadLecture("�̵���_�˾��̰���")
    
    # lm.ListLecture()

    # lm.MakePart("�˾˿˾˿˾˿˾�")
    # lm.MakePart("���־� ��Ʃ��� ������ �ȸ³׿�")
    # lm.MakePart("���.h")
    # lm.MakePart("���������̿�(����ǥ)")
    # lm.DeletePart("���������̿�(����ǥ)")
    # lm.MakePart("���������̿�(����ǥ)")
    # lm.LoadPart("���־� ��Ʃ��� ������ �ȸ³׿�")
    # lm.LoadPart("���־� ��Ʃ��� ������ �ȸ³׿�")
    
    # lm.ListPart()

    # print(lm.ReadContext())
    # infoKrTexts = """ 
    # �ΰ����� �н��� �������� �ð�, ����, ��� ���� ���ѱ��� �䱸�Ǵ� Ȱ��.
    # ������ ��ü���� ��� ����, ȯ�� ���� ����� ���� ���� �����н� ���� ���� �����ϴ� ���� �θ� �����ִ�.
    # �̸� ���� �÷������� Ʈ��������, ������̽� ���� �ִ�.       
    # �츰 �̷� �����н� ���� ���ؿ� �̼� ����(fine-tuning)�� ������ ����ڿ��� �����ϸ� �Ǵ� ���̴�.      
    # Transformer ���� �Ϲ������� �Ը� �ſ� Ů�ϴ�.
    # ���鸸���� ��õ�� ���� �Ű������� ���Ե� ���� �н��ϰ� �����ϴ� ���� �ſ� ������ �۾��Դϴ�.
    # �Դٰ� ���ο� ���� ���� ���� ��õǰ� ���� ������ ���� ����� �ֱ� ������, �� ��� �𵨵��� ������ ���� �� ���� ���� ���� �ƴմϴ�.
    # Transformers ���̺귯���� �̷��� ������ �ذ��ϱ� ���� ����������ϴ�.
    # �� ���̺귯���� ��ǥ�� ��� Transformer �𵨵��� �����ϰ�, �н��ϰ�, ������ �� �ִ� ���� API�� �����ϴ� ��.
    # �ڻ��� �л��� �Ŵ��� AI ���� �н���Ű�� �����ϱ� ���ؼ� �ʿ��մϴ�.
    # �ڻ��� �л��� AI ���� �����ϰ� �н���Ű�°� �ſ� �Ǹ��մϴ�.
    # �ڻ��� �л��� �ΰ����� ���߿� ����� ������ �ֽ��ϴ�.
    # �������� �����迡�� ���� �α��ִ� �����̴�.
    # �������� 5��5�� ����Ǵ� AOS �帣�� �����Դϴ�.
    # �������� ������ �������� �ý��۰� ������ Ÿ�ݰ�, ���� ��Ī�ý��� ���� �ֽ��ϴ�.
    # �ڻ��� �л��� �������� ���� �����մϴ�.
    # �������� �ų� HGC��� ���������� �ſ� �α��ִ� e-sports ��ȸ�� ��մϴ�."""
    

    # lm.WriteContext(infoKrTexts)
    # print(lm.ReadContext())
    
    # a = input("insert any")
    # exit()

    


    infoKrTexts = ["""
        �ΰ����� �н��� �������� �ð�, ����, ��� ���� ���ѱ��� �䱸�Ǵ� Ȱ��.
        ������ ��ü���� ��� ����, ȯ�� ���� ����� ���� ���� �����н� ���� ���� �����ϴ� ���� �θ� �����ִ�.
        �̸� ���� �÷������� Ʈ��������, ������̽� ���� �ִ�.       
        �츰 �̷� �����н� ���� ���ؿ� �̼� ����(fine-tuning)�� ������ ����ڿ��� �����ϸ� �Ǵ� ���̴�.
        ""","""           
        Transformer ���� �Ϲ������� �Ը� �ſ� Ů�ϴ�.
        ���鸸���� ��õ�� ���� �Ű������� ���Ե� ���� �н��ϰ� �����ϴ� ���� �ſ� ������ �۾��Դϴ�.
        �Դٰ� ���ο� ���� ���� ���� ��õǰ� ���� ������ ���� ����� �ֱ� ������, �� ��� �𵨵��� ������ ���� �� ���� ���� ���� �ƴմϴ�.
        Transformers ���̺귯���� �̷��� ������ �ذ��ϱ� ���� ����������ϴ�.
        �� ���̺귯���� ��ǥ�� ��� Transformer �𵨵��� �����ϰ�, �н��ϰ�, ������ �� �ִ� ���� API�� �����ϴ� ��.
        ""","""
        �ڻ��� �л��� �Ŵ��� AI ���� �н���Ű�� �����ϱ� ���ؼ� �ʿ��մϴ�.
        �ڻ��� �л��� AI ���� �����ϰ� �н���Ű�°� �ſ� �Ǹ��մϴ�.
        �ڻ��� �л��� �ΰ����� ���߿� ����� ������ �ֽ��ϴ�.
        ""","""
        �������� �����迡�� ���� �α��ִ� �����̴�.
        �������� 5��5�� ����Ǵ� AOS �帣�� �����Դϴ�.
        �������� ������ �������� �ý��۰� ������ Ÿ�ݰ�, ���� ��Ī�ý��� ���� �ֽ��ϴ�.
        �ڻ��� �л��� �������� ���� �����մϴ�.
        �������� �ų� HGC��� ���������� �ſ� �α��ִ� e-sports ��ȸ�� ��մϴ�.
        """]
    proc.SetInfo(infoKrTexts)

    while True :
        inputKrText = input("input : ")
        
        outputKrText = proc.GetAnswer(inputKrText)
        
        print("output : " + outputKrText)

MainProcess()

