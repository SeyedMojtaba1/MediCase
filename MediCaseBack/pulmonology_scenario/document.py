from langchain_core.documents import Document

PNEUMONIA_PROFILE_REF = """
disease: Pneumonia
chief_complaint: Acute onset of fever, cough (productive or dry), dyspnea, and 20% of times pleuritic chest pain
"""

PNEUMONIA_HISTORY_REF = """
disease: Pneumonia
present_illness:
    question1: Symptoms typically start acutely over 1 to 7 days
    question2: Onset is usually relatively sudden, 50% of times following a viral URI. 50% of times there is no URI
    question3: Shortness of breath is 55% of times present, 15% of times is present at rest or exertion.there is no shortness of breath at 45% of times
    question4: Cough is 95% of times present. Sputum is 40% of times purulent (yellow/green), rusty (pneumococcal), or currant jelly (Klebsiella)
    question5: Wheezing sound is 5% of times present (if underlying comorbidity like asthma). 95% of times is not present
    question6: Pleuritic chest pain is 20% of times prsent
    question7: Fever, chills (rigors), and night sweats are classic systemic symptoms.(Fever and Chills are 80% of times present. night sweats are 30% of times present)
    question8: Leg swelling is not typical unless there is comorbid heart failure in 40% of over 55y old patients. 60% of times is not present
    question9: Recurrent episodes are 30% of times present (suggesting aspiration or immunodeficiency)
    question10: Fatigue and anorexia are 80% of times present. 20% of time none of them are present
    
past_medical_history:
    question1:
        question1a: Risk factors include COPD, asthma, diabetes, heart failure and one is randomly present in 45% of times
        question1b: Duration of comorbidities is between 2-5 years
    question2: 
        question2a: History of splenectomy is 5% of times present. 85% of times there is no former surgery. 10% of times one of these surgeries is present:Appendectomy, Cholecystectomy, Hernia Repair, Cataract Surgery, CABG, Knee/Hip Replacement, Mastectomy, Hysterectomy, Tonsillectomy, Laminectomy
        question2b: Hospitalization history is present if surgery is present, or 10% of times for other reasons (like infection)
    question3: History of lung/heart disease is present in 40% of over 55y old patients
    question4: Active cancer or chemotherapy is 2% of times present. 98% of times is not present
    question5: Childhood history is 2% of times present. 98% of times is not present
    question6: Vaccination status (Influenza, Pneumococcal) is negative 70% of times. 30% of times vaccination has been done

drug_history:
    question1:
        question1a: Immunosuppressants (steroids, biologic agents) are present in 5-10% of cases (high risk). Regular medications for comorbidities are present in 45% of cases
        question1b: Recent antibiotic use is present in 15% of cases (increases risk of resistant organisms)
        question1c: Change in regular medication (e.g., stopping a dose) is present in 5% of cases
    question2: Use of OTC medications (e.g., Tylenol, cough suppressants) for flu-like symptoms is present in 50% of cases
    
allergies:
    question1:
        question1a: Drug allergy (e.g., Penicillin) is reported in 10% of cases
        question1b: The reported reaction severity determines alternative empiric antibiotic choices

family_history:
    question1: 
        question1a: Irrelevant for acute infection in 99% of cases. Unless immunodeficiency runs in family (rare, <1%)
        question1b: Details of family history are generally non-contributory for acute CAP
    question2: Family history of heart/lung disease is present in 40% of cases (as general context)
    question3: 
        question3a: Family history of cancer is 20% of times present
        question3b: Details are usually non-contributory for acute infection

social_history:
    question1:
        question1a: Smoking history (current or former) is present in 60% of adult patients (a significant risk factor)
        question1b: If former, duration since quitting is relevant for risk assessment
    question2: Heavy alcohol use (risk factor for aspiration) is present in 25% of cases
    question3: 
        question3a: IV drug use (risk factor for Staph aureus pneumonia) is present in 2% of cases
        question3b: Last use date is critical if positive
    question4: Living in crowded settings (e.g., nursing home, dormitory) is present in 15% of cases (risk for Mycoplasma, TB)
    
ROS:
    question1: Fever, chills, fatigue are positive in 80% of cases
    question2: Rash (e.g., erythema multiforme) is seen in <5% of cases (Atypical Pneumonia)
    question3: Headache is present in 20-30% of cases (Atypical Pneumonia)
    question4: Eye symptoms (e.g., conjunctivitis) are seen in <5% of cases (Atypical)
    question5: Sore throat or otitis media is seen in 10-20% of cases (Atypical/Viral)
    question6: Pleuritic Chest Pain (20%), Palpitations (10%). Edema is not typical (90% negative)
    question7: Cough, dyspnea, sputum are positive in 95% of cases. Hemoptysis is rare (2-5%)
    question8: GI symptoms (Nausea, Vomiting, Diarrhea) are present in 20% of cases (especially Legionella/Viral)
    question9: Urinary symptoms are not typical (95% negative)
    question10: Myalgias/arthralgias are present in 30% of cases (Viral/Atypical)
    question11: Confusion/LOC change is a red flag (CURB-65), present in 30% of cases (elderly/severe)
    question12: Mood changes are not typical (95% negative)
    question13: Endocrine symptoms are not typical (95% negative)
    question14: Hematologic symptoms are not typical (95% negative)
"""

COPD_PROFILE_REF = """
disease: COPD (Stable/Chronic Phase)
chief_complaint: Chronic progressive dyspnea (worsening over years) in 90% of cases, exercise intolerance in 80% of cases, or chronic productive cough in 70% of cases for routine checkup
"""

COPD_HISTORY_REF = """
disease: COPD
present_illness:
    question1: In 100% of cases, symptoms have been present for years and are slowly progressive. Patients adapt their lifestyle to accommodate limitations in 85% of cases
    question2: In 100% of cases, onset is insidious and gradual. Sudden onset is 0% in the stable phase
    question3: Shortness of breath is present in 90% of cases. In 80% of cases, it is 'Dyspnea on Exertion' (DOE). In 20% of severe cases, it is present at rest or with minimal activity
    question4: Chronic cough is present in 70% of cases (Chronic Bronchitis phenotype). In 30% of cases (predominantly Emphysema), cough is minimal or absent. Sputum is clear/mucoid in 90% of stable cases
    question5: Wheezing is reported in 50% of cases, often varying day to day or with weather changes. In 50% of cases, no wheezing is reported
    question6: Chest pain is absent in 90% of cases. In 10% of cases, vague chest tightness or musculoskeletal pain from coughing is reported
    question7: Fever, chills, and night sweats are ABSENT in 95% of stable COPD cases. Their presence is 5% (suggesting a new complication)
    question8: Leg swelling (bilateral pitting edema) is present in 25% of cases (suggesting Cor Pulmonale/Right Heart Failure). In 75% of cases, it is absent
    question9: History of progressive decline is present in 100% of cases. History of previous 'bad days' or hospitalizations is present in 60% of cases
    question10: Weight loss/Cachexia is present in 30% of cases (Emphysema phenotype). Fatigue is present in 70% of cases. In 30% of cases (Chronic Bronchitis "Blue Bloater"), patients may be overweight
    
past_medical_history:
    question1:
        question1a: Comorbidities are common: Hypertension is present in 50% of cases, Ischemic Heart Disease in 30%, Diabetes in 20%, and Anxiety/Depression in 40%
        question1b: Duration of comorbidities is present for >5 years in 75% of cases
    question2: 
        question2a: History of previous hospitalizations for respiratory issues is present in 50% of moderate-to-severe cases. 80% of times no unrelated major surgery
        question2b: History of intubation is present in <10% of stable outpatients
    question3: History of heart disease is present in 40% of cases (shared smoking risk)
    question4: History of Lung Cancer (cured/remission) is present in 5% of cases. 95% of times not present
    question5: Childhood respiratory infections are reported in 30% of cases
    question6: Vaccination (Influenza/Pneumococcal) is done in 60% of cases. In 40% of cases, it is missed

drug_history:
    question1:
        question1a: In 80% of cases, patients use maintenance inhalers (LAMA, LABA/LAMA, or ICS/LABA). In 20% of mild cases, only SABA (Salbutamol) is used prn
        question1b: Inhaler technique errors are present in 40% of cases
        question1c: In stable phase, doses are unchanged in 90% of times
    question2: Use of mucolytics or antioxidants is present in 20% of cases

allergies:
    question1:
        question1a: True drug allergy is present in 10% of cases. In 30% of cases, patients may report 'hay fever' (Asthma-COPD overlap)
        question1b: Severity of reaction varies in 100% of reported cases

family_history:
    question1: 
        question1a: Alpha-1 Antitrypsin deficiency in family is present in <1% of cases. Family history of COPD is present in 20% of cases
        question1b: Details often relate to heavy smoking in parents in 80% of cases
    question2: Family history of cardiovascular disease is present in 50% of cases
    question3: 
        question3a: Family history of lung cancer is present in 15% of cases
        question3b: Details of cancer are generally non-contributory for the acute presentation in 99% of cases

social_history:
    question1:
        question1a: Smoking is the cause in 80% of cases. 40% are Current Smokers, 40% are Former Smokers. 20% are Never Smokers (Biomass/Occupational/Genetic causes)
        question1b: Pack-year history is greater than 20 pack-years in 90% of cases
    question2: Alcohol use (social) is present in 30% of cases. Heavy use is present in 10% of cases
    question3: 
        question3a: Recreational drug use is present in <5% of cases
        question3b: Last use date is critical if positive in 100% of cases
    question4: Exposure to biomass fuel or occupational dusts is present in 15% of cases (especially if non-smoker)
    
ROS:
    question1: Fatigue is positive in 60% of cases. Weight change is positive in 40% (Loss in Emphysema, Gain in Bronchitis)
    question2: Skin is normal in 70% of cases. Thin skin/bruising (steroid effect) is present in 20%. Central cyanosis is present in 10% (severe disease)
    question3: Morning headaches are present in 10% of cases (severe CO2 retention)
    question4: Eye symptoms are negative in 95% of cases
    question5: Chronic nasal congestion is present in 30% of cases
    question6: Palpitations are present in 20% of cases (often due to inhaler side effects). Chest pain is negative in 90% of cases
    question7: Dyspnea and Cough are the main positives (see HPI) in 95% of cases. Hemoptysis is present in <5% of stable COPD cases
    question8: GERD symptoms are present in 40% of cases
    question9: Urinary symptoms are present in 30% of cases (e.g., BPH in older males)
    question10: Muscle weakness/wasting is present in 30% of cases
    question11: Neurological symptoms are negative in 95% of cases unless severe hypoxia/hypercapnia exists
    question12: Anxiety/Depression symptoms are positive in 40% of cases
    question13: Joint pains (Osteoarthritis) are present in 50% of elderly COPD patients
    question14: Hematologic symptoms are negative in 85% of cases. Secondary polycythemia is present in 15% of cases (suggesting chronic hypoxemia)
"""

