import pandas as pd
from openpyxl import load_workbook
from settings import REGEX_PATTERNS_FOR_XLSX_HEADERS


def convert_xls_to_xlsx(path_to_source, path_to_destination):
    pd.read_excel(path_to_source).to_excel(
        path_to_destination, engine="openpyxl", index=False
    )


def get_xlsx_headers_cells(path_to_xlsx):
    wb = load_workbook(filename=path_to_xlsx)
    sheet = wb.active
    xlsx_headers = {}
    for row in sheet.iter_rows():
        for cell in row:
            for key in REGEX_PATTERNS_FOR_XLSX_HEADERS:
                try:
                    if REGEX_PATTERNS_FOR_XLSX_HEADERS[key].match(cell.value):
                        print(cell.coordinate, cell.value)
                        xlsx_headers[key] = cell
                except TypeError:
                    continue
    wb.close()
    return xlsx_headers
