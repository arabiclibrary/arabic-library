# -*- coding: utf-8 -*-
"""
المكتبة العربية الشاملة - الإصدار المتميز 9.3
يتضمن دعم GraphQL، Redis، طلبات دفعية، WebSocket، وتوثيق OpenAPI
"""

import asyncio
import aiohttp
import sqlite3
import os
import gettext
import locale
import logging
import gzip
import io
from typing import Any, Union, List, Dict, Tuple, Callable, Optional, Awaitable, Iterable
from pathlib import Path
from functools import wraps, reduce, partial, lru_cache
import inspect
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import motor.motor_asyncio
import jwt
from cryptography.fernet import Fernet
import asyncssh
import json
import unittest
from unittest import IsolatedAsyncioTestCase
import tempfile
import click
from email.mime.text import MIMEText
import smtplib
import websockets
from aiohttp import ClientSession
import aioredis

__version__ = "9.3"

# إعداد التدويل (i18n)
locale.setlocale(locale.LC_ALL, 'ar_SA.UTF-8')
try:
    ar = gettext.translation('arabic_library', localedir='locale', languages=['ar'])
    ar.install()
    _ = ar.gettext
except FileNotFoundError:
    _ = lambda x: x

# ============ نظام الأخطاء المخصص ============
class خطأ_المكتبة(Exception):
    """الفئة الأساسية لأخطاء المكتبة"""
    def __init__(self, الرسالة: str, الخطأ_الأصلي: Exception = None, سياق: str = None):
        super().__init__(الرسالة)
        self.الخطأ_الأصلي = الخطأ_الأصلي
        self.الوقت = datetime.now()
        self.السياق = سياق or inspect.stack()[1].function

class خطأ_قاعدة_بيانات(خطأ_المكتبة):
    """خطأ متعلق بقاعدة البيانات"""
    pass

class خطأ_ملف(خطأ_المكتبة):
    """خطأ متعلق بالملفات"""
    pass

class خطأ_شبكة(خطأ_المكتبة):
    """خطأ متعلق بالشبكة"""
    pass

class خطأ_تقسيم_ملف(خطأ_ملف):
    """خطأ أثناء تقسيم الملف"""
    pass

class خطأ_تشفير(خطأ_المكتبة):
    """خطأ متعلق بالتشفير"""
    pass

class خطأ_websocket(خطأ_شبكة):
    """خطأ متعلق باتصال WebSocket"""
    pass

class خطأ_redis(خطأ_المكتبة):
    """خطأ متعلق بـ Redis"""
    pass

# ============ نظام تسجيل الأخطاء المتقدم ============
class مسجل_الأخطاء:
    """فئة متقدمة لتسجيل الأخطاء مع دعم مستويات متعددة وتنبيهات"""
    
    def __init__(self, مسار_السجل: str = "سجل_الأخطاء.log", مستوى_السجل: str = "ERROR", 
                 طباعة_للمستخدم: bool = False, إرسال_تنبيهات: Dict = None):
        self.مسار_السجل = Path(مسار_السجل)
        self.مستوى_السجل = getattr(logging, مستوى_السجل.upper(), logging.ERROR)
        self.طباعة_للمستخدم = طباعة_للمستخدم
        self.إرسال_تنبيهات = إرسال_تنبيهات or {}
        self._إعداد_التسجيل()
    
    def _إعداد_التسجيل(self):
        """تهيئة نظام التسجيل"""
        تنسيق = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
        معالج_ملف = logging.FileHandler(self.مسار_السجل, encoding='utf-8')
        معالج_ملف.setFormatter(تنسيق)
        
        self.المسجل = logging.getLogger('المكتبة_العربية')
        self.المسجل.setLevel(self.مستوى_السجل)
        self.المسجل.addHandler(معالج_ملف)
    
    def تسجيل(self, مستوى: str, رسالة: str, سياق: str = None, خطأ: Exception = None):
        """تسجيل رسالة مع مستوى معين"""
        رسالة_كاملة = رسالة
        if سياق:
            رسالة_كاملة += f" | السياق: {سياق}"
        if خطأ:
            رسالة_كاملة += f" | الخطأ: {type(خطأ).__name__}: {str(خطأ)}"
        
        getattr(self.المسجل, مستوى.lower())(رسالة_كاملة, exc_info=خطأ)
        
        if self.طباعة_للمستخدم:
            print(f"{مستوى}: {رسالة_كاملة}")
        
        if self.إرسال_تنبيهات and مستوى in ["ERROR", "CRITICAL"]:
            self._إرسال_تنبيه(رسالة_كاملة)
    
    def _إرسال_تنبيه(self, رسالة: str):
        """إرسال تنبيه عبر البريد الإلكتروني"""
        if "email" in self.إرسال_تنبيهات:
            إعدادات = self.إرسال_تنبيهات["email"]
            msg = MIMEText(رسالة, 'plain', 'utf-8')
            msg['Subject'] = 'تنبيه خطأ من المكتبة العربية'
            msg['From'] = إعدادات.get("from", "no-reply@library.com")
            msg['To'] = إعدادات["to"]
            
            try:
                with smtplib.SMTP(إعدادات["smtp_server"], إعدادات.get("port", 587)) as خادم:
                    خادم.starttls()
                    خادم.login(إعدادات["user"], إعدادات["password"])
                    خادم.send_message(msg)
            except Exception as e:
                self.المسجل.error(f"فشل إرسال التنبيه: {str(e)}")
    
    def تسجيل_الخطأ(self, خطأ: Exception, سياق: str = None):
        """تسجيل خطأ"""
        self.تسجيل("ERROR", f"{type(خطأ).__name__}: {str(خطأ)}", سياق, خطأ)
    
    def تسجيل_تحذير(self, رسالة: str, سياق: str = None):
        """تسجيل تحذير"""
        self.تسجيل("WARNING", رسالة, سياق)
    
    def تسجيل_معلومات(self, رسالة: str, سياق: str = None):
        """تسجيل معلومات"""
        self.تسجيل("INFO", رسالة, سياق)