ASTHMA_BOUNDARIES_REF = """
### بخش ۱ — مرزهای بیماری (Disease Boundaries)

**علائم اصلی (Core Symptoms Spectrum):**
* تنگی نفس (Dyspnea) [متغیر: حمله‌ای تا مزمن]
* خس‌خس سینه (Wheezing) [به‌ویژه در بازدم]
* سرفه (Cough) [خشک یا با خلط کم، تشدید در شب یا صبح زود]
* احساس سنگینی یا فشار در قفسه سینه (Chest Tightness)

**علائم اختیاری (Optional Symptoms):**
* خلط (Sputum) [شفاف یا سفید، مگر در صورت عفونت همزمان]
* خستگی ناشی از تلاش تنفسی
* اضطراب یا بی‌قراری (در حملات حاد)
* اختلال خواب (بیدار شدن با سرفه یا تنگی نفس)

**علائم ممنوعه (Forbidden Symptoms - رد کننده تشخیص):**
* استریدور (Stridor) [نشانه انسداد راه هوایی فوقانی]
* هموپتزی وسیع (Massive Hemoptysis)
* کرپیتاسیون یا رال‌های موضعی (Localized Crackles) [مگر در صورت پنومونی همزمان]
* درد قفسه سینه پلورتیک (Pleuritic Chest Pain) [مگر در پنوموتوراکس]
* کاهش وزن توجیه‌ناپذیر

**محدوده‌های شدت (Severity Ranges):**
1.  متناوب (Intermittent)
2.  خفیف پایدار (Mild Persistent)
3.  متوسط پایدار (Moderate Persistent)
4.  شدید پایدار (Severe Persistent)
5.  حمله حاد شدید (Status Asthmaticus)

**محدوده‌های فیزیولوژیک (Physiology Ranges):**
* اشباع اکسیژن ($SpO_2$): $88\%$ (حمله مرگبار) تا $99\%$ (نرمال/بین حملات)
* تعداد تنفس (RR): $12$ تا $40$ تنفس در دقیقه
* جریان بازدمی اوج (PEF): $30\%$ تا $100\%$ مقدار پیش‌بینی شده

**مرزهای محرک (Trigger Limits):**
* باید حداقل یک عامل محرک یا الگوی زمانی (شبانه/فصلی) وجود داشته باشد (مگر در موارد آسم ذاتی شدید).

"""

ASTHMA_VARIABILITY_REF = """
### بخش ۲ — موتور تغییرپذیری (Variability Engine)

**الف. شدت تصادفی (Random Intensity):**
* **فرکانس علائم:** از $<2$ بار در هفته تا چندین بار در روز.
* **بیدار شدن شبانه:** از $0$ بار تا هر شب.
* **محدودیت فعالیت:** از "هیچ" تا "ناتوانی در صحبت کردن".
* **نمره ACT (تست کنترل آسم):** محدوده $5$ تا $25$.

**ب. مسیر تصادفی (Random Trajectory) [احتمالات]:**
* اپیزودیک/حمله‌ای (۶۰٪): دوره‌های بی‌علامتی بین حملات.
* فصلی (۱۵٪): تشدید در بهار یا پاییز.
* مزمن پیشرونده (۱۵٪): علائم دائمی با نوسانات کم.
* شروع دیررس (۱۰٪): شروع علائم در بزرگسالی بدون سابقه کودکی.

**ج. جاسازی زمینه تصادفی (Context Embedding):**
* **محیطی:** حیوانات خانگی (گربه/سگ)، گرد و غبار، رطوبت خانه.
* **شغلی:** نانوا (آرد)، نقاش (ایزوسیانات‌ها)، کشاورز، کارگر نظافت.
* **سبک زندگی:** سیگاری (فعال/غیرفعال)، ورزشکار (آسم ناشی از ورزش).
* **فصلی:** گرده گیاهان، هوای سرد و خشک.
* **عفونی:** شروع علائم پس از عفونت ویروسی تنفسی.

**د. تزریق نویز واقع‌گرایانه (Realistic Noise Injection):**
* **یادآوری مبهم:** "فکر می‌کنم از بچگی داشتم، مطمئن نیستم."
* **توصیف غیردقیق:** "سینه‌ام خس‌خس نمی‌کند، فقط سوت می‌کشد."
* **عدم قطعیت دارویی:** "اسپری آبی را میزنم ولی اسمش را نمی‌دانم."
* **همپوشانی:** اشتباه گرفتن علائم با رفلاکس معده یا عدم تناسب اندام.

**هـ. تغییرات ترکیبی چندگانه (Multi-factor Cross Variation):**
* **خوشه آتوپیک:** آسم + اگزما + رینیت آلرژیک (احتمال بالا).
* **خوشه چاقی:** BMI بالا + آسم شدیدتر + پاسخ کمتر به استروئید.
* **خوشه سالمندان:** آسم + COPD (سندرم همپوشانی ACOS).
"""

ASTHMA_HISTORY_REF = """
### بخش ۳ — قالب تاریخچه ساختاریافته (Structured History Template)

**الف. شکایت اصلی (Chief Complaint Pool):**
* انتخاب ۱ از: ["تنگی نفس"، "سرفه‌های مداوم"، "خس‌خس سینه"، "احساس خفگی"، "تست عملکرد ریه غیرطبیعی (چکاپ)"]
* مدت زمان: متغیر ($1$ ساعت تا $20$ سال).

**ب. مولد بیماری فعلی (Present Illness Generator):**
* **شروع (Onset):** ناگهانی (در مواجهه با محرک) یا تدریجی (پس از سرماخوردگی).
* **محرک‌ها (Triggers Pool):** [ورزش، هوای سرد، گربه، عطر تند، دود سیگار، آسپرین، استرس].
* **الگو (Pattern):** بدتر شدن در شب یا اوایل صبح (احتمال ۸۰٪).
* **عوامل تسکین‌دهنده:** اسپری سالبوتامول (SABA)، نشستن، هوای تازه، کورتون خوراکی.
* **تاثیر بر زندگی:** غیبت از مدرسه/کار، ناتوانی در ورزش.

**ج. مولد سابقه پزشکی (Past Medical Generator):**
* **همبودی‌ها (Comorbidities Pool):** رینیت آلرژیک (۶۰-۸۰٪)، سینوزیت، پولیپ بینی، درماتیت آتوپیک (اگزما)، GERD، چاقی.
* **سابقه بستری:** $0$ تا $N$ بار بستری در ICU یا بخش (نشان‌دهنده شدت).
* **اینتوباسیون قبلی:** [بله/خیر] (پرچم قرمز برای خطر مرگ).

**د. مولد سابقه دارویی (Drug History Generator):**
* **داروهای فعلی:** SABA (Salbutamol)، ICS (Fluticasone, Budesonide)، LABA+ICS، LTRA (Montelukast).
* **پایبندی (Adherence):** [خوب، مصرف نامنظم، قطع خودسرانه به دلیل ترس از کورتون].
* **تکنیک:** [صحیح، غلط] (استفاده از دمیار/Spacer).

**هـ. مولد سابقه خانوادگی (Family History Generator):**
* **ژنتیک:** سابقه آسم، آلرژی یا اگزما در بستگان درجه یک (مادر/پدر/خواهر/برادر).

**و. مولد سابقه اجتماعی (Social History Generator):**
* **سیگار:** [هرگز، سیگاری سابق، سیگاری فعال، در معرض دود دست دوم].
* **محیط خانه:** فرش‌های قدیمی، وجود کپک، حیوانات خانگی.
* **شغل:** بررسی احتمال آسم شغلی.

**ز. مرور سیستم‌ها (ROS Generator):**
* **ENT:** آبریزش بینی، گرفتگی گوش، عطسه.
* **Skin:** راش‌های اگزمایی (چین آرنج/زانو).
* **GI:** سوزش سر دل (تشدید کننده سرفه).
"""

