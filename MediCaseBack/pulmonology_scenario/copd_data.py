import random
import re
from .history_taking_creator import history_taking_creator

class COPDDataGenerator:
    """
    کلاسی برای تولید داده‌های شبیه‌سازی شده COPD.
    
    Logic Drivers (سه متغیر اصلی):
    1. PHENOTYPE: Emphysema vs Chronic Bronchitis
    2. SEVERITY: GOLD 1 (Mild) to GOLD 4 (Very Severe)
    3. COR_PULMONALE: Present vs Absent
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
            "راننده تاکسی", "مهندس نرم‌افزار", "کارمند بازنشسته", "کارگر ساختمانی", "نقاش ساختمان",
            "تکنسین برق", "کشاورز", "فروشنده بازار", "وکیل", "معمار", "استاد دانشگاه"
        ],
        "occupations_female": [
            "خانه‌دار", "معلم بازنشسته", "پرستار", "خیاط", "حسابدار",
            "پزشک عمومی", "فروشنده", "کارمند اداری", "استاد دانشگاه"
        ],
        "occupations_retirement": [
            "معلم بازنشسته", "بازنشسته نیروهای مسلح", "بازنشسته تأمین اجتماعی", "بازنشسته شرکت نفت"
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
        
        # 1. CORE LOGIC INITIALIZATION
        # Phenotype Distribution: Emphysema (60%) vs Chronic Bronchitis (40%)
        self.phenotype = self.random.choices(
            ["Emphysema", "Chronic Bronchitis"], 
            weights=[60, 40], k=1
        )[0]
        
        # Severity Distribution: Mild(10%), Moderate(40%), Severe(30%), Very Severe(20%)
        self.severity = self.random.choices(
            ["GOLD_1", "GOLD_2", "GOLD_3", "GOLD_4"],
            weights=[10, 40, 30, 20], k=1
        )[0]
        
        # Cor Pulmonale Distribution: Present(30%) vs Absent(70%)
        self.cor_pulmonale = self.random.choices(
            ["Present", "Absent"],
            weights=[30, 70], k=1
        )[0]

        self.vital_signs = {} 

    # --- Demographic Helpers ---
    def _select_occupation(self, gender, age_str):
        age = int(age_str.split()[0])
        if age > 60:
            return self.random.choice(self.RANDOM_DATA_LISTS["occupations_retirement"])
        if gender == "مرد":
            return self.random.choice(self.RANDOM_DATA_LISTS["occupations_male"])
        return self.random.choice(self.RANDOM_DATA_LISTS["occupations_female"])

    def _select_place_of_residence(self, place_of_birth):
        if self.random.random() < 0.7:
            nearby = self.RANDOM_DATA_LISTS["city_proximity"].get(place_of_birth, [])
            if nearby: return self.random.choice(nearby)
        return self.random.choice(self.RANDOM_DATA_LISTS["famous_cities_sample_30"])

    def _generate_personal_information(self):
        gender = self.random.choice(["مرد", "زن"])
        # COPD usually presents in older adults
        age_num = self.random.randint(45, 85)
        age_str = f"{age_num} ساله"
        
        name_key = "MALE" if gender == "مرد" else "FEMALE"
        first_name = self.random.choice(self.RANDOM_DATA_LISTS["first_names_sample_100"][name_key])
        last_name = self.random.choice(self.RANDOM_DATA_LISTS["last_names_sample_100"])
        
        occupation = self._select_occupation(gender, age_str)
        birth = self.random.choice(self.RANDOM_DATA_LISTS["famous_cities_sample_30"])
        residence = self._select_place_of_residence(birth)
        marital = self.random.choices(["متأهل", "همسر متوفی", "مجرد"], weights=[70, 25, 5], k=1)[0]
        
        return {
            "first_name": first_name, "last_name": last_name, "age": age_str,
            "gender": gender, "occupation": occupation,
            "place_of_birth": birth, "place_of_residence": residence,
            "marital_status": marital
        }

    # --- Value Generators ---
    def _generate_value(self, distributions, is_int=False, precision=2):
        ranges = [d["range"] for d in distributions]
        weights = [d["weight"] for d in distributions]
        chosen_range = self.random.choices(ranges, weights=weights, k=1)[0]
        if is_int:
            val = self.random.randint(chosen_range[0], chosen_range[1])
            return str(val)
        val = self.random.uniform(chosen_range[0], chosen_range[1])
        return str(round(val, precision))

    # --- Vital Signs Logic ---
    def _generate_vitals(self):
        # BP: Normal/HTN (80%) vs Low Normal (20%)
        bp_weights = [80, 20]
        chosen_bp = self.random.choices(["Normal/HTN", "Low Normal"], weights=bp_weights, k=1)[0]
        if chosen_bp == "Normal/HTN":
            sys = self.random.randint(110, 150)
            dia = self.random.randint(70, 95)
        else:
            sys = self.random.randint(90, 109)
            dia = self.random.randint(60, 70)
        
        # Temp: Mostly normal
        t_weights = [95, 5]
        t_choice = self.random.choices(["Normal", "Low Grade"], weights=t_weights, k=1)[0]
        temp = round(self.random.uniform(36.5, 37.5), 1) if t_choice == "Normal" else round(self.random.uniform(37.6, 38.0), 1)

        # Pulse: Normal vs Mild Tachycardia
        pr_weights = [70, 30]
        pr_choice = self.random.choices(["Normal", "Tachycardia"], weights=pr_weights, k=1)[0]
        pr = self.random.randint(60, 100) if pr_choice == "Normal" else self.random.randint(101, 115)

        # RR (Respiratory Rate): Depends on SEVERITY
        if self.severity in ["GOLD_1"]:
            rr = self.random.randint(16, 18)
        elif self.severity in ["GOLD_2"]:
            rr = self.random.randint(18, 20)
        else: # GOLD_3, GOLD_4
            rr = self.random.randint(20, 24)

        # SpO2: Depends on SEVERITY
        # Rule: Hypoxemia (<=92%) aligns with GOLD 3/4
        if self.severity in ["GOLD_1", "GOLD_2"]:
            spo2 = self.random.randint(93, 98)
        else:
            # Higher chance of low SpO2 in severe disease
            if self.random.random() < 0.6: # 60% chance of hypoxemia in severe cases
                spo2 = self.random.randint(86, 92)
            else:
                spo2 = self.random.randint(92, 94)

        # GCS: Generally 15, unless GOLD 4 + Hypercapnia (drowsy)
        if self.severity == "GOLD_4" and self.random.random() < 0.25: # 5% total chance (25% of 20%)
            gcs = str(self.random.randint(13, 14))
        else:
            gcs = "15"

        return {
            "BP": f"{sys}/{dia} mmHg",
            "T": f"{temp} °C",
            "PR": f"{pr} bpm and regular rhythm",
            "RR": f"{rr} breaths/min",
            "SpO2": f"{spo2}% (RA)",
            "GCS": gcs
        }

    # --- Physical Exam Logic ---
    def _gen_general_appearance(self, gcs_val):
        # LOC
        if int(gcs_val) < 15:
            loc = "Drowsy but arousable, following simple commands."
        else:
            loc = "Alert and Oriented to Person, Place, and Time."
        
        # Mood
        mood = self.random.choices(
            ["Appears Chronically Ill, Not in acute distress.", "Anxious/Apprehensive (due to chronic dyspnea)."],
            weights=[80, 20]
        )[0]
        
        # Posture
        if self.severity == "GOLD_4":
             # Higher chance of Tripod in severe
             pos = self.random.choices(["Comfortable", "Upright", "Tripod"], weights=[40, 30, 30])[0]
        else:
             pos = "Comfortable in bed or seated."
        
        # Nutritional Status (PHENOTYPE RULE)
        if self.phenotype == "Emphysema":
            # Pink Puffer -> Thin
            nutrition = self.random.choices(["Cachectic (Low BMI)", "Normal"], weights=[70, 30])[0]
        else:
            # Blue Bloater -> Obese/Normal
            nutrition = self.random.choices(["Normal/Obese", "Obese"], weights=[60, 40])[0]

        # Cyanosis (SpO2 Rule)
        spo2_val = int(re.search(r'\d+', self.vital_signs["SpO2"]).group())
        if spo2_val < 92:
            cyanosis = "Central Cyanosis (Tongue/Lips) Present."
        else:
            cyanosis = "Absent."

        # Edema (COR PULMONALE Rule)
        if self.cor_pulmonale == "Present":
            edema = "Bilateral Pitting Edema (1+ to 3+)."
        else:
            edema = "Absent (No pedal/periorbital swelling)."
            
        return {
            "loc": loc, "mood": mood, "posture": pos, "nutrition": nutrition,
            "cyanosis": cyanosis, "edema": edema
        }

    def _gen_resp_exam(self):
        # Inspection
        barrel_chest = self.random.choices(["Symmetrical, Normal shape", "Barrel Chest"], weights=[60, 40])[0]
        accessory = "Present" if self.severity in ["GOLD_3", "GOLD_4"] else "Absent"
        
        # Palpation
        # Reduced expansion is bilateral in COPD
        expansion = self.random.choices(["Bilateral Reduced Expansion", "Symmetrical expansion"], weights=[85, 15])[0]
        fremitus = self.random.choices(["Decreased and Symmetrical", "Normal"], weights=[70, 30])[0]
        
        # Percussion
        percussion = self.random.choices(["Diffuse Hyperresonant", "Resonant"], weights=[90, 10])[0]
        
        # Auscultation
        # Breath Sounds: Emphysema -> Diminished
        if self.phenotype == "Emphysema":
            bs_intensity = self.random.choices(["Reduced intensity", "Normal Vesicular"], weights=[85, 15])[0]
        else:
            bs_intensity = self.random.choices(["Reduced intensity", "Normal Vesicular"], weights=[60, 40])[0]
        
        bs_desc = f"{bs_intensity} with Prolonged Expiration"
        
        # Adventitious:
        # Cor Pulmonale -> Crackles?
        adv_opts = []
        adv_weights = []
        
        # Base Wheeze probability
        adv_opts.append("Wheezing Diffuse (Expiratory)")
        adv_weights.append(50)
        
        if self.cor_pulmonale == "Present":
            adv_opts.append("Fine Crackles (Basilar)")
            adv_weights.append(10) # Added chance
            adv_opts.append("No Adventitious Sounds")
            adv_weights.append(40)
        else:
            adv_opts.append("No Adventitious Sounds")
            adv_weights.append(50)
            
        # Normalize weights if needed, random.choices handles it
        adventitious = self.random.choices(adv_opts, weights=adv_weights, k=1)[0]
        
        return {
            "barrel": barrel_chest, "accessory": accessory,
            "expansion": expansion, "fremitus": fremitus,
            "percussion": percussion, "bs": bs_desc, "adv": adventitious
        }

    def _gen_cv_exam(self):
        # JVP (Cor Pulmonale Rule)
        if self.cor_pulmonale == "Present":
            jvp = self.random.choices(["> 4 cm above sternal angle", "< 4 cm"], weights=[70, 30])[0]
            rv_heave = self.random.choices(["Right Ventricular Heave detected", "No heave"], weights=[30, 70])[0]
            murmur = self.random.choices(["Soft Systolic Murmur (TR) or S3", "No S3/S4 or Murmur"], weights=[30, 70])[0]
        else:
            jvp = "< 4 cm above sternal angle"
            rv_heave = "No heave, lift, or thrill detected."
            murmur = "No S3/S4 or Murmur."
            
        # Heart Sounds (Hyperinflation rule)
        hs = self.random.choices(["Muffled/Distant S1 and S2", "Normal S1 and S2"], weights=[70, 30])[0]
        
        return {"jvp": jvp, "heave": rv_heave, "murmur": murmur, "hs": hs}

    # --- Paraclinic Logic ---
    def _gen_cbc(self):
        # Polycythemia Rule: High only if Cor Pulmonale + Low SpO2 (Severe)
        spo2_val = int(re.search(r'\d+', self.vital_signs["SpO2"]).group())
        
        if self.cor_pulmonale == "Present" and spo2_val < 92:
            # High chance of Polycythemia
            hb = self._generate_value([{"range": (17.1, 19.0), "weight": 100}], precision=1) + " g/dL"
        else:
            hb = self._generate_value([{"range": (12.0, 16.5), "weight": 100}], precision=1) + " g/dL"

        wbc = self._generate_value([{"range": (4000, 12000), "weight": 90}, {"range": (12001, 14000), "weight": 10}], is_int=True)
        plt = self._generate_value([{"range": (150000, 450000), "weight": 70}, {"range": (450001, 550000), "weight": 30}], is_int=True)
        return {"Hb": hb, "WBC": f"{wbc} /µL", "Plt": f"{plt} /µL"}

    def _gen_vbg(self):
        # pH & PaO2 linked to Severity
        if self.severity == "GOLD_4":
            # Risk of Acidosis
            ph = self._generate_value([{"range": (7.32, 7.35), "weight": 25}, {"range": (7.35, 7.45), "weight": 75}], precision=2)
            pao2 = self._generate_value([{"range": (50, 60), "weight": 80}, {"range": (60, 70), "weight": 20}], is_int=True)
        elif self.severity == "GOLD_3":
             ph = self._generate_value([{"range": (7.35, 7.45), "weight": 100}], precision=2)
             pao2 = self._generate_value([{"range": (55, 65), "weight": 60}, {"range": (65, 80), "weight": 40}], is_int=True)
        else: # GOLD 1/2
             ph = self._generate_value([{"range": (7.38, 7.45), "weight": 100}], precision=2)
             pao2 = self._generate_value([{"range": (70, 90), "weight": 100}], is_int=True)
             
        return {"pH": ph, "PaO2": f"{pao2} mmHg"}

    def _gen_bnp(self):
        if self.cor_pulmonale == "Present":
            return "Elevated (>100 pg/mL)"
        return "Within normal range"

    def _gen_imaging(self):
        # CXR
        cxr_findings = ["Hyperinflation (Flat Diaphragms, Narrow Heart)"]
        if self.phenotype == "Emphysema" and self.random.random() < 0.3:
            cxr_findings.append("Bullae visible in upper lobes")
        
        # CT
        ct_findings = "Emphysema/Air Trapping Changes"
        if self.phenotype == "Chronic Bronchitis":
             ct_findings = "Bronchial Wall Thickening, Air Trapping"
             
        return {
            "cxr": f"{', '.join(cxr_findings)}. No Consolidation/Effusion.",
            "ct": ct_findings
        }

    def _gen_spirometry(self):
        # MUST BE OBSTRUCTIVE: FEV1/FVC < 0.70
        ratio = round(self.random.uniform(0.45, 0.68), 2)
        
        # FEV1 MUST MATCH GOLD STAGE
        if self.severity == "GOLD_1": # >= 80%
            pred_percent = self.random.randint(80, 95)
        elif self.severity == "GOLD_2": # 50-79%
            pred_percent = self.random.randint(50, 79)
        elif self.severity == "GOLD_3": # 30-49%
            pred_percent = self.random.randint(30, 49)
        else: # GOLD_4 < 30%
            pred_percent = self.random.randint(15, 29)
            
        # Mocking volumes
        predicted_fev1 = 3.0 # Approx
        measured_fev1 = round(predicted_fev1 * (pred_percent/100), 2)
        
        desc = (f"Obstructive Pattern (FEV1/FVC = {ratio}). "
                f"FEV1 Measured: {measured_fev1}L ({pred_percent}% Predicted). "
                f"Consistent with {self.severity}.")
                
        # DLCO Logic (Phenotype)
        if self.phenotype == "Emphysema":
            dlco = "Reduced DLCO (< 70% predicted)"
        else:
            dlco = "Normal DLCO"
            
        return {"spiro": desc, "dlco": dlco}

    def _gen_bmp(self):
        """
        تولید مقادیر پنل متابولیک پایه طبق 
        """
        # Sodium (Na): 85% Normal (135-145), 15% Hyponatremia (<135) 
        na_val = self._generate_value([
            {"range": (135, 145), "weight": 85}, 
            {"range": (128, 134), "weight": 15}
        ], is_int=True)

        # BUN: 80% Normal (7-20), 20% Elevated (>20) 
        bun_val = self._generate_value([
            {"range": (7, 20), "weight": 80}, 
            {"range": (21, 35), "weight": 20}
        ], is_int=True)

        # Creatinine (Cr): 80% Normal (0.7-1.2), 20% Elevated (>1.2) 
        cr_val = self._generate_value([
            {"range": (0.7, 1.2), "weight": 80}, 
            {"range": (1.3, 1.8), "weight": 20}
        ], precision=1)

        return {
            "Na": f"{na_val} mEq/L",
            "BUN": f"{bun_val} mg/dL",
            "Cr": f"{cr_val} mg/dL"
        }

    def _gen_lfts(self):
        """
        تولید تست‌های عملکرد کبد طبق 
        """
        # ALT & AST: 90% Normal (22-45), 10% Mildly Elevated (45-90)
        lft_dist = [{"range": (22, 45), "weight": 90}, {"range": (46, 90), "weight": 10}]
        
        alt = self._generate_value(lft_dist, is_int=True)
        ast = self._generate_value(lft_dist, is_int=True)
        
        return {"ALT": f"{alt} U/L", "AST": f"{ast} U/L"}

    def _gen_sputum_gram(self):
        """
        تولید نتیجه رنگ‌آمیزی گرم خلط طبق 
        """
        # 80% Normal Flora, 20% Positive (Colonization in chronic bronchitis)
        return self.random.choices(
            ["Normal Flora / Mixed", "Positive for specific organism (Colonization)"],
            weights=[80, 20], k=1
        )[0]

    def _gen_sputum_afb(self):
        """
        تولید نتیجه AFB خلط طبق 
        """
        # 95% Negative, 5% Positive (Comorbidity)
        return self.random.choices(["Negative", "Positive"], weights=[95, 5], k=1)[0]

    def _gen_a1at(self):
        """
        سطح آلفا-1 آنتی‌تریپسین طبق 
        """
        # 99% Normal, 1% Low (Genetic Cause)
        return self.random.choices(
            ["Within normal range", "Below normal range (Genetic variant suspicion)"],
            weights=[99, 1], k=1
        )[0]

    def _gen_ddimer(self):
        """
        تولید دی-دایمر طبق 
        """
        # 90% < 500 (Rule out PE), 10% > 500
        dist = [
            {"range": (200, 499), "weight": 90}, 
            {"range": (500, 1500), "weight": 10}
        ]
        val = self._generate_value(dist, is_int=True)
        return f"{val} ng/mL FEU"
    
    def _gen_head_neck(self):
        """
        تولید یافته‌های سر و گردن طبق 
        """
        # Eyes: 95% Pink, 5% Pale 
        conjunctiva = self.random.choices(
            ["Pink conjunctiva, Anicteric sclera", "Pale conjunctiva, Anicteric sclera"],
            weights=[95, 5], k=1
        )[0]

        # Carotid Bruit: 90% Absent, 10% Present 
        carotid = self.random.choices(
            ["No bruits", "Carotid bruit present"],
            weights=[90, 10], k=1
        )[0]

        # Lymph Nodes: 90% Non-palpable, 10% Small firm 
        lymph = self.random.choices(
            ["Non-palpable or small, soft nodes", "Small (<1 cm), firm nodes"],
            weights=[90, 10], k=1
        )[0]
        
        return {
            "eyes": {"sclera_and_conjunctiva": conjunctiva, "pupils": "PERRL", "eom": "EOM intact"},
            "neck": {
                "tracheal_position": "Midline", 
                "lymph_nodes": lymph, 
                "carotid": carotid,
                "thyroid": "Non-enlarged, non-tender"
            }
        }

    def _gen_peripheral_pulses(self):
        """
        تولید نبض‌های محیطی و پرفیوژن 
        """
        # Pulses: 70% Normal quality, 30% Tachycardic (>100) 
        # (Check PR from vitals to be consistent, usually >100 aligns with Tachycardic quality)
        pr_val = int(re.search(r'\d+', self.vital_signs["PR"]).group())
        if pr_val > 100:
            quality = "Tachycardic quality (>100 bpm)"
        else:
            quality = "Normal quality (60-100 bpm)"
            
        desc = f"Symmetrical and Regular. {quality}"

        # Cap Refill: 85% < 2s, 15% > 2s (Hypoxemia/Severe) 
        # Logic: If Severe (GOLD 3/4) OR SpO2 < 92, increase chance of > 2s
        spo2_val = int(re.search(r'\d+', self.vital_signs["SpO2"]).group())
        
        if self.severity in ["GOLD_3", "GOLD_4"] or spo2_val < 92:
            cap_refill = self.random.choices(["< 2 seconds", "> 2 seconds"], weights=[60, 40])[0]
        else:
            cap_refill = self.random.choices(["< 2 seconds", "> 2 seconds"], weights=[95, 5])[0]

        return {"desc": desc, "cap_refill": cap_refill}

    def _gen_abdominal(self):
        """
        معاینه شکم 
        """
        # Vascular Bruits: 95% Absent, 5% Present 
        bruits = self.random.choices(["Absent", "Present"], weights=[95, 5])[0]
        
        # Liver Palpation: Hepatic Congestion if Cor Pulmonale 
        if self.cor_pulmonale == "Present":
            # 5% chance in general logic, but practically linked to Cor Pulmonale presence
            palpation = self.random.choices(
                ["No masses, Liver/Spleen non-palpable", "Mildly palpable liver edge below costal margin (Hepatic Congestion)"],
                weights=[30, 70] # Higher chance if Cor Pulmonale is actually present
            )[0]
        else:
            palpation = "No masses, Liver/Spleen non-palpable"
            
        return {
            "inspection": "Flat/Rounded, Symmetrical, No obvious scars",
            "auscultation": f"Normoactive Bowel Sounds. Vascular Bruits: {bruits}",
            "palpation": f"Soft, non-tender. {palpation}"
        }

    def _gen_neuro(self):
        """
        معاینه عصبی 
        """
        # Mental Status: 95% A&Ox3, 5% Drowsy (Severe) 
        # This should align with General Appearance LOC logic
        gcs_val = int(self.vital_signs["GCS"])
        if gcs_val < 15:
            ms = "Drowsy or Mildly Confused (Consistent with Hypercapnia)"
        else:
            ms = "Alert and Oriented to Person, Place, and Time (A&Ox3)"

        # Motor: 70% 5/5, 20% 4/5 (Cachexia/Severe), 10% Asymmetrical 
        # If Emphysema (Cachectic) or Severe, higher chance of 4/5
        if self.phenotype == "Emphysema" or self.severity == "GOLD_4":
            motor = self.random.choices(
                ["Motor Strength 5/5, Normal Tone", "Motor Strength 4/5 (Generalized weakness/Muscle Wasting)"],
                weights=[60, 40]
            )[0]
        else:
             motor = self.random.choices(
                ["Motor Strength 5/5, Normal Tone", "Asymmetrical weakness (Unrelated Comorbidity)"],
                weights=[90, 10]
            )[0]
            
        # Tremor (Beta-agonist side effect)
        tremor = self.random.choices(["Absent", "Fine Tremor"], weights=[95, 5])[0]
        
        return {"ms": ms, "motor": motor, "tremor": tremor}

    def _gen_plethysmography(self):
        """
        
        """
        # 80% Increased Lung Volumes, 20% Normal
        return self.random.choices(
            ["Increased Lung Volumes (Increased RV/TLC)", "Within normal range"],
            weights=[80, 20]
        )[0]
    
    def generate_paraclinic_case(self):
        self.vital_signs = self._generate_vitals()
        personal_info = self._generate_personal_information()
        
        # Parse logic variables
        gcs_val = self.vital_signs["GCS"]
        
        # 1. General Appearance
        gen_app = self._gen_general_appearance(gcs_val)
        
        # 2. Head & Neck (New Dynamic)
        hn_exam = self._gen_head_neck()
        
        # 3. Respiratory
        resp_exam = self._gen_resp_exam()
        
        # 4. Cardiovascular (Updated)
        cv_exam = self._gen_cv_exam() # Center (Heart)
        peri_exam = self._gen_peripheral_pulses() # Periphery
        
        # 5. Abdominal (New Dynamic)
        abd_exam = self._gen_abdominal()
        
        # 6. Neurological (New Dynamic)
        neuro_exam = self._gen_neuro()
        
        # 7. Labs
        cbc = self._gen_cbc()
        bmp = self._gen_bmp()
        lfts = self._gen_lfts()
        vbg = self._gen_vbg()
        bnp = self._gen_bnp()
        imaging = self._gen_imaging()
        
        # 8. Functional
        spiro = self._gen_spirometry()
        pleth = self._gen_plethysmography() # New Dynamic

        data = {
            "patient_profile": {
                "personal_information": personal_info
            },
            "physical_exam": {
                "vital_signs": self.vital_signs,
                "general_appearance": {
                    "level_of_consciousness": gen_app["loc"],
                    "mood_and_behavior": gen_app["mood"],
                    "posture_and_position": gen_app["posture"],
                    "overall_appearance": f"Nutritional: {gen_app['nutrition']}",
                    "cardiopulmonary_and_circulatory_clues": {
                        "cyanosis": gen_app["cyanosis"],
                        "dyspnea": f"Severity Consistent with {self.severity} (MMRC scale)",
                        "edema": gen_app["edema"]
                    }
                },
                "head_and_neck": {
                    "eyes": hn_exam["eyes"],
                    "neck_and_lymphatics": hn_exam["neck"]
                },
                "respiratory_system": {
                    "inspection": {
                        "accessory_muscles": resp_exam["accessory"],
                        "chest_shape_and_symmetry": resp_exam["barrel"]
                    },
                    "palpation": {
                        "chest_expansion": resp_exam["expansion"],
                        "tactile_fremitus": resp_exam["fremitus"]
                    },
                    "percussion": resp_exam["percussion"],
                    "auscultation": {
                        "breath_sounds": resp_exam["bs"],
                        "adventitious_sounds": resp_exam["adv"]
                    }
                },
                "cardiovascular_system": {
                    "precordium": cv_exam["heave"],
                    "auscultation": {
                        "heart_sounds_s1_s2": cv_exam["hs"],
                        "murmurs": cv_exam["murmur"]
                    },
                    "peripheral_pulses": peri_exam["desc"],
                    "cap_refill": peri_exam["cap_refill"]
                },
                "abdominal_system": {
                    "inspection": abd_exam["inspection"],
                    "auscultation": abd_exam["auscultation"],
                    "percussion_palpation": abd_exam["palpation"]
                },
                "neurological": {
                    "mental_status": neuro_exam["ms"],
                    "motor": neuro_exam["motor"],
                    "involuntary_movements": neuro_exam["tremor"]
                },
                "musculoskeletal_system": {
                    "joints_and_muscles": self.random.choices(
                        ["No joint swelling/tenderness", "Diffuse myalgias"], 
                        weights=[95, 5]
                    )[0]
                }
            },
            "paraclinic": {
                "basic_blood_tests": {
                    "CBC": cbc,
                    "ESR": self._generate_value([{"range": (5, 29), "weight": 70}, {"range": (30, 60), "weight": 30}], is_int=True) + " mm/h",
                    "CRP": self._generate_value([{"range": (1, 19), "weight": 70}, {"range": (20, 50), "weight": 30}], is_int=True) + " mg/L",
                    "BMP": bmp,
                    "LFTs": lfts,
                    "VBG": vbg
                },
                "specialized_lung_tests": {
                    "Sputum_analysis": {
                        "Gram_Stain": self._gen_sputum_gram(),
                        "Sample_Quality": "Not Indicated for Routine Stable Visit"
                    },
                    "Sputum_AFB": self._gen_sputum_afb(),
                    "a1_antitrypsin_level": self._gen_a1at(),
                    "D_dimer": self._gen_ddimer(),
                    "BNP_NT_proBNP": bnp
                },
                "immunity_and_serology": {
                    "HIV_test": self.random.choices(["Negative", "Positive"], weights=[98, 2])[0],
                    "Autoimmune_pannel": self.random.choices(["Negative", "Positive"], weights=[95, 5])[0]
                },
                "simple_imaging": {
                    "Chest_X_Ray": {
                        "Findings": imaging["cxr"]
                    }
                },
                "advanced_imaging": {
                    "Chest_CT": {
                         "Findings": imaging["ct"]
                    }
                },
                "functional_tests": {
                    "Spirometry": spiro["spiro"],
                    "DLCO": spiro["dlco"],
                    "plethysmography": pleth,
                    "peak_flow": self.random.choices(["Reduced", "Normal"], weights=[80, 20])[0]
                },
                "procedures": {
                    "Bronchoscopy": "Not Indicated for Routine Stable Visit",
                    "torachonthesis": "Not Indicated"
                }
            }
        }
        return data
