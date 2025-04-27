# المكتبة العربية الشاملة

**الإصدار 0.0.1** - مكتبة Python قوية ومتعددة الاستخدامات مصممة خصيصًا للمطورين الناطقين بالعربية. تهدف إلى تسهيل تطوير التطبيقات بتقديم أدوات متقدمة لإدارة قواعد البيانات، الشبكات، الملفات، التشفير، وإنشاء واجهات برمجة تطبيقات (APIs).

---

## **فكرة المكتبة**

### **الهدف**
المكتبة العربية الشاملة هي مشروع مفتوح المصدر يهدف إلى:
- **تمكين المطورين العرب**: توفير مكتبة بلغة Python تدعم اللغة العربية بشكل كامل في الأسماء (مثل الفئات والدوال) والتوثيق.
- **تبسيط المهام الشائعة**: توفير أدوات جاهزة للتعامل مع قواعد البيانات (SQL/NoSQL)، طلبات الشبكة (HTTP/GraphQL/WebSocket)، إدارة الملفات، والتشفير.
- **دعم التطوير الحديث**: تضم ميزات مثل التخزين المؤقت بـ Redis، توثيق OpenAPI، وواجهة سطر أوامر (CLI).
- **المرونة والتوسع**: تصميم معياري يسمح بإضافة ميزات جديدة بسهولة.

### **الرؤية**
- أن تكون المكتبة الأولى التي يلجأ إليها المطورون العرب لتطوير تطبيقات قوية وحديثة.
- دعم المجتمع العربي بتوثيق شامل وأمثلة عملية.
- تعزيز ثقافة البرمجة مفتوحة المصدر باللغة العربية.

### **لماذا المكتبة العربية؟**
- **واجهة عربية**: أسماء الفئات (مثل `البرمجة`، `مدير_الملفات`) والدوال (مثل `طلب_شبكة`، `استعلام_graphql`) بالعربية لتسهيل الفهم.
- **دعم شامل**: تغطي معظم احتياجات التطوير (قواعد بيانات، شبكات، ملفات، أمان).
- **اختبارات مدمجة**: تحتوي على اختبارات وحدات وتكامل لضمان الجودة.
- **توثيق OpenAPI**: لإنشاء وثائق API تلقائيًا.

---

## **مميزات المكتبة**
- **قواعد البيانات**: دعم SQLite، PostgreSQL، MySQL، MongoDB، وRedis.
- **إدارة الملفات**: تقسيم الملفات، ضغط/فك ضغط بصيغة gzip، تحميل عبر SFTP.
- **الشبكات**: طلبات HTTP دفعية، GraphQL، WebSocket، مع التخزين المؤقت بـ Redis.
- **الأمان**: تشفير البيانات (Fernet)، توثيق JWT.
- **التوثيق**: إنشاء مواصفات OpenAPI تلقائيًا.
- **واجهة CLI**: أوامر لتقسيم الملفات، تنفيذ الاستعلامات، وإنشاء OpenAPI.
- **اختبارات**: اختبارات وحدات وتكامل لضمان الأداء.

---

## **متطلبات النظام**
- **Python**: الإصدار 3.7 أو أحدث.
- **التبعيات**:
  - `aiohttp>=3.8.0`
  - `sqlalchemy>=1.4.0`
  - `aiosqlite>=0.17.0`
  - `asyncpg>=0.27.0`
  - `motor>=3.0.0`
  - `pyjwt>=2.4.0`
  - `cryptography>=38.0.0`
  - `asyncssh>=2.12.0`
  - `click>=8.1.0`
  - `websockets>=10.0`
  - `aioredis>=2.0.0`
- **اختياري** (لاختبار الأداء):
  - `locust>=2.0.0`

---

## **التثبيت**

1. **تثبيت Python**:
   تأكد من تثبيت Python 3.7+ على جهازك. يمكنك التحقق باستخدام:
   ```bash
   python --version
   ```

2. **إنشاء بيئة افتراضية** (اختياري ولكنه موصى به):
   ```bash
   python -m venv venv
   source venv/bin/activate  # على Linux/Mac
   venv\Scripts\activate     # على Windows
   ```

