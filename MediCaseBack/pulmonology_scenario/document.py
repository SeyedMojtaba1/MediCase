from langchain_core.documents import Document

PNEUMONIA_REF = """
## 1. CHIEF COMPLAINT (CONCEPT ONLY - REPHRASE)
**Rule:** Max 5 words (single) or 8 words (dual). NO duration mentioned.
* **[Scenario: typical_lobar]:**
    * "تب و لرز شدید دارم"
    * "سینه‌م خیلی درد می‌کنه"
    * "نفس‌هام به خس‌خس افتاده"
* **[Scenario: complicated_effusion]:**
    * "پهلوم بدجور تیر می‌کشه"
    * "نفس عمیق نمی‌تونم بکشم"
    * "درد پهلو و تنگی نفس دارم"
* **[Scenario: atypical_walking]:**
    * "بدنم کوفته‌ست و سرفه می‌کنم"
    * "سرفه‌های خشک ولم نمی‌کنه"
    * "همش احساس خستگی دارم"

## 2. HISTORY OF PRESENT ILLNESS (DATA POOLS)
**Instruction:** Mix and match concepts. Be colloquial.

### A. Symptom Description
* **Fever/Chills:** ["دندونام بهم می‌خورد از لرز"، "انگار تو آتیشم"، "یهو بدنم داغ میشه یهو سرد"]
* **Pain (Pleuritic):** ["انگار چاقو تو پهلومه"، "نفس که می‌کشم تیر می‌کشه"، "انگار یه وزنه رو سینمه"]
* **Cough/Sputum:**
    * **[typical_lobar]:** ["خلطم رنگش عجیبه (قهوه‌ای/زنگ‌زده)"، "خلط کثیف دارم"]
    * **[atypical/complicated]:** ["سرفه‌م خشکه"، "چیزی بالا نمیاد"]

### B. Onset (Start)
* "یهو افتادم." / "فکر کردم سرماخوردگی ساده‌ست ولی بدتر شد."

---

## 3. PAST MEDICAL & DRUGS
* **History:** "من همیشه سالم بودم." / "مریضی خاصی ندارم."
* **Drugs:** "فقط قرص سرماخوردگی خوردم." / "استامینوفن می‌خورم برای تبم."

---

## 4. SOCIAL & FAMILY
* **Social/Pets (Distractor):** "یه قناری (یا گربه/سگ) تو خونه داریم." / "حیوون خونگی داریم ولی تمیزه."
* **Family:** "نه کسی اینطوری نشده."
"""

COPD_REF = """
## 1. CHIEF COMPLAINT (CONCEPT ONLY - REPHRASE)
**Rule:** Max 5 words (single) or 8 words (dual). NO duration mentioned.
* **[Scenario: chronic_bronchitis]:**
    * "خیلی خلط دارم"
    * "سرفه‌های خلط‌ دار می‌کنم"
    * "همش سینه‌م پره"
* **[Scenario: emphysema]:**
    * "جونِ راه رفتن ندارم"
    * "خیلی زود به نفس‌نفس می‌افتم"
    * "نفسم تنگه و لاغر شدم"
* **[Scenario: copd_cor_pulmonale]:**
    * "پاهام ورم کرده"
    * "نفس تنگی و ورم پا دارم"

## 2. HISTORY OF PRESENT ILLNESS (DATA POOLS)
**Instruction:** Mix and match concepts. Be colloquial.

### A. Symptom Description
* **Cough:** ["اول صبح کلی خلط میاد"، "سرفه‌هام کثیفه"، "انگار سینه‌م می‌جوشه"]
* **Dyspnea:** ["دو قدم میرم خسته میشم"، "انگار ریه‌م پر نمیشه"]
* **Edema (Scenario C):** ["پاهام باد کرده تو کفش نمیره"]

### B. Smoking Context
* "سیگار می‌کشم (یا می‌کشیدم)." / "گفتم لابد مال سیگاره که سرفه می‌کنم."

---

## 3. PAST MEDICAL & DRUGS
* **History:** "مریضی خاصی نداشتم، فقط همین سرفه‌ها بود."
* **Drugs:** "گاهی شربت سینه می‌خورم."

---

## 4. SOCIAL & FAMILY
* **Social/Pets (Distractor):** "یه پرنده (یا سگ) دارم تو خونه."
* **Family:** "پدرم هم سرفه می‌کرد (چون سیگاری بود)."
"""

