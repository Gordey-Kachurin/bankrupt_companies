from settings import FIERFOX_PROFILE_PATH, FOLDERS, PATTERNS_FOR_XLSX_TABLENAME
from utils.webdriver_setup import get_driver
from utils.file_helpers import (
    prepare_excel_files_for_parsing,
    get_file_headers,
    write_errors,
)
from utils.browsing import browse_for_files
import os

if __name__ == "__main__":
    for folder in FOLDERS:
        if not os.path.exists(FOLDERS[folder]):
            os.mkdir(FOLDERS[folder])

    driver = get_driver(FIERFOX_PROFILE_PATH)
    browse_for_files(driver)
    driver.quit()
    prepare_excel_files_for_parsing()
    errors_while_searching = get_file_headers(PATTERNS_FOR_XLSX_TABLENAME)
    write_errors(errors_while_searching)
