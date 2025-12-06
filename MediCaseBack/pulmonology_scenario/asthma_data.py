import random

class AsthmaDataGenerator:
    """
    کلاسی برای تولید داده‌های شبیه‌سازی شده Asthma بر اساس فایل Asthma.txt و منطق آسم.docx.
    
    Logic Drivers (سه متغیر اصلی برای حفظ سازگاری):
    1. PHENOTYPE: Allergic (Eosinophilic) vs Non-Allergic
    2. CONTROL_LEVEL: Controlled vs Partially Controlled vs Uncontrolled
    3. COMPLICATIONS: Steroid Side Effects vs None
    """
    
    # --- داده‌های دموگرافیک (مشابه فایل COPD برای حفظ یکپارچگی) ---
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
            "دانشجو", "مهندس نرم‌افزار", "کارمند بانک", "معلم", "نقاش ساختمان",
            "تکنسین برق", "ورزشکار", "فروشنده", "وکیل", "معمار", "استاد دانشگاه"
        ],
        "occupations_female": [
            "خانه دار", "معلم", "پرستار", "خیاط", "حسابدار",
            "پزشک", "فروشنده", "کارمند اداری", "استاد دانشگاه", "دانشجو"
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
            "bوشهر": ["شیراز", "اهواز"],
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
        
        # 1. CORE LOGIC INITIALIZATION (Drivers based on "منطق آسم.docx")
        
        # Phenotype: Allergic (70%) vs Non-Allergic (30%)
        # تاثیر: Eosinophils, IgE, Allergic Rhinitis, Allergic Shiners
        self.phenotype = self.random.choices(
            ["Allergic", "Non-Allergic"], 
            weights=[70, 30], k=1
        )[0]
        
        # Control Level: Controlled (60%), Partially Controlled (30%), Uncontrolled (10%)
        # تاثیر: Vitals (RR, HR), Wheezing, Peak Flow, Dyspnea frequency
        self.control_level = self.random.choices(
            ["Controlled", "Partially Controlled", "Uncontrolled"],
            weights=[60, 30, 10], k=1
        )[0]
        
        # Complications: Steroid Side Effects (10%) vs None (90%)
        # تاثیر: Oral Candidiasis, Myopathy, Mild Leukocytosis
        self.complications = self.random.choices(
            ["Steroid Side Effects", "None"],
            weights=[10, 90], k=1
        )[0]

        # Holder for consistency checks
        self.simulated_spo2_val = 98
        self.simulated_rr_val = 20

    # --- Demographic Helpers ---
    def _select_occupation(self, gender, age_str):
        age = int(age_str.split()[0])
        if age > 60:
            return "بازنشسته"
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
        # Asthma can happen at any age, typically younger than COPD
        age_num = self.random.randint(20, 55) 
        age_str = f"{age_num} ساله"
        
        name_key = "MALE" if gender == "مرد" else "FEMALE"
        first_name = self.random.choice(self.RANDOM_DATA_LISTS["first_names_sample_100"][name_key])
        last_name = self.random.choice(self.RANDOM_DATA_LISTS["last_names_sample_100"])
        
        occupation = self._select_occupation(gender, age_str)
        birth = self.random.choice(self.RANDOM_DATA_LISTS["famous_cities_sample_30"])
        residence = self._select_place_of_residence(birth)
        marital = self.random.choices(["متأهل", "مجرد"], weights=[60, 40], k=1)[0]
        
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
        # BP: 90% Normal, 10% Variable
        sys = self.random.randint(100, 140)
        dia = self.random.randint(60, 90)
        
        # Temp: 95% Normal, 5% slightly high (NOT infection, minor variability)
        temp_w = [95, 5]
        temp = round(self.random.uniform(36.5, 37.5), 1) if self.random.choices([0, 1], weights=temp_w)[0] == 0 else round(self.random.uniform(37.5, 38.0), 1)

        # PR: Rule - Tachycardia (>100) in 30% (Side effect or Uncontrolled)
        if self.control_level in ["Partially Controlled", "Uncontrolled"] or self.random.random() < 0.15:
             # Higher chance of Tachycardia
             pr_choice = self.random.choices(["Normal", "Tachycardia"], weights=[50, 50])[0]
        else:
             pr_choice = "Normal"
             
        pr = self.random.randint(60, 100) if pr_choice == "Normal" else self.random.randint(101, 115)

        # RR: Rule - Tachypnea (18-22) mostly if Uncontrolled/Partially Controlled
        if self.control_level == "Controlled":
            rr_val = self.random.randint(12, 18)
        else:
            # 20% total chance of Tachypnea in logic doc
            rr_val = self.random.choices(
                [self.random.randint(12, 18), self.random.randint(18, 22)],
                weights=[60, 40]
            )[0]

        # SpO2: Rule - Mild Hypoxemia (92-94) ONLY if poor control (2% total chance)
        if self.control_level == "Uncontrolled":
            # Small chance of hypoxemia
            spo2_val = self.random.choices(
                [self.random.randint(95, 99), self.random.randint(92, 94)],
                weights=[80, 20]
            )[0]
        else:
            spo2_val = self.random.randint(95, 99)
        
        self.simulated_spo2_val = spo2_val

        rr_choice = self.random.choices(["Tachypnea", "Normal"], weights=[80, 20])[0]
        if rr_choice == "Tachypnea":
            rr = self.random.randint(12, 18) # High RR due to V/Q mismatch
        else:
            rr = self.random.randint(18, 22)
        
        self.simulated_rr_val = rr
        
        # GCS: RULE - Always 15 for stable asthma
        gcs_val = 15

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
        # LOC: Always Alert
        loc = "Alert and Oriented to Person, Place, and Time, following commands."

        # Mood & Behavior
        if self.control_level == "Controlled":
             mood = "Appears Well, Not in acute distress."
             behav = "Cooperative."
        else:
             # Mild anxiety if not fully controlled
             mood = self.random.choices(["Appears Well.", "Mildly Anxious/Apprehensive."], weights=[70, 30])[0]
             behav = self.random.choices(["Cooperative.", "Anxious."], weights=[80, 20])[0]

        # Posture
        if self.control_level == "Uncontrolled":
            pos = self.random.choices(["Comfortable in bed.", "Sitting upright."], weights=[60, 40])[0]
        else:
            pos = "Comfortable in bed or seated."

        # Nutrition: BMI can be anything
        nutr = self.random.choices(
            ["Normal weight", "Overweight", "Obese"],
            weights=[90, 5, 5]
        )[0]

        # Cyanosis: Always Absent in stable asthma
        cyan = "Absent."

        # Dyspnea: Strongly correlates with Control Level
        if self.control_level == "Controlled":
            dysp = "Absent/Mild dyspnea only on significant exertion."
        elif self.control_level == "Partially Controlled":
             dysp = "Intermittent dyspnea on minimal activity or with specific triggers."
        else: # Uncontrolled
             dysp = "Intermittent dyspnea on minimal activity."

        return {
            "level_of_consciousness_mood_and_behavior": {
                "level_of_consciousness": loc,
                "mood": mood,
                "behavior": behav
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
                "edema": "Absent."
            }
        }

    # --- 3. Head and Neck ---
    def _gen_head_neck(self):
        # Eyes: Allergic clues if Phenotype is Allergic
        if self.phenotype == "Allergic":
            # 30% chance of showing signs
            eye_finding = self.random.choices(
                ["Pink conjunctiva, Anicteric sclera.", "Mild periorbital darkening (Allergic Shiners).", "Conjunctival erythema."],
                weights=[70, 15, 15]
            )[0]
        else:
            eye_finding = "Pink conjunctiva, Anicteric sclera."
        
        # Nose: Polyps (10%) or Allergic Rhinitis (30% if Allergic)
        if self.phenotype == "Allergic":
             nose_finding = self.random.choices(
                ["Midline Septum, No discharge.", "Pale, boggy, swollen nasal mucosa with clear discharge.", "Nasal Polyps present."],
                weights=[50, 40, 10]
             )[0]
        else:
             # Non-allergic: less likely to have boggy mucosa, but polyps still possible
             nose_finding = self.random.choices(
                ["Midline Septum, No discharge.", "Nasal Polyps present."],
                weights=[90, 10]
             )[0]

        # Sinuses
        sinus = self.random.choices(["No sinus tenderness.", "Mild tenderness."], weights=[90, 10])[0]

        # Mouth: Thrush if Steroid Complications
        if self.complications == "Steroid Side Effects":
             mouth_finding = self.random.choices(
                 ["Moist mucosa, No lesions.", "Oral thrush present."],
                 weights=[50, 50]
             )[0]
        else:
             mouth_finding = "Moist mucosa, No lesions."

        # Lymph Nodes
        if self.phenotype == "Allergic":
             ln_finding = self.random.choices(
                ["Non-palpable or small, soft nodes.", "small (<1 cm), firm, mobile nodes."],
                weights=[85, 15]
             )[0]
        else:
             ln_finding = "Non-palpable or small, soft nodes."

        return {
            "head_and_face": {
                "symmetry_and_lesions": "Symmetrical, No acute lesions or masses.",
                "tenderness": "No tenderness on palpation of the skull."
            },
            "eyes": {
                "sclera_and_conjunctiva": eye_finding,
                "pupils_reaction": "Pupils equal, round, and reactive to light (PERRL).",
                "extraocular_movements": "Full Range of Motion."
            },
            "ears": {
                "external_and_tenderness": "Normal external appearance, No mastoid tenderness.",
                "eardrum_appearance": "Normal appearance."
            },
            "nose_and_sinuses": {
                "septum_and_discharge": nose_finding,
                "sinus_tenderness": sinus
            },
            "mouth_and_pharynx": {
                "oral_mucosa_and_lesions": mouth_finding,
                "pharynx_and_tonsils": "Non-erythematous pharynx, Tonsils non-enlarged."
            },
            "neck_and_lymphatics": {
                "inspection": "No swelling, redness, or visible masses.",
                "tracheal_position": "Midline, no deviation.",
                "thyroid_gland": "Non-enlarged, non-tender.",
                "carotid_bruit": "Absent.",
                "lymph_nodes_size_consistency": ln_finding,
                "lymph_nodes_mobility_tenderness": "Mobile and non-tender."
            }
        }

    # --- 4. Respiratory System ---
    def _gen_respiratory(self):
        # Inspection
        # Accessory Muscles: Only if suboptimal control
        if self.control_level in ["Partially Controlled", "Uncontrolled"]:
             acc_muscles = self.random.choices(
                 ["Absent.", "Accessory Muscles Present (Mild use)."],
                 weights=[60, 40]
             )[0]
        else:
             acc_muscles = "Absent."
             
        # Barrel Chest (10% - Longstanding)
        chest_shape = self.random.choices(["Symmetrical movement, Normal shape.", "Mild Barrel Chest."], weights=[90, 10])[0]

        # Palpation
        # Expansion: 20% Reduced (Hyperinflation)
        exp_choice = self.random.choices(["Symmetrical and Full.", "Symmetrical and Mildly Reduced Expansion."], weights=[80, 20])[0]

        # Percussion
        # Hyperresonant (20%)
        perc_choice = self.random.choices(["Resonant.", "Mild Hyperresonant."], weights=[80, 20])[0]

        # Auscultation
        # Breath Sounds
        bs_int = self.random.choices(
            ["Normal Vesicular breath sounds.", "Prolonged Expiration with normal intensity."],
            weights=[50, 50]
        )[0]

        # Adventitious: Depends on CONTROL LEVEL
        if self.control_level == "Controlled":
            adv_sounds = "Absent."
        else:
            # Partially/Uncontrolled -> High chance of Wheezing
            adv_sounds = self.random.choices(
                ["Absent.", "Wheezing Diffuse (Expiratory).", "Monophonic Wheeze (End-Expiratory)."],
                weights=[20, 60, 20]
            )[0]

        return {
            "inspection": {
                "accessory_muscles": acc_muscles,
                "chest_shape_and_symmetry": chest_shape
            },
            "palpation": {
                "chest_expansion": exp_choice,
                "tactile_fremitus": "Normal and Symmetrical."
            },
            "percussion": perc_choice,
            "auscultation": {
                "breath_sounds_intensity": bs_int,
                "adventitious_sounds": adv_sounds
            }
        }

    # --- 5. Cardiovascular System ---
    def _gen_cardio(self):
        # JVP & Heart Sounds are Normal in Asthma (unless severe attack, but this is stable visit)
        # Pulse Tachycardia Logic handled in Vitals, reflected here in description
        
        # Pulses
        if int(self._gen_vitals()["PR"].split()[0]) > 100:
             pulse_desc = "Symmetrical, Regular, and Tachycardic quality (>100 bpm)."
        else:
             pulse_desc = "Symmetrical, Regular, and Normal quality (60-100 bpm)."

        return {
            "JVP_assessment": "< 4 cm above sternal angle.",
            "palpation": {
                "precordial_palpation_heave_thrill": "No heave, lift, or thrill detected.",
                "pmi_assessment": "ormal size/strength."
            },
            "auscultation": {
                "heart_sounds_s1_s2": "Normal S1 and S2.",
                "extra_sounds_s3_s4_murmurs": "No S3/S4 or Murmur."
            },
            "peripheral_pulses_and_extremities": {
                "peripheral_pulses_symmetry_and_quality": pulse_desc,
                "extremities_color_and_trophic_changes": "No clubbing or trophic changes.",
                "extremities_temperature_and_cap_refill": "Extremities warm, Capillary Refill Time < 2 seconds.",
                "extremities_edema": "Absent."
            }
        }

    # --- 6. Abdominal System ---
    def _gen_abdominal(self):
        # Completely Normal for Asthma
        return {
            "inspection": "Flat/Rounded, Symmetrical, No obvious scars or masses.",
            "auscultation": {
                "bowel_sounds": "Normoactive Bowel Sounds.",
                "vascular_bruits": "Absent."
            },
            "percussion": {
                "general": "Tympanic throughout.",
                "organ_borders": "Liver/Spleen borders not percussed as enlarged."
            },
            "palpation": {
                "superficial_tenderness": "No superficial tenderness.",
                "deep_masses_and_organs": "No masses, Liver/Spleen non-palpable.",
                "peritoneal_signs": "Absent (No Rebound Tenderness or Guarding)."
            }
        }

    # --- 7. Neurological ---
    def _gen_neuro(self):
        # Motor: Steroid Myopathy (5-10%) only if Complications present
        if self.complications == "Steroid Side Effects":
            motor = self.random.choices(
                ["Motor Strength 5/5, Normal Tone.", "Mild proximal weakness."],
                weights=[50, 50]
            )[0]
        else:
            motor = "Motor Strength 5/5, Normal Tone."
            
        # Tremor: Beta-agonist side effect (10% General probability)
        tremor = self.random.choices(["Absent.", "Fine Tremor."], weights=[90, 10])[0]

        return {
            "mental_status_and_LOC": "A&Ox3.",
            "cranial_nerves": "Cranial Nerves II-XII intact.",
            "motor_strength_and_tone": motor,
            "involuntary_movements": tremor,
            "sensory_light_touch_and_pain": "Symmetrical and Intact.",
            "deep_tendon_reflexes": "2+ and Symmetrical.",
            "coordination_and_gait": "Normal coordination and Gait."
        }

    # --- 8. Musculoskeletal ---
    def _gen_msk(self):
        # Similar to Neuro, check for Atrophy
        if self.complications == "Steroid Side Effects":
             muscles = self.random.choices(["No obvious atrophy.", "Mild Atrophy."], weights=[60, 40])[0]
        else:
             muscles = "No obvious atrophy."

        return {
            "inspection": {
                "joints": "No swelling, redness, or deformity.",
                "muscles": muscles
            },
            "palpation": {
                "tenderness_and_crepitus": "No tenderness or crepitus."
            },
            "range_of_motion_active_passive": "Full ROM Active/Passive.",
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
            weights=[80, 10, 10], k=1
        )[0]
        
        if choice == "Positive":
            return "FEV1 increase > 12% AND > 200 mL"
            
        elif choice == "Negative_Volume":
            return "FEV1 increase > 12% but < 200 mL"
            
        elif choice == "Negative_Fixed":
            return "FEV1 increase < 12% AND < 200 mL"
            
        return "Not Indicated"

    def _gen_spirometry_data(self):
        """
        تولید داده‌های اسپیرومتری (FEV1, FVC, Ratio) بر اساس الگوهای آسم و احتمالات داده شده.
        FEV1 به عنوان درایور اصلی (60% Obstructive, 30% Normal, 10% Severe).
        """
        
        # 1. تعریف مقادیر پیش‌بینی شده (Predicted values)
        P_FEV1 = 3.50
        P_FVC = 4.00
        P_RATIO = 0.80 # 0.80 = 80%

        # 2. انتخاب الگوی اصلی FEV1 (60/30/10)
        pattern = self.random.choices(
            ["Obstructive", "Normal", "Severe Obstructive"], 
            weights=[60, 30, 10], k=1
        )[0]
        
        # 3. تعریف محدوده‌ها (Ranges) و کامنت‌ها بر اساس الگوی انتخابی
        
        # FEV1 Ranges
        if pattern == "Obstructive":
            fev1_range = (1.50, 2.80)
            fev1_comment = "# Obstructive Pattern (Acute exacerbation or uncontrolled)"
            
            # FVC is usually preserved (80%) but can be reduced due to air trapping (20%)
            fvc_range = self.random.choices([(3.20, 4.80), (2.00, 3.15)], weights=[80, 20], k=1)[0]
            if fvc_range == (3.20, 4.80):
                 fvc_comment = "# Usually preserved (Pure airway disease)"
            else:
                 fvc_comment = "# Reduced due to air trapping (Pseudorestriction)"

        elif pattern == "Normal":
            fev1_range = (2.85, 4.20)
            fev1_comment = "# Normal Pattern (Intermittent or well-controlled asthma)"
            
            # FVC must be in the preserved range for Normal Pattern
            fvc_range = (3.20, 4.80)
            fvc_comment = "# Usually preserved (Pure airway disease)"
            
        elif pattern == "Severe Obstructive":
            fev1_range = (1.00, 1.45)
            fev1_comment = "# Severe Obstruction (Severe persistent asthma)"
            
            # FVC can be preserved or reduced
            fvc_range = self.random.choices([(3.20, 4.80), (2.00, 3.15)], weights=[60, 40], k=1)[0]
            if fvc_range == (3.20, 4.80):
                 fvc_comment = "# Usually preserved (Pure airway disease)"
            else:
                 fvc_comment = "# Reduced due to air trapping (Pseudorestriction)"
                 
        # 4. تولید مقادیر تصادفی FEV1 و FVC
        FEV1_val = self.random.uniform(*fev1_range)
        FVC_val = self.random.uniform(*fvc_range)
        
        # اطمینان از سازگاری منطقی: FEV1 باید کوچکتر یا مساوی FVC باشد.
        if FEV1_val > FVC_val:
            # اگر FEV1 تصادفی بزرگتر از FVC شد، FEV1 را به کمتر از FVC تعدیل می‌کنیم.
            FEV1_val = self.random.uniform(fev1_range[0], min(FVC_val, fev1_range[1]))
            
        # 5. محاسبه Ratio از مقادیر تولید شده
        Ratio_val = FEV1_val / FVC_val

        # 6. تعیین کامنت و فرکانس Ratio بر اساس مقدار محاسبه شده
        if Ratio_val < 0.70: # مطابق با الگوی انسدادی (Obstructive)
            ratio_comment = "# Obstructive Pattern (Reduced Ratio)"
            ratio_freq = "In 70% of times"
        else: # مطابق با الگوی نرمال (Normal)
            ratio_comment = "# Normal Pattern (Intermittent/Well-controlled)"
            ratio_freq = "In 30% of times"


        # 7. قالب‌بندی خروجی‌های نهایی
        
        # FEV1
        fev1_measured_str = f"{round(FEV1_val, 2)} L"
        fev1_percent_predicted = round(FEV1_val / P_FEV1 * 100)
        
        if pattern == "Normal":
             fev1_freq = "In 30% of times"
        elif pattern == "Obstructive":
             fev1_freq = "In 60% of times"
        else: # Severe Obstructive
             fev1_freq = "In 10% of times"

        fev1_output = f"Measured: {fev1_measured_str}, Predicted: {P_FEV1} L, %Predicted: {fev1_percent_predicted}%"
        
        # FVC
        fvc_measured_str = f"{round(FVC_val, 2)} L"
        fvc_percent_predicted = round(FVC_val / P_FVC * 100)

        if fvc_comment == "# Usually preserved (Pure airway disease)":
            # این فرکانس 80% شامل حالت Normal و بخش اعظم Obstructive است
            fvc_freq = "In 80% of times"
        else:
            # این فرکانس 20% شامل بخش کمی از Obstructive و Severe Obstructive است
            fvc_freq = "In 20% of times"
            
        fvc_output = f"Measured: {fvc_measured_str}, Predicted: {P_FVC} L, %Predicted: {fvc_percent_predicted}%"

        # Ratio
        ratio_measured_str = f"{round(Ratio_val, 2)}"
        ratio_percent_predicted = round(Ratio_val / P_RATIO * 100)
        
        ratio_output = f"Measured: {ratio_measured_str}, Predicted: {P_RATIO}, %Predicted: {ratio_percent_predicted}%"

        # 8. تجمیع ساختار نهایی
        return {
            "FEV1": fev1_output,
            "FVC": fvc_output,
            "FEV1/FVC_Ratio": ratio_output
        }
    
    # --- 9. Paraclinic Tests ---
    def _gen_paraclinic(self):
        # CBC
        # WBC: Eosinophilia if Allergic; Mild Leuko if Steroid
        wbc_range = (4000, 12000)
        eos_note = ""
        
        if self.phenotype == "Allergic":
             # 40% chance of Eosinophilia in general, higher if allergic phenotype selected
             if self.random.random() < 0.6: 
                 eos_note = " with Eosinophil count elevated (>5%)."
        
        if self.complications == "Steroid Side Effects":
             # Mild Leukocytosis
             wbc_range = (11000, 14000)
             if "Eosinophil" not in eos_note:
                 eos_note = " with Neutrophil predominance."

        wbc_val = self.random.randint(wbc_range[0], wbc_range[1])
        wbc_str = f"{wbc_val} /µL"

        if self.phenotype == "Allergic":
             tot_ige = self.random.choices(["Elevated (>100 IU/mL)", "within normal range"], weights=[80, 20])[0]
             spec_ige = self.random.choices(["Positive to common environmental allergens", "Negative"], weights=[80, 20])[0]
        else:
             tot_ige = "within normal range."
             spec_ige = "Negative."

        if self.phenotype == "Allergic":
             sputum_gram = self.random.choices(["Normal Flora / Mixed.", "Eosinophils present."], weights=[70, 30])[0]
        else:
             sputum_gram = "Normal Flora / Mixed."

        cxr = self.random.choices(
            ["Normal Lung Fields, Clear Costophrenic Angles.", "Mild Hyperinflation (Flat Diaphragms)."],
            weights=[80, 20]
        )[0]
        
        ct = self.random.choices(
            ["Normal.", "Mild peribronchial thickening.", "Air trapping on expiratory views."],
            weights=[70, 15, 15]
        )[0]

        fev1_pred = self.random.randint(60, 95)
        reversibility = self._gen_reversibility()
        spirometry_results = self._gen_spirometry_data()
        
        if self.simulated_rr_val > 20:
            ph = str(round(self.random.uniform(7.45, 7.60), 2))
            paco2 = str(self.random.randint(30, 40))
            
            hco3_scenario = self.random.choices(
                ["Compensatory decrease", "Normal"], 
                weights=[10, 90], 
                k=1
            )[0]

            if hco3_scenario == "Compensatory decrease":
                num = random.randint(18, 21)
                hco3 = f"{num} mEq/L"
            else:
                num = random.randint(22, 26)
                hco3 = f"{num} mEq/L"
                
            
        else:
            ph = str(round(self.random.uniform(7.35, 7.45), 2))
            paco2 = str(self.random.randint(45, 50))
            num = random.randint(22, 26)
            hco3 = f"{num} mEq/L"
        
        if self.control_level == "Controlled":
             pf = "within normal range."
        else:
             pf = "Reduced (compared to predicted) with significant diurnal variability."

        return {
            "basic_blood_tests": {
                "CBC": {
                    "Hb": f"{self.random.randint(12, 17)} g/dL",
                    "WBC": wbc_str,
                    "Plt": f"{self.random.randint(15, 45)*10000} /µL"
                },
                "ESR": "less than 20 mm/h.",
                "CRP": "less than 10 mg/L.",
                "BMP": {
                    "Na": "135-145 mEq/L.",
                    "BUN": "7-20 mg/dL.",
                    "Cr": "0.7-1.2 mg/dL."
                },
                "LFTs": {
                    "ALT": "within normal range.",
                    "AST": "within normal range."
                },
                "VBG": {
                    "pH": f"{ph}",
                    "PaO2": f"{paco2}",
                    "HCO3": f"{hco3}"
                }
            },
            "specialized_lung_tests": {
                "Sputum_analysis": {
                    "Gram_Stain": sputum_gram,
                    "Sample_Quality": "Not Indicated for Routine Stable Visit."
                },
                "Sputum_AFB": "Negative.",
                "a1_antitrypsin_level": "within normal range.",
                "D_dimer": "less than 500 ng/mL FEU.",
                "BNP_NT_proBNP": "within normal range."
            },
            "immunity_and_serology": {
                "HIV_test": "Negative",
                "Autoimmune_pannel_ANA_ANCA": "Negative",
                "Total_IgE": tot_ige,
                "Specific_IgE_Rast_Test": spec_ige
            },
            "simple_imaging": {
                "Chest_X_Ray": {
                    "PA_Lateral_Findings_and_Effusion": cxr
                }
            },
            "advanced_imaging": {
                "Chest_CT_CTPA": {
                    "Lung_Parenchyma_and_Pleura": ct
                }
            },
            "functional_tests": {
                "Spirometry": {
                    "result": spirometry_results,
                    "Reversibility": reversibility
                },
                "peak_flow": pf,
                "plethysmography": self.random.choices(["within normal range.", "Mildly Increased Residual Volume (RV)."], weights=[70, 30])[0]
            },
            "procedures": {
                "Bronchoscopy": "Not Indicated.",
                "torachonthesis": "Not Indicated."
            }
        }

    def generate_paraclinic_case(self):
        personal_info = self._generate_personal_information()
        
        vitals = self._gen_vitals()
        
        gen_app = self._gen_general_appearance()
        hn_exam = self._gen_head_neck()
        resp_exam = self._gen_respiratory()
        cv_exam = self._gen_cardio()
        abd_exam = self._gen_abdominal()
        neuro_exam = self._gen_neuro()
        msk_exam = self._gen_msk()
        paraclinic = self._gen_paraclinic()

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
