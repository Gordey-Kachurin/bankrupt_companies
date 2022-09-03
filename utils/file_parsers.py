import pandas as pd
from openpyxl import load_workbook
import sys
import os
import rarfile
import xlrd

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from settings import (
    REGEX_PATTERNS_FOR_XLSX_HEADERS,
    ROOT_FOLDER,
    COPIES_FOLDER,
    URLS,
    DOWNLOADS_FOLDER,
)
from utils.parsers import rename_and_move
from utils.exceptions import UnexpectedFileExtention


def create_directories_for_copies(downloads):
    for region in downloads:
        if not os.path.exists(os.path.join(COPIES_FOLDER, region)):
            os.mkdir(os.path.join(COPIES_FOLDER, region))


if not os.path.exists(COPIES_FOLDER):
    os.mkdir(COPIES_FOLDER)


def get_downloaded_filenames_by_region():
    downloads = {}
    for folder in URLS:
        try:
            files = os.listdir(os.path.join(ROOT_FOLDER, folder))
        except FileNotFoundError:
            continue
        downloads[folder] = files

    return downloads


def get_regions_files_by_file_extention(downloads, file_extention):
    """
    file_extention examples ".xlsx", ".xls", ".rar"
    """
    regions_files_by_file_extention = {}
    for region in downloads:
        files = []
        for filename in downloads[region]:
            if filename.endswith(file_extention):
                files.append(filename)
        if files != []:
            regions_files_by_file_extention[region] = files
    return regions_files_by_file_extention


# On Linux install unrar: sudo apt install unrar
def extract_rar_files(regions_rar_files):
    rar_file_names = []
    for region in regions_rar_files:
        for rar_filename in regions_rar_files[region]:
            splitted = rar_filename.split()
            year = splitted[1] + " " + splitted[2]
            rf = rarfile.RarFile(os.path.join(ROOT_FOLDER, region, rar_filename))
            print(rf.filename)
            rf.extractall(DOWNLOADS_FOLDER)
            rename_and_move(ROOT_FOLDER, DOWNLOADS_FOLDER, region, year)


def delete_rar_files(region_rar_files):
    for region in region_rar_files:
        for rar_filename in region_rar_files[region]:
            os.remove(os.path.join(ROOT_FOLDER, region, rar_filename))


def convert_xls_to_xlsx(
    path_to_source_file, path_to_destination_file, engine_for_source=None
):
    pd.read_excel(path_to_source_file, engine=engine_for_source).to_excel(
        path_to_destination_file, engine="openpyxl", index=False
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


def copy_files(downloads, engine_for_source=None):
    for region in downloads:
        for filename in downloads[region]:
            print(region, filename)
            if filename.endswith(".xls"):
                new_filename = filename[:-3] + "xlsx"
                try:
                    convert_xls_to_xlsx(
                        os.path.join(ROOT_FOLDER, region, filename),
                        os.path.join(COPIES_FOLDER, region, new_filename),
                        engine_for_source,
                    )
                except xlrd.XLRDError:
                    print(f"Поврежденный файл: {filename}")
                    continue

            elif filename.endswith(".xlsx"):
                convert_xls_to_xlsx(
                    os.path.join(ROOT_FOLDER, region, filename),
                    os.path.join(COPIES_FOLDER, region, filename),
                )
            else:
                raise UnexpectedFileExtention


downloads = get_downloaded_filenames_by_region()
regions_rar_files = get_regions_files_by_file_extention(downloads, ".rar")
extract_rar_files(regions_rar_files)
delete_rar_files(regions_rar_files)
create_directories_for_copies(downloads)

regions_xls_files = get_regions_files_by_file_extention(downloads, ".xls")
regions_xlsx_files = get_regions_files_by_file_extention(downloads, ".xlsx")
regions_ods_files = get_regions_files_by_file_extention(downloads, ".ods")
regions_xlsm_files = get_regions_files_by_file_extention(downloads, ".xlsm")


# copy_files(regions_rar_files)
copy_files(regions_xls_files, engine_for_source="xlrd")
copy_files(regions_xlsx_files, engine_for_source="openpyxl")


# for region in downloads:
#     print(downloads[region])
#     for f in downloads[region]:
#         convert_xls_to_xlsx(os.path.join(ROOT_FOLDER, region, f), os.path.join(COPIES_FOLDER, region, f))
