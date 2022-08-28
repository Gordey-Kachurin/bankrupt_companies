from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# https://stackoverflow.com/questions/1681208/python-platform-independent-way-to-modify-path-environment-variable
os.environ["PATH"] += os.pathsep + os.getcwd()
PATH_TO_FIERFOX_PROFILE = r'C:\Users\admin\AppData\Roaming\Mozilla\Firefox\Profiles\ht3xghcx.default-release'
PATTERNS = {
 'ur_licam' : 'Юридическим лицам'

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
    "trk": "http://trk.kgd.gov.kz"
}