3. **تثبيت المكتبة**:
   إذا كنت تستخدم المكتبة من PyPI:
   ```bash
   pip install arabic-library
   ```
   أو إذا كنت تستخدم الملفات المحلية:
   ```bash
   pip install -r requirements.txt
   ```
   (ملاحظة: يمكنك إنشاء `requirements.txt` باستخدام التبعيات المذكورة في `setup.py`).

4. **التحقق من التثبيت**:
   جرب تشغيل واجهة CLI:
   ```bash
   python arabic_library.py --help
   ```

---

## **كيفية استخدام المكتبة**

المكتبة توفر واجهات سهلة الاستخدام للتعامل مع قواعد البيانات، الشبكات، الملفات، والأمان. إليك أمثلة عملية:

### **1. استعلام GraphQL**
لإرسال استعلام GraphQL إلى خادم:
```python
import asyncio
from arabic_library import البرمجة

async def مثال_graphql():
    استعلام = """
    query {
        user(id: 1) {
            name
        }
    }
    """
    نتيجة = await البرمجة.استعلام_graphql("https://api.example.com/graphql", استعلام)
    print(نتيجة)

asyncio.run(مثال_graphql())
```

### **2. استخدام Redis للتخزين المؤقت**
لحفظ واسترجاع البيانات من Redis:
```python
import asyncio
from arabic_library import مدير_redis

async def مثال_redis():
    async with مدير_redis() as redis:
        await redis.حفظ("مفتاح", {"قيمة": "بيانات"}, مدة_الصلاحية=60)
        نتيجة = await redis.جلب("مفتاح", كائن=True)
        print(نتيجة)

asyncio.run(مثال_redis())
```

### **3. طلبات دفعية HTTP**
لإرسال عدة طلبات HTTP في وقت واحد:
```python
import asyncio
from arabic_library import البرمجة

async def مثال_دفعية():
    طلبات = [
        {"طريقة": "GET", "رابط": "https://api.example.com/data1"},
        {"طريقة": "POST", "رابط": "https://api.example.com/data2", "بيانات": {"key": "value"}}
    ]
    نتائج = await البرمجة.طلبات_دفعية(طلبات)
    print(نتائج)

asyncio.run(مثال_دفعية())
```

### **4. تقسيم ملف كبير**
لتجزئة ملف إلى أجزاء أصغر:
```bash
python arabic_library.py تقسيم_ملف ملف_كبير.txt --حجم_القطعة 1048576
```

### **5. إنشاء توثيق OpenAPI**
لإنشاء مواصفات OpenAPI لـ API:
```bash
python arabic_library.py إنشاء_openapi openapi.json
```

### **6. تشغيل الاختبارات**
للتحقق من أداء المكتبة:
```bash
python -m unittest arabic_library
```

---

## **تطوير المكتبة**

المكتبة مصممة لتكون **معيارية** وسهلة التوسع. إليك دليلًا من الألف إلى الياء لتطوير المكتبة، مع أمثلة كود.

### **هيكلية المكتبة**
الملف الرئيسي (`arabic_library.py`) يحتوي على:
- **نظام الأخطاء المخصص**: فئات مثل `خطأ_المكتبة`، `خطأ_شبكة`.
- **نظام التسجيل**: فئة `مسجل_الأخطاء` لتتبع الأخطاء.
- **الفئات الرئيسية**:
  - `البرمجة`: للشبكات (HTTP، GraphQL، WebSocket) والتشفير (JWT).
  - `قاعدة_بيانات_متقدمة`: لـ SQL/NoSQL.
  - `مدير_الملفات`: لإدارة الملفات (تقسيم، ضغط، SFTP).
  - `مدير_redis`: للتخزين المؤقت.
  - `مولد_openapi`: لتوثيق API.
- **واجهة CLI**: باستخدام مكتبة `click`.
- **اختبارات**: باستخدام `unittest`.

### **خطوات التطوير**

1. **فهم الهيكلية**:
   - الكود منظم في فئات مستقلة (مثل `البرمجة`، `مدير_الملفات`).
   - كل فئة مسؤولة عن مهمة محددة (مثل الشبكات، الملفات).
   - الاختبارات موجودة في نهاية الملف (`اختبار_البرمجة`، `اختبار_مدير_الملفات`).

