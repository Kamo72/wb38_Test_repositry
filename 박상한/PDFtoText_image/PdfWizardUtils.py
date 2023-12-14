"""
PdfWizardUtils.py

author: 코드장인
blog: https://blog.naver.com/shawgibal
"""

import os
from pathlib import Path

"""
출력 파일을 저장할 디렉토리 생성
-> PDF 파일이 있는 디렉토리 + PDF 파일 이름 
"""
DATA_DIR = '\\data'

def createWorkDir(pdfFilePath):
    try:
        print("PDF file name = {}".format(pdfFilePath))

        # 경로와 파일 이름 분리
        path, pdfFileName = os.path.split(pdfFilePath)

        # 파일 이름과 확장자 분리
        pdfNameOnly = Path(pdfFileName).stem

        # 작업 디렉토리
        workDir = path + '/' + pdfNameOnly
        print("work directory = {}".format(workDir))

        # 디렉토리 생성
        if not os.path.exists(workDir):
            os.makedirs(workDir)

    except Exception as e:
        raise(e)

    return workDir



"""
test
"""

if __name__ == '__main__':
    try:
        pdfFileName = 'PDF 텍스트 추출 테스트.pdf'
        dataDir = os.getcwd() + '\\data'
        pdfFilePath = dataDir + "\\" + pdfFileName        
        
        createWorkDir(pdfFilePath)

    except Exception as e:
        print(e)