مسجل = مسجل_الأخطاء(طباعة_للمستخدم=True)

# ============ نظام التشفير ============
class مدير_التشفير:
    """فئة لتشفير وفك تشفير البيانات"""
    
    def __init__(self):
        self.مفتاح = Fernet.generate_key()
        self.مشفر = Fernet(self.مفتاح)
    
    def تشفير(self, بيانات: Union[str, bytes]) -> bytes:
        """تشفير البيانات"""
        if isinstance(بيانات, str):
            بيانات = بيانات.encode('utf-8')
        try:
            return self.مشفر.encrypt(بيانات)
        except Exception as e:
            raise خطأ_تشفير(f"فشل التشفير: {str(e)}", e)
    
    def فك_تشفير(self, بيانات_مشفرة: bytes) -> str:
        """فك تشفير البيانات"""
        try:
            return self.مشفر.decrypt(بيانات_مشفرة).decode('utf-8')
        except Exception as e:
            raise خطأ_تشفير(f"فشل فك التشفير: {str(e)}", e)

# ============ دعم قواعد البيانات الموسع ============
class قاعدة_بيانات_متقدمة:
    """فئة متقدمة للتعامل مع قواعد البيانات المتعددة"""
    
    def __init__(self, رابط_الاتصال: str, نوع_قاعدة: str = "sql"):
        self.نوع_قاعدة = نوع_قاعدة
        try:
            if نوع_قاعدة == "sql":
                self.المحرك = create_async_engine(رابط_الاتصال)
                self.جلسة = None
            elif نوع_قاعدة == "nosql":
                self.عميل = motor.motor_asyncio.AsyncIOMotorClient(رابط_الاتصال)
                self.قاعدة = self.عميل.get_database(رابط_الاتصال.split("/")[-1])
            else:
                raise خطأ_قاعدة_بيانات("نوع قاعدة بيانات غير مدعوم")
        except Exception as e:
            raise خطأ_قاعدة_بيانات(f"تعذر الاتصال بقاعدة البيانات: {str(e)}", e)
    
    async def __aenter__(self):
        if self.نوع_قاعدة == "sql":
            self.جلسة = AsyncSession(self.المحرك)
            return self
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.نوع_قاعدة == "sql" and self.جلسة:
            if exc_type is None:
                await self.جلسة.commit()
            else:
                await self.جلسة.rollback()
            await self.جلسة.close()
        elif self.نوع_قاعدة == "nosql":
            self.عميل.close()
    
    async def تنفيذ(self, استعلام: str, معاملات: Dict = None):
        if self.نوع_قاعدة != "sql":
            raise خطأ_قاعدة_بيانات("التنفيذ متاح فقط لقواعد SQL")
        try:
            if not self.جلسة:
                raise خطأ_قاعدة_بيانات("الجلسة غير نشطة")
            نتيجة = await self.جلسة.execute(sa.text(استعلام), معاملات or {})
            return نتيجة
        except Exception as e:
            raise خطأ_قاعدة_بيانات(f"خطأ في تنفيذ الاستعلام: {str(e)}", e)
    
    async def جلب_الكل(self, استعلام: str, معاملات: Dict = None) -> List[Dict]:
        نتيجة = await self.تنفيذ(استعلام, معاملات)
        return [dict(صف._mapping) for صف in نتيجة.fetchall()]
    
    async def جلب_واحد(self, استعلام: str, معاملات: Dict = None) -> Dict:
        نتيجة = await self.تنفيذ(استعلام, معاملات)
        صف = نتيجة.fetchone()
        return dict(صف._mapping) if صف else None
    
    async def إدراج_nosql(self, مجموعة: str, بيانات: Dict):
        if self.نوع_قاعدة != "nosql":
            raise خطأ_قاعدة_بيانات("الإدراج متاح فقط لقواعد NoSQL")
        try:
            نتيجة = await self.قاعدة[مجموعة].insert_one(بيانات)
            return نتيجة.inserted_id
        except Exception as e:
            raise خطأ_قاعدة_بيانات(f"خطأ في إدراج البيانات: {str(e)}", e)
    
    async def جلب_nosql(self, مجموعة: str, استعلام: Dict) -> List[Dict]:
        if self.نوع_قاعدة != "nosql":
            raise خطأ_قاعدة_بيانات("الجلب متاح فقط لقواعد NoSQL")
        try:
            المؤشر = self.قاعدة[مجموعة].find(استعلام)
            return [د async for د in المؤشر]
        except Exception as e:
            raise خطأ_قاعدة_بيانات(f"خطأ في جلب البيانات: {str(e)}", e)

