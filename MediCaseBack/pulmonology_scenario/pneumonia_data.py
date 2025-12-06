import random
import re
import json

class PneumoniaDataGenerator:
    """
    کلاسی برای تولید داده‌های شبیه‌سازی شده پنومونی.
    اصلاح شده بر اساس قواعد آماری دقیق فایل متنی 'معاینات فیزیکی'.
    """
    
    RANDOM_DATA_LISTS = {
        "first_names_sample_100": {
            "MALE": [
                "محمد", "علی", "رضا", "حسین", "امیر", "مهدی", "سجاد", "آریا", "کیان", "پویا",
                "محسن", "جواد", "مجید", "بهنام", "فرهاد", "کوروش", "فرزاد", "سامان", "سعید", "یوسف",
                "اشکان", "داریوش", "کسری", "هومن", "آرمین", "مانی", "پارسا", "میلاد", "یاسر", "ناصر",
                "احمد", "جمال", "وحید", "مازیار", "حامد", "سینا", "عرفان", "شهرام", "مرتضی", "مصطفی",
                "بهرام", "کامران", "شایان", "فرشید", "پیمان", "الیاس", "آرش", "نوید", "ناصر", "نادر"
            ],
            "FEMALE": [
                "فاطمه", "زهرا", "مریم", "سارا", "آزاده", "نگار", "لیلا", "نازنین", "مهسا", "زینب",
                "الناز", "آتوسا", "پریسا", "نسترن", "شبنم", "فریبا", "سودابه", "ژاله", "آرزو", "مهناز",
                "رویا", "محبوبه", "نسرین", "آیلین", "پگاه", "عاطفه", "حدیث", "میترا", "درسا", "هانیه",
                "شکیبا", "سوگل", "مرجان", "بهاره", "مینو", "کتایون", "شیوا", "پریا", "سایه", "مهتاب",
                "روژان", "طناز", "سما", "سپیده", "الهام", "ریحانه", "دنیا", "هما", "فروزان", "مینا"
            ]
        },
        "last_names_sample_100": [
            "محمدی", "احمدی", "کریمی", "حسینی", "رضایی", "موسوی", "فرهادی", "هاشمی", "نوری", "زارعی",
            "باقری", "صادقی", "میرزایی", "جلیلی", "افشار", "نجفی", "سلیمانی", "شریفی", "قاسمی", "ملکی",
            "رحمتی", "یزدانی", "کمالی", "طاهری", "دهقان", "اکبری", "شفیعی", "کاظمی", "فلاح", "مرادی",
            "عباسی", "یاراحمدی", "مهاجر", "نعمتی", "حیدری", "لطفی", "آذری", "صفری", "خسروی", "پورحسن",
            "نیک‌نظر", "جهانی", "اسدی", "حبیبی", "خدایی", "عزیزی", "شهبازی", "ابراهیمی", "بیاتی", "بختیاری",
            "فتاحی", "توسلی", "مجیدی", "خانی", "شهریاری", "جهانگیری", "سپاهی", "امیری", "مظفری", "اسماعیلی",
            "سادات", "بابایی", "پناهی", "عطایی", "کیانی", "شعبانی", "یوسفی", "گلستانه", "سجادی", "فدایی",
            "عالم", "دانشمند", "صالحی", "جمشیدی", "میرداماد", "صمدی", "عمرانی", "فرهمند", "آزاد", "نیکو"
        ],
        "occupations_male": [
            "راننده تاکسی", "مهندس نرم‌افزار", "کارمند بانک", "کارگر ساده", "نقاش ساختمان",
            "تکنسین برق", "پزشک عمومی", "فروشنده بازار", "وکیل", "معمار", "استاد دانشگاه"
        ],
        "occupations_female": [
            "خانه‌دار", "معلم بازنشسته", "پرستار", "آرایشگر", "حسابدار شرکت خصوصی",
            "پزشک عمومی", "فروشنده بازار", "وکیل", "خیاط", "استاد دانشگاه"
        ],
        "occupations_retirement": [
            "معلم بازنشسته", "بازنشسته نیروهای مسلح", "بازنشسته تأمین اجتماعی"
        ],
        "famous_cities_sample_30": [
            "تهران", "مشهد", "اصفهان", "شیراز", "تبریز", "اهواز", "کرج", "قم", "کرمان", "یزد",
            "رشت", "ساری", "بندرعباس", "کرمانشاه", "ارومیه", "زاهدان", "همدان", "قزوین", "اردبیل", "زنجان",
            "گرگان", "سنندج", "بیرجند", "بوشهر", "سمنان", "خرم‌آباد", "ایلام", "یاسوج", "شهرکرد", "سیرجان"
        ],
        "city_proximity": {
            "تهران": ["کرج", "قم", "قزوین", "سمنان", "همدان"],
            "مشهد": ["بیرجند", "سمنان"],
            "اصفهان": ["شیراز", "قم", "یزد", "شهرکرد", "همدان"],
            "شیراز": ["اصفهان", "بوشهر", "یاسوج"],
            "تبریز": ["ارومیه", "زنجان", "اردبیل"],
            "اهواز": ["خرم‌آباد", "ایلام", "بوشهر"],
            "کرج": ["تهران", "قزوین", "سمنان"],
            "قم": ["تهران", "اصفهان", "سمنان"],
            "کرمان": ["یزد", "زاهدان", "سیرجان"],
            "یزد": ["کرمان", "اصفهان"],
            "رشت": ["ساری", "قزوین", "زنجان"],
            "ساری": ["رشت", "گرگان"],
            "بندرعباس": ["کرمان", "زاهدان"],
            "کرمانشاه": ["همدان", "ایلام", "سنندج"],
            "ارومیه": ["تبریز", "سنندج"],
            "زاهدان": ["کرمان", "بیرجند"],
            "همدان": ["کرمانشاه", "قزوین", "زنجان"],
            "قزوین": ["تهران", "زنجان", "رشت"],
            "اردبیل": ["تبریز"],
            "زنجان": ["تبریز", "قزوین", "همدان"],
            "گرگان": ["ساری"],
            "سنندج": ["کرمانشاه", "ارومیه"],
            "بیرجند": ["مشهد", "زاهدان"],
            "بوشهر": ["شیراز", "اهواز"],
            "سمنان": ["تهران", "مشهد"],
            "خرم‌آباد": ["اهواز", "ایلام"],
            "ایلام": ["کرمانشاه", "خرم‌آباد"],
            "یاسوج": ["شیراز", "شهرکرد"],
            "شهرکرد": ["اصفهان", "یاسوج"],
            "سیرجان": ["کرمان"]
        }
    }
    
    def __init__(self):
        self.random = random
        # دیگر نیازی به self.case_type یا severity_level برای تعیین منطق نیست
        # زیرا منطق دقیقا بر اساس درصدهای فایل متنی پیاده می‌شود.

    # --- Demographic Helpers ---
    def _select_occupation(self, gender, age_str):
        age = int(age_str.split()[0])
        if age > 65: return self.random.choice(self.RANDOM_DATA_LISTS["occupations_retirement"])
        if 55 <= age <= 65:
            return self.random.choice(self.RANDOM_DATA_LISTS["occupations_retirement"]) if self.random.random() < 0.5 else (self.random.choice(self.RANDOM_DATA_LISTS["occupations_male"]) if gender == "مرد" else self.random.choice(self.RANDOM_DATA_LISTS["occupations_female"]))
        return self.random.choice(self.RANDOM_DATA_LISTS["occupations_male"]) if gender == "مرد" else self.random.choice(self.RANDOM_DATA_LISTS["occupations_female"])

    def _select_place_of_residence(self, place_of_birth):
        if self.random.random() < 0.7:
            nearby_cities = self.RANDOM_DATA_LISTS["city_proximity"].get(place_of_birth, [])
            if nearby_cities: return self.random.choice(nearby_cities)
        return self.random.choice(self.RANDOM_DATA_LISTS["famous_cities_sample_30"])

    def _select_marital_status(self, gender, age_str):
        age = int(age_str.split()[0])
        prob_married = 0
        if gender == "مرد": prob_married = 0.8 if age >= 45 else 0.5
        elif gender == "زن": prob_married = 0.9 if age >= 35 else 0.6
        return self.random.choices(["متأهل", "همسر متوفی"], weights=[90, 10], k=1)[0] if self.random.random() < prob_married else self.random.choices(["مجرد", "مطلقه"], weights=[70, 30], k=1)[0]

    def _generate_personal_information(self):
        gender = self.random.choice(["مرد", "زن"])
        age_num = self.random.randint(40, 75)
        age_str = f"{age_num} ساله"
        name_key = "MALE" if gender == "مرد" else "FEMALE"
        return {
            "first_name": self.random.choice(self.RANDOM_DATA_LISTS["first_names_sample_100"][name_key]),
            "last_name": self.random.choice(self.RANDOM_DATA_LISTS["last_names_sample_100"]),
            "age": age_str, "gender": gender,
            "occupation": self._select_occupation(gender, age_str),
            "place_of_birth": (birth := self.random.choice(self.RANDOM_DATA_LISTS["famous_cities_sample_30"])),
            "place_of_residence": self._select_place_of_residence(birth),
            "marital_status": self._select_marital_status(gender, age_str)
        }

    def _generate_value(self, distributions, is_int=False, precision=2):
        ranges = [d["range"] for d in distributions]
        weights = [d["weight"] for d in distributions]
        chosen_range = self.random.choices(ranges, weights=weights, k=1)[0]
        if is_int: return str(self.random.randint(chosen_range[0], chosen_range[1]))
        return str(round(self.random.uniform(chosen_range[0], chosen_range[1]), precision))

    # ==========================================
    # 1. PHYSICAL EXAM - VITAL SIGNS (RULES APPLIED)
    # ==========================================
    def _gen_vital_bp(self):
        # 20% <90, 60% 90-140, 20% >140
        scenario = self.random.choices(["Hypotension", "Normal", "Hypertension"], weights=[20, 60, 20])[0]
        if scenario == "Hypotension":
            sys = self.random.randint(70, 89)
            dia = self.random.randint(40, 59)
        elif scenario == "Normal":
            sys = self.random.randint(90, 140)
            dia = self.random.randint(60, 90)
        else: # Hypertension
            sys = self.random.randint(141, 180)
            dia = self.random.randint(91, 110)
        return f"{sys}/{dia} mmHg"

    def _gen_vital_temp(self):
        # 75% > 38.0, 25% < 37.5
        scenario = self.random.choices(["Fever", "Normal/Low"], weights=[75, 25])[0]
        if scenario == "Fever":
            return f"{round(self.random.uniform(38.1, 40.0), 1)} C"
        else:
            return f"{round(self.random.uniform(36.0, 37.4), 1)} C"

    def _gen_vital_pr(self):
        # 80% > 100, 20% 60-100
        scenario = self.random.choices(["Tachycardia", "Normal"], weights=[80, 20])[0]
        if scenario == "Tachycardia":
            val = self.random.randint(101, 130)
        else:
            val = self.random.randint(60, 100)
        return f"{val} bpm"

    def _gen_vital_rr(self):
        # 85% > 20, 15% 12-20
        scenario = self.random.choices(["Tachypnea", "Normal"], weights=[85, 15])[0]
        if scenario == "Tachypnea":
            val = self.random.randint(21, 35)
        else:
            val = self.random.randint(12, 20)
        return f"{val} breaths/min"

    def _gen_vital_spo2(self):
        # 60% < 94, 40% >= 94
        scenario = self.random.choices(["Hypoxemia", "Normal"], weights=[60, 40])[0]
        if scenario == "Hypoxemia":
            val = self.random.randint(85, 93)
        else:
            val = self.random.randint(94, 99)
        return f"{val}% on Room Air"

    def _gen_vital_gcs(self):
        # 80% 15/15, 20% < 15
        scenario = self.random.choices(["Normal", "Confusion"], weights=[80, 20])[0]
        if scenario == "Normal":
            return "15/15"
        else:
            return str(self.random.randint(13, 14))

    # ==========================================
    # 2. PHYSICAL EXAM - GENERAL APPEARANCE
    # ==========================================
    def _gen_ga_mood(self):
        # 40% Anxious, 20% Lethargic, 40% Calm
        return self.random.choices(
            ["Anxious due to dyspnea", "Lethargic (Severe infection)", "Calm"],
            weights=[40, 20, 40]
        )[0]

    def _gen_ga_overall(self):
        # 60% Ill-appearing, 30% Mild distress, 10% Comfortable
        return self.random.choices(
            ["Ill-appearing/Toxic", "Mildly distressed", "Comfortable, No acute distress"],
            weights=[60, 30, 10]
        )[0]

    def _gen_ga_posture(self):
        # 30% Splinting, 20% Tripod, 50% No specific
        return self.random.choices(
            ["Splinting (lying on affected side)", "Tripod position", "Supine/No specific preference"],
            weights=[30, 20, 50]
        )[0]

    def _gen_ga_loc(self):
        # 80% Alert, 20% Confused
        return self.random.choices(
            ["Alert and Oriented", "Confused (Sepsis/Hypoxia)"],
            weights=[80, 20]
        )[0]
    
    def _gen_ga_clues(self):
        # Edema: 100% No
        edema = "No peripheral edema"
        # Dyspnea: 80% Visible, 20% Absent
        dyspnea = self.random.choices(["Visible dyspnea present", "No visible dyspnea"], weights=[80, 20])[0]
        # Cyanosis: 15% Central, 85% Absent
        cyanosis = self.random.choices(["Central Cyanosis present", "Absent"], weights=[15, 85])[0]
        return {"edema": edema, "dyspnea": dyspnea, "cyanosis": cyanosis}

    # ==========================================
    # 3. PHYSICAL EXAM - HEAD AND NECK
    # ==========================================
    def _gen_hn_ears(self):
        # 95% Normal, 5% Bullous
        return self.random.choices(
            ["Normal appearance", "Bullous Myringitis (Bullous lesions)"],
            weights=[95, 5]
        )[0]

    def _gen_hn_nose(self):
        # 40% Nasal flaring, 60% Normal
        return self.random.choices(
            ["Nasal flaring present", "Normal, no flaring"],
            weights=[40, 60]
        )[0]

    def _gen_hn_mouth(self):
        # 50% Dry, 50% Moist
        return self.random.choices(
            ["Dry mucous membranes (Dehydration)", "Moist mucous membranes"],
            weights=[50, 50]
        )[0]

    def _gen_hn_lymph(self):
        # 90% Normal, 10% Reactive
        return self.random.choices(
            ["No lymphadenopathy", "Mild cervical lymphadenopathy (Reactive)"],
            weights=[90, 10]
        )[0]

    # ==========================================
    # 4. PHYSICAL EXAM - RESPIRATORY SYSTEM
    # ==========================================
    def _gen_resp_inspection(self):
        # Accessory: 50% Present, 50% Normal
        acc = self.random.choices(["Accessory muscle use present", "No accessory muscle use"], weights=[50, 50])[0]
        # Chest Shape: 30% Splinting/Lag, 70% Normal
        shape = self.random.choices(["Asymmetrical movement (Lag on affected side)", "Symmetrical movement"], weights=[30, 70])[0]
        return {"accessory_muscles": acc, "chest_shape_and_symmetry": shape}

    def _gen_resp_palpation(self):
        # Expansion: 40% Reduced, 60% Normal
        exp = self.random.choices(["Reduced expansion on affected side", "Symmetrical expansion"], weights=[40, 60])[0]
        # Fremitus: 70% Increased, 30% Normal
        frem = self.random.choices(["Increased tactile fremitus over consolidation", "Normal tactile fremitus"], weights=[70, 30])[0]
        return {"chest_expansion": exp, "tactile_fremitus": frem}

    def _gen_resp_percussion(self):
        # 75% Dullness, 25% Resonant
        return self.random.choices(["Dullness to percussion", "Resonant"], weights=[75, 25])[0]

    def _gen_resp_auscultation(self):
        # Breath Sounds: 60% Bronchial, 40% Vesicular
        bs = self.random.choices(["Bronchial breath sounds", "Vesicular breath sounds (Normal)"], weights=[60, 40])[0]
        # Adventitious: 70% Crackles, 15% Rhonchi, 10% Egophony, 5% Clear
        adv = self.random.choices(
            ["Localized crackles (Rales)", "Rhonchi", "Egophony (E to A change)", "Clear"],
            weights=[70, 15, 10, 5]
        )[0]
        return {"breath_sounds": bs, "adventitious_sounds": adv}

    # ==========================================
    # 5. PHYSICAL EXAM - CARDIOVASCULAR
    # ==========================================
    def _gen_cv_auscultation(self):
        # Heart Sounds: 70% Tachycardia, 30% Normal
        hs = self.random.choices(["Tachycardic S1, S2", "Normal rate and rhythm"], weights=[70, 30])[0]
        # Murmurs: 100% None
        mur = "No murmurs"
        return {"heart_sounds_s1_s2": hs, "murmurs": mur}

    def _gen_cv_peripheral(self):
        # Pulses: 40% Bounding, 60% Normal
        pulses = self.random.choices(["Bounding pulses", "Normal quality"], weights=[40, 60])[0]
        # Temp: 60% Warm, 40% Normal
        temp = self.random.choices(["Extremities Warm (Fever)", "Extremities Normal"], weights=[60, 40])[0]
        return {
            "peripheral_pulses_symmetry_and_quality": pulses,
            "extremities_color_and_trophic_changes": "Normal", # 100%
            "extremities_temperature_and_cap_refill": temp,
            "extremities_edema": "No edema" # 100%
        }

    # ==========================================
    # 6. PHYSICAL EXAM - ABDOMINAL
    # ==========================================
    def _gen_abd_all(self):
        # Bowel Sounds: 90% Normal, 10% Hypoactive
        bs = self.random.choices(["Normal bowel sounds", "Hypoactive bowel sounds"], weights=[90, 10])[0]
        # Tenderness: 10% Upper abd (Referred), 90% Non-tender
        tend = self.random.choices(["Upper abdominal tenderness (Referred)", "Non-tender"], weights=[10, 90])[0]
        
        return {
            "inspection": "Flat/Normal", # 100%
            "auscultation": {
                "bowel_sounds": bs,
                "vascular_bruits": "No bruits" # 100%
            },
            "percussion": {
                "general": "Tympanic", # 100%
                "organ_borders": "Normal" # 100%
            },
            "palpation": {
                "superficial_tenderness": tend,
                "deep_masses_and_organs": "No masses" # 100%
            },
            "peritoneal_signs": "Absent" # 100%
        }

    # ==========================================
    # 7. PHYSICAL EXAM - NEURO & MSK
    # ==========================================
    def _gen_neuro_status(self):
        # 25% Confusion, 75% Normal
        ms = self.random.choices(["Confusion/Delirium", "Normal"], weights=[25, 75])[0]
        return {
            "mental_status_and_LOC": ms,
            "cranial_nerves": "Intact", # 100%
            "motor_strength_and_tone": "Normal", # 100%
            "involuntary_movements": "None", # 100%
            "sensory_light_touch_and_pain": "Intact", # 100%
            "deep_tendon_reflexes": "Normal", # 100%
            "coordination_and_gait": "Normal" # 100%
        }

    def _gen_msk_all(self):
        # All 100% Normal according to file
        return {
            "inspection": {"joints": "Normal", "muscles": "Normal"},
            "palpation": {"tenderness_and_crepitus": "Non-tender"},
            "range_of_motion_active_passive": "Normal",
            "stability_and_function": "Normal"
        }

    # ==========================================
    # 8. PARACLINIC (PRESERVED & INTEGRATED)
    # ==========================================
    # ... Helper generators for paraclinic ...
    def _generate_hemoglobin_value(self):
        dists = [{"range": (12.0, 16.0), "weight": 50}, {"range": (10.0, 12.0), "weight": 30}, {"range": (7.0, 9.9), "weight": 20}]
        return f"{self._generate_value(dists, precision=1)} g/dL"
    def _generate_wbc_count(self): 
        dists = [{"range": (12000, 25000), "weight": 70}, {"range": (4000, 12000), "weight": 20}, {"range": (2000, 3999), "weight": 10}]
        return f"{self._generate_value(dists, is_int=True)} /µL"
    def _generate_platelet_count(self): 
        dists = [{"range": (150000, 450000), "weight": 60}, {"range": (450001, 600000), "weight": 30}, {"range": (50000, 149000), "weight": 10}]
        return f"{self._generate_value(dists, is_int=True)} /µL"
    def _generate_esr_value(self): 
        dists = [{"range": (51, 120), "weight": 50}, {"range": (20, 50), "weight": 30}, {"range": (5, 19), "weight": 20}]
        return f"{self._generate_value(dists, is_int=True)} mm/h"
    def _generate_crp_value(self): 
        dists = [{"range": (101, 200), "weight": 65}, {"range": (20, 100), "weight": 25}, {"range": (1, 19), "weight": 10}]
        return f"{self._generate_value(dists, is_int=True)} mg/L"
    def _gen_na(self):
        dists = [{"range": (135, 145), "weight": 85}, {"range": (125, 134), "weight": 15}]
        return f"{self._generate_value(dists, is_int=True)} mEq/L"
    def _gen_bun(self):
        dists = [{"range": (7, 20), "weight": 75}, {"range": (21, 50), "weight": 25}]
        return f"{self._generate_value(dists, is_int=True)} mg/dL"
    def _gen_cr(self):
        dists = [{"range": (0.7, 1.2), "weight": 75}, {"range": (1.3, 2.5), "weight": 25}]
        return f"{self._generate_value(dists, precision=2)} mg/dL"
    def _gen_liver(self):
        dists = [{"range": (22, 45), "weight": 80}, {"range": (46, 90), "weight": 20}]
        val = self._generate_value(dists, is_int=True)
        return f"{val} U/L"
    def _gen_ph(self):
        dists = [{"range": (7.35, 7.45), "weight": 80}, {"range": (7.46, 7.55), "weight": 15}, {"range": (7.25, 7.34), "weight": 5}]
        return self._generate_value(dists, precision=2)
    def _gen_gram_stain(self):
        return self.random.choices(["Positive for specific organism", "Normal Flora / Mixed", "No Organism seen"], weights=[50, 30, 20], k=1)[0]
    def _gen_sample_quality(self):
        return self.random.choices(["Good Quality (>25 PMNs, <10 Epithelial cells)", "Poor Quality"], weights=[70, 30], k=1)[0]
    def _gen_afb(self):
        return self.random.choices(["Negative", "Positive"], weights=[95, 5], k=1)[0]
    def _gen_a1at(self):
        return self.random.choices(["within normal range", "below normal range"], weights=[99, 1], k=1)[0]
    def _gen_ddimer(self):
        dists = [{"range": (501, 2000), "weight": 60}, {"range": (100, 500), "weight": 40}]
        return f"{self._generate_value(dists, is_int=True)} ng/mL FEU"
    def _gen_bnp(self):
        return self.random.choices(["within normal range", "mildly elevated"], weights=[80, 20], k=1)[0]
    def _gen_hiv(self): return self.random.choices(["Negative", "Positive"], weights=[98, 2], k=1)[0]
    def _gen_autoimmune(self): return self.random.choices(["Negative", "Positive"], weights=[95, 5], k=1)[0]
    def _gen_mri(self): return self.random.choices(["Normal", "Abnormal signal intensity"], weights=[95, 5], k=1)[0]
    def _gen_pet(self): return self.random.choices(["Increased metabolic activity in affected area", "Normal metabolic activity"], weights=[90, 10], k=1)[0]
    def _gen_spirometry(self):
        opts = [
            "Not Indicated or Unable to perform",
            "FEV1 Measured 55-70% Predicted, FVC Measured 50-65% Predicted, FEV1/FVC Measured 85-110% Predicted",
            "FEV1 Measured 85-110% Predicted, FVC Measured 85-110% Predicted, FEV1/FVC Measured 80-110% Predicted"
        ]
        return self.random.choices(opts, weights=[60, 30, 10], k=1)[0]
    def _gen_peak(self): return self.random.choices(["within normal range", "reduced"], weights=[50, 50], k=1)[0]
    def _gen_pleth(self): return self.random.choices(["within normal range", "reduced Lung Volumes"], weights=[90, 10], k=1)[0]
    def _gen_bronch(self): return self.random.choices(["Normal Anatomy with Secretions", "Mucosal Inflammation or Obstruction"], weights=[90, 10], k=1)[0]
    
    def _gen_cxr(self):
        # Using simplified logic consistent with previous version but generalized
        return self.random.choice(["Lobar Consolidation", "Patchy Infiltrates", "Pleural Effusion present"])

    def _gen_ct(self):
        return "Consolidation or Infiltrates confirmed"

    def _gen_thora(self):
        # 30% chance of successful tap if effusion present (simplified for this context)
        if self.random.random() < 0.3:
            return "Fluid Aspirated: Exudative criteria met."
        return "Not Indicated"

    def _get_dlco_finding(self):
        findings = ["Reduced", "Normal"]
        weights = [70, 30]
        chosen_status = self.random.choices(findings, weights=weights, k=1)[0]
        if chosen_status == "Reduced": dlco_val = self.random.randint(40, 79)
        else: dlco_val = self.random.randint(80, 100)
        return chosen_status, f"{dlco_val}% predicted"

    def _gen_reversibility(self):
        choice = self.random.choices(["Positive", "Negative"], weights=[5, 95], k=1)[0]
        if choice == "Positive": return "FEV1 increase > 12% AND > 200 mL"
        return "FEV1 increase < 12% AND < 200 mL"

    # --- VBG Logic (Added in previous step) ---
    def _gen_pco2_logic(self):
        scenario = self.random.choices(["Hypocapnia", "Normal", "Hypercapnia"], weights=[60, 30, 10], k=1)[0]
        if scenario == "Hypocapnia": val = self.random.randint(25, 34)
        elif scenario == "Normal": val = self.random.randint(35, 45)
        else: val = self.random.randint(46, 60)
        return f"{val} mmHg"

    def _gen_hco3_logic(self):
        scenario = self.random.choices(["Normal", "Low"], weights=[80, 20], k=1)[0]
        if scenario == "Normal": val = self.random.randint(22, 26)
        else: val = self.random.randint(15, 21)
        return f"{val} mEq/L"

    # ==========================================
    # MAIN GENERATION METHOD
    # ==========================================
    def generate_paraclinic_case(self):
        
        # 1. Personal Info
        personal_info = self._generate_personal_information()
        
        # 2. Vital Signs (Rules Applied)
        vitals = {
            "BP": self._gen_vital_bp(),
            "T": self._gen_vital_temp(),
            "PR": self._gen_vital_pr(),
            "RR": self._gen_vital_rr(),
            "SpO2": self._gen_vital_spo2(),
            "GCS": self._gen_vital_gcs()
        }
        
        # 3. General Appearance
        ga_clues = self._gen_ga_clues()
        general_appearance = {
            "level_of_consciousness": self._gen_ga_loc(),
            "mood_and_behavior": self._gen_ga_mood(),
            "posture_and_position": self._gen_ga_posture(),
            "overall_appearance": self._gen_ga_overall(),
            "cardiopulmonary_and_circulatory_clues": ga_clues
        }
        
        # 4. Head and Neck
        head_neck = {
            "head_and_face": {"symmetry_and_lesions": "Normal", "tenderness": "Non-tender"},
            "eyes": {"sclera_and_conjunctiva": "Normal", "pupils_reaction": "PERRLA", "extraocular_movements": "Intact"},
            "ears": {"external_and_tenderness": "Normal", "eardrum_appearance": self._gen_hn_ears()},
            "nose_and_sinuses": {"septum_and_discharge": self._gen_hn_nose(), "sinus_tenderness": "Non-tender"},
            "mouth_and_pharynx": {"oral_mucosa_and_lesions": self._gen_hn_mouth(), "pharynx_and_tonsils": "Normal"},
            "neck_and_lymphatics": {
                "inspection": "Normal", "tracheal_position": "Central", "thyroid_gland": "Non-palpable",
                "carotid_bruit": "No bruits", "lymph_nodes_size_consistency": self._gen_hn_lymph(),
                "lymph_nodes_mobility_tenderness": "N/A"
            }
        }
        
        # 5. Respiratory
        respiratory = {
            "inspection": self._gen_resp_inspection(),
            "palpation": self._gen_resp_palpation(),
            "percussion": self._gen_resp_percussion(),
            "auscultation": self._gen_resp_auscultation()
        }
        
        # 6. Cardiovascular
        cardio = {
            "JVP_assessment": "Normal JVP",
            "palpation": {"precordial_palpation_heave_thrill": "No heaves or thrills", "pmi_assessment": "Normal location"},
            "auscultation": self._gen_cv_auscultation(),
            "peripheral_pulses_and_extremities": self._gen_cv_peripheral()
        }
        
        # 7. Abdominal
        abdominal = self._gen_abd_all()
        
        # 8. Neuro & MSK
        neuro = self._gen_neuro_status()
        msk = self._gen_msk_all()

        # 9. Paraclinic Data Assembly
        data = {
            "patient_profile": {
                "personal_information": personal_info
            },
            "physical_exam": {
                "vital_signs": vitals,
                "general_appearance": general_appearance,
                "head_and_neck": head_neck,
                "respiratory_system": respiratory,
                "cardiovascular_system": cardio,
                "abdominal_system": abdominal,
                "neurological": neuro,
                "musculoskeletal_system": msk
            },
            "paraclinic": {
                "basic_blood_tests": {
                    "CBC": {
                        "Hb": self._generate_hemoglobin_value(),
                        "WBC": self._generate_wbc_count(),
                        "Plt": self._generate_platelet_count()
                    },
                    "ESR": self._generate_esr_value(),
                    "CRP": self._generate_crp_value(),
                    "BMP": {
                        "Na": self._gen_na(), "BUN": self._gen_bun(), "Cr": self._gen_cr()
                    },
                    "LFTs": {
                        "ALT": self._gen_liver(), "AST": self._gen_liver()
                    },
                    "VBG": {
                        "pH": self._gen_ph(),
                        "PCO2": self._gen_pco2_logic(),
                        "HCO3": self._gen_hco3_logic()
                    }
                },
                "specialized_lung_tests": {
                    "Sputum_analysis": {
                        "Gram_Stain": self._gen_gram_stain(), "Sample_Quality": self._gen_sample_quality()
                    },
                    "Sputum_AFB": self._gen_afb(),
                    "a1_antitrypsin_level": self._gen_a1at(),
                    "D_dimer": self._gen_ddimer(),
                    "BNP_NT_proBNP": self._gen_bnp()
                },
                "immunity_and_serology": {
                    "HIV_test": self._gen_hiv(), "Autoimmune_pannel_ANA_ANCA": self._gen_autoimmune()
                },
                "simple_imaging": {
                    "Chest_X_Ray": {"PA_Lateral_Findings_and_Effusion": self._gen_cxr()}
                },
                "advanced_imaging": {
                    "Chest_CT_CTPA": {"Lung_Parenchyma_and_Pleura": self._gen_ct()},
                    "MRI_chest": self._gen_mri(), "Pet_scan": self._gen_pet()
                },
                "functional_tests": {
                    "Spirometry": {"result": self._gen_spirometry(), "reversibility": self._gen_reversibility()},
                    "dlco": self._get_dlco_finding()[1],
                    "peak_flow": self._gen_peak(), "plethysmography": self._gen_pleth()
                },
                "procedures": {
                    "Bronchoscopy": self._gen_bronch(), "torachonthesis": self._gen_thora()
                }
            }
        }
        return data
