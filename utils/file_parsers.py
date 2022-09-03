import pandas as pd
from openpyxl import load_workbook
import sys
import os
import rarfile

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from settings import REGEX_PATTERNS_FOR_XLSX_HEADERS, ROOT_FOLDER, COPIES_FOLDER, URLS
   

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

if not os.path.exists(COPIES_FOLDER):
        os.mkdir(COPIES_FOLDER)

def get_downloaded_filenames():
    downloads = {}
    for folder in URLS:
        files = os.listdir(os.path.join(ROOT_FOLDER, folder))
        downloads[folder] = files
         
    return downloads

def create_directories_for_copies():
    for region in URLS:
        if not os.path.exists(os.path.join(COPIES_FOLDER, region)):
            os.mkdir(os.path.join(COPIES_FOLDER, region))

def get_non_excel_files(downloads):
    rar_files = {}
    
    for region in downloads:
        files = []
        for f in downloads[region]:
            if f[-4:] == ".rar":
                files.append(f)
            # if f[-4:] == ".xls" or f[-4:] == "xlsx":
            #     continue
            # else:
            #     files.append(f)
        if files != []:        
            rar_files[region] = files
    return rar_files

downloads = get_downloaded_filenames()
create_directories_for_copies()
rar_files = get_non_excel_files(downloads)

# On Linux install sudo apt install unrar
def extract_rar_files(rar_files):
    rar_file_names = []
    for region in rar_files:
        for f_rar in rar_files[region]:
            rf = rarfile.RarFile(os.path.join(ROOT_FOLDER, region, f_rar))
            print(rf.filename)
            rf.extractall(os.path.join(ROOT_FOLDER, region))
             

        
# for region in downloads:
#     print(downloads[region])
#     for f in downloads[region]:
#         convert_xls_to_xlsx(os.path.join(ROOT_FOLDER, region, f), os.path.join(COPIES_FOLDER, region, f))
