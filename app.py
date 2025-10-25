from fastapi import FastAPI, HTTPException
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from flask import Flask, jsonify, request
from flask_caching import Cache
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
import os
import datetime
from datetime import timedelta
import uvicorn

# تجاهل تحذيرات SSL
warnings.filterwarnings("ignore", category=InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV = b'6oyZDr22E3ychjM%'

# تهيئة colorama
init(autoreset=True)

# ✅ إنشاء تطبيق FastAPI
fastapi_app = FastAPI(title="Free Fire Likes API", description="API for Free Fire Likes Bot")

# تهيئة تطبيق Flask (محفوظ كما هو)
app = Flask(__name__)

# تكوين Flask-Caching
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 25200})

# ✅ الحسابات مخزنة مباشرة في الكود
ACCOUNTS = [
    {
        "uid": "4238482847",
        "password": "BY_PARAHEX-RCTN0RQ6G-REDZED"
    }
]

# إعدادات تيليجرام
TELEGRAM_BOT_TOKEN = "8097054676:AAFINJ5mtnA0KCeoT8u2y2wSNLNlvuvIxcE"

# ملفات التخزين
ACCOUNTS_FILE = "accounts.json"
LIKED_IDS_FILE = "liked_ids.json"
AUTO_LIKE_IDS_FILE = "auto_like_ids.json"

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
    with app.app_context():
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
        cache.set('responses', responses)
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
        'ReleaseVersion': "OB50"  # تم تصحيح الخطأ هنا
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


# ========== الملفات الجديدة ==========

def load_json_file(filename, default=[]):
    """تحميل ملف JSON"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
    return default

def save_json_file(filename, data):
    """حفظ بيانات إلى ملف JSON"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False

def update_accounts_from_file():
    """تحديث الحسابات من الملف"""
    global ACCOUNTS
    try:
        if os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
                new_accounts = json.load(f)
                if isinstance(new_accounts, list) and len(new_accounts) > 0:
                    ACCOUNTS = new_accounts
                    print(f"✅ تم تحديث الحسابات من الملف، العدد: {len(ACCOUNTS)}")
                    return True
    except Exception as e:
        print(f"❌ خطأ في تحديث الحسابات: {e}")
    return False

