"""
Pdf2ImageConverter.py

author: 코드장인
blog: https://blog.naver.com/shawgibal
"""

import os
from pathlib import Path
import traceback
import pdf2image

class Pdf2ImageConverter:
    IMG_EXT = '.jpg'
    IMG_FORMAT = 'JPEG'
    IMG_SIZE_FULL_HD = (1920, 1080)

    def __init__(self):
        self.__poppler_path__ = os.getcwd() + "\\lib\\poppler-21.10.0\\Library\\bin\\"
        print("poppler path = " + self.__poppler_path__)

    def convert(self, pdfFilePath, outputPath):
        print("PDF file path = {}".format(pdfFilePath))
        print("output dir = {}".format(outputPath))
        # 저장할 폴더가 존재하지 않으면 새로 생성
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)

        # 파일 경로와 파일 이름 분리
        path, pdfFileName = os.path.split(pdfFilePath)

        # 파일 이름과 확장자 분리
        image_prefix = Path(pdfFileName).stem

        # pdf에서 이미지 추출
        pdf2images = pdf2image.convert_from_path(pdfFilePath, 
                                                poppler_path = self.__poppler_path__,
                                                size=self.IMG_SIZE_FULL_HD)

        # 추출한 이미지를 outputPath 아래에 jpg 파일로 저장
        image_file_path_list = []
        for i in range(len(pdf2images)):
            image_name = image_prefix + '-page-' + str(i).zfill(3) + self.IMG_EXT
            image_filepath = outputPath + "\\" + image_name
            pdf2images[i].save(image_filepath, self.IMG_FORMAT)
            image_file_path_list.append(image_filepath)

        return image_file_path_list



"""
Test Pdf2ImageConverter
"""

def testPdf2ImageConverter():
    try:
        pdf_file_name = 'PDF 이미지 변환 테스트.pdf'

        data_dir = os.getcwd() + '\\data'
        pdf_file_path = data_dir + "\\" + pdf_file_name
        output_dir = data_dir + "\\" + Path(pdf_file_name).stem + "\\image"

        pdf2ImageConverter = Pdf2ImageConverter()
        image_file_path_list = pdf2ImageConverter.convert(pdf_file_path, output_dir)
        print(image_file_path_list)
    except Exception as e:
        print(e)
        traceback.format_exc(e)


if __name__ == '__main__':
    testPdf2ImageConverter()