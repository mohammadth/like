from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
import my_pb2
import output_pb2
import json
from colorama import Fore, Style, init
import warnings
from urllib3.exceptions import InsecureRequestWarning
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import schedule
import time
import threading
import asyncio
import aiohttp
from google.protobuf.json_format import MessageToJson
import like_pb2, like_count_pb2, uid_generator_pb2
from google.protobuf.message import DecodeError
import urllib3

# تجاهل تحذيرات SSL
warnings.filterwarnings("ignore", category=InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV = b'6oyZDr22E3ychjM%'

# تهيئة colorama
init(autoreset=True)

# تهيئة تطبيق FastAPI
app = FastAPI()

# تخزين البيانات في الذاكرة
responses_cache = []

# ✅ الحسابات مخزنة مباشرة في الكود
ACCOUNTS = [
    {
        "uid": "4255940428",
        "password": "BY_PARAHEX-WRWPKQA85-REDZED"
    },
    {
        "uid": "4255940653",
        "password": "BY_PARAHEX-OXHPSZMBA-REDZED"
    },
    {
        "uid": "4255941935",
        "password": "BY_PARAHEX-EFAMB9AW1-REDZED"
    },
    {
        "uid": "4255942486",
        "password": "BY_PARAHEX-NV5RRK9N3-REDZED"
    },
    {
        "uid": "4255942729",
        "password": "BY_PARAHEX-RQLK69ZUI-REDZED"
    },
    {
        "uid": "4255944114",
        "password": "BY_PARAHEX-0CPFH5PEY-REDZED"
    },
    {
        "uid": "4255945120",
        "password": "BY_PARAHEX-EL1QQ8N0W-REDZED"
    },
    {
        "uid": "4255945724",
        "password": "BY_PARAHEX-CSVHRTM10-REDZED"
    },
    {
        "uid": "4255946421",
        "password": "BY_PARAHEX-NMPTTVNB6-REDZED"
    },
    {
        "uid": "4255947367",
        "password": "BY_PARAHEX-MGHO5OMZY-REDZED"
    },
    {
        "uid": "4255948743",
        "password": "BY_PARAHEX-3OXCMKJBO-REDZED"
    },
    {
        "uid": "4255948921",
        "password": "BY_PARAHEX-8OSOJ8I5X-REDZED"
    },
    {
        "uid": "4255949533",
        "password": "BY_PARAHEX-9GAYKWSS2-REDZED"
    },
    {
        "uid": "4255949801",
        "password": "BY_PARAHEX-6LZCTKVXL-REDZED"
    },
    {
        "uid": "4255950584",
        "password": "BY_PARAHEX-1IBHHUJKJ-REDZED"
    },
    {
        "uid": "4255950769",
        "password": "BY_PARAHEX-QQTQ5SVQI-REDZED"
    },
    {
        "uid": "4255950939",
        "password": "BY_PARAHEX-HG7QPPFCS-REDZED"
    },
    {
        "uid": "4255951951",
        "password": "BY_PARAHEX-LS9IRQ64Q-REDZED"
    },
    {
        "uid": "4255952850",
        "password": "BY_PARAHEX-QJPRTJI2Q-REDZED"
    },
    {
        "uid": "4255953437",
        "password": "BY_PARAHEX-EMAU3RTUG-REDZED"
    },
    {
        "uid": "4255954524",
        "password": "BY_PARAHEX-PMKDUKJHR-REDZED"
    },
    {
        "uid": "4255955364",
        "password": "BY_PARAHEX-MQHKDW7E1-REDZED"
    },
    {
        "uid": "4255956274",
        "password": "BY_PARAHEX-ZQGBW202D-REDZED"
    },
    {
        "uid": "4255956404",
        "password": "BY_PARAHEX-QHYRSVAQK-REDZED"
    },
    {
        "uid": "4255956941",
        "password": "BY_PARAHEX-IZJX8GND3-REDZED"
    },
    {
        "uid": "4255957140",
        "password": "BY_PARAHEX-6EIROK9TO-REDZED"
    },
    {
        "uid": "4255958166",
        "password": "BY_PARAHEX-EWDOY1DD6-REDZED"
    },
    {
        "uid": "4255959357",
        "password": "BY_PARAHEX-NE0LK1IBY-REDZED"
    },
    {
        "uid": "4255960160",
        "password": "BY_PARAHEX-5AW9COPXD-REDZED"
    },
    {
        "uid": "4255960888",
        "password": "BY_PARAHEX-1QAEPAD5P-REDZED"
    },
    {
        "uid": "4255962773",
        "password": "BY_PARAHEX-JCKMSTBRA-REDZED"
    },
    {
        "uid": "4255964311",
        "password": "BY_PARAHEX-BOTUATMBC-REDZED"
    },
    {
        "uid": "4255964523",
        "password": "BY_PARAHEX-ZF9YMOXTC-REDZED"
    },
    {
        "uid": "4255965395",
        "password": "BY_PARAHEX-MNPFOODUT-REDZED"
    },
    {
        "uid": "4255966078",
        "password": "BY_PARAHEX-HPBGG4GOB-REDZED"
    },
    {
        "uid": "4255967493",
        "password": "BY_PARAHEX-XGWJS9ZEC-REDZED"
    },
    {
        "uid": "4255967769",
        "password": "BY_PARAHEX-NH4WVYSI5-REDZED"
    },
    {
        "uid": "4255968554",
        "password": "BY_PARAHEX-3H2HAL1AY-REDZED"
    },
    {
        "uid": "4255968760",
        "password": "BY_PARAHEX-QNDBLUJJ2-REDZED"
    },
    {
        "uid": "4255968896",
        "password": "BY_PARAHEX-UGH4SDKCQ-REDZED"
    },
    {
        "uid": "4255969408",
        "password": "BY_PARAHEX-IEWAFVIKW-REDZED"
    },
    {
        "uid": "4255973168",
        "password": "BY_PARAHEX-SR4FEJZFO-REDZED"
    },
    {
        "uid": "4255973579",
        "password": "BY_PARAHEX-ZQFLBPSBG-REDZED"
    },
    {
        "uid": "4255974099",
        "password": "BY_PARAHEX-YICLTKKPK-REDZED"
    },
    {
        "uid": "4255974573",
        "password": "BY_PARAHEX-HF9NLOURX-REDZED"
    },
    {
        "uid": "4255974950",
        "password": "BY_PARAHEX-R42WEJSLT-REDZED"
    },
    {
        "uid": "4255976059",
        "password": "BY_PARAHEX-R3JLDGK4D-REDZED"
    },
    {
        "uid": "4255978040",
        "password": "BY_PARAHEX-9VLGXOR09-REDZED"
    },
    {
        "uid": "4255979116",
        "password": "BY_PARAHEX-CFO6KSTOE-REDZED"
    },
    {
        "uid": "4255980143",
        "password": "BY_PARAHEX-PWNSTPWJE-REDZED"
    },
    {
        "uid": "4255981403",
        "password": "BY_PARAHEX-D7CPSIXZI-REDZED"
    },
    {
        "uid": "4255981756",
        "password": "BY_PARAHEX-VPTEE8TS4-REDZED"
    },
    {
        "uid": "4255986038",
        "password": "BY_PARAHEX-ZYSLNEL2B-REDZED"
    },
    {
        "uid": "4255987242",
        "password": "BY_PARAHEX-WIVUC3DL6-REDZED"
    },
    {
        "uid": "4255987644",
        "password": "BY_PARAHEX-EOAYFQ5MA-REDZED"
    },
    {
        "uid": "4255988014",
        "password": "BY_PARAHEX-6EIBWL7FY-REDZED"
    },
    {
        "uid": "4255988404",
        "password": "BY_PARAHEX-ETYHIWHUN-REDZED"
    },
    {
        "uid": "4255989538",
        "password": "BY_PARAHEX-3FVMFP91E-REDZED"
    },
    {
        "uid": "4255990025",
        "password": "BY_PARAHEX-PPDPPDQXN-REDZED"
    },
    {
        "uid": "4255990444",
        "password": "BY_PARAHEX-2VUBFFOOZ-REDZED"
    },
    {
        "uid": "4255991879",
        "password": "BY_PARAHEX-RAJST9JK9-REDZED"
    },
    {
        "uid": "4255992755",
        "password": "BY_PARAHEX-XMWBKSHGQ-REDZED"
    },
    {
        "uid": "4255993415",
        "password": "BY_PARAHEX-KQIDXS4CR-REDZED"
    },
    {
        "uid": "4255993997",
        "password": "BY_PARAHEX-YHLFPKUBI-REDZED"
    },
    {
        "uid": "4255996107",
        "password": "BY_PARAHEX-HACMY7R9L-REDZED"
    },
    {
        "uid": "4255997339",
        "password": "BY_PARAHEX-QJ0RF4XFR-REDZED"
    },
    {
        "uid": "4255998686",
        "password": "BY_PARAHEX-PQH9BIZ6T-REDZED"
    },
    {
        "uid": "4255999373",
        "password": "BY_PARAHEX-33DLSDFYI-REDZED"
    },
    {
        "uid": "4255999913",
        "password": "BY_PARAHEX-0VKEMOSPQ-REDZED"
    },
    {
        "uid": "4256001185",
        "password": "BY_PARAHEX-5J5TJN86X-REDZED"
    },
    {
        "uid": "4256004209",
        "password": "BY_PARAHEX-IM69YTPUO-REDZED"
    },
    {
        "uid": "4256004686",
        "password": "BY_PARAHEX-PSZHTDQ21-REDZED"
    },
    {
        "uid": "4256006465",
        "password": "BY_PARAHEX-0E9DJDLKI-REDZED"
    },
    {
        "uid": "4256006926",
        "password": "BY_PARAHEX-NT13SGBE0-REDZED"
    },
    {
        "uid": "4256008088",
        "password": "BY_PARAHEX-E9SFFM37R-REDZED"
    },
    {
        "uid": "4256009134",
        "password": "BY_PARAHEX-YDSVTULMN-REDZED"
    },
    {
        "uid": "4256010404",
        "password": "BY_PARAHEX-P3XM4VP6D-REDZED"
    },
    {
        "uid": "4256010829",
        "password": "BY_PARAHEX-X2LSNDUAB-REDZED"
    },
    {
        "uid": "4256012723",
        "password": "BY_PARAHEX-JVURAM0FQ-REDZED"
    },
    {
        "uid": "4256013837",
        "password": "BY_PARAHEX-50NSZSRM0-REDZED"
    },
    {
        "uid": "4256014198",
        "password": "BY_PARAHEX-OFO7GX3EC-REDZED"
    },
    {
        "uid": "4256014568",
        "password": "BY_PARAHEX-POJWOYDC9-REDZED"
    },
    {
        "uid": "4256014915",
        "password": "BY_PARAHEX-TZ3RC5X57-REDZED"
    },
    {
        "uid": "4256016070",
        "password": "BY_PARAHEX-GGSGDYNCL-REDZED"
    },
    {
        "uid": "4256016404",
        "password": "BY_PARAHEX-OPVOZRAGO-REDZED"
    },
    {
        "uid": "4256017520",
        "password": "BY_PARAHEX-FYNRHOIAS-REDZED"
    },
    {
        "uid": "4256017848",
        "password": "BY_PARAHEX-MAV7YS5MB-REDZED"
    },
    {
        "uid": "4256019011",
        "password": "BY_PARAHEX-JUS0BADDN-REDZED"
    },
    {
        "uid": "4256020024",
        "password": "BY_PARAHEX-D2VAW886S-REDZED"
    },
    {
        "uid": "4256022557",
        "password": "BY_PARAHEX-JLFYFWTGF-REDZED"
    },
    {
        "uid": "4256022917",
        "password": "BY_PARAHEX-UWOZYMMSI-REDZED"
    },
    {
        "uid": "4256023298",
        "password": "BY_PARAHEX-ZHDCBVALR-REDZED"
    },
    {
        "uid": "4256023753",
        "password": "BY_PARAHEX-38GZDJFGU-REDZED"
    },
    {
        "uid": "4256024255",
        "password": "BY_PARAHEX-O2EYNS6HY-REDZED"
    },
    {
        "uid": "4256025369",
        "password": "BY_PARAHEX-01QFV7RYB-REDZED"
    },
    {
        "uid": "4256025729",
        "password": "BY_PARAHEX-BTSROW9QT-REDZED"
    },
    {
        "uid": "4256027576",
        "password": "BY_PARAHEX-QS9D3GXCQ-REDZED"
    },
    {
        "uid": "4256029647",
        "password": "BY_PARAHEX-SBAZNOKYX-REDZED"
    },
    {
        "uid": "4256030034",
        "password": "BY_PARAHEX-YCSDQEVLL-REDZED"
    },
    {
        "uid": "4256031262",
        "password": "BY_PARAHEX-XMOJSJAKL-REDZED"
    },
    {
        "uid": "4256032413",
        "password": "BY_PARAHEX-NH3DNOQHL-REDZED"
    },
    {
        "uid": "4256033856",
        "password": "BY_PARAHEX-XRAI71JWJ-REDZED"
    },
    {
        "uid": "4256035620",
        "password": "BY_PARAHEX-FDHI7B1HF-REDZED"
    },
    {
        "uid": "4256036588",
        "password": "BY_PARAHEX-SXBNRHX6W-REDZED"
    },
    {
        "uid": "4256037809",
        "password": "BY_PARAHEX-VQ8KIKH2C-REDZED"
    },
    {
        "uid": "4256038096",
        "password": "BY_PARAHEX-M1GX5CVTB-REDZED"
    },
    {
        "uid": "4256039120",
        "password": "BY_PARAHEX-KGBXAVTBP-REDZED"
    },
    {
        "uid": "4256041576",
        "password": "BY_PARAHEX-FZX5UQC9V-REDZED"
    },
    {
        "uid": "4256041886",
        "password": "BY_PARAHEX-T6L4EEHXP-REDZED"
    },
    {
        "uid": "4256043239",
        "password": "BY_PARAHEX-4NCAZ128P-REDZED"
    },
    {
        "uid": "4256043597",
        "password": "BY_PARAHEX-LA3INMLOL-REDZED"
    },
    {
        "uid": "4256044582",
        "password": "BY_PARAHEX-RORKNTQ4X-REDZED"
    },
    {
        "uid": "4256045617",
        "password": "BY_PARAHEX-6TFWVHI1M-REDZED"
    },
    {
        "uid": "4256046627",
        "password": "BY_PARAHEX-BA5WFWAHC-REDZED"
    },
    {
        "uid": "4256047005",
        "password": "BY_PARAHEX-3WJQGP9G6-REDZED"
    },
    {
        "uid": "4256048341",
        "password": "BY_PARAHEX-YNQGTRHOS-REDZED"
    },
    {
        "uid": "4256048670",
        "password": "BY_PARAHEX-AZVNHQ4LL-REDZED"
    },
    {
        "uid": "4256049962",
        "password": "BY_PARAHEX-WQNFJCDNM-REDZED"
    },
    {
        "uid": "4256051181",
        "password": "BY_PARAHEX-EHN8S6PM3-REDZED"
    },
    {
        "uid": "4256052782",
        "password": "BY_PARAHEX-EWNXYMYQT-REDZED"
    },
    {
        "uid": "4256054595",
        "password": "BY_PARAHEX-XOCI9VNZZ-REDZED"
    },
    {
        "uid": "4256055700",
        "password": "BY_PARAHEX-LJMVCUBSG-REDZED"
    },
    {
        "uid": "4256057556",
        "password": "BY_PARAHEX-3XC2INKGD-REDZED"
    },
    {
        "uid": "4256059274",
        "password": "BY_PARAHEX-ZPTQZT0AQ-REDZED"
    },
    {
        "uid": "4256060248",
        "password": "BY_PARAHEX-SLXEO14HB-REDZED"
    },
    {
        "uid": "4256061201",
        "password": "BY_PARAHEX-NU0WAPWII-REDZED"
    },
    {
        "uid": "4256063130",
        "password": "BY_PARAHEX-Y8DTL85SW-REDZED"
    },
    {
        "uid": "4256063566",
        "password": "BY_PARAHEX-KTWAXHNN2-REDZED"
    },
    {
        "uid": "4256063952",
        "password": "BY_PARAHEX-2PUNCVAUJ-REDZED"
    },
    {
        "uid": "4256064604",
        "password": "BY_PARAHEX-8PMEZSCNA-REDZED"
    },
    {
        "uid": "4256064948",
        "password": "BY_PARAHEX-UISODMNVF-REDZED"
    },
    {
        "uid": "4256066748",
        "password": "BY_PARAHEX-NTBLWMAJH-REDZED"
    },
    {
        "uid": "4256068045",
        "password": "BY_PARAHEX-ESP32IPKV-REDZED"
    },
    {
        "uid": "4256070883",
        "password": "BY_PARAHEX-K1Q068TGQ-REDZED"
    },
    {
        "uid": "4256072196",
        "password": "BY_PARAHEX-W6XLIN0DS-REDZED"
    },
    {
        "uid": "4256074210",
        "password": "BY_PARAHEX-SHBTTOXRF-REDZED"
    },
    {
        "uid": "4256075777",
        "password": "BY_PARAHEX-H0HKNUSG1-REDZED"
    },
    {
        "uid": "4256077049",
        "password": "BY_PARAHEX-IAMSPG2HM-REDZED"
    },
    {
        "uid": "4256077921",
        "password": "BY_PARAHEX-YUYZZ39HU-REDZED"
    },
    {
        "uid": "4256079143",
        "password": "BY_PARAHEX-C2T6BCBBC-REDZED"
    },
    {
        "uid": "4256081707",
        "password": "BY_PARAHEX-QCGKYJX0B-REDZED"
    },
    {
        "uid": "4256082431",
        "password": "BY_PARAHEX-THKFDWRDJ-REDZED"
    },
    {
        "uid": "4256083727",
        "password": "BY_PARAHEX-0CBPD9WKF-REDZED"
    },
    {
        "uid": "4256084935",
        "password": "BY_PARAHEX-KANX9ZMNQ-REDZED"
    },
    {
        "uid": "4256085529",
        "password": "BY_PARAHEX-P4MNEHTZT-REDZED"
    },
    {
        "uid": "4256086548",
        "password": "BY_PARAHEX-AAUPLZZYT-REDZED"
    },
    {
        "uid": "4256087764",
        "password": "BY_PARAHEX-OCOA89SBF-REDZED"
    },
    {
        "uid": "4256088414",
        "password": "BY_PARAHEX-7VDUFZDOB-REDZED"
    },
    {
        "uid": "4256088794",
        "password": "BY_PARAHEX-TNMWJZWUD-REDZED"
    },
    {
        "uid": "4256090042",
        "password": "BY_PARAHEX-HLYVDCFYH-REDZED"
    },
    {
        "uid": "4256090422",
        "password": "BY_PARAHEX-U3HOY6A0W-REDZED"
    },
    {
        "uid": "4256091497",
        "password": "BY_PARAHEX-AXHTL2EWB-REDZED"
    },
    {
        "uid": "4256092744",
        "password": "BY_PARAHEX-UJWOXYWK7-REDZED"
    },
    {
        "uid": "4256094721",
        "password": "BY_PARAHEX-PYYTCRDA1-REDZED"
    },
    {
        "uid": "4256095227",
        "password": "BY_PARAHEX-48G22JFW9-REDZED"
    },
    {
        "uid": "4256096320",
        "password": "BY_PARAHEX-N5ACWTZLM-REDZED"
    },
    {
        "uid": "4256098100",
        "password": "BY_PARAHEX-JCF9DZUNS-REDZED"
    },
    {
        "uid": "4256098564",
        "password": "BY_PARAHEX-3QKROMAJ9-REDZED"
    },
    {
        "uid": "4256100319",
        "password": "BY_PARAHEX-NWC9VLR8E-REDZED"
    },
    {
        "uid": "4256103956",
        "password": "BY_PARAHEX-TE8GSTKZP-REDZED"
    },
    {
        "uid": "4256105814",
        "password": "BY_PARAHEX-68LDKPYKP-REDZED"
    },
    {
        "uid": "4256106970",
        "password": "BY_PARAHEX-B8JBLWBDI-REDZED"
    },
    {
        "uid": "4256107809",
        "password": "BY_PARAHEX-BIJVHHPHU-REDZED"
    },
    {
        "uid": "4256108496",
        "password": "BY_PARAHEX-Y6EYFCL3F-REDZED"
    },
    {
        "uid": "4256110381",
        "password": "BY_PARAHEX-ZRFAVH4T0-REDZED"
    },
    {
        "uid": "4256110955",
        "password": "BY_PARAHEX-2DYPZCZ2A-REDZED"
    },
    {
        "uid": "4256112263",
        "password": "BY_PARAHEX-ZCISBY7JU-REDZED"
    },
    {
        "uid": "4256112812",
        "password": "BY_PARAHEX-RS26SYK0H-REDZED"
    },
    {
        "uid": "4256114864",
        "password": "BY_PARAHEX-H8PAOQC4C-REDZED"
    },
    {
        "uid": "4256115282",
        "password": "BY_PARAHEX-BI0PASMTP-REDZED"
    },
    {
        "uid": "4256115958",
        "password": "BY_PARAHEX-ABJ3SED9G-REDZED"
    },
    {
        "uid": "4256116703",
        "password": "BY_PARAHEX-PABUWJ5LH-REDZED"
    },
    {
        "uid": "4256117344",
        "password": "BY_PARAHEX-LUQNMDLCM-REDZED"
    },
    {
        "uid": "4256118629",
        "password": "BY_PARAHEX-FLBQPDOMU-REDZED"
    },
    {
        "uid": "4256119151",
        "password": "BY_PARAHEX-JU462S8EV-REDZED"
    },
    {
        "uid": "4256119904",
        "password": "BY_PARAHEX-KEJOK5AMD-REDZED"
    },
    {
        "uid": "4256122265",
        "password": "BY_PARAHEX-N8IPJED2H-REDZED"
    },
    {
        "uid": "4256123909",
        "password": "BY_PARAHEX-8FIPQSZAE-REDZED"
    },
    {
        "uid": "4256125100",
        "password": "BY_PARAHEX-YBKBGRNOT-REDZED"
    },
    {
        "uid": "4256125506",
        "password": "BY_PARAHEX-L3HMHRPV4-REDZED"
    },
    {
        "uid": "4256125906",
        "password": "BY_PARAHEX-23BQHAARK-REDZED"
    },
    {
        "uid": "4256127139",
        "password": "BY_PARAHEX-PJSD0UO5A-REDZED"
    },
    {
        "uid": "4256127664",
        "password": "BY_PARAHEX-QJVTMVUXH-REDZED"
    },
    {
        "uid": "4256128670",
        "password": "BY_PARAHEX-LO3DS3XZL-REDZED"
    },
    {
        "uid": "4256129868",
        "password": "BY_PARAHEX-5RNA8V9EW-REDZED"
    },
    {
        "uid": "4256130446",
        "password": "BY_PARAHEX-K33250WSD-REDZED"
    },
    {
        "uid": "4256131595",
        "password": "BY_PARAHEX-E6LMWISGE-REDZED"
    },
    {
        "uid": "4256132602",
        "password": "BY_PARAHEX-PLXMOPVYD-REDZED"
    },
    {
        "uid": "4256133167",
        "password": "BY_PARAHEX-6R2CNOICD-REDZED"
    },
    {
        "uid": "4256135302",
        "password": "BY_PARAHEX-JX4TCWW6M-REDZED"
    },
    {
        "uid": "4256135732",
        "password": "BY_PARAHEX-WZDOLUJ4Q-REDZED"
    },
    {
        "uid": "4256136141",
        "password": "BY_PARAHEX-EFHDYQQIQ-REDZED"
    },
    {
        "uid": "4256136528",
        "password": "BY_PARAHEX-YYMFDOMUN-REDZED"
    },
    {
        "uid": "4256136929",
        "password": "BY_PARAHEX-CQZRQTFDL-REDZED"
    },
    {
        "uid": "4256137551",
        "password": "BY_PARAHEX-8TQGEJJ9S-REDZED"
    },
    {
        "uid": "4256139302",
        "password": "BY_PARAHEX-HLPNCFG1F-REDZED"
    },
    {
        "uid": "4256139976",
        "password": "BY_PARAHEX-Y11YWRRRJ-REDZED"
    },
    {
        "uid": "4256141073",
        "password": "BY_PARAHEX-66V76ULH5-REDZED"
    },
    {
        "uid": "4256142390",
        "password": "BY_PARAHEX-2NIMX408M-REDZED"
    },
    {
        "uid": "4256144199",
        "password": "BY_PARAHEX-5JUUWGEJA-REDZED"
    },
    {
        "uid": "4256145785",
        "password": "BY_PARAHEX-MDBQ5RETW-REDZED"
    },
    {
        "uid": "4256146988",
        "password": "BY_PARAHEX-6AQKVCITR-REDZED"
    },
    {
        "uid": "4256147712",
        "password": "BY_PARAHEX-751LJDHXP-REDZED"
    },
    {
        "uid": "4256148332",
        "password": "BY_PARAHEX-JWMGOYVA6-REDZED"
    },
    {
        "uid": "4256148986",
        "password": "BY_PARAHEX-EEJYPBWZK-REDZED"
    },
    {
        "uid": "4256150081",
        "password": "BY_PARAHEX-2W3DFWPFO-REDZED"
    },
    {
        "uid": "4256150574",
        "password": "BY_PARAHEX-CHVMCV1W7-REDZED"
    },
    {
        "uid": "4256150932",
        "password": "BY_PARAHEX-28OM1EBUB-REDZED"
    },
    {
        "uid": "4256151865",
        "password": "BY_PARAHEX-C0S5WZKFQ-REDZED"
    },
    {
        "uid": "4256153673",
        "password": "BY_PARAHEX-Y5OJMMZMW-REDZED"
    },
    {
        "uid": "4256154203",
        "password": "BY_PARAHEX-0RAJNENON-REDZED"
    },
    {
        "uid": "4256154603",
        "password": "BY_PARAHEX-GDWDNSRHW-REDZED"
    },
    {
        "uid": "4256155304",
        "password": "BY_PARAHEX-4YOXDY3GH-REDZED"
    },
    {
        "uid": "4256156346",
        "password": "BY_PARAHEX-LROMEQR8Z-REDZED"
    },
    {
        "uid": "4256157842",
        "password": "BY_PARAHEX-QBUNKFGBJ-REDZED"
    },
    {
        "uid": "4256158325",
        "password": "BY_PARAHEX-FXIANZJMM-REDZED"
    },
    {
        "uid": "4256158860",
        "password": "BY_PARAHEX-OB9DFW9HX-REDZED"
    },
    {
        "uid": "4256161404",
        "password": "BY_PARAHEX-HMHCSX0NO-REDZED"
    },
    {
        "uid": "4256161857",
        "password": "BY_PARAHEX-JGFGRPCLX-REDZED"
    },
    {
        "uid": "4256162264",
        "password": "BY_PARAHEX-OMOHVHR5G-REDZED"
    },
    {
        "uid": "4256164063",
        "password": "BY_PARAHEX-GY9FGFCMQ-REDZED"
    },
    {
        "uid": "4256164421",
        "password": "BY_PARAHEX-NXDR5AXEY-REDZED"
    },
    {
        "uid": "4256164852",
        "password": "BY_PARAHEX-RXBR3GUEP-REDZED"
    },
    {
        "uid": "4256165360",
        "password": "BY_PARAHEX-A7LHIZ0XW-REDZED"
    },
    {
        "uid": "4256166510",
        "password": "BY_PARAHEX-DDEJ6HLLS-REDZED"
    },
    {
        "uid": "4256167748",
        "password": "BY_PARAHEX-WBFI9ORDL-REDZED"
    },
    {
        "uid": "4256169568",
        "password": "BY_PARAHEX-G3WEFXHO8-REDZED"
    },
    {
        "uid": "4256170097",
        "password": "BY_PARAHEX-TIDUERBAG-REDZED"
    },
    {
        "uid": "4256172150",
        "password": "BY_PARAHEX-TCBQJ0JWL-REDZED"
    },
    {
        "uid": "4256172643",
        "password": "BY_PARAHEX-8NUYKDLAC-REDZED"
    },
    {
        "uid": "4256173069",
        "password": "BY_PARAHEX-2PIRPYJWH-REDZED"
    },
    {
        "uid": "4256174104",
        "password": "BY_PARAHEX-RNYRFSZVV-REDZED"
    },
    {
        "uid": "4256174700",
        "password": "BY_PARAHEX-BPSQDI1AO-REDZED"
    },
    {
        "uid": "4256175790",
        "password": "BY_PARAHEX-FMBIAS7TP-REDZED"
    },
    {
        "uid": "4256178583",
        "password": "BY_PARAHEX-WZWIMQCYF-REDZED"
    },
    {
        "uid": "4256178974",
        "password": "BY_PARAHEX-Q3MS9KKEK-REDZED"
    },
    {
        "uid": "4256179446",
        "password": "BY_PARAHEX-IWMLE9BGL-REDZED"
    },
    {
        "uid": "4256179977",
        "password": "BY_PARAHEX-POZISBZOP-REDZED"
    },
    {
        "uid": "4256182727",
        "password": "BY_PARAHEX-MA6HIAC7F-REDZED"
    },
    {
        "uid": "4256185008",
        "password": "BY_PARAHEX-90AGR87KB-REDZED"
    },
    {
        "uid": "4256186275",
        "password": "BY_PARAHEX-UJLQHJORU-REDZED"
    },
    {
        "uid": "4256188009",
        "password": "BY_PARAHEX-HY3WNPT2W-REDZED"
    },
    {
        "uid": "4256189382",
        "password": "BY_PARAHEX-VCBB9VPX8-REDZED"
    },
    {
        "uid": "4256190825",
        "password": "BY_PARAHEX-YSHUQMKQW-REDZED"
    },
    {
        "uid": "4256191785",
        "password": "BY_PARAHEX-REO90F6NB-REDZED"
    },
    {
        "uid": "4256193669",
        "password": "BY_PARAHEX-2TWROV0YE-REDZED"
    },
    {
        "uid": "4256195048",
        "password": "BY_PARAHEX-JGYXWBEAQ-REDZED"
    },
    {
        "uid": "4256195930",
        "password": "BY_PARAHEX-JXKNZO7RD-REDZED"
    },
    {
        "uid": "4256196843",
        "password": "BY_PARAHEX-MNWEEMJZQ-REDZED"
    },
    {
        "uid": "4256197508",
        "password": "BY_PARAHEX-CDQ1N2MRQ-REDZED"
    },
    {
        "uid": "4256197927",
        "password": "BY_PARAHEX-ZUB4WCHTD-REDZED"
    },
    {
        "uid": "4256200251",
        "password": "BY_PARAHEX-DWBP3KWHC-REDZED"
    },
    {
        "uid": "4256201406",
        "password": "BY_PARAHEX-HQGUQTYZ1-REDZED"
    },
    {
        "uid": "4256203029",
        "password": "BY_PARAHEX-26OYHVREF-REDZED"
    },
    {
        "uid": "4256204977",
        "password": "BY_PARAHEX-ISDXLUKPB-REDZED"
    },
    {
        "uid": "4256205535",
        "password": "BY_PARAHEX-X6VSLN9VA-REDZED"
    },
    {
        "uid": "4256206678",
        "password": "BY_PARAHEX-WHMWPNADJ-REDZED"
    },
    {
        "uid": "4256208061",
        "password": "BY_PARAHEX-5CBHSIM7V-REDZED"
    },
    {
        "uid": "4256208474",
        "password": "BY_PARAHEX-M0UHTI7VX-REDZED"
    },
    {
        "uid": "4256209025",
        "password": "BY_PARAHEX-2QYGDPTUZ-REDZED"
    },
    {
        "uid": "4256210873",
        "password": "BY_PARAHEX-RXOWEUBPV-REDZED"
    },
    {
        "uid": "4256211275",
        "password": "BY_PARAHEX-YZ7VWF46U-REDZED"
    },
    {
        "uid": "4256212493",
        "password": "BY_PARAHEX-PZYQTPNAV-REDZED"
    },
    {
        "uid": "4256214287",
        "password": "BY_PARAHEX-V2522UXWI-REDZED"
    },
    {
        "uid": "4256214850",
        "password": "BY_PARAHEX-Q9XL4ELCU-REDZED"
    },
    {
        "uid": "4256215975",
        "password": "BY_PARAHEX-V38RBSJ4R-REDZED"
    },
    {
        "uid": "4256216366",
        "password": "BY_PARAHEX-KQUCYTQOI-REDZED"
    },
    {
        "uid": "4256217426",
        "password": "BY_PARAHEX-CBY0PHHMW-REDZED"
    },
    {
        "uid": "4256219200",
        "password": "BY_PARAHEX-FTXG815JF-REDZED"
    },
    {
        "uid": "4256221092",
        "password": "BY_PARAHEX-WNQ9QXSJX-REDZED"
    },
    {
        "uid": "4256221617",
        "password": "BY_PARAHEX-DRRYNEWLS-REDZED"
    },
    {
        "uid": "4256222668",
        "password": "BY_PARAHEX-EFUR8YFG2-REDZED"
    },
    {
        "uid": "4256223122",
        "password": "BY_PARAHEX-X7VOKSI4P-REDZED"
    },
    {
        "uid": "4256223523",
        "password": "BY_PARAHEX-NOABVPB6V-REDZED"
    },
    {
        "uid": "4256224036",
        "password": "BY_PARAHEX-VJHJSBBLV-REDZED"
    },
    {
        "uid": "4256226245",
        "password": "BY_PARAHEX-QWLI8XXBZ-REDZED"
    },
    {
        "uid": "4256226727",
        "password": "BY_PARAHEX-9RR7EMNBY-REDZED"
    },
    {
        "uid": "4256227900",
        "password": "BY_PARAHEX-LMC1SNWVF-REDZED"
    },
    {
        "uid": "4256230151",
        "password": "BY_PARAHEX-8XE1G1Y8M-REDZED"
    },
    {
        "uid": "4256230643",
        "password": "BY_PARAHEX-NEJSJ3IO5-REDZED"
    },
    {
        "uid": "4256231039",
        "password": "BY_PARAHEX-N3UFRM8IK-REDZED"
    },
    {
        "uid": "4256234757",
        "password": "BY_PARAHEX-0BAC17LLE-REDZED"
    },
    {
        "uid": "4256235324",
        "password": "BY_PARAHEX-SG0KPLTSF-REDZED"
    },
    {
        "uid": "4256236641",
        "password": "BY_PARAHEX-WG9HLG619-REDZED"
    },
    {
        "uid": "4256237160",
        "password": "BY_PARAHEX-6ZLOMTUAU-REDZED"
    },
    {
        "uid": "4256238408",
        "password": "BY_PARAHEX-MVMYZMVJ5-REDZED"
    },
    {
        "uid": "4256240312",
        "password": "BY_PARAHEX-I5X85V49Z-REDZED"
    },
    {
        "uid": "4256240762",
        "password": "BY_PARAHEX-BYZWBAYMZ-REDZED"
    },
    {
        "uid": "4256243605",
        "password": "BY_PARAHEX-X9YU0I5TS-REDZED"
    },
    {
        "uid": "4256244220",
        "password": "BY_PARAHEX-LTUQXSZOO-REDZED"
    },
    {
        "uid": "4256245540",
        "password": "BY_PARAHEX-Z93RL8G96-REDZED"
    },
    {
        "uid": "4256246651",
        "password": "BY_PARAHEX-8FZV9ZE0M-REDZED"
    },
    {
        "uid": "4256247361",
        "password": "BY_PARAHEX-BMJLG0H8J-REDZED"
    },
    {
        "uid": "4256248328",
        "password": "BY_PARAHEX-BS72Y0VG5-REDZED"
    },
    {
        "uid": "4256249481",
        "password": "BY_PARAHEX-YOWXGXAU3-REDZED"
    },
    {
        "uid": "4256249903",
        "password": "BY_PARAHEX-LNTDF8KU2-REDZED"
    },
    {
        "uid": "4256250939",
        "password": "BY_PARAHEX-TQXEHC8UI-REDZED"
    },
    {
        "uid": "4256252282",
        "password": "BY_PARAHEX-QUCCQQYLZ-REDZED"
    },
    {
        "uid": "4256253176",
        "password": "BY_PARAHEX-CNLWNUUWC-REDZED"
    },
    {
        "uid": "4256255116",
        "password": "BY_PARAHEX-FLJ1AB5BR-REDZED"
    },
    {
        "uid": "4256256454",
        "password": "BY_PARAHEX-YQHO4NEQC-REDZED"
    },
    {
        "uid": "4256257481",
        "password": "BY_PARAHEX-3UQYNDV51-REDZED"
    },
    {
        "uid": "4256258564",
        "password": "BY_PARAHEX-IEIPVREOW-REDZED"
    },
    {
        "uid": "4256259746",
        "password": "BY_PARAHEX-3URGSOLJE-REDZED"
    },
    {
        "uid": "4256260948",
        "password": "BY_PARAHEX-X3TFUOJA2-REDZED"
    },
    {
        "uid": "4256261685",
        "password": "BY_PARAHEX-LHHHOZM2P-REDZED"
    },
    {
        "uid": "4256262073",
        "password": "BY_PARAHEX-UPVEGKVBL-REDZED"
    },
    {
        "uid": "4256262520",
        "password": "BY_PARAHEX-AQMCGWVBK-REDZED"
    },
    {
        "uid": "4256263268",
        "password": "BY_PARAHEX-XCWHC1HO9-REDZED"
    },
    {
        "uid": "4256264416",
        "password": "BY_PARAHEX-GX8VZLWXK-REDZED"
    },
    {
        "uid": "4256265559",
        "password": "BY_PARAHEX-9RNNITDGW-REDZED"
    },
    {
        "uid": "4256266147",
        "password": "BY_PARAHEX-MZBPO00KU-REDZED"
    },
    {
        "uid": "4256267343",
        "password": "BY_PARAHEX-XKJVTUO17-REDZED"
    },
    {
        "uid": "4256268514",
        "password": "BY_PARAHEX-6WSXF7ASX-REDZED"
    },
    {
        "uid": "4256269760",
        "password": "BY_PARAHEX-X2CMCXIAV-REDZED"
    },
    {
        "uid": "4256270149",
        "password": "BY_PARAHEX-FYKT7TCS1-REDZED"
    },
    {
        "uid": "4256270958",
        "password": "BY_PARAHEX-EUR6Q0XQM-REDZED"
    },
    {
        "uid": "4256272576",
        "password": "BY_PARAHEX-T4NINZ1S7-REDZED"
    },
    {
        "uid": "4256274104",
        "password": "BY_PARAHEX-HE7Y1UMD7-REDZED"
    },
    {
        "uid": "4256276669",
        "password": "BY_PARAHEX-ICBOPXUTU-REDZED"
    },
    {
        "uid": "4256277117",
        "password": "BY_PARAHEX-H06SZZFE1-REDZED"
    },
    {
        "uid": "4256278165",
        "password": "BY_PARAHEX-4MJPXV42F-REDZED"
    },
    {
        "uid": "4256279874",
        "password": "BY_PARAHEX-5F9YCMEPL-REDZED"
    },
    {
        "uid": "4256280924",
        "password": "BY_PARAHEX-NGSPN5SEY-REDZED"
    },
    {
        "uid": "4256281284",
        "password": "BY_PARAHEX-F7GFFGWK4-REDZED"
    },
    {
        "uid": "4256283231",
        "password": "BY_PARAHEX-L0IFHP3YS-REDZED"
    },
    {
        "uid": "4256284138",
        "password": "BY_PARAHEX-AZGFDC6SG-REDZED"
    },
    {
        "uid": "4256284566",
        "password": "BY_PARAHEX-3ATZKSP4P-REDZED"
    },
    {
        "uid": "4256285460",
        "password": "BY_PARAHEX-MZWK1PKTA-REDZED"
    },
    {
        "uid": "4256288093",
        "password": "BY_PARAHEX-INQL3INYW-REDZED"
    },
    {
        "uid": "4256289310",
        "password": "BY_PARAHEX-PA2UKIWJU-REDZED"
    },
    {
        "uid": "4256289649",
        "password": "BY_PARAHEX-2QJ5S5LXL-REDZED"
    },
    {
        "uid": "4256290007",
        "password": "BY_PARAHEX-OSPPP2KW3-REDZED"
    },
    {
        "uid": "4256290973",
        "password": "BY_PARAHEX-XZ244MKLD-REDZED"
    },
    {
        "uid": "4256292109",
        "password": "BY_PARAHEX-JAZ8HRRP9-REDZED"
    },
    {
        "uid": "4256292395",
        "password": "BY_PARAHEX-QSKQJXRAX-REDZED"
    },
    {
        "uid": "4256293488",
        "password": "BY_PARAHEX-CWUTTVFVL-REDZED"
    },
    {
        "uid": "4256293911",
        "password": "BY_PARAHEX-CH4YWPE6X-REDZED"
    },
    {
        "uid": "4256294323",
        "password": "BY_PARAHEX-O5RMVHXRO-REDZED"
    },
    {
        "uid": "4256294697",
        "password": "BY_PARAHEX-0EIZ80HKP-REDZED"
    },
    {
        "uid": "4256295268",
        "password": "BY_PARAHEX-PNUU3QVXG-REDZED"
    },
    {
        "uid": "4256295973",
        "password": "BY_PARAHEX-YVOUYDQIQ-REDZED"
    },
    {
        "uid": "4256296294",
        "password": "BY_PARAHEX-7TPXFPDQ6-REDZED"
    },
    {
        "uid": "4256298161",
        "password": "BY_PARAHEX-PQMPZIINH-REDZED"
    },
    {
        "uid": "4256299650",
        "password": "BY_PARAHEX-Q86KDMRQB-REDZED"
    },
    {
        "uid": "4256300110",
        "password": "BY_PARAHEX-JNPGNJXE7-REDZED"
    },
    {
        "uid": "4256301028",
        "password": "BY_PARAHEX-8GQDLSQTZ-REDZED"
    },
    {
        "uid": "4256301611",
        "password": "BY_PARAHEX-NBDQ2ALS2-REDZED"
    },
    {
        "uid": "4256302020",
        "password": "BY_PARAHEX-MNIN0S1KY-REDZED"
    },
    {
        "uid": "4256302418",
        "password": "BY_PARAHEX-8MHRYWSN3-REDZED"
    },
    {
        "uid": "4256303442",
        "password": "BY_PARAHEX-LXDAM4QXK-REDZED"
    },
    {
        "uid": "4256304446",
        "password": "BY_PARAHEX-0BRIRPXXY-REDZED"
    },
    {
        "uid": "4256304850",
        "password": "BY_PARAHEX-SBEA3SO4Z-REDZED"
    },
    {
        "uid": "4256305997",
        "password": "BY_PARAHEX-SCF8ZOTLS-REDZED"
    },
    {
        "uid": "4256307877",
        "password": "BY_PARAHEX-B6QA9SKXW-REDZED"
    },
    {
        "uid": "4256308489",
        "password": "BY_PARAHEX-EYVRVHMBB-REDZED"
    },
    {
        "uid": "4256310241",
        "password": "BY_PARAHEX-HFDZA9UZZ-REDZED"
    },
    {
        "uid": "4256311806",
        "password": "BY_PARAHEX-NGGMOLZNC-REDZED"
    },
    {
        "uid": "4256313436",
        "password": "BY_PARAHEX-ZQUERNN6T-REDZED"
    },
    {
        "uid": "4256314151",
        "password": "BY_PARAHEX-NPIA2SFM7-REDZED"
    },
    {
        "uid": "4256315031",
        "password": "BY_PARAHEX-3FBN4RGBF-REDZED"
    },
    {
        "uid": "4256317622",
        "password": "BY_PARAHEX-L3AZZVFFI-REDZED"
    },
    {
        "uid": "4256319250",
        "password": "BY_PARAHEX-R0ZVORLXK-REDZED"
    },
    {
        "uid": "4256319583",
        "password": "BY_PARAHEX-P4AUFFOKU-REDZED"
    },
    {
        "uid": "4256320535",
        "password": "BY_PARAHEX-BXRFJNXQH-REDZED"
    },
    {
        "uid": "4256321437",
        "password": "BY_PARAHEX-Q8AOLR5HP-REDZED"
    },
    {
        "uid": "4256321889",
        "password": "BY_PARAHEX-GVSJSDROX-REDZED"
    },
    {
        "uid": "4256322366",
        "password": "BY_PARAHEX-O35KTTPYR-REDZED"
    },
    {
        "uid": "4256323246",
        "password": "BY_PARAHEX-2SSTX76OA-REDZED"
    },
    {
        "uid": "4256323609",
        "password": "BY_PARAHEX-DFIQYX9IN-REDZED"
    },
    {
        "uid": "4256324750",
        "password": "BY_PARAHEX-9CGZNMHA8-REDZED"
    },
    {
        "uid": "4256325578",
        "password": "BY_PARAHEX-BMNNKKLRV-REDZED"
    },
    {
        "uid": "4256327411",
        "password": "BY_PARAHEX-EJT3CZT1U-REDZED"
    },
    {
        "uid": "4256329286",
        "password": "BY_PARAHEX-OWTYHEDV0-REDZED"
    },
    {
        "uid": "4256331339",
        "password": "BY_PARAHEX-6X7OUU3PV-REDZED"
    },
    {
        "uid": "4256332036",
        "password": "BY_PARAHEX-O6HGO30RF-REDZED"
    },
    {
        "uid": "4256332297",
        "password": "BY_PARAHEX-95PYTL40J-REDZED"
    },
    {
        "uid": "4256333861",
        "password": "BY_PARAHEX-WQYH3ICDY-REDZED"
    },
    {
        "uid": "4256335139",
        "password": "BY_PARAHEX-L5TZUB3OA-REDZED"
    },
    {
        "uid": "4256336656",
        "password": "BY_PARAHEX-9PBWSJVPG-REDZED"
    },
    {
        "uid": "4256337650",
        "password": "BY_PARAHEX-IWUBV3S2O-REDZED"
    },
    {
        "uid": "4256338498",
        "password": "BY_PARAHEX-JMYACZERX-REDZED"
    },
    {
        "uid": "4256339291",
        "password": "BY_PARAHEX-HSZRCBRMG-REDZED"
    },
    {
        "uid": "4256340742",
        "password": "BY_PARAHEX-PYH8IO6YC-REDZED"
    },
    {
        "uid": "4256341715",
        "password": "BY_PARAHEX-RCRFNHJPT-REDZED"
    },
    {
        "uid": "4256342204",
        "password": "BY_PARAHEX-RNVVR8XDA-REDZED"
    },
    {
        "uid": "4256342560",
        "password": "BY_PARAHEX-NS6LOM1N6-REDZED"
    },
    {
        "uid": "4256344746",
        "password": "BY_PARAHEX-K9IBUUILH-REDZED"
    },
    {
        "uid": "4256345964",
        "password": "BY_PARAHEX-6XR6XW64M-REDZED"
    },
    {
        "uid": "4256347159",
        "password": "BY_PARAHEX-RI4KMPJU8-REDZED"
    },
    {
        "uid": "4256349227",
        "password": "BY_PARAHEX-8HFUP48ZP-REDZED"
    },
    {
        "uid": "4256350705",
        "password": "BY_PARAHEX-LW3OPU4PP-REDZED"
    },
    {
        "uid": "4256351928",
        "password": "BY_PARAHEX-4QIQHYCYS-REDZED"
    },
    {
        "uid": "4256353467",
        "password": "BY_PARAHEX-GPZCJTPJU-REDZED"
    },
    {
        "uid": "4256354412",
        "password": "BY_PARAHEX-AR9XC2YMI-REDZED"
    },
    {
        "uid": "4256355393",
        "password": "BY_PARAHEX-9NULE9CXV-REDZED"
    },
    {
        "uid": "4256356576",
        "password": "BY_PARAHEX-MASFAGHGX-REDZED"
    },
    {
        "uid": "4256360548",
        "password": "BY_PARAHEX-LHLM8YLYN-REDZED"
    },
    {
        "uid": "4256361753",
        "password": "BY_PARAHEX-KTUEXXYMO-REDZED"
    },
    {
        "uid": "4256362642",
        "password": "BY_PARAHEX-EEFACX6A7-REDZED"
    }
]


# ✅ دالة تحميل الحسابات من المتغير الثابت
def load_accounts():
    accounts_dict = {}
    for account in ACCOUNTS:
        accounts_dict[account["uid"]] = account["password"]
    print(f"Loaded {len(accounts_dict)} accounts from embedded accounts")
    return accounts_dict


# ✅ دالة تحميل التوكنات (لا تعتمد على ملفات)
def load_tokens_from_accounts(limit=None):
    accounts = load_accounts()
    tokens_list = [(uid, password) for uid, password in accounts.items()]

    if limit is not None:
        tokens_list = random.sample(tokens_list, min(limit, len(tokens_list)))

    print(f"Loaded {len(tokens_list)} tokens from embedded accounts")
    return tokens_list


def get_token(password, uid):
    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    response = requests.post(url, headers=headers, data=data, verify=False)
    if response.status_code != 200:
        return None
    return response.json()


def encrypt_message(key, iv, plaintext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(plaintext, AES.block_size)
    encrypted_message = cipher.encrypt(padded_message)
    return encrypted_message


def parse_response(response_content):
    response_dict = {}
    lines = response_content.split("\n")
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            response_dict[key.strip()] = value.strip().strip('"')
    return response_dict


def process_token(uid, password):
    print(f"Processing token for UID: {uid}")
    token_data = get_token(password, uid)
    if not token_data:
        print(f"Failed to retrieve token for UID: {uid}")
        return {"uid": uid, "error": "Failed to retrieve token"}

    # إنشاء GameData Protobuf
    game_data = my_pb2.GameData()
    game_data.timestamp = "2024-12-05 18:15:32"
    game_data.game_name = "free fire"
    game_data.game_version = 1
    game_data.version_code = "1.108.3"
    game_data.os_info = "Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)"
    game_data.device_type = "Handheld"
    game_data.network_provider = "Verizon Wireless"
    game_data.connection_type = "WIFI"
    game_data.screen_width = 1280
    game_data.screen_height = 960
    game_data.dpi = "240"
    game_data.cpu_info = "ARMv7 VFPv3 NEON VMH | 2400 | 4"
    game_data.total_ram = 5951
    game_data.gpu_name = "Adreno (TM) 640"
    game_data.gpu_version = "OpenGL ES 3.0"
    game_data.user_id = "Google|74b585a9-0268-4ad3-8f36-ef41d2e53610"
    game_data.ip_address = "172.190.111.97"
    game_data.language = "en"
    game_data.open_id = token_data['open_id']
    game_data.access_token = token_data['access_token']
    game_data.platform_type = 4
    game_data.device_form_factor = "Handheld"
    game_data.device_model = "Asus ASUS_I005DA"
    game_data.field_60 = 32968
    game_data.field_61 = 29815
    game_data.field_62 = 2479
    game_data.field_63 = 914
    game_data.field_64 = 31213
    game_data.field_65 = 32968
    game_data.field_66 = 31213
    game_data.field_67 = 32968
    game_data.field_70 = 4
    game_data.field_73 = 2
    game_data.library_path = "/data/app/com.dts.freefireth-QPvBnTUhYWE-7DMZSOGdmA==/lib/arm"
    game_data.field_76 = 1
    game_data.apk_info = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-QPvBnTUhYWE-7DMZSOGdmA==/base.apk"
    game_data.field_78 = 6
    game_data.field_79 = 1
    game_data.os_architecture = "32"
    game_data.build_number = "2019117877"
    game_data.field_85 = 1
    game_data.graphics_backend = "OpenGLES2"
    game_data.max_texture_units = 16383
    game_data.rendering_api = 4
    game_data.encoded_field_89 = "\u0017T\u0011\u0017\u0002\b\u000eUMQ\bEZ\u0003@ZK;Z\u0002\u000eV\ri[QVi\u0003\ro\t\u0007e"
    game_data.field_92 = 9204
    game_data.marketplace = "3rd_party"
    game_data.encryption_key = "KqsHT2B4It60T/65PGR5PXwFxQkVjGNi+IMCK3CFBCBfrNpSUA1dZnjaT3HcYchlIFFL1ZJOg0cnulKCPGD3C3h1eFQ="
    game_data.total_storage = 111107
    game_data.field_97 = 1
    game_data.field_98 = 1
    game_data.field_99 = "4"
    game_data.field_100 = "4"

    # تسلسل البيانات
    serialized_data = game_data.SerializeToString()

    # تشفير البيانات
    encrypted_data = encrypt_message(AES_KEY, AES_IV, serialized_data)
    hex_encrypted_data = binascii.hexlify(encrypted_data).decode('utf-8')

    # إرسال البيانات المشفرة إلى الخادم
    url = "https://loginbp.common.ggbluefox.com/MajorLogin"
    headers = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/octet-stream",
        'Expect': "500-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB51"
    }
    edata = bytes.fromhex(hex_encrypted_data)

    try:
        response = requests.post(url, data=edata, headers=headers, verify=False, timeout=30)
        if response.status_code == 200:
            # محاولة فك تشفير الـ Protobuf
            example_msg = output_pb2.Garena_420()
            try:
                example_msg.ParseFromString(response.content)
                # تحليل الـ response لاستخراج الحقول المهمة
                response_dict = parse_response(str(example_msg))
                print(f"Successfully processed token for UID: {uid}")
                return {"uid": uid, "token": response_dict.get("token", "N/A")}
            except Exception as e:
                print(f"Failed to deserialize the response for UID: {uid}: {e}")
                return None
        else:
            print(f"Failed to get response for UID: {uid}: HTTP {response.status_code}, {response.reason}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred while making the request for UID: {uid}: {e}")
        return None


def fetch_tokens():
    global responses_cache
    # تحميل التوكنات من الحسابات المضمنة في الكود
    tokens_from_accounts = load_tokens_from_accounts(limit=1000)

    if not tokens_from_accounts:
        print("No accounts found in embedded accounts")
        return

    responses = []

    # استخدام ThreadPoolExecutor لتنفيذ المهام بشكل متوازي
    with ThreadPoolExecutor(max_workers=15) as executor:
        future_to_uid = {executor.submit(process_token, uid, password): uid for uid, password in
                         tokens_from_accounts}
        for future in as_completed(future_to_uid):
            try:
                token_info = future.result()
                if token_info and token_info.get("token") and token_info["token"] != "N/A":
                    responses.append(token_info)
            except Exception as e:
                print(f"Error processing token: {e}")

    # تخزين النتائج في الكاش
    responses_cache = responses
    print(f"Stored {len(responses)} tokens in cache.")


# ✅ الدوال الخاصة باللايكات
def encrypt_message_like(plaintext):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    return binascii.hexlify(cipher.encrypt(pad(plaintext, AES.block_size))).decode()


def create_uid_proto(uid):
    pb = uid_generator_pb2.uid_generator()
    pb.saturn_ = int(uid)
    pb.garena = 1
    return pb.SerializeToString()


def create_like_proto(uid):
    pb = like_pb2.like()
    pb.uid = int(uid)
    return pb.SerializeToString()


def decode_protobuf_like(binary):
    try:
        pb = like_count_pb2.Info()
        pb.ParseFromString(binary)
        return pb
    except DecodeError:
        return None


def make_like_request(enc_uid, token):
    url = "https://clientbp.ggblueshark.com/GetPlayerPersonalShow"
    headers = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/x-www-form-urlencoded",
        'Expect': "500-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB51"
    }
    try:
        res = requests.post(url, data=bytes.fromhex(enc_uid), headers=headers, verify=False, timeout=30)
        return decode_protobuf_like(res.content)
    except Exception as e:
        print(f"Error in make_like_request: {e}")
        return None


