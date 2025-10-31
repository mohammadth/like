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
        "uid": "4232198746",
        "password": "BY_PARAHEX-CZJRGX6C5-REDZED"
    },
    {
        "uid": "4232199064",
        "password": "BY_PARAHEX-FNO5PCIQB-REDZED"
    },
    {
        "uid": "4232199346",
        "password": "BY_PARAHEX-KSUWG6ZUP-REDZED"
    },
    {
        "uid": "4232199656",
        "password": "BY_PARAHEX-OLHBJTHSJ-REDZED"
    },
    {
        "uid": "4232200009",
        "password": "BY_PARAHEX-B64SD5OIY-REDZED"
    },
    {
        "uid": "4232200350",
        "password": "BY_PARAHEX-MANYOR9FC-REDZED"
    },
    {
        "uid": "4232200536",
        "password": "BY_PARAHEX-WLSZSYI1A-REDZED"
    },
    {
        "uid": "4232200878",
        "password": "BY_PARAHEX-K0PP1MLVD-REDZED"
    },
    {
        "uid": "4232201191",
        "password": "BY_PARAHEX-M6X2OEB5W-REDZED"
    },
    {
        "uid": "4232201469",
        "password": "BY_PARAHEX-ZHMZJX4S2-REDZED"
    },
    {
        "uid": "4232201693",
        "password": "BY_PARAHEX-3WA8HOGVJ-REDZED"
    },
    {
        "uid": "4232201948",
        "password": "BY_PARAHEX-D22OFGZIE-REDZED"
    },
    {
        "uid": "4232202205",
        "password": "BY_PARAHEX-TI80T3JDS-REDZED"
    },
    {
        "uid": "4232202459",
        "password": "BY_PARAHEX-FJVECKZCO-REDZED"
    },
    {
        "uid": "4232202833",
        "password": "BY_PARAHEX-MRH6NKSTX-REDZED"
    },
    {
        "uid": "4232203127",
        "password": "BY_PARAHEX-VBTE9Z7HG-REDZED"
    },
    {
        "uid": "4232203431",
        "password": "BY_PARAHEX-BKPQGLGDJ-REDZED"
    },
    {
        "uid": "4232203646",
        "password": "BY_PARAHEX-U07QZ6NTI-REDZED"
    },
    {
        "uid": "4232204018",
        "password": "BY_PARAHEX-D9LON3FBK-REDZED"
    },
    {
        "uid": "4232204306",
        "password": "BY_PARAHEX-CFZ4LEMLD-REDZED"
    },
    {
        "uid": "4232204661",
        "password": "BY_PARAHEX-LCX2EBDX8-REDZED"
    },
    {
        "uid": "4232204922",
        "password": "BY_PARAHEX-PFIUAGNVU-REDZED"
    },
    {
        "uid": "4232205148",
        "password": "BY_PARAHEX-Z9GRLVYKG-REDZED"
    },
    {
        "uid": "4232205403",
        "password": "BY_PARAHEX-DAPKLAVLX-REDZED"
    },
    {
        "uid": "4232205750",
        "password": "BY_PARAHEX-UTYVN0EIU-REDZED"
    },
    {
        "uid": "4232205985",
        "password": "BY_PARAHEX-1N14T7YSA-REDZED"
    },
    {
        "uid": "4232206314",
        "password": "BY_PARAHEX-KQFQPS92Z-REDZED"
    },
    {
        "uid": "4232206547",
        "password": "BY_PARAHEX-0FW2NQITO-REDZED"
    },
    {
        "uid": "4232206954",
        "password": "BY_PARAHEX-YBBKIBXOH-REDZED"
    },
    {
        "uid": "4232207337",
        "password": "BY_PARAHEX-LCPBRK1XK-REDZED"
    },
    {
        "uid": "4232207576",
        "password": "BY_PARAHEX-UIPWLEORK-REDZED"
    },
    {
        "uid": "4232207805",
        "password": "BY_PARAHEX-9QH2MP3JX-REDZED"
    },
    {
        "uid": "4232208045",
        "password": "BY_PARAHEX-E4GNY36IX-REDZED"
    },
    {
        "uid": "4232208236",
        "password": "BY_PARAHEX-Y2ERFH1CR-REDZED"
    },
    {
        "uid": "4232208565",
        "password": "BY_PARAHEX-UBTAGWYBR-REDZED"
    },
    {
        "uid": "4232208942",
        "password": "BY_PARAHEX-RMNWIAAM8-REDZED"
    },
    {
        "uid": "4232209286",
        "password": "BY_PARAHEX-72RXHELPR-REDZED"
    },
    {
        "uid": "4232209624",
        "password": "BY_PARAHEX-F8OSUX2HD-REDZED"
    },
    {
        "uid": "4232209912",
        "password": "BY_PARAHEX-2XEA5IUAW-REDZED"
    },
    {
        "uid": "4232210131",
        "password": "BY_PARAHEX-FFBV20ERK-REDZED"
    },
    {
        "uid": "4232210407",
        "password": "BY_PARAHEX-WVW7SRQLZ-REDZED"
    },
    {
        "uid": "4232210656",
        "password": "BY_PARAHEX-A7ZIBENM9-REDZED"
    },
    {
        "uid": "4232210947",
        "password": "BY_PARAHEX-CAFZTDYTG-REDZED"
    },
    {
        "uid": "4232211253",
        "password": "BY_PARAHEX-CEWWZI4X1-REDZED"
    },
    {
        "uid": "4232211518",
        "password": "BY_PARAHEX-S675N3AIK-REDZED"
    },
    {
        "uid": "4232211798",
        "password": "BY_PARAHEX-EUOA6VS5Z-REDZED"
    },
    {
        "uid": "4232212022",
        "password": "BY_PARAHEX-EWXWDNEQW-REDZED"
    },
    {
        "uid": "4232212190",
        "password": "BY_PARAHEX-EL3U1GUSK-REDZED"
    },
    {
        "uid": "4232212491",
        "password": "BY_PARAHEX-OW0D22FH4-REDZED"
    },
    {
        "uid": "4232212682",
        "password": "BY_PARAHEX-VGIV2ENUJ-REDZED"
    },
    {
        "uid": "4232212942",
        "password": "BY_PARAHEX-D07JZBFAO-REDZED"
    },
    {
        "uid": "4232213248",
        "password": "BY_PARAHEX-S3LIVMQSQ-REDZED"
    },
    {
        "uid": "4232213556",
        "password": "BY_PARAHEX-JATHGLYPI-REDZED"
    },
    {
        "uid": "4232213867",
        "password": "BY_PARAHEX-HRNWIUSR9-REDZED"
    },
    {
        "uid": "4232214154",
        "password": "BY_PARAHEX-W9XR8OPXZ-REDZED"
    },
    {
        "uid": "4232214492",
        "password": "BY_PARAHEX-ZWNNBMTQQ-REDZED"
    },
    {
        "uid": "4232214706",
        "password": "BY_PARAHEX-AVLO4YIIU-REDZED"
    },
    {
        "uid": "4232215051",
        "password": "BY_PARAHEX-UVTOAJQKQ-REDZED"
    },
    {
        "uid": "4232215367",
        "password": "BY_PARAHEX-ZG9UPFFOP-REDZED"
    },
    {
        "uid": "4232215730",
        "password": "BY_PARAHEX-8KXXJZYKL-REDZED"
    },
    {
        "uid": "4232215995",
        "password": "BY_PARAHEX-0MLA3K0N1-REDZED"
    },
    {
        "uid": "4232216350",
        "password": "BY_PARAHEX-JUL5IMNND-REDZED"
    },
    {
        "uid": "4232216563",
        "password": "BY_PARAHEX-K0GWKVHYE-REDZED"
    },
    {
        "uid": "4232216804",
        "password": "BY_PARAHEX-OBTB1O9AJ-REDZED"
    },
    {
        "uid": "4232217123",
        "password": "BY_PARAHEX-NCZZEAM2F-REDZED"
    },
    {
        "uid": "4232217468",
        "password": "BY_PARAHEX-WHKSJTKKY-REDZED"
    },
    {
        "uid": "4232217725",
        "password": "BY_PARAHEX-MLAZILZ90-REDZED"
    },
    {
        "uid": "4232217980",
        "password": "BY_PARAHEX-GYBBGUNAL-REDZED"
    },
    {
        "uid": "4232218205",
        "password": "BY_PARAHEX-KECZGVFRN-REDZED"
    },
    {
        "uid": "4232218401",
        "password": "BY_PARAHEX-2SJRH1Q8P-REDZED"
    },
    {
        "uid": "4232218628",
        "password": "BY_PARAHEX-P4ZUSYOY5-REDZED"
    },
    {
        "uid": "4232218851",
        "password": "BY_PARAHEX-Q4WOT3CAC-REDZED"
    },
    {
        "uid": "4232219014",
        "password": "BY_PARAHEX-GBDZGARMR-REDZED"
    },
    {
        "uid": "4232219434",
        "password": "BY_PARAHEX-TLNVEGZSP-REDZED"
    },
    {
        "uid": "4232219701",
        "password": "BY_PARAHEX-WLR5TDOA2-REDZED"
    },
    {
        "uid": "4232219937",
        "password": "BY_PARAHEX-B7YPPAHMD-REDZED"
    },
    {
        "uid": "4232220181",
        "password": "BY_PARAHEX-DAUNHRAAV-REDZED"
    },
    {
        "uid": "4232220482",
        "password": "BY_PARAHEX-TEXDZ7LDW-REDZED"
    },
    {
        "uid": "4232220685",
        "password": "BY_PARAHEX-M01PSYXN9-REDZED"
    },
    {
        "uid": "4232220891",
        "password": "BY_PARAHEX-OPBJKFK1C-REDZED"
    },
    {
        "uid": "4232221097",
        "password": "BY_PARAHEX-CXCINVDZW-REDZED"
    },
    {
        "uid": "4232221463",
        "password": "BY_PARAHEX-TIYEWUEMP-REDZED"
    },
    {
        "uid": "4232221699",
        "password": "BY_PARAHEX-0XRYHXQNL-REDZED"
    },
    {
        "uid": "4232222031",
        "password": "BY_PARAHEX-JOBDLXZNH-REDZED"
    },
    {
        "uid": "4232222264",
        "password": "BY_PARAHEX-PBKV8OBLK-REDZED"
    },
    {
        "uid": "4232222466",
        "password": "BY_PARAHEX-W3SVAFVBV-REDZED"
    },
    {
        "uid": "4232222750",
        "password": "BY_PARAHEX-CWR9XFH4T-REDZED"
    },
    {
        "uid": "4232223064",
        "password": "BY_PARAHEX-Y6VMGKZLA-REDZED"
    },
    {
        "uid": "4232223346",
        "password": "BY_PARAHEX-3HOYFKPK1-REDZED"
    },
    {
        "uid": "4232223748",
        "password": "BY_PARAHEX-EMFGGMYAL-REDZED"
    },
    {
        "uid": "4232224025",
        "password": "BY_PARAHEX-NEXK4B6ED-REDZED"
    },
    {
        "uid": "4232224403",
        "password": "BY_PARAHEX-R1PQSJHXZ-REDZED"
    },
    {
        "uid": "4232224658",
        "password": "BY_PARAHEX-HRHA2WZUR-REDZED"
    },
    {
        "uid": "4232225044",
        "password": "BY_PARAHEX-BMP8T40AT-REDZED"
    },
    {
        "uid": "4232225592",
        "password": "BY_PARAHEX-QTGIBAMPU-REDZED"
    },
    {
        "uid": "4232225954",
        "password": "BY_PARAHEX-EGKXHGP0U-REDZED"
    },
    {
        "uid": "4232226285",
        "password": "BY_PARAHEX-RQ05QBVDU-REDZED"
    },
    {
        "uid": "4232226598",
        "password": "BY_PARAHEX-M44AQUCSU-REDZED"
    },
    {
        "uid": "4232226921",
        "password": "BY_PARAHEX-GWMSZIIJJ-REDZED"
    },
    {
        "uid": "4232227386",
        "password": "BY_PARAHEX-DGU3ERQZT-REDZED"
    },
    {
        "uid": "4232227680",
        "password": "BY_PARAHEX-KEODWNSVX-REDZED"
    },
    {
        "uid": "4232228006",
        "password": "BY_PARAHEX-NPWS9RMER-REDZED"
    },
    {
        "uid": "4232228273",
        "password": "BY_PARAHEX-X5QR0RV8N-REDZED"
    },
    {
        "uid": "4232228509",
        "password": "BY_PARAHEX-KD9BUM957-REDZED"
    },
    {
        "uid": "4232228933",
        "password": "BY_PARAHEX-WDIEA7UBA-REDZED"
    },
    {
        "uid": "4232229240",
        "password": "BY_PARAHEX-TE8W3PQEF-REDZED"
    },
    {
        "uid": "4232229470",
        "password": "BY_PARAHEX-EJUHLPLUL-REDZED"
    },
    {
        "uid": "4232229711",
        "password": "BY_PARAHEX-L0ESODNMF-REDZED"
    },
    {
        "uid": "4232230016",
        "password": "BY_PARAHEX-JVAUS2TKF-REDZED"
    },
    {
        "uid": "4232230316",
        "password": "BY_PARAHEX-F5BSNWR1P-REDZED"
    },
    {
        "uid": "4232230575",
        "password": "BY_PARAHEX-BYBWRX9YQ-REDZED"
    },
    {
        "uid": "4232230886",
        "password": "BY_PARAHEX-AZA1POZY5-REDZED"
    },
    {
        "uid": "4232231281",
        "password": "BY_PARAHEX-6ZJFOUWMT-REDZED"
    },
    {
        "uid": "4232231604",
        "password": "BY_PARAHEX-2XVNLWIQQ-REDZED"
    },
    {
        "uid": "4232231911",
        "password": "BY_PARAHEX-5XGYZ67QB-REDZED"
    },
    {
        "uid": "4232232182",
        "password": "BY_PARAHEX-EABKMBZWC-REDZED"
    },
    {
        "uid": "4232232472",
        "password": "BY_PARAHEX-ED9ZUAZIH-REDZED"
    },
    {
        "uid": "4232232728",
        "password": "BY_PARAHEX-QFBMETUIM-REDZED"
    },
    {
        "uid": "4232232989",
        "password": "BY_PARAHEX-9DJ3TCNDH-REDZED"
    },
    {
        "uid": "4232233252",
        "password": "BY_PARAHEX-HXOSMHGNE-REDZED"
    },
    {
        "uid": "4232233520",
        "password": "BY_PARAHEX-UXANKBGIB-REDZED"
    },
    {
        "uid": "4232233756",
        "password": "BY_PARAHEX-QMVNVQGDH-REDZED"
    },
    {
        "uid": "4232233987",
        "password": "BY_PARAHEX-RCMOOJMK1-REDZED"
    },
    {
        "uid": "4232234273",
        "password": "BY_PARAHEX-SQ8U3TDC2-REDZED"
    },
    {
        "uid": "4232234455",
        "password": "BY_PARAHEX-Q5LMV09QJ-REDZED"
    },
    {
        "uid": "4232234697",
        "password": "BY_PARAHEX-9IBWCATGM-REDZED"
    },
    {
        "uid": "4232234921",
        "password": "BY_PARAHEX-BXP5IR7LP-REDZED"
    },
    {
        "uid": "4232235317",
        "password": "BY_PARAHEX-H528QDRMW-REDZED"
    },
    {
        "uid": "4232235616",
        "password": "BY_PARAHEX-MGYZWEU18-REDZED"
    },
    {
        "uid": "4232235958",
        "password": "BY_PARAHEX-UBXZRHMGL-REDZED"
    },
    {
        "uid": "4232236249",
        "password": "BY_PARAHEX-UKDVEEZDD-REDZED"
    },
    {
        "uid": "4232236502",
        "password": "BY_PARAHEX-UTHI7DBWP-REDZED"
    },
    {
        "uid": "4232236720",
        "password": "BY_PARAHEX-IQW9GVRKO-REDZED"
    },
    {
        "uid": "4232236959",
        "password": "BY_PARAHEX-WZWPPR3GD-REDZED"
    },
    {
        "uid": "4232237310",
        "password": "BY_PARAHEX-MUSN95FV8-REDZED"
    },
    {
        "uid": "4232237744",
        "password": "BY_PARAHEX-BG4RHBCXA-REDZED"
    },
    {
        "uid": "4232238027",
        "password": "BY_PARAHEX-NFVKU0HTM-REDZED"
    },
    {
        "uid": "4232238244",
        "password": "BY_PARAHEX-PGLIN1SXY-REDZED"
    },
    {
        "uid": "4232238491",
        "password": "BY_PARAHEX-ZPOGS1GAT-REDZED"
    },
    {
        "uid": "4232238753",
        "password": "BY_PARAHEX-EAOECQ4A5-REDZED"
    },
    {
        "uid": "4232239052",
        "password": "BY_PARAHEX-ZRFNYASZE-REDZED"
    },
    {
        "uid": "4232239344",
        "password": "BY_PARAHEX-WNETRFTWD-REDZED"
    },
    {
        "uid": "4232239709",
        "password": "BY_PARAHEX-DXNDJZJWN-REDZED"
    },
    {
        "uid": "4232239910",
        "password": "BY_PARAHEX-CWFTY2AGG-REDZED"
    },
    {
        "uid": "4232240148",
        "password": "BY_PARAHEX-WOTCG8FNI-REDZED"
    },
    {
        "uid": "4232240372",
        "password": "BY_PARAHEX-ENPOGZHBA-REDZED"
    },
    {
        "uid": "4232240629",
        "password": "BY_PARAHEX-JTYP1KQ9F-REDZED"
    },
    {
        "uid": "4232240886",
        "password": "BY_PARAHEX-EG6R6E8AM-REDZED"
    },
    {
        "uid": "4232241114",
        "password": "BY_PARAHEX-G4YDLOPFJ-REDZED"
    },
    {
        "uid": "4232241422",
        "password": "BY_PARAHEX-B2ZX1F9F9-REDZED"
    },
    {
        "uid": "4232241713",
        "password": "BY_PARAHEX-P1KWJXWVT-REDZED"
    },
    {
        "uid": "4232168011",
        "password": "BY_PARAHEX-W3FNQAX9U-REDZED"
    },
    {
        "uid": "4232168431",
        "password": "BY_PARAHEX-2FRJIVBMI-REDZED"
    },
    {
        "uid": "4232168733",
        "password": "BY_PARAHEX-2YOSJ1YHU-REDZED"
    },
    {
        "uid": "4232168933",
        "password": "BY_PARAHEX-JCEF79J6K-REDZED"
    },
    {
        "uid": "4232169131",
        "password": "BY_PARAHEX-ZMDNEPUQS-REDZED"
    },
    {
        "uid": "4232169385",
        "password": "BY_PARAHEX-VSBKDTJW8-REDZED"
    },
    {
        "uid": "4232169650",
        "password": "BY_PARAHEX-YLQ4EIBFF-REDZED"
    },
    {
        "uid": "4232169869",
        "password": "BY_PARAHEX-WGE6MVSXS-REDZED"
    },
    {
        "uid": "4232170111",
        "password": "BY_PARAHEX-WCTJNVCCV-REDZED"
    },
    {
        "uid": "4232170547",
        "password": "BY_PARAHEX-6K7UW7HNA-REDZED"
    },
    {
        "uid": "4232170829",
        "password": "BY_PARAHEX-6WBXZJGHG-REDZED"
    },
    {
        "uid": "4232171148",
        "password": "BY_PARAHEX-OIWMWOMRN-REDZED"
    },
    {
        "uid": "4232171504",
        "password": "BY_PARAHEX-O3RUA3Q74-REDZED"
    },
    {
        "uid": "4232171812",
        "password": "BY_PARAHEX-I6GNIZPV8-REDZED"
    },
    {
        "uid": "4232172164",
        "password": "BY_PARAHEX-D4UROAUXV-REDZED"
    },
    {
        "uid": "4232172623",
        "password": "BY_PARAHEX-3ZP0OQ9KK-REDZED"
    },
    {
        "uid": "4232173008",
        "password": "BY_PARAHEX-K6KSWGBKE-REDZED"
    },
    {
        "uid": "4232173515",
        "password": "BY_PARAHEX-YBFW51BKS-REDZED"
    },
    {
        "uid": "4232173945",
        "password": "BY_PARAHEX-BLYS3RJ8T-REDZED"
    },
    {
        "uid": "4232174401",
        "password": "BY_PARAHEX-HBVNVAMWI-REDZED"
    },
    {
        "uid": "4232174897",
        "password": "BY_PARAHEX-UW7HGJ4YL-REDZED"
    },
    {
        "uid": "4232175429",
        "password": "BY_PARAHEX-MNNMHJ8RQ-REDZED"
    },
    {
        "uid": "4232175836",
        "password": "BY_PARAHEX-I7HJBZGMN-REDZED"
    },
    {
        "uid": "4232176407",
        "password": "BY_PARAHEX-2LXOT90IR-REDZED"
    },
    {
        "uid": "4232176766",
        "password": "BY_PARAHEX-YEQEPSVFR-REDZED"
    },
    {
        "uid": "4232177148",
        "password": "BY_PARAHEX-PYJDBZROG-REDZED"
    },
    {
        "uid": "4232177482",
        "password": "BY_PARAHEX-O2SJZBZIM-REDZED"
    },
    {
        "uid": "4232177819",
        "password": "BY_PARAHEX-SKXUHEZ8E-REDZED"
    },
    {
        "uid": "4232178129",
        "password": "BY_PARAHEX-BAFNZEPVR-REDZED"
    },
    {
        "uid": "4232178647",
        "password": "BY_PARAHEX-HYBNZHLMF-REDZED"
    },
    {
        "uid": "4232178908",
        "password": "BY_PARAHEX-MQUSE5UMR-REDZED"
    },
    {
        "uid": "4232179269",
        "password": "BY_PARAHEX-KBPZKDPDG-REDZED"
    },
    {
        "uid": "4232179545",
        "password": "BY_PARAHEX-F2TSJPMAR-REDZED"
    },
    {
        "uid": "4232179886",
        "password": "BY_PARAHEX-VCEZDJH3W-REDZED"
    },
    {
        "uid": "4232180122",
        "password": "BY_PARAHEX-YO7OYI126-REDZED"
    },
    {
        "uid": "4232180485",
        "password": "BY_PARAHEX-CV7PLF346-REDZED"
    },
    {
        "uid": "4232180781",
        "password": "BY_PARAHEX-VLHTRP3LZ-REDZED"
    },
    {
        "uid": "4232181370",
        "password": "BY_PARAHEX-KNUPSSPYA-REDZED"
    },
    {
        "uid": "4232182384",
        "password": "BY_PARAHEX-1JRHOQRKX-REDZED"
    },
    {
        "uid": "4232182724",
        "password": "BY_PARAHEX-M5NLQKCKA-REDZED"
    },
    {
        "uid": "4232183065",
        "password": "BY_PARAHEX-GPAADCLCI-REDZED"
    },
    {
        "uid": "4232183487",
        "password": "BY_PARAHEX-BZ8P5UMJ4-REDZED"
    },
    {
        "uid": "4232183926",
        "password": "BY_PARAHEX-CWQEMJH20-REDZED"
    },
    {
        "uid": "4232184175",
        "password": "BY_PARAHEX-1FPN76CZ7-REDZED"
    },
    {
        "uid": "4232184652",
        "password": "BY_PARAHEX-MOKLG8MKB-REDZED"
    },
    {
        "uid": "4232184970",
        "password": "BY_PARAHEX-UTTVDZAQP-REDZED"
    },
    {
        "uid": "4232185476",
        "password": "BY_PARAHEX-DXFWC5IBF-REDZED"
    },
    {
        "uid": "4232185739",
        "password": "BY_PARAHEX-YT6DMLPIR-REDZED"
    },
    {
        "uid": "4232186542",
        "password": "BY_PARAHEX-HOAAXMD8Q-REDZED"
    },
    {
        "uid": "4232187063",
        "password": "BY_PARAHEX-QGJDHOS9X-REDZED"
    },
    {
        "uid": "4232047318",
        "password": "BY_PARAHEX-A2ZNMI4OV-REDZED"
    },
    {
        "uid": "4232047531",
        "password": "BY_PARAHEX-EDHNUPMUE-REDZED"
    },
    {
        "uid": "4232047756",
        "password": "BY_PARAHEX-FSYSAMNM9-REDZED"
    },
    {
        "uid": "4232047974",
        "password": "BY_PARAHEX-STFH2AU9X-REDZED"
    },
    {
        "uid": "4232048214",
        "password": "BY_PARAHEX-M15IXIAZF-REDZED"
    },
    {
        "uid": "4232048412",
        "password": "BY_PARAHEX-PVYRLFJOB-REDZED"
    },
    {
        "uid": "4232048752",
        "password": "BY_PARAHEX-7Z7EJYNIA-REDZED"
    },
    {
        "uid": "4232049027",
        "password": "BY_PARAHEX-OZO5N6TLV-REDZED"
    },
    {
        "uid": "4232049222",
        "password": "BY_PARAHEX-5U1AEO7OI-REDZED"
    },
    {
        "uid": "4232049400",
        "password": "BY_PARAHEX-TBIWELJTS-REDZED"
    },
    {
        "uid": "4232049636",
        "password": "BY_PARAHEX-QQTSZRIXO-REDZED"
    },
    {
        "uid": "4232049860",
        "password": "BY_PARAHEX-P02V00N7N-REDZED"
    },
    {
        "uid": "4232050088",
        "password": "BY_PARAHEX-GLKIV9AUE-REDZED"
    },
    {
        "uid": "4232050300",
        "password": "BY_PARAHEX-PTPX04PBN-REDZED"
    },
    {
        "uid": "4232050526",
        "password": "BY_PARAHEX-RESVAVLLP-REDZED"
    },
    {
        "uid": "4232050707",
        "password": "BY_PARAHEX-9EPPEXOYU-REDZED"
    },
    {
        "uid": "4232051028",
        "password": "BY_PARAHEX-H1QPACIO1-REDZED"
    },
    {
        "uid": "4232051275",
        "password": "BY_PARAHEX-2XYXA4UKT-REDZED"
    },
    {
        "uid": "4232051525",
        "password": "BY_PARAHEX-O8TKPZXWZ-REDZED"
    },
    {
        "uid": "4232051774",
        "password": "BY_PARAHEX-UFBJNVS3S-REDZED"
    },
    {
        "uid": "4232051965",
        "password": "BY_PARAHEX-FMLHUHAMC-REDZED"
    },
    {
        "uid": "4232052142",
        "password": "BY_PARAHEX-QLWNPT3GD-REDZED"
    },
    {
        "uid": "4232052315",
        "password": "BY_PARAHEX-KDWZKYM09-REDZED"
    },
    {
        "uid": "4232052508",
        "password": "BY_PARAHEX-WJGXXNSIO-REDZED"
    },
    {
        "uid": "4232052804",
        "password": "BY_PARAHEX-VELRAPBZK-REDZED"
    },
    {
        "uid": "4232053117",
        "password": "BY_PARAHEX-BEWBEFBBZ-REDZED"
    },
    {
        "uid": "4232053342",
        "password": "BY_PARAHEX-OQX3GQZMI-REDZED"
    },
    {
        "uid": "4232053580",
        "password": "BY_PARAHEX-2W2IKLXZZ-REDZED"
    },
    {
        "uid": "4232053783",
        "password": "BY_PARAHEX-24IOVTI8P-REDZED"
    },
    {
        "uid": "4232053990",
        "password": "BY_PARAHEX-U0KAD1CXE-REDZED"
    },
    {
        "uid": "4232054190",
        "password": "BY_PARAHEX-JIV9XFSX0-REDZED"
    },
    {
        "uid": "4232054401",
        "password": "BY_PARAHEX-BVRYRA4MW-REDZED"
    },
    {
        "uid": "4232054552",
        "password": "BY_PARAHEX-I1LRFLBYA-REDZED"
    },
    {
        "uid": "4232054849",
        "password": "BY_PARAHEX-GTGKBIUSN-REDZED"
    },
    {
        "uid": "4232055053",
        "password": "BY_PARAHEX-9Z8TPNARP-REDZED"
    },
    {
        "uid": "4232055258",
        "password": "BY_PARAHEX-QWMLZIBBV-REDZED"
    },
    {
        "uid": "4232055509",
        "password": "BY_PARAHEX-0WLOSRTYO-REDZED"
    },
    {
        "uid": "4232055788",
        "password": "BY_PARAHEX-BVETDZB4W-REDZED"
    },
    {
        "uid": "4232055984",
        "password": "BY_PARAHEX-MJ9TQWXJ4-REDZED"
    },
    {
        "uid": "4232056193",
        "password": "BY_PARAHEX-4TPNTVXMD-REDZED"
    },
    {
        "uid": "4232056421",
        "password": "BY_PARAHEX-WAOZG10VA-REDZED"
    },
    {
        "uid": "4232056594",
        "password": "BY_PARAHEX-BIISJEOBU-REDZED"
    },
    {
        "uid": "4232056855",
        "password": "BY_PARAHEX-TJJNEE1EI-REDZED"
    },
    {
        "uid": "4232057047",
        "password": "BY_PARAHEX-OESSEAQIR-REDZED"
    },
    {
        "uid": "4232057245",
        "password": "BY_PARAHEX-ZPBGUN3MA-REDZED"
    },
    {
        "uid": "4232057529",
        "password": "BY_PARAHEX-PUZ32BZB2-REDZED"
    },
    {
        "uid": "4232057731",
        "password": "BY_PARAHEX-FGY7XWWIB-REDZED"
    },
    {
        "uid": "4232057935",
        "password": "BY_PARAHEX-JNOHJHFJW-REDZED"
    },
    {
        "uid": "4232058122",
        "password": "BY_PARAHEX-J2JP7PTMM-REDZED"
    },
    {
        "uid": "4232058293",
        "password": "BY_PARAHEX-H5BILHDUK-REDZED"
    },
    {
        "uid": "4231979199",
        "password": "BY_PARAHEX-MUUWYDU1Q-REDZED"
    },
    {
        "uid": "4231979564",
        "password": "BY_PARAHEX-38X40BXNE-REDZED"
    },
    {
        "uid": "4231980079",
        "password": "BY_PARAHEX-G9GKOGCMG-REDZED"
    },
    {
        "uid": "4231980434",
        "password": "BY_PARAHEX-T9KREWFSA-REDZED"
    },
    {
        "uid": "4231980805",
        "password": "BY_PARAHEX-T3ODWNKSD-REDZED"
    },
    {
        "uid": "4231981881",
        "password": "BY_PARAHEX-KDU00CGD3-REDZED"
    },
    {
        "uid": "4231982777",
        "password": "BY_PARAHEX-0NWBQ0BBF-REDZED"
    },
    {
        "uid": "4231983743",
        "password": "BY_PARAHEX-ONW1HG7VA-REDZED"
    },
    {
        "uid": "4231984217",
        "password": "BY_PARAHEX-NX20TGNMI-REDZED"
    },
    {
        "uid": "4231984772",
        "password": "BY_PARAHEX-XVHKYWHFL-REDZED"
    },
    {
        "uid": "4231985768",
        "password": "BY_PARAHEX-TUMLCDZQI-REDZED"
    },
    {
        "uid": "4231986117",
        "password": "BY_PARAHEX-A1W6V2MEV-REDZED"
    },
    {
        "uid": "4231986445",
        "password": "BY_PARAHEX-GNSEE5SHG-REDZED"
    },
    {
        "uid": "4231986691",
        "password": "BY_PARAHEX-RYHXW7UNR-REDZED"
    },
    {
        "uid": "4231987075",
        "password": "BY_PARAHEX-HMGCBR1B6-REDZED"
    },
    {
        "uid": "4231987507",
        "password": "BY_PARAHEX-Q2IDI9E13-REDZED"
    },
    {
        "uid": "4231987730",
        "password": "BY_PARAHEX-ETRGEQ9RO-REDZED"
    },
    {
        "uid": "4231987963",
        "password": "BY_PARAHEX-EWXHPWBUR-REDZED"
    },
    {
        "uid": "4231988327",
        "password": "BY_PARAHEX-XUDTVGRTE-REDZED"
    },
    {
        "uid": "4231988558",
        "password": "BY_PARAHEX-RNNGY8L5K-REDZED"
    },
    {
        "uid": "4231988842",
        "password": "BY_PARAHEX-5VFX1VZGG-REDZED"
    },
    {
        "uid": "4231989301",
        "password": "BY_PARAHEX-DBS6JJVTH-REDZED"
    },
    {
        "uid": "4231989598",
        "password": "BY_PARAHEX-JHIDYDJRU-REDZED"
    },
    {
        "uid": "4231989885",
        "password": "BY_PARAHEX-CM8YMNPSE-REDZED"
    },
    {
        "uid": "4231990229",
        "password": "BY_PARAHEX-RQQ9KXBCZ-REDZED"
    },
    {
        "uid": "4231990507",
        "password": "BY_PARAHEX-IMQWIB2YG-REDZED"
    },
    {
        "uid": "4231990837",
        "password": "BY_PARAHEX-EUFSUEBCM-REDZED"
    },
    {
        "uid": "4231991097",
        "password": "BY_PARAHEX-7VEMKDKE4-REDZED"
    },
    {
        "uid": "4231991331",
        "password": "BY_PARAHEX-OTSSBPMYN-REDZED"
    },
    {
        "uid": "4231991592",
        "password": "BY_PARAHEX-D9AR1MOKZ-REDZED"
    },
    {
        "uid": "4231991860",
        "password": "BY_PARAHEX-7O4XZDHUV-REDZED"
    },
    {
        "uid": "4231992117",
        "password": "BY_PARAHEX-8UQG1OQE8-REDZED"
    },
    {
        "uid": "4231992356",
        "password": "BY_PARAHEX-DRHNIPADY-REDZED"
    },
    {
        "uid": "4231992602",
        "password": "BY_PARAHEX-MMHB5GNVP-REDZED"
    },
    {
        "uid": "4231992846",
        "password": "BY_PARAHEX-O7GULPP6I-REDZED"
    },
    {
        "uid": "4231993056",
        "password": "BY_PARAHEX-TPTAPCPLW-REDZED"
    },
    {
        "uid": "4231993278",
        "password": "BY_PARAHEX-YASXHCRRP-REDZED"
    },
    {
        "uid": "4231993468",
        "password": "BY_PARAHEX-GZONM34TU-REDZED"
    },
    {
        "uid": "4231993681",
        "password": "BY_PARAHEX-64UEV2VJV-REDZED"
    },
    {
        "uid": "4231993920",
        "password": "BY_PARAHEX-PKKX9SVP8-REDZED"
    },
    {
        "uid": "4231994125",
        "password": "BY_PARAHEX-OXPHG1DDD-REDZED"
    },
    {
        "uid": "4231994366",
        "password": "BY_PARAHEX-HRNO0N1EK-REDZED"
    },
    {
        "uid": "4231994575",
        "password": "BY_PARAHEX-XEMUF2AGS-REDZED"
    },
    {
        "uid": "4231994822",
        "password": "BY_PARAHEX-NKKWQVXQF-REDZED"
    },
    {
        "uid": "4231994998",
        "password": "BY_PARAHEX-NS15AOEWW-REDZED"
    },
    {
        "uid": "4231995380",
        "password": "BY_PARAHEX-UPQCZ11SV-REDZED"
    },
    {
        "uid": "4231995667",
        "password": "BY_PARAHEX-RKXPKGHXP-REDZED"
    },
    {
        "uid": "4231995881",
        "password": "BY_PARAHEX-S4R3FRICY-REDZED"
    },
    {
        "uid": "4231996108",
        "password": "BY_PARAHEX-6NXUKFZPO-REDZED"
    },
    {
        "uid": "4231996422",
        "password": "BY_PARAHEX-HCDMF4KGW-REDZED"
    },
    {
        "uid": "4231951894",
        "password": "BY_PARAHEX-CEZOIJRCX-REDZED"
    },
    {
        "uid": "4231952245",
        "password": "BY_PARAHEX-LVS1C0CBY-REDZED"
    },
    {
        "uid": "4231952546",
        "password": "BY_PARAHEX-KTKWO5PUI-REDZED"
    },
    {
        "uid": "4231952779",
        "password": "BY_PARAHEX-NYF39LQX5-REDZED"
    },
    {
        "uid": "4231952975",
        "password": "BY_PARAHEX-9IMCWILLK-REDZED"
    },
    {
        "uid": "4231953292",
        "password": "BY_PARAHEX-MANZDSN0K-REDZED"
    },
    {
        "uid": "4231953571",
        "password": "BY_PARAHEX-XQNUD4GSH-REDZED"
    },
    {
        "uid": "4231953748",
        "password": "BY_PARAHEX-LUVE8WHXX-REDZED"
    },
    {
        "uid": "4231954344",
        "password": "BY_PARAHEX-5VNHPRUQ1-REDZED"
    },
    {
        "uid": "4231954644",
        "password": "BY_PARAHEX-Q6IJE63AM-REDZED"
    },
    {
        "uid": "4231954881",
        "password": "BY_PARAHEX-ZFOPJNDDK-REDZED"
    },
    {
        "uid": "4231955232",
        "password": "BY_PARAHEX-0H2EF36VV-REDZED"
    },
    {
        "uid": "4231955572",
        "password": "BY_PARAHEX-MFLHK1MPA-REDZED"
    },
    {
        "uid": "4231955980",
        "password": "BY_PARAHEX-HPRCIWW6G-REDZED"
    },
    {
        "uid": "4231956287",
        "password": "BY_PARAHEX-NCGMA7UZQ-REDZED"
    },
    {
        "uid": "4231956508",
        "password": "BY_PARAHEX-HNQ1KB1AF-REDZED"
    },
    {
        "uid": "4231956697",
        "password": "BY_PARAHEX-RK6HT3HID-REDZED"
    },
    {
        "uid": "4231956965",
        "password": "BY_PARAHEX-RBLU8FUJC-REDZED"
    },
    {
        "uid": "4231957297",
        "password": "BY_PARAHEX-URN5EFDOV-REDZED"
    },
    {
        "uid": "4231957533",
        "password": "BY_PARAHEX-6HQ0NBKOV-REDZED"
    },
    {
        "uid": "4231957749",
        "password": "BY_PARAHEX-IFBLZOSTP-REDZED"
    },
    {
        "uid": "4231957951",
        "password": "BY_PARAHEX-J0HHWFR11-REDZED"
    },
    {
        "uid": "4231958202",
        "password": "BY_PARAHEX-HK1HAD8AZ-REDZED"
    },
    {
        "uid": "4231958458",
        "password": "BY_PARAHEX-YBN1HQPFN-REDZED"
    },
    {
        "uid": "4231958660",
        "password": "BY_PARAHEX-N4XPWIRHI-REDZED"
    },
    {
        "uid": "4231958901",
        "password": "BY_PARAHEX-RRQQRSEIY-REDZED"
    },
    {
        "uid": "4231959159",
        "password": "BY_PARAHEX-DXEZ30WF9-REDZED"
    },
    {
        "uid": "4231959411",
        "password": "BY_PARAHEX-HSGVMKOUN-REDZED"
    },
    {
        "uid": "4231959653",
        "password": "BY_PARAHEX-RGPSI1WBV-REDZED"
    },
    {
        "uid": "4231959860",
        "password": "BY_PARAHEX-R5Y2E8HWC-REDZED"
    },
    {
        "uid": "4231960088",
        "password": "BY_PARAHEX-VPYY3AOR6-REDZED"
    },
    {
        "uid": "4231960283",
        "password": "BY_PARAHEX-I2LLOWNMQ-REDZED"
    },
    {
        "uid": "4231960589",
        "password": "BY_PARAHEX-N3PBAKC5Y-REDZED"
    },
    {
        "uid": "4231960852",
        "password": "BY_PARAHEX-ELCIRYQKT-REDZED"
    },
    {
        "uid": "4231961053",
        "password": "BY_PARAHEX-C30ORDGSH-REDZED"
    },
    {
        "uid": "4231961374",
        "password": "BY_PARAHEX-Y76FNVCHH-REDZED"
    },
    {
        "uid": "4231961628",
        "password": "BY_PARAHEX-AKAFGTRNI-REDZED"
    },
    {
        "uid": "4231961831",
        "password": "BY_PARAHEX-ZAFVEPB3O-REDZED"
    },
    {
        "uid": "4231962061",
        "password": "BY_PARAHEX-TCCM8OBTH-REDZED"
    },
    {
        "uid": "4231962345",
        "password": "BY_PARAHEX-EKFQL25IZ-REDZED"
    },
    {
        "uid": "4231962648",
        "password": "BY_PARAHEX-XRBRHMVOG-REDZED"
    },
    {
        "uid": "4231962917",
        "password": "BY_PARAHEX-B5GD2LP4K-REDZED"
    },
    {
        "uid": "4231963208",
        "password": "BY_PARAHEX-V7YDBAYHA-REDZED"
    },
    {
        "uid": "4231963661",
        "password": "BY_PARAHEX-QTVFQUTRL-REDZED"
    },
    {
        "uid": "4231964054",
        "password": "BY_PARAHEX-0R8FEGO7O-REDZED"
    },
    {
        "uid": "4231964363",
        "password": "BY_PARAHEX-3ZGYMRO5D-REDZED"
    },
    {
        "uid": "4231964633",
        "password": "BY_PARAHEX-RMQVHSN3G-REDZED"
    },
    {
        "uid": "4231965107",
        "password": "BY_PARAHEX-YITEPNIQU-REDZED"
    },
    {
        "uid": "4231965417",
        "password": "BY_PARAHEX-26P6P6UDG-REDZED"
    },
    {
        "uid": "4231965711",
        "password": "BY_PARAHEX-GDPZF2W2Q-REDZED"
    },
    {
        "uid": "4231904223",
        "password": "BY_PARAHEX-WKK8EJ7OC-REDZED"
    },
    {
        "uid": "4231904436",
        "password": "BY_PARAHEX-WH8UHXMRN-REDZED"
    },
    {
        "uid": "4231904639",
        "password": "BY_PARAHEX-GCMH0ER5H-REDZED"
    },
    {
        "uid": "4231905206",
        "password": "BY_PARAHEX-S8VDOF3WM-REDZED"
    },
    {
        "uid": "4231905885",
        "password": "BY_PARAHEX-FI5CXBGIT-REDZED"
    },
    {
        "uid": "4231906156",
        "password": "BY_PARAHEX-F1675HPBO-REDZED"
    },
    {
        "uid": "4231906448",
        "password": "BY_PARAHEX-O1BVFVQKK-REDZED"
    },
    {
        "uid": "4231906803",
        "password": "BY_PARAHEX-E3A4VD1F5-REDZED"
    },
    {
        "uid": "4231907153",
        "password": "BY_PARAHEX-K2PNZI9GM-REDZED"
    },
    {
        "uid": "4231907707",
        "password": "BY_PARAHEX-CFLLITG6L-REDZED"
    },
    {
        "uid": "4231907979",
        "password": "BY_PARAHEX-A7FTXOQOB-REDZED"
    },
    {
        "uid": "4231908280",
        "password": "BY_PARAHEX-UD8VISE6S-REDZED"
    },
    {
        "uid": "4231908519",
        "password": "BY_PARAHEX-IOTC7ZHKR-REDZED"
    },
    {
        "uid": "4231908909",
        "password": "BY_PARAHEX-IFSFBRTV0-REDZED"
    },
    {
        "uid": "4231909230",
        "password": "BY_PARAHEX-RLAEBNDKR-REDZED"
    },
    {
        "uid": "4231909521",
        "password": "BY_PARAHEX-TIVKCFDTE-REDZED"
    },
    {
        "uid": "4231909850",
        "password": "BY_PARAHEX-A7Z0O0FUS-REDZED"
    },
    {
        "uid": "4231910194",
        "password": "BY_PARAHEX-MRIYM4TFO-REDZED"
    },
    {
        "uid": "4231912538",
        "password": "BY_PARAHEX-P5XAAPTND-REDZED"
    },
    {
        "uid": "4231912881",
        "password": "BY_PARAHEX-QYTKKANEA-REDZED"
    },
    {
        "uid": "4231913162",
        "password": "BY_PARAHEX-UAD2IA442-REDZED"
    },
    {
        "uid": "4231913392",
        "password": "BY_PARAHEX-HTC0AEXO3-REDZED"
    },
    {
        "uid": "4231913671",
        "password": "BY_PARAHEX-UPX4QKFET-REDZED"
    },
    {
        "uid": "4231913865",
        "password": "BY_PARAHEX-SDDGMERRE-REDZED"
    },
    {
        "uid": "4231914251",
        "password": "BY_PARAHEX-WI9XNBD91-REDZED"
    },
    {
        "uid": "4231914652",
        "password": "BY_PARAHEX-8NJLVFYTK-REDZED"
    },
    {
        "uid": "4231914856",
        "password": "BY_PARAHEX-HXRWNH8IR-REDZED"
    },
    {
        "uid": "4231915112",
        "password": "BY_PARAHEX-B6MUJL85Q-REDZED"
    },
    {
        "uid": "4231915383",
        "password": "BY_PARAHEX-E5ANT0KT1-REDZED"
    },
    {
        "uid": "4231915610",
        "password": "BY_PARAHEX-AB3LFZVL2-REDZED"
    },
    {
        "uid": "4231915840",
        "password": "BY_PARAHEX-CVRRSPS9W-REDZED"
    },
    {
        "uid": "4231916072",
        "password": "BY_PARAHEX-OMJNVIIVP-REDZED"
    },
    {
        "uid": "4231916327",
        "password": "BY_PARAHEX-YKNQZW2NG-REDZED"
    },
    {
        "uid": "4231916522",
        "password": "BY_PARAHEX-1FBOLLFSD-REDZED"
    },
    {
        "uid": "4231916707",
        "password": "BY_PARAHEX-SKCHRE0JB-REDZED"
    },
    {
        "uid": "4231916930",
        "password": "BY_PARAHEX-WMOLYEZOU-REDZED"
    },
    {
        "uid": "4231917138",
        "password": "BY_PARAHEX-DNMKT8GK8-REDZED"
    },
    {
        "uid": "4231917381",
        "password": "BY_PARAHEX-JGWBEVJOD-REDZED"
    },
    {
        "uid": "4231917570",
        "password": "BY_PARAHEX-QS7OYGYNR-REDZED"
    },
    {
        "uid": "4231917852",
        "password": "BY_PARAHEX-KIFUZAEGI-REDZED"
    },
    {
        "uid": "4231918133",
        "password": "BY_PARAHEX-HF9TVZBTS-REDZED"
    },
    {
        "uid": "4231918319",
        "password": "BY_PARAHEX-ZIOD680VK-REDZED"
    },
    {
        "uid": "4231918525",
        "password": "BY_PARAHEX-VGQC7INZS-REDZED"
    },
    {
        "uid": "4231918743",
        "password": "BY_PARAHEX-NR7RSTMPR-REDZED"
    },
    {
        "uid": "4231918916",
        "password": "BY_PARAHEX-2A9DM3NC9-REDZED"
    },
    {
        "uid": "4231919159",
        "password": "BY_PARAHEX-NUISIPGCX-REDZED"
    },
    {
        "uid": "4231919392",
        "password": "BY_PARAHEX-MCAPXUSEP-REDZED"
    },
    {
        "uid": "4231919656",
        "password": "BY_PARAHEX-NIOUJVJVP-REDZED"
    },
    {
        "uid": "4231919932",
        "password": "BY_PARAHEX-5IFOXTSHV-REDZED"
    },
    {
        "uid": "4231819208",
        "password": "BY_PARAHEX-Z8N8TEKFJ-REDZED"
    },
    {
        "uid": "4231820279",
        "password": "BY_PARAHEX-S7YSBZ33O-REDZED"
    },
    {
        "uid": "4231820676",
        "password": "BY_PARAHEX-RCWZQB42N-REDZED"
    },
    {
        "uid": "4231821948",
        "password": "BY_PARAHEX-KVHAVPTTW-REDZED"
    },
    {
        "uid": "4231822278",
        "password": "BY_PARAHEX-ZXXIQMZGC-REDZED"
    },
    {
        "uid": "4231823064",
        "password": "BY_PARAHEX-XR4NVCSFL-REDZED"
    },
    {
        "uid": "4231824079",
        "password": "BY_PARAHEX-DG5J5HQYV-REDZED"
    },
    {
        "uid": "4231824440",
        "password": "BY_PARAHEX-WZ35TI9BR-REDZED"
    },
    {
        "uid": "4231826078",
        "password": "BY_PARAHEX-5LMXSVH3E-REDZED"
    },
    {
        "uid": "4231826923",
        "password": "BY_PARAHEX-VQT4UY7HG-REDZED"
    },
    {
        "uid": "4231828157",
        "password": "BY_PARAHEX-M8R0C9B3N-REDZED"
    },
    {
        "uid": "4231828630",
        "password": "BY_PARAHEX-C1XLO3KN6-REDZED"
    },
    {
        "uid": "4231829078",
        "password": "BY_PARAHEX-ZDNNSXVJB-REDZED"
    },
    {
        "uid": "4231829573",
        "password": "BY_PARAHEX-M4IFBMKHN-REDZED"
    },
    {
        "uid": "4231831175",
        "password": "BY_PARAHEX-4YVG4LWXE-REDZED"
    },
    {
        "uid": "4231832396",
        "password": "BY_PARAHEX-0LCID5JWQ-REDZED"
    },
    {
        "uid": "4231833250",
        "password": "BY_PARAHEX-5JIB2NQD4-REDZED"
    },
    {
        "uid": "4231834126",
        "password": "BY_PARAHEX-UCDNULJ2C-REDZED"
    },
    {
        "uid": "4231836209",
        "password": "BY_PARAHEX-BWVSNOUE8-REDZED"
    },
    {
        "uid": "4231836752",
        "password": "BY_PARAHEX-VGQNV8HWP-REDZED"
    },
    {
        "uid": "4231838088",
        "password": "BY_PARAHEX-FE1OQW5PI-REDZED"
    },
    {
        "uid": "4231838992",
        "password": "BY_PARAHEX-7IEIDHROT-REDZED"
    },
    {
        "uid": "4231839449",
        "password": "BY_PARAHEX-9KKXMTYTD-REDZED"
    },
    {
        "uid": "4231841006",
        "password": "BY_PARAHEX-DM8C91XIX-REDZED"
    },
    {
        "uid": "4231841593",
        "password": "BY_PARAHEX-WWV82DRX0-REDZED"
    },
    {
        "uid": "4231842494",
        "password": "BY_PARAHEX-FG71RXOZD-REDZED"
    },
    {
        "uid": "4231843385",
        "password": "BY_PARAHEX-5SK2TWZNX-REDZED"
    },
    {
        "uid": "4231844388",
        "password": "BY_PARAHEX-5G7BRDGOF-REDZED"
    },
    {
        "uid": "4231845404",
        "password": "BY_PARAHEX-BCNBNB3TH-REDZED"
    },
    {
        "uid": "4231847813",
        "password": "BY_PARAHEX-JY86MQ33D-REDZED"
    },
    {
        "uid": "4231848824",
        "password": "BY_PARAHEX-OR68NOYSF-REDZED"
    },
    {
        "uid": "4231849889",
        "password": "BY_PARAHEX-CPPCFMBRS-REDZED"
    },
    {
        "uid": "4231850874",
        "password": "BY_PARAHEX-XFXYZXMA3-REDZED"
    },
    {
        "uid": "4231851753",
        "password": "BY_PARAHEX-YFZZYTI9A-REDZED"
    },
    {
        "uid": "4231852732",
        "password": "BY_PARAHEX-VXJDX1CKH-REDZED"
    },
    {
        "uid": "4231854185",
        "password": "BY_PARAHEX-IPFLZAPIH-REDZED"
    },
    {
        "uid": "4231854594",
        "password": "BY_PARAHEX-QMP9MOINN-REDZED"
    },
    {
        "uid": "4231855553",
        "password": "BY_PARAHEX-GGK2R94SX-REDZED"
    },
    {
        "uid": "4231855955",
        "password": "BY_PARAHEX-OKNTOYLNT-REDZED"
    },
    {
        "uid": "4231856871",
        "password": "BY_PARAHEX-BQEDA3AYU-REDZED"
    },
    {
        "uid": "4231857909",
        "password": "BY_PARAHEX-FK5R3NHV6-REDZED"
    },
    {
        "uid": "4231858283",
        "password": "BY_PARAHEX-GQ7NSM0GE-REDZED"
    },
    {
        "uid": "4231858647",
        "password": "BY_PARAHEX-1ZE4ZAAAJ-REDZED"
    },
    {
        "uid": "4231618127",
        "password": "BY_PARAHEX-6FC8UYVNH-REDZED"
    },
    {
        "uid": "4231618887",
        "password": "BY_PARAHEX-YWL8IRVDC-REDZED"
    },
    {
        "uid": "4231620145",
        "password": "BY_PARAHEX-82RXYSLOW-REDZED"
    },
    {
        "uid": "4231621486",
        "password": "BY_PARAHEX-WUZW69AIS-REDZED"
    },
    {
        "uid": "4231621990",
        "password": "BY_PARAHEX-HQZKFBUOT-REDZED"
    },
    {
        "uid": "4231623301",
        "password": "BY_PARAHEX-IWOLDKKOX-REDZED"
    },
    {
        "uid": "4231625287",
        "password": "BY_PARAHEX-MFWDD1ZNQ-REDZED"
    },
    {
        "uid": "4231626334",
        "password": "BY_PARAHEX-DISQTDD0M-REDZED"
    },
    {
        "uid": "4231626858",
        "password": "BY_PARAHEX-SQJMPFYLY-REDZED"
    },
    {
        "uid": "4231627333",
        "password": "BY_PARAHEX-YJMJ7QW31-REDZED"
    },
    {
        "uid": "4231629254",
        "password": "BY_PARAHEX-OYVFNUYBT-REDZED"
    },
    {
        "uid": "4231630199",
        "password": "BY_PARAHEX-WOORPCJWB-REDZED"
    },
    {
        "uid": "4231630822",
        "password": "BY_PARAHEX-GK1CQAA9O-REDZED"
    },
    {
        "uid": "4231632388",
        "password": "BY_PARAHEX-MRUOKPSBR-REDZED"
    },
    {
        "uid": "4231633369",
        "password": "BY_PARAHEX-ZPHQOUSA5-REDZED"
    },
    {
        "uid": "4231635326",
        "password": "BY_PARAHEX-OS282AN46-REDZED"
    },
    {
        "uid": "4231636212",
        "password": "BY_PARAHEX-GIZCGQZWL-REDZED"
    },
    {
        "uid": "4231636580",
        "password": "BY_PARAHEX-9UC1UNWHF-REDZED"
    },
    {
        "uid": "4231637884",
        "password": "BY_PARAHEX-PMHVXM7S3-REDZED"
    },
    {
        "uid": "4231639323",
        "password": "BY_PARAHEX-C1F0LSH2T-REDZED"
    },
    {
        "uid": "4231640075",
        "password": "BY_PARAHEX-PSR4UGVYY-REDZED"
    },
    {
        "uid": "4231640949",
        "password": "BY_PARAHEX-FDWHI6G8M-REDZED"
    },
    {
        "uid": "4231641384",
        "password": "BY_PARAHEX-8ZJ3X2B4Z-REDZED"
    },
    {
        "uid": "4231642343",
        "password": "BY_PARAHEX-KIIS2W4LX-REDZED"
    },
    {
        "uid": "4231643147",
        "password": "BY_PARAHEX-GHMLPZ73E-REDZED"
    },
    {
        "uid": "4231643877",
        "password": "BY_PARAHEX-320SOQ068-REDZED"
    },
    {
        "uid": "4231644205",
        "password": "BY_PARAHEX-LUXFZAMDQ-REDZED"
    },
    {
        "uid": "4231644964",
        "password": "BY_PARAHEX-JJWJ0HD3M-REDZED"
    },
    {
        "uid": "4231645507",
        "password": "BY_PARAHEX-JCLODA1WD-REDZED"
    },
    {
        "uid": "4231646368",
        "password": "BY_PARAHEX-DMIZ9N9GN-REDZED"
    },
    {
        "uid": "4231646711",
        "password": "BY_PARAHEX-CN49DFMNF-REDZED"
    },
    {
        "uid": "4231648117",
        "password": "BY_PARAHEX-RXEKJIFP0-REDZED"
    },
    {
        "uid": "4231648988",
        "password": "BY_PARAHEX-GBR85MEHS-REDZED"
    },
    {
        "uid": "4231649928",
        "password": "BY_PARAHEX-BHAWEWUA4-REDZED"
    },
    {
        "uid": "4231650973",
        "password": "BY_PARAHEX-TGD7CIFWN-REDZED"
    },
    {
        "uid": "4231652188",
        "password": "BY_PARAHEX-N3DLE5GCY-REDZED"
    },
    {
        "uid": "4231653052",
        "password": "BY_PARAHEX-0BIWCA2RN-REDZED"
    },
    {
        "uid": "4231654405",
        "password": "BY_PARAHEX-5UXMIXEFN-REDZED"
    },
    {
        "uid": "4231654713",
        "password": "BY_PARAHEX-E0W5BOVII-REDZED"
    },
    {
        "uid": "4231655908",
        "password": "BY_PARAHEX-Y6HLYEDG3-REDZED"
    },
    {
        "uid": "4231656432",
        "password": "BY_PARAHEX-IPKCAPBBV-REDZED"
    },
    {
        "uid": "4231657974",
        "password": "BY_PARAHEX-8YUE25QGD-REDZED"
    },
    {
        "uid": "4231658497",
        "password": "BY_PARAHEX-CIBBR0NLF-REDZED"
    },
    {
        "uid": "4231659408",
        "password": "BY_PARAHEX-SMNRIJRKA-REDZED"
    },
    {
        "uid": "4231660320",
        "password": "BY_PARAHEX-KDLCTKJMH-REDZED"
    },
    {
        "uid": "4231661826",
        "password": "BY_PARAHEX-MQNOJKTHB-REDZED"
    },
    {
        "uid": "4231663592",
        "password": "BY_PARAHEX-QPYQWK2OE-REDZED"
    },
    {
        "uid": "4231718237",
        "password": "BY_PARAHEX-TMCPT3EVH-REDZED"
    },
    {
        "uid": "4231718763",
        "password": "BY_PARAHEX-9XBGYYYIU-REDZED"
    },
    {
        "uid": "4231719653",
        "password": "BY_PARAHEX-ZVCT3V40Y-REDZED"
    },
    {
        "uid": "4231720522",
        "password": "BY_PARAHEX-RKXCWFQDE-REDZED"
    },
    {
        "uid": "4231720913",
        "password": "BY_PARAHEX-EJZQHZH1W-REDZED"
    },
    {
        "uid": "4231721385",
        "password": "BY_PARAHEX-B0MLHSXZ9-REDZED"
    },
    {
        "uid": "4231721748",
        "password": "BY_PARAHEX-OAVQYMB9L-REDZED"
    },
    {
        "uid": "4231722155",
        "password": "BY_PARAHEX-LPFSMA0EL-REDZED"
    },
    {
        "uid": "4231723093",
        "password": "BY_PARAHEX-BVPNDMDYB-REDZED"
    },
    {
        "uid": "4231723932",
        "password": "BY_PARAHEX-MNOHT44YR-REDZED"
    },
    {
        "uid": "4231724314",
        "password": "BY_PARAHEX-GH2KHQRFI-REDZED"
    },
    {
        "uid": "4231725199",
        "password": "BY_PARAHEX-S556TV4GK-REDZED"
    },
    {
        "uid": "4231725989",
        "password": "BY_PARAHEX-CHQFJHPFS-REDZED"
    },
    {
        "uid": "4231726922",
        "password": "BY_PARAHEX-6RPCSGQ6V-REDZED"
    },
    {
        "uid": "4231727814",
        "password": "BY_PARAHEX-IVDXPJFC6-REDZED"
    },
    {
        "uid": "4231729073",
        "password": "BY_PARAHEX-LI2K1XNTE-REDZED"
    },
    {
        "uid": "4231729407",
        "password": "BY_PARAHEX-CT5KZC6DB-REDZED"
    },
    {
        "uid": "4231729846",
        "password": "BY_PARAHEX-P2TPFPPDF-REDZED"
    },
    {
        "uid": "4231730781",
        "password": "BY_PARAHEX-XMQB5DFNI-REDZED"
    },
    {
        "uid": "4231731243",
        "password": "BY_PARAHEX-KQF9PGVDK-REDZED"
    },
    {
        "uid": "4231732136",
        "password": "BY_PARAHEX-L8I7GPIIS-REDZED"
    },
    {
        "uid": "4231733158",
        "password": "BY_PARAHEX-WCVQ6XGOL-REDZED"
    },
    {
        "uid": "4231734531",
        "password": "BY_PARAHEX-GI2S5XKYL-REDZED"
    },
    {
        "uid": "4231734948",
        "password": "BY_PARAHEX-XVQNS0WPZ-REDZED"
    },
    {
        "uid": "4231737054",
        "password": "BY_PARAHEX-DPKCKMYDQ-REDZED"
    },
    {
        "uid": "4231738034",
        "password": "BY_PARAHEX-G1W4MJVAH-REDZED"
    },
    {
        "uid": "4231739015",
        "password": "BY_PARAHEX-2UQI5URAI-REDZED"
    },
    {
        "uid": "4231740206",
        "password": "BY_PARAHEX-OYGG3HMOB-REDZED"
    },
    {
        "uid": "4231741279",
        "password": "BY_PARAHEX-HVRBX3VZV-REDZED"
    },
    {
        "uid": "4231742252",
        "password": "BY_PARAHEX-7VWHYMONU-REDZED"
    },
    {
        "uid": "4231742598",
        "password": "BY_PARAHEX-YEDSUKQ7U-REDZED"
    },
    {
        "uid": "4231743924",
        "password": "BY_PARAHEX-LY9B1SKJE-REDZED"
    },
    {
        "uid": "4231744471",
        "password": "BY_PARAHEX-KXYDIPPES-REDZED"
    },
    {
        "uid": "4231746082",
        "password": "BY_PARAHEX-LM26TVNC2-REDZED"
    },
    {
        "uid": "4231749503",
        "password": "BY_PARAHEX-UFPNVWOSQ-REDZED"
    },
    {
        "uid": "4231750563",
        "password": "BY_PARAHEX-0VAHRJZ9H-REDZED"
    },
    {
        "uid": "4231751018",
        "password": "BY_PARAHEX-SHBMJTBHA-REDZED"
    },
    {
        "uid": "4231752217",
        "password": "BY_PARAHEX-9GR7GZZFT-REDZED"
    },
    {
        "uid": "4231753122",
        "password": "BY_PARAHEX-HHYY2TJBQ-REDZED"
    },
    {
        "uid": "4231754533",
        "password": "BY_PARAHEX-BUZH2XB9K-REDZED"
    },
    {
        "uid": "4231755016",
        "password": "BY_PARAHEX-HKKHXUVHB-REDZED"
    },
    {
        "uid": "4231755434",
        "password": "BY_PARAHEX-U7OVKIAXP-REDZED"
    },
    {
        "uid": "4231756773",
        "password": "BY_PARAHEX-RMMDQF6GY-REDZED"
    },
    {
        "uid": "4231758077",
        "password": "BY_PARAHEX-MSEJRG6LS-REDZED"
    },
    {
        "uid": "4231759404",
        "password": "BY_PARAHEX-FRVEELNOQ-REDZED"
    },
    {
        "uid": "4231759709",
        "password": "BY_PARAHEX-NCABFY2ZI-REDZED"
    },
    {
        "uid": "4231760297",
        "password": "BY_PARAHEX-Q0L6ZL1DJ-REDZED"
    },
    {
        "uid": "4231760763",
        "password": "BY_PARAHEX-ZEODIIEGJ-REDZED"
    },
    {
        "uid": "4231761287",
        "password": "BY_PARAHEX-RDYJCPXQZ-REDZED"
    },
    {
        "uid": "4231761787",
        "password": "BY_PARAHEX-DHYYUCFVQ-REDZED"
    },
    {
        "uid": "4230595792",
        "password": "BY_PARAHEX-2W2OZIOLJ-REDZED"
    },
    {
        "uid": "4230595966",
        "password": "BY_PARAHEX-TF9RWIHT7-REDZED"
    },
    {
        "uid": "4230596081",
        "password": "BY_PARAHEX-VXLT3CVXH-REDZED"
    },
    {
        "uid": "4230596170",
        "password": "BY_PARAHEX-56NHEMBJ6-REDZED"
    },
    {
        "uid": "4230596236",
        "password": "BY_PARAHEX-CNPW73LQZ-REDZED"
    },
    {
        "uid": "4230596314",
        "password": "BY_PARAHEX-Q6ABNX6TF-REDZED"
    },
    {
        "uid": "4230596419",
        "password": "BY_PARAHEX-AR3HZXRGY-REDZED"
    },
    {
        "uid": "4230596495",
        "password": "BY_PARAHEX-1SYYGRGYN-REDZED"
    },
    {
        "uid": "4230596577",
        "password": "BY_PARAHEX-IORYUJOAB-REDZED"
    },
    {
        "uid": "4230596651",
        "password": "BY_PARAHEX-AUM18F8BA-REDZED"
    },
    {
        "uid": "4230596735",
        "password": "BY_PARAHEX-UHL5XATK1-REDZED"
    },
    {
        "uid": "4230596827",
        "password": "BY_PARAHEX-NNDBWJW8T-REDZED"
    },
    {
        "uid": "4230596880",
        "password": "BY_PARAHEX-3AAVUPPHA-REDZED"
    },
    {
        "uid": "4230596969",
        "password": "BY_PARAHEX-PSNHOZYN8-REDZED"
    },
    {
        "uid": "4230597260",
        "password": "BY_PARAHEX-AOVK6M2LP-REDZED"
    },
    {
        "uid": "4230597341",
        "password": "BY_PARAHEX-DEEZ92JBF-REDZED"
    },
    {
        "uid": "4230597431",
        "password": "BY_PARAHEX-SQKBJAYRK-REDZED"
    },
    {
        "uid": "4230597503",
        "password": "BY_PARAHEX-G370AYV7O-REDZED"
    },
    {
        "uid": "4230597575",
        "password": "BY_PARAHEX-AK8BCM659-REDZED"
    },
    {
        "uid": "4230597651",
        "password": "BY_PARAHEX-AEGCAQCJO-REDZED"
    },
    {
        "uid": "4230597732",
        "password": "BY_PARAHEX-K99NEXWFT-REDZED"
    },
    {
        "uid": "4230597896",
        "password": "BY_PARAHEX-AP6K3GHCJ-REDZED"
    },
    {
        "uid": "4230597978",
        "password": "BY_PARAHEX-JCOCL3NM6-REDZED"
    },
    {
        "uid": "4230598061",
        "password": "BY_PARAHEX-JJQIBH3GZ-REDZED"
    },
    {
        "uid": "4230598155",
        "password": "BY_PARAHEX-ED9OWX6DK-REDZED"
    },
    {
        "uid": "4230598220",
        "password": "BY_PARAHEX-B1BMCYZ2A-REDZED"
    },
    {
        "uid": "4230598300",
        "password": "BY_PARAHEX-OCMPAO33R-REDZED"
    },
    {
        "uid": "4230598411",
        "password": "BY_PARAHEX-CMLGV2FFI-REDZED"
    },
    {
        "uid": "4230598509",
        "password": "BY_PARAHEX-ETO17XK9S-REDZED"
    },
    {
        "uid": "4230598639",
        "password": "BY_PARAHEX-NLBCDE9HZ-REDZED"
    },
    {
        "uid": "4230598742",
        "password": "BY_PARAHEX-1JUMRWRJO-REDZED"
    },
    {
        "uid": "4230598824",
        "password": "BY_PARAHEX-9K2NPZCEN-REDZED"
    },
    {
        "uid": "4230598914",
        "password": "BY_PARAHEX-VTBPQD34C-REDZED"
    },
    {
        "uid": "4230598997",
        "password": "BY_PARAHEX-NDCXI02DZ-REDZED"
    },
    {
        "uid": "4230599079",
        "password": "BY_PARAHEX-XCY7PZR0J-REDZED"
    },
    {
        "uid": "4230599151",
        "password": "BY_PARAHEX-5IRYRRQUW-REDZED"
    },
    {
        "uid": "4230599235",
        "password": "BY_PARAHEX-XJBRMOVCE-REDZED"
    },
    {
        "uid": "4230599364",
        "password": "BY_PARAHEX-HGAONLIN1-REDZED"
    },
    {
        "uid": "4230599458",
        "password": "BY_PARAHEX-WUVJ6TXTK-REDZED"
    },
    {
        "uid": "4230599535",
        "password": "BY_PARAHEX-6KUARJ0GI-REDZED"
    },
    {
        "uid": "4230599613",
        "password": "BY_PARAHEX-54H6JWTTG-REDZED"
    },
    {
        "uid": "4230599695",
        "password": "BY_PARAHEX-E5YSIWF1G-REDZED"
    },
    {
        "uid": "4230599764",
        "password": "BY_PARAHEX-VY93W9NU1-REDZED"
    },
    {
        "uid": "4230599840",
        "password": "BY_PARAHEX-CVAO34GBL-REDZED"
    },
    {
        "uid": "4230599916",
        "password": "BY_PARAHEX-YIGUYCVNM-REDZED"
    },
    {
        "uid": "4230600030",
        "password": "BY_PARAHEX-7T23AZVBV-REDZED"
    },
    {
        "uid": "4230600117",
        "password": "BY_PARAHEX-XPPAULDLV-REDZED"
    },
    {
        "uid": "4230600213",
        "password": "BY_PARAHEX-OZ8A1CL09-REDZED"
    },
    {
        "uid": "4230600295",
        "password": "BY_PARAHEX-M834E7KMG-REDZED"
    },
    {
        "uid": "4230600374",
        "password": "BY_PARAHEX-AU8XPURYO-REDZED"
    },
    {
        "uid": "4230524185",
        "password": "BY_PARAHEX-O5VSTTX3Q-REDZED"
    },
    {
        "uid": "4230524271",
        "password": "BY_PARAHEX-BAKY1RK1W-REDZED"
    },
    {
        "uid": "4230524360",
        "password": "BY_PARAHEX-H1GIHMRLO-REDZED"
    },
    {
        "uid": "4230524483",
        "password": "BY_PARAHEX-HV02JAWEY-REDZED"
    },
    {
        "uid": "4230524577",
        "password": "BY_PARAHEX-ANBHDSCZA-REDZED"
    },
    {
        "uid": "4230524743",
        "password": "BY_PARAHEX-RY1ICFE66-REDZED"
    },
    {
        "uid": "4230524859",
        "password": "BY_PARAHEX-ACLSEXIKD-REDZED"
    },
    {
        "uid": "4230524965",
        "password": "BY_PARAHEX-IIBO5WAPL-REDZED"
    },
    {
        "uid": "4230525076",
        "password": "BY_PARAHEX-DPRSXEOP6-REDZED"
    },
    {
        "uid": "4230525222",
        "password": "BY_PARAHEX-VHU7VCD8R-REDZED"
    },
    {
        "uid": "4230525318",
        "password": "BY_PARAHEX-UVMHEM4FA-REDZED"
    },
    {
        "uid": "4230525450",
        "password": "BY_PARAHEX-7LUZIPKYY-REDZED"
    },
    {
        "uid": "4230525586",
        "password": "BY_PARAHEX-O4ZMX73OV-REDZED"
    },
    {
        "uid": "4230525720",
        "password": "BY_PARAHEX-2GT7QSUW2-REDZED"
    },
    {
        "uid": "4230525843",
        "password": "BY_PARAHEX-C1J9CJ2F0-REDZED"
    },
    {
        "uid": "4230525985",
        "password": "BY_PARAHEX-EM6EBWFNU-REDZED"
    },
    {
        "uid": "4230526126",
        "password": "BY_PARAHEX-X7HXOQQXO-REDZED"
    },
    {
        "uid": "4230526311",
        "password": "BY_PARAHEX-V5DXWCOLR-REDZED"
    },
    {
        "uid": "4230526444",
        "password": "BY_PARAHEX-AYSNPPYOF-REDZED"
    },
    {
        "uid": "4230526539",
        "password": "BY_PARAHEX-SHJFNNBTR-REDZED"
    },
    {
        "uid": "4230526652",
        "password": "BY_PARAHEX-ZYWG7UXSJ-REDZED"
    },
    {
        "uid": "4230526775",
        "password": "BY_PARAHEX-CCM2PJHVF-REDZED"
    },
    {
        "uid": "4230526882",
        "password": "BY_PARAHEX-B7G8VZYJZ-REDZED"
    },
    {
        "uid": "4230527008",
        "password": "BY_PARAHEX-BKFGFUOUF-REDZED"
    },
    {
        "uid": "4230527092",
        "password": "BY_PARAHEX-HUDVTGXPX-REDZED"
    },
    {
        "uid": "4230527208",
        "password": "BY_PARAHEX-WUMXFSGSN-REDZED"
    },
    {
        "uid": "4230527308",
        "password": "BY_PARAHEX-RLJGMYM7X-REDZED"
    },
    {
        "uid": "4230527455",
        "password": "BY_PARAHEX-APHYRIHWA-REDZED"
    },
    {
        "uid": "4230527551",
        "password": "BY_PARAHEX-RPQNZD1EP-REDZED"
    },
    {
        "uid": "4230527673",
        "password": "BY_PARAHEX-FJOSXOHKW-REDZED"
    },
    {
        "uid": "4230527785",
        "password": "BY_PARAHEX-9M7SCIATU-REDZED"
    },
    {
        "uid": "4230527895",
        "password": "BY_PARAHEX-REJCR2XIB-REDZED"
    },
    {
        "uid": "4230528022",
        "password": "BY_PARAHEX-WLEIHUJPZ-REDZED"
    },
    {
        "uid": "4230528150",
        "password": "BY_PARAHEX-VIXZIYPUP-REDZED"
    },
    {
        "uid": "4230528425",
        "password": "BY_PARAHEX-DID1HXEHV-REDZED"
    },
    {
        "uid": "4230528624",
        "password": "BY_PARAHEX-27EZM1EBJ-REDZED"
    },
    {
        "uid": "4230528769",
        "password": "BY_PARAHEX-X9D0H4QAI-REDZED"
    },
    {
        "uid": "4230528957",
        "password": "BY_PARAHEX-SGYZVVUYM-REDZED"
    },
    {
        "uid": "4230529125",
        "password": "BY_PARAHEX-BOY1VFIOZ-REDZED"
    },
    {
        "uid": "4230529291",
        "password": "BY_PARAHEX-YEAN0TTYK-REDZED"
    },
    {
        "uid": "4230529462",
        "password": "BY_PARAHEX-KY9QFAZZ7-REDZED"
    },
    {
        "uid": "4230529652",
        "password": "BY_PARAHEX-SQ4EIRFDZ-REDZED"
    },
    {
        "uid": "4230529863",
        "password": "BY_PARAHEX-DKBR3LSCB-REDZED"
    },
    {
        "uid": "4230530043",
        "password": "BY_PARAHEX-TNJOPX5E2-REDZED"
    },
    {
        "uid": "4230530184",
        "password": "BY_PARAHEX-FTD1AUVZF-REDZED"
    },
    {
        "uid": "4230530438",
        "password": "BY_PARAHEX-SA6LU5U68-REDZED"
    },
    {
        "uid": "4230530607",
        "password": "BY_PARAHEX-9RE9QELGM-REDZED"
    },
    {
        "uid": "4230530838",
        "password": "BY_PARAHEX-TBCGNZYJM-REDZED"
    },
    {
        "uid": "4230530960",
        "password": "BY_PARAHEX-HIXTWCIQ9-REDZED"
    },
    {
        "uid": "4230531042",
        "password": "BY_PARAHEX-CY0BLEJ4Z-REDZED"
    },
    {
        "uid": "4230532798",
        "password": "BY_PARAHEX-4XYKNAYJO-REDZED"
    },
    {
        "uid": "4230532957",
        "password": "BY_PARAHEX-VM8BLUH73-REDZED"
    },
    {
        "uid": "4230533094",
        "password": "BY_PARAHEX-G1DKEPC93-REDZED"
    },
    {
        "uid": "4230533228",
        "password": "BY_PARAHEX-H8W3HVZCG-REDZED"
    },
    {
        "uid": "4230533403",
        "password": "BY_PARAHEX-TRVY1NJG0-REDZED"
    },
    {
        "uid": "4230533600",
        "password": "BY_PARAHEX-FKMAK3ROH-REDZED"
    },
    {
        "uid": "4230533729",
        "password": "BY_PARAHEX-FLPBPY0ZA-REDZED"
    },
    {
        "uid": "4230533874",
        "password": "BY_PARAHEX-50BHGJDTU-REDZED"
    },
    {
        "uid": "4230534002",
        "password": "BY_PARAHEX-4GDXDGT1S-REDZED"
    },
    {
        "uid": "4230534152",
        "password": "BY_PARAHEX-1MLRXOVJS-REDZED"
    },
    {
        "uid": "4230534326",
        "password": "BY_PARAHEX-REY7ZK5ZV-REDZED"
    },
    {
        "uid": "4230534460",
        "password": "BY_PARAHEX-JHABZYMQV-REDZED"
    },
    {
        "uid": "4230534626",
        "password": "BY_PARAHEX-OYBE2PFDH-REDZED"
    },
    {
        "uid": "4230534774",
        "password": "BY_PARAHEX-2PUVOOMAU-REDZED"
    },
    {
        "uid": "4230534944",
        "password": "BY_PARAHEX-D8BX1ALWR-REDZED"
    },
    {
        "uid": "4230535053",
        "password": "BY_PARAHEX-MXTMTNXD1-REDZED"
    },
    {
        "uid": "4230535211",
        "password": "BY_PARAHEX-0XTVTU2GD-REDZED"
    },
    {
        "uid": "4230535357",
        "password": "BY_PARAHEX-PVDKWPPB9-REDZED"
    },
    {
        "uid": "4230535449",
        "password": "BY_PARAHEX-HG71SL6JN-REDZED"
    },
    {
        "uid": "4230535582",
        "password": "BY_PARAHEX-GR0OVXR0W-REDZED"
    },
    {
        "uid": "4230535818",
        "password": "BY_PARAHEX-TULOU4OIO-REDZED"
    },
    {
        "uid": "4230535931",
        "password": "BY_PARAHEX-FKFTE80O2-REDZED"
    },
    {
        "uid": "4230536029",
        "password": "BY_PARAHEX-OLZI3KXW7-REDZED"
    },
    {
        "uid": "4230536159",
        "password": "BY_PARAHEX-8UOQFXGIA-REDZED"
    },
    {
        "uid": "4230536257",
        "password": "BY_PARAHEX-A6GYF0IAJ-REDZED"
    },
    {
        "uid": "4230536398",
        "password": "BY_PARAHEX-OFSEACNZP-REDZED"
    },
    {
        "uid": "4230536531",
        "password": "BY_PARAHEX-BGZAM7XK5-REDZED"
    },
    {
        "uid": "4230536687",
        "password": "BY_PARAHEX-8LETXPYGL-REDZED"
    },
    {
        "uid": "4230536810",
        "password": "BY_PARAHEX-HYCMPFMZG-REDZED"
    },
    {
        "uid": "4230536980",
        "password": "BY_PARAHEX-KKYLPMYQA-REDZED"
    },
    {
        "uid": "4230537170",
        "password": "BY_PARAHEX-C1KIPKXBX-REDZED"
    },
    {
        "uid": "4230537465",
        "password": "BY_PARAHEX-CJBYCHUII-REDZED"
    },
    {
        "uid": "4230537664",
        "password": "BY_PARAHEX-KOJATARI0-REDZED"
    },
    {
        "uid": "4230537864",
        "password": "BY_PARAHEX-OEN7ZXXAU-REDZED"
    },
    {
        "uid": "4230538030",
        "password": "BY_PARAHEX-YKVBEDVIV-REDZED"
    },
    {
        "uid": "4230538176",
        "password": "BY_PARAHEX-6BQZEH1ZI-REDZED"
    },
    {
        "uid": "4230538279",
        "password": "BY_PARAHEX-N540VNYHV-REDZED"
    },
    {
        "uid": "4230538375",
        "password": "BY_PARAHEX-UBZDHRMBG-REDZED"
    },
    {
        "uid": "4230538493",
        "password": "BY_PARAHEX-R7DQN3JX5-REDZED"
    },
    {
        "uid": "4230538657",
        "password": "BY_PARAHEX-CU4VC4UKF-REDZED"
    },
    {
        "uid": "4230538797",
        "password": "BY_PARAHEX-INUG42LH0-REDZED"
    },
    {
        "uid": "4230538937",
        "password": "BY_PARAHEX-UUVEONRYZ-REDZED"
    },
    {
        "uid": "4230539092",
        "password": "BY_PARAHEX-IGBXSVFQX-REDZED"
    },
    {
        "uid": "4230539207",
        "password": "BY_PARAHEX-ZBYJTH12W-REDZED"
    },
    {
        "uid": "4230539366",
        "password": "BY_PARAHEX-XB1DSQSXK-REDZED"
    },
    {
        "uid": "4230539488",
        "password": "BY_PARAHEX-ZH2GFQQDU-REDZED"
    },
    {
        "uid": "4230539607",
        "password": "BY_PARAHEX-F2ZGQERTJ-REDZED"
    },
    {
        "uid": "4230539694",
        "password": "BY_PARAHEX-JLTJQPK5Z-REDZED"
    },
    {
        "uid": "4230539812",
        "password": "BY_PARAHEX-K7D77MNJI-REDZED"
    },
    {
        "uid": "4230539936",
        "password": "BY_PARAHEX-TKCSEEYJE-REDZED"
    },
    {
        "uid": "4230541149",
        "password": "BY_PARAHEX-FZMEDRK8R-REDZED"
    },
    {
        "uid": "4230541300",
        "password": "BY_PARAHEX-JDFN0EBMC-REDZED"
    },
    {
        "uid": "4230541449",
        "password": "BY_PARAHEX-07FLMSDET-REDZED"
    },
    {
        "uid": "4230541770",
        "password": "BY_PARAHEX-WJZK8CNZB-REDZED"
    },
    {
        "uid": "4230541901",
        "password": "BY_PARAHEX-VGD9S686E-REDZED"
    },
    {
        "uid": "4230542056",
        "password": "BY_PARAHEX-Y1B1LBL6C-REDZED"
    },
    {
        "uid": "4230542275",
        "password": "BY_PARAHEX-D5KQJBYF8-REDZED"
    },
    {
        "uid": "4230542394",
        "password": "BY_PARAHEX-75ZH7DOYW-REDZED"
    },
    {
        "uid": "4230542531",
        "password": "BY_PARAHEX-BN9HJVMC6-REDZED"
    },
    {
        "uid": "4230542648",
        "password": "BY_PARAHEX-DVRTVPEBV-REDZED"
    },
    {
        "uid": "4230542826",
        "password": "BY_PARAHEX-U4TQKLOCB-REDZED"
    },
    {
        "uid": "4230543010",
        "password": "BY_PARAHEX-ER1CDN9RU-REDZED"
    },
    {
        "uid": "4230543147",
        "password": "BY_PARAHEX-IIYTEX7QA-REDZED"
    },
    {
        "uid": "4230543326",
        "password": "BY_PARAHEX-CU6YJK2CQ-REDZED"
    },
    {
        "uid": "4230543451",
        "password": "BY_PARAHEX-7TZGTZAPY-REDZED"
    },
    {
        "uid": "4230543606",
        "password": "BY_PARAHEX-WAPVDP7WP-REDZED"
    },
    {
        "uid": "4230543738",
        "password": "BY_PARAHEX-QTIKJF7JB-REDZED"
    },
    {
        "uid": "4230543859",
        "password": "BY_PARAHEX-8VUDDF03I-REDZED"
    },
    {
        "uid": "4230543995",
        "password": "BY_PARAHEX-LJAGBTBCW-REDZED"
    },
    {
        "uid": "4230544143",
        "password": "BY_PARAHEX-IHTDN1GSJ-REDZED"
    },
    {
        "uid": "4230544232",
        "password": "BY_PARAHEX-2BTWGLZSS-REDZED"
    },
    {
        "uid": "4230544384",
        "password": "BY_PARAHEX-RNCGROF8S-REDZED"
    },
    {
        "uid": "4230544521",
        "password": "BY_PARAHEX-IPUUMVKNJ-REDZED"
    },
    {
        "uid": "4230544648",
        "password": "BY_PARAHEX-OOK1JHUON-REDZED"
    },
    {
        "uid": "4230544783",
        "password": "BY_PARAHEX-EDJXRIZDL-REDZED"
    },
    {
        "uid": "4230544898",
        "password": "BY_PARAHEX-YPQVC79LS-REDZED"
    },
    {
        "uid": "4230545057",
        "password": "BY_PARAHEX-VLQ5PXY96-REDZED"
    },
    {
        "uid": "4230545235",
        "password": "BY_PARAHEX-LWD30VT7G-REDZED"
    },
    {
        "uid": "4230545450",
        "password": "BY_PARAHEX-SYQBB4AN0-REDZED"
    },
    {
        "uid": "4230545594",
        "password": "BY_PARAHEX-LKTCBRAL1-REDZED"
    },
    {
        "uid": "4230545725",
        "password": "BY_PARAHEX-PGAIDLEPL-REDZED"
    },
    {
        "uid": "4230545896",
        "password": "BY_PARAHEX-X2R6KTJ8T-REDZED"
    },
    {
        "uid": "4230546223",
        "password": "BY_PARAHEX-IJH16NQSJ-REDZED"
    },
    {
        "uid": "4230546367",
        "password": "BY_PARAHEX-TFGOB7SSY-REDZED"
    },
    {
        "uid": "4230546516",
        "password": "BY_PARAHEX-LX3APIOLT-REDZED"
    },
    {
        "uid": "4230546720",
        "password": "BY_PARAHEX-GOAWBK3EO-REDZED"
    },
    {
        "uid": "4230546939",
        "password": "BY_PARAHEX-FLHJL15SL-REDZED"
    },
    {
        "uid": "4230547115",
        "password": "BY_PARAHEX-ZTAU4AGUX-REDZED"
    },
    {
        "uid": "4230547352",
        "password": "BY_PARAHEX-6JMIGWHVF-REDZED"
    },
    {
        "uid": "4230547526",
        "password": "BY_PARAHEX-KNBNDJJBX-REDZED"
    },
    {
        "uid": "4230547812",
        "password": "BY_PARAHEX-S8DWJCJ6Y-REDZED"
    },
    {
        "uid": "4230547974",
        "password": "BY_PARAHEX-R9AHZCEPZ-REDZED"
    },
    {
        "uid": "4230548104",
        "password": "BY_PARAHEX-A519PZKPQ-REDZED"
    },
    {
        "uid": "4230548247",
        "password": "BY_PARAHEX-YO2QEJMIW-REDZED"
    },
    {
        "uid": "4230548384",
        "password": "BY_PARAHEX-JADREUSA3-REDZED"
    },
    {
        "uid": "4230548479",
        "password": "BY_PARAHEX-9Y8NQ5JXD-REDZED"
    },
    {
        "uid": "4230548613",
        "password": "BY_PARAHEX-NOQI0KCB1-REDZED"
    },
    {
        "uid": "4230548776",
        "password": "BY_PARAHEX-UJJ9ZE3BC-REDZED"
    },
    {
        "uid": "4230548887",
        "password": "BY_PARAHEX-TAQSKC3U9-REDZED"
    },
    {
        "uid": "4230549027",
        "password": "BY_PARAHEX-A30NQDFOX-REDZED"
    },
    {
        "uid": "4230551379",
        "password": "BY_PARAHEX-0MSPEVFYW-REDZED"
    },
    {
        "uid": "4230551579",
        "password": "BY_PARAHEX-7XFIGLPMK-REDZED"
    },
    {
        "uid": "4230551721",
        "password": "BY_PARAHEX-0QXGRT57S-REDZED"
    },
    {
        "uid": "4230551841",
        "password": "BY_PARAHEX-HWKKGCEGF-REDZED"
    },
    {
        "uid": "4230551982",
        "password": "BY_PARAHEX-YOYZGCO9W-REDZED"
    },
    {
        "uid": "4230552115",
        "password": "BY_PARAHEX-KP3QW1WBZ-REDZED"
    },
    {
        "uid": "4230552268",
        "password": "BY_PARAHEX-X738KPE6G-REDZED"
    },
    {
        "uid": "4230552397",
        "password": "BY_PARAHEX-LKIOVWDOH-REDZED"
    },
    {
        "uid": "4230552490",
        "password": "BY_PARAHEX-F59CQ48RZ-REDZED"
    },
    {
        "uid": "4230552606",
        "password": "BY_PARAHEX-EIRL9OYUZ-REDZED"
    },
    {
        "uid": "4230552714",
        "password": "BY_PARAHEX-Q77PUJDSO-REDZED"
    },
    {
        "uid": "4230552900",
        "password": "BY_PARAHEX-DDFUTQPXC-REDZED"
    },
    {
        "uid": "4230553040",
        "password": "BY_PARAHEX-VGYC4MBLU-REDZED"
    },
    {
        "uid": "4230553189",
        "password": "BY_PARAHEX-OTHIENYGD-REDZED"
    },
    {
        "uid": "4230553323",
        "password": "BY_PARAHEX-UNGZHXED7-REDZED"
    },
    {
        "uid": "4230553426",
        "password": "BY_PARAHEX-JROBADI3I-REDZED"
    },
    {
        "uid": "4230553568",
        "password": "BY_PARAHEX-URTIFUEAL-REDZED"
    },
    {
        "uid": "4230553768",
        "password": "BY_PARAHEX-0NTLYKCLC-REDZED"
    },
    {
        "uid": "4230553910",
        "password": "BY_PARAHEX-R04QAUK6K-REDZED"
    },
    {
        "uid": "4230554043",
        "password": "BY_PARAHEX-KSUG9QFYE-REDZED"
    },
    {
        "uid": "4230554143",
        "password": "BY_PARAHEX-YAWJEVSD7-REDZED"
    },
    {
        "uid": "4230554328",
        "password": "BY_PARAHEX-C3DUJOFRA-REDZED"
    },
    {
        "uid": "4230554464",
        "password": "BY_PARAHEX-5H4DFFYWY-REDZED"
    },
    {
        "uid": "4230554568",
        "password": "BY_PARAHEX-6UAFXZZES-REDZED"
    },
    {
        "uid": "4230554846",
        "password": "BY_PARAHEX-K7ZK6EITZ-REDZED"
    },
    {
        "uid": "4230555105",
        "password": "BY_PARAHEX-DI9BHCILF-REDZED"
    },
    {
        "uid": "4230555379",
        "password": "BY_PARAHEX-5EPN2WMMY-REDZED"
    },
    {
        "uid": "4230555486",
        "password": "BY_PARAHEX-YGV0HDZ8Y-REDZED"
    },
    {
        "uid": "4230555640",
        "password": "BY_PARAHEX-NU8LJ15HC-REDZED"
    },
    {
        "uid": "4230555875",
        "password": "BY_PARAHEX-A4YJ9AB97-REDZED"
    },
    {
        "uid": "4230555984",
        "password": "BY_PARAHEX-CS34VQA9B-REDZED"
    },
    {
        "uid": "4230556180",
        "password": "BY_PARAHEX-M3LSS7ESQ-REDZED"
    },
    {
        "uid": "4230556325",
        "password": "BY_PARAHEX-YI1X4ELGW-REDZED"
    },
    {
        "uid": "4230556492",
        "password": "BY_PARAHEX-Q75IWPBOU-REDZED"
    },
    {
        "uid": "4230556635",
        "password": "BY_PARAHEX-MCMS4U6K3-REDZED"
    },
    {
        "uid": "4230556743",
        "password": "BY_PARAHEX-HI0RMB3UK-REDZED"
    },
    {
        "uid": "4230556850",
        "password": "BY_PARAHEX-4NMV2NV8T-REDZED"
    },
    {
        "uid": "4230557044",
        "password": "BY_PARAHEX-MBNQV4WIK-REDZED"
    },
    {
        "uid": "4230557291",
        "password": "BY_PARAHEX-KLS8RTQVF-REDZED"
    },
    {
        "uid": "4230557453",
        "password": "BY_PARAHEX-7GLLA6NDG-REDZED"
    },
    {
        "uid": "4230557574",
        "password": "BY_PARAHEX-TXUTUACM9-REDZED"
    },
    {
        "uid": "4230557806",
        "password": "BY_PARAHEX-FNHD5K3AZ-REDZED"
    },
    {
        "uid": "4230557959",
        "password": "BY_PARAHEX-BZOUX5FQS-REDZED"
    },
    {
        "uid": "4230558061",
        "password": "BY_PARAHEX-T0YRRY26I-REDZED"
    },
    {
        "uid": "4230558193",
        "password": "BY_PARAHEX-G3RU5DHIM-REDZED"
    },
    {
        "uid": "4230558338",
        "password": "BY_PARAHEX-CR56AQQK8-REDZED"
    },
    {
        "uid": "4230558486",
        "password": "BY_PARAHEX-FYWFQLTY8-REDZED"
    },
    {
        "uid": "4230558717",
        "password": "BY_PARAHEX-LA7UERZOH-REDZED"
    },
    {
        "uid": "4230558835",
        "password": "BY_PARAHEX-BQSXMCPR0-REDZED"
    },
    {
        "uid": "4230559234",
        "password": "BY_PARAHEX-QIEO29QRW-REDZED"
    },
    {
        "uid": "4230560841",
        "password": "BY_PARAHEX-UISIVB0OE-REDZED"
    },
    {
        "uid": "4230560963",
        "password": "BY_PARAHEX-WJ7GSOFCK-REDZED"
    },
    {
        "uid": "4230561128",
        "password": "BY_PARAHEX-8GUYQWO2K-REDZED"
    },
    {
        "uid": "4230561284",
        "password": "BY_PARAHEX-UIDP6CKPD-REDZED"
    },
    {
        "uid": "4230561410",
        "password": "BY_PARAHEX-EEHFE7UTI-REDZED"
    },
    {
        "uid": "4230561594",
        "password": "BY_PARAHEX-4OZHCIWM2-REDZED"
    },
    {
        "uid": "4230561843",
        "password": "BY_PARAHEX-73Y1IV1QT-REDZED"
    },
    {
        "uid": "4230562079",
        "password": "BY_PARAHEX-XOZAV0XL0-REDZED"
    },
    {
        "uid": "4230562218",
        "password": "BY_PARAHEX-NFZUKPHJD-REDZED"
    },
    {
        "uid": "4230562356",
        "password": "BY_PARAHEX-RE4OMSL9W-REDZED"
    },
    {
        "uid": "4230562532",
        "password": "BY_PARAHEX-Q0LA13SAV-REDZED"
    },
    {
        "uid": "4230562715",
        "password": "BY_PARAHEX-AQQBCQHJW-REDZED"
    },
    {
        "uid": "4230562844",
        "password": "BY_PARAHEX-YDWJCGE6Z-REDZED"
    },
    {
        "uid": "4230562938",
        "password": "BY_PARAHEX-QWRETKXPJ-REDZED"
    },
    {
        "uid": "4230563138",
        "password": "BY_PARAHEX-WZ6NXZSVV-REDZED"
    },
    {
        "uid": "4230563286",
        "password": "BY_PARAHEX-9Y0PDED1S-REDZED"
    },
    {
        "uid": "4230563432",
        "password": "BY_PARAHEX-AADNARBHV-REDZED"
    },
    {
        "uid": "4230563573",
        "password": "BY_PARAHEX-GDCXP4BZU-REDZED"
    },
    {
        "uid": "4230563752",
        "password": "BY_PARAHEX-J1UBXARKY-REDZED"
    },
    {
        "uid": "4230563909",
        "password": "BY_PARAHEX-237JYN5YA-REDZED"
    },
    {
        "uid": "4230564109",
        "password": "BY_PARAHEX-FQNJHX2CX-REDZED"
    },
    {
        "uid": "4230564219",
        "password": "BY_PARAHEX-I0WCJP4UE-REDZED"
    },
    {
        "uid": "4230564363",
        "password": "BY_PARAHEX-LYRZNPIJ5-REDZED"
    },
    {
        "uid": "4230564519",
        "password": "BY_PARAHEX-CKTWY1Y9A-REDZED"
    },
    {
        "uid": "4230564669",
        "password": "BY_PARAHEX-CJRZT3DMM-REDZED"
    },
    {
        "uid": "4230564821",
        "password": "BY_PARAHEX-IZAOG8SGO-REDZED"
    },
    {
        "uid": "4230564941",
        "password": "BY_PARAHEX-AA2TTAHAA-REDZED"
    },
    {
        "uid": "4230565110",
        "password": "BY_PARAHEX-00VUYKCON-REDZED"
    },
    {
        "uid": "4230565305",
        "password": "BY_PARAHEX-XHC3BBKSU-REDZED"
    },
    {
        "uid": "4230565439",
        "password": "BY_PARAHEX-ZJUOV4XDZ-REDZED"
    },
    {
        "uid": "4230565582",
        "password": "BY_PARAHEX-XIDSVZCS4-REDZED"
    },
    {
        "uid": "4230565747",
        "password": "BY_PARAHEX-PSWXTGDHQ-REDZED"
    },
    {
        "uid": "4230565926",
        "password": "BY_PARAHEX-1IKUSHLQZ-REDZED"
    },
    {
        "uid": "4230566104",
        "password": "BY_PARAHEX-CJRA0SUND-REDZED"
    },
    {
        "uid": "4230566236",
        "password": "BY_PARAHEX-NDRE9Q4FY-REDZED"
    },
    {
        "uid": "4230566380",
        "password": "BY_PARAHEX-CWRUQ18C3-REDZED"
    },
    {
        "uid": "4230566544",
        "password": "BY_PARAHEX-ORQFBIWLA-REDZED"
    },
    {
        "uid": "4230566660",
        "password": "BY_PARAHEX-YTMHHYP9Q-REDZED"
    },
    {
        "uid": "4230566837",
        "password": "BY_PARAHEX-7QM2Q13LC-REDZED"
    },
    {
        "uid": "4230566990",
        "password": "BY_PARAHEX-TJYI3XNHK-REDZED"
    },
    {
        "uid": "4230567189",
        "password": "BY_PARAHEX-E5FJRG1V5-REDZED"
    },
    {
        "uid": "4230567394",
        "password": "BY_PARAHEX-OBI3EQRHR-REDZED"
    },
    {
        "uid": "4230567530",
        "password": "BY_PARAHEX-11MJGSDX6-REDZED"
    },
    {
        "uid": "4230567662",
        "password": "BY_PARAHEX-MWULIKNOY-REDZED"
    },
    {
        "uid": "4230567858",
        "password": "BY_PARAHEX-OKZUIWL79-REDZED"
    },
    {
        "uid": "4230568009",
        "password": "BY_PARAHEX-QXKBJNAUP-REDZED"
    },
    {
        "uid": "4230568234",
        "password": "BY_PARAHEX-QOKQ0NNAT-REDZED"
    },
    {
        "uid": "4230568348",
        "password": "BY_PARAHEX-6KKG5GLGH-REDZED"
    },
    {
        "uid": "4230568550",
        "password": "BY_PARAHEX-XGXDRE7PA-REDZED"
    },
    {
        "uid": "4230568695",
        "password": "BY_PARAHEX-V3PTRK5HI-REDZED"
    },
    {
        "uid": "4230576838",
        "password": "BY_PARAHEX-MPAFOO5E8-REDZED"
    },
    {
        "uid": "4230577016",
        "password": "BY_PARAHEX-WXKNRGOPH-REDZED"
    },
    {
        "uid": "4230577149",
        "password": "BY_PARAHEX-IMWSVT1AV-REDZED"
    },
    {
        "uid": "4230577280",
        "password": "BY_PARAHEX-EUQJNMGJK-REDZED"
    },
    {
        "uid": "4230577482",
        "password": "BY_PARAHEX-ZWCABS44T-REDZED"
    },
    {
        "uid": "4230577651",
        "password": "BY_PARAHEX-TOIB5YTT3-REDZED"
    },
    {
        "uid": "4230577816",
        "password": "BY_PARAHEX-C9HGPN9QN-REDZED"
    },
    {
        "uid": "4230578002",
        "password": "BY_PARAHEX-8NCZRQX7U-REDZED"
    },
    {
        "uid": "4230578121",
        "password": "BY_PARAHEX-WEX7MVYWU-REDZED"
    },
    {
        "uid": "4230578310",
        "password": "BY_PARAHEX-P7CHTQY1X-REDZED"
    },
    {
        "uid": "4230578461",
        "password": "BY_PARAHEX-NOO8MK17G-REDZED"
    },
    {
        "uid": "4230578626",
        "password": "BY_PARAHEX-OI5RHEKMW-REDZED"
    },
    {
        "uid": "4230578758",
        "password": "BY_PARAHEX-VZ6SJIAAM-REDZED"
    },
    {
        "uid": "4230578969",
        "password": "BY_PARAHEX-WPOAIJLMO-REDZED"
    },
    {
        "uid": "4230579129",
        "password": "BY_PARAHEX-IPDL0SA7M-REDZED"
    },
    {
        "uid": "4230579249",
        "password": "BY_PARAHEX-BSU2GHOEK-REDZED"
    },
    {
        "uid": "4230579394",
        "password": "BY_PARAHEX-VB9VTKFXF-REDZED"
    },
    {
        "uid": "4230579545",
        "password": "BY_PARAHEX-ROXIBBZOP-REDZED"
    },
    {
        "uid": "4230579749",
        "password": "BY_PARAHEX-FHQJIEMUP-REDZED"
    },
    {
        "uid": "4230579914",
        "password": "BY_PARAHEX-64IWNR5P8-REDZED"
    },
    {
        "uid": "4230580033",
        "password": "BY_PARAHEX-OQXHR4CJJ-REDZED"
    },
    {
        "uid": "4230580191",
        "password": "BY_PARAHEX-BEHHF73R8-REDZED"
    },
    {
        "uid": "4230580323",
        "password": "BY_PARAHEX-V3VEK2PHQ-REDZED"
    },
    {
        "uid": "4230580511",
        "password": "BY_PARAHEX-MS9QXF21N-REDZED"
    },
    {
        "uid": "4230580655",
        "password": "BY_PARAHEX-FSUWCTRGP-REDZED"
    },
    {
        "uid": "4230580775",
        "password": "BY_PARAHEX-VHSNIA89W-REDZED"
    },
    {
        "uid": "4230580896",
        "password": "BY_PARAHEX-QCFSFCT9X-REDZED"
    },
    {
        "uid": "4230581061",
        "password": "BY_PARAHEX-9VIDE8DKT-REDZED"
    },
    {
        "uid": "4230581210",
        "password": "BY_PARAHEX-YEJVU1FE5-REDZED"
    },
    {
        "uid": "4230581405",
        "password": "BY_PARAHEX-118ZPJZ6T-REDZED"
    },
    {
        "uid": "4230581533",
        "password": "BY_PARAHEX-OY3DVWOJ1-REDZED"
    },
    {
        "uid": "4230581676",
        "password": "BY_PARAHEX-M8XIMBARS-REDZED"
    },
    {
        "uid": "4230581936",
        "password": "BY_PARAHEX-RTXD5ZWF5-REDZED"
    },
    {
        "uid": "4230582105",
        "password": "BY_PARAHEX-OAKIBK07N-REDZED"
    },
    {
        "uid": "4230582219",
        "password": "BY_PARAHEX-UHTOQUZR5-REDZED"
    },
    {
        "uid": "4230582341",
        "password": "BY_PARAHEX-EAZZMVWXD-REDZED"
    },
    {
        "uid": "4230582547",
        "password": "BY_PARAHEX-WXMGVATME-REDZED"
    },
    {
        "uid": "4230582703",
        "password": "BY_PARAHEX-MSUVECQYY-REDZED"
    },
    {
        "uid": "4230582842",
        "password": "BY_PARAHEX-VSCYNVBQK-REDZED"
    },
    {
        "uid": "4230582984",
        "password": "BY_PARAHEX-FABJ0O6UH-REDZED"
    },
    {
        "uid": "4230583093",
        "password": "BY_PARAHEX-5Y9NIV3ZB-REDZED"
    },
    {
        "uid": "4230583296",
        "password": "BY_PARAHEX-DWH7AXKOG-REDZED"
    },
    {
        "uid": "4230583460",
        "password": "BY_PARAHEX-XAPEKKYXE-REDZED"
    },
    {
        "uid": "4230583621",
        "password": "BY_PARAHEX-5UYA48YI5-REDZED"
    },
    {
        "uid": "4230583755",
        "password": "BY_PARAHEX-BLUQWVVFO-REDZED"
    },
    {
        "uid": "4230583883",
        "password": "BY_PARAHEX-TOQM5AGWL-REDZED"
    },
    {
        "uid": "4230584051",
        "password": "BY_PARAHEX-VUMORGQVX-REDZED"
    },
    {
        "uid": "4230584203",
        "password": "BY_PARAHEX-ENFRFLTAP-REDZED"
    },
    {
        "uid": "4230584317",
        "password": "BY_PARAHEX-L66KHY9OZ-REDZED"
    },
    {
        "uid": "4230584484",
        "password": "BY_PARAHEX-O179RP3DA-REDZED"
    },
    {
        "uid": "4230585605",
        "password": "BY_PARAHEX-01XSONNTM-REDZED"
    },
    {
        "uid": "4230585724",
        "password": "BY_PARAHEX-U1URHN4OE-REDZED"
    },
    {
        "uid": "4230585859",
        "password": "BY_PARAHEX-TVQXJIZBJ-REDZED"
    },
    {
        "uid": "4230585955",
        "password": "BY_PARAHEX-ZLWNOXJJ0-REDZED"
    },
    {
        "uid": "4230586083",
        "password": "BY_PARAHEX-LBOJKAU7J-REDZED"
    },
    {
        "uid": "4230586204",
        "password": "BY_PARAHEX-748UZHJAH-REDZED"
    },
    {
        "uid": "4230586363",
        "password": "BY_PARAHEX-NVKMHGGFH-REDZED"
    },
    {
        "uid": "4230586456",
        "password": "BY_PARAHEX-DFDCD2S4E-REDZED"
    },
    {
        "uid": "4230586542",
        "password": "BY_PARAHEX-28OO2H06S-REDZED"
    },
    {
        "uid": "4230586647",
        "password": "BY_PARAHEX-APBOIFSTI-REDZED"
    },
    {
        "uid": "4230586742",
        "password": "BY_PARAHEX-U1HJA4WPB-REDZED"
    },
    {
        "uid": "4230586871",
        "password": "BY_PARAHEX-V1ZNJEGLK-REDZED"
    },
    {
        "uid": "4230586995",
        "password": "BY_PARAHEX-CJJD0IMNE-REDZED"
    },
    {
        "uid": "4230587084",
        "password": "BY_PARAHEX-DQIS1C0PE-REDZED"
    },
    {
        "uid": "4230587181",
        "password": "BY_PARAHEX-XO7BN2SCA-REDZED"
    },
    {
        "uid": "4230587270",
        "password": "BY_PARAHEX-QUHBAOI9U-REDZED"
    },
    {
        "uid": "4230587358",
        "password": "BY_PARAHEX-RL2C57V0O-REDZED"
    },
    {
        "uid": "4230587462",
        "password": "BY_PARAHEX-GUZAZXFZR-REDZED"
    },
    {
        "uid": "4230587598",
        "password": "BY_PARAHEX-EBL7MNWHV-REDZED"
    },
    {
        "uid": "4230587727",
        "password": "BY_PARAHEX-XWAVV1N2L-REDZED"
    },
    {
        "uid": "4230587852",
        "password": "BY_PARAHEX-7EVRDUSG1-REDZED"
    },
    {
        "uid": "4230587956",
        "password": "BY_PARAHEX-R7XHNDTVE-REDZED"
    },
    {
        "uid": "4230588059",
        "password": "BY_PARAHEX-BPPPLMFI9-REDZED"
    },
    {
        "uid": "4230588172",
        "password": "BY_PARAHEX-AFDAAG2MT-REDZED"
    },
    {
        "uid": "4230588350",
        "password": "BY_PARAHEX-NQ4CUSFWP-REDZED"
    },
    {
        "uid": "4230588484",
        "password": "BY_PARAHEX-ASDV33FIL-REDZED"
    },
    {
        "uid": "4230588613",
        "password": "BY_PARAHEX-PBH6AIPUN-REDZED"
    },
    {
        "uid": "4230588715",
        "password": "BY_PARAHEX-1J7V0AUFW-REDZED"
    },
    {
        "uid": "4230588810",
        "password": "BY_PARAHEX-N2ZCIWI6K-REDZED"
    },
    {
        "uid": "4230588924",
        "password": "BY_PARAHEX-7KHKPZK0D-REDZED"
    },
    {
        "uid": "4230589066",
        "password": "BY_PARAHEX-9GCB6YFPT-REDZED"
    },
    {
        "uid": "4230589195",
        "password": "BY_PARAHEX-YAFUFSX9V-REDZED"
    },
    {
        "uid": "4230589312",
        "password": "BY_PARAHEX-DPBKMOXDA-REDZED"
    },
    {
        "uid": "4230589419",
        "password": "BY_PARAHEX-TI4UXVZRX-REDZED"
    },
    {
        "uid": "4230589531",
        "password": "BY_PARAHEX-CK3OYJOVO-REDZED"
    },
    {
        "uid": "4230589642",
        "password": "BY_PARAHEX-LCLVNLRMK-REDZED"
    },
    {
        "uid": "4230589819",
        "password": "BY_PARAHEX-H0XQAGS3A-REDZED"
    },
    {
        "uid": "4230589941",
        "password": "BY_PARAHEX-K1NH7G1JF-REDZED"
    },
    {
        "uid": "4230590041",
        "password": "BY_PARAHEX-JTRKAUZN1-REDZED"
    },
    {
        "uid": "4230590145",
        "password": "BY_PARAHEX-OZQFOFEEI-REDZED"
    },
    {
        "uid": "4230590248",
        "password": "BY_PARAHEX-KSIL5AEMM-REDZED"
    },
    {
        "uid": "4230590336",
        "password": "BY_PARAHEX-DVC8BWLRP-REDZED"
    },
    {
        "uid": "4230590432",
        "password": "BY_PARAHEX-VSXUR4CQL-REDZED"
    },
    {
        "uid": "4230590587",
        "password": "BY_PARAHEX-2R78VWMM0-REDZED"
    },
    {
        "uid": "4230590748",
        "password": "BY_PARAHEX-YPN2SLWNF-REDZED"
    },
    {
        "uid": "4230590860",
        "password": "BY_PARAHEX-C18TEIUYZ-REDZED"
    },
    {
        "uid": "4230590984",
        "password": "BY_PARAHEX-YAHDC3FAG-REDZED"
    },
    {
        "uid": "4230591126",
        "password": "BY_PARAHEX-N7GDNV9HJ-REDZED"
    },
    {
        "uid": "4230591263",
        "password": "BY_PARAHEX-GUCTHZTZK-REDZED"
    },
    {
        "uid": "4230591390",
        "password": "BY_PARAHEX-FBMYRJAGR-REDZED"
    },
    {
        "uid": "4231618127",
        "password": "BY_PARAHEX-6FC8UYVNH-REDZED"
    },
    {
        "uid": "4231618887",
        "password": "BY_PARAHEX-YWL8IRVDC-REDZED"
    },
    {
        "uid": "4231620145",
        "password": "BY_PARAHEX-82RXYSLOW-REDZED"
    },
    {
        "uid": "4231621486",
        "password": "BY_PARAHEX-WUZW69AIS-REDZED"
    },
    {
        "uid": "4231621990",
        "password": "BY_PARAHEX-HQZKFBUOT-REDZED"
    },
    {
        "uid": "4231623301",
        "password": "BY_PARAHEX-IWOLDKKOX-REDZED"
    },
    {
        "uid": "4231625287",
        "password": "BY_PARAHEX-MFWDD1ZNQ-REDZED"
    },
    {
        "uid": "4231626334",
        "password": "BY_PARAHEX-DISQTDD0M-REDZED"
    },
    {
        "uid": "4231626858",
        "password": "BY_PARAHEX-SQJMPFYLY-REDZED"
    },
    {
        "uid": "4231627333",
        "password": "BY_PARAHEX-YJMJ7QW31-REDZED"
    },
    {
        "uid": "4231629254",
        "password": "BY_PARAHEX-OYVFNUYBT-REDZED"
    },
    {
        "uid": "4231630199",
        "password": "BY_PARAHEX-WOORPCJWB-REDZED"
    },
    {
        "uid": "4231630822",
        "password": "BY_PARAHEX-GK1CQAA9O-REDZED"
    },
    {
        "uid": "4231632388",
        "password": "BY_PARAHEX-MRUOKPSBR-REDZED"
    },
    {
        "uid": "4231633369",
        "password": "BY_PARAHEX-ZPHQOUSA5-REDZED"
    },
    {
        "uid": "4231635326",
        "password": "BY_PARAHEX-OS282AN46-REDZED"
    },
    {
        "uid": "4231636212",
        "password": "BY_PARAHEX-GIZCGQZWL-REDZED"
    },
    {
        "uid": "4231636580",
        "password": "BY_PARAHEX-9UC1UNWHF-REDZED"
    },
    {
        "uid": "4231637884",
        "password": "BY_PARAHEX-PMHVXM7S3-REDZED"
    },
    {
        "uid": "4231639323",
        "password": "BY_PARAHEX-C1F0LSH2T-REDZED"
    },
    {
        "uid": "4231640075",
        "password": "BY_PARAHEX-PSR4UGVYY-REDZED"
    },
    {
        "uid": "4231640949",
        "password": "BY_PARAHEX-FDWHI6G8M-REDZED"
    },
    {
        "uid": "4231641384",
        "password": "BY_PARAHEX-8ZJ3X2B4Z-REDZED"
    },
    {
        "uid": "4231642343",
        "password": "BY_PARAHEX-KIIS2W4LX-REDZED"
    },
    {
        "uid": "4231643147",
        "password": "BY_PARAHEX-GHMLPZ73E-REDZED"
    },
    {
        "uid": "4231643877",
        "password": "BY_PARAHEX-320SOQ068-REDZED"
    },
    {
        "uid": "4231644205",
        "password": "BY_PARAHEX-LUXFZAMDQ-REDZED"
    },
    {
        "uid": "4231644964",
        "password": "BY_PARAHEX-JJWJ0HD3M-REDZED"
    },
    {
        "uid": "4231645507",
        "password": "BY_PARAHEX-JCLODA1WD-REDZED"
    },
    {
        "uid": "4231646368",
        "password": "BY_PARAHEX-DMIZ9N9GN-REDZED"
    },
    {
        "uid": "4231646711",
        "password": "BY_PARAHEX-CN49DFMNF-REDZED"
    },
    {
        "uid": "4231648117",
        "password": "BY_PARAHEX-RXEKJIFP0-REDZED"
    },
    {
        "uid": "4231648988",
        "password": "BY_PARAHEX-GBR85MEHS-REDZED"
    },
    {
        "uid": "4231649928",
        "password": "BY_PARAHEX-BHAWEWUA4-REDZED"
    },
    {
        "uid": "4231650973",
        "password": "BY_PARAHEX-TGD7CIFWN-REDZED"
    },
    {
        "uid": "4231652188",
        "password": "BY_PARAHEX-N3DLE5GCY-REDZED"
    },
    {
        "uid": "4231653052",
        "password": "BY_PARAHEX-0BIWCA2RN-REDZED"
    },
    {
        "uid": "4231654405",
        "password": "BY_PARAHEX-5UXMIXEFN-REDZED"
    },
    {
        "uid": "4231654713",
        "password": "BY_PARAHEX-E0W5BOVII-REDZED"
    },
    {
        "uid": "4231655908",
        "password": "BY_PARAHEX-Y6HLYEDG3-REDZED"
    },
    {
        "uid": "4231656432",
        "password": "BY_PARAHEX-IPKCAPBBV-REDZED"
    },
    {
        "uid": "4231657974",
        "password": "BY_PARAHEX-8YUE25QGD-REDZED"
    },
    {
        "uid": "4231658497",
        "password": "BY_PARAHEX-CIBBR0NLF-REDZED"
    },
    {
        "uid": "4231659408",
        "password": "BY_PARAHEX-SMNRIJRKA-REDZED"
    },
    {
        "uid": "4231660320",
        "password": "BY_PARAHEX-KDLCTKJMH-REDZED"
    },
    {
        "uid": "4231661826",
        "password": "BY_PARAHEX-MQNOJKTHB-REDZED"
    },
    {
        "uid": "4231663592",
        "password": "BY_PARAHEX-QPYQWK2OE-REDZED"
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



