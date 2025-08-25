# py
import os
from pathlib import Path
# flet
# third
from pypdf import PdfWriter # type: ignore
# own

def merge_pdfs(input_folder, name_output_file="pdfs_fusionados.pdf"):
    try:
        # create merger.
        writer = PdfWriter()
        # verify if folder exits.
        if not os.path.exists(input_folder):
            # print(f"Error: El folder {input_folder} no existe.")
            return
        # get all pdfs.
        pdfs = [f for f in Path(input_folder).glob("*.pdf")]
        if not pdfs:
            # print(f"No se encontrarón PDFs en {input_folder}.")
            return
        # print(f"Se encontrarón {len(pdfs)} PDFs.")
        # add every PDF al merger.
        for pdf in pdfs:
            # print(f"Added: {pdf.name}")
            writer.append(str(pdf))
        # save the PDF merged.
        path_pdf_merged = os.path.join(input_folder, name_output_file).replace("\\", "/")
        writer.write(path_pdf_merged)
        writer.close()
    except Exception as _:
        pass

# input_folder = "./assets/files/PDFs"

# merge_pdfs(input_folder)