ASTHMA_REF = """
## 1. CHIEF COMPLAINT (CONCEPT ONLY - REPHRASE)
**Rule:** Max 5 words (single) or 8 words (dual). NO duration mentioned.
* **[Scenario: mild_allergic]:**
    * "تک و توک سرفه می‌کنم"
    * "بعضی وقتا سینه‌م می‌گیره"
    * "آبریزش بینی و سرفه دارم"
* **[Scenario: severe_uncontrolled]:**
    * "نفسم اصلا بالا نمیاد"
    * "سینه‌م سوت می‌کشه"
    * "تنگی نفس و سرفه شدید دارم"
* **[Scenario: exercise_induced]:**
    * "موقع دویدن کم میارم"
    * "بعد ورزش سرفه‌م می‌گیره"
    * "سینه‌م موقع فعالیت می‌سوزه"

## 2. HISTORY OF PRESENT ILLNESS (DATA POOLS)
**Instruction:** Mix and match concepts. Be colloquial.

### A. Symptom Description
* **Dyspnea:** ["انگار هوا بهم نمی‌رسه"، "باید زور بزنم تا نفس بکشم"، "انگار راه گلوم بسته میشه"]
* **Wheezing:** ["صدای گربه از سینه‌م میاد"، "سینه‌م خس‌خس می‌کنه"]
* **Triggers (If asked):**
    * **[mild]:** ["وقتی گرد و خاک میشه"، "فصل بهار بدتره"]
    * **[exercise]:** ["فقط وقتی میدوم یا فوتبال بازی می‌کنم"]

### B. Time Pattern
* **[severe]:** ["شبا از خواب می‌پرم"، "همش اذیتم"]
* **[mild]:** ["همیشگی نیست، میاد و میره"]

---

## 3. PAST MEDICAL & DRUGS
* **History:** "سابقه خاصی ندارم." / "بچگی شاید یکم پوستم حساس بود."
* **Drugs:** "هیچی." / "گاهی مسکن ساده می‌خورم."

---

## 4. SOCIAL & FAMILY
* **Social/Pets (Distractor):** "آره یه گربه (یا پرنده) داریم." / "تو خونه حیوون نگه می‌داریم."
* **Sports (Hidden):** *Only mention if asked specifically regarding activity:* "آره ورزش می‌کنم (فوتبال/دو)."
* **Family:** "نه، همه سالمن."
"""

PTE_REF = """
## 1. CHIEF COMPLAINT (CONCEPT ONLY - REPHRASE)
**Rule:** Max 5 words (single) or 8 words (dual). NO duration mentioned.
* **[Scenario: massive_pte]:**
    * "یهو از حال رفتم"
    * "قلبم داره کنده میشه"
    * "بی‌حالی شدید و تنگی نفس"
* **[Scenario: peripheral_infarct]:**
    * "سینه‌م تیر می‌کشه"
    * "با نفس کشیدن درد دارم"
    * "خون تو آب دهنم دیدم"
* **[Scenario: submassive_pte]:**
    * "تپش قلب شدید دارم"
    * "یهو نفسم گرفت"

## 2. HISTORY OF PRESENT ILLNESS (DATA POOLS)
**Instruction:** Mix and match concepts. Be colloquial.

### A. Symptom Description
* **Onset:** ["همه چی یهویی شد"، "داشتم راه می‌رفتم یهو شد"، "نشسته بودم که اینطوری شدم"]
* **Pain:** ["دردش مثل چاقو میمونه"، "نفس میکشم بدتر میشه"]
* **Leg Symptoms (If asked):** ["پشت ساق پام درد می‌کرد"، "پام ورم کرده بود فکر کردم ضربه خورده"]

### B. Context Triggers (If asked)
* "تازه از مسافرت اومدم." / "پام تو گچ بود تازه باز کردم."

---

## 3. PAST MEDICAL & DRUGS
* **History:** "من سالمِ سالمم." / "سابقه لخته و اینا نداشتم."
* **Drugs:** "هیچی مصرف نمی‌کنم."

---

## 4. SOCIAL & FAMILY
* **Social/Pets (Distractor):** "حیوان خانگی داریم (سگ/گربه)."
* **Family:** "نه، کسی تو فامیل سکته یا لخته نداشته."
"""