ASTHMA_CONSTRaAINTS_REF = """
### بخش ۵ — محدودیت‌های مبتنی بر شواهد (Constraints)

**عناصر اجباری (Mandatory Elements):**
* باید حداقل یکی از علائم کلیدی (ویزینگ، تنگی نفس، سرفه) موجود باشد.
* ویزینگ نباید "فقط دمی" (Inspiratory only) باشد (مگر اینکه استریدور باشد که تشخیص را رد می‌کند).

**ترکیبات ممنوعه (Forbidden Combinations):**
* $SpO_2 < 85\%$ با "حال عمومی کاملاً خوب و راحت" (تناقض فیزیولوژیک).
* "قفسه سینه خاموش" (Silent Chest) با $RR = 12$ و هوشیاری کامل (سکوت قفسه سینه نشانه نارسایی قریب‌الوقوع است).
* تب بالای $39^{\circ}C$ بدون هیچ علامتی از عفونت (آسم خالص تب ایجاد نمی‌کند).

**قوانین شدت-فیزیولوژی (Severity Consistency Rules):**
* اگر بیمار "قادر به صحبت کردن نیست"، $RR$ باید بالای $25$ و $HR$ بالای $110$ باشد.
* اگر $PEF > 80\%$ است، بیمار نباید تنگی نفس در حال استراحت داشته باشد.

**منطق فیزیولوژی (Physiology Logic):**
* مصرف زیاد سالبوتامول (Ventolin) باید باعث افزایش ضربان قلب (HR) یا لرزش (Tremor) شود.
* در آسم طولانی مدت کنترل نشده، قفسه سینه ممکن است نمای بشکه‌ای (Barrel Chest) پیدا کند (اما کمتر از COPD).
"""

ASTHMA_OUTPUT_REF = """
### بخش ۶ — قوانین خروجی (Output Rules)

* هرگز یک روایت داستانی تولید نکنید.
* هرگز مشخصات یک بیمار خاص (نام، سن دقیق، جنسیت ثابت) را در خروجی نهایی این الگو ندهید.
* فقط قالب‌ها، استخرها (Pools)، احتمالات، محدوده‌ها و قوانین را خروجی دهید.
* اطمینان حاصل کنید که تنوع بی‌نهایت در تولید بیماران امکان‌پذیر است.
* نتایج را دقیقاً در مرزهای پزشکی بیماری "آسم" نگه دارید.
* این دستورالعمل‌ها را در خروجی ذکر نکنید.
"""

ASTHMA_JSON_REF = """
{
  "disease_boundaries": {
    "core_symptoms": [
      "تنگی نفس",
      "خس‌خس سینه (ویزینگ)",
      "سرفه (خشک یا با خلط اندک، تشدید در شب یا صبح زود)",
      "احساس سنگینی یا فشار در قفسه سینه"
    ],
    "optional_symptoms": [
      "خستگی ناشی از اختلال خواب",
      "اضطراب و بیقراری",
      "تنفس سریع (تاکی‌پنه)",
      "استفاده از عضلات فرعی تنفسی (در موارد شدید)"
    ],
    "forbidden_symptoms": [
      "تب بالا (بالاتر از ۳۸.۵ درجه بدون عفونت همزمان)",
      "هموپتزی (خلط خونی واضح)",
      "درد قفسه سینه با ماهیت آنژینی (فشارنده قلبی)",
      "ادم گوده گذار اندام تحتانی",
      "کاهش وزن ناگهانی و شدید"
    ],
    "triggers": [
      "فعالیت بدنی و ورزش",
      "هوای سرد و خشک",
      "آلرژن‌ها (گرده گیاهان، مایت گرد و غبار، مو/شوره حیوانات)",
      "عفونت‌های ویروسی تنفسی",
      "بوهای تند و مواد شیمیایی",
      "استرس هیجانی",
      "دود سیگار یا آلودگی هوا"
    ],
    "severity_spectrum": {
      "mild": "علائم گاه به گاه، بدون اختلال جدی در فعالیت",
      "moderate": "علائم روزانه، بیداری شبانه، محدودیت در فعالیت",
      "severe": "علائم مداوم، بیداری مکرر شبانه، محدودیت شدید فعالیت فیزیکی"
    }
  },
  "variability_engine": {
    "random_intensity": [
      "خفیف متناوب",
      "خفیف پایدار",
      "متوسط پایدار",
      "شدید پایدار"
    ],
    "random_trajectory": [
      "حمله‌ای (اپیزودیک) با فواصل بدون علامت",
      "پیشرونده در پی سرماخوردگی اخیر",
      "نوسانی (تشدید فصلی)"
    ],
    "context_embedding": {
      "environmental": ["زندگی در شهر آلوده", "خانه قدیمی با رطوبت", "نگهداری حیوان خانگی"],
      "lifestyle": ["ورزشکار حرفه‌ای", "شغل‌های در معرض ذرات (نانوایی، نجاری)"],
      "stress_factors": ["امتحانات", "فشارهای کاری"]
    },
    "realistic_noise": {
      "recall_error": ["فراموشی زمان دقیق شروع علائم", "ابهام در تعداد بیداری‌های شبانه"],
      "variable_reporting": ["کم‌اهمیت جلوه دادن علائم توسط بیمار", "اغراق در شدت تنگی نفس به دلیل اضطراب"]
    },
    "multi_factor_cross_variation": [
      "ترکیب رینیت آلرژیک با آسم (سندرم راه‌های هوایی یکپارچه)",
      "تشدید علائم رفلاکس معده (GERD) با سرفه",
      "چاقی و تشدید تنگی نفس"
    ]
  },
  "history_taking": {
    "chief_complaint": {
      "conceptual_goal": "بیان مشکل اصلی از زبان بیمار",
      "symptom_pools": [
        "نمی‌توانم نفس بکشم",
        "سینه‌ام خس‌خس می‌کند",
        "سرفه‌هایم قطع نمی‌شود",
        "موقع ورزش نفسم می‌گیرد"
      ],
      "variability_rules": "تمرکز بر یکی از علائم اصلی (تنگی نفس، سرفه، ویز) به عنوان شکایت غالب"
    },
    "present_illness": {
      "conceptual_goal": "بررسی سیر زمانی، شدت و عوامل مرتبط",
      "onset": ["ناگهانی (پس از تماس با محرک)", "تدریجی (طی چند هفته اخیر)"],
      "progression": ["ثابت", "بدتر شونده", "نوسانی"],
      "triggers": "انتخاب تصادفی از لیست محرک‌ها (حیوانات، سرما، ورزش)",
      "associated_symptoms": ["آبریزش بینی", "اشک‌ریزش", "خارش گلو"],
      "diurnal_variation": "تشدید علائم در شب یا اوایل صبح (ویژگی کلیدی)",
      "general_symptoms": ["خستگی", "کلافگی"]
    },
    "past_medical_history": {
      "conceptual_goal": "یافتن بیماری‌های همراه یا زمینه‌ای آتوپیک",
      "symptom_pools": [
        "اگزما (درماتیت آتوپیک)",
        "رینیت آلرژیک (تب یونجه)",
        "سینوزیت مزمن",
        "پلیپ بینی",
        "رفلاکس معده به مری (GERD)"
      ],
      "probabilities": "احتمال بالای وجود بیماری‌های آتوپیک (تریاد آتوپی)",
      "negative_symptoms": ["نارسایی قلبی", "بیماری انسدادی مزمن ریه (در افراد غیر سیگاری جوان)"]
    },
    "drug_history": {
      "conceptual_goal": "بررسی داروهای مصرفی فعلی (غیر از درمان اصلی آسم)",
      "prescribed_drugs": [
        "آنتی‌هیستامین‌ها (مثل ستیریزین، لوراتادین)",
        "مهارکننده پمپ پروتون (مثل امپرازول برای رفلاکس)",
        "قطره‌های چشمی یا بینی"
      ],
      "otc_and_supplements": ["مولتی‌ویتامین", "مسکن‌های ساده"],
      "recent_changes": ["مصرف اخیر آسپیرین یا NSAID (بررسی حساسیت دارویی)"],
      "constraint": "عدم ذکر اسپری‌های تنفسی یا کورتون‌های سیستمیک به عنوان داروی روتین (مگر در سناریوی آسم کنترل نشده شناخته شده)"
    },
    "allergies": {
      "conceptual_goal": "شناسایی آلرژی‌های دارویی و محیطی",
      "probability": "بسیار بالا (۷۰-۹۰ درصد)",
      "type_of_reaction": ["تنفسی (تنگی نفس)", "پوستی (کهیر)", "گوارشی"],
      "specific_allergens": ["گرده گل", "غذاهای خاص (بادام زمینی، تخم مرغ)", "آسپیرین (در آسم حساس به آسپیرین)"]
    },
    "family_history": {
      "conceptual_goal": "بررسی زمینه ژنتیکی آتوپی",
      "hereditary_conditions": ["آسم", "اگزما", "آلرژی فصلی"],
      "relatives": ["پدر", "مادر", "خواهر/برادر"]
    },
    "social_history": {
      "conceptual_goal": "بررسی فاکتورهای محیطی و سبک زندگی",
      "smoking": ["سیگاری فعال", "سیگاری غیرفعال (دود دست دوم)", "قلیان", "غیر سیگاری"],
      "living_situation": ["وجود قالی/موکت قدیمی", "رطوبت منزل", "حیوانات خانگی (گربه، سگ، پرنده)"],
      "occupation": ["دانش‌آموز", "کارمند اداری", "شغل‌های صنعتی (رنگ‌کاری، نجاری)"]
    },
    "ROS": {
      "conceptual_goal": "بررسی سیستماتیک برای یافتن علائم همراه یا رد تشخیص‌های افتراقی",
      "positive_findings": {
        "HEENT": ["گرفتگی بینی", "ترشحات پشت حلق", "خارش چشم"],
        "Skin": ["خشکی پوست", "ضایعات اگزمایی"],
        "Resp": ["تنگی نفس کوششی", "ویزینگ بازدمی"]
      },
      "negative_findings": {
        "CV": ["تپش قلب غیرطبیعی", "درد قفسه سینه فعالیتی", "اورتوپنه شدید (مختص نارسایی قلب)"],
        "GI": ["تهوع و استفراغ (مگر ناشی از سرفه شدید)"],
        "General": ["تب", "لرز"]
      }
    }
  },
  "constraints": {
    "mandatory_symptoms": [
      "حداقل یکی از سه علامت اصلی (سرفه، ویزینگ، تنگی نفس) باید وجود داشته باشد."
    ],
    "consistency_rules": [
      "اگر شدت بیماری 'شدید' توصیف شود، بیمار نباید قادر به صحبت کردن با جملات کامل باشد.",
      "اگر بیمار سیگاری قهار و مسن است، علائم باید با تشخیص افتراقی COPD همپوشانی منطقی داشته باشد (اما تشخیص نهایی آسم بماند).",
      "علائم نباید صرفاً با فعالیت بدنی ایجاد شوند مگر در نوع 'آسم ناشی از ورزش'."
    ],
    "forbidden_combinations": [
      "تب بالا + شروع ناگهانی تنگی نفس (بیشتر مطرح کننده پنومونی است تا حمله آسم خالص).",
      "تنگی نفس دمی (استریدور) به جای بازدمی (ویزینگ) (مطرح کننده انسداد راه هوایی فوقانی است)."
    ],
    "logic_control": "تنوع نامحدود در ترکیب محرک‌ها و شدت، اما الگوی کلی باید 'برگشت‌پذیر بودن' یا 'نوسانی بودن' علائم را حفظ کند."
  }
}
"""

