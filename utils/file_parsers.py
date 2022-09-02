import pandas as pd
from openpyxl import load_workbook
from settings import ROOT_FOLDER


def convert_xls_to_xlsx(path_to_source, path_to_destination):
    pd.read_excel(path_to_source).to_excel(
        path_to_destination, engine="openpyxl", index=False
    )


def read_xlsx(path_to_xlsx):
    wb = load_workbook(filename=path_to_xlsx)
    sheet = wb.active
    for row in sheet.iter_rows():
        for cell in row:
            print(cell.value, end=" ")
        print()