IPF_REF = """
## 1. CHIEF COMPLAINT (CONCEPT ONLY - REPHRASE)
**Rule:** Max 5 words (single) or 8 words (dual). NO duration mentioned.
* **[Scenario: stable_ipf]:**
    * "سرفه خشک ولم نمی‌کنه"
    * "راه میرم نفسم می‌گیره"
    * "سرفه خشک و تنگی نفس دارم"
* **[Scenario: acute_ipf_exacerbation]:**
    * "دارم خفه میشم"
    * "اصلا نمی‌تونم نفس بکشم"
* **[Scenario: rheumatoid_ild]:**
    * "مفاصل انگشتام درد می‌کنه"
    * "بدن درد و تنگی نفس دارم"

## 2. HISTORY OF PRESENT ILLNESS (DATA POOLS)
**Instruction:** Mix and match concepts. Be colloquial.

### A. Symptom Description
* **Cough:** ["سرفه‌هام خشکه"، "هیچی بالا نمیاد"، "سرفه‌های تک و توک ولی آزاردهنده"]
* **Dyspnea:** ["انگار ریه‌م کوچیک شده"، "نفس عمیق نمیتونم بکشم"]
* **Rheumatoid Signs (Scenario C):** ["انگشتام صبح‌ها خشکه"، "چشم و دهنم خشک میشه"]

---

## 3. PAST MEDICAL & DRUGS
* **History:** "مریضی خاصی نداشتم." / "فقط گاهی پادرد داشتم (نوع روماتیسمی)."
* **Drugs:** "گاهی مسکن می‌خورم برای دردهام."

---

## 4. SOCIAL & FAMILY
* **Social/Pets (Distractor):** "یه گربه داریم تو حیاط." / "قناری نگه میدارم."
* **Family:** "نه، کسی اینطوری نشده بود."
"""

PH_REF = """
## 1. CHIEF COMPLAINT (CONCEPT ONLY - REPHRASE)
**Rule:** Max 5 words (single) or 8 words (dual). NO duration mentioned.
* **[Scenario: idiopathic_pah]:**
    * "با فعالیت تپش قلب می‌گیرم"
    * "زود خسته میشم"
    * "غش کردم موقع راه رفتن"
* **[Scenario: ph_left_heart]:**
    * "شبا نفسم میگیره"
    * "نفس تنگی موقع خواب دارم"
* **[Scenario: ph_lung_disease]:**
    * "لبام کبود میشه"
    * "نفسم اصلا یاری نمیکنه"

## 2. HISTORY OF PRESENT ILLNESS (DATA POOLS)
**Instruction:** Mix and match concepts. Be colloquial.

### A. Symptom Description
* **Exertion:** ["چهار تا پله میرم قلبم میخواد کنده شه"، "قبلا کوه میرفتم الان نمیتونم"]
* **Orthopnea (Scenario B):** ["باید چند تا بالش بذارم زیر سرم"، "دراز میکشم خفه میشم"]
* **Color:** ["رنگم میپره"، "لبام تیره میشه"]

---

## 3. PAST MEDICAL & DRUGS
* **History:** "من سالم بودم." / "فقط شاید فشارم یکم بالا بود (برای نوع قلبی)."
* **Drugs:** "قرص ویتامین یا آهن."

---

## 4. SOCIAL & FAMILY
* **Social/Pets (Distractor):** "آره یه سگ کوچیک دارم." / "پرنده نگه میداریم."
* **Family:** "نه سابقه قلبی تو جوونا نداریم."
"""

documents = [
    Document(page_content=PNEUMONIA_REF, metadata={"disease": "Pneumonia"}),
    Document(page_content=COPD_REF, metadata={"disease": "COPD"}),
    Document(page_content=ASTHMA_REF, metadata={"disease": "Asthma"}),
    Document(page_content=PTE_REF, metadata={"disease": "PTE"}),
    Document(page_content=IPF_REF, metadata={"disease": "IPF"}),
    Document(page_content=PH_REF, metadata={"disease": "PH"}),
]