# ============ إدارة Redis ============
class مدير_redis:
    """فئة للتعامل مع قاعدة بيانات Redis غير المتزامنة"""
    
    def __init__(self, رابط_الاتصال: str = "redis://localhost:6379"):
        self.رابط_الاتصال = رابط_الاتصال
        self.اتصال = None
    
    async def __aenter__(self):
        try:
            self.اتصال = await aioredis.create_redis_pool(self.رابط_الاتصال)
            return self
        except Exception as e:
            raise خطأ_redis(f"تعذر الاتصال بـ Redis: {str(e)}", e)
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.اتصال:
            self.اتصال.close()
            await self.اتصال.wait_closed()
    
    async def حفظ(self, مفتاح: str, قيمة: Union[str, Dict], مدة_الصلاحية: int = None):
        """حفظ قيمة في Redis"""
        try:
            if isinstance(قيمة, Dict):
                قيمة = json.dumps(قيمة, ensure_ascii=False)
            await self.اتصال.set(mفتاح, قيمة, expire=مدة_الصلاحية)
        except Exception as e:
            raise خطأ_redis(f"فشل الحفظ في Redis: {str(e)}", e)
    
    async def جلب(self, مفتاح: str, كائن: bool = False) -> Union[str, Dict, None]:
        """جلب قيمة من Redis"""
        try:
            قيمة = await self.اتصال.get(mفتاح, encoding='utf-8')
            if قيمة and كائن:
                return json.loads(قيمة)
            return قيمة
        except Exception as e:
            raise خطأ_redis(f"فشل الجلب من Redis: {str(e)}", e)