# ✅ إرسال لايك واحد
async def send_like_request(enc_uid, token_info):
    url = "https://clientbp.ggblueshark.com/LikeProfile"
    headers = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Authorization': f"Bearer {token_info['token']}",
        'Content-Type': "application/x-www-form-urlencoded",
        'Expect': "500-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB51"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=bytes.fromhex(enc_uid), headers=headers, timeout=15) as r:
                return {
                    "uid": token_info["uid"],
                    "status": r.status,
                    "success": r.status == 200
                }
    except asyncio.TimeoutError:
        return {
            "uid": token_info["uid"],
            "status": "timeout",
            "success": False
        }
    except Exception as e:
        return {
            "uid": token_info["uid"],
            "status": "error",
            "error": str(e),
            "success": False
        }


# ✅ إرسال لايكات لكل التوكنات
async def send_likes(uid, tokens):
    enc_uid = encrypt_message_like(create_like_proto(uid))
    tasks = [send_like_request(enc_uid, token_info) for token_info in tokens]
    return await asyncio.gather(*tasks)


@app.get('/token')
async def get_responses():
    if not responses_cache:
        print("No data available in cache.")
        return JSONResponse(content={"error": "No data available yet"})
    return JSONResponse(content={"tokens": responses_cache})


@app.get('/like')
async def like_handler(uid: str):
    if not uid:
        return JSONResponse(content={"error": "Missing UID"}, status_code=400)

    try:
        print(f"Starting like process for UID: {uid}")

        tokens = responses_cache
        if not tokens:
            return JSONResponse(content={"error": "No valid tokens available. Please refresh tokens first."}, status_code=401)

        print(f"Using {len(tokens)} valid tokens")

        enc_uid = encrypt_message_like(create_uid_proto(uid))
        before = make_like_request(enc_uid, tokens[0]["token"])
        if not before:
            return JSONResponse(content={"error": "Failed to retrieve player info"}, status_code=500)

        before_data = json.loads(MessageToJson(before))
        likes_before = int(before_data.get("AccountInfo", {}).get("Likes", 0))
        nickname = before_data.get("AccountInfo", {}).get("PlayerNickname", "Unknown")
        player_level = before_data.get("AccountInfo", {}).get("Level", 0)
        region = before_data.get("AccountInfo", {}).get("region", "Unknown")

        print(f"Before: {likes_before} likes for {nickname}")

        print("Sending likes...")
        responses = await send_likes(uid, tokens)
        success_count = sum(1 for r in responses if r.get("success"))

        print(f"Successfully sent {success_count} likes")

        after = make_like_request(enc_uid, tokens[0]["token"])
        likes_after = likes_before
        if after:
            after_data = json.loads(MessageToJson(after))
            likes_after = int(after_data.get("AccountInfo", {}).get("Likes", 0))

        actual_likes_added = likes_after - likes_before

        return JSONResponse(content={
            "PlayerNickname": nickname,
            "UID": uid,
            "Region": region,
            "PlayerLevel": player_level,
            "LikesBefore": likes_before,
            "LikesAfter": likes_after,
            "LikesGivenByAPI": actual_likes_added,
            "SuccessfulRequests": success_count,
            "TotalAccountsUsed": len(tokens),
            "status": 1 if actual_likes_added > 0 else 2
        })

    except Exception as e:
        print(f"Error in like_handler: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post('/refresh_tokens')
async def refresh_tokens():
    try:
        fetch_tokens()
        return JSONResponse(content={
            "message": "Tokens refreshed successfully",
            "total_tokens": len(responses_cache)
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get('/')
async def home():
    return JSONResponse(content={
        "status": "online",
        "message": "Like API is running ✅",
        "cached_tokens": len(responses_cache),
        "embedded_accounts": len(ACCOUNTS),
        "endpoints": {
            "/like?uid=UID": "Send likes to player",
            "/token": "Get cached tokens",
            "/refresh_tokens": "Refresh tokens (POST)"
        }
    })


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


# تشغيل fetch_tokens فورًا عند بدء التشغيل
fetch_tokens()

# جدولة المهمة كل 7 ساعات
schedule.every(7).hours.do(fetch_tokens)

# تشغيل السكيدولر في ثانوية منفصلة
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)




