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
    server.Send("CreateLecture#박상한의 케로로학")
    time.sleep(1)
    server.Send("DeleteLecture#박상한의 케로로학")
    time.sleep(1)
    server.Send("CreateLecture#박상한의 케로로학")
    time.sleep(1)
    server.Send("ListLecture#")
    time.sleep(1)
    server.Send("CreatePart#박상한의 케로로학@케로케로링")
    time.sleep(1)
    server.Send("DeletePart#박상한의 케로로학@케로케로링")
    time.sleep(1)
    server.Send("CreatePart#박상한의 케로로학@케로케로링")
    time.sleep(1)
    server.Send("CreatePart#박상한의 케로로학@아마겟돈 천분의 일")
    time.sleep(1)
    server.Send("Listpart#박상한의 케로로학")
    time.sleep(1)
    server.Send("ResetContext#박상한의 케로로학@케로케로링")
    time.sleep(1)
    server.Send("AppendContext#박상한의 케로로학@케로케로링@박상한은 전교 1등의 학생이다. 박상한 학생은 매우 똑똑하며, 인공지능 분야에서 큰 능력을 발휘한다. 박상한 학생은 좋은 성적을 가지고 있는 학생이다.")
    time.sleep(1)
    server.Send("ResetContext#박상한의 케로로학@아마겟돈 천분의 일")
    time.sleep(1)
    server.Send("AppendContext#박상한의 케로로학@아마겟돈 천분의 일@박상한은 우송대에서 탈출한 학생이다. 박상한 학생은 우송대에 싫증을 느끼고 있었다. 박상한 학생은 우송대를 싫어한다. 박상한 학생은 우송대에서 도망쳤다.")
    time.sleep(1)
    server.Send("LoadContext#박상한의 케로로학@아마겟돈 천분의 일")
    time.sleep(10)
    server.Send("GetAnswer#1@박상한 학생에 대해 설명해줄래?")
    time.sleep(1)
    server.Send("LoadContext#박상한의 케로로학@케로케로링")
    time.sleep(10)
    server.Send("GetAnswer#2@박상한 학생에 대해 설명해줄래?")

    a = input("insert any")
    exit()





    
    # lm.LoadLecture("이동우_옹알이개론")
    # lm.LoadPart("비주얼 스튜디오 버전이 안맞네요")
    # print(lm.ReadContext())
    # lm.WriteContext("sadsadasdsadsadsa")
    # print(lm.ReadContext())
    
    # a = input("insert any")
    # exit()



    # lm.MakeLecture("이동우_옹알이개론")
    # lm.ListLecture()
    # lm.LoadLecture("이동우_옹알이개론")
    
    # lm.ListLecture()

    # lm.MakePart("옹알옹알옹알옹알")
    # lm.MakePart("비주얼 스튜디오 버전이 안맞네요")
    # lm.MakePart("헤더.h")
    # lm.MakePart("만사형통이여(물음표)")
    # lm.DeletePart("만사형통이여(물음표)")
    # lm.MakePart("만사형통이여(물음표)")
    # lm.LoadPart("비주얼 스튜디오 버전이 안맞네요")
    # lm.LoadPart("비주얼 스튜디오 버전이 안맞네요")
    
    # lm.ListPart()

    # print(lm.ReadContext())
    # infoKrTexts = """ 
    # 인공지능 학습은 에너지와 시간, 정보, 장비 등이 극한까지 요구되는 활동.
    # 때문에 전체적인 비용 증가, 환경 오염 등등을 막기 위해 사전학습 모델을 서로 공유하는 것이 널리 퍼져있다.
    # 이를 위한 플랫폼으로 트랜스포머, 허깅페이스 등이 있다.       
    # 우린 이런 사전학습 모델을 구해와 미세 조정(fine-tuning)을 적용해 사용자에게 제공하면 되는 것이다.      
    # Transformer 모델은 일반적으로 규모가 매우 큽니다.
    # 수백만에서 수천억 개의 매개변수가 포함된 모델을 학습하고 배포하는 일은 매우 복잡한 작업입니다.
    # 게다가 새로운 모델이 거의 매일 출시되고 각각 고유한 구현 방식이 있기 때문에, 이 모든 모델들을 시험해 보는 것 또한 쉬운 일이 아닙니다.
    # Transformers 라이브러리는 이러한 문제를 해결하기 위해 만들어졌습니다.
    # 이 라이브러리의 목표는 모든 Transformer 모델들을 적재하고, 학습하고, 저장할 수 있는 단일 API를 제공하는 것.
    # 박상한 학생은 거대한 AI 모델을 학습시키고 보급하기 위해서 필요합니다.
    # 박상한 학생은 AI 모델을 개발하고 학습시키는게 매우 훌륭합니다.
    # 박상한 학생은 인공지능 개발에 재능을 가지고 있습니다.
    # 히오스는 전세계에서 가장 인기있는 게임이다.
    # 히오스는 5대5로 진행되는 AOS 장르의 게임입니다.
    # 히오스의 장점은 공산주의 시스템과 끔찍한 타격감, 느린 매칭시스템 등이 있습니다.
    # 박상한 학생은 히오스를 정말 좋아합니다.
    # 히오스는 매년 HGC라는 세계적으로 매우 인기있는 e-sports 대회를 운영합니다."""
    

    # lm.WriteContext(infoKrTexts)
    # print(lm.ReadContext())
    
    # a = input("insert any")
    # exit()

    


    infoKrTexts = ["""
        인공지능 학습은 에너지와 시간, 정보, 장비 등이 극한까지 요구되는 활동.
        때문에 전체적인 비용 증가, 환경 오염 등등을 막기 위해 사전학습 모델을 서로 공유하는 것이 널리 퍼져있다.
        이를 위한 플랫폼으로 트랜스포머, 허깅페이스 등이 있다.       
        우린 이런 사전학습 모델을 구해와 미세 조정(fine-tuning)을 적용해 사용자에게 제공하면 되는 것이다.
        ""","""           
        Transformer 모델은 일반적으로 규모가 매우 큽니다.
        수백만에서 수천억 개의 매개변수가 포함된 모델을 학습하고 배포하는 일은 매우 복잡한 작업입니다.
        게다가 새로운 모델이 거의 매일 출시되고 각각 고유한 구현 방식이 있기 때문에, 이 모든 모델들을 시험해 보는 것 또한 쉬운 일이 아닙니다.
        Transformers 라이브러리는 이러한 문제를 해결하기 위해 만들어졌습니다.
        이 라이브러리의 목표는 모든 Transformer 모델들을 적재하고, 학습하고, 저장할 수 있는 단일 API를 제공하는 것.
        ""","""
        박상한 학생은 거대한 AI 모델을 학습시키고 보급하기 위해서 필요합니다.
        박상한 학생은 AI 모델을 개발하고 학습시키는게 매우 훌륭합니다.
        박상한 학생은 인공지능 개발에 재능을 가지고 있습니다.
        ""","""
        히오스는 전세계에서 가장 인기있는 게임이다.
        히오스는 5대5로 진행되는 AOS 장르의 게임입니다.
        히오스의 장점은 공산주의 시스템과 끔찍한 타격감, 느린 매칭시스템 등이 있습니다.
        박상한 학생은 히오스를 정말 좋아합니다.
        히오스는 매년 HGC라는 세계적으로 매우 인기있는 e-sports 대회를 운영합니다.
        """]
    proc.SetInfo(infoKrTexts)

    while True :
        inputKrText = input("input : ")
        
        outputKrText = proc.GetAnswer(inputKrText)
        
        print("output : " + outputKrText)

MainProcess()