PTE_PROFILE_REF = """
disease: آمبولی ریه (Pulmonary Thromboembolism - PTE)
chief_complaint: تنگی نفس ناگهانی (شایع‌ترین)، درد قفسه سینه پلورتیک (شایع)، سرفه (شایع)، تاکی‌پنه (تنفس سریع) (شایع‌ترین یافته فیزیکی)
"""

PTE_HISTORY_REF = """
disease: آمبولی ریه (Pulmonary Thromboembolism - PTE)

present_illness:
    question1: علائم از چه زمانی شروع شدند و چه تغییری کردند؟ شروع ناگهانی علائم (تنگی نفس و درد سینه) (شایع)، بدتر شدن علائم در طول چند دقیقه تا چند ساعت
    question2: شروع علائم ناگهانی بوده یا تدریجی؟ بعد از اتفاق خاصی شروع شد؟ شروع ناگهانی (شایع)، بعد از بی‌حرکتی طولانی (پرواز، بستری)، بعد از جراحی یا تروما (شایع)
    question3: آیا تنگی نفس دارید؟ وضعیت و وابستگی آن به فعالیت/استراحت؟ تنگی نفس ناگهانی (شایع‌ترین)، تنگی نفس مداوم، تشدید با فعالیت (ممکن)
    question4: سرفه دارید؟ خشک یا خلط‌دار؟ رنگ و حجم خلط چطور است؟ سرفه (شایع)، سرفه خشک یا خلط‌دار (ممکن)، هموپتیزی (خلط خونی) (گاهی اوقات، نشان‌دهنده انفارکتوس ریوی)
    question5: آیا خس‌خس یا صدای غیرعادی در تنفس شنیدید؟ خس‌خس یا صدای غیرعادی (نادر)
    question6: احساس درد یا فشار در قفسه سینه دارید؟ با تنفس تغییر می‌کند؟ درد قفسه سینه پلورتیک (تیز، با تنفس بدتر می‌شود) (شایع)، درد سینه آنژین‌مانند (فشار، در آمبولی‌های بزرگ) (ممکن)
    question7: تب، لرز یا تعریق شبانه داشتید؟ تب خفیف (شایع)، تب، لرز یا تعریق شبانه (نادر، مگر با عفونت همزمان)
    question8: تورم پا، تپش قلب یا احساس سبکی سر دارید؟ تورم پا (شایع، در صورت سابقه ترومبوز ورید عمقی - DVT)، تپش قلب (شایع، به دلیل تاکی‌کاردی)، احساس سبکی سر یا سنکوپ (در آمبولی‌های بزرگ)
    question9: قبلاً هم چنین حمله‌ای داشتید؟ درمان مؤثر چه بود؟ سابقه آمبولی ریه یا DVT قبلی (عامل خطر شایع)، درمان مؤثر ضدانعقاد (شایع)
    question10: احساس کاهش وزن، خستگی یا بی‌اشتهایی داشتید؟ خستگی (شایع)، کاهش وزن یا بی‌اشتهایی (نادر، مگر در صورت بیماری مزمن زمینه‌ای)

past_medical_history:
    question1a: بیماری‌های مزمن (دیابت، فشار خون، آسم، مشکلات کلیوی/کبدی) سابقه بیماری‌های مزمن (مانند نارسایی قلبی یا COPD)
    question1b: مدت زمان ابتلا مدت زمان ابتلا به بیماری‌های زمینه‌ای
    question2a: سابقه جراحی یا بستری سابقه جراحی اخیر (به خصوص ارتوپدی)، سابقه بستری اخیر (بیش از ۳ روز)
    question2b: دلیل و تاریخ بستری/جراحی دلیل و تاریخ بستری/جراحی
    question3: سابقه بیماری‌های قلبی، ریوی، مغزی سابقه نارسایی قلبی، سابقه بیماری‌های دریچه‌ای قلب، سابقه سکته مغزی
    question4: سابقه سرطان فعال سابقه سرطان فعال (عامل خطر قوی برای آمبولی)
    question5: بیماری‌های خاص دوران کودکی بیماری‌های خاص دوران کودکی
    question6: وضعیت واکسیناسیون وضعیت واکسیناسیون

drug_history:
    question1a: داروهای مصرفی منظم داروهای مصرفی منظم (مانند داروهای ضد بارداری خوراکی، استروژن‌ها) (عامل خطر)
    question1b: دوز و دفعات مصرف دوز و دفعات مصرف دارو
    question1c: تغییرات اخیر در داروها تغییرات اخیر در داروها
    question2: مصرف داروهای OTC، مکمل‌ها یا گیاهی مصرف داروهای OTC، مکمل‌ها یا گیاهی

allergies:
    question1a: آلرژی به دارو، غذا یا ماده خاص آلرژی به دارو، غذا یا ماده خاص
    question1b: نوع واکنش نوع واکنش

family_history:
    question1a: سابقه بیماری‌های مزمن در خانواده درجه یک سابقه بیماری‌های مزمن در خانواده درجه یک
    question1b: فرد مبتلا و سن ابتلا فرد مبتلا و سن ابتلا
    question2: سابقه بیماری‌های قلبی/سکته/نارسایی قلبی سابقه بیماری‌های قلبی/سکته/نارسایی قلبی
    question3a: سابقه سرطان در خانواده درجه یک سابقه سرطان در خانواده درجه یک
    question3b: نوع سرطان و سن تشخیص نوع سرطان و سن تشخیص

social_history:
    question1a: مصرف سیگار، قلیان، پیپ یا نیکوتین مصرف سیگار (عامل خطر)
    question1b: زمان ترک در صورت سابقه زمان ترک در صورت سابقه
    question2: مصرف الکل (نوع و میزان) مصرف الکل (نوع و میزان)
    question3a: مصرف مواد مخدر مصرف مواد مخدر
    question3b: نوع و زمان آخرین مصرف نوع و زمان آخرین مصرف
    question4: وضعیت زندگی (با چه کسانی زندگی می‌کنید) وضعیت زندگی (با چه کسانی زندگی می‌کنید)

ROS:
    question1: عمومی (تب، لرز، کاهش وزن، خستگی شدید) تب خفیف (شایع)، خستگی (شایع)، لرز، کاهش وزن (نادر)
    question2: پوستی (راش، خارش، تغییر رنگ/بافت) تعریق (شایع)، سیانوز (کبودی، در آمبولی‌های بزرگ)
    question3: سر/گردن/لنفاوی (سردرد، سفتی گردن، بزرگی غدد) بزرگ شدن وریدهای گردن (در آمبولی‌های بزرگ با نارسایی قلب راست)
    question4: چشمی (تاری دید، دوبینی، درد/قرمزی چشم) تاری دید، دوبینی، درد/قرمزی چشم (نادر)
    question5: گوش/حلق/بینی (وزوز، کاهش شنوایی، گلودرد، بلع مشکل) وزوز، کاهش شنوایی، گلودرد، بلع مشکل (نادر)
    question6: قلبی (درد قفسه سینه، تپش، تنگی نفس، تورم پا) درد قفسه سینه (شایع)، تپش قلب (شایع)، تنگی نفس (شایع)، تورم پا (شایع، در صورت DVT)
    question7: تنفسی (سرفه، خس‌خس، خلط خونی) سرفه (شایع)، خلط خونی (گاهی اوقات)، خس‌خس (نادر)
    question8: گوارشی (تهوع، استفراغ، درد شکم، تغییر اجابت مزاج) تهوع، استفراغ، درد شکم، تغییر اجابت مزاج (نادر)
    question9: ادراری تناسلی (سوزش، تکرر، خون در ادرار، ترشحات) سوزش/تکرر ادرار/خون در ادرار/ترشحات (نادر)
    question10: عضلانی اسکلتی (درد/سفتی/تورم مفاصل، ضعف عضلانی) درد، تورم، قرمزی و گرمی ساق پا (شایع در صورت DVT)
    question11: عصبی (سردرد جدید، تشنج، بی‌حسی، اختلال تعادل/حافظه) سبکی سر یا سنکوپ (در آمبولی‌های بزرگ)
    question12: روانی (افسردگی، اضطراب، تغییر خلق، اختلال خواب) اضطراب (شایع به دلیل تنگی نفس)
    question13: غدد درون‌ریز (افزایش تشنگی/گرسنگی/ادرار، عدم تحمل گرما/سرما) افزایش تشنگی/گرسنگی/ادرار، عدم تحمل گرما/سرما (نادر)
    question14: خون و لنفاوی (کبودی آسان، خونریزی طولانی، کم‌خونی شدید) کبودی آسان (نادر)
"""