2. **إعداد بيئة التطوير**:
   - قم بتنزيل الملفات (`arabic_library.py`، `README.md`، `setup.py`، `locustfile.py`).
   - أنشئ بيئة افتراضية وثبّت التبعيات:
     ```bash
     python -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```
   - استخدم محرر مثل VS Code لتحرير `arabic_library.py`.

3. **إضافة دالة جديدة**:
   لنفترض أنك تريد إضافة دالة جديدة لتحليل ملفات CSV في فئة `مدير_الملفات`.

   **الخطوة 1: إضافة الدالة**
   افتح `arabic_library.py` وابحث عن فئة `مدير_الملفات`. أضف الدالة التالية:
   ```python
   @staticmethod
   async def تحليل_csv(مسار: Union[str, Path], فاصل: str = ",") -> List[Dict]:
       """تحليل ملف CSV إلى قائمة من القواميس"""
       import csv
       مسار = Path(مسار)
       if not مسار.exists():
           raise خطأ_ملف(f"الملف غير موجود: {مسار}")
       
       سجلات = []
       async def _تحليل():
           with مسار.open('r', encoding='utf-8') as ملف:
               قارئ = csv.DictReader(ملف, delimiter=فاصل)
               for صف in قارئ:
                   سجلات.append(dict(صف))
       
       await asyncio.get_event_loop().run_in_executor(None, _تحليل)
       return سجلات
   ```

   **الخطوة 2: إضافة اختبار**
   ابحث عن فئة `اختبار_مدير_الملفات` وأضف اختبارًا جديدًا:
   ```python
   async def test_تحليل_csv(self):
       with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.csv') as tmp:
           tmp.write("اسم,عمر\nمحمد,30\nعلي,25")
           tmp_path = tmp.name
       
       try:
           سجلات = await مدير_الملفات.تحليل_csv(tmp_path)
           self.assertEqual(len(سجلات), 2)
           self.assertEqual(سجلات[0]["اسم"], "محمد")
           self.assertEqual(سجلات[0]["عمر"], "30")
       finally:
           Path(tmp_path).unlink()
   ```

   **الخطوة 3: تحديث واجهة CLI**
   إذا أردت إضافة أمر CLI لتحليل CSV، أضف إلى قسم CLI:
   ```python
   @مكتبة.command()
   @click.argument('مسار_ملف')
   @click.option('--فاصل', default=',', help='الفاصل في ملف CSV')
   def تحليل_csv(مسار_ملف: str, فاصل: str):
       async def _تحليل():
           سجلات = await مدير_الملفات.تحليل_csv(مسار_ملف, فاصل)
           click.echo(json.dumps(سجلات, ensure_ascii=False, indent=2))
       asyncio.run(_تحليل())
   ```

   **الخطوة 4: اختبار التعديل**
   ```bash
   python -m unittest arabic_library
   python arabic_library.py تحليل_csv test.csv
   ```

4. **إضافة فئة جديدة**:
   لنفترض أنك تريد إضافة فئة `مدير_الصور` لمعالجة الصور (مثل تغيير الحجم).

   **الخطوة 1: إضافة الفئة**
   أضف الفئة بعد `مدير_الملفات`:
   ```python
   from PIL import Image

   class مدير_الصور:
       """فئة لمعالجة الصور"""
       
       @staticmethod
       async def تغيير_حجم_صورة(مسار_الإدخال: Union[str, Path], مسار_الإخراج: Union[str, Path], حجم: Tuple[int, int]) -> None:
           """تغيير حجم الصورة"""
           مسار_الإدخال = Path(مسار_الإدخال)
           مسار_الإخراج = Path(مسار_الإخراج)
           if not مسار_الإدخال.exists():
               raise خطأ_ملف(f"الصورة غير موجودة: {مسار_الإدخال}")
           
           async def _تغيير_الحجم():
               with Image.open(مسار_الإدخال) as صورة:
                   صورة_معدلة = صورة.resize(حجم)
                   صورة_معدلة.save(مسار_الإخراج)
           
           await asyncio.get_event_loop().run_in_executor(None, _تغيير_الحجم)
   ```

   **الخطوة 2: إضافة تبعية**
   أضف `Pillow` إلى `setup.py`:
   ```python
   install_requires=[
       ...
       "Pillow>=9.0.0"
   ]
   ```

   **الخطوة 3: إضافة اختبار**
   أضف فئة اختبار جديدة:
   ```python
   class اختبار_مدير_الصور(IsolatedAsyncioTestCase):
       async def test_تغيير_حجم_صورة(self):
           with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
               img = Image.new('RGB', (100, 100), color='red')
               img.save(tmp.name)
               tmp_path = tmp.name
           
           مسار_إخراج = Path(tmp_path).with_suffix('.resized.png')
           try:
               await مدير_الصور.تغيير_حجم_صورة(tmp_path, مسار_إخراج, (50, 50))
               self.assertTrue(مسار_إخراج.exists())
               with Image.open(مسار_إخراج) as صورة:
                   self.assertEqual(صورة.size, (50, 50))
           finally:
               Path(tmp_path).unlink()
               if مسار_إخراج.exists():
                   مسار_إخراج.unlink()
   ```

   **الخطوة 4: اختبار التعديل**
   ```bash
   pip install Pillow
   python -m unittest arabic_library
   ```