# ============ إدارة الملفات المتقدمة ============
class مدير_الملفات:
    """فئة متقدمة للتعامل مع الملفات مع دعم SFTP والتحميل التدريجي"""
    
    @staticmethod
    async def تقسيم_ملف(مسار_الإدخال: Union[str, Path], حجم_القطعة: int = 1024*1024) -> List[Path]:
        مسار_الإدخال = Path(مسار_الإدخال)
        if not مسار_الإدخال.exists():
            raise خطأ_تقسيم_ملف(f"الملف غير موجود: {مسار_الإدخال}")
        
        مسارات_الأجزاء = []
        رقم_الجزء = 1
        
        async def _تقسيم():
            nonlocal رقم_الجزء
            with مسار_الإدخال.open('rb') as ملف:
                while True:
                    قطعة = ملف.read(حجم_القطعة)
                    if not قطعة:
                        break
                    مسار_الجزء = مسار_الإدخال.with_name(f"{مسار_الإدخال.stem}.جزء{رقم_الجزء}{مسار_الإدخال.suffix}")
                    with مسار_الجزء.open('wb') as جزء:
                        جزء.write(قطعة)
                    مسارات_الأجزاء.append(مسار_الجزء)
                    رقم_الجزء += 1
        
        await asyncio.get_event_loop().run_in_executor(None, _تقسيم)
        return مسارات_الأجزاء
    
    @staticmethod
    async def ضغط_ملف(مسار_الإدخال: Union[str, Path], مسار_الإخراج: Union[str, Path] = None) -> Path:
        مسار_الإدخال = Path(مسار_الإدخال)
        if not مسار_الإدخال.exists():
            raise خطأ_ملف(f"الملف غير موجود: {مسار_الإدخال}")
        
        مسار_الإخراج = مسار_الإخراج or مسار_الإدخال.with_suffix(مسار_الإدخال.suffix + '.gz')
        
        async def _ضغط():
            with مسار_الإدخال.open('rb') as ملف_إدخال, gzip.open(مسار_الإخراج, 'wb') as ملف_إخراج:
                while True:
                    قطعة = ملف_إدخال.read(8192)
                    if not قطعة:
                        break
                    ملف_إخراج.write(قطعة)
        
        await asyncio.get_event_loop().run_in_executor(None, _ضغط)
        return مسار_الإخراج
    
    @staticmethod
    async def فك_ضغط_ملف(مسار_الإدخال: Union[str, Path], مسار_الإخراج: Union[str, Path] = None) -> Path:
        مسار_الإدخال = Path(مسار_الإدخال)
        if not مسار_الإدخال.exists():
            raise خطأ_ملف(f"الملف غير موجود: {مسار_الإدخال}")
        
        مسار_الإخراج = مسار_الإخراج or مسار_الإدخال.with_suffix('').with_suffix(مسار_الإدخال.stem)
        
        async def _فك_ضغط():
            with gzip.open(مسار_الإدخال, 'rb') as ملف_إدخال, مسار_الإخراج.open('wb') as ملف_إخراج:
                while True:
                    قطعة = ملف_إدخال.read(8192)
                    if not قطعة:
                        break
                    ملف_إخراج.write(قطعة)
        
        await asyncio.get_event_loop().run_in_executor(None, _فك_ضغط)
        return مسار_الإخراج
    
    @staticmethod
    async def إحصائيات_ملف(مسار: Union[str, Path]) -> Dict:
        مسار = Path(مسار)
        if not مسار.exists():
            raise خطأ_ملف(f"الملف غير موجود: {مسار}")
        return {
            "حجم": مسار.stat().st_size,
            "تاريخ_التعديل": datetime.fromtimestamp(مسار.stat().st_mtime),
            "امتداد": مسار.suffix,
            "قابل_للقراءة": مسار.is_file() and os.access(مسار, os.R_OK)
        }
    
    @staticmethod
    async def تحميل_sftp(مضيف: str, اسم_مستخدم: str, كلمة_مرور: str, 
                        مسار_بعيد: str, مسار_محلي: Union[str, Path]) -> None:
        try:
            async with asyncssh.connect(مضيف, username=اسم_مستخدم, password=كلمة_مرور) as اتصال:
                async with اتصال.start_sftp_client() as sftp:
                    await sftp.get(مسار_بعيد, مسار_محلي)
        except Exception as e:
            raise خطأ_شبكة(f"فشل تحميل الملف عبر SFTP: {str(e)}", e)

