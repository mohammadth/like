from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
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

# تكوين CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تخزين البيانات في الذاكرة بدلاً من الكاش
responses_cache = []

# ✅ الحسابات مخزنة مباشرة في الكود
ACCOUNTS = [
    {
        "uid": "4244495322",
        "password": "BY_PARAHEX-1GDWXSH9P-REDZED"
    },
    {
        "uid": "4244495705",
        "password": "BY_PARAHEX-END7IZ0DX-REDZED"
    },
    {
        "uid": "4244495898",
        "password": "BY_PARAHEX-TY8MJWZUP-REDZED"
    },
    {
        "uid": "4244496275",
        "password": "BY_PARAHEX-L5CHYAEBM-REDZED"
    },
    {
        "uid": "4244496549",
        "password": "BY_PARAHEX-JRDSQFOCA-REDZED"
    },
    {
        "uid": "4244496947",
        "password": "BY_PARAHEX-MDA3I3461-REDZED"
    },
    {
        "uid": "4244497293",
        "password": "BY_PARAHEX-HUQNJMMD5-REDZED"
    },
    {
        "uid": "4244497561",
        "password": "BY_PARAHEX-QXIWV1YFH-REDZED"
    },
    {
        "uid": "4244497752",
        "password": "BY_PARAHEX-D39MQX7EQ-REDZED"
    },
    {
        "uid": "4244497955",
        "password": "BY_PARAHEX-ONYI1VV4L-REDZED"
    },
    {
        "uid": "4244498229",
        "password": "BY_PARAHEX-YVLUPMR52-REDZED"
    },
    {
        "uid": "4244498577",
        "password": "BY_PARAHEX-XF8SGMYZM-REDZED"
    },
    {
        "uid": "4244498883",
        "password": "BY_PARAHEX-D8HCZRYR5-REDZED"
    },
    {
        "uid": "4244499183",
        "password": "BY_PARAHEX-X2DSMILF8-REDZED"
    },
    {
        "uid": "4244499403",
        "password": "BY_PARAHEX-FDDR6IX9W-REDZED"
    },
    {
        "uid": "4244499700",
        "password": "BY_PARAHEX-EF2V3X3DA-REDZED"
    },
    {
        "uid": "4244500076",
        "password": "BY_PARAHEX-KN43ZYVZA-REDZED"
    },
    {
        "uid": "4244500526",
        "password": "BY_PARAHEX-T04EIIRV9-REDZED"
    },
    {
        "uid": "4244500956",
        "password": "BY_PARAHEX-TBEMWNXED-REDZED"
    },
    {
        "uid": "4244501184",
        "password": "BY_PARAHEX-BBYFCAHBB-REDZED"
    },
    {
        "uid": "4244501386",
        "password": "BY_PARAHEX-4S1FEG2BN-REDZED"
    },
    {
        "uid": "4244501588",
        "password": "BY_PARAHEX-783X6M4ZX-REDZED"
    },
    {
        "uid": "4244501857",
        "password": "BY_PARAHEX-RCDVYE41K-REDZED"
    },
    {
        "uid": "4244502111",
        "password": "BY_PARAHEX-3LLW99TQ1-REDZED"
    },
    {
        "uid": "4244502670",
        "password": "BY_PARAHEX-Q9P4G9S5Q-REDZED"
    },
    {
        "uid": "4244503229",
        "password": "BY_PARAHEX-AZRFFO3SB-REDZED"
    },
    {
        "uid": "4244503454",
        "password": "BY_PARAHEX-HRG70JYDM-REDZED"
    },
    {
        "uid": "4244503870",
        "password": "BY_PARAHEX-OC6Y95GIK-REDZED"
    },
    {
        "uid": "4244504198",
        "password": "BY_PARAHEX-NQKQ7FJIC-REDZED"
    },
    {
        "uid": "4244504493",
        "password": "BY_PARAHEX-ZKPZTHHTX-REDZED"
    },
    {
        "uid": "4244504802",
        "password": "BY_PARAHEX-LOSJFPATI-REDZED"
    },
    {
        "uid": "4244505133",
        "password": "BY_PARAHEX-N5D0NXWMO-REDZED"
    },
    {
        "uid": "4244505474",
        "password": "BY_PARAHEX-8JVIFDJE0-REDZED"
    },
    {
        "uid": "4244505822",
        "password": "BY_PARAHEX-BDCW9SLM9-REDZED"
    },
    {
        "uid": "4244506227",
        "password": "BY_PARAHEX-HOIRGLMRQ-REDZED"
    },
    {
        "uid": "4244506693",
        "password": "BY_PARAHEX-IL3HJTTJN-REDZED"
    },
    {
        "uid": "4244506986",
        "password": "BY_PARAHEX-DRXYE91CF-REDZED"
    },
    {
        "uid": "4244507293",
        "password": "BY_PARAHEX-JZLNNFCCG-REDZED"
    },
    {
        "uid": "4244507603",
        "password": "BY_PARAHEX-X1TOTRU7I-REDZED"
    },
    {
        "uid": "4244507831",
        "password": "BY_PARAHEX-DZXX54JYE-REDZED"
    },
    {
        "uid": "4244508179",
        "password": "BY_PARAHEX-FRPULZDKT-REDZED"
    },
    {
        "uid": "4244508557",
        "password": "BY_PARAHEX-UV86EQDGO-REDZED"
    },
    {
        "uid": "4244508915",
        "password": "BY_PARAHEX-01VCXJCYX-REDZED"
    },
    {
        "uid": "4244509410",
        "password": "BY_PARAHEX-7MQSR3LGW-REDZED"
    },
    {
        "uid": "4244509735",
        "password": "BY_PARAHEX-DLVYM04YC-REDZED"
    },
    {
        "uid": "4244510138",
        "password": "BY_PARAHEX-UNLMU8QPL-REDZED"
    },
    {
        "uid": "4244510559",
        "password": "BY_PARAHEX-R9ZXL0PTV-REDZED"
    },
    {
        "uid": "4244510912",
        "password": "BY_PARAHEX-9OBN142EE-REDZED"
    },
    {
        "uid": "4244511199",
        "password": "BY_PARAHEX-Q0LEAOQQT-REDZED"
    },
    {
        "uid": "4244511585",
        "password": "BY_PARAHEX-HSEPRTWNF-REDZED"
    },
    {
        "uid": "4244512163",
        "password": "BY_PARAHEX-RUCDDNBX4-REDZED"
    },
    {
        "uid": "4244512544",
        "password": "BY_PARAHEX-LUALF72MP-REDZED"
    },
    {
        "uid": "4244513383",
        "password": "BY_PARAHEX-GKRFM5BJU-REDZED"
    },
    {
        "uid": "4244513691",
        "password": "BY_PARAHEX-EXLATH8T7-REDZED"
    },
    {
        "uid": "4244514332",
        "password": "BY_PARAHEX-MTROKXNNK-REDZED"
    },
    {
        "uid": "4244514675",
        "password": "BY_PARAHEX-EFBGFOG41-REDZED"
    },
    {
        "uid": "4244515046",
        "password": "BY_PARAHEX-R3KWEAKC5-REDZED"
    },
    {
        "uid": "4244515441",
        "password": "BY_PARAHEX-H0QC0LFVM-REDZED"
    },
    {
        "uid": "4244515896",
        "password": "BY_PARAHEX-LM0PCHOXK-REDZED"
    },
    {
        "uid": "4244516265",
        "password": "BY_PARAHEX-VMBXAMJZV-REDZED"
    },
    {
        "uid": "4244516659",
        "password": "BY_PARAHEX-88Y0585XD-REDZED"
    },
    {
        "uid": "4244516920",
        "password": "BY_PARAHEX-LMZZMSIIQ-REDZED"
    },
    {
        "uid": "4244517256",
        "password": "BY_PARAHEX-S8QJFJ9CQ-REDZED"
    },
    {
        "uid": "4244517515",
        "password": "BY_PARAHEX-OYSGUAFMA-REDZED"
    },
    {
        "uid": "4244517857",
        "password": "BY_PARAHEX-QQOX0FVUD-REDZED"
    },
    {
        "uid": "4244518327",
        "password": "BY_PARAHEX-F9SNJMVXX-REDZED"
    },
    {
        "uid": "4244518705",
        "password": "BY_PARAHEX-AXQZANTV4-REDZED"
    },
    {
        "uid": "4244519127",
        "password": "BY_PARAHEX-VDHO9PHOZ-REDZED"
    },
    {
        "uid": "4244519543",
        "password": "BY_PARAHEX-4RHIICWFD-REDZED"
    },
    {
        "uid": "4244519985",
        "password": "BY_PARAHEX-CGBPNRPXJ-REDZED"
    },
    {
        "uid": "4244520603",
        "password": "BY_PARAHEX-GMVRIGSY1-REDZED"
    },
    {
        "uid": "4244520946",
        "password": "BY_PARAHEX-YEX13H4QM-REDZED"
    },
    {
        "uid": "4244521313",
        "password": "BY_PARAHEX-FSYWWOMRB-REDZED"
    },
    {
        "uid": "4244521622",
        "password": "BY_PARAHEX-OOVOCLTYA-REDZED"
    },
    {
        "uid": "4244522043",
        "password": "BY_PARAHEX-QBUCEXWAD-REDZED"
    },
    {
        "uid": "4244522535",
        "password": "BY_PARAHEX-SXW4R1HEY-REDZED"
    },
    {
        "uid": "4244522895",
        "password": "BY_PARAHEX-QMPF17DHV-REDZED"
    },
    {
        "uid": "4244523306",
        "password": "BY_PARAHEX-R1RJH8LYU-REDZED"
    },
    {
        "uid": "4244523570",
        "password": "BY_PARAHEX-MPHYKQK6X-REDZED"
    },
    {
        "uid": "4244524068",
        "password": "BY_PARAHEX-LB5PVE49M-REDZED"
    },
    {
        "uid": "4244524439",
        "password": "BY_PARAHEX-OCPZORABU-REDZED"
    },
    {
        "uid": "4244524771",
        "password": "BY_PARAHEX-7POJ4VOGO-REDZED"
    },
    {
        "uid": "4244525075",
        "password": "BY_PARAHEX-CKCBHTXXW-REDZED"
    },
    {
        "uid": "4244525286",
        "password": "BY_PARAHEX-RABPAQMLW-REDZED"
    },
    {
        "uid": "4244525884",
        "password": "BY_PARAHEX-L7HEF8KDT-REDZED"
    },
    {
        "uid": "4244526353",
        "password": "BY_PARAHEX-DZHAHBKXB-REDZED"
    },
    {
        "uid": "4244526825",
        "password": "BY_PARAHEX-WNVCW6D6V-REDZED"
    },
    {
        "uid": "4244527274",
        "password": "BY_PARAHEX-2VHJJGFOT-REDZED"
    },
    {
        "uid": "4244527726",
        "password": "BY_PARAHEX-H4MA8EAZA-REDZED"
    },
    {
        "uid": "4244528162",
        "password": "BY_PARAHEX-KGWD01YRR-REDZED"
    },
    {
        "uid": "4244528667",
        "password": "BY_PARAHEX-WVRSHU9X6-REDZED"
    },
    {
        "uid": "4244529257",
        "password": "BY_PARAHEX-U9PSNYFK0-REDZED"
    },
    {
        "uid": "4244529696",
        "password": "BY_PARAHEX-P62B4QDWD-REDZED"
    },
    {
        "uid": "4244530285",
        "password": "BY_PARAHEX-UDKC1EN68-REDZED"
    },
    {
        "uid": "4244530986",
        "password": "BY_PARAHEX-O3QCIW1M5-REDZED"
    },
    {
        "uid": "4244531709",
        "password": "BY_PARAHEX-R6B0BUKRR-REDZED"
    },
    {
        "uid": "4244532379",
        "password": "BY_PARAHEX-A9ZONXUAR-REDZED"
    },
    {
        "uid": "4244532983",
        "password": "BY_PARAHEX-Y8N07HVU3-REDZED"
    },
    {
        "uid": "4244533497",
        "password": "BY_PARAHEX-KZDVYX16A-REDZED"
    },
    {
        "uid": "4244534070",
        "password": "BY_PARAHEX-PYSXV0NIF-REDZED"
    },
    {
        "uid": "4244534542",
        "password": "BY_PARAHEX-LNGJLDRJH-REDZED"
    },
    {
        "uid": "4244534957",
        "password": "BY_PARAHEX-PX3FFPHWM-REDZED"
    },
    {
        "uid": "4244535395",
        "password": "BY_PARAHEX-RS2CU1LWM-REDZED"
    },
    {
        "uid": "4244535667",
        "password": "BY_PARAHEX-BPVG9S2Q1-REDZED"
    },
    {
        "uid": "4244536565",
        "password": "BY_PARAHEX-L77MLPLSA-REDZED"
    },
    {
        "uid": "4244537034",
        "password": "BY_PARAHEX-6ZCSUDIDS-REDZED"
    },
    {
        "uid": "4244537560",
        "password": "BY_PARAHEX-T78BLU0XV-REDZED"
    },
    {
        "uid": "4244538038",
        "password": "BY_PARAHEX-FXJPQ8ZS8-REDZED"
    },
    {
        "uid": "4244538508",
        "password": "BY_PARAHEX-QPYZQM9RV-REDZED"
    },
    {
        "uid": "4244538826",
        "password": "BY_PARAHEX-HQ7EZJYOA-REDZED"
    },
    {
        "uid": "4244539116",
        "password": "BY_PARAHEX-WFDGYXLVL-REDZED"
    },
    {
        "uid": "4244540161",
        "password": "BY_PARAHEX-UER2Z9PFG-REDZED"
    },
    {
        "uid": "4244540675",
        "password": "BY_PARAHEX-XMIM3BVNO-REDZED"
    },
    {
        "uid": "4244541193",
        "password": "BY_PARAHEX-YXOJPVX9W-REDZED"
    },
    {
        "uid": "4244541915",
        "password": "BY_PARAHEX-YO4AWREX1-REDZED"
    },
    {
        "uid": "4244542591",
        "password": "BY_PARAHEX-NL9NRJPPM-REDZED"
    },
    {
        "uid": "4244543031",
        "password": "BY_PARAHEX-SRDQKSRAM-REDZED"
    },
    {
        "uid": "4244543720",
        "password": "BY_PARAHEX-IWC49D25S-REDZED"
    },
    {
        "uid": "4244544115",
        "password": "BY_PARAHEX-AVJNOO4KG-REDZED"
    },
    {
        "uid": "4244544627",
        "password": "BY_PARAHEX-ZVOXGEVHA-REDZED"
    },
    {
        "uid": "4244545198",
        "password": "BY_PARAHEX-ODK5KSBD4-REDZED"
    },
    {
        "uid": "4244545948",
        "password": "BY_PARAHEX-U3JTZMDKP-REDZED"
    },
    {
        "uid": "4244546504",
        "password": "BY_PARAHEX-GIP07JYL5-REDZED"
    },
    {
        "uid": "4244547185",
        "password": "BY_PARAHEX-MADTSOOYG-REDZED"
    },
    {
        "uid": "4244547607",
        "password": "BY_PARAHEX-DZ00UMQ8L-REDZED"
    },
    {
        "uid": "4244548051",
        "password": "BY_PARAHEX-XLAHFFLVP-REDZED"
    },
    {
        "uid": "4244548333",
        "password": "BY_PARAHEX-ERJSB6T7W-REDZED"
    },
    {
        "uid": "4244549110",
        "password": "BY_PARAHEX-4MZSM8OHV-REDZED"
    },
    {
        "uid": "4244549805",
        "password": "BY_PARAHEX-CGMBQPOOZ-REDZED"
    },
    {
        "uid": "4244550215",
        "password": "BY_PARAHEX-18DBL08ZA-REDZED"
    },
    {
        "uid": "4244550692",
        "password": "BY_PARAHEX-Y8ITKK1S7-REDZED"
    },
    {
        "uid": "4244551078",
        "password": "BY_PARAHEX-WT3PYIISE-REDZED"
    },
    {
        "uid": "4244551377",
        "password": "BY_PARAHEX-MJ91DMHR3-REDZED"
    },
    {
        "uid": "4244551668",
        "password": "BY_PARAHEX-YAMXKWDVB-REDZED"
    },
    {
        "uid": "4244551879",
        "password": "BY_PARAHEX-NHSHOX0S8-REDZED"
    },
    {
        "uid": "4244552201",
        "password": "BY_PARAHEX-UNWTUJ7BJ-REDZED"
    },
    {
        "uid": "4244552708",
        "password": "BY_PARAHEX-ANMMRZMTL-REDZED"
    },
    {
        "uid": "4244553387",
        "password": "BY_PARAHEX-D2TV209BM-REDZED"
    },
    {
        "uid": "4244553953",
        "password": "BY_PARAHEX-SSL34UOOV-REDZED"
    },
    {
        "uid": "4244554425",
        "password": "BY_PARAHEX-DAWTI8VA3-REDZED"
    },
    {
        "uid": "4244554954",
        "password": "BY_PARAHEX-URVXCZ6V2-REDZED"
    },
    {
        "uid": "4244555438",
        "password": "BY_PARAHEX-J9GBYCGJA-REDZED"
    },
    {
        "uid": "4244555814",
        "password": "BY_PARAHEX-UJQIBZING-REDZED"
    },
    {
        "uid": "4244556280",
        "password": "BY_PARAHEX-JU8FANWPP-REDZED"
    },
    {
        "uid": "4244556862",
        "password": "BY_PARAHEX-7ALDFWY2W-REDZED"
    },
    {
        "uid": "4244557209",
        "password": "BY_PARAHEX-TQTSUFDAH-REDZED"
    },
    {
        "uid": "4244558027",
        "password": "BY_PARAHEX-2TALWEUQX-REDZED"
    },
    {
        "uid": "4244558445",
        "password": "BY_PARAHEX-QKIJVY2LP-REDZED"
    },
    {
        "uid": "4244558876",
        "password": "BY_PARAHEX-TTGK9ILYR-REDZED"
    },
    {
        "uid": "4244559634",
        "password": "BY_PARAHEX-Z0REZPIEJ-REDZED"
    },
    {
        "uid": "4244560101",
        "password": "BY_PARAHEX-00X2EQKCQ-REDZED"
    },
    {
        "uid": "4244560464",
        "password": "BY_PARAHEX-ECWTKFTVM-REDZED"
    },
    {
        "uid": "4244560904",
        "password": "BY_PARAHEX-UZMEQ2WPA-REDZED"
    },
    {
        "uid": "4244561487",
        "password": "BY_PARAHEX-NJ07ZTTO9-REDZED"
    },
    {
        "uid": "4244561721",
        "password": "BY_PARAHEX-PKK9KFV8T-REDZED"
    },
    {
        "uid": "4244562149",
        "password": "BY_PARAHEX-4WVIXKNGL-REDZED"
    },
    {
        "uid": "4244562775",
        "password": "BY_PARAHEX-PWTYOA7RW-REDZED"
    },
    {
        "uid": "4244563346",
        "password": "BY_PARAHEX-HATPBROXK-REDZED"
    },
    {
        "uid": "4244563903",
        "password": "BY_PARAHEX-DP2M2RBQE-REDZED"
    },
    {
        "uid": "4244564613",
        "password": "BY_PARAHEX-U4ZFVVDYF-REDZED"
    },
    {
        "uid": "4244565101",
        "password": "BY_PARAHEX-UC1QID1GG-REDZED"
    },
    {
        "uid": "4244565399",
        "password": "BY_PARAHEX-QRAEKM7SF-REDZED"
    },
    {
        "uid": "4244565635",
        "password": "BY_PARAHEX-3MZPINCKT-REDZED"
    },
    {
        "uid": "4244566502",
        "password": "BY_PARAHEX-R6WUMDGNM-REDZED"
    },
    {
        "uid": "4244566934",
        "password": "BY_PARAHEX-UHQ61VWWZ-REDZED"
    },
    {
        "uid": "4244567308",
        "password": "BY_PARAHEX-KSSNALEEY-REDZED"
    },
    {
        "uid": "4244568029",
        "password": "BY_PARAHEX-4Z3NXY902-REDZED"
    },
    {
        "uid": "4244568557",
        "password": "BY_PARAHEX-AN5U56CCJ-REDZED"
    },
    {
        "uid": "4244569392",
        "password": "BY_PARAHEX-94ZJDGLKD-REDZED"
    },
    {
        "uid": "4244570479",
        "password": "BY_PARAHEX-HIQFV5XEJ-REDZED"
    },
    {
        "uid": "4244570764",
        "password": "BY_PARAHEX-WICB36WGX-REDZED"
    },
    {
        "uid": "4244571003",
        "password": "BY_PARAHEX-44D7IC1J1-REDZED"
    },
    {
        "uid": "4244571286",
        "password": "BY_PARAHEX-ELRYAL6I9-REDZED"
    },
    {
        "uid": "4244571694",
        "password": "BY_PARAHEX-VX1AINU3Z-REDZED"
    },
    {
        "uid": "4244572115",
        "password": "BY_PARAHEX-ZYI7HVVCR-REDZED"
    },
    {
        "uid": "4244572437",
        "password": "BY_PARAHEX-SRPSBQFDW-REDZED"
    },
    {
        "uid": "4244572710",
        "password": "BY_PARAHEX-UZENA88BE-REDZED"
    },
    {
        "uid": "4244573223",
        "password": "BY_PARAHEX-BONTBDFZI-REDZED"
    },
    {
        "uid": "4244573830",
        "password": "BY_PARAHEX-DWRMKGUEF-REDZED"
    },
    {
        "uid": "4244574361",
        "password": "BY_PARAHEX-85WEGOALS-REDZED"
    },
    {
        "uid": "4244574910",
        "password": "BY_PARAHEX-JZALKFJNG-REDZED"
    },
    {
        "uid": "4244575254",
        "password": "BY_PARAHEX-WHKN2CHVF-REDZED"
    },
    {
        "uid": "4244575718",
        "password": "BY_PARAHEX-VWH47F5RI-REDZED"
    },
    {
        "uid": "4244576260",
        "password": "BY_PARAHEX-AEF7ZZPWH-REDZED"
    },
    {
        "uid": "4244576642",
        "password": "BY_PARAHEX-JY4WSMBGT-REDZED"
    },
    {
        "uid": "4244576976",
        "password": "BY_PARAHEX-I4W9FHSJA-REDZED"
    },
    {
        "uid": "4244577334",
        "password": "BY_PARAHEX-RSFRDKYTI-REDZED"
    },
    {
        "uid": "4244578110",
        "password": "BY_PARAHEX-PITXCATWX-REDZED"
    },
    {
        "uid": "4244578520",
        "password": "BY_PARAHEX-CFHH3DBTB-REDZED"
    },
    {
        "uid": "4244579063",
        "password": "BY_PARAHEX-DCZG6RHZI-REDZED"
    },
    {
        "uid": "4244579635",
        "password": "BY_PARAHEX-TQNA1LIMM-REDZED"
    },
    {
        "uid": "4244579981",
        "password": "BY_PARAHEX-74X5MZMO8-REDZED"
    },
    {
        "uid": "4244580331",
        "password": "BY_PARAHEX-KPCLRBSYB-REDZED"
    },
    {
        "uid": "4244580556",
        "password": "BY_PARAHEX-LSP0WHEF0-REDZED"
    },
    {
        "uid": "4244580871",
        "password": "BY_PARAHEX-INY9U3EA2-REDZED"
    },
    {
        "uid": "4244581158",
        "password": "BY_PARAHEX-FYV4B0JPI-REDZED"
    },
    {
        "uid": "4244581477",
        "password": "BY_PARAHEX-QYUVWKKBD-REDZED"
    },
    {
        "uid": "4244581791",
        "password": "BY_PARAHEX-MA5QOZLI9-REDZED"
    },
    {
        "uid": "4244582046",
        "password": "BY_PARAHEX-D4RREGNWZ-REDZED"
    },
    {
        "uid": "4244582533",
        "password": "BY_PARAHEX-X34YDPAPX-REDZED"
    },
    {
        "uid": "4244582978",
        "password": "BY_PARAHEX-SDF0UVHU0-REDZED"
    },
    {
        "uid": "4244583286",
        "password": "BY_PARAHEX-TUTUTIP6M-REDZED"
    },
    {
        "uid": "4244583594",
        "password": "BY_PARAHEX-H6P3BV4DA-REDZED"
    },
    {
        "uid": "4244584090",
        "password": "BY_PARAHEX-LHYFYG4OY-REDZED"
    },
    {
        "uid": "4244584439",
        "password": "BY_PARAHEX-RX5H3PZ5B-REDZED"
    },
    {
        "uid": "4244584774",
        "password": "BY_PARAHEX-O8WM4VGRQ-REDZED"
    },
    {
        "uid": "4244585652",
        "password": "BY_PARAHEX-U0RA0LWE4-REDZED"
    },
    {
        "uid": "4244586088",
        "password": "BY_PARAHEX-S3YUB1N3P-REDZED"
    },
    {
        "uid": "4244586389",
        "password": "BY_PARAHEX-NQCGMLZRY-REDZED"
    },
    {
        "uid": "4244586686",
        "password": "BY_PARAHEX-TF8MXI6MC-REDZED"
    },
    {
        "uid": "4244586993",
        "password": "BY_PARAHEX-GX84NN6RR-REDZED"
    },
    {
        "uid": "4244587279",
        "password": "BY_PARAHEX-IH2CWMJC7-REDZED"
    },
    {
        "uid": "4244587711",
        "password": "BY_PARAHEX-HTBBVMJ5Q-REDZED"
    },
    {
        "uid": "4244587950",
        "password": "BY_PARAHEX-XZYNC9TMH-REDZED"
    },
    {
        "uid": "4244588322",
        "password": "BY_PARAHEX-45WNJKWER-REDZED"
    },
    {
        "uid": "4244588560",
        "password": "BY_PARAHEX-SRVKWABFX-REDZED"
    },
    {
        "uid": "4244588793",
        "password": "BY_PARAHEX-GNR8MMWNQ-REDZED"
    },
    {
        "uid": "4244589110",
        "password": "BY_PARAHEX-ZKBFIJCC7-REDZED"
    },
    {
        "uid": "4244589449",
        "password": "BY_PARAHEX-MWUCZ0R3A-REDZED"
    },
    {
        "uid": "4244589745",
        "password": "BY_PARAHEX-2OOI5ELPF-REDZED"
    },
    {
        "uid": "4244590008",
        "password": "BY_PARAHEX-DCTNP1AR2-REDZED"
    },
    {
        "uid": "4244590303",
        "password": "BY_PARAHEX-DE1SPY7VN-REDZED"
    },
    {
        "uid": "4244590538",
        "password": "BY_PARAHEX-EFDEJ5QDQ-REDZED"
    },
    {
        "uid": "4244590841",
        "password": "BY_PARAHEX-SYK4YH4O8-REDZED"
    },
    {
        "uid": "4244591108",
        "password": "BY_PARAHEX-NPB2AXTDW-REDZED"
    },
    {
        "uid": "4244591335",
        "password": "BY_PARAHEX-0UP29XPCQ-REDZED"
    },
    {
        "uid": "4244591743",
        "password": "BY_PARAHEX-922G2GUHR-REDZED"
    },
    {
        "uid": "4244591997",
        "password": "BY_PARAHEX-8WLGTARUV-REDZED"
    },
    {
        "uid": "4244592201",
        "password": "BY_PARAHEX-FBVVDL8ZY-REDZED"
    },
    {
        "uid": "4244592676",
        "password": "BY_PARAHEX-WWLKLZ5FS-REDZED"
    },
    {
        "uid": "4244593014",
        "password": "BY_PARAHEX-KRNWIW8XE-REDZED"
    },
    {
        "uid": "4244593520",
        "password": "BY_PARAHEX-YSEWQHAPL-REDZED"
    },
    {
        "uid": "4244593751",
        "password": "BY_PARAHEX-40R66YD2L-REDZED"
    },
    {
        "uid": "4244594004",
        "password": "BY_PARAHEX-PHXENLGGK-REDZED"
    },
    {
        "uid": "4244594425",
        "password": "BY_PARAHEX-RT0CUBFPV-REDZED"
    },
    {
        "uid": "4244594799",
        "password": "BY_PARAHEX-TM1LV7JJF-REDZED"
    },
    {
        "uid": "4244595234",
        "password": "BY_PARAHEX-2FRPYWPWE-REDZED"
    },
    {
        "uid": "4238482847",
        "password": "BY_PARAHEX-RCTN0RQ6G-REDZED"
    },
    {
        "uid": "4238483641",
        "password": "BY_PARAHEX-OQ9OPWFYV-REDZED"
    },
    {
        "uid": "4238483930",
        "password": "BY_PARAHEX-ZDG5RAWIR-REDZED"
    },
    {
        "uid": "4238484353",
        "password": "BY_PARAHEX-9GU9UIE73-REDZED"
    },
    {
        "uid": "4238484937",
        "password": "BY_PARAHEX-JH7FIUHZ5-REDZED"
    },
    {
        "uid": "4238485421",
        "password": "BY_PARAHEX-PS7OSYGGA-REDZED"
    },
    {
        "uid": "4238486594",
        "password": "BY_PARAHEX-GFDCVWE2E-REDZED"
    },
    {
        "uid": "4238487850",
        "password": "BY_PARAHEX-LV7DZJC8B-REDZED"
    },
    {
        "uid": "4238488258",
        "password": "BY_PARAHEX-WM4LU305T-REDZED"
    },
    {
        "uid": "4238488913",
        "password": "BY_PARAHEX-R00SAMFHW-REDZED"
    },
    {
        "uid": "4238489569",
        "password": "BY_PARAHEX-BXGJCV8UT-REDZED"
    },
    {
        "uid": "4238490146",
        "password": "BY_PARAHEX-DFHJRTF8C-REDZED"
    },
    {
        "uid": "4238490678",
        "password": "BY_PARAHEX-FECEORP5R-REDZED"
    },
    {
        "uid": "4238491318",
        "password": "BY_PARAHEX-5DSCHF4NP-REDZED"
    },
    {
        "uid": "4238491969",
        "password": "BY_PARAHEX-41JV5JMFC-REDZED"
    },
    {
        "uid": "4238492514",
        "password": "BY_PARAHEX-W67ZMEE6U-REDZED"
    },
    {
        "uid": "4238493184",
        "password": "BY_PARAHEX-PXMQ5TBNC-REDZED"
    },
    {
        "uid": "4238493653",
        "password": "BY_PARAHEX-R7UZJXDGO-REDZED"
    },
    {
        "uid": "4238494245",
        "password": "BY_PARAHEX-HHAFWMXP3-REDZED"
    },
    {
        "uid": "4238494827",
        "password": "BY_PARAHEX-Y7KVTZ5RT-REDZED"
    },
    {
        "uid": "4238495427",
        "password": "BY_PARAHEX-6YAYM6ULU-REDZED"
    },
    {
        "uid": "4238495867",
        "password": "BY_PARAHEX-NJSP40UGZ-REDZED"
    },
    {
        "uid": "4238496398",
        "password": "BY_PARAHEX-KK7CPDGLT-REDZED"
    },
    {
        "uid": "4238497001",
        "password": "BY_PARAHEX-8QO0IS2KN-REDZED"
    },
    {
        "uid": "4238497630",
        "password": "BY_PARAHEX-PLYUTIN7S-REDZED"
    },
    {
        "uid": "4238498243",
        "password": "BY_PARAHEX-ALEWMHXVG-REDZED"
    },
    {
        "uid": "4238498684",
        "password": "BY_PARAHEX-DN0WIAVVU-REDZED"
    },
    {
        "uid": "4238499310",
        "password": "BY_PARAHEX-NQQZM2QKD-REDZED"
    },
    {
        "uid": "4238499839",
        "password": "BY_PARAHEX-AUES26TUK-REDZED"
    },
    {
        "uid": "4238500354",
        "password": "BY_PARAHEX-8XVQQUU5X-REDZED"
    },
    {
        "uid": "4238500872",
        "password": "BY_PARAHEX-MFKAHHBGL-REDZED"
    },
    {
        "uid": "4238501366",
        "password": "BY_PARAHEX-P5ECLO087-REDZED"
    },
    {
        "uid": "4238502287",
        "password": "BY_PARAHEX-KDJ9V0ZHC-REDZED"
    },
    {
        "uid": "4238502700",
        "password": "BY_PARAHEX-YNWAVYIML-REDZED"
    },
    {
        "uid": "4238503351",
        "password": "BY_PARAHEX-DFJ3UKDKD-REDZED"
    },
    {
        "uid": "4238503965",
        "password": "BY_PARAHEX-3NTBFMCPO-REDZED"
    },
    {
        "uid": "4238504468",
        "password": "BY_PARAHEX-PBUBZF9KV-REDZED"
    },
    {
        "uid": "4238505408",
        "password": "BY_PARAHEX-5YZSBUD5V-REDZED"
    },
    {
        "uid": "4238506061",
        "password": "BY_PARAHEX-NE7HPRZJY-REDZED"
    },
    {
        "uid": "4238507104",
        "password": "BY_PARAHEX-VMUID1IOL-REDZED"
    },
    {
        "uid": "4238507485",
        "password": "BY_PARAHEX-AQEXCSFCV-REDZED"
    },
    {
        "uid": "4238507854",
        "password": "BY_PARAHEX-JF4CTEXV7-REDZED"
    },
    {
        "uid": "4238508378",
        "password": "BY_PARAHEX-7H8IX0ISP-REDZED"
    },
    {
        "uid": "4238509230",
        "password": "BY_PARAHEX-EZN9RFLJS-REDZED"
    },
    {
        "uid": "4238509632",
        "password": "BY_PARAHEX-RCEOFUDJK-REDZED"
    },
    {
        "uid": "4238510706",
        "password": "BY_PARAHEX-7SYKHLEBJ-REDZED"
    },
    {
        "uid": "4238511102",
        "password": "BY_PARAHEX-JZZ44ZTXH-REDZED"
    },
    {
        "uid": "4238511876",
        "password": "BY_PARAHEX-VZVOVJG63-REDZED"
    },
    {
        "uid": "4238512340",
        "password": "BY_PARAHEX-TGFANPWST-REDZED"
    },
    {
        "uid": "4238512899",
        "password": "BY_PARAHEX-Z99QSJYRJ-REDZED"
    },
    {
        "uid": "4238513158",
        "password": "BY_PARAHEX-56ABQONU3-REDZED"
    },
    {
        "uid": "4238513754",
        "password": "BY_PARAHEX-IKP9FG3YZ-REDZED"
    },
    {
        "uid": "4238514292",
        "password": "BY_PARAHEX-LKZYNPRPK-REDZED"
    },
    {
        "uid": "4238514880",
        "password": "BY_PARAHEX-7PCRCA1KI-REDZED"
    },
    {
        "uid": "4238515552",
        "password": "BY_PARAHEX-AJMRU2KAU-REDZED"
    },
    {
        "uid": "4238515816",
        "password": "BY_PARAHEX-RGS7MM5R8-REDZED"
    },
    {
        "uid": "4238516592",
        "password": "BY_PARAHEX-ZNVDOB1CA-REDZED"
    },
    {
        "uid": "4238517090",
        "password": "BY_PARAHEX-Z73K3WSRY-REDZED"
    },
    {
        "uid": "4238517588",
        "password": "BY_PARAHEX-RFSJHAOCB-REDZED"
    },
    {
        "uid": "4238518085",
        "password": "BY_PARAHEX-EALVJNY8W-REDZED"
    },
    {
        "uid": "4238518695",
        "password": "BY_PARAHEX-5HWUUQ0BR-REDZED"
    },
    {
        "uid": "4238519121",
        "password": "BY_PARAHEX-UKXDBY2QN-REDZED"
    },
    {
        "uid": "4238519799",
        "password": "BY_PARAHEX-AGXRLILDS-REDZED"
    },
    {
        "uid": "4238520162",
        "password": "BY_PARAHEX-969HXKOLO-REDZED"
    },
    {
        "uid": "4238521031",
        "password": "BY_PARAHEX-RDYAJSYXZ-REDZED"
    },
    {
        "uid": "4238521597",
        "password": "BY_PARAHEX-HA0FJUGFX-REDZED"
    },
    {
        "uid": "4238522353",
        "password": "BY_PARAHEX-VLSLAYJK0-REDZED"
    },
    {
        "uid": "4238522929",
        "password": "BY_PARAHEX-JVWVIRYS4-REDZED"
    },
    {
        "uid": "4238523207",
        "password": "BY_PARAHEX-BIQYNPYI7-REDZED"
    },
    {
        "uid": "4238523536",
        "password": "BY_PARAHEX-X9AEZO0FX-REDZED"
    },
    {
        "uid": "4238524036",
        "password": "BY_PARAHEX-5EBTVYPIK-REDZED"
    },
    {
        "uid": "4238524347",
        "password": "BY_PARAHEX-H9XA5ZC8M-REDZED"
    },
    {
        "uid": "4238524780",
        "password": "BY_PARAHEX-RI6NTPKX9-REDZED"
    },
    {
        "uid": "4238525287",
        "password": "BY_PARAHEX-3IX1ASH2O-REDZED"
    },
    {
        "uid": "4238525858",
        "password": "BY_PARAHEX-DABQNDQDZ-REDZED"
    },
    {
        "uid": "4238526194",
        "password": "BY_PARAHEX-WQCBNKANQ-REDZED"
    },
    {
        "uid": "4238526522",
        "password": "BY_PARAHEX-AGNNPWOCA-REDZED"
    },
    {
        "uid": "4238526911",
        "password": "BY_PARAHEX-SXRJJMTCQ-REDZED"
    },
    {
        "uid": "4238527541",
        "password": "BY_PARAHEX-OOK3XQLPP-REDZED"
    },
    {
        "uid": "4238528065",
        "password": "BY_PARAHEX-Q6B2SDGMH-REDZED"
    },
    {
        "uid": "4238528377",
        "password": "BY_PARAHEX-EFY30GMVZ-REDZED"
    },
    {
        "uid": "4238528931",
        "password": "BY_PARAHEX-SJRV7E778-REDZED"
    },
    {
        "uid": "4238529421",
        "password": "BY_PARAHEX-ARBRXMRK8-REDZED"
    },
    {
        "uid": "4238529883",
        "password": "BY_PARAHEX-JHMPO1YKW-REDZED"
    },
    {
        "uid": "4238530356",
        "password": "BY_PARAHEX-O8875VCMY-REDZED"
    },
    {
        "uid": "4238530940",
        "password": "BY_PARAHEX-ESVRTU3SL-REDZED"
    },
    {
        "uid": "4238531522",
        "password": "BY_PARAHEX-OWK05EU35-REDZED"
    },
    {
        "uid": "4238532200",
        "password": "BY_PARAHEX-XLEQY6ZM4-REDZED"
    },
    {
        "uid": "4238533234",
        "password": "BY_PARAHEX-1ABHZO59N-REDZED"
    },
    {
        "uid": "4238533822",
        "password": "BY_PARAHEX-SHHL980X4-REDZED"
    },
    {
        "uid": "4238534333",
        "password": "BY_PARAHEX-DO5BQG0ST-REDZED"
    },
    {
        "uid": "4238534939",
        "password": "BY_PARAHEX-KPLFHUPB7-REDZED"
    },
    {
        "uid": "4238535543",
        "password": "BY_PARAHEX-JIQPHM7LV-REDZED"
    },
    {
        "uid": "4238536282",
        "password": "BY_PARAHEX-GFVVL2QO1-REDZED"
    },
    {
        "uid": "4238536913",
        "password": "BY_PARAHEX-ZMJULIMOC-REDZED"
    },
    {
        "uid": "4238537410",
        "password": "BY_PARAHEX-74DCFWNZP-REDZED"
    },
    {
        "uid": "4238537860",
        "password": "BY_PARAHEX-1AC0TTHJW-REDZED"
    },
    {
        "uid": "4238538902",
        "password": "BY_PARAHEX-DQQDNQCSW-REDZED"
    },
    {
        "uid": "4238539393",
        "password": "BY_PARAHEX-NPGGDOJ7L-REDZED"
    },
    {
        "uid": "4238539726",
        "password": "BY_PARAHEX-PRGPQYODS-REDZED"
    },
    {
        "uid": "4238540363",
        "password": "BY_PARAHEX-0NGWEXBCR-REDZED"
    },
    {
        "uid": "4238540973",
        "password": "BY_PARAHEX-F3PTMOI2W-REDZED"
    },
    {
        "uid": "4238541992",
        "password": "BY_PARAHEX-LRGGDFC3M-REDZED"
    },
    {
        "uid": "4238542462",
        "password": "BY_PARAHEX-YM3NWGGIL-REDZED"
    },
    {
        "uid": "4238542943",
        "password": "BY_PARAHEX-T5TLCWPT5-REDZED"
    },
    {
        "uid": "4238543641",
        "password": "BY_PARAHEX-3AJXAAE7H-REDZED"
    },
    {
        "uid": "4238544469",
        "password": "BY_PARAHEX-VUY2N0ENS-REDZED"
    },
    {
        "uid": "4238544837",
        "password": "BY_PARAHEX-SZAAUBUET-REDZED"
    },
    {
        "uid": "4238545225",
        "password": "BY_PARAHEX-XPJW0BYKY-REDZED"
    },
    {
        "uid": "4238545755",
        "password": "BY_PARAHEX-YHXTIPJ5O-REDZED"
    },
    {
        "uid": "4238546094",
        "password": "BY_PARAHEX-K7DAWRXXR-REDZED"
    },
    {
        "uid": "4238546700",
        "password": "BY_PARAHEX-IYHTWWBI6-REDZED"
    },
    {
        "uid": "4238547052",
        "password": "BY_PARAHEX-TL8RQ9X0R-REDZED"
    },
    {
        "uid": "4238547385",
        "password": "BY_PARAHEX-9B5CB5EL6-REDZED"
    },
    {
        "uid": "4238547738",
        "password": "BY_PARAHEX-Y0T28RF9D-REDZED"
    },
    {
        "uid": "4238548296",
        "password": "BY_PARAHEX-XTOHXDGX4-REDZED"
    },
    {
        "uid": "4238548899",
        "password": "BY_PARAHEX-PBBUAMYF9-REDZED"
    },
    {
        "uid": "4238549363",
        "password": "BY_PARAHEX-QQO1JTOHT-REDZED"
    },
    {
        "uid": "4238550098",
        "password": "BY_PARAHEX-C1O9LQGP0-REDZED"
    },
    {
        "uid": "4238550595",
        "password": "BY_PARAHEX-Z0J5DYFL6-REDZED"
    },
    {
        "uid": "4238551106",
        "password": "BY_PARAHEX-4NUB1PPK9-REDZED"
    },
    {
        "uid": "4238551635",
        "password": "BY_PARAHEX-M3BXJL4IW-REDZED"
    },
    {
        "uid": "4238552641",
        "password": "BY_PARAHEX-7OPFLLII8-REDZED"
    },
    {
        "uid": "4238553118",
        "password": "BY_PARAHEX-DMKYA0FEB-REDZED"
    },
    {
        "uid": "4238553470",
        "password": "BY_PARAHEX-6JADCHQCS-REDZED"
    },
    {
        "uid": "4238553792",
        "password": "BY_PARAHEX-6HBHDXKVK-REDZED"
    },
    {
        "uid": "4238554721",
        "password": "BY_PARAHEX-5ENAFXBVF-REDZED"
    },
    {
        "uid": "4238555199",
        "password": "BY_PARAHEX-R6FMK3NOE-REDZED"
    },
    {
        "uid": "4238555604",
        "password": "BY_PARAHEX-WCQDNW2SD-REDZED"
    },
    {
        "uid": "4238556020",
        "password": "BY_PARAHEX-9DVB4YVJI-REDZED"
    },
    {
        "uid": "4238556468",
        "password": "BY_PARAHEX-JNOO275VS-REDZED"
    },
    {
        "uid": "4238556900",
        "password": "BY_PARAHEX-KOKMCVC40-REDZED"
    },
    {
        "uid": "4238557532",
        "password": "BY_PARAHEX-VMZ62Y6OP-REDZED"
    },
    {
        "uid": "4238557946",
        "password": "BY_PARAHEX-3AQB0QIOY-REDZED"
    },
    {
        "uid": "4238558260",
        "password": "BY_PARAHEX-10ODBSPYL-REDZED"
    },
    {
        "uid": "4238558678",
        "password": "BY_PARAHEX-RCBUYNDME-REDZED"
    },
    {
        "uid": "4238558944",
        "password": "BY_PARAHEX-II0K3D9X0-REDZED"
    },
    {
        "uid": "4238559219",
        "password": "BY_PARAHEX-H88ZBOEFP-REDZED"
    },
    {
        "uid": "4238559426",
        "password": "BY_PARAHEX-1PPGQUHNE-REDZED"
    },
    {
        "uid": "4238559678",
        "password": "BY_PARAHEX-H2G0EEDNC-REDZED"
    },
    {
        "uid": "4238559930",
        "password": "BY_PARAHEX-QXOUKCVIU-REDZED"
    },
    {
        "uid": "4238560672",
        "password": "BY_PARAHEX-HA8WRQFOC-REDZED"
    },
    {
        "uid": "4238563926",
        "password": "BY_PARAHEX-4OYSOKQAN-REDZED"
    },
    {
        "uid": "4238564456",
        "password": "BY_PARAHEX-PHNKUHK5V-REDZED"
    },
    {
        "uid": "4238564782",
        "password": "BY_PARAHEX-6EPQCBV6A-REDZED"
    },
    {
        "uid": "4238565045",
        "password": "BY_PARAHEX-HLGSIQOKV-REDZED"
    },
    {
        "uid": "4238565329",
        "password": "BY_PARAHEX-C3JUG944D-REDZED"
    },
    {
        "uid": "4238565565",
        "password": "BY_PARAHEX-BDZWNOW9S-REDZED"
    },
    {
        "uid": "4238565955",
        "password": "BY_PARAHEX-1FGEE2NYK-REDZED"
    },
    {
        "uid": "4238566151",
        "password": "BY_PARAHEX-WHIOE94JU-REDZED"
    },
    {
        "uid": "4238566445",
        "password": "BY_PARAHEX-1VUP9FLD3-REDZED"
    },
    {
        "uid": "4238566684",
        "password": "BY_PARAHEX-HOHLPAUFO-REDZED"
    },
    {
        "uid": "4238566883",
        "password": "BY_PARAHEX-9AYOQZGMW-REDZED"
    },
    {
        "uid": "4238567189",
        "password": "BY_PARAHEX-QVIBWSTPJ-REDZED"
    },
    {
        "uid": "4238567531",
        "password": "BY_PARAHEX-SRSKRG9FX-REDZED"
    },
    {
        "uid": "4238567738",
        "password": "BY_PARAHEX-BZPZRZDGN-REDZED"
    },
    {
        "uid": "4238568077",
        "password": "BY_PARAHEX-AHW5DFAWX-REDZED"
    },
    {
        "uid": "4238568605",
        "password": "BY_PARAHEX-OYAJ3FKIQ-REDZED"
    },
    {
        "uid": "4238571392",
        "password": "BY_PARAHEX-2TOERXPIA-REDZED"
    },
    {
        "uid": "4238573456",
        "password": "BY_PARAHEX-L08XUC8TR-REDZED"
    },
    {
        "uid": "4238573949",
        "password": "BY_PARAHEX-YKWPA2B94-REDZED"
    },
    {
        "uid": "4238574650",
        "password": "BY_PARAHEX-A2WLLVO54-REDZED"
    },
    {
        "uid": "4238575110",
        "password": "BY_PARAHEX-S6SDSIMIE-REDZED"
    },
    {
        "uid": "4238575937",
        "password": "BY_PARAHEX-DJACXTSIP-REDZED"
    },
    {
        "uid": "4238576628",
        "password": "BY_PARAHEX-BOYS7ASZY-REDZED"
    },
    {
        "uid": "4238576934",
        "password": "BY_PARAHEX-0LJ7R0ABR-REDZED"
    },
    {
        "uid": "4238577248",
        "password": "BY_PARAHEX-YYQHGCSTH-REDZED"
    },
    {
        "uid": "4238577554",
        "password": "BY_PARAHEX-UXO4GEQ4O-REDZED"
    },
    {
        "uid": "4238577894",
        "password": "BY_PARAHEX-EM2MFGOF2-REDZED"
    },
    {
        "uid": "4238578191",
        "password": "BY_PARAHEX-OBAGFBCZG-REDZED"
    },
    {
        "uid": "4238578792",
        "password": "BY_PARAHEX-OY1F8TQ0Y-REDZED"
    },
    {
        "uid": "4238579043",
        "password": "BY_PARAHEX-RMX79XO9Y-REDZED"
    },
    {
        "uid": "4238579412",
        "password": "BY_PARAHEX-SIXXZNIGP-REDZED"
    },
    {
        "uid": "4238579705",
        "password": "BY_PARAHEX-QNLI2DZ0I-REDZED"
    },
    {
        "uid": "4238580024",
        "password": "BY_PARAHEX-FOGMYCUAD-REDZED"
    },
    {
        "uid": "4238580305",
        "password": "BY_PARAHEX-NUF2H9RQP-REDZED"
    },
    {
        "uid": "4238580748",
        "password": "BY_PARAHEX-G2YIIWKLR-REDZED"
    },
    {
        "uid": "4238580979",
        "password": "BY_PARAHEX-LJL6KBSI2-REDZED"
    },
    {
        "uid": "4238581903",
        "password": "BY_PARAHEX-EAECJLPPH-REDZED"
    },
    {
        "uid": "4238582275",
        "password": "BY_PARAHEX-6PYLOTWOE-REDZED"
    },
    {
        "uid": "4238582682",
        "password": "BY_PARAHEX-7RXHTESP6-REDZED"
    },
    {
        "uid": "4238583038",
        "password": "BY_PARAHEX-0X3JL5TSH-REDZED"
    },
    {
        "uid": "4238583601",
        "password": "BY_PARAHEX-5VBMUONX8-REDZED"
    },
    {
        "uid": "4238583946",
        "password": "BY_PARAHEX-JFGDB52DP-REDZED"
    },
    {
        "uid": "4238584382",
        "password": "BY_PARAHEX-HN4C0LQL6-REDZED"
    },
    {
        "uid": "4238584755",
        "password": "BY_PARAHEX-1P6EXUTYS-REDZED"
    },
    {
        "uid": "4238585862",
        "password": "BY_PARAHEX-LYDNBKTRM-REDZED"
    },
    {
        "uid": "4238592997",
        "password": "BY_PARAHEX-O9YNG8XOT-REDZED"
    },
    {
        "uid": "4238595231",
        "password": "BY_PARAHEX-JLYAPYGLQ-REDZED"
    },
    {
        "uid": "4238597305",
        "password": "BY_PARAHEX-XGRHE7OZQ-REDZED"
    },
    {
        "uid": "4238600200",
        "password": "BY_PARAHEX-UQUVXCJGE-REDZED"
    },
    {
        "uid": "4238602395",
        "password": "BY_PARAHEX-ECUTAD9XD-REDZED"
    },
    {
        "uid": "4238604117",
        "password": "BY_PARAHEX-OZTBTGRBK-REDZED"
    },
    {
        "uid": "4238606076",
        "password": "BY_PARAHEX-ZNKO8BJSB-REDZED"
    },
    {
        "uid": "4238607740",
        "password": "BY_PARAHEX-BGLYOE3LB-REDZED"
    },
    {
        "uid": "4238612681",
        "password": "BY_PARAHEX-9PYYKAFGP-REDZED"
    },
    {
        "uid": "4238621738",
        "password": "BY_PARAHEX-SS9UBSFIJ-REDZED"
    },
    {
        "uid": "4238624073",
        "password": "BY_PARAHEX-T1PAPQRVH-REDZED"
    },
    {
        "uid": "4238627110",
        "password": "BY_PARAHEX-34UTV1A0M-REDZED"
    },
    {
        "uid": "4238629218",
        "password": "BY_PARAHEX-I973FPOFS-REDZED"
    },
    {
        "uid": "4238631436",
        "password": "BY_PARAHEX-0SPAHFOLA-REDZED"
    },
    {
        "uid": "4238634099",
        "password": "BY_PARAHEX-JDCGRGNQZ-REDZED"
    },
    {
        "uid": "4238635674",
        "password": "BY_PARAHEX-AOQAVUHXE-REDZED"
    },
    {
        "uid": "4238637734",
        "password": "BY_PARAHEX-XVWBSEKLP-REDZED"
    },
    {
        "uid": "4238639952",
        "password": "BY_PARAHEX-BYQHCOUOR-REDZED"
    },
    {
        "uid": "4238642204",
        "password": "BY_PARAHEX-CQXVQUACM-REDZED"
    },
    {
        "uid": "4238643455",
        "password": "BY_PARAHEX-8YSVTDEJ2-REDZED"
    },
    {
        "uid": "4238645809",
        "password": "BY_PARAHEX-F3UDOKVJF-REDZED"
    },
    {
        "uid": "4238648154",
        "password": "BY_PARAHEX-SO6RGWCPN-REDZED"
    },
    {
        "uid": "4238651027",
        "password": "BY_PARAHEX-HY8ZLDX5Q-REDZED"
    },
    {
        "uid": "4238652118",
        "password": "BY_PARAHEX-1CI4QNAIU-REDZED"
    },
    {
        "uid": "4238653727",
        "password": "BY_PARAHEX-TM923AHJB-REDZED"
    },
    {
        "uid": "4238654910",
        "password": "BY_PARAHEX-NITXH0OJZ-REDZED"
    },
    {
        "uid": "4238657102",
        "password": "BY_PARAHEX-TPOJLSZMB-REDZED"
    },
    {
        "uid": "4238661041",
        "password": "BY_PARAHEX-V1SFNGEJA-REDZED"
    },
    {
        "uid": "4238663833",
        "password": "BY_PARAHEX-T7EHIOYRN-REDZED"
    },
    {
        "uid": "4238667535",
        "password": "BY_PARAHEX-V46G2CAJZ-REDZED"
    },
    {
        "uid": "4238669861",
        "password": "BY_PARAHEX-COB9C8MG6-REDZED"
    },
    {
        "uid": "4238671626",
        "password": "BY_PARAHEX-OFW3LYJT2-REDZED"
    },
    {
        "uid": "4238672588",
        "password": "BY_PARAHEX-GXJAIRW9W-REDZED"
    },
    {
        "uid": "4238673087",
        "password": "BY_PARAHEX-1REHQBG1G-REDZED"
    },
    {
        "uid": "4238673386",
        "password": "BY_PARAHEX-6UMA4CFYN-REDZED"
    },
    {
        "uid": "4238673634",
        "password": "BY_PARAHEX-VUYF5YCSG-REDZED"
    },
    {
        "uid": "4238673943",
        "password": "BY_PARAHEX-QOLWG444J-REDZED"
    },
    {
        "uid": "4238674323",
        "password": "BY_PARAHEX-MC6E8RSQV-REDZED"
    },
    {
        "uid": "4238674702",
        "password": "BY_PARAHEX-XEZXEHXDY-REDZED"
    },
    {
        "uid": "4238675013",
        "password": "BY_PARAHEX-9CQ5KU6NR-REDZED"
    },
    {
        "uid": "4238675272",
        "password": "BY_PARAHEX-R33D4OTNC-REDZED"
    },
    {
        "uid": "4238675579",
        "password": "BY_PARAHEX-GJHX1VP9T-REDZED"
    },
    {
        "uid": "4238676069",
        "password": "BY_PARAHEX-LRFVPD1VM-REDZED"
    },
    {
        "uid": "4238676357",
        "password": "BY_PARAHEX-CODOAKFV4-REDZED"
    },
    {
        "uid": "4238676510",
        "password": "BY_PARAHEX-TJHPLQA0Y-REDZED"
    },
    {
        "uid": "4238676901",
        "password": "BY_PARAHEX-NFMZGT9TE-REDZED"
    },
    {
        "uid": "4238677150",
        "password": "BY_PARAHEX-41TFOOKXX-REDZED"
    },
    {
        "uid": "4238677483",
        "password": "BY_PARAHEX-RTCDFHJKY-REDZED"
    },
    {
        "uid": "4238677622",
        "password": "BY_PARAHEX-8VUVPOESW-REDZED"
    },
    {
        "uid": "4238678122",
        "password": "BY_PARAHEX-JS0KJFE7R-REDZED"
    },
    {
        "uid": "4238678467",
        "password": "BY_PARAHEX-YND3DK9XY-REDZED"
    },
    {
        "uid": "4238678778",
        "password": "BY_PARAHEX-DWM1D5Z37-REDZED"
    },
    {
        "uid": "4238679115",
        "password": "BY_PARAHEX-VXEPVVJEW-REDZED"
    },
    {
        "uid": "4238679354",
        "password": "BY_PARAHEX-XXBWD0QXK-REDZED"
    },
    {
        "uid": "4238679675",
        "password": "BY_PARAHEX-Q9CDTRUBH-REDZED"
    },
    {
        "uid": "4238679956",
        "password": "BY_PARAHEX-THOETCQ1H-REDZED"
    },
    {
        "uid": "4238680232",
        "password": "BY_PARAHEX-ZAFDZGLGJ-REDZED"
    },
    {
        "uid": "4238680439",
        "password": "BY_PARAHEX-OYNXIAWFI-REDZED"
    },
    {
        "uid": "4238680744",
        "password": "BY_PARAHEX-AZC8ELJNH-REDZED"
    },
    {
        "uid": "4238680953",
        "password": "BY_PARAHEX-6VMBXJWE0-REDZED"
    },
    {
        "uid": "4238681107",
        "password": "BY_PARAHEX-DQE4Z4D5J-REDZED"
    },
    {
        "uid": "4238681326",
        "password": "BY_PARAHEX-YZBJDGFAC-REDZED"
    },
    {
        "uid": "4238681507",
        "password": "BY_PARAHEX-GIXAZA034-REDZED"
    },
    {
        "uid": "4238681678",
        "password": "BY_PARAHEX-0UUZNPCIM-REDZED"
    },
    {
        "uid": "4238681823",
        "password": "BY_PARAHEX-CVSMKFMQS-REDZED"
    },
    {
        "uid": "4238682126",
        "password": "BY_PARAHEX-UGRLZURGE-REDZED"
    },
    {
        "uid": "4238682312",
        "password": "BY_PARAHEX-ERKP6Y3XU-REDZED"
    },
    {
        "uid": "4238682479",
        "password": "BY_PARAHEX-OUHB1QYWN-REDZED"
    },
    {
        "uid": "4238682648",
        "password": "BY_PARAHEX-HMD6M9WZN-REDZED"
    },
    {
        "uid": "4238682836",
        "password": "BY_PARAHEX-MCNQ2BASW-REDZED"
    },
    {
        "uid": "4238683036",
        "password": "BY_PARAHEX-TOYUTBBFU-REDZED"
    },
    {
        "uid": "4238683235",
        "password": "BY_PARAHEX-KNDYFVRSB-REDZED"
    },
    {
        "uid": "4238683369",
        "password": "BY_PARAHEX-9GV6ILZSA-REDZED"
    },
    {
        "uid": "4238683601",
        "password": "BY_PARAHEX-B99QO5JZP-REDZED"
    },
    {
        "uid": "4238683792",
        "password": "BY_PARAHEX-QE0C1MKLI-REDZED"
    },
    {
        "uid": "4238684105",
        "password": "BY_PARAHEX-IJY23JBYO-REDZED"
    },
    {
        "uid": "4238684313",
        "password": "BY_PARAHEX-IGLM14EFX-REDZED"
    },
    {
        "uid": "4238684495",
        "password": "BY_PARAHEX-HKI6SKUJU-REDZED"
    },
    {
        "uid": "4238684625",
        "password": "BY_PARAHEX-GXOJHGMSY-REDZED"
    },
    {
        "uid": "4238684841",
        "password": "BY_PARAHEX-S2DSRNTSM-REDZED"
    },
    {
        "uid": "4238685079",
        "password": "BY_PARAHEX-QZGP1LMX3-REDZED"
    },
    {
        "uid": "4238685278",
        "password": "BY_PARAHEX-0OE1A8P37-REDZED"
    },
    {
        "uid": "4238685599",
        "password": "BY_PARAHEX-MAKXXLDBZ-REDZED"
    },
    {
        "uid": "4238685832",
        "password": "BY_PARAHEX-JFE4HMEVU-REDZED"
    },
    {
        "uid": "4238686033",
        "password": "BY_PARAHEX-TAAMSZG0V-REDZED"
    },
    {
        "uid": "4238686231",
        "password": "BY_PARAHEX-FNKSBMIBY-REDZED"
    },
    {
        "uid": "4238686432",
        "password": "BY_PARAHEX-4SOS5DQQB-REDZED"
    },
    {
        "uid": "4238686583",
        "password": "BY_PARAHEX-HZDVR5EYY-REDZED"
    },
    {
        "uid": "4238686835",
        "password": "BY_PARAHEX-MTO6F4TVU-REDZED"
    },
    {
        "uid": "4238687000",
        "password": "BY_PARAHEX-92SDGGUVN-REDZED"
    },
    {
        "uid": "4238687209",
        "password": "BY_PARAHEX-JNOVNPNWT-REDZED"
    },
    {
        "uid": "4238687410",
        "password": "BY_PARAHEX-2YOWHKAPD-REDZED"
    },
    {
        "uid": "4238687603",
        "password": "BY_PARAHEX-VGOP0KUZJ-REDZED"
    },
    {
        "uid": "4238687794",
        "password": "BY_PARAHEX-EK18MPQ8Z-REDZED"
    },
    {
        "uid": "4238688010",
        "password": "BY_PARAHEX-YNLBF5SYN-REDZED"
    },
    {
        "uid": "4238688352",
        "password": "BY_PARAHEX-NSDMNBEJL-REDZED"
    },
    {
        "uid": "4238688637",
        "password": "BY_PARAHEX-RJ39PB7DK-REDZED"
    },
    {
        "uid": "4238688812",
        "password": "BY_PARAHEX-3POMRWYQA-REDZED"
    },
    {
        "uid": "4238688957",
        "password": "BY_PARAHEX-WOOHAGNPM-REDZED"
    },
    {
        "uid": "4238689127",
        "password": "BY_PARAHEX-X5EFM0SQG-REDZED"
    },
    {
        "uid": "4238689260",
        "password": "BY_PARAHEX-CNDILZ2UT-REDZED"
    },
    {
        "uid": "4238689480",
        "password": "BY_PARAHEX-GU8BU1AQG-REDZED"
    },
    {
        "uid": "4238689677",
        "password": "BY_PARAHEX-UFWNMTRAR-REDZED"
    },
    {
        "uid": "4238689886",
        "password": "BY_PARAHEX-BBHYIBSIS-REDZED"
    },
    {
        "uid": "4238690022",
        "password": "BY_PARAHEX-3GJ6GFV0Z-REDZED"
    },
    {
        "uid": "4238690252",
        "password": "BY_PARAHEX-E1MOTL9CK-REDZED"
    },
    {
        "uid": "4238690408",
        "password": "BY_PARAHEX-FCZQN64PZ-REDZED"
    },
    {
        "uid": "4238690631",
        "password": "BY_PARAHEX-3RPK2XMOS-REDZED"
    },
    {
        "uid": "4238690782",
        "password": "BY_PARAHEX-YVTFENPFN-REDZED"
    },
    {
        "uid": "4238691076",
        "password": "BY_PARAHEX-9L68QXAUG-REDZED"
    },
    {
        "uid": "4238691372",
        "password": "BY_PARAHEX-NNJVDGWGJ-REDZED"
    },
    {
        "uid": "4238691591",
        "password": "BY_PARAHEX-ISPTVB9TI-REDZED"
    },
    {
        "uid": "4238691815",
        "password": "BY_PARAHEX-TPMMZ6I7Q-REDZED"
    },
    {
        "uid": "4238692004",
        "password": "BY_PARAHEX-GCZZZ0SQT-REDZED"
    },
    {
        "uid": "4238692123",
        "password": "BY_PARAHEX-FJEZRTM8M-REDZED"
    },
    {
        "uid": "4238692304",
        "password": "BY_PARAHEX-RDNCTCIDE-REDZED"
    },
    {
        "uid": "4238692473",
        "password": "BY_PARAHEX-BZLX48OWH-REDZED"
    },
    {
        "uid": "4238692727",
        "password": "BY_PARAHEX-WUN4ACUGZ-REDZED"
    },
    {
        "uid": "4238693217",
        "password": "BY_PARAHEX-FWJDNUI7C-REDZED"
    },
    {
        "uid": "4238693408",
        "password": "BY_PARAHEX-0QGJPQSLN-REDZED"
    },
    {
        "uid": "4238693620",
        "password": "BY_PARAHEX-BJPAR6RWN-REDZED"
    },
    {
        "uid": "4238693794",
        "password": "BY_PARAHEX-EULKNXFK5-REDZED"
    },
    {
        "uid": "4238693993",
        "password": "BY_PARAHEX-BCAIYTPNO-REDZED"
    },
    {
        "uid": "4238694257",
        "password": "BY_PARAHEX-KR2RJFDIW-REDZED"
    },
    {
        "uid": "4238694562",
        "password": "BY_PARAHEX-KICCDJOJY-REDZED"
    },
    {
        "uid": "4238695055",
        "password": "BY_PARAHEX-Y6SXGK3RQ-REDZED"
    },
    {
        "uid": "4238695411",
        "password": "BY_PARAHEX-QAS38CAPJ-REDZED"
    },
    {
        "uid": "4238695643",
        "password": "BY_PARAHEX-2DWQ1XHJO-REDZED"
    },
    {
        "uid": "4238695810",
        "password": "BY_PARAHEX-XAATOADNU-REDZED"
    },
    {
        "uid": "4238696130",
        "password": "BY_PARAHEX-93UREL6KQ-REDZED"
    },
    {
        "uid": "4238696358",
        "password": "BY_PARAHEX-J6LWZVTPP-REDZED"
    },
    {
        "uid": "4238696652",
        "password": "BY_PARAHEX-Y8WIFO6WJ-REDZED"
    },
    {
        "uid": "4238696912",
        "password": "BY_PARAHEX-UW8KYVMEY-REDZED"
    },
    {
        "uid": "4238697157",
        "password": "BY_PARAHEX-ZJZZEV4KC-REDZED"
    },
    {
        "uid": "4238697437",
        "password": "BY_PARAHEX-5CS2NB5UB-REDZED"
    },
    {
        "uid": "4238697643",
        "password": "BY_PARAHEX-RWXAYNG3J-REDZED"
    },
    {
        "uid": "4238697897",
        "password": "BY_PARAHEX-KRQZJNYVG-REDZED"
    },
    {
        "uid": "4238698167",
        "password": "BY_PARAHEX-F9QYYPTDL-REDZED"
    },
    {
        "uid": "4238698386",
        "password": "BY_PARAHEX-3SSMZZAM3-REDZED"
    },
    {
        "uid": "4238698614",
        "password": "BY_PARAHEX-LUHDBMFX5-REDZED"
    },
    {
        "uid": "4238698789",
        "password": "BY_PARAHEX-YY85Q1S8E-REDZED"
    },
    {
        "uid": "4238698999",
        "password": "BY_PARAHEX-S458AKOMQ-REDZED"
    },
    {
        "uid": "4238699225",
        "password": "BY_PARAHEX-M0GDUFZA9-REDZED"
    },
    {
        "uid": "4238699543",
        "password": "BY_PARAHEX-BA3BQE3FO-REDZED"
    },
    {
        "uid": "4238699744",
        "password": "BY_PARAHEX-V3Z0SQGIP-REDZED"
    },
    {
        "uid": "4238699978",
        "password": "BY_PARAHEX-T29GIQIDQ-REDZED"
    },
    {
        "uid": "4238700178",
        "password": "BY_PARAHEX-PSDDG8M23-REDZED"
    },
    {
        "uid": "4238700387",
        "password": "BY_PARAHEX-WWMPNIPD0-REDZED"
    },
    {
        "uid": "4238700670",
        "password": "BY_PARAHEX-FFP7YHRMP-REDZED"
    },
    {
        "uid": "4238700872",
        "password": "BY_PARAHEX-FJFLXX6CM-REDZED"
    },
    {
        "uid": "4238701164",
        "password": "BY_PARAHEX-KJE1ZTVDY-REDZED"
    },
    {
        "uid": "4238701380",
        "password": "BY_PARAHEX-ZPLYGOFZ6-REDZED"
    },
    {
        "uid": "4238701609",
        "password": "BY_PARAHEX-QCCJ5RAUM-REDZED"
    },
    {
        "uid": "4238701767",
        "password": "BY_PARAHEX-6GANH4JFH-REDZED"
    },
    {
        "uid": "4238702025",
        "password": "BY_PARAHEX-FQFBCXHCQ-REDZED"
    },
    {
        "uid": "4238702220",
        "password": "BY_PARAHEX-C7CRUAFKA-REDZED"
    },
    {
        "uid": "4238702377",
        "password": "BY_PARAHEX-AQIZ71ICZ-REDZED"
    },
    {
        "uid": "4238702582",
        "password": "BY_PARAHEX-QZ42FKQ2Z-REDZED"
    },
    {
        "uid": "4238702745",
        "password": "BY_PARAHEX-J5UM2FXBB-REDZED"
    },
    {
        "uid": "4238702907",
        "password": "BY_PARAHEX-XDVCJVOZZ-REDZED"
    },
    {
        "uid": "4238703096",
        "password": "BY_PARAHEX-EQRDGDVWP-REDZED"
    },
    {
        "uid": "4238703320",
        "password": "BY_PARAHEX-MG1W0NED2-REDZED"
    },
    {
        "uid": "4238703606",
        "password": "BY_PARAHEX-I7I4KPEUB-REDZED"
    },
    {
        "uid": "4238703826",
        "password": "BY_PARAHEX-6SRPUZJGU-REDZED"
    },
    {
        "uid": "4238704263",
        "password": "BY_PARAHEX-USKIPYEAP-REDZED"
    },
    {
        "uid": "4238704448",
        "password": "BY_PARAHEX-UXVVHCJGH-REDZED"
    },
    {
        "uid": "4238704683",
        "password": "BY_PARAHEX-0CS2KBY2S-REDZED"
    },
    {
        "uid": "4238704842",
        "password": "BY_PARAHEX-1EY3JZLFW-REDZED"
    },
    {
        "uid": "4238705111",
        "password": "BY_PARAHEX-QPFR9M7NN-REDZED"
    },
    {
        "uid": "4238705280",
        "password": "BY_PARAHEX-2ZAWSJL8X-REDZED"
    },
    {
        "uid": "4238705586",
        "password": "BY_PARAHEX-ZXKMDMSWC-REDZED"
    },
    {
        "uid": "4238705919",
        "password": "BY_PARAHEX-UHIZSJECQ-REDZED"
    },
    {
        "uid": "4238706161",
        "password": "BY_PARAHEX-TTSXHR83Z-REDZED"
    },
    {
        "uid": "4238706448",
        "password": "BY_PARAHEX-BKDYU2M0E-REDZED"
    },
    {
        "uid": "4238706760",
        "password": "BY_PARAHEX-BMLCXQ510-REDZED"
    },
    {
        "uid": "4238707094",
        "password": "BY_PARAHEX-HZHQPO6HK-REDZED"
    },
    {
        "uid": "4238707365",
        "password": "BY_PARAHEX-LJUBQQE2P-REDZED"
    },
    {
        "uid": "4238707610",
        "password": "BY_PARAHEX-FM1UYOSMW-REDZED"
    },
    {
        "uid": "4238707860",
        "password": "BY_PARAHEX-LVHPAUNR0-REDZED"
    },
    {
        "uid": "4238708171",
        "password": "BY_PARAHEX-NDCZEKXMQ-REDZED"
    },
    {
        "uid": "4238708558",
        "password": "BY_PARAHEX-SPDAL9WN1-REDZED"
    },
    {
        "uid": "4238709003",
        "password": "BY_PARAHEX-XSRJKMVJE-REDZED"
    },
    {
        "uid": "4238709305",
        "password": "BY_PARAHEX-G6SMVHQ0N-REDZED"
    },
    {
        "uid": "4238709550",
        "password": "BY_PARAHEX-ZNGWOQ9BJ-REDZED"
    },
    {
        "uid": "4238710010",
        "password": "BY_PARAHEX-DSQGRWOBD-REDZED"
    },
    {
        "uid": "4238710353",
        "password": "BY_PARAHEX-WHLXJLGQW-REDZED"
    },
    {
        "uid": "4238710661",
        "password": "BY_PARAHEX-QEADTPBBJ-REDZED"
    },
    {
        "uid": "4238711165",
        "password": "BY_PARAHEX-XW3ZVRNM4-REDZED"
    },
    {
        "uid": "4238711668",
        "password": "BY_PARAHEX-YKPRMCR4F-REDZED"
    },
    {
        "uid": "4238712099",
        "password": "BY_PARAHEX-JYGBRWQ17-REDZED"
    },
    {
        "uid": "4238712451",
        "password": "BY_PARAHEX-F2DROHKT5-REDZED"
    },
    {
        "uid": "4238712760",
        "password": "BY_PARAHEX-XLBS2EA3E-REDZED"
    },
    {
        "uid": "4238713249",
        "password": "BY_PARAHEX-ZTRUO9B3X-REDZED"
    },
    {
        "uid": "4238713784",
        "password": "BY_PARAHEX-8CCSUFQH4-REDZED"
    },
    {
        "uid": "4238714258",
        "password": "BY_PARAHEX-3ZOECZNC2-REDZED"
    },
    {
        "uid": "4238715167",
        "password": "BY_PARAHEX-Z9GV1YIMM-REDZED"
    },
    {
        "uid": "4238715516",
        "password": "BY_PARAHEX-O72FB0HZK-REDZED"
    },
    {
        "uid": "4238716055",
        "password": "BY_PARAHEX-2VH1Y4W0Z-REDZED"
    },
    {
        "uid": "4238716674",
        "password": "BY_PARAHEX-LFCIVOXIZ-REDZED"
    },
    {
        "uid": "4238717182",
        "password": "BY_PARAHEX-XH2A5ZC34-REDZED"
    },
    {
        "uid": "4238717619",
        "password": "BY_PARAHEX-NNR72KO1R-REDZED"
    },
    {
        "uid": "4238717932",
        "password": "BY_PARAHEX-2HCICVNHJ-REDZED"
    },
    {
        "uid": "4238718341",
        "password": "BY_PARAHEX-47P8CPXDR-REDZED"
    },
    {
        "uid": "4238718688",
        "password": "BY_PARAHEX-YJAOCOOUC-REDZED"
    },
    {
        "uid": "4238719207",
        "password": "BY_PARAHEX-AUL0FPIEZ-REDZED"
    },
    {
        "uid": "4238720013",
        "password": "BY_PARAHEX-TM9BR85HA-REDZED"
    },
    {
        "uid": "4238720653",
        "password": "BY_PARAHEX-1DQS7REYW-REDZED"
    },
    {
        "uid": "4238720994",
        "password": "BY_PARAHEX-HRULMHS6H-REDZED"
    },
    {
        "uid": "4238721341",
        "password": "BY_PARAHEX-GSNWB1JCR-REDZED"
    },
    {
        "uid": "4238721655",
        "password": "BY_PARAHEX-FZO8ECPLA-REDZED"
    },
    {
        "uid": "4238722070",
        "password": "BY_PARAHEX-4AQDFO5IY-REDZED"
    },
    {
        "uid": "4238722555",
        "password": "BY_PARAHEX-NJNQI6JLW-REDZED"
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
        'Expect': "100-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB50"
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
    tokens_from_accounts = load_tokens_from_accounts(limit=100)

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
        'Expect': "100-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB50"
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
        'Expect': "100-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB50"
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
async def like_handler(uid: str = None):
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
        tokens = responses_cache
        return JSONResponse(content={
            "message": "Tokens refreshed successfully",
            "total_tokens": len(tokens)
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get('/')
async def home():
    tokens = responses_cache
    return JSONResponse(content={
        "status": "online",
        "message": "Like API is running ✅",
        "cached_tokens": len(tokens),
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


if __name__ == "__main__":
    import uvicorn
    
    # جدولة المهمة كل 7 ساعات
    schedule.every(7).hours.do(fetch_tokens)

    # تشغيل fetch_tokens فورًا عند بدء التشغيل
    fetch_tokens()

    # تشغيل السكيدولر في ثانوية منفصلة
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    # تشغيل تطبيق FastAPI
    uvicorn.run(app, host="0.0.0.0", port=5000)