5. **تحسين الأداء**:
   - **التخزين المؤقت**: قم بتوسيع استخدام `مدير_redis` لتخزين نتائج أخرى (مثل نتائج تحليل CSV).
   - **التوازي**: استخدم `asyncio.gather` لتحسين أداء العمليات المتعددة (مثل تحليل عدة ملفات CSV).
   - **تقليل استهلاك الموارد**: استخدم `@lru_cache` للدوال التي تُستخدم بشكل متكرر.

6. **إضافة ميزات متقدمة**:
   - **دعم gRPC**: أضف فئة `مدير_grpc` للتعامل مع طلبات gRPC.
   - **تكامل مع قواعد بيانات أخرى**: مثل Cassandra أو DynamoDB.
   - **واجهة ويب**: أنشئ واجهة ويب بسيطة باستخدام FastAPI لعرض وظائف المكتبة.

### **أمثلة تطوير إضافية**

#### **تعديل دالة موجودة**
لنفترض أنك تريد تحسين دالة `طلب_شبكة` لدعم معالجة الملفات الكبيرة (مثل تحميل ملفات).
أضف معامل `تحميل_ملف`:
```python
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
    ذاكرة_مؤقتة: Dict = None,
    تحميل_ملف: Union[str, Path] = None
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
                if تحميل_ملف:
                    with open(تحميل_ملف, 'rb') as ملف:
                        بيانات = {'file': ملف}
                        async with جلسة.post(رابط, data=بيانات) as رد:
                            if رد.status != 200:
                                خطأ = await رد.text()
                                raise خطأ_شبكة(f"{رد.status}: {خطأ}")
                            نتيجة = await رد.json()
                            async with مدير_redis() as redis:
                                await redis.حفظ(mفتاح_التخزين, نتيجة, مدة_الصلاحية=3600)
                            return نتيجة
                else:
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
```

#### **إضافة اختبار للدالة المعدلة**
أضف إلى `اختبار_البرمجة`:
```python
async def test_طلب_شبكة_مع_ملف(self):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"محتوى ملف")
        tmp_path = tmp.name
    try:
        نتيجة = await البرمجة.طلب_شبكة("POST", "https://api.example.com/upload", تحميل_ملف=tmp_path)
        self.assertIsInstance(نتيجة, dict)
    except خطأ_شبكة:
        pass
    finally:
        Path(tmp_path).unlink()
```

---



## **الترخيص**
المكتبة مرخصة بموجب **MIT License**.

---

## **الدعم**
- **البريد الإلكتروني**: aaiiddeenn0770@Gmail.com
- **GitHub Issues**: افتح قضية على المستودع.
- **المجتمع**: غير متوفر 

---

## **خاتمة**
المكتبة العربية الشاملة هي أداة قوية ومرنة لتطوير التطبيقات الحديثة. سواء كنت مبتدئًا أو مطورًا محترفًا، يمكنك استخدامها لتبسيط مهامك أو توسيعها بميزات جديدة. المكتبة مفتوحة للمساهمات، ونرحب بأي أفكار أو تحسينات!

إذا كنت بحاجة إلى مساعدة في التثبيت، الاستخدام، أو التطوير، تواصل معنا! 🚀