# ============ مولد توثيق OpenAPI ============
class مولد_openapi:
    """فئة لإنشاء مواصفات OpenAPI تلقائيًا"""
    
    @staticmethod
    def إنشاء_مواصفات(نقاط_نهائية: List[Dict], معلومات: Dict = None) -> Dict:
        معلومات = معلومات or {
            "title": "المكتبة العربية الشاملة API",
            "version": __version__,
            "description": "واجهة برمجة تطبيقات للمكتبة العربية"
        }
        
        مواصفات = {
            "openapi": "3.0.3",
            "info": معلومات,
            "paths": {}
        }
        
        for نقطة in نقاط_نهائية:
            مسار = نقطة["مسار"]
            طريقة = نقطة["طريقة"].lower()
            مواصفات["paths"].setdefault(مسار, {})
            مواصفات["paths"][مسار][طريقة] = {
                "summary": نقطة.get("ملخص", "لا يوجد ملخص"),
                "description": نقطة.get("وصف", ""),
                "responses": نقطة.get("استجابات", {
                    "200": {"description": "نجاح"},
                    "400": {"description": "طلب غير صالح"},
                    "500": {"description": "خطأ داخلي"}
                }),
                "parameters": نقطة.get("معاملات", []),
                "requestBody": نقطة.get("جسم_الطلب", None)
            }
        
        return مواصفات
    
    @staticmethod
    def حفظ_مواصفات(مواصفات: Dict, مسار_الإخراج: Union[str, Path] = "openapi.json"):
        with Path(مسار_الإخراج).open('w', encoding='utf-8') as ملف:
            json.dump(مواصفات, ملف, ensure_ascii=False, indent=2)

