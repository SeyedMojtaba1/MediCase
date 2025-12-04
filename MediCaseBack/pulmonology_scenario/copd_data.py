import random
import re
from history_taking_creator import history_taking_creator

class COPDDataGenerator:
    """
    کلاسی برای تولید داده‌های شبیه‌سازی شده COPD بر اساس فایل COPD.txt.
    
    Logic Drivers (سه متغیر اصلی برای حفظ سازگاری):
    1. PHENOTYPE: Emphysema vs Chronic Bronchitis
    2. SEVERITY: GOLD 1 to GOLD 4
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
        
        # 1. CORE LOGIC INITIALIZATION (Drivers)
        # Phenotype
        self.phenotype = self.random.choices(
            ["Emphysema", "Chronic Bronchitis"], 
            weights=[60, 40], k=1
        )[0]
        
        # Severity Distribution based on text frequency (derived from FEV1 buckets)
        # GOLD 1 (10%), GOLD 2 (40%), GOLD 3 (30%), GOLD 4 (20%)
        self.severity = self.random.choices(
            ["GOLD_1", "GOLD_2", "GOLD_3", "GOLD_4"],
            weights=[10, 40, 30, 20], k=1
        )[0]
        
        # Cor Pulmonale Distribution
        self.cor_pulmonale = self.random.choices(
            ["Present", "Absent"],
            weights=[30, 70], k=1
        )[0]

        # Holder for consistency checks
        self.simulated_spo2_val = 95
        self.simulated_gcs_val = 15

    # --- Demographic Helpers (No changes from text required, kept for context) ---
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

    # --- Value Generator Helper ---
    def _generate_value(self, distributions, is_int=False, precision=2):
        ranges = [d["range"] for d in distributions]
        weights = [d["weight"] for d in distributions]
        chosen_range = self.random.choices(ranges, weights=weights, k=1)[0]
        if is_int:
            val = self.random.randint(chosen_range[0], chosen_range[1])
            return str(val)
        val = self.random.uniform(chosen_range[0], chosen_range[1])
        return str(round(val, precision))

    # --- 1. Vital Signs ---
    def _gen_vitals(self):
        # BP: 80% Normal/HTN, 20% Low Normal
        bp_choice = self.random.choices(["Normal/HTN", "Low Normal"], weights=[80, 20])[0]
        if bp_choice == "Normal/HTN":
            sys = self.random.randint(100, 140)
            dia = self.random.randint(60, 90)
        else:
            sys = self.random.randint(90, 100)
            dia = self.random.randint(60, 70)
            
        # T: 95% Normal, 5% Low Grade
        t_choice = self.random.choices(["Normal", "Low Grade"], weights=[95, 5])[0]
        temp = round(self.random.uniform(36.5, 37.5), 1) if t_choice == "Normal" else round(self.random.uniform(37.5, 38.0), 1)

        # PR: 70% Normal, 30% Tachycardia
        pr_choice = self.random.choices(["Normal", "Tachycardia"], weights=[70, 30])[0]
        pr = self.random.randint(60, 100) if pr_choice == "Normal" else self.random.randint(101, 115)

        # RR: RULE - Tachypnea must correlate with GOLD 3/4
        # 40% (16-18), 35% (18-20), 25% (20-22)
        if self.severity in ["GOLD_3", "GOLD_4"]:
            # High probability of tachypnea
            rr_val = self.random.randint(20, 22)
        else:
            # Normal or mild tachypnea
            rr_val = self.random.choice([self.random.randint(16, 18), self.random.randint(18, 20)])

        # SpO2: RULE - Hypoxemia (<=92%) must correlate with GOLD 3/4
        # 40% (>94), 30% (92-94), 30% (<92)
        if self.severity in ["GOLD_3", "GOLD_4"]:
             # Higher chance of < 92
            if self.random.random() < 0.6: # Bias towards hypoxemia in severe
                 spo2_val = self.random.randint(88, 92)
            else:
                 spo2_val = self.random.randint(92, 94)
        else:
            # Mild/Moderate usually > 92
            spo2_val = self.random.randint(93, 98)
        
        self.simulated_spo2_val = spo2_val # Store for logic checks

        # GCS: RULE - 13-14 applies only if GOLD 4 (Chronic Hypercapnia)
        # 95% 15, 5% 13-14
        if self.severity == "GOLD_4" and self.random.random() < 0.25: # Roughly 5% total prob if GOLD 4 is 20%
             gcs_val = self.random.randint(13, 14)
        else:
             gcs_val = 15
        
        self.simulated_gcs_val = gcs_val

        return {
            "BP": f"{sys}/{dia} mmHg",
            "T": f"{temp} °C",
            "PR": f"{pr} bpm and regular rhythm",
            "RR": f"{rr_val} breaths/min",
            "SpO2": f"{spo2_val}% (Room Air)",
            "GCS": str(gcs_val)
        }

    # --- 2. General Appearance ---
    def _gen_general_appearance(self):
        # LOC: CONSISTENCY - Drowsy only if GCS 13-14
        if self.simulated_gcs_val < 15:
            loc = "Drowsy but arousable, following simple commands."
        else:
            loc = "Alert and Oriented to Person, Place, and Time, following commands."

        # Mood & Behavior
        mood = self.random.choices(
            ["Appears Chronically Ill, Not in acute distress.", "Anxious/Apprehensive."],
            weights=[80, 20]
        )[0]
        behavior = self.random.choices(
            ["Cooperative.", "Anxious or mildly depressed."],
            weights=[80, 20]
        )[0]

        # Posture
        pos_w = [75, 15, 10] # Comfort, Upright, Tripod
        if self.severity == "GOLD_4": 
            # Tripod more likely in severe
            pos = self.random.choices(["Comfortable in bed or seated.", "Sitting upright.", "Tripod position."], weights=[40, 30, 30])[0]
        else:
            pos = self.random.choices(["Comfortable in bed or seated.", "Sitting upright.", "Tripod position."], weights=pos_w)[0]

        # Nutrition: Phenotype Rule
        if self.phenotype == "Emphysema":
            # 40% Cachectic implies 60% Normal (derived)
            nutr = self.random.choices(["Cachectic (Low BMI).", "Normal BMI."], weights=[40, 60])[0]
        else:
            # Chronic Bronchitis: 60% Normal/Obese (interpreted as normal here), 20% Obese
            nutr = self.random.choices(["Normal/Obese.", "Obese."], weights=[60, 40])[0] # Normalized weights for binary choice

        # Cyanosis: Rule - Present only if SpO2 < 92%
        if self.simulated_spo2_val < 92:
            cyan = "Central Cyanosis (Tongue/Lips) Present."
        else:
            cyan = "Absent."

        # Dyspnea: Severe correlates with GOLD 4
        if self.severity == "GOLD_4":
            dysp = "Severe dyspnea at rest."
        else:
            dysp = self.random.choices(
                ["Mild dyspnea only on exertion.", "Moderate dyspnea with minimal activity."],
                weights=[50, 50]
            )[0]

        # Edema: Depends on COR PULMONALE
        if self.cor_pulmonale == "Present":
            edema = self.random.choices(["Bilateral Pitting Edema (1+ to 3+).", "Absent."], weights=[90, 10])[0]
        else:
            edema = "Absent."

        return {
            "level_of_consciousness_mood_and_behavior": {
                "level_of_consciousness": loc,
                "mood": mood,
                "behavior": behavior
            },
            "posture_and_position": {
                "position_of_comfort": pos
            },
            "overall_appearance": {
                "nutritional_status": nutr
            },
            "cardiopulmonary_and_circulatory_clues": {
                "cyanosis": cyan,
                "dyspnea": dysp,
                "edema": edema
            }
        }

    # --- 3. Head and Neck ---
    def _gen_head_neck(self):
        # Eyes
        conjunctiva = self.random.choices(["Pink conjunctiva, Anicteric sclera.", "Pale conjunctiva."], weights=[95, 5])[0]
        
        # Mouth
        mucosa = self.random.choices(["Moist mucosa, No lesions.", "Dry mucosa."], weights=[90, 10])[0]
        
        # Neck - Carotid Bruit (10% Present)
        carotid = self.random.choices(["Absent.", "Present."], weights=[90, 10])[0]
        
        # Lymph Nodes (10% small firm)
        nodes = self.random.choices(
            ["Non-palpable or small, soft nodes.", "small (less than 1 cm), firm."],
            weights=[90, 10]
        )[0]

        return {
            "head_and_face": {
                "symmetry_and_lesions": "Symmetrical, No acute lesions or masses.",
                "tenderness": "No tenderness on palpation of the skull."
            },
            "eyes": {
                "sclera_and_conjunctiva": conjunctiva,
                "pupils_reaction": "Pupils equal, round, and reactive to light (PERRL).",
                "extraocular_movements": "Full Range of Motion."
            },
            "ears": {
                "external_and_tenderness": "Normal external appearance, No mastoid tenderness.",
                "eardrum_appearance": "Normal appearance."
            },
            "nose_and_sinuses": {
                "septum_and_discharge": self.random.choices(["Midline Septum, No purulent/bloody discharge.", "Mild mucosal swelling."], weights=[95, 5])[0],
                "sinus_tenderness": "No sinus tenderness on palpation."
            },
            "mouth_and_pharynx": {
                "oral_mucosa_and_lesions": mucosa,
                "pharynx_and_tonsils": "Non-erythematous pharynx, Tonsils non-enlarged."
            },
            "neck_and_lymphatics": {
                "inspection": "No swelling, redness, or visible masses.",
                "tracheal_position": "Midline, no deviation.",
                "thyroid_gland": "Non-enlarged, non-tender.",
                "carotid_bruit": carotid,
                "lymph_nodes_size_consistency": nodes,
                "lymph_nodes_mobility_tenderness": "Mobile and non-tender."
            }
        }

    # --- 4. Respiratory System ---
    def _gen_respiratory(self):
        # Inspection
        acc_muscles = self.random.choices(["Present (Sternocleidomastoid/Scalene use).", "Absent."], weights=[90, 10])[0]
        barrel = self.random.choices(["Symmetrical movement, Normal shape.", "Barrel Chest."], weights=[60, 40])[0]
        
        # Palpation
        expansion = self.random.choices(["Bilateral Reduced Expansion.", "Symmetrical expansion."], weights=[85, 15])[0]
        fremitus = self.random.choices(["Decreased and Symmetrical", "Normal and Symmetrical"], weights=[70, 30])[0]
        
        # Percussion
        percussion = self.random.choices(["Diffuse Hyperresonant.", "Resonant."], weights=[90, 10])[0]
        
        # Auscultation
        # Breath Sounds: Reduced intensity 85% if Phenotype is Emphysema
        if self.phenotype == "Emphysema":
            bs = self.random.choices(["Reduced intensity.", "Normal Vesicular breath sounds."], weights=[85, 15])[0]
        else:
            bs = self.random.choices(["Reduced intensity.", "Normal Vesicular breath sounds."], weights=[70, 30])[0]
            
        bs_full = f"Prolonged Expiration. {bs}"

        # Adventitious: 5% Crackles IF Cor Pulmonale
        adv_opts = ["Wheezing Diffuse.", "No Adventitious Sounds."]
        adv_weights = [50, 45] # Base weights 
        
        if self.cor_pulmonale == "Present":
            # Add crackles option
            chosen_adv = self.random.choices(
                ["Wheezing Diffuse.", "Fine Crackles.", "No Adventitious Sounds."],
                weights=[50, 5, 45]
            )[0]
        else:
            chosen_adv = self.random.choices(adv_opts, weights=[55, 45])[0] # Normalized

        return {
            "inspection": {
                "accessory_muscles": acc_muscles,
                "chest_shape_and_symmetry": barrel
            },
            "palpation": {
                "chest_expansion": expansion,
                "tactile_fremitus": fremitus
            },
            "percussion": percussion,
            "auscultation": {
                "breath_sounds_intensity": bs_full,
                "adventitious_sounds": chosen_adv
            }
        }

    # --- 5. Cardiovascular System ---
    def _gen_cardio(self):
        # JVP: Rule - >4cm in 70% if Cor Pulmonale is Present
        if self.cor_pulmonale == "Present":
            jvp = self.random.choices(["> 4 cm above sternal angle.", "< 4 cm above sternal angle."], weights=[70, 30])[0]
            heave = self.random.choices(["Right Ventricular Heave (RVH) detected.", "No heave, lift, or thrill detected."], weights=[10, 90])[0]
            murmur = self.random.choices(["Soft Systolic Murmur or S3 detected.", "No S3/S4 or Murmur."], weights=[10, 90])[0]
        else:
            jvp = "< 4 cm above sternal angle."
            heave = "No heave, lift, or thrill detected."
            murmur = "No S3/S4 or Murmur."

        # PMI
        pmi = self.random.choices(["PMI non-palpable or muffled.", "Palpable in 5th ICS MCL, Normal size."], weights=[70, 30])[0]
        
        # Heart Sounds
        s1s2 = self.random.choices(["Muffled/Distant S1 and S2.", "Normal S1 and S2."], weights=[70, 30])[0]
        
        # Peripheral Pulses (30% Tachycardic)
        pulses_qual = self.random.choices(["Normal quality.", "Tachycardic quality."], weights=[70, 30])[0]
        
        # Extremities (Cyanosis/Clubbing)
        if self.simulated_spo2_val < 92:
            ext_col = "Central Cyanosis and/or mild clubbing."
        else:
            ext_col = "No clubbing or trophic changes."
            
        # Cap Refill (Rule: >2s if Hypoxemia/Severe)
        if self.severity in ["GOLD_3", "GOLD_4"] or self.simulated_spo2_val < 92:
            crt = self.random.choices(["Capillary Refill Time < 2 seconds.", "Capillary Refill Time > 2 seconds."], weights=[85, 15])[0]
        else:
            crt = "Capillary Refill Time < 2 seconds."
            
        # Edema (Same rule as general appearance)
        if self.cor_pulmonale == "Present":
            pedal_edema = "Bilateral Pitting Edema."
        else:
            pedal_edema = "Absent."

        return {
            "JVP_assessment": jvp,
            "palpation": {
                "precordial_palpation_heave_thrill": heave,
                "pmi_assessment": pmi
            },
            "auscultation": {
                "heart_sounds_s1_s2": s1s2,
                "extra_sounds_s3_s4_murmurs": murmur
            },
            "peripheral_pulses_and_extremities": {
                "peripheral_pulses_symmetry_and_quality": f"Symmetrical and Regular. {pulses_qual}",
                "extremities_color_and_trophic_changes": ext_col,
                "extremities_temperature_and_cap_refill": f"Extremities warm, {crt}",
                "extremities_edema": pedal_edema
            }
        }

    # --- 6. Abdominal System ---
    def _gen_abdominal(self):
        # Bruits
        bruits = self.random.choices(["Absent.", "Present (Comorbidity)."], weights=[95, 5])[0]
        
        # Liver Palpation (Hepatic Congestion if Cor Pulmonale)
        if self.cor_pulmonale == "Present":
            palp = self.random.choices(
                ["No masses, Liver/Spleen non-palpable.", "Mildly palpable liver edge below the costal margin."],
                weights=[95, 5] 
            )[0]
        else:
            palp = "No masses, Liver/Spleen non-palpable."

        return {
            "inspection": "Flat/Rounded, Symmetrical, No obvious scars or masses.",
            "auscultation": {
                "bowel_sounds": "Normoactive Bowel Sounds.",
                "vascular_bruits": bruits
            },
            "percussion": {
                "general": "Tympanic throughout.",
                "organ_borders": "Liver/Spleen borders not percussed as enlarged."
            },
            "palpation": {
                "superficial_tenderness": "No superficial tenderness.",
                "deep_masses_and_organs": palp,
                "peritoneal_signs": "Absent (No Rebound Tenderness or Guarding)."
            }
        }

    # --- 7. Neurological ---
    def _gen_neuro(self):
        # Mental Status (Match General Appearance LOC)
        if self.simulated_gcs_val < 15:
            ms = "Drowsy or Mildly Confused."
        else:
            ms = "A&Ox3."
            
        # Motor
        motor_w = [70, 20, 10]
        if self.severity == "GOLD_4": # Bias for cachexia weakness
             motor = self.random.choices(
                ["Motor Strength 5/5, Normal Tone.", "Motor Strength 4/5.", "Asymmetrical weakness."],
                weights=[40, 50, 10]
             )[0]
        else:
             motor = self.random.choices(
                ["Motor Strength 5/5, Normal Tone.", "Motor Strength 4/5.", "Asymmetrical weakness."],
                weights=motor_w
             )[0]
             
        # Tremor (5%)
        tremor = self.random.choices(["Absent.", "Fine Tremor."], weights=[95, 5])[0]
        
        return {
            "mental_status_and_LOC": ms,
            "cranial_nerves": "Cranial Nerves II-XII intact.",
            "motor_strength_and_tone": motor,
            "involuntary_movements": tremor,
            "sensory_light_touch_and_pain": "Symmetrical and Intact.",
            "deep_tendon_reflexes": self.random.choices(["2+ and Symmetrical.", "Asymmetrical DTRs."], weights=[90, 10])[0],
            "coordination_and_gait": self.random.choices(["Normal coordination and Gait.", "Mild Unsteadiness or slightly broad-based Gait."], weights=[90, 10])[0]
        }

    # --- 8. Musculoskeletal ---
    def _gen_msk(self):
        # Muscles: Atrophy in 20% (Severe)
        atrophy = self.random.choices(["No obvious atrophy.", "Atrophy Present."], weights=[80, 20])[0]
        
        # ROM
        rom = self.random.choices(["Full ROM Active/Passive.", "Reduced ROM."], weights=[80, 20])[0]
        
        return {
            "inspection": {
                "joints": "No swelling, redness, or deformity.",
                "muscles": atrophy
            },
            "palpation": {
                "tenderness_and_crepitus": self.random.choices(["No tenderness or crepitus.", "Diffuse tenderness."], weights=[80, 20])[0]
            },
            "range_of_motion_active_passive": rom,
            "stability_and_function": "Stable and Functional."
        }

    def _gen_reversibility(self):
        """
        تولید خروجی تست Reversibility (پاسخ به برونکودیلاتور) بر اساس منطق آسم.
        توزیع احتمال: 80% مثبت، 10% منفی (حجمی)، 10% منفی (ثابت).
        """
        
        # تعیین نوع خروجی بر اساس وزن‌های 80، 10 و 10 درصد
        choice = self.random.choices(
            ["Positive", "Negative_Volume", "Negative_Fixed"], 
            weights=[50, 30, 20], k=1
        )[0]
        
        if choice == "Positive":
            return "FEV1 increase < 12% AND < 200 mL"
            
        elif choice == "Negative_Volume":
            return "FEV1 increase > 12% but < 200 mL"
            
        elif choice == "Negative_Fixed":
            return "FEV1 increase > 12% AND > 200 mL"
            
        return "Not Indicated"
    
    def _get_dlco_finding(self):
        """
        بر اساس فراوانی‌های مشخص شده، وضعیت DLCO را برمی‌گرداند.
        60% Reduced (< 80% predicted), 40% Normal (> 80% predicted).

        Low DLCO indicates Emphysema phenotype (Alveolar destruction).
        Normal DLCO indicates Chronic Bronchitis phenotype (Airway inflammation only).
        """
        # تعریف یافته‌ها و وزن‌های (فراوانی‌های) متناظر آن‌ها
        findings = [
            "Reduced (< 80% predicted)",   # 60% - نشان‌دهنده فنوتیپ آمفیزم
            "Normal (> 80% predicted)"     # 40% - نشان‌دهنده فنوتیپ برونشیت مزمن
        ]
        
        weights = [60, 40]
        
        # انتخاب تصادفی وضعیت
        # از 'self.random.choices' استفاده می‌شود، فرض می‌شود 'self.random' یک ماژول 'random' یا مشابه است.
        chosen_status = self.random.choices(findings, weights=weights, k=1)[0]
        
        # تولید مقدار عددی منطبق بر وضعیت انتخاب شده
        if chosen_status == "Reduced (< 80% predicted)":
            # 40% تا 79% برای وضعیت کاهش یافته
            dlco_val = self.random.randint(40, 79)
        else: # chosen_status == "Normal (> 80% predicted)"
            # 80% تا 100% برای وضعیت طبیعی
            dlco_val = self.random.randint(80, 100)
                
        # برگرداندن هر دو (متن و مقدار) برای سازگاری با ساختار داده
        return chosen_status, f"{dlco_val}% predicted"
    
    def _gen_spirometry_data(self):
        """
        تولید داده‌های اسپیرومتری (FEV1, FVC, Ratio) بر اساس الگوی COPD و GOLD Staging.
        """
        
        # 1. تعریف مقادیر پیش‌بینی شده (Predicted values)
        P_FEV1 = 3.50
        P_FVC = 4.00
        P_RATIO = 0.80 # 0.80 = 80%

        # 2. انتخاب الگوی اصلی FEV1 بر اساس GOLD Staging (50/20/30)
        # GOLD 2&3: Moderate to Severe (50%)
        # GOLD 4: Very Severe (20%)
        # GOLD 1: Mild (30%)
        pattern = self.random.choices(
            ["GOLD 2&3", "GOLD 4", "GOLD 1"], 
            weights=[50, 20, 30], k=1
        )[0]
        
        # 3. تعریف محدوده‌ها (Ranges) بر اساس الگوی انتخابی
        
        # FEV1 Ranges
        if pattern == "GOLD 2&3":
            fev1_range = (1.10, 2.80) # %Predicted: 30-79%
            fev1_comment = "# GOLD 2 & 3 (Moderate to Severe Obstruction - Most common presentation)"
            fev1_freq = "In 50% of times"
        
        elif pattern == "GOLD 4":
            fev1_range = (0.70, 1.05) # %Predicted: 20-29%
            fev1_comment = "# GOLD 4 (Very Severe Obstruction)"
            fev1_freq = "In 20% of times"
            
        elif pattern == "GOLD 1":
            fev1_range = (2.85, 3.40) # %Predicted: 80-95% (Near Normal, but Ratio still must be < 0.70)
            fev1_comment = "# GOLD 1 (Mild Obstruction)"
            fev1_freq = "In 30% of times"
            
        # FVC Logic (70% Preserved / 30% Reduced)
        fvc_range_choice = self.random.choices(
            [(3.20, 4.40, "# Usually preserved (Pure airway disease)", "In 70% of times"), 
             (2.00, 3.15, "# Reduced due to severe air trapping (Pseudorestriction)", "In 30% of times")], 
            weights=[70, 30], k=1
        )[0]
        fvc_range = (fvc_range_choice[0], fvc_range_choice[1])
        fvc_comment = fvc_range_choice[2]
        fvc_freq = fvc_range_choice[3]
        
        # 4. تولید مقادیر تصادفی FEV1 و FVC با رعایت محدودیت‌های فیزیولوژیک و تشخیصی
        
        # 4a. تولید اولیه FVC و FEV1
        FVC_val = self.random.uniform(*fvc_range)
        FEV1_val = self.random.uniform(*fev1_range)

        # 4b. اعمال دو شرط اساسی برای COPD (Ratio < 0.70) و فیزیولوژی (FEV1 <= FVC)
        
        # حلقه تضمین می‌کند که هر دو شرط رعایت شوند.
        while True:
            # 1. شرط Ratio: FEV1 / FVC MUST be < 0.70 (Hallmark of COPD)
            # FEV1_max_allowed = FVC_val * 0.69 (استفاده از 0.69 برای تضمین < 0.70)
            new_fev1_max_ratio = FVC_val * 0.69

            # 2. شرط فیزیولوژیک: FEV1 MUST be <= FVC
            new_fev1_max_physio = FVC_val
            
            # ماکسیمم FEV1 مجاز (کوچکترین مقدار بین حد بالایی بازه انتخابی، حد Ratio و FVC)
            overall_max_fev1 = min(fev1_range[1], new_fev1_max_ratio, new_fev1_max_physio)
            
            if overall_max_fev1 < fev1_range[0]:
                # اگر ماکسیمم مجاز کمتر از مینیمم بازه FEV1 باشد، یعنی FVC انتخابی خیلی پایین بوده 
                # و شرط Ratio < 0.70 را نقض می‌کند. باید FVC را افزایش دهیم.
                
                # حداقل FVC لازم برای حفظ Ratio < 0.70 با توجه به حداقل FEV1:
                min_fvc_required = fev1_range[0] / 0.69
                
                # بازتولید FVC با حداقل جدید
                FVC_val = self.random.uniform(min_fvc_required, max(fvc_range[1], min_fvc_required + 0.5))
                
                # از ابتدا تکرار می‌کنیم تا FEV1 جدید را با FVC جدید بسنجیم.
                # FEV1_val را هم موقتاً دوباره تولید می‌کنیم تا حلقه دوباره چک شود.
                FEV1_val = self.random.uniform(*fev1_range)
                continue
            
            # تولید نهایی FEV1 در بازه معتبر
            FEV1_val = self.random.uniform(fev1_range[0], overall_max_fev1)
            
            # محاسبه Ratio و خروج از حلقه
            Ratio_val = FEV1_val / FVC_val
            
            if Ratio_val < 0.70 and FEV1_val <= FVC_val:
                break
            else:
                # این حالت نباید رخ دهد، اما اگر رخ داد، دوباره امتحان می‌کنیم (به عنوان یک Fail-safe)
                continue

        # 5. محاسبه Ratio نهایی
        Ratio_val = FEV1_val / FVC_val

        # 6. تعیین کامنت و فرکانس Ratio
        ratio_comment = "# Hallmark of COPD: Post-bronchodilator ratio < 0.70"
        ratio_freq = "In 100% of times" 
        
        # 7. قالب‌بندی خروجی‌های نهایی
        
        # FEV1
        fev1_measured_str = f"{round(FEV1_val, 2)} L"
        fev1_percent_predicted = round(FEV1_val / P_FEV1 * 100)
        fev1_output = f"Measured: {fev1_measured_str}, Predicted: {P_FEV1} L, %Predicted: {fev1_percent_predicted}%"
        
        # FVC
        fvc_measured_str = f"{round(FVC_val, 2)} L"
        fvc_percent_predicted = round(FVC_val / P_FVC * 100)
        fvc_output = f"Measured: {fvc_measured_str}, Predicted: {P_FVC} L, %Predicted: {fvc_percent_predicted}%"

        # Ratio
        ratio_measured_str = f"{round(Ratio_val, 2)}"
        ratio_percent_predicted = round(Ratio_val / P_RATIO * 100)
        ratio_output = f"Measured: {ratio_measured_str}, Predicted: {P_RATIO}, %Predicted: {ratio_percent_predicted}%"

        return {
            "FEV1": f"{fev1_output}",
            "FVC": f"{fvc_output}",
            "FEV1/FVC_Ratio": f"{ratio_output}"
        }
    
    # --- 9. Paraclinic Tests ---
    def _gen_paraclinic(self):
        # CBC
        # Hb: Polycythemia Rule: 50% chance if SpO2 low AND Cor Pulmonale Present
        if self.simulated_spo2_val < 92 and self.cor_pulmonale == "Present":
            hb_choice = self.random.choices(["Normal", "Polycythemia"], weights=[50, 50])[0]
        else:
            hb_choice = self.random.choices(["Normal", "Polycythemia"], weights=[85, 15])[0]
            
        hb = self.random.uniform(12, 17) if hb_choice == "Normal" else self.random.uniform(17.1, 19.0)
        
        # WBC & Plt
        wbc = self._generate_value([{"range": (4000, 12000), "weight": 90}, {"range": (12000, 15000), "weight": 10}], is_int=True)
        plt = self._generate_value([{"range": (15, 45), "weight": 60}, {"range": (450001, 600000), "weight": 30}, {"range": (100000, 149999), "weight": 10}], is_int=True)

        # VBG
        # pH: Acidosis only for 5% GOLD 4 cases
        if self.severity == "GOLD_4" and self.random.random() < 0.25: # small chance
             ph = self.random.uniform(7.30, 7.34)
        else:
             ph_choice = self.random.choices(["Normal", "Alkalosis"], weights=[75, 20])[0]
             ph = self.random.uniform(7.35, 7.45) if ph_choice == "Normal" else self.random.uniform(7.46, 7.50)
        
        # PaO2: Consistent with SpO2/Severity
        if self.severity in ["GOLD_3", "GOLD_4"]:
            pao2 = self.random.randint(50, 65) # Hypoxemia
        else:
            pao2 = self.random.randint(65, 90)

        # HCO3: Elevated if Acidosis/Severe
        if float(ph) < 7.35 or self.severity == "GOLD_4":
            hco3 = self.random.randint(27, 32)
        else:
            hco3 = self.random.randint(22, 26)

        # BNP: Rule - Elevated 70% if Cor Pulmonale
        if self.cor_pulmonale == "Present":
             bnp = self.random.choices(["within normal range", "elevated"], weights=[30, 70])[0]
        else:
             bnp = "within normal range"

        # --- SPIROMETRY LOGIC START ---
        
        # 1. Generate Predicted Values (Reference)
        # Pred ranges selected to allow realistic measured values within requested bounds
        fvc_pred_vol = round(self.random.uniform(4.0, 5.5), 2)
        fev1_pred_vol = round(self.random.uniform(3.0, 4.5), 2)
        
        # 2. Generate Measured FVC
        # Rule: Measured 3.0 - 4.5 L, Predicted% usually > 70% (Near Normal)
        fvc_meas_vol = round(self.random.uniform(3.0, 4.5), 2)
        # Cap measured to not exceed predicted unrealistically
        if fvc_meas_vol > fvc_pred_vol: fvc_meas_vol = fvc_pred_vol
        fvc_pct = int((fvc_meas_vol / fvc_pred_vol) * 100)
        
        # 3. Generate Measured FEV1 based on GOLD Stage
        # Rule: FEV1 % Predicted must align with GOLD criteria
        target_pct_range = {
            "GOLD_1": (0.80, 0.95),
            "GOLD_2": (0.50, 0.79),
            "GOLD_3": (0.30, 0.49),
            "GOLD_4": (0.15, 0.29)
        }
        low_p, high_p = target_pct_range[self.severity]
        fev1_meas_vol = round(fev1_pred_vol * self.random.uniform(low_p, high_p), 2)
        
        # Rule: Measured range 1.0 - 3.0 L
        fev1_meas_vol = max(1.0, min(3.0, fev1_meas_vol))
        
        # Recalculate percent after clamping
        fev1_pct = int((fev1_meas_vol / fev1_pred_vol) * 100)
        
        # 4. Ratio Consistency Check
        # Rule: Ratio must be < 0.70 for COPD
        ratio = fev1_meas_vol / fvc_meas_vol
        
        if ratio >= 0.70:
            # Force adjustment to satisfy COPD definition (<0.7)
            # Typically implies increasing FVC or decreasing FEV1. 
            # Decreasing FEV1 is safer to maintain obstruction profile.
            fev1_meas_vol = round(fvc_meas_vol * self.random.uniform(0.55, 0.68), 2)
            fev1_pct = int((fev1_meas_vol / fev1_pred_vol) * 100)
            ratio = fev1_meas_vol / fvc_meas_vol
        
        # 5. Reversibility Check
        # Rule: 90% chance of being <12% AND <200mL increase
        is_reversible = self.random.choices([False, True], weights=[90, 10])[0]
        spirometry_results = self._gen_spirometry_data()
        reversibility = self._gen_reversibility()
        
        if not is_reversible:
            # Generate small increase (Non-significant)
            delta_ml = self.random.randint(10, 190) # < 200ml
            max_pct_increase = fev1_meas_vol * 0.11 # < 12%
            delta_vol_l = min(delta_ml / 1000.0, max_pct_increase)
            reversibility_str = f"Reversibility: Negative (Post-BD increase {int(delta_vol_l*1000)} mL)"
        else:
            # Significant increase (Asthma Overlap)
            delta_ml = self.random.randint(210, 400)
            delta_vol_l = delta_ml / 1000.0
            reversibility_str = f"Reversibility: Positive (Post-BD increase {delta_ml} mL)"
            
        fev1_post = round(fev1_meas_vol + delta_vol_l, 2)
        
        # Formating Strings
        fev1_str = f"Meas: {fev1_meas_vol} L ({fev1_pct}% Pred) [{self.severity}]. Post-BD: {fev1_post} L. {reversibility_str}"
        fvc_str = f"Meas: {fvc_meas_vol} L ({fvc_pct}% Pred)"
        ratio_str = f"{round(ratio, 2)}"

        # --- SPIROMETRY LOGIC END ---

        return {
            "basic_blood_tests": {
                "CBC": {
                    "Hb": f"{round(hb, 1)} g/dL",
                    "WBC": f"{wbc} /µL",
                    "Plt": f"{plt} /µL"
                },
                "ESR": self._generate_value([{"range": (5, 29), "weight": 70}, {"range": (30, 60), "weight": 30}], is_int=True) + " mm/h",
                "CRP": self._generate_value([{"range": (1, 19), "weight": 70}, {"range": (20, 50), "weight": 30}], is_int=True) + " mg/L",
                "BMP": {
                    "Na": self._generate_value([{"range": (135, 145), "weight": 85}, {"range": (128, 134), "weight": 15}], is_int=True) + " mEq/L",
                    "BUN": self._generate_value([{"range": (7, 20), "weight": 80}, {"range": (21, 35), "weight": 20}], is_int=True) + " mg/dL",
                    "Cr": self._generate_value([{"range": (0.7, 1.2), "weight": 80}, {"range": (1.3, 1.8), "weight": 20}], precision=1) + " mg/dL"
                },
                "LFTs": {
                    "ALT": self._generate_value([{"range": (22, 45), "weight": 90}, {"range": (46, 90), "weight": 10}], is_int=True) + " U/L",
                    "AST": self._generate_value([{"range": (22, 45), "weight": 90}, {"range": (46, 90), "weight": 10}], is_int=True) + " U/L"
                },
                "VBG": {
                    "pH": str(round(ph, 2)),
                    "PaO2": f"{pao2} mmHg",
                    "HCO3": f"{hco3} mEq/L"
                }
            },
            "specialized_lung_tests": {
                "Sputum_analysis": {
                    "Gram_Stain": self.random.choices(["Normal Flora / Mixed", "Positive for specific organism"], weights=[80, 20])[0],
                    "Sample_Quality": "Not Indicated for Routine Stable Visit."
                },
                "Sputum_AFB": self.random.choices(["Negative", "Positive"], weights=[95, 5])[0],
                "a1_antitrypsin_level": self.random.choices(["within normal range", "below normal range"], weights=[99, 1])[0],
                "D_dimer": self.random.choices(["< 500 ng/mL FEU", "> 500 ng/mL FEU"], weights=[90, 10])[0],
                "BNP_NT_proBNP": bnp
            },
            "immunity_and_serology": {
                "HIV_test": self.random.choices(["Negative", "Positive"], weights=[98, 2])[0],
                "Autoimmune_pannel_ANA_ANCA": self.random.choices(["Negative", "Positive"], weights=[95, 5])[0]
            },
            "simple_imaging": {
                "Chest_X_Ray": {
                    "PA_Lateral_Findings_and_Effusion": self.random.choices(["Hyperinflation findings (Flat Diaphragms)", "Bullae"], weights=[70, 30])[0]
                }
            },
            "advanced_imaging": {
                "Chest_CT_CTPA": {
                    "Lung_Parenchyma_and_Pleura": self.random.choices(["Emphysema/Air Trapping Changes", "Bullae or Bronchiectatic Changes"], weights=[70, 30])[0]
                }
            },
            "functional_tests": {
                "Spirometry": {
                    "result": spirometry_results,
                    "Reversibility": reversibility
                },
                "dlco": self._get_dlco_finding()[1],
                "peak_flow": self.random.choices(["Reduced", "within normal range"], weights=[80, 20])[0],
                "plethysmography": self.random.choices(["Increased Lung Volumes", "within normal range"], weights=[70, 30])[0]
            },
            "procedures": {
                "Bronchoscopy": "Not Indicated for Routine Stable Visit.",
                "torachonthesis": "Not Indicated and fluid cannot be aspirated."
            }
        }

    def generate_paraclinic_case(self):
        # 1. Personal Info
        personal_info = self._generate_personal_information()
        
        # 2. Vitals (Sets internal simulation state for logic checks)
        vitals = self._gen_vitals()
        
        # 3. Component Generation
        gen_app = self._gen_general_appearance()
        hn_exam = self._gen_head_neck()
        resp_exam = self._gen_respiratory()
        cv_exam = self._gen_cardio()
        abd_exam = self._gen_abdominal()
        neuro_exam = self._gen_neuro()
        msk_exam = self._gen_msk()
        paraclinic = self._gen_paraclinic()

        # 4. Assembly
        data = {
            "patient_profile": {
                "personal_information": personal_info
            },
            "physical_exam": {
                "vital_signs": vitals,
                "general_appearance": gen_app,
                "head_and_neck": hn_exam,
                "respiratory_system": resp_exam,
                "cardiovascular_system": cv_exam,
                "abdominal_system": abd_exam,
                "neurological": neuro_exam,
                "musculoskeletal_system": msk_exam
            },
            "paraclinic": paraclinic
        }
        
        return data

if __name__ == "__main__":
    import json
    generator = COPDDataGenerator()
    print(json.dumps(generator.generate_paraclinic_case(), ensure_ascii=False, indent=4))