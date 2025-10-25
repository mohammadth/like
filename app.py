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
        "uid": "4238482847",
        "password": "BY_PARAHEX-RCTN0RQ6G-REDZED"
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