IPF_PROFILE_REF = """
disease: فیبروز ریوی ایدیوپاتیک (IPF)
chief_complaint: تنگی نفس (شایع‌ترین)، سرفه خشک و مزمن (شایع)
"""

IPF_HISTORY_REF = """
disease: فیبروز ریوی ایدیوپاتیک (IPF)

present_illness:
    question1: علائم از چه زمانی شروع شدند و چه تغییری کردند؟ شروع تدریجی (شایع)، بدتر شدن تدریجی علائم با گذشت زمان (شایع)، معمولاً در افراد بالای ۵۰ سال
    question2: شروع علائم ناگهانی بوده یا تدریجی؟ بعد از اتفاق خاصی شروع شد؟ شروع تدریجی و مبهم (شایع)، بدون سابقه عفونت اخیر یا محرک مشخص (شایع)
    question3: آیا تنگی نفس دارید؟ وضعیت و وابستگی آن به فعالیت/استراحت؟ تنگی نفس در ابتدا با فعالیت (شایع‌ترین)، تنگی نفس پیشرونده که در نهایت در استراحت نیز رخ می‌دهد (شایع)
    question4: سرفه دارید؟ خشک یا خلط‌دار؟ رنگ و حجم خلط چطور است؟ سرفه خشک و مزمن (شایع)، سرفه بدون خلط قابل توجه (شایع)
    question5: آیا خس‌خس یا صدای غیرعادی در تنفس شنیدید؟ عدم وجود خس‌خس (افتراق از آسم یا COPD)، صدای غیرعادی مانند کراکل‌های (Crepitations) انتهای دمی (معمولاً در IPF شنیده می‌شود)
    question6: احساس درد یا فشار در قفسه سینه دارید؟ درد قفسه سینه (نادر)، فشار قفسه سینه ناشی از تنگی نفس (ممکن)
    question7: تب، لرز یا تعریق شبانه داشتید؟ تب، لرز یا تعریق شبانه (معمولاً وجود ندارد، مگر در تشدید حاد یا عفونت)
    question8: تورم پا، تپش قلب یا احساس سبکی سر دارید؟ تورم پا (نادر در مراحل اولیه، اما می‌تواند نشان‌دهنده پرفشاری خون ریوی یا نارسایی قلب راست باشد)، تپش قلب (نادر)، احساس سبکی سر (نادر)
    question9: قبلاً هم چنین حمله‌ای داشتید؟ درمان مؤثر چه بود؟ سابقه تنگی نفس یا سرفه مزمن (ممکن)، درمان‌های قبلی غیرمؤثر برای آسم یا COPD (ممکن)
    question10: احساس کاهش وزن، خستگی یا بی‌اشتهایی داشتید؟ خستگی و ضعف (شایع)، کاهش وزن (ممکن است در مراحل پیشرفته)، بی‌اشتهایی (ممکن است در مراحل پیشرفته)

past_medical_history:
    question1a: بیماری‌های مزمن (دیابت، فشار خون، آسم، مشکلات کلیوی/کبدی) نداشتن آسم یا COPD (افتراق از سایر بیماری‌های ریوی)، سابقه بیماری‌های ریوی قبلی (مانند سابقه پنومونی)
    question1b: مدت زمان ابتلا مدت زمان ابتلا به بیماری‌های زمینه‌ای
    question2a: سابقه جراحی یا بستری سابقه جراحی یا بستری قبلی
    question2b: دلیل و تاریخ بستری/جراحی دلیل و تاریخ بستری/جراحی
    question3: سابقه بیماری‌های قلبی، ریوی، مغزی سابقه پرفشاری خون ریوی یا نارسایی قلب راست (عارضه IPF)
    question4: سابقه سرطان فعال سابقه سرطان فعال
    question5: بیماری‌های خاص دوران کودکی بیماری‌های خاص دوران کودکی
    question6: وضعیت واکسیناسیون وضعیت واکسیناسیون (توصیه به واکسن‌های آنفولانزا و پنوموکوک برای کاهش خطر عفونت)

drug_history:
    question1a: داروهای مصرفی منظم داروهای مصرفی منظم (داروهای ضد فیبروز مانند پرفنیدون یا نینتدانیب در صورت تشخیص IPF)
    question1b: دوز و دفعات مصرف دوز و دفعات مصرف دارو
    question1c: تغییرات اخیر در داروها تغییرات اخیر در داروها
    question2: مصرف داروهای OTC، مکمل‌ها یا گیاهی مصرف داروهای OTC، مکمل‌ها یا گیاهی

allergies:
    question1a: آلرژی به دارو، غذا یا ماده خاص آلرژی به دارو، غذا یا ماده خاص
    question1b: نوع واکنش نوع واکنش

family_history:
    question1a: سابقه بیماری‌های مزمن در خانواده درجه یک سابقه بیماری‌های مزمن در خانواده درجه یک
    question1b: فرد مبتلا و سن ابتلا فرد مبتلا و سن ابتلا
    question2: سابقه بیماری‌های قلبی/سکته/نارسایی قلبی سابقه بیماری‌های قلبی/سکته/نارسایی قلبی
    question3a: سابقه سرطان در خانواده درجه یک سابقه سرطان در خانواده درجه یک
    question3b: نوع سرطان و سن تشخیص نوع سرطان و سن تشخیص

social_history:
    question1a: مصرف سیگار، قلیان، پیپ یا نیکوتین مصرف سیگار (عامل خطر شایع برای IPF)
    question1b: زمان ترک در صورت سابقه زمان ترک در صورت سابقه
    question2: مصرف الکل (نوع و میزان) مصرف الکل (نوع و میزان)
    question3a: مصرف مواد مخدر مصرف مواد مخدر
    question3b: نوع و زمان آخرین مصرف نوع و زمان آخرین مصرف
    question4: وضعیت زندگی (با چه کسانی زندگی می‌کنید) وضعیت زندگی (با چه کسانی زندگی می‌کنید)

ROS:
    question1: عمومی (تب، لرز، کاهش وزن، خستگی شدید) خستگی شدید (شایع)، کاهش وزن (ممکن است در مراحل پیشرفته)، تب، لرز (معمولاً وجود ندارد)
    question2: پوستی (راش، خارش، تغییر رنگ/بافت) چماقی شدن انگشتان (Clubbing) (شایع، یافته بالینی)، کبودی ناخن‌ها (نادر)
    question3: سر/گردن/لنفاوی (سردرد، سفتی گردن، بزرگی غدد) سردرد، سفتی گردن، بزرگی غدد (نادر)
    question4: چشمی (تاری دید، دوبینی، درد/قرمزی چشم) تاری دید، دوبینی، درد/قرمزی چشم (نادر)
    question5: گوش/حلق/بینی (وزوز، کاهش شنوایی، گلودرد، بلع مشکل) گلودرد، بلع مشکل (نادر)
    question6: قلبی (درد قفسه سینه، تپش، تنگی نفس، تورم پا) تنگی نفس (شایع)، تورم پا (در صورت عارضه پرفشاری ریوی)، درد قفسه سینه (نادر)
    question7: تنفسی (سرفه، خس‌خس، خلط خونی) سرفه خشک و مزمن (شایع)، عدم وجود خس‌خس (شایع)، خلط خونی (نادر)
    question8: گوارشی (تهوع، استفراغ، درد شکم، تغییر اجابت مزاج) رفلاکس اسید معده (GERD) (همراهی شایع با IPF)
    question9: ادراری تناسلی (سوزش، تکرر، خون در ادرار، ترشحات) سوزش/تکرر ادرار/خون در ادرار/ترشحات (نادر)
    question10: عضلانی اسکلتی (درد/سفتی/تورم مفاصل، ضعف عضلانی) درد عضلانی و مفصلی (ممکن است در اوایل)، ضعف عضلانی (در مراحل پیشرفته)
    question11: عصبی (سردرد جدید، تشنج، بی‌حسی، اختلال تعادل/حافظه) سردرد جدید، تشنج، بی‌حسی، اختلال تعادل/حافظه (نادر)
    question12: روانی (افسردگی، اضطراب، تغییر خلق، اختلال خواب) افسردگی و اضطراب (شایع به دلیل بیماری مزمن)
    question13: غدد درون‌ریز (افزایش تشنگی/گرسنگی/ادرار، عدم تحمل گرما/سرما) افزایش تشنگی/گرسنگی/ادرار، عدم تحمل گرما/سرما (نادر)
    question14: خون و لنفاوی (کبودی آسان، خونریزی طولانی، کم‌خونی شدید) کبودی آسان، خونریزی طولانی، کم‌خونی شدید (نادر)
"""

