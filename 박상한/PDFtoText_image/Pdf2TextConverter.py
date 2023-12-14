"""
Pdf2TextConverter.py

author: 코드장인
blog: https://blog.naver.com/shawgibal
"""

import os
from pathlib import Path
import traceback
import PyPDF2
import pdfplumber

import PdfWizardUtils

class Pdf2TextConverter:
    TXT_EXT = '.txt'

    def __init__(self):
        pass

    def convert(self, pdfFilePath, outputDir):
        try:
            print("PDF file path = {}".format(pdfFilePath))
            print("output dir = {}".format(outputDir))

            # 저장할 폴더가 존재하지 않으면 새로 생성
            if not os.path.exists(outputDir):
                os.makedirs(outputDir)

            # 파일 경로와 파일 이름 분리
            path, pdfFileName = os.path.split(pdfFilePath)

            # 파일 이름과 확장자 분리
            pdfFileNameWithoutExt = Path(pdfFileName).stem

            # pdf page 갯수 가져 오기
            pageNumber = 0
            with open(pdfFilePath, 'rb') as pdfFile:
                pdfReader = PyPDF2.PdfFileReader(pdfFile)
                pageNumber = pdfReader.numPages
                print('page number = ' + str(pageNumber))

            # pdf 페이지별로 text 추출 후 txt 파일로 저장
            textFilePathList = []
            with pdfplumber.open(pdfFilePath) as pdf:
                for i in range(pageNumber):
                    # PDF 페이지별로 텍스트 추출
                    page = pdf.pages[i]
                    text = page.extract_text()
                    print(text)

                    # text 파일 이름 생성
                    txtFileName = pdfFileNameWithoutExt + '-page-' + str(i).zfill(3) + self.TXT_EXT
                    txtFilepath = outputDir + "\\" + txtFileName

                    # text를 txt 파일로 저장
                    with open(txtFilepath, 'w', encoding='UTF-8') as txtFile:
                        txtFile.write(text)

                    # text file path를 리스트에 추가
                    textFilePathList.append(txtFilepath)

            return textFilePathList

        except Exception as e:
            raise(e)





"""
Test Pdf2TextConverter
"""

def testPdf2TextConverter():
    try:
        # 변환할 PDF 파일
        pdfFileName = 'PDF 텍스트 추출 테스트.pdf'

        dataDir = os.getcwd() + '\\data'
        # 입력: PDF 파일 전체 경로
        pdfFilePath = dataDir + "\\" + pdfFileName
        # 출력: 텍스트 파일을 저장할 디렉토리        
        outputDir = dataDir + "\\" + Path(pdfFileName).stem + "\\text"

        # PDF에서 TEXT 파일 추출하고 txt 파일로 저장
        pdf2TextConverter = Pdf2TextConverter()
        textFilePathList = pdf2TextConverter.convert(pdfFilePath, outputDir)

        # txt 파일 리스트를 출력
        print('\n')
        print('-' * 60)
        print('PDF 텍스트 추출 파일 리스트')
        print('-' * 60)
        [print(textFilePath) for textFilePath in textFilePathList]

    except Exception as e:
        print(e)
        traceback.format_exc(e)


if __name__ == '__main__':
    testPdf2TextConverter()