import random
import re
from history_taking_creator import history_taking_creator 
import json

class PneumoniaDataGenerator:
    """
    کلاسی برای تولید داده‌های شبیه‌سازی شده آزمایشگاهی، پاراکلینیکی و معاینات فیزیکی.
    نسخه به روز شده با منطق هماهنگ‌سازی و اضافه شدن Patient Profile پیشرفته.
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
        self.case_type = self._determine_case_type()
        self.pe_status = "PE Present" if self.case_type == "LOBAR_PE_PRESENT" else "PE Absent"
        self.vital_signs = {} 
        self.severity_level = None 


    def _select_occupation(self, gender, age_str):
        age = int(age_str.split()[0])
        
        if age > 65:
            return self.random.choice(self.RANDOM_DATA_LISTS["occupations_retirement"])
        
        if 55 <= age <= 65:
            if self.random.random() < 0.5:
                return self.random.choice(self.RANDOM_DATA_LISTS["occupations_retirement"])
            else:
                if gender == "مرد":
                    return self.random.choice(self.RANDOM_DATA_LISTS["occupations_male"])
                else:
                    return self.random.choice(self.RANDOM_DATA_LISTS["occupations_female"])

        else:
            if gender == "مرد":
                return self.random.choice(self.RANDOM_DATA_LISTS["occupations_male"])
            else:
                return self.random.choice(self.RANDOM_DATA_LISTS["occupations_female"])

    def _select_place_of_residence(self, place_of_birth):
        if self.random.random() < 0.7:
            nearby_cities = self.RANDOM_DATA_LISTS["city_proximity"].get(place_of_birth, [])
            if nearby_cities:
                return self.random.choice(nearby_cities)
            
        all_cities = self.RANDOM_DATA_LISTS["famous_cities_sample_30"]
        return self.random.choice(all_cities)

    def _select_marital_status(self, gender, age_str):
        age = int(age_str.split()[0])
        
        prob_married = 0
        
        if gender == "مرد":
            prob_married = 0.8 if age >= 45 else 0.5
        elif gender == "زن":
            prob_married = 0.9 if age >= 35 else 0.6
                
        if self.random.random() < prob_married:
            return self.random.choices(["متأهل", "همسر متوفی"], weights=[90, 10], k=1)[0]
        else:
            return self.random.choices(["مجرد", "مطلقه"], weights=[70, 30], k=1)[0]

    def _generate_personal_information(self):
        gender = self.random.choice(["مرد", "زن"])
        age_num = self.random.randint(40, 75)
        age_str = f"{age_num} ساله"
        
        name_key = "MALE" if gender == "مرد" else "FEMALE"
        first_name = self.random.choice(self.RANDOM_DATA_LISTS["first_names_sample_100"][name_key])
        last_name = self.random.choice(self.RANDOM_DATA_LISTS["last_names_sample_100"])
        
        occupation = self._select_occupation(gender, age_str)
        
        place_of_birth = self.random.choice(self.RANDOM_DATA_LISTS["famous_cities_sample_30"])
        place_of_residence = self._select_place_of_residence(place_of_birth)
        
        marital_status = self._select_marital_status(gender, age_str)
        
        return {
            "first_name": first_name,
            "last_name": last_name,
            "age": age_str,
            "gender": gender,
            "occupation": occupation,
            "place_of_birth": place_of_birth,
            "place_of_residence": place_of_residence,
            "marital_status": marital_status
        }

    def _determine_case_type(self):
        return self.random.choices(
            ["LOBAR_PE_PRESENT", "LOBAR_PE_ABSENT", "INTERSTITIAL"], 
            weights=[15, 60, 25], k=1
        )[0]

    def _determine_severity(self):
        pr_match = re.search(r'\d+', self.vital_signs.get("PR", "0"))
        rr_match = re.search(r'\d+', self.vital_signs.get("RR", "0"))
        t_match = re.search(r'(\d+\.\d+|\d+)', self.vital_signs.get("T", "0"))
        spo2_match = re.search(r'\d+', self.vital_signs.get("SpO2", "0"))

        pr_val = int(pr_match.group(0)) if pr_match else 0
        rr_val = int(rr_match.group(0)) if rr_match else 0
        t_val = float(t_match.group(0)) if t_match else 0.0
        spo2_val = int(spo2_match.group(0)) if spo2_match else 0

        if pr_val > 100 or rr_val > 20 or t_val > 38.0 or spo2_val < 95:
            return "SEVERE" 
        else:
            return "MILD"

    def _generate_value(self, distributions, is_int=False, precision=2):
        ranges = [d["range"] for d in distributions]
        weights = [d["weight"] for d in distributions]
        chosen_range = self.random.choices(ranges, weights=weights, k=1)[0]
        
        if is_int:
            value = self.random.randint(chosen_range[0], chosen_range[1])
            return str(value)
        else:
            value = self.random.uniform(chosen_range[0], chosen_range[1])
            return str(round(value, precision))

    def _generate_bp_value(self):
        distributions = [{"sys_range": (100, 140), "dia_range": (60, 90), "weight": 80}, 
                         {"sys_range": (70, 89), "dia_range": (40, 59), "weight": 20}]
        chosen = self.random.choices(distributions, weights=[d["weight"] for d in distributions], k=1)[0]
        sys = self.random.randint(chosen["sys_range"][0], chosen["sys_range"][1])
        dia = self.random.randint(chosen["dia_range"][0], chosen["dia_range"][1])
        return f"{sys}/{dia} mmHg"

    def _generate_t_value(self):
        distributions = [{"range": (37.0, 38.0), "weight": 40}, {"range": (38.1, 40.5), "weight": 60}]
        return f"{self._generate_value(distributions, precision=1)} °C"

    def _generate_pr_value(self):
        distributions = [{"range": (60, 100), "weight": 70}, {"range": (101, 140), "weight": 30}]
        chosen = self.random.choices(distributions, weights=[d["weight"] for d in distributions], k=1)[0]
        val = self.random.randint(chosen["range"][0], chosen["range"][1])
        return f"{val} bpm and regular rhythm"

    def _generate_rr_value(self):
        distributions = [{"range": (12, 20), "weight": 40}, {"range": (21, 24), "weight": 35}, {"range": (25, 40), "weight": 25}]
        chosen = self.random.choices(distributions, weights=[d["weight"] for d in distributions], k=1)[0]
        return f"{self.random.randint(chosen['range'][0], chosen['range'][1])} breaths/min"

    def _generate_spo2_value(self):
        distributions = [{"range": (95, 100), "weight": 60}, {"range": (90, 94), "weight": 30}, {"range": (80, 89), "weight": 10}]
        chosen = self.random.choices(distributions, weights=[d["weight"] for d in distributions], k=1)[0]
        return f"{self.random.randint(chosen['range'][0], chosen['range'][1])}% (RA)"

    def _generate_gcs_value(self):
        if self.severity_level == "MILD":
            return "15"
        else:
            return str(self.random.choice([13, 14]))

    def _gen_loc(self):
        if self.severity_level == "MILD":
            return "Alert and Oriented to Person, Place, and Time"
        else:
            return "Lethargic or Drowsy, but arousable" 

    def _gen_mood(self):
        opts = ["Cooperative and Appears Acutely Ill", "Restless with evident discomfort"]
        return self.random.choices(opts, weights=[80, 20], k=1)[0]
    
    def _gen_posture(self):
        opts = ["Comfortable in bed", "Sitting upright", "Tripod position"]
        return self.random.choices(opts, weights=[75, 15, 10], k=1)[0]

    def _gen_overall_app(self):
        opts = ["No obvious signs of cachexia or obesity", "Cachectic", "Obese"]
        return self.random.choices(opts, weights=[90, 5, 5], k=1)[0]

    def _gen_cyanosis(self):
        opts = ["Absent", "Present (Peri-oral cyanosis)", "Present (Nail bed cyanosis)"]
        return self.random.choices(opts, weights=[80, 10, 10], k=1)[0]

    def _gen_dyspnea(self):
        if self.severity_level == "MILD":
            return "Mild dyspnea only on exertion"
        else:
            opts = ["Moderate dyspnea at rest, without accessory muscle use", "Severe dyspnea at rest, with accessory muscle use"]
            return self.random.choice(opts)

    def _gen_edema(self):
        opts = ["Absent", "Mild Pitting Edema"]
        return self.random.choices(opts, weights=[90, 10], k=1)[0]

    def _gen_eyes(self):
        opts = ["Pink conjunctiva, Anicteric sclera", "Pale conjunctiva"]
        return self.random.choices(opts, weights=[85, 15], k=1)[0]

    def _gen_lymph(self):
        opts = ["Non-palpable or Small, non-tender cervical nodes", "Tender, enlarged, mobile anterior cervical nodes"]
        return self.random.choices(opts, weights=[70, 30], k=1)[0]

    def _gen_accessory_muscles(self):
        if self.severity_level == "MILD":
            return "Absent"
        else:
            return "Present"

    def _gen_chest_shape(self):
        opts = ["Symmetrical movement, Normal shape", "Reduced movement on one side", "Barrel Chest", "Pectus Excavatum", "Pectus Carinatum"]
        return self.random.choices(opts, weights=[90, 7, 2, 0.5, 0.5], k=1)[0]

    def _gen_chest_expansion(self):
        if self.case_type in ["LOBAR_PE_PRESENT", "LOBAR_PE_ABSENT"]:
            return "Unilateral reduced expansion over affected area"
        else:
            return "Symmetrical expansion"

    def _gen_tactile_fremitus(self):
        if self.case_type == "LOBAR_PE_PRESENT":
            return "Decreased over pleural effusion area"
        elif self.case_type == "LOBAR_PE_ABSENT":
            return "Increased over consolidation"
        else:
            return "Normal and Symmetrical"

    def _gen_percussion(self):
        if self.case_type == "LOBAR_PE_PRESENT":
            return "Flatness over pleural effusion area"
        elif self.case_type == "LOBAR_PE_ABSENT":
            return "Dullness over consolidation"
        else:
            return "Resonant"

    def _gen_breath_sounds(self):
        if self.case_type in ["LOBAR_PE_PRESENT", "LOBAR_PE_ABSENT"]:
            return self.random.choice(["Bronchial breath sounds", "Reduced intensity"])
        else:
            return "Normal Vesicular breath sounds"

    def _gen_adventitious(self):
        if self.case_type in ["LOBAR_PE_PRESENT", "LOBAR_PE_ABSENT"]:
            return self.random.choice(["Coarse crackles", "Rhonchi", "Pleural friction rub"])
        else:
            return "Coarse crackles"

    def _parse_vitals(self):
        pr_match = re.search(r'\d+', self.vital_signs.get("PR", "0"))
        sbp_match = re.search(r'(\d+)/\d+', self.vital_signs.get("BP", "0/0"))
        gcs_match = re.search(r'\d+', self.vital_signs.get("GCS", "15"))

        pr_val = int(pr_match.group(0)) if pr_match else 0
        sbp_val = int(sbp_match.group(1)) if sbp_match else 0
        gcs_val = int(gcs_match.group(0)) if gcs_match else 15
        return pr_val, sbp_val, gcs_val

    def _generate_cv_findings(self):
        pr_val, sbp_val, _ = self._parse_vitals()
        
        jvp = self.random.choices(["< 4 cm above sternal angle", "> 4 cm above sternal angle"], weights=[90, 10], k=1)[0]
        s3 = self.random.choices(["Normal S1 and S2", "Tachycardia with S3 gallop"], weights=[95, 5], k=1)[0]
        murmur = self.random.choices(["Absent", "Soft Systolic Murmur"], weights=[90, 10], k=1)[0]
        pulse_desc = self.vital_signs["PR"]
        
        if self.severity_level == "SEVERE" or sbp_val < 90:
             cap = "> 2 seconds"
        else:
             cap = "< 2 seconds"

        return jvp, s3, murmur, pulse_desc, cap

    def _generate_abdominal_system(self):
        return "Soft, non-tender, non-distended, no organomegaly"

    def _generate_neuro_findings(self):
        if self.severity_level == "MILD":
            ms = "A&Ox3"
        else:
            ms = "Consistent with General Appearance (Lethargic)"
        
        motor = self.random.choices(
            ["Motor Strength 5/5, DTRs 2+ and Symmetrical", "Mild weakness", "Asymmetrical DTRs"],
            weights=[95, 3, 2], k=1)[0]
        return ms, motor

    def _generate_msk_findings(self):
        return self.random.choices(
            ["No joint swelling, tenderness, or muscle atrophy", "Diffuse myalgias and arthralgias without swelling"],
            weights=[95, 5], k=1)[0]

    def _gen_cxr(self):
        if self.pe_status == "PE Present":
            return self.random.choice(["Lobar Consolidation (Small Pleural Effusion present)", "Patchy or Segmental Infiltrates (Small Pleural Effusion present)"])
        else:
            return self.random.choice(["Lobar Consolidation (NO Effusion)", "Patchy or Segmental Infiltrates (NO Effusion)", "Diffuse Interstitial Infiltrates (NO Effusion)", "Normal CXR (NO Effusion)"])

    def _gen_ct(self):
        if self.pe_status == "PE Present":
            return "Consolidation with Effusion (fluid collection)"
        else:
            return self.random.choice(["Dense or Patchy Consolidation with NO Pleural abnormality", "Normal CT Scan"])
    
    def _gen_thora(self):
        if self.pe_status == "PE Present":
            pf_prot = round(self.random.uniform(3.5, 5.0), 1)
            ser_prot = round(self.random.uniform(6.0, 8.0), 1)
            pf_ldh = self.random.randint(150, 300)
            ser_ldh = self.random.randint(100, 200)
            pf_alb = round(self.random.uniform(2.0, 3.5), 1)
            ser_alb = round(self.random.uniform(3.5, 5.0), 1)

            return f"Fluid was successfully aspirated : Pleural Fluid Protein {pf_prot} g/dL, Serum Protein {ser_prot} g/dL, Pleural Fluid LDH {pf_ldh} U/L, Serum LDH {ser_ldh} U/L, Pleural Fluid Albumin {pf_alb} g/dL, Serum Albumin {ser_alb} g/dL"
        else:
            return "Not Indicated and fluid cannot be aspirated"
            
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
    def _gen_pao2(self):
        dists = [{"range": (60, 80), "weight": 40}, {"range": (81, 100), "weight": 40}, {"range": (40, 59), "weight": 20}]
        return f"{self._generate_value(dists, is_int=True)} mmHg"
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

    def _get_dlco_finding(self):
        """
        بر اساس فراوانی‌های مشخص شده، وضعیت DLCO را برمی‌گرداند.
        90% Reduced (< 80% predicted), 10% Normal.
        """
        # تعریف یافته‌ها و وزن‌های (فراوانی‌های) متناظر آن‌ها
        findings = [
            "Reduced",  # 90%
            "Normal"                     # 10%
        ]
        
        weights = [70, 30]
        
        # انتخاب تصادفی وضعیت
        chosen_status = self.random.choices(findings, weights=weights, k=1)[0]
        
        # تولید مقدار عددی منطبق بر وضعیت انتخاب شده
        if chosen_status == "Reduced (< 80% predicted)":
            dlco_val = self.random.randint(40, 79)
        else:
            dlco_val = self.random.randint(80, 100)
            
        # برگرداندن هر دو (متن و مقدار) برای سازگاری با ساختار داده
        return chosen_status, f"{dlco_val}% predicted"
    
    def _gen_reversibility(self):
        """
        تولید خروجی تست Reversibility (پاسخ به برونکودیلاتور) بر اساس منطق آسم.
        توزیع احتمال: 80% مثبت، 10% منفی (حجمی)، 10% منفی (ثابت).
        """
        
        # تعیین نوع خروجی بر اساس وزن‌های 80، 10 و 10 درصد
        choice = self.random.choices(
            ["Positive", "Negative"], 
            weights=[5, 95], k=1
        )[0]
        
        if choice == "Positive":
            return "FEV1 increase > 12% AND > 200 mL"
            
        elif choice == "Negative":
            return "FEV1 increase < 12% AND < 200 mL"
            
        return "Not Indicated"
    
    def generate_paraclinic_case(self):
        """
        تولید داده‌ها دقیقاً با ساختار درخواستی و اعمال منطق هماهنگ‌سازی.
        """
        self.vital_signs = {
            "BP": self._generate_bp_value(),
            "T": self._generate_t_value(),
            "PR": self._generate_pr_value(),
            "RR": self._generate_rr_value(),
            "SpO2": self._generate_spo2_value(),
            "GCS": "15",
        }
        
        self.severity_level = self._determine_severity()
        
        self.vital_signs["GCS"] = self._generate_gcs_value()
        
        personal_info = self._generate_personal_information()
        
        jvp, s3, murmur, pulses, cap_refill = self._generate_cv_findings()
        ms_neuro, motor_neuro = self._generate_neuro_findings()
        msk_finding = self._generate_msk_findings()
        
        data = {
            "patient_profile": {
                "personal_information": personal_info
            },
            "physical_exam": {
                "vital_signs": self.vital_signs,
                "general_appearance": {
                    "level_of_consciousness": self._gen_loc(),
                    "mood_and_behavior": self._gen_mood(),
                    "posture_and_position": self._gen_posture(),
                    "overall_appearance": self._gen_overall_app(),
                    "cardiopulmonary_and_circulatory_clues": {
                        "cyanosis": self._gen_cyanosis(),
                        "dyspnea": self._gen_dyspnea(),
                        "edema": self._gen_edema()
                    }
                },
                "head_and_neck": {
                    "eyes": {
                        "sclera_and_conjunctiva": self._gen_eyes()
                    },
                    "neck_and_lymphatics": {
                        "tracheal_position": "Midline",
                        "lymph_nodes": self._gen_lymph()
                    }
                },
                "respiratory_system": {
                    "inspection": {
                        "accessory_muscles": self._gen_accessory_muscles(),
                        "chest_shape_and_symmetry": self._gen_chest_shape()
                    },
                    "palpation": {
                        "chest_expansion": self._gen_chest_expansion(),
                        "tactile_fremitus": self._gen_tactile_fremitus()
                    },
                    "percussion": self._gen_percussion(),
                    "auscultation": {
                        "breath_sounds": self._gen_breath_sounds(),
                        "adventitious_sounds": self._gen_adventitious()
                    }
                },
                "cardiovascular_system": {
                    "JVP_assessment": jvp,
                    "auscultation": {
                        "heart_sounds_s1_s2": s3,
                        "murmurs": murmur
                    },
                    "peripheral_pulses": pulses,
                    "cap_refill": cap_refill
                },
                "abdominal_system": {
                    "percussion_palpation": self._generate_abdominal_system()
                },
                "neurological": {
                    "mental_status_and_LOC": ms_neuro,
                    "motor_strength_and_DTRs": motor_neuro
                },
                "musculoskeletal_system": {
                    "joints_and_muscles": msk_finding
                }
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
                        "Na": self._gen_na(),
                        "BUN": self._gen_bun(),
                        "Cr": self._gen_cr()
                    },
                    "LFTs": {
                        "ALT": self._gen_liver(),
                        "AST": self._gen_liver()
                    },
                    "VBG": {
                        "pH": self._gen_ph(),
                        "PaO2": self._gen_pao2()
                    }
                },
                "specialized_lung_tests": {
                    "Sputum_analysis": {
                        "Gram_Stain": self._gen_gram_stain(),
                        "Sample_Quality": self._gen_sample_quality()
                    },
                    "Sputum_AFB": self._gen_afb(),
                    "a1_antitrypsin_level": self._gen_a1at(),
                    "D_dimer": self._gen_ddimer(),
                    "BNP_NT_proBNP": self._gen_bnp()
                },
                "immunity_and_serology": {
                    "HIV_test": self._gen_hiv(),
                    "Autoimmune_pannel_ANA_ANCA": self._gen_autoimmune()
                },
                "simple_imaging": {
                    "Chest_X_Ray": {
                        "PA_Lateral_Findings_and_Effusion": self._gen_cxr()
                    }
                },
                "advanced_imaging": {
                    "Chest_CT_CTPA": {
                        "Lung_Parenchyma_and_Pleura": self._gen_ct()
                    },
                    "MRI_chest": self._gen_mri(),
                    "Pet_scan": self._gen_pet()
                },
                "functional_tests": {
                    "Spirometry": {
                        "result": self._gen_spirometry(),
                        "Reversibility": self._gen_reversibility()
                    },
                    "dlco": self._get_dlco_finding()[1],
                    "peak_flow": self._gen_peak(),
                    "plethysmography": self._gen_pleth()
                },
                "procedures": {
                    "Bronchoscopy": self._gen_bronch(),
                    "torachonthesis": self._gen_thora()
                }
            }
        }
        return data

if __name__ == "__main__":
    import json
    generator = PneumoniaDataGenerator()
    print(json.dumps(generator.generate_paraclinic_case(), ensure_ascii=False, indent=4))