def can_send_likes(uid):
    """التحقق إذا كان يمكن إرسال لايكات للـUID"""
    liked_ids = load_json_file(LIKED_IDS_FILE, {})
    
    if uid not in liked_ids:
        return True, "يمكن إرسال لايكات الآن"
    
    last_like_time = datetime.datetime.fromisoformat(liked_ids[uid])
    next_like_time = last_like_time + timedelta(hours=24)
    now = datetime.datetime.now()
    
    if now >= next_like_time:
        return True, "يمكن إرسال لايكات الآن"
    else:
        remaining = next_like_time - now
        hours = int(remaining.total_seconds() // 3600)
        minutes = int((remaining.total_seconds() % 3600) // 60)
        return False, f"⏳ يجب الانتظار {hours} ساعة و {minutes} دقيقة"

def record_like_sent(uid):
    """تسجيل وقت إرسال اللايكات"""
    liked_ids = load_json_file(LIKED_IDS_FILE, {})
    liked_ids[uid] = datetime.datetime.now().isoformat()
    save_json_file(LIKED_IDS_FILE, liked_ids)

def add_auto_like_id(uid):
    """إضافة ID لللايكات التلقائية"""
    auto_like_ids = load_json_file(AUTO_LIKE_IDS_FILE, [])
    if uid not in auto_like_ids:
        auto_like_ids.append(uid)
        save_json_file(AUTO_LIKE_IDS_FILE, auto_like_ids)
        return True
    return False

def remove_auto_like_id(uid):
    """إزالة ID من اللايكات التلقائية"""
    auto_like_ids = load_json_file(AUTO_LIKE_IDS_FILE, [])
    if uid in auto_like_ids:
        auto_like_ids.remove(uid)
        save_json_file(AUTO_LIKE_IDS_FILE, auto_like_ids)
        return True
    return False

def send_auto_likes():
    """إرسال اللايكات التلقائية"""
    auto_like_ids = load_json_file(AUTO_LIKE_IDS_FILE, [])
    if not auto_like_ids:
        return
    
    tokens = cache.get('responses') or []
    if not tokens:
        print("❌ لا توجد توكنات متاحة لللايكات التلقائية")
        return
    
    print(f"🔄 إرسال لايكات تلقائية لـ {len(auto_like_ids)} ID")
    
    for uid in auto_like_ids:
        try:
            can_send, message = can_send_likes(uid)
            if can_send:
                print(f"✅ إرسال لايكات تلقائية لـ {uid}")
                responses = asyncio.run(send_likes(uid, tokens))
                success_count = sum(1 for r in responses if r.get("success"))
                record_like_sent(uid)
                print(f"✅ تم إرسال {success_count} لايك لـ {uid}")
            else:
                print(f"⏳ لم يحن وقت الإرسال لـ {uid}: {message}")
        except Exception as e:
            print(f"❌ خطأ في الإرسال التلقائي لـ {uid}: {e}")

# ========== وظائف تيليجرام ==========

async def start(update: Update, context: CallbackContext) -> None:
    """إرسال رسالة ترحيبية عند استخدام الأمر /start"""
    welcome_text = """
🎮 **مرحباً بك في بوت Free Fire Likes!**

📋 **الأوامر المتاحة:**
/start - عرض هذه الرسالة
/like <UID> - إرسال لايكات للاعب
/lik <UID> - إرسال لايكات (تخطي وقت الانتظار)
/like24 <UID> - إضافة ID لللايكات التلقائية كل 24 ساعة
/upload - رفع ملف حسابات جديد
/tokens - عرض عدد التوكنات المخزنة
/refresh - تحديث التوكنات
/status - حالة البوت
/mylikes - عرض الـ IDs المضافة لللايكات التلقائية
/remove <UID> - إزالة ID من اللايكات التلقائية

⚡ **مثال:** 
`/like 1234567890`
`/like24 10405791946`
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def like_command(update: Update, context: CallbackContext) -> None:
    """معالجة أمر الإعجاب مع التحقق من الوقت"""
    if not context.args:
        await update.message.reply_text("❌ يرجى تقديم UID\nمثال: `/like 1234567890`", parse_mode='Markdown')
        return

    uid = context.args[0]
    
    # التحقق من صحة UID
    if not uid.isdigit():
        await update.message.reply_text("❌ UID غير صالح. يجب أن يحتوي على أرقام فقط.")
        return

    # التحقق من الوقت
    can_send, message = can_send_likes(uid)
    if not can_send:
        await update.message.reply_text(f"❌ {message}\n\nاستخدم `/lik {uid}` لتخطي وقت الانتظار", parse_mode='Markdown')
        return

    await update.message.reply_text(f"⏳ جاري إرسال لايكات للاعب {uid}...")

    try:
        tokens = cache.get('responses')
        if not tokens:
            await update.message.reply_text("❌ لا توجد توكنات متاحة. يرجى استخدام /refresh لتحديث التوكنات أولاً.")
            return

        enc_uid = encrypt_message_like(create_uid_proto(uid))
        before = make_like_request(enc_uid, tokens[0]["token"])
        if not before:
            await update.message.reply_text("❌ فشل في الحصول على معلومات اللاعب.")
            return

        before_data = json.loads(MessageToJson(before))
        likes_before = int(before_data.get("AccountInfo", {}).get("Likes", 0))
        nickname = before_data.get("AccountInfo", {}).get("PlayerNickname", "Unknown")
        player_level = before_data.get("AccountInfo", {}).get("Level", 0)
        region = before_data.get("AccountInfo", {}).get("region", "Unknown")

        # إرسال رسالة التقدم
        progress_msg = await update.message.reply_text(
            f"📊 **معلومات اللاعب:**\n"
            f"👤 الاسم: {nickname}\n"
            f"🆔 UID: {uid}\n"
            f"🌍 المنطقة: {region}\n"
            f"⭐ المستوى: {player_level}\n"
            f"❤️ اللايكات الحالية: {likes_before}\n"
            f"🔄 جاري إرسال {len(tokens)} لايك..."
        )

        # إرسال اللايكات
        responses = await send_likes(uid, tokens)
        success_count = sum(1 for r in responses if r.get("success"))

        # الحصول على عدد اللايكات الجديد
        after = make_like_request(enc_uid, tokens[0]["token"])
        likes_after = likes_before
        if after:
            after_data = json.loads(MessageToJson(after))
            likes_after = int(after_data.get("AccountInfo", {}).get("Likes", 0))

        actual_likes_added = likes_after - likes_before

        # تسجيل وقت الإرسال
        record_like_sent(uid)

        # إرسال النتيجة النهائية
        result_text = (
            f"✅ **تم إرسال اللايكات بنجاح!**\n\n"
            f"👤 **اللاعب:** {nickname}\n"
            f"🆔 **UID:** {uid}\n"
            f"❤️ **اللايكات قبل:** {likes_before}\n"
            f"❤️ **اللايكات بعد:** {likes_after}\n"
            f"📈 **تم إضافة:** {actual_likes_added} لايك\n"
            f"✅ **الطلبات الناجحة:** {success_count}/{len(tokens)}\n"
            f"⏰ **يمكنك الإرسال مرة أخرى بعد 24 ساعة**\n"
            f"🏆 **الحالة:** {'نجاح' if actual_likes_added > 0 else 'لا توجد تغييرات'}"
        )

        await progress_msg.edit_text(result_text)

    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")

async def lik_command(update: Update, context: CallbackContext) -> None:
    """إرسال لايكات مع تخطي وقت الانتظار"""
    if not context.args:
        await update.message.reply_text("❌ يرجى تقديم UID\nمثال: `/lik 1234567890`", parse_mode='Markdown')
        return

    uid = context.args[0]
    
    if not uid.isdigit():
        await update.message.reply_text("❌ UID غير صالح. يجب أن يحتوي على أرقام فقط.")
        return

    await update.message.reply_text(f"⚡ **تخطي وقت الانتظار**\n⏳ جاري إرسال لايكات للاعب {uid}...")

    try:
        tokens = cache.get('responses')
        if not tokens:
            await update.message.reply_text("❌ لا توجد توكنات متاحة. يرجى استخدام /refresh لتحديث التوكنات أولاً.")
            return

        enc_uid = encrypt_message_like(create_uid_proto(uid))
        before = make_like_request(enc_uid, tokens[0]["token"])
        if not before:
            await update.message.reply_text("❌ فشل في الحصول على معلومات اللاعب.")
            return

        before_data = json.loads(MessageToJson(before))
        likes_before = int(before_data.get("AccountInfo", {}).get("Likes", 0))
        nickname = before_data.get("AccountInfo", {}).get("PlayerNickname", "Unknown")
        player_level = before_data.get("AccountInfo", {}).get("Level", 0)
        region = before_data.get("AccountInfo", {}).get("region", "Unknown")

        progress_msg = await update.message.reply_text(
            f"📊 **معلومات اللاعب:**\n"
            f"👤 الاسم: {nickname}\n"
            f"🆔 UID: {uid}\n"
            f"🌍 المنطقة: {region}\n"
            f"⭐ المستوى: {player_level}\n"
            f"❤️ اللايكات الحالية: {likes_before}\n"
            f"🔄 جاري إرسال {len(tokens)} لايك..."
        )

        responses = await send_likes(uid, tokens)
        success_count = sum(1 for r in responses if r.get("success"))

        after = make_like_request(enc_uid, tokens[0]["token"])
        likes_after = likes_before
        if after:
            after_data = json.loads(MessageToJson(after))
            likes_after = int(after_data.get("AccountInfo", {}).get("Likes", 0))

        actual_likes_added = likes_after - likes_before

        # تسجيل وقت الإرسال (حتى مع التخطي)
        record_like_sent(uid)

        result_text = (
            f"✅ **تم إرسال اللايكات بنجاح!** (تخطي انتظار)\n\n"
            f"👤 **اللاعب:** {nickname}\n"
            f"🆔 **UID:** {uid}\n"
            f"❤️ **اللايكات قبل:** {likes_before}\n"
            f"❤️ **اللايكات بعد:** {likes_after}\n"
            f"📈 **تم إضافة:** {actual_likes_added} لايك\n"
            f"✅ **الطلبات الناجحة:** {success_count}/{len(tokens)}\n"
            f"🏆 **الحالة:** {'نجاح' if actual_likes_added > 0 else 'لا توجد تغييرات'}"
        )

        await progress_msg.edit_text(result_text)

    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")

async def like24_command(update: Update, context: CallbackContext) -> None:
    """إضافة ID لللايكات التلقائية كل 24 ساعة"""
    if not context.args:
        await update.message.reply_text("❌ يرجى تقديم UID\nمثال: `/like24 10405791946`", parse_mode='Markdown')
        return

    uid = context.args[0]
    
    if not uid.isdigit():
        await update.message.reply_text("❌ UID غير صالح. يجب أن يحتوي على أرقام فقط.")
        return

    if add_auto_like_id(uid):
        await update.message.reply_text(
            f"✅ **تم إضافة الـ ID لللايكات التلقائية!**\n\n"
            f"🆔 **UID:** {uid}\n"
            f"⏰ **سيتم إرسال اللايكات كل 24 ساعة تلقائياً**\n"
            f"📋 **استخدم /mylikes لمشاهدة جميع الـ IDs**\n"
            f"🗑️ **استخدم /remove {uid} لإزالة الـ ID**"
        )
    else:
        await update.message.reply_text(f"❌ الـ ID {uid} مضاف مسبقاً لللايكات التلقائية")

async def upload_command(update: Update, context: CallbackContext) -> None:
    """رفع ملف حسابات جديد"""
    await update.message.reply_text(
        "📁 **لرفع ملف حسابات جديد:**\n\n"
        "1. أرسل ملف JSON يحتوي على الحسابات\n"
        "2. يجب أن يكون بنفس التنسيق:\n"
        "```json\n"
        "[\n"
        "    {\n"
        "        \"uid\": \"4238482847\",\n"
        "        \"password\": \"BY_PARAHEX-RCTN0RQ6G-REDZED\"\n"
        "    }\n"
        "]\n"
        "```\n"
        "3. سيتم حذف الحسابات القديمة واستبدالها بالجديدة"
    )

async def handle_document(update: Update, context: CallbackContext) -> None:
    """معالجة الملفات المرسلة"""
    document = update.message.document
    
    if document.mime_type != "application/json":
        await update.message.reply_text("❌ يرجى إرسال ملف JSON فقط")
        return

    file = await context.bot.get_file(document.file_id)
    await file.download_to_drive(ACCOUNTS_FILE)
    
    if update_accounts_from_file():
        await update.message.reply_text(
            f"✅ **تم تحديث الحسابات بنجاح!**\n\n"
            f"📊 **عدد الحسابات الجديدة:** {len(ACCOUNTS)}\n"
            f"🔄 **جاري تحديث التوكنات...**"
        )
        # تحديث التوكنات تلقائياً
        fetch_tokens()
    else:
        await update.message.reply_text("❌ فشل في تحديث الحسابات. تأكد من تنسيق الملف")

async def tokens_command(update: Update, context: CallbackContext) -> None:
    """عرض عدد التوكنات المتاحة"""
    tokens = cache.get('responses') or []
    await update.message.reply_text(f"🔑 **التوكنات المخزنة:** {len(tokens)} توكن")

async def refresh_command(update: Update, context: CallbackContext) -> None:
    """تحديث التوكنات"""
    msg = await update.message.reply_text("🔄 جاري تحديث التوكنات...")
    
    try:
        def refresh_tokens_sync():
            fetch_tokens()
            return cache.get('responses') or []
        
        loop = asyncio.get_event_loop()
        tokens = await loop.run_in_executor(None, refresh_tokens_sync)
        
        await msg.edit_text(f"✅ **تم تحديث التوكنات بنجاح!**\n🔑 **عدد التوكنات:** {len(tokens)}")
    except Exception as e:
        await msg.edit_text(f"❌ **فشل في تحديث التوكنات:** {str(e)}")

async def status_command(update: Update, context: CallbackContext) -> None:
    """عرض حالة البوت"""
    tokens = cache.get('responses') or []
    auto_like_ids = load_json_file(AUTO_LIKE_IDS_FILE, [])
    liked_ids = load_json_file(LIKED_IDS_FILE, {})
    
    status_text = (
        "🤖 **حالة البوت:** ✅ يعمل\n\n"
        f"🔑 **التوكنات المخزنة:** {len(tokens)}\n"
        f"👥 **الحسابات المضمنة:** {len(ACCOUNTS)}\n"
        f"🔄 **اللايكات التلقائية:** {len(auto_like_ids)} ID\n"
        f"📊 **الـ IDs المخزنة:** {len(liked_ids)}\n"
        f"⏰ **تحديث تلقائي:** كل 7 ساعات\n"
        f"⏰ **لايكات تلقائية:** كل 24 ساعة\n\n"
        "استخدم /start لرؤية جميع الأوامر"
    )
    await update.message.reply_text(status_text)

async def mylikes_command(update: Update, context: CallbackContext) -> None:
    """عرض الـ IDs المضافة لللايكات التلقائية"""
    auto_like_ids = load_json_file(AUTO_LIKE_IDS_FILE, [])
    
    if not auto_like_ids:
        await update.message.reply_text("❌ لا توجد أي IDs مضافة لللايكات التلقائية")
        return
    
    ids_text = "📋 **قائمة الـ IDs لللايكات التلقائية:**\n\n"
    for i, uid in enumerate(auto_like_ids, 1):
        can_send, message = can_send_likes(uid)
        status = "✅ جاهز" if can_send else f"⏳ {message}"
        ids_text += f"{i}. `{uid}` - {status}\n"
    
    ids_text += f"\n🗑️ **لإزالة استخدم:** /remove [UID]"
    await update.message.reply_text(ids_text, parse_mode='Markdown')

async def remove_command(update: Update, context: CallbackContext) -> None:
    """إزالة ID من اللايكات التلقائية"""
    if not context.args:
        await update.message.reply_text("❌ يرجى تقديم UID\nمثال: `/remove 10405791946`", parse_mode='Markdown')
        return

    uid = context.args[0]
    
    if remove_auto_like_id(uid):
        await update.message.reply_text(f"✅ **تم إزالة الـ ID {uid} من اللايكات التلقائية**")
    else:
        await update.message.reply_text(f"❌ الـ ID {uid} غير موجود في قائمة اللايكات التلقائية")

# ========== FastAPI Routes ==========

@fastapi_app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}

@fastapi_app.get("/fastapi/tokens")
async def get_fastapi_tokens():
    """الحصول على التوكنات المخزنة عبر FastAPI"""
    tokens = cache.get('responses')
    if tokens is None:
        raise HTTPException(status_code=404, detail="No tokens available")
    return {"tokens": tokens, "count": len(tokens)}

@fastapi_app.get("/fastapi/like")
async def fastapi_like_handler(uid: str):
    """إرسال لايكات عبر FastAPI"""
    if not uid:
        raise HTTPException(status_code=400, detail="Missing UID parameter")
    
    try:
        print(f"Starting like process for UID: {uid} via FastAPI")

        tokens = cache.get('responses')
        if not tokens:
            raise HTTPException(status_code=401, detail="No valid tokens available")

        print(f"Using {len(tokens)} valid tokens")

        enc_uid = encrypt_message_like(create_uid_proto(uid))
        before = make_like_request(enc_uid, tokens[0]["token"])
        if not before:
            raise HTTPException(status_code=500, detail="Failed to retrieve player info")

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

        return {
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
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in fastapi_like_handler: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@fastapi_app.post("/fastapi/refresh_tokens")
async def fastapi_refresh_tokens():
    """تحديث التوكنات عبر FastAPI"""
    try:
        fetch_tokens()
        tokens = cache.get('responses') or []
        return {
            "message": "Tokens refreshed successfully",
            "total_tokens": len(tokens)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@fastapi_app.get("/fastapi/status")
async def fastapi_status():
    """عرض حالة البوت عبر FastAPI"""
    tokens = cache.get('responses') or []
    auto_like_ids = load_json_file(AUTO_LIKE_IDS_FILE, [])
    liked_ids = load_json_file(LIKED_IDS_FILE, {})
    
    return {
        "status": "online",
        "bot_status": "✅ يعمل",
        "cached_tokens": len(tokens),
        "embedded_accounts": len(ACCOUNTS),
        "auto_like_ids": len(auto_like_ids),
        "stored_ids": len(liked_ids),
        "auto_refresh": "كل 7 ساعات",
        "auto_likes": "كل 24 ساعة"
    }

# ========== وظائف Flask الأصلية (محفوظة بدون تعديل) ==========

@app.route('/token', methods=['GET'])
def get_responses():
    responses = cache.get('responses')
    if responses is None:
        print("No data available in cache.")
        return jsonify({"error": "No data available yet"})
    return jsonify({"tokens": responses})


@app.route('/like', methods=['GET'])
def like_handler():
    uid = request.args.get("uid")
    if not uid:
        return jsonify({"error": "Missing UID"}), 400

    try:
        print(f"Starting like process for UID: {uid}")

        tokens = cache.get('responses')
        if not tokens:
            return jsonify({"error": "No valid tokens available. Please refresh tokens first."}), 401

        print(f"Using {len(tokens)} valid tokens")

        enc_uid = encrypt_message_like(create_uid_proto(uid))
        before = make_like_request(enc_uid, tokens[0]["token"])
        if not before:
            return jsonify({"error": "Failed to retrieve player info"}), 500

        before_data = json.loads(MessageToJson(before))
        likes_before = int(before_data.get("AccountInfo", {}).get("Likes", 0))
        nickname = before_data.get("AccountInfo", {}).get("PlayerNickname", "Unknown")
        player_level = before_data.get("AccountInfo", {}).get("Level", 0)
        region = before_data.get("AccountInfo", {}).get("region", "Unknown")

        print(f"Before: {likes_before} likes for {nickname}")

        print("Sending likes...")
        responses = asyncio.run(send_likes(uid, tokens))
        success_count = sum(1 for r in responses if r.get("success"))

        print(f"Successfully sent {success_count} likes")

        after = make_like_request(enc_uid, tokens[0]["token"])
        likes_after = likes_before
        if after:
            after_data = json.loads(MessageToJson(after))
            likes_after = int(after_data.get("AccountInfo", {}).get("Likes", 0))

        actual_likes_added = likes_after - likes_before

        return jsonify({
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
        return jsonify({"error": str(e)}), 500


@app.route('/refresh_tokens', methods=['POST'])
def refresh_tokens():
    try:
        fetch_tokens()
        tokens = cache.get('responses') or []
        return jsonify({
            "message": "Tokens refreshed successfully",
            "total_tokens": len(tokens)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    tokens = cache.get('responses') or []
    return jsonify({
        "status": "online",
        "message": "Like API is running ✅",
        "cached_tokens": len(tokens),
        "embedded_accounts": len(ACCOUNTS),
        "endpoints": {
            "/like?uid=UID": "Send likes to player",
            "/token": "Get cached tokens",
            "/refresh_tokens": "Refresh tokens (POST)",
            "/fastapi/docs": "FastAPI Documentation"
        }
    })


def run_scheduler():
    """تشغيل السكيدولر في loop منفصل"""
    while True:
        schedule.run_pending()
        time.sleep(1)


def run_flask():
    """تشغيل تطبيق Flask في thread منفصل"""
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)


def run_fastapi():
    """تشغيل تطبيق FastAPI في thread منفصل"""
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000, log_level="info")


def run_telegram_bot():
    """تشغيل بوت تيليجرام في thread منفصل"""
    # إنشاء تطبيق تيليجرام
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # إضافة handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("like", like_command))
    application.add_handler(CommandHandler("lik", lik_command))
    application.add_handler(CommandHandler("like24", like24_command))
    application.add_handler(CommandHandler("upload", upload_command))
    application.add_handler(CommandHandler("tokens", tokens_command))
    application.add_handler(CommandHandler("refresh", refresh_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("mylikes", mylikes_command))
    application.add_handler(CommandHandler("remove", remove_command))
    
    # إضافة handler للملفات
    from telegram.ext import MessageHandler, filters
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # بدء البوت
    print("🤖 بوت تيليجرام يعمل...")
    application.run_polling()


def main():
    """الدالة الرئيسية لتشغيل كل شيء"""
    
    # تشغيل السكيدولر
    schedule.every(7).hours.do(fetch_tokens)
    schedule.every(24).hours.do(send_auto_likes)
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    # تشغيل fetch_tokens فوراً
    print("🔄 جاري تحميل التوكنات الأولية...")
    fetch_tokens()

    # تشغيل Flask في thread منفصل
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # تشغيل FastAPI في thread منفصل
    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.daemon = True
    fastapi_thread.start()

    # تشغيل Telegram Bot في thread منفصل
    telegram_thread = threading.Thread(target=run_telegram_bot)
    telegram_thread.daemon = True
    telegram_thread.start()

    print("🚀 جميع الخدمات تعمل:")
    print("   • Flask API: http://0.0.0.0:5000")
    print("   • FastAPI: http://0.0.0.0:8000")
    print("   • FastAPI Docs: http://0.0.0.0:8000/docs")
    print("   • Telegram Bot: يعمل")

    # البقاء في التشغيل
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 إيقاف البوت...")


if __name__ == "__main__":
    # تأكد من وضع توكن البوت هنا
    if TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("❌ يرجى تعيين TELEGRAM_BOT_TOKEN الصحيح في الكود")
        exit(1)
    
    # تشغيل البوت
    main()