# ============ الفئة الرئيسية المتميزة ============
class البرمجة:
    """الفئة الرئيسية مع دعم GraphQL، Redis، طلبات دفعية، WebSocket، وOpenAPI"""
    
    @staticmethod
    def إنشاء_رمز_jwt(بيانات: Dict, مفتاح_سري: str, مدة_الصلاحية: int = 3600) -> str:
        بيانات["exp"] = datetime.utcnow().timestamp() + مدة_الصلاحية
        try:
            return jwt.encode(بيانات, مفتاح_سري, algorithm="HS256")
        except Exception as e:
            raise خطأ_تشفير(f"فشل إنشاء رمز JWT: {str(e)}", e)
    
    @staticmethod
    def التحقق_من_رمز_jwt(رمز: str, مفتاح_سري: str) -> Dict:
        try:
            return jwt.decode(رمز, مفتاح_سري, algorithms=["HS256"])
        except Exception as e:
            raise خطأ_تشفير(f"رمز JWT غير صالح: {str(e)}", e)
    
    @staticmethod
    @lru_cache(maxsize=100)
    async def طلب_شبكة(
        طريقة: str,
        رابط: str,
        بيانات: Dict = None,
        رؤوس: Dict = None,
        وقت_اتصال: int = 10,
        وقت_قراءة: int = 30,
        عدد_إعادة_المحاولة: int = 3,
        ذاكرة_مؤقتة: Dict = None
    ) -> Dict:
        async with مدير_redis() as redis:
            مفتاح_التخزين = f"cache:{طريقة}:{رابط}"
            نتيجة_مخزنة = await redis.جلب(mفتاح_التخزين, كائن=True)
            if نتيجة_مخزنة:
                مسجل.تسجيل_معلومات(f"استخدام بيانات مخزنة من Redis لـ {رابط}", "طلب_شبكة")
                return نتيجة_مخزنة
        
        آخر_خطأ = None
        for محاولة in range(1, عدد_إعادة_المحاولة + 1):
            try:
                async with aiohttp.ClientSession(
                    headers=رؤوس,
                    timeout=aiohttp.ClientTimeout(connect=وقت_اتصال, total=وقت_قراءة)
                ) as جلسة:
                    async with getattr(جلسة, طريقة.lower())(رابط, json=بيانات) as رد:
                        if رد.status != 200:
                            خطأ = await رد.text()
                            raise خطأ_شبكة(f"{رد.status}: {خطأ}")
                        نتيجة = await رد.json()
                        async with مدير_redis() as redis:
                            await redis.حفظ(mفتاح_التخزين, نتيجة, مدة_الصلاحية=3600)
                        return نتيجة
            except aiohttp.ClientError as e:
                آخر_خطأ = e
                if محاولة < عدد_إعادة_المحاولة:
                    await asyncio.sleep(1 * محاولة)
                continue
            except json.JSONDecodeError as e:
                raise خطأ_شبكة("تعذر تحليل الاستجابة كـ JSON", e)
        
        if ذاكرة_مؤقتة:
            مسجل.تسجيل_تحذير("استخدام بيانات مؤقتة بسبب فشل الاتصال", رابط)
            return ذاكرة_مؤقتة
        
        raise خطأ_شبكة(f"فشل بعد {عدد_إعادة_المحاولة} محاولات: {str(آخر_خطأ)}", آخر_خطأ)
    
    @staticmethod
    async def طلبات_دفعية(
        طلبات: List[Dict],
        وقت_اتصال: int = 10,
        وقت_قراءة: int = 30,
        عدد_إعادة_المحاولة: int = 3
    ) -> List[Dict]:
        نتائج = []
        async def _تنفيذ_طلب(طلب: Dict, جلسة: ClientSession) -> Dict:
            طريقة = طلب.get("طريقة", "GET")
            رابط = طلب["رابط"]
            بيانات = طلب.get("بيانات")
            رؤوس = طلب.get("رؤوس")
            ذاكرة_مؤقتة = طلب.get("ذاكرة_مؤقتة")
            
            async with مدير_redis() as redis:
                مفتاح_التخزين = f"cache:{طريقة}:{رابط}"
                نتيجة_مخزنة = await redis.جلب(mفتاح_التخزين, كائن=True)
                if نتيجة_مخزنة:
                    مسجل.تسجيل_معلومات(f"استخدام بيانات مخزنة من Redis لـ {رابط}", "طلبات_دفعية")
                    return نتيجة_مخزنة
            
            for محاولة in range(1, عدد_إعادة_المحاولة + 1):
                try:
                    async with getattr(جلسة, طريقة.lower())(رابط, json=بيانات, headers=رؤوس) as رد:
                        if رد.status != 200:
                            خطأ = await رد.text()
                            raise خطأ_شبكة(f"{رد.status}: {خطأ}")
                        نتيجة = await رد.json()
                        async with مدير_redis() as redis:
                            await redis.حفظ(mفتاح_التخزين, نتيجة, مدة_الصلاحية=3600)
                        return نتيجة
                except aiohttp.ClientError as e:
                    if محاولة < عدد_إعادة_المحاولة:
                        await asyncio.sleep(1 * محاولة)
                    else:
                        if ذاكرة_مؤقتة:
                            مسجل.تسجيل_تحذير(f"استخدام بيانات مؤقتة لـ {رابط}", "طلبات_دفعية")
                            return ذاكرة_مؤقتة
                        raise خطأ_شبكة(f"فشل الطلب {رابط} بعد {عدد_إعادة_المحاولة} محاولات", e)
                except json.JSONDecodeError as e:
                    raise خطأ_شبكة("تعذر تحليل الاستجابة كـ JSON", e)
        
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(connect=وقت_اتصال, total=وقت_قراءة)
        ) as جلسة:
            مهام = [asyncio.create_task(_تنفيذ_طلب(طلب, جلسة)) for طلب in طلبات]
            نتائج = await asyncio.gather(*مهام, return_exceptions=True)
        
        for نتيجة in نتائج:
            if isinstance(نتيجة, Exception):
                مسجل.تسجيل_الخطأ(نتيجة, "طلبات_دفعية")
        
        return نتائج
    
    @staticmethod
    async def اتصال_websocket(
        رابط: str,
        معالج_الرسائل: Callable[[str], Awaitable[None]],
        رؤوس: Dict = None,
        عدد_إعادة_المحاولة: int = 3,
        تأخير_إعادة_الاتصال: int = 5
    ) -> None:
        for محاولة in range(1, عدد_إعادة_المحاولة + 1):
            try:
                async with websockets.connect(رابط, extra_headers=رؤوس) as websocket:
                    مسجل.تسجيل_معلومات(f"تم الاتصال بـ WebSocket: {رابط}", "اتصال_websocket")
                    while True:
                        try:
                            رسالة = await websocket.recv()
                            await معالج_الرسائل(رسالة)
                        except websockets.ConnectionClosed:
                            مسجل.تسجيل_تحذير(f"انقطع اتصال WebSocket: {رابط}", "اتصال_websocket")
                            break
            except Exception as e:
                مسجل.تسجيل_الخطأ(e, f"فشل الاتصال بـ WebSocket، المحاولة {محاولة}")
                if محاولة < عدد_إعادة_المحاولة:
                    await asyncio.sleep(تأخير_إعادة_الاتصال)
                else:
                    raise خطأ_websocket(f"فشل الاتصال بـ WebSocket بعد {عدد_إعادة_المحاولة} محاولات", e)
    
    @staticmethod
    async def استعلام_graphql(
        رابط: str,
        استعلام: str,
        متغيرات: Dict = None,
        رؤوس: Dict = None,
        وقت_اتصال: int = 10,
        وقت_قراءة: int = 30,
        عدد_إعادة_المحاولة: int = 3
    ) -> Dict:
        """إرسال استعلام GraphQL"""
        بيانات = {"query": استعلام}
        if متغيرات:
            بيانات["variables"] = متغيرات
        
        async with مدير_redis() as redis:
            مفتاح_التخزين = f"cache:graphql:{رابط}:{hash(استعلام)}"
            نتيجة_مخزنة = await redis.جلب(mفتاح_التخزين, كائن=True)
            if نتيجة_مخزنة:
                مسجل.تسجيل_معلومات(f"استخدام بيانات مخزنة من Redis لـ GraphQL {رابط}", "استعلام_graphql")
                return نتيجة_مخزنة
        
        for محاولة in range(1, عدد_إعادة_المحاولة + 1):
            try:
                async with aiohttp.ClientSession(
                    headers=رؤوس,
                    timeout=aiohttp.ClientTimeout(connect=وقت_اتصال, total=وقت_قراءة)
                ) as جلسة:
                    async with جلسة.post(رابط, json=بيانات) as رد:
                        if رد.status != 200:
                            خطأ = await رد.text()
                            raise خطأ_شبكة(f"{رد.status}: {خطأ}")
                        نتيجة = await رد.json()
                        if "errors" in نتيجة:
                            raise خطأ_شبكة(f"خطأ GraphQL: {نتيجة['errors']}")
                        async with مدير_redis() as redis:
                            await redis.حفظ(mفتاح_التخزين, نتيجة, مدة_الصلاحية=3600)
                        return نتيجة
            except aiohttp.ClientError as e:
                if محاولة < عدد_إعادة_المحاولة:
                    await asyncio.sleep(1 * محاولة)
                else:
                    raise خطأ_شبكة(f"فشل استعلام GraphQL بعد {عدد_إعادة_المحاولة} محاولات", e)
            except json.JSONDecodeError as e:
                raise خطأ_شبكة("تعذر تحليل استجابة GraphQL كـ JSON", e)

