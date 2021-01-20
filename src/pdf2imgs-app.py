import base64
import os
import shutil

import numpy as np
import PyPDF2
import streamlit as st
from pdf2image import convert_from_bytes, convert_from_path
# import pdfminer
# from pdfminer import extract_pages
from PyPDF2 import PdfFileReader, PdfFileWriter

from utils import load_image, upload_pdf


def add_encryption(input_pdf, output_pdf, password):
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(input_pdf)

    for page in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(page))

    pdf_writer.encrypt(user_pwd=password, owner_pwd=None,
                       use_128bit=True)

    with open(output_pdf, 'wb') as fh:
        pdf_writer.write(fh)


class pdf2img:
    def __init__(self):
        self.run_the_app()
        # st = st.empty()
        # st = st.empty()

    def run_the_app(self, ):
        # st.set_page_config(layout="wide")
        st.title('PDF to Image convertor')
        st.balloons()
        pdf_file = upload_pdf()
        if not os.path.exists("data"):
            os.mkdir("data")
        if pdf_file is not None:
            if os.path.exists("data"):
                self.show_pdf(pdf_file)
                self.write_pdf(pdf_file)
                self.convert_pdf2img()
                self.show_img()
        if os.path.exists("data"):
            shutil.rmtree("data")

    def show_pdf(self, pdf_file):
        st.markdown('## PDF')
        base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
        st.markdown(pdf_display, unsafe_allow_html=True)

    def write_pdf(self, pdf_file):
        pdf_writer = PdfFileWriter()
        pdf_reader = PdfFileReader(pdf_file, strict=False)
        # Rotate page 90 degrees to the right
        page_1 = pdf_reader.getPage(0)
        pdf_writer.addPage(page_1)
        # Rotate page 90 degrees to the left
        page_2 = pdf_reader.getPage(1)
        pdf_writer.addPage(page_2)
        # Add a page in normal orientation
        pdf_writer.addPage(pdf_reader.getPage(2))

        with open('data/temp.pdf', 'wb') as fh:
            pdf_writer.write(fh)

    def convert_pdf2img(self):

        convert_from_path(
            'data/temp.pdf',
            dpi=200,
            output_folder="data",
            first_page=None,
            last_page=None,
            fmt="jpg",
            jpegopt=None,
            thread_count=1,
            userpw=None,
            use_cropbox=False,
            strict=False,
            transparent=False,
            single_file=False,
            output_file="temp",
            poppler_path=None,
            grayscale=False,
            size=None,
            paths_only=False,
            use_pdftocairo=False,
            timeout=None,
        )

    def show_img(self):
        st.markdown('## Images')
        for path in [p for p in os.listdir("data") if 'jpg' in p]:
            output = load_image(path, "data")
            st.image(image=output.astype(np.uint8),
                     use_column_width=True
                     )


if __name__ == "__main__":
    pdf2img()
