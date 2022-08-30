from dotenv import load_dotenv
import os
import re

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

FIREFOX_PROFILE_FOLDER = "ht3xghcx.default-release"
FIERFOX_PROFILE_PATH = rf"C:\Users\{os.getlogin()}\AppData\Roaming\Mozilla\Firefox\Profiles\{FIREFOX_PROFILE_FOLDER}"


PATTERNS = {
    "legal_entities": "Юридическим лицам",
    "rehabilitation_and_bankrupcy": "Реабилитация и банкротство",
    "regex_pattern_for_year": re.compile(r"2[0-9]{3} год"),
    "regex_pattern_for_link": re.compile(r".*depsection.*"),
    "regex_patterns_for_informational_messages": [
        re.compile(r"Информационные сообщения$")
    ],
    "bankrupcy": "банкротстве",
    "rehabilitation": "реабилитации",
    "litigation": "возбуждении",
}


ROOT_FOLDER = os.path.join(
    os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop"),
    "Rehabilitation and Bankrupcy",
)  # TODO: Russian language gives weird errors in foldername

DOWNLOADS_FOLDER = os.path.join(ROOT_FOLDER, "temp")

URLS = {
    # "nursultan": "http://nursultan.kgd.gov.kz",
    # "almaty": "http://almaty.kgd.gov.kz",
    # "shymkent": "http://shymkent.kgd.gov.kz",
    "akm": "http://akm.kgd.gov.kz",
    # "akb": "http://akb.kgd.gov.kz",
    # "alm": "http://alm.kgd.gov.kz",
    # "atr": "http://atr.kgd.gov.kz",
    # "vko": "http://vko.kgd.gov.kz",
    # "zhmb": "http://zhmb.kgd.gov.kz",
    # "zko": "http://zko.kgd.gov.kz",
    # "krg": "http://krg.kgd.gov.kz",
    # "kst": "http://kst.kgd.gov.kz",
    # "kzl": "http://kzl.kgd.gov.kz",
    # "mng": "http://mng.kgd.gov.kz",
    # "pvl": "http://pvl.kgd.gov.kz",
    # "sko": "http://sko.kgd.gov.kz",
    # "trk": "http://trk.kgd.gov.kz",
}
