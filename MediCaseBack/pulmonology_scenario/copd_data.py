import random
import json
import re
from scenario import scenario_creator
# نیازی به ایمپورت LabDataGenerator نیست.

class COPDDataGenerator:
    """
    کلاسی کاملاً مستقل برای تولید سناریوهای COPD بر اساس منطق پیوستگی فنوتیپ، شدت (GOLD) و Cor Pulmonale.
    این کلاس هیچ وابستگی به LabDataGenerator ندارد.
    """
    
    # --- منابع داده برای تولید Patient Profile ---
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
                "فاطمه", "زهرا", "مریم", "سارا", "نازنین", "عسل", "مهسا", "زینب", "پریسا", "آیدا",
                "رعنا", "فرزانه", "شیدا", "رویا", "مهناز", "فریبا", "نیره", "مرضیه", "افسانه", "سیمین",
                "شهلا", "ثریا", "ناهید", "لیلا", "ژاله", "نیلوفر", "نسرین", "سمیرا", "کیمیا", "آزاده",
                "آیلین", "سوگند", "ترانه", "محبوبه", "صدیقه", "پرستو", "بهار", "شبنم", "فاطیما", "مهتاب"
            ]
        },
        "last_names_sample_100": [
            "کریمی", "محمدی", "جعفری", "حسینی", "رضایی", "مرادی", "باقری", "صادقی", "نجفی", "رحمانی",
            "زارعی", "موسوی", "احمدی", "علوی", "صالحی", "کرمی", "قاسمی", "نوروزی", "شفیعی", "عباسی",
            "یزدانی", "مظفری", "کاظمی", "فلاح", "امیری", "سلطانی", "فرهمند", "پورحیدری", "مختاری", "میرزایی",
            "ملکی", "پاکدل", "مقدس", "تیموری", "لطفی", "بهشتی", "آریایی", "خالقی", "کیانی", "توکلی"
        ],
        "occupations_male": [
            "راننده بازنشسته", "کارگر ساختمانی", "معلم بازنشسته", "فروشنده بازار", "آزاد"
        ],
        "occupations_female": [
            "خانه‌دار", "معلم بازنشسته", "خیاط", "آزاد", "کارمند بازنشسته"
        ],
        "occupations_retirement": [
            "بازنشسته تامین اجتماعی", "بازنشسته ارتش", "بازنشسته آموزش و پرورش"
        ],
        "famous_cities_sample_30": [
            "تهران", "اصفهان", "مشهد", "شیراز", "تبریز", "اهواز", "کرج", "یزد", "بندرعباس", "کرمانشاه", "رشت"
        ],
        "city_proximity": { # یک دیکشنری ساده برای انتخاب محل زندگی نزدیک به محل تولد
            "تهران": ["کرج", "قم", "قزوین"],
            "اصفهان": ["شیراز", "یزد"],
            "مشهد": ["نیشابور", "سبزوار"]
        }
    }
    
    def __init__(self):
        self.random = random
        
        # --- ۱. منطق هسته و تعیین متغیرهای اصلی COPD ---
        
        # تعیین فنوتیپ: Emphysema Dominant (60%) / Chronic Bronchitis Dominant (40%)
        self.PHENOTYPE = self.random.choices(
            ["Emphysema Dominant", "Chronic Bronchitis Dominant"], 
            weights=[60, 40], k=1
        )[0]
        
        # تعیین شدت (GOLD Stage): توزیع احتمالات ارسالی
        self.GOLD_STAGE = self.random.choices(
            ["GOLD 1", "GOLD 2", "GOLD 3", "GOLD 4"], 
            weights=[10, 40, 30, 20], k=1
        )[0]
        
        # تعیین Cor Pulmonale: Present (30%) / Absent (70%)
        self.COR_PULMONALE = self.random.choices(
            ["Present", "Absent"], 
            weights=[30, 70], k=1
        )[0]
        
        self.severity_level = "SEVERE" if self.GOLD_STAGE in ["GOLD 3", "GOLD 4"] else "MILD"
        
        # متغیرهای داخلی مورد نیاز
        self.vital_signs = {} 
        self.pa_o2_val = None 
        
    # --- توابع کاربردی (Utility Functions) ---

    def _generate_value(self, distributions, is_int=False, precision=2):
        """تولید یک مقدار عددی تصادفی بر اساس توزیع‌های مشخص شده."""
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
        """تولید فشار خون بر اساس منطق COPD"""
        distributions = [{"sys_range": (100, 140), "dia_range": (60, 90), "weight": 80}, 
                         {"sys_range": (90, 100), "dia_range": (60, 70), "weight": 20}]
        chosen = self.random.choices(distributions, weights=[d["weight"] for d in distributions], k=1)[0]
        sys = self.random.randint(chosen["sys_range"][0], chosen["sys_range"][1])
        dia = self.random.randint(chosen["dia_range"][0], chosen["dia_range"][1])
        return f"{sys}/{dia} mmHg"

    # --- توابع انتخاب پروفایل (Patient Profile Selectors) ---
    
    def _select_occupation(self, gender, age_str):
        age = int(age_str.split()[0])
        if age > 65:
            return self.random.choice(self.RANDOM_DATA_LISTS["occupations_retirement"])
        if 55 <= age <= 65:
            if self.random.random() < 0.5: 
                return self.random.choice(self.RANDOM_DATA_LISTS["occupations_retirement"])
            else:
                return self.random.choice(self.RANDOM_DATA_LISTS["occupations_male"]) if gender == "مرد" else self.random.choice(self.RANDOM_DATA_LISTS["occupations_female"])
        else:
            return self.random.choice(self.RANDOM_DATA_LISTS["occupations_male"]) if gender == "مرد" else self.random.choice(self.RANDOM_DATA_LISTS["occupations_female"])

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
            
    # --- توابع تولید داده‌های COPD (Core Functions) ---
    
    def _generate_personal_information(self):
        gender = self.random.choice(["مرد", "زن"])
        age_num = self.random.randint(55, 85) # سن بالاتر برای COPD
        age_str = f"{age_num} ساله"
        name_key = "MALE" if gender == "مرد" else "FEMALE"
        first_name = self.random.choice(self.RANDOM_DATA_LISTS["first_names_sample_100"][name_key])
        last_name = self.random.choice(self.RANDOM_DATA_LISTS["last_names_sample_100"])
        occupation = self._select_occupation(gender, age_str) 
        place_of_birth = self.random.choice(self.RANDOM_DATA_LISTS["famous_cities_sample_30"])
        place_of_residence = self._select_place_of_residence(place_of_birth)
        marital_status = self._select_marital_status(gender, age_str)
        
        return {
            "first_name": first_name, "last_name": last_name, "age": age_str, "gender": gender,
            "occupation": occupation, "place_of_birth": place_of_birth, "place_of_residence": place_of_residence,
            "marital_status": marital_status
        }
    
    def _generate_chief_complaint(self):
        if self.severity_level == "SEVERE":
            return self.random.choice([
                "تنگی نفس شدید و مزمن، که اخیراً بدتر شده است.",
                "سرفه مزمن خلط دار و مشکل در تنفس.",
                "ناتوانی در انجام فعالیت‌های روزمره به دلیل نفس تنگی."
            ])
        else:
            return self.random.choice([
                "سرفه مزمن خلط دار که سال‌هاست وجود دارد.",
                "تنگی نفس خفیف در هنگام فعالیت‌های سنگین.",
                "حس سنگینی در قفسه سینه و سرفه صبحگاهی."
            ])

    # --- علائم حیاتی ---

    def _generate_t_value(self):
        # T: ۹۵٪ نرمال (۳۶.۵ تا ۳۷.۵ °C)، ۵٪ تب خفیف (< ۳۸ °C)
        distributions = [{"range": (36.5, 37.5), "weight": 95}, {"range": (37.5, 38.0), "weight": 5}]
        return f"{self._generate_value(distributions, precision=1)} °C" 

    def _generate_pr_value(self):
        # PR: ۷۰٪ نرمال (۶۰-۱۰۰)، ۳۰٪ تاکیکاردی خفیف (>۱۰۰)
        distributions = [{"range": (60, 100), "weight": 70}, {"range": (101, 120), "weight": 30}]
        val = self._generate_value(distributions, is_int=True)
        return f"{val} bpm and regular rhythm" 

    def _generate_rr_value(self):
        # RR: هماهنگ با شدت GOLD
        if self.GOLD_STAGE in ["GOLD 1", "GOLD 2"]:
            distributions = [{"range": (16, 18), "weight": 40}, {"range": (18, 20), "weight": 35}, {"range": (20, 22), "weight": 25}] 
        else: 
            distributions = [{"range": (20, 22), "weight": 50}, {"range": (23, 25), "weight": 50}] 
        return f"{self._generate_value(distributions, is_int=True)} breaths/min"

    def _generate_spo2_value(self):
        # SpO2: هماهنگ با شدت GOLD
        if self.GOLD_STAGE in ["GOLD 1", "GOLD 2"]: 
            distributions = [{"range": (94, 100), "weight": 40}, {"range": (92, 93), "weight": 30}, {"range": (90, 91), "weight": 30}] 
        else: 
            distributions = [{"range": (92, 94), "weight": 40}, {"range": (90, 91), "weight": 30}, {"range": (80, 89), "weight": 30}] 
        return f"{self._generate_value(distributions, is_int=True)}% (RA)"

    def _generate_gcs_value(self):
        # GCS 13-14 فقط در GOLD 4 (۵٪)
        if self.GOLD_STAGE == "GOLD 4" and self.random.random() < 0.05:
            return str(self.random.choice([13, 14]))
        return "15"
    
    # --- معاینه فیزیکی ---
    
    def _gen_loc(self):
        if self.vital_signs.get("GCS") in ["13", "14"]:
            return "Lethargic or Drowsy, but arousable (Hypercapnia)"
        return "Alert and Oriented to Person, Place, and Time (A&Ox3)"

    def _gen_overall_app(self):
        # وضعیت ظاهری: بستگی به PHENOTYPE
        if self.PHENOTYPE == "Emphysema Dominant":
            opts = ["Cachectic (Muscle Wasting)", "No obvious signs of cachexia or obesity"]
            return self.random.choices(opts, weights=[40, 60], k=1)[0]
        elif self.PHENOTYPE == "Chronic Bronchitis Dominant":
            opts = ["No obvious signs of cachexia or obesity", "Obese"]
            return self.random.choices(opts, weights=[75, 25], k=1)[0]
        return "No obvious signs of cachexia or obesity"
    
    def _gen_cyanosis(self):
        spo2_match = re.search(r'\d+', self.vital_signs.get("SpO2", "100"))
        spo2_val = int(spo2_match.group(0)) if spo2_match else 100
        
        if spo2_val < 92 and self.random.random() < 0.5: 
            return "Present (Central Cyanosis)"
        return "Absent"
        
    def _gen_edema(self):
        # Edema: اگر Cor Pulmonale Present باشد، ۹۰٪ ادم دوطرفه
        if self.COR_PULMONALE == "Present":
            return self.random.choices(["Bilateral Pitting Edema", "Absent"], weights=[90, 10], k=1)[0]
        return "Absent" 
    
    def _gen_chest_shape(self):
        # ۴۰٪ Barrel Chest
        return self.random.choices(["Barrel Chest (increased AP diameter)", "Symmetrical movement, Normal shape"], weights=[40, 60], k=1)[0]
    
    def _gen_chest_expansion(self):
        # ۸۵٪ کاهش یافته دوطرفه (Bilateral Reduced)
        return self.random.choices(["Bilateral Reduced Expansion", "Symmetrical expansion"], weights=[85, 15], k=1)[0]

    def _gen_tactile_fremitus(self):
        # ۷۰٪ کاهش یافته و دوسویه
        return self.random.choices(["Decreased and Symmetrical (due to Hyperinflation)", "Normal and Symmetrical"], weights=[70, 30], k=1)[0]

    def _gen_percussion(self):
        # ۹۰٪ هایپررزونانت منتشر
        return self.random.choices(["Diffuse Hyperresonant", "Resonant"], weights=[90, 10], k=1)[0]

    def _gen_breath_sounds(self):
        # ۱۰۰٪ طولانی شدن بازدم
        result = "Prolonged Expiration (100% of cases). "
        reduced_intensity_chance = 0.70 
        if self.PHENOTYPE == "Emphysema Dominant":
            reduced_intensity_chance = 0.85 
            
        if self.random.random() < reduced_intensity_chance:
            result += "Reduced intensity (Diminished Breath Sounds)."
        else:
            result += "Normal Vesicular breath sounds."
        return result

    def _gen_adventitious(self):
        # ۵۰٪ Wheezing منتشر
        options = ["Wheezing Diffuse (Bronchospasm)", "No Adventitious Sounds"]
        weights = [50, 45]
        
        if self.COR_PULMONALE == "Present" and self.random.random() < 0.15: 
             return "Fine Crackles (base of lungs)"
             
        return self.random.choices(options, weights=weights, k=1)[0]

    def _generate_cv_findings(self):
        # JVP: اگر COR_PULMONALE Present باشد، ۷۰٪ JVD
        jvp = "< 4 cm above sternal angle"
        if self.COR_PULMONALE == "Present" and self.random.random() < 0.70:
            jvp = "> 4 cm above sternal angle (Jugular Venous Distension)"
            
        s1_s2_opts = ["Muffled/Distant S1 and S2", "Normal S1 and S2"]
        s1_s2 = self.random.choices(s1_s2_opts, weights=[70, 30], k=1)[0]
        
        return {
            "JVP_assessment": jvp,
            "s1_s2_description": s1_s2,
            "murmur_description": self.random.choices(["Absent", "Soft Systolic Murmur"], weights=[90, 10], k=1)[0],
            "peripheral_pulses": self.vital_signs["PR"]
        }
    
    # --- پاراکلینیک ---
    
    def _generate_hemoglobin_value(self):
        # Hb (Polycythemia): هماهنگ با SpO2 و Cor Pulmonale
        polycythemia_chance = 0.15 
        spo2_match = re.search(r'\d+', self.vital_signs.get("SpO2", "100"))
        spo2_val = int(spo2_match.group(0)) if spo2_match else 100

        if spo2_val < 92 and self.COR_PULMONALE == "Present":
            polycythemia_chance = 0.50

        if self.random.random() < polycythemia_chance:
            dists = [{"range": (17.1, 20.0), "weight": 100}]
        else:
            dists = [{"range": (12.0, 17.0), "weight": 100}]
            
        return f"{self._generate_value(dists, precision=1)} g/dL"

    def _generate_wbc_count(self):
        # WBC: ۹۰٪ نرمال (۴-۱۲k)، ۱۰٪ کمی بالا (۱۲-۱۵k)
        dists = [{"range": (4000, 12000), "weight": 90}, {"range": (12001, 15000), "weight": 10}]
        return f"{self._generate_value(dists, is_int=True)} /µL"

    def _generate_crp_value(self):
        # CRP: ۷۰٪ نرمال (< ۱۰)، ۳۰٪ کمی بالا (۲۰-۵۰)
        dists = [{"range": (1, 10), "weight": 70}, {"range": (20, 50), "weight": 30}]
        return f"{self._generate_value(dists, is_int=True)} mg/L"

    def _gen_bnp(self):
        # BNP: اگر Cor Pulmonale Present باشد، ۷۰٪ بالا
        if self.COR_PULMONALE == "Present":
            return self.random.choices(["elevated (>100 pg/mL)", "within normal range"], weights=[70, 30], k=1)[0]
        return "within normal range"
        
    def _gen_vbg(self):
        # VBG: منطق اسیدوز تنفسی مزمن جبران شده
        
        ph_val = self._generate_value([{"range": (7.35, 7.45), "weight": 95}], precision=2) 
        paco2_val = self._generate_value([{"range": (35, 45), "weight": 95}], is_int=True)

        if self.GOLD_STAGE == "GOLD 4" and self.random.random() < 0.05:
            ph_val = self._generate_value([{"range": (7.30, 7.35), "weight": 100}], precision=2) 
            paco2_val = self._generate_value([{"range": (45, 60), "weight": 100}], is_int=True) 
        
        # PaO2: هماهنگ با شدت
        if self.severity_level == "SEVERE":
            dists = [{"range": (40, 60), "weight": 20}, {"range": (61, 80), "weight": 40}, {"range": (81, 100), "weight": 40}]
        else:
            dists = [{"range": (81, 100), "weight": 60}, {"range": (61, 80), "weight": 30}, {"range": (50, 60), "weight": 10}]
            
        pa_o2_val = self._generate_value(dists, is_int=True)
        self.pa_o2_val = pa_o2_val 
        
        return f"pH: {ph_val}, PaO2: {pa_o2_val} mmHg, PaCO2: {paco2_val} mmHg, Bicarb: WNL"
        
    def _gen_spirometry(self):
        # FEV1 % Predicted باید دقیقاً با GOLD Stage هماهنگ باشد.
        
        if self.GOLD_STAGE == "GOLD 1": fev1_range = (80, 100)
        elif self.GOLD_STAGE == "GOLD 2": fev1_range = (50, 79)
        elif self.GOLD_STAGE == "GOLD 3": fev1_range = (30, 49)
        elif self.GOLD_STAGE == "GOLD 4": fev1_range = (15, 29)
        
        fev1_perc = self.random.randint(fev1_range[0], fev1_range[1])
        fev1_fvc_ratio = self._generate_value([{"range": (0.40, 0.70), "weight": 100}], precision=2)
        
        return (f"Obstructive Pattern confirmed (FEV1/FVC Ratio: {fev1_fvc_ratio} < 0.70). "
                f"FEV1 % Predicted: {fev1_perc}%. FVC % Predicted: {self.random.randint(60, 80)}%. "
                f"Result is consistent with {self.GOLD_STAGE} severity.")

    def _gen_dlco(self):
        # DLCO: کاهش یافته (۹۰٪) اگر Emphysema
        if self.PHENOTYPE == "Emphysema Dominant":
            return self.random.choices(["Reduced (< 70% Predicted)", "Within normal range"], weights=[90, 10], k=1)[0]
        # Chronic Bronchitis Dominant: ۹۰٪ نرمال
        return self.random.choices(["Within normal range", "Reduced (< 70% Predicted)"], weights=[90, 10], k=1)[0]
        
    def _gen_cxr(self):
        # CXR: ۷۰٪ Hyperinflation، ۳۰٪ Bullae.
        options = ["Hyperinflation findings (Flat Diaphragms, Narrow Heart Shadow)", "Bullae (Air-filled cysts in Lung Fields)"]
        return self.random.choices(options, weights=[70, 30], k=1)[0]

    def _gen_ct(self):
        # CT: ۷۰٪ Emphysema/Air Trapping، ۳۰٪ Bullae/Bronchiectatic
        options = ["Emphysema/Air Trapping Changes", "Bullae or Bronchiectatic Changes"]
        return self.random.choices(options, weights=[70, 30], k=1)[0]
        
    def _gen_thora(self):
        return "Not Indicated (No Pleural Effusion on Imaging)"
        
    def _generate_platelet_count(self):
        dists = [{"range": (150000, 450000), "weight": 60}, {"range": (450001, 600000), "weight": 30}, {"range": (50000, 149000), "weight": 10}]
        return f"{self._generate_value(dists, is_int=True)} /µL"
        
    def _generate_esr_value(self):
        dists = [{"range": (51, 120), "weight": 50}, {"range": (20, 50), "weight": 30}, {"range": (5, 19), "weight": 20}]
        return f"{self._generate_value(dists, is_int=True)} mm/h"


    def generate_paraclinic_case(self):
        """ تابع اصلی تولید داده‌ها با ساختار JSON کامل """
        
        # ۱. تولید علائم حیاتی
        self.vital_signs = {
            "BP": self._generate_bp_value(), 
            "T": self._generate_t_value(), 
            "PR": self._generate_pr_value(), 
            "RR": self._generate_rr_value(),
            "SpO2": self._generate_spo2_value(),
            "GCS": self._generate_gcs_value(),
        }
        
        # ۲. تولید کامل داده‌ها
        data = {
            "patient_profile": {
                **self._generate_personal_information(),
                "chief_complaint": self._generate_chief_complaint(),
            },
            "physical_exam": {
                "vital_signs": self.vital_signs,
                "general_appearance": {
                    "level_of_consciousness": self._gen_loc(),
                    "mood_and_behavior": self.random.choices(["Cooperative and Appears Chronically Ill", "Anxious/Depressed"], weights=[80, 20], k=1)[0],
                    "posture_and_position": self.random.choices(["Comfortable in bed or seated", "Sitting upright", "Tripod position (In severe chronic disease)"], weights=[75, 15, 10], k=1)[0],
                    "overall_appearance": self._gen_overall_app(),
                    "cardiopulmonary_and_circulatory_clues": {
                        "cyanosis": self._gen_cyanosis(), 
                        "dyspnea": self.random.choices(["Mild dyspnea only on exertion", "Moderate dyspnea with minimal activity", "Severe dyspnea at rest, with accessory muscle use (In GOLD 4)"], weights=[40, 40, 20], k=1)[0], 
                        "edema": self._gen_edema()
                    }
                },
                "respiratory_system": {
                    "inspection": {
                        "accessory_muscles": self.random.choices(["Present (Chronic Use)", "Absent"], weights=[90, 10], k=1)[0], 
                        "chest_shape_and_symmetry": self._gen_chest_shape(),
                    },
                    "palpation": {
                        "chest_expansion": self._gen_chest_expansion(),
                        "tactile_fremitus": self._gen_tactile_fremitus(),
                    },
                    "percussion": self._gen_percussion(),
                    "auscultation": {
                        "breath_sounds": self._gen_breath_sounds(),
                        "adventitious_sounds": self._gen_adventitious(),
                    },
                },
                "cardiovascular_system": self._generate_cv_findings(),
                "abdominal_system": {
                    "percussion_palpation": self.random.choices(["Soft, non-tender, non-distended, no organomegaly", "Hepatic Congestion (if Cor Pulmonale is severe)"], weights=[95, 5], k=1)[0]
                },
                "neurological": {
                    "mental_status_and_LOC": self._gen_loc(),
                    "motor_strength_and_DTRs": self.random.choices(["Motor Strength 5/5, DTRs 2+ and Symmetrical", "Mild weakness/Muscle Wasting (Cachexia)"], weights=[70, 30], k=1)[0]
                },
            },
            "paraclinic": {
                "basic_blood_tests": {
                    "CBC": {
                        "Hb": self._generate_hemoglobin_value(),
                        "WBC": self._generate_wbc_count(), 
                        "Plt": self._generate_platelet_count(),
                    },
                    "Inflammatory_markers": {
                        "ESR": self._generate_esr_value(), 
                        "CRP": self._generate_crp_value(),
                    },
                    "Cardiac_Markers": { 
                        "BNP": self._gen_bnp(),
                    },
                    "VBG": self._gen_vbg(),
                },
                "simple_imaging": {
                    "Chest_X_Ray": self._gen_cxr(),
                },
                "advanced_imaging": {
                    "Chest_CT": self._gen_ct(),
                    "MRI_chest": self.random.choices(["Normal", "Abnormal signal intensity"], weights=[95, 5], k=1)[0],
                },
                "functional_tests": {
                    "Spirometry": self._gen_spirometry(),
                    "DLCO": self._gen_dlco(),
                    "plethysmography": self.random.choices(["Reduced Lung Volumes (Hyperinflation)", "within normal range"], weights=[90, 10], k=1)[0],
                },
                "procedures": {
                    "Bronchoscopy": self.random.choices(["Normal Anatomy with Secretions", "Mucosal Inflammation or Obstruction"], weights=[90, 10], k=1)[0],
                    "torachonthesis": self._gen_thora()
                }
            }
        }
        return data
    