PH_PROFILE_REF = """
disease: Pulmonary Hypertension
chief_complaint: تنگی نفس پیش‌رونده (60 درصد)، خستگی و ضعف (20 درصد)، درد قفسه سینه (10 درصد)، سنکوپ یا غش (5 درصد)، تورم پاها (5 درصد)
"""

PH_HISTORY_REF = """
disease: Pulmonary Hypertension

present_illness:
    question1: علائم از چه زمانی شروع شدند و چه تغییری کردند؟ پیشرفت تدریجی طی ماه‌ها تا سال‌ها (80 درصد)، شروع نسبتاً سریع (20 درصد)
    question2: شروع علائم ناگهانی بوده یا تدریجی؟ بعد از اتفاق خاصی شروع شد؟ شروع تدریجی و مبهم (90 درصد)، شروع پس از آمبولی ریه (5 درصد)، شروع پس از بارداری (5 درصد)
    question3: آیا تنگی نفس دارید؟ وضعیت و وابستگی آن به فعالیت/استراحت؟ تنگی نفس فعالیتی (95 درصد)، تنگی نفس در استراحت (مراحل پیشرفته) (40 درصد)، ارتوپنه (در صورت نارسایی قلب چپ) (30 درصد)
    question4: سرفه دارید؟ خشک یا خلط‌دار؟ رنگ و حجم خلط چطور است؟ سرفه خشک (20 درصد)، خلط خونی (هموپتزی) (5 درصد)، بدون سرفه (75 درصد)
    question5: آیا خس‌خس یا صدای غیرعادی در تنفس شنیدید؟ خس‌خس سینه (در صورت همراهی با COPD/آسم) (15 درصد)، بدون صدای غیرعادی (85 درصد)
    question6: احساس درد یا فشار در قفسه سینه دارید؟ با تنفس تغییر می‌کند؟ درد آنژینی قفسه سینه (ناشی از ایسکمی بطن راست) (40 درصد)، درد پلورتیک (10 درصد)، بدون درد (50 درصد)
    question7: تب، لرز یا تعریق شبانه داشتید؟ خیر (95 درصد)، بله (در صورت بیماری‌های عفونی یا خودایمنی زمینه‌ای) (5 درصد)
    question8: تورم پا، تپش قلب یا احساس سبکی سر دارید؟ ادم محیطی و تورم پا (50 درصد)، تپش قلب (30 درصد)، سبکی سر (40 درصد)
    question9: قبلاً هم چنین حمله‌ای داشتید؟ درمان مؤثر چه بود؟ سابقه حملات سنکوپ (15 درصد)، علائم پایدار بدون حمله حاد (85 درصد)
    question10: احساس کاهش وزن، خستگی یا بی‌اشتهایی داشتید؟ خستگی مفرط (80 درصد)، افزایش وزن ناشی از ادم (30 درصد)، کاهش وزن (کاکسکی قلبی) (10 درصد)

past_medical_history:
    question1a: بیماری‌های مزمن (دیابت، فشار خون، آسم، مشکلات کلیوی/کبدی) نارسایی قلب چپ (40 درصد)، بیماری‌های ریوی مزمن مانند COPD یا فیبروز (30 درصد)، آپنه خواب (15 درصد)، بیماری‌های بافت همبند مانند اسکلرودرمی (10 درصد)، عفونت HIV (1 درصد)
    question1b: مدت زمان ابتلا متغیر بسته به بیماری زمینه‌ای (100 درصد)
    question1c: وضعیت کنترل بیماری تحت کنترل (50 درصد)، کنترل نشده (50 درصد)
    question2a: سابقه جراحی یا بستری سابقه بستری برای نارسایی قلب (30 درصد)، سابقه آمبولی ریه (CTEPH) (5 درصد)، بدون سابقه بستری مرتبط (65 درصد)
    question2b: دلیل و تاریخ بستری/جراحی بستری اخیر جهت تنظیم دارو (20 درصد)
    question3: سابقه بیماری‌های قلبی، ریوی، مغزی نارسایی دریچه میترال یا آئورت (30 درصد)، بیماری انسدادی ریه (25 درصد)، بیماری بینابینی ریه (15 درصد)
    question4: سابقه سرطان فعال خیر (95 درصد)، بله (ممکن است تحت شیمی‌درمانی باشند) (5 درصد)
    question5: بیماری‌های خاص دوران کودکی بیماری مادرزادی قلب (ASD/VSD) (10 درصد)، بدون سابقه (90 درصد)
    question6: وضعیت واکسیناسیون کامل (80 درصد)، ناقص (20 درصد)

drug_history:
    question1a: داروهای مصرفی منظم دیورتیک‌ها (فوروزماید/اسپیرونولاکتون) (40 درصد)، مسدودکننده کانال کلسیم (10 درصد)، سیلدنافیل/تادالافیل (30 درصد)، آنتی‌کوآگولانت (20 درصد)
    question1b: دوز و دفعات مصرف متغیر بر اساس شدت بیماری (100 درصد)
    question1c: تغییرات اخیر در داروها افزایش دوز دیورتیک (20 درصد)، شروع داروی جدید (10 درصد)، بدون تغییر (70 درصد)
    question2: مصرف داروهای OTC، مکمل‌ها یا گیاهی مصرف مکمل‌های کاهش وزن (تاریخچه مصرف داروهای ضداشتها) (5 درصد)، مصرف مولتی‌ویتامین (30 درصد)

allergies:
    question1a: آلرژی به دارو، غذا یا ماده خاص بدون آلرژی شناخته شده (80 درصد)، حساسیت به پنی‌سیلین (10 درصد)، حساسیت به سولفا (5 درصد)
    question1b: نوع واکنش راش پوستی (15 درصد)، کهیر (5 درصد)

family_history:
    question1a: سابقه بیماری‌های مزمن در خانواده درجه یک فشار خون ریوی ارثی (HPAH) (6 درصد)، بیماری بافت همبند (10 درصد)، بدون سابقه مرتبط (84 درصد)
    question1b: فرد مبتلا و سن ابتلا بستگان درجه اول (6 درصد)
    question2: سابقه بیماری‌های قلبی/سکته/نارسایی قلبی نارسایی قلبی در والدین (30 درصد)، سکته قلبی زودرس (20 درصد)
    question3a: سابقه سرطان در خانواده درجه یک مثبت (30 درصد)، منفی (70 درصد)
    question3b: نوع سرطان و سن تشخیص غیر مرتبط با بیماری فعلی (100 درصد)

social_history:
    question1a: مصرف سیگار، قلیان، پیپ یا نیکوتین سابقه مصرف سیگار (در بیماران COPD) (40 درصد)، غیرسیگاری (60 درصد)
    question1b: زمان ترک در صورت سابقه ترک کرده (20 درصد)، مصرف کننده فعلی (20 درصد)
    question2: مصرف الکل (نوع و میزان) مصرف اجتماعی (30 درصد)، مصرف زیاد (مرتبط با بیماری کبدی پورتوپلمونری) (5 درصد)، منفی (65 درصد)
    question3a: مصرف مواد مخدر سابقه مصرف متامفتامین یا کوکائین (ریسک فاکتور شناخته شده) (5 درصد)، منفی (95 درصد)
    question3b: نوع و زمان آخرین مصرف متغیر (5 درصد)
    question4: وضعیت زندگی (با چه کسانی زندگی می‌کنید) زندگی با خانواده (70 درصد)، تنها (30 درصد)

ROS:
    question1: عمومی (تب، لرز، کاهش وزن، خستگی شدید) خستگی مفرط (80 درصد)، ضعف عمومی (60 درصد)، کاهش تحمل فعالیت (90 درصد)
    question2: پوستی (راش، خارش، تغییر رنگ/بافت) پدیده رینود (سردی و تغییر رنگ انگشتان) (10 درصد)، سیانوز (کبودی لب و انگشتان) (20 درصد)، تلانژکتازی (5 درصد)
    question3: سر/گردن/لنفاوی (سردرد، سفتی گردن، بزرگی غدد) برجستگی وریدهای گردنی (JVD) (50 درصد)، سردرد (ناشی از هیپوکسی) (10 درصد)
    question4: چشمی (تاری دید، دوبینی، درد/قرمزی چشم) طبیعی (90 درصد)، پرخونی ملتحمه (در آپنه خواب) (10 درصد)
    question5: گوش/حلق/بینی (وزوز، کاهش شنوایی، گلودرد، بلع مشکل) گرفتگی صدا (سندروم اورتنر - نادر) (2 درصد)، طبیعی (98 درصد)
    question6: قلبی (درد قفسه سینه، تپش، تنگی نفس، تورم پا) تنگی نفس (95 درصد)، ادم پدال (50 درصد)، تپش قلب (30 درصد)، درد سینه (40 درصد)
    question7: تنفسی (سرفه، خس‌خس، خلط خونی) سرفه خشک (20 درصد)، هموپتزی (5 درصد)، تنگی نفس شبانه (30 درصد)
    question8: گوارشی (تهوع، استفراغ، درد شکم، تغییر اجابت مزاج) اتساع شکم/آسیت (20 درصد)، سیری زودرس (ناشی از احتقان کبد) (15 درصد)، درد ربع فوقانی راست شکم (15 درصد)
    question9: ادراری تناسلی (سوزش، تکرر، خون در ادرار، ترشحات) اولیگوری (کاهش ادرار در نارسایی قلب) (10 درصد)، شب‌ادراری (15 درصد)، طبیعی (75 درصد)
    question10: عضلانی اسکلتی (درد/سفتی/تورم مفاصل، ضعف عضلانی) درد مفاصل (در بیماری‌های بافت همبند) (15 درصد)، تورم ساق پا (50 درصد)
    question11: عصبی (سردرد جدید، تشنج، بی‌حسی، اختلال تعادل/حافظه) سرگیجه (40 درصد)، سنکوپ (غش کردن) (15 درصد)، خواب‌آلودگی طی روز (آپنه خواب) (15 درصد)
    question12: روانی (افسردگی، اضطراب، تغییر خلق، اختلال خواب) اضطراب (مرتبط با تنگی نفس) (40 درصد)، افسردگی (30 درصد)، اختلال خواب (30 درصد)
    question13: غدد درون‌ریز (افزایش تشنگی/گرسنگی/ادرار، عدم تحمل گرما/سرما) کم‌کاری تیروئید (همراهی شایع) (15 درصد)، دیابت (20 درصد)
    question14: خون و لنفاوی (کبودی آسان، خونریزی طولانی، کم‌خونی شدید) کم‌خونی (10 درصد)، پلی‌سیتمی (افزایش غلظت خون ناشی از هیپوکسی مزمن) (15 درصد)
"""