# ============ واجهة سطر الأوامر (CLI) ============
@click.group()
def مكتبة():
    """واجهة سطر أوامر للمكتبة العربية الشاملة"""
    pass

@مكتبة.command()
@click.argument('مسار_ملف')
@click.option('--حجم_القطعة', default=1024*1024, help='حجم القطعة بالبايت')
def تقسيم_ملف(مسار_ملف: str, حجم_القطعة: int):
    async def _تقسيم():
        أجزاء = await مدير_الملفات.تقسيم_ملف(مسار_ملف, حجم_القطعة)
        click.echo(f"تم تقسيم الملف إلى: {أجزاء}")
    asyncio.run(_تقسيم())

@مكتبة.command()
@click.argument('رابط_الاتصال')
@click.argument('استعلام')
def تنفيذ_استعلام(رابط_الاتصال: str, استعلام: str):
    async def _تنفيذ():
        async with قاعدة_بيانات_متقدمة(رابط_الاتصال) as قاعدة:
            نتيجة = await قاعدة.جلب_الكل(استعلام)
            click.echo(json.dumps(نتيجة, ensure_ascii=False, indent=2))
    asyncio.run(_تنفيذ())

@مكتبة.command()
@click.argument('مسار_الإخراج', default="openapi.json")
def إنشاء_openapi(مسار_الإخراج: str):
    نقاط_نهائية = [
        {
            "مسار": "/data",
            "طريقة": "GET",
            "ملخص": "جلب البيانات",
            "وصف": "استرجاع البيانات من الخادم",
            "استجابات": {
                "200": {"description": "تم استرجاع البيانات بنجاح"},
                "404": {"description": "الموارد غير موجودة"}
            }
        },
        {
            "مسار": "/data",
            "طريقة": "POST",
            "ملخص": "إنشاء بيانات",
            "وصف": "إضافة بيانات جديدة إلى الخادم",
            "جسم_الطلب": {
                "content": {
                    "application/json": {
                        "schema": {"type": "object", "properties": {"key": {"type": "string"}}}
                    }
                }
            }
        },
        {
            "مسار": "/graphql",
            "طريقة": "POST",
            "ملخص": "استعلام GraphQL",
            "وصف": "إرسال استعلامات أو تحويلات GraphQL",
            "جسم_الطلب": {
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string"},
                                "variables": {"type": "object"}
                            }
                        }
                    }
                }
            }
        }
    ]
    مواصفات = مولد_openapi.إنشاء_مواصفات(نقاط_نهائية)
    مولد_openapi.حفظ_مواصفات(مواصفات, مسار_الإخراج)
    click.echo(f"تم إنشاء مواصفات OpenAPI في: {مسار_الإخراج}")

