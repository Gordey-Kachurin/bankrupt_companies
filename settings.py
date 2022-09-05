from dotenv import load_dotenv
import os
import re
import platform

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

if platform.system() == "Windows":
    FIREFOX_PROFILE_FOLDER = "ht3xghcx.default-release"
    FIERFOX_PROFILE_PATH = os.path.join(
        os.getenv("APPDATA"), "Mozilla", "Firefox", "Profiles", FIREFOX_PROFILE_FOLDER
    )
    ROOT_FOLDER = os.path.join(
        os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop"),
        "Rehabilitation and Bankrupcy",
    )  # TODO: Russian language gives weird errors in foldername

if platform.system() == "Linux":
    FIREFOX_PROFILE_FOLDER = "9h9tufst.default-release"
    FIERFOX_PROFILE_PATH = (
        f"/home/{os.getlogin()}/.mozilla/firefox/{FIREFOX_PROFILE_FOLDER}"
    )
    ROOT_FOLDER = os.path.join(
        os.environ["HOME"], "Desktop", "Rehabilitation and Bankrupcy"
    )

FOLDERS = {
    "root": ROOT_FOLDER,
    "temp": os.path.join(ROOT_FOLDER, "temp"),
    "downloads": os.path.join(ROOT_FOLDER, "downloads"),
    "copies": os.path.join(ROOT_FOLDER, "copies"),
}


PATTERNS = {
    "legal_entities": "Юридическим лицам",
    "rehabilitation_and_bankrupcy": "Реабилитация и банкротство",
    "regex_pattern_for_year": re.compile(r"2[0-9]{3} год"),
    "regex_pattern_for_link": re.compile(r".*depsection.*"),
    "regex_patterns_for_informational_messages": [
        re.compile(r"Информационн[ыо]е сообщени[ея]$"),
        re.compile(r"Информационные сообщение 2019$"),  # Atyrau
        re.compile(r"1-7 Информационные сообщения$"),  # Karaganda since 2019
        re.compile(r"2021 Информационные сообщения$"),  # Mangystau
        re.compile(r"ИНФОРМАЦИОННЫЕ СООБЩЕНИЯ$"),  # Severo-Kazahstanskaya oblast
    ],
    "bankrupcy": "банкротстве",
    "rehabilitation": re.compile(r".*реа(били|либи)тации.*"),
    "litigation": re.compile(r".*возбуждени[ие].*"),
}

REGEX_PATTERNS_FOR_XLSX_HEADERS = {
    "bin": re.compile(r"БИН"),
    "registration": re.compile(r"регистрац"),
    "dolzhnik": re.compile(r"Наименование /Ф.И.О.должника"),
}

PATTERNS_FOR_XLSX_TABLENAME = {
    # On pages in Russian, Excel files may be in Kazakh
    "litigation": [
        re.compile(r".*возбуждени[ие].*"),
        re.compile(r".*іс қозғалғандығы.*"),
        re.compile(r".*іс жүргізуді қозғау.*"),
    ],
}

XPATHS_TO_SEARCH_A_ELEMENTS = [
    "//table/tbody/tr//a",
    "//div[@class='content']//div[@class='field-items']//ul/li/a",
    "//div[@class='content']//div[@class='field-items']//p/a",
]

XPATHS_TO_SEARCH_INFORMATIONAL_MESSAGES = {
    "view-header": "//div[@class='content']/div[contains(@class,'view-taxonomy-term')]/div[@class='view-header']/div[@class='catmenu']/ul[@class='menu']/li/a",
    "view-content": "//div[@class='content']/div[contains(@class,'view-taxonomy-term')]/div[@class='view-content']//h3/a",
}

URLS = {
    "nursultan": "http://nursultan.kgd.gov.kz",
    "almaty": "http://almaty.kgd.gov.kz",
    "shymkent": "http://shymkent.kgd.gov.kz",
    "akm": "http://akm.kgd.gov.kz",
    "akb": "http://akb.kgd.gov.kz",
    "alm": "http://alm.kgd.gov.kz",
    "atr": "http://atr.kgd.gov.kz",
    "vko": "http://vko.kgd.gov.kz",
    "zhmb": "http://zhmb.kgd.gov.kz",
    "zko": "http://zko.kgd.gov.kz",
    "krg": "http://krg.kgd.gov.kz",
    "kst": "http://kst.kgd.gov.kz",
    "kzl": "http://kzl.kgd.gov.kz",
    "mng": "http://mng.kgd.gov.kz",
    "pvl": "http://pvl.kgd.gov.kz",
    "sko": "http://sko.kgd.gov.kz",
    "trk": "http://trk.kgd.gov.kz",
}