ARDS_PROFILE_REF = """
disease: سندرم دیسترس تنفسی حاد (ARDS)
chief_complaint: تنگی نفس شدید و ناگهانی (۹۰ درصد)، تنفس سریع و سطحی (۸۰ درصد)، اضطراب و بی‌قراری ناشی از کمبود اکسیژن (۴۰ درصد)، سرفه (۳۰ درصد)
"""

ARDS_HISTORY_REF = """
disease: سندرم دیسترس تنفسی حاد (ARDS)

present_illness:
    question1: علائم از چه زمانی شروع شدند و چه تغییری کردند؟ شروع ناگهانی (۱۰۰ درصد)، بدتر شدن سریع علائم در عرض چند ساعت (۹۰ درصد)
    question2: شروع علائم ناگهانی بوده یا تدریجی؟ بعد از اتفاق خاصی شروع شد؟ شروع ناگهانی پس از عفونت ریوی یا سپسیس (۶۰ درصد)، شروع پس از تروما (۳۰ درصد)، پس از آسپیراسیون (۱۰ درصد)
    question3: آیا تنگی نفس دارید؟ وضعیت و وابستگی آن به فعالیت/استراحت؟ تنگی نفس شدید در استراحت (۹۵ درصد)، عدم بهبود با اکسیژن درمانی استاندارد (۹۰ درصد)
    question4: سرفه دارید؟ خشک یا خلط‌دار؟ رنگ و حجم خلط چطور است؟ سرفه خشک (۴۰ درصد)، سرفه با خلط چرکی (در صورت پنومونی) (۳۰ درصد)، بدون سرفه (۳۰ درصد)
    question5: آیا خس‌خس یا صدای غیرعادی در تنفس شنیدید؟ کراکل یا رال دوطرفه (۹۰ درصد)، خس‌خس (۱۰ درصد)
    question6: احساس درد یا فشار در قفسه سینه دارید؟ با تنفس تغییر می‌کند؟ درد قفسه سینه پلورتیک (در صورت ذات‌الریه) (۲۰ درصد)، بدون درد (۸۰ درصد)
    question7: تب، لرز یا تعریق شبانه داشتید؟ تب و لرز (در صورت وجود سپسیس یا پنومونی) (۷۰ درصد)، بدون تب (۳۰ درصد)
    question8: تورم پا، تپش قلب یا احساس سبکی سر دارید؟ تپش قلب (تاکی‌کاردی) (۹۰ درصد)، سبکی سر یا گیجی (هیپوکسی) (۵۰ درصد)، تورم پا (نادر)
    question9: قبلاً هم چنین حمله‌ای داشتید؟ درمان مؤثر چه بود؟ خیر، اولین تجربه (۹۵ درصد)، بله (سابقه بیماری ریوی مزمن تشدید شده) (۵ درصد)
    question10: احساس کاهش وزن، خستگی یا بی‌اشتهایی داشتید؟ خستگی و ضعف حاد (۱۰۰ درصد)، بدون سابقه کاهش وزن اخیر (۹۰ درصد)

past_medical_history:
    question1a: بیماری‌های مزمن (دیابت، فشار خون، آسم، مشکلات کلیوی/کبدی) اختلال مصرف الکل (ریسک فاکتور مهم) (۳۰ درصد)، بیماری مزمن کبدی (۱۰ درصد)، بیماری مزمن کلیوی (۱۰ درصد)
    question1b: مدت زمان ابتلا مدت زمان ابتلا به بیماری‌های زمینه‌ای
    question2a: سابقه جراحی یا بستری سابقه بستری اخیر یا جراحی اورژانس (۲۰ درصد)، تروماهای شدید اخیر (۱۵ درصد)
    question2b: دلیل و تاریخ بستری/جراحی دلیل و تاریخ بستری/جراحی
    question3: سابقه بیماری‌های قلبی، ریوی، مغزی نارسایی قلبی (برای تشخیص افتراقی مهم است) (۱۰ درصد)، سابقه بیماری ریوی مزمن (۲۰ درصد)
    question4: سابقه سرطان فعال بدخیمی‌های تحت شیمی‌درمانی (تضعیف ایمنی) (۱۰ درصد)، منفی (۹۰ درصد)
    question5: بیماری‌های خاص دوران کودکی بیماری‌های خاص دوران کودکی
    question6: وضعیت واکسیناسیون نقص در واکسیناسیون آنفولانزا یا پنوموکوک (در موارد پنومونی ویروسی/باکتریال) (۲۰ درصد)، نامشخص (۸۰ درصد)

drug_history:
    question1a: داروهای مصرفی منظم داروهای سرکوب‌گر ایمنی (۱۰ درصد)، داروهای بیماری‌های مزمن (۴۰ درصد)، هیچ (۵۰ درصد)
    question1b: دوز و دفعات مصرف دوز و دفعات مصرف دارو
    question1c: تغییرات اخیر در داروها آمیودارون (نادر) (۱ درصد)، بدون تغییر (۹۴ درصد)
    question2: مصرف داروهای OTC، مکمل‌ها یا گیاهی غیر مرتبط (۱۰۰ درصد)

allergies:
    question1a: آلرژی به دارو، غذا یا ماده خاص واکنش آنافیلاکسی (که منجر به شوک شده باشد) (۱ درصد)، خیر (۹۹ درصد)
    question1b: نوع واکنش نوع واکنش

family_history:
    question1a: سابقه بیماری‌های مزمن در خانواده درجه یک غیر مرتبط با ARDS حاد (۱۰۰ درصد)
    question1b: فرد مبتلا و سن ابتلا غیر مرتبط (۱۰۰ درصد)
    question2: سابقه بیماری‌های قلبی/سکته/نارسایی قلبی سابقه نارسایی قلبی (جهت رد علل قلبی) (۲۰ درصد)
    question3a: سابقه سرطان در خانواده درجه یک غیر مرتبط (۱۰۰ درصد)
    question3b: نوع سرطان و سن تشخیص غیر مرتبط (۱۰۰ درصد)

social_history:
    question1a: مصرف سیگار، قلیان، پیپ یا نیکوتین مصرف سیگار (افزایش ریسک آسیب ریوی) (۴۰ درصد)، منفی (۶۰ درصد)
    question1b: زمان ترک در صورت سابقه متغیر (۱۰۰ درصد)
    question2: مصرف الکل (نوع و میزان) مصرف مزمن و زیاد الکل (ریسک فاکتور مهم) (۳۰ درصد)
    question3a: مصرف مواد مخدر مصرف تزریقی (ریسک سپسیس) (۱۰ درصد)، استنشاقی (آسیب مستقیم ریه) (۵ درصد)
    question3b: نوع و زمان آخرین مصرف نوع و زمان آخرین مصرف
    question4: وضعیت زندگی (با چه کسانی زندگی می‌کنید) غیر موثر در پاتولوژی حاد (۱۰۰ درصد)

ROS:
    question1: عمومی (تب، لرز، کاهش وزن، خستگی شدید) تب بالا (۷۰ درصد)، ضعف شدید (۱۰۰ درصد)، لرز (۷۰ درصد)
    question2: پوستی (راش، خارش، تغییر رنگ/بافت) سیانوز یا کبودی انتهاها و لب‌ها (۶۰ درصد)، پوست سرد و مرطوب (در شوک) (۳۰ درصد)
    question3: سر/گردن/لنفاوی (سردرد، سفتی گردن، بزرگی غدد) طبیعی (۸۰ درصد)، استفاده از عضلات فرعی تنفسی (۹۰ درصد)
    question4: چشمی (تاری دید، دوبینی، درد/قرمزی چشم) طبیعی (۱۰۰ درصد)
    question5: گوش/حلق/بینی (وزوز، کاهش شنوایی، گلودرد، بلع مشکل) طبیعی (۱۰۰ درصد)
    question6: قلبی (درد قفسه سینه، تپش، تنگی نفس، تورم پا) تاکی‌کاردی (۹۰ درصد)، افت فشار خون (در شوک) (۵۰ درصد)، بدون تورم پا (۹۰ درصد)
    question7: تنفسی (سرفه، خس‌خس، خلط خونی) تنفس سریع و سطحی (۸۰ درصد)، کراکل دوطرفه (۹۰ درصد)، عدم وجود خس‌خس (۹۰ درصد)
    question8: گوارشی (تهوع، استفراغ، درد شکم، تغییر اجابت مزاج) تهوع و استفراغ (۲۰ درصد)، طبیعی (۸۰ درصد)
    question9: ادراری تناسلی (سوزش، تکرر، خون در ادرار، ترشحات) اولیگوری (کاهش ادرار ناشی از شوک) (۴۰ درصد)، عفونت ادراری (منشا سپسیس) (۱۰ درصد)
    question10: عضلانی اسکلتی (درد/سفتی/تورم مفاصل، ضعف عضلانی) شکستگی‌های متعدد (عامل تروما) (۱۰ درصد)، طبیعی (۹۰ درصد)
    question11: عصبی (سردرد جدید، تشنج، بی‌حسی، اختلال تعادل/حافظه) تغییر سطح هوشیاری (گیجی/خواب آلودگی) (۵۰ درصد)، تشنج/سردرد (نادر)
    question12: روانی (افسردگی، اضطراب، تغییر خلق، اختلال خواب) اضطراب شدید (مرگ قریب‌الوقوع) (۶۰ درصد)، اختلال خواب (۱۰۰ درصد)
    question13: غدد درون‌ریز (افزایش تشنگی/گرسنگی/ادرار، عدم تحمل گرما/سرما) افزایش تشنگی/گرسنگی/ادرار (نادر)، طبیعی (۱۰۰ درصد)
    question14: خون و لنفاوی (کبودی آسان، خونریزی طولانی، کم‌خونی شدید) اختلالات انعقادی (DIC) (۱۰ درصد)، لوکوسیتوز (۸۰ درصد)
"""

