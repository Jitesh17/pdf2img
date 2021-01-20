from __future__ import annotations

import os

import streamlit as st
from pdf2image import convert_from_bytes, convert_from_path

from utils import load_image, upload_pdf

st.set_page_config(layout="wide")

class pdf2img:
    def __init__(self):
        self.run_the_app()
        
    def run_the_app(self, ):
        st.title('PDF to Image convertor')
        pdf_file = upload_pdf()
        if not os.path.exists("data"):
            os.mkdir("data")
        convert_from_bytes(
            pdf_file,
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
        output = load_image("data/temp.jpg")
        st.image(image=output,
                        use_column_width=True
                        )
if __name__ == "__main__":
    pdf2img()
