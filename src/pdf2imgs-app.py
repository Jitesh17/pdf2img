import base64
import os
import shutil
from datetime import datetime
import io
from PIL import Image
import numpy as np
# import PyPDF2
import streamlit as st
from pdf2image import convert_from_bytes, convert_from_path
# import pdfminer
# from pdfminer import extract_pages
from PyPDF2 import PdfFileReader, PdfFileWriter

from utils import load_image, upload_pdf

st.set_page_config(layout="wide")
def get_image_download_link(img):
	"""Generates a link allowing the PIL image to be downloaded
	in:  PIL image
	out: href string
	"""
	buffered = io.BytesIO()
	img.save(buffered, format="JPEG")
	img_str = base64.b64encode(buffered.getvalue()).decode()
	href = f'<a href="data:file/jpg;base64,{img_str}">Download</a>'
	return href


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
                # self.show_pdf(pdf_file)
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

        now = datetime.now()
        dt_string = now.strftime("%Y_%m_%d_%H_%M_%S")
        pdf2img_col = st.sidebar.beta_container()
        dpi = pdf2img_col.number_input('Enter DPI', value=200)
        fmt = pdf2img_col.selectbox('Select image format', ['jpeg', 'jpg', 'png', 'ppm'], index=1)
        convert_from_path(
            'data/temp.pdf',
            dpi=dpi,
            output_folder="data",
            first_page=None,
            last_page=None,
            fmt=fmt,
            jpegopt=None,
            thread_count=1,
            userpw=None,
            use_cropbox=False,
            strict=False,
            transparent=False,
            single_file=False,
            output_file=f"temp_{dt_string}",
            poppler_path=None,
            grayscale=False,
            size=None,
            paths_only=False,
            use_pdftocairo=False,
            timeout=None,
        )

    def show_img(self):
        st.markdown('## Images')
        image_paths =[p for p in os.listdir("data") if 'jpg' in p]
        col = []
        n = len(image_paths)
        n_cols = st.slider('Number of columns', min_value=1, max_value=10, value=3)
        while n > 0:
            col += st.beta_columns([1]*n_cols)
            n = n - n_cols
        for i, path in enumerate(image_paths):
            output = load_image(path, "data")
            col[i].image(image=output.astype(np.uint8),
                     use_column_width=True
                     )
            result = Image.fromarray(output)
            col[i].markdown(get_image_download_link(result), unsafe_allow_html=True)

if __name__ == "__main__":
    pdf2img()