documents = [
    Document(page_content=PNEUMONIA_PROFILE_REF, metadata={"disease": "Pneumonia", "section": "patient_profile"}),
    Document(page_content=PNEUMONIA_HISTORY_REF, metadata={"disease": "Pneumonia", "section": "history_taking"}),
    Document(page_content=COPD_PROFILE_REF, metadata={"disease": "COPD", "section": "patient_profile"}),
    Document(page_content=COPD_HISTORY_REF, metadata={"disease": "COPD", "section": "history_taking"}),
    Document(page_content=ASTHMA_BOUNDARIES_REF, metadata={"disease": "Asthma", "section": "BOUNDARIES"}),
    Document(page_content=ASTHMA_VARIABILITY_REF, metadata={"disease": "Asthma", "section": "VARIABILITY"}),
    Document(page_content=ASTHMA_HISTORY_REF, metadata={"disease": "Asthma", "section": "HISTORY"}),
    Document(page_content=ASTHMA_CONSTRaAINTS_REF, metadata={"disease": "Asthma", "section": "CONSTRaAINTS"}),
    Document(page_content=ASTHMA_OUTPUT_REF, metadata={"disease": "Asthma", "section": "OUTPUT"}),
    Document(page_content=ASTHMA_JSON_REF, metadata={"disease": "Asthma", "section": "JSON"}),
    Document(page_content=PTE_PROFILE_REF, metadata={"disease": "PTE", "section": "patient_profile"}),
    Document(page_content=PTE_HISTORY_REF, metadata={"disease": "PTE", "section": "history_taking"}),
    Document(page_content=IPF_PROFILE_REF, metadata={"disease": "IPF", "section": "patient_profile"}),
    Document(page_content=IPF_HISTORY_REF, metadata={"disease": "IPF", "section": "history_taking"}),
    Document(page_content=PH_PROFILE_REF, metadata={"disease": "PH", "section": "patient_profile"}),
    Document(page_content=PH_HISTORY_REF, metadata={"disease": "PH", "section": "history_taking"}),
    Document(page_content=ARDS_PROFILE_REF, metadata={"disease": "ARDS", "section": "patient_profile"}),
    Document(page_content=ARDS_HISTORY_REF, metadata={"disease": "ARDS", "section": "history_taking"}),
]