# ... (کدهای LabDataGenerator و سپس کلاس جدید COPDDataGenerator) ...

def create_copd_case_json():
    """ 
    اجرای COPDDataGenerator برای تولید سناریوی COPD.
    """
    
    # فراخوانی کلاس مستقل
    copd_generator = COPDDataGenerator() 
    paraclinic_output = copd_generator.generate_paraclinic_case()
    
    # فرض می‌شود scenario_creator یا منطق تولید شرح حال COPD در دسترس است.
    # اگر از scenario_creator برای Pneumonia استفاده می‌کردید، باید مطمئن شوید 
    # که یک منطق مشابه برای COPD نیز وجود دارد یا آن را ساده نگه دارید.
    
    history_data, _ = scenario_creator()
    
    final_patient_profile = paraclinic_output["patient_profile"]
    
    final_history_taking = history_data["history_taking"]
    
    final_physical_exam = paraclinic_output["physical_exam"]
    final_paraclinic = paraclinic_output["paraclinic"]
    
    
    final_case = {
        "patient_profile": final_patient_profile,
        "history_taking": final_history_taking,
        "physical_exam": final_physical_exam,
        "paraclinic": final_paraclinic
    }
    
    return json.dumps(final_case, ensure_ascii=False, indent=4)

# مثال اجرا:
if __name__ == "__main__":
    copd_case = create_copd_case_json()
    print(copd_case)