# ============ اختبارات الوحدات والتكامل ============
class اختبار_قاعدة_بيانات_المتقدمة(IsolatedAsyncioTestCase):
    async def test_الاتصال_والتنفيذ_sql(self):
        async with قاعدة_بيانات_متقدمة("sqlite+aiosqlite:///:memory:") as قاعدة:
            await قاعدة.تنفيذ("CREATE TABLE test (id INTEGER, name TEXT)")
            await قاعدة.تنفيذ("INSERT INTO test VALUES (:id, :name)", {"id": 1, "name": "اختبار"})
            نتيجة = await قاعدة.جلب_واحد("SELECT * FROM test")
            self.assertEqual(نتيجة["id"], 1)
            self.assertEqual(نتيجة["name"], "اختبار")
    
    async def test_إدراج_وجلب_nosql(self):
        async with قاعدة_بيانات_متقدمة("mongodb://localhost:27017/test", "nosql") as قاعدة:
            معرف = await قاعدة.إدراج_nosql("test_collection", {"name": "اختبار"})
            نتيجة = await قاعدة.جلب_nosql("test_collection", {"_id": معرف})
            self.assertEqual(نتيجة[0]["name"], "اختبار")

class اختبار_مدير_الملفات(IsolatedAsyncioTestCase):
    async def test_ضغط_وفك_ضغط(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write("محتوى اختبار".encode('utf-8'))
            tmp_path = tmp.name
        
        try:
            مسار_مضغوط = await مدير_الملفات.ضغط_ملف(tmp_path)
            self.assertTrue(Path(مسار_مضغوط).exists())
            مسار_مفكوك = await مدير_الملفات.فك_ضغط_ملف(مسار_مضغوط)
            self.assertTrue(Path(مسار_مفكوك).exists())
            self.assertEqual(Path(مسار_مفكوك).read_text(encoding='utf-8'), "محتوى اختبار")
        finally:
            for path in [tmp_path, مسار_مضغوط, مسار_مفكوك]:
                if path and Path(path).exists():
                    Path(path).unlink()
    
    async def test_إحصائيات_ملف(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write("محتوى".encode('utf-8'))
            tmp_path = tmp.name
        try:
            إحصائيات = await مدير_الملفات.إحصائيات_ملف(tmp_path)
            self.assertEqual(إحصائيات["حجم"], 6)
            self.assertTrue(إحصائيات["قابل_للقراءة"])
        finally:
            Path(tmp_path).unlink()

class اختبار_البرمجة(IsolatedAsyncioTestCase):
    async def test_طلبات_دفعية(self):
        طلبات = [
            {"طريقة": "GET", "رابط": "https://api.example.com/data1", "ذاكرة_مؤقتة": {"data": "مؤقت1"}},
            {"طريقة": "POST", "رابط": "https://api.example.com/data2", "بيانات": {"key": "value"}, "ذاكرة_مؤقتة": {"data": "مؤقت2"}}
        ]
        نتائج = await البرمجة.طلبات_دفعية(طلبات)
        self.assertEqual(len(نتائج), 2)
    
    async def test_اتصال_websocket(self):
        async def معالج_الرسائل(رسالة: str):
            print(f"استلمت: {رسالة}")
        
        try:
            await البرمجة.اتصال_websocket("ws://echo.websocket.org", معالج_الرسائل)
        except خطأ_websocket:
            pass
    
    async def test_استعلام_graphql(self):
        استعلام = """
        query {
            user(id: 1) {
                name
            }
        }
        """
        try:
            نتيجة = await البرمجة.استعلام_graphql("https://api.example.com/graphql", استعلام)
            self.assertIsInstance(نتيجة, dict)
        except خطأ_شبكة:
            pass

class اختبار_مدير_redis(IsolatedAsyncioTestCase):
    async def test_حفظ_وجلب(self):
        async with مدير_redis() as redis:
            await redis.حفظ("مفتاح_اختبار", {"قيمة": "اختبار"}, مدة_الصلاحية=60)
            نتيجة = await redis.جلب("مفتاح_اختبار", كائن=True)
            self.assertEqual(نتيجة["قيمة"], "اختبار")

if __name__ == "__main__":
    مكتبة()