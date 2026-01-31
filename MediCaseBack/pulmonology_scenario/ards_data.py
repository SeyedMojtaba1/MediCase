import random

class ARDSDataGenerator:
    """
    کلاسی برای تولید داده‌های شبیه‌سازی شده ARDS بر اساس فایل ARDS.txt و منطقARDS.docx.
    
    Logic Drivers (دو متغیر اصلی برای حفظ سازگاری):
    1. ETIOLOGY: Infectious/Sepsis (60-70%) vs Non-Infectious/Trauma (30-40%)
       - تأثیر بر: Temperature, WBC, Sputum, Shock Type (Warm vs Cold).
       
    2. STAGE: Early/Compensated (40-50%) vs Late/Shock (50-60%)
       - تأثیر بر: BP, GCS, pH (Alkalosis vs Acidosis), Skin condition.
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
        
        # Etiology: Infectious (Sepsis/Pneumonia) vs Non-Infectious (Trauma/Pancreatitis)
        # Weights: 65% Infectious, 35% Non-Infectious (approx from docs)
        self.etiology = self.random.choices(
            ["Infectious", "Non-Infectious"], 
            weights=[65, 35], k=1
        )[0]
        
        # Clinical Stage: Early/Compensated vs Late/Shock
        # Weights: 45% Early, 55% Late
        self.stage = self.random.choices(
            ["Early", "Late"],
            weights=[45, 55], k=1
        )[0]

        # Holder for consistency checks to pass between methods
        self.simulated_temp_val = 37.0
        self.simulated_sbp_val = 120
        self.simulated_gcs_val = 15
        self.simulated_spo2_val = 88

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
        # ARDS can happen at any age, but skewed older or trauma young adults. Keeping generic range.
        age_num = self.random.randint(25, 85)
        age_str = f"{age_num} ساله"
        
        name_key = "MALE" if gender == "مرد" else "FEMALE"
        first_name = self.random.choice(self.RANDOM_DATA_LISTS["first_names_sample_100"][name_key])
        last_name = self.random.choice(self.RANDOM_DATA_LISTS["last_names_sample_100"])
        
        occupation = self._select_occupation(gender, age_str)
        birth = self.random.choice(self.RANDOM_DATA_LISTS["famous_cities_sample_30"])
        residence = self._select_place_of_residence(birth)
        marital = self.random.choices(["متأهل", "همسر متوفی", "مجرد"], weights=[60, 20, 20], k=1)[0]
        
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
        # BP: Dependent on Stage
        if self.stage == "Late":
            # Hypotension/Shock
            sys = self.random.randint(70, 89)
            dia = self.random.randint(40, 60)
            bp_str = f"{sys}/{dia} mmHg"
        else:
            # Early: HTN (Stress) or Normal
            if self.random.random() < 0.6: # HTN
                sys = self.random.randint(141, 160)
                dia = self.random.randint(85, 100)
                bp_str = f"{sys}/{dia} mmHg"
            else: # Normal
                sys = self.random.randint(110, 139)
                dia = self.random.randint(70, 85)
                bp_str = f"{sys}/{dia} mmHg"
        
        self.simulated_sbp_val = sys

        # T: Dependent on Etiology
        if self.etiology == "Infectious":
            # High Fever
            temp = round(self.random.uniform(38.1, 40.0), 1)
            t_str = f"{temp} °C"
        else:
            # Normal or slight elevation (Stress/SIRS)
            temp = round(self.random.uniform(36.5, 37.8), 1)
            t_str = f"{temp} °C"
            
        self.simulated_temp_val = temp

        # PR: Universal Tachycardia
        pr_val = self.random.randint(105, 135)
        pr_str = f"{pr_val} bpm"

        # RR: Severe Tachypnea
        # Rare pre-arrest bradypnea handled by weight
        is_bradypnea = self.random.choices([True, False], weights=[5, 95])[0]
        if is_bradypnea and self.stage == "Late":
            rr_val = self.random.randint(8, 11)
            rr_str = f"{rr_val} breaths/min (Respiratory Fatigue)"
        else:
            rr_val = self.random.randint(26, 45)
            rr_str = f"{rr_val} breaths/min"

        # SpO2: Refractory Hypoxemia
        if self.stage == "Early":
            spo2 = self.random.randint(88, 92)
            spo2_str = f"{spo2}% (Room Air)"
        else:
            spo2 = self.random.randint(75, 87)
            spo2_str = f"{spo2}% (Room Air - Refractory)"
        
        self.simulated_spo2_val = spo2

        # GCS: Dependent on Stage
        if self.stage == "Late":
             gcs = self.random.randint(3, 13)
        else:
             gcs = 15
        
        self.simulated_gcs_val = gcs

        return {
            "BP": bp_str,
            "T": t_str,
            "PR": pr_val,
            "RR": rr_str,
            "SpO2": spo2_str,
            "GCS": f"{gcs}"
        }

    # --- 2. General Appearance ---
    def _gen_general_appearance(self):
        # LOC
        if self.simulated_gcs_val == 15:
            loc = "Alert but extremely Anxious."
            mood = "Extremely Anxious/Fear of death."
            beh = "Visible struggle to breathe (Air Hunger)."
            pos = "Tripod position (if not intubated)."
        else:
            if self.simulated_gcs_val > 8:
                loc = "Confused/Agitated due to hypoxia."
                mood = "Distressed/Combative."
                beh = "Restless."
                pos = "Supine/Semi-fowlers."
            else:
                loc = "Obtunded/Unresponsive."
                mood = "Not assessable."
                beh = "Lethargic/Comatose."
                pos = "Supine (passive)."

        # Cyanosis
        if self.simulated_spo2_val < 88:
            cyan = "Central Cyanosis present."
        else:
            cyan = "Mild peripheral cyanosis or Absent."

        # Edema: Non-cardiogenic, so usually spare periphery unless Sepsis Leak
        if self.etiology == "Infectious" and self.stage == "Late":
            edema = "Generalized edema."
        else:
            edema = "No significant peripheral edema."

        return {
            "level_of_consciousness_mood_and_behavior": {
                "level_of_consciousness": loc,
                "mood": mood,
                "behavior": beh
            },
            "posture_and_position": {
                "position_of_comfort": pos
            },
            "overall_appearance": {
                "nutritional_status": "Variable based on comorbidities."
            },
            "cardiopulmonary_and_circulatory_clues": {
                "cyanosis": cyan,
                "dyspnea": "Severe dyspnea at rest (Air Hunger).",
                "edema": edema
            }
        }

    # --- 3. Head and Neck ---
    def _gen_head_neck(self):
        # Mucosa: Dry if Sepsis/Dehydration
        if self.etiology == "Infectious":
            mucosa = "Dry mucosa."
        else:
            mucosa = "Moist mucosa."
            
        # Nasal Flaring: Universal in ARDS
        flaring = "Nasal flaring present."

        # JVP: CRITICAL RULE - Must be flat to differentiate from CHF
        jvp = "Flat neck veins (JVP < 8 cmH2O)"

        return {
            "head_and_face": {
                "symmetry_and_lesions": "Symmetrical, No acute lesions.",
                "tenderness": "Non-tender."
            },
            "eyes": {
                "sclera_and_conjunctiva": "Normal.",
                "pupils_reaction": "PERRLA.",
                "extraocular_movements": "Intact."
            },
            "ears": {
                "external_and_tenderness": "Normal.",
                "eardrum_appearance": "Normal."
            },
            "nose_and_sinuses": {
                "septum_and_discharge": flaring,
                "sinus_tenderness": "No sinus tenderness."
            },
            "mouth_and_pharynx": {
                "oral_mucosa_and_lesions": mucosa,
                "pharynx_and_tonsils": "Non-erythematous."
            },
            "neck_and_lymphatics": {
                "inspection": jvp,
                "tracheal_position": "Midline.",
                "thyroid_gland": "Non-enlarged.",
                "carotid_bruit": "Absent.",
                "lymph_nodes_size_consistency": "No lymphadenopathy.",
                "lymph_nodes_mobility_tenderness": "Not applicable."
            }
        }

    # --- 4. Respiratory System ---
    def _gen_respiratory(self):
        # Inspection
        acc = "Prominent use of accessory muscles (Sternocleidomastoid/Scalene)."
        
        # Palpation
        fremitus = self.random.choices(["Increased.", "Normal."], weights=[60, 40])[0]
        
        # Percussion
        perc = "Dullness to percussion."
        
        # Auscultation
        # Crackles are Hallmark
        adv = "Diffuse Crackles (Rales) bilaterally."
        bs = "Bronchial breath sounds over dependent areas."

        return {
            "inspection": {
                "accessory_muscles": acc,
                "chest_shape_and_symmetry": "Symmetrical chest wall."
            },
            "palpation": {
                "chest_expansion": "Symmetrical expansion.",
                "tactile_fremitus": fremitus
            },
            "percussion": perc,
            "auscultation": {
                "breath_sounds_intensity": bs,
                "adventitious_sounds": adv
            }
        }

    # --- 5. Cardiovascular System ---
    def _gen_cardio(self):
        # Heart Sounds
        # No S3 is critical for ARDS dx vs CHF
        s3 = "No S3 gallop." 
        rhythm = "Tachycardic, Regular rhythm."

        # Perfusion / Extremities
        # Depends on Shock Type (Warm vs Cold)
        # Infectious often Warm (Early) or Cold (Late). Trauma often Cold.
        
        if self.etiology == "Infectious" and self.stage == "Early":
            # Warm Shock
            pulses = "Bounding pulses."
            ext_temp = "Extremities warm and flushed."
            cap_refill = "Capillary Refill < 2 seconds."
        else:
            # Cold Shock (Late Sepsis or Trauma)
            pulses = "Weak/Thready pulses."
            ext_temp = "Extremities cool/mottled."
            cap_refill = "Capillary Refill > 3 seconds."

        return {
            "JVP_assessment": "Not elevated.",
            "palpation": {
                "precordial_palpation_heave_thrill": "No heaves or thrills.",
                "pmi_assessment": "Normal location and size."
            },
            "auscultation": {
                "heart_sounds_s1_s2": rhythm,
                "extra_sounds_s3_s4_murmurs": s3
            },
            "peripheral_pulses_and_extremities": {
                "peripheral_pulses_symmetry_and_quality": f"Symmetrical. {pulses}",
                "extremities_color_and_trophic_changes": "No clubbing.",
                "extremities_temperature_and_cap_refill": f"{ext_temp} {cap_refill}",
                "extremities_edema": "Absent/Trace."
            }
        }

    # --- 6. Abdominal System ---
    def _gen_abdominal(self):
        # Sepsis/Ileus adjustments
        if self.etiology == "Infectious":
            bs = self.random.choices(["Hypoactive/Absent.", "Normoactive."], weights=[40, 60])[0]
        else:
            bs = "Normoactive."

        return {
            "inspection": "Flat/Rounded, No distension.",
            "auscultation": {
                "bowel_sounds": bs,
                "vascular_bruits": "Absent."
            },
            "percussion": {
                "general": "Tympanic.",
                "organ_borders": "Normal liver span."
            },
            "palpation": {
                "superficial_tenderness": "Non-tender.",
                "deep_masses_and_organs": "No organomegaly.",
                "peritoneal_signs": "Absent."
            }
        }

    # --- 7. Neurological ---
    def _gen_neuro(self):
        # Consistency with General Appearance/GCS
        if self.simulated_gcs_val == 15:
            status = "A&Ox3. Anxious."
        elif self.simulated_gcs_val > 8:
            status = "Confused / Delirious."
        else:
            status = "Unresponsive / Comatose."

        # Critical Illness Myopathy (Weakness)
        motor = self.random.choices(["Normal strength.", "Generalized weakness."], weights=[80, 20])[0]

        return {
            "mental_status_and_LOC": status,
            "cranial_nerves": "Intact.",
            "motor_strength_and_tone": motor,
            "involuntary_movements": "None.",
            "sensory_light_touch_and_pain": "Intact.",
            "deep_tendon_reflexes": "2+ Symmetrical.",
            "coordination_and_gait": "Not assessable."
        }

    # --- 8. Musculoskeletal ---
    def _gen_msk(self):
        return {
            "inspection": {
                "joints": "Normal.",
                "muscles": "Normal."
            },
            "palpation": {
                "tenderness_and_crepitus": "Non-tender."
            },
            "range_of_motion_active_passive": "Full Passive ROM.",
            "stability_and_function": "Bedbound."
        }

    def _get_dlco_finding(self):
        """
        بر اساس فراوانی‌های مشخص شده، وضعیت DLCO را برمی‌گرداند.
        90% Reduced (< 80% predicted), 10% Normal.
        """
        # تعریف یافته‌ها و وزن‌های (فراوانی‌های) متناظر آن‌ها
        findings = [
            "Reduced (< 80% predicted)",  # 90%
            "Normal"                     # 10%
        ]
        
        weights = [90, 10]
        
        # انتخاب تصادفی وضعیت
        chosen_status = self.random.choices(findings, weights=weights, k=1)[0]
        
        # تولید مقدار عددی منطبق بر وضعیت انتخاب شده
        if chosen_status == "Reduced (< 80% predicted)":
            dlco_val = self.random.randint(40, 79)
        else:
            dlco_val = self.random.randint(80, 100)
            
        # برگرداندن هر دو (متن و مقدار) برای سازگاری با ساختار داده
        return chosen_status, f"{dlco_val}% predicted"

    # در داخل کلاس PHDataGenerator

    # def _get_spirometry_data(self):
    #     """
    #     تولید داده‌های FEV1, FVC و FEV1/FVC Ratio بر اساس وابستگی‌های اعلام شده.
    #     این داده‌ها عمدتاً برای Group 1 PAH (بیماری عروقی خالص) معتبر هستند.
    #     """
        
    #     # مقادیر مرجع (Predicted) را با اندکی تغییر در رنج‌های شما تعریف می‌کنیم
    #     # این مقادیر فقط برای محاسبه 'Measured' استفاده می‌شوند.
    #     pred_fev1_val = self.random.uniform(3.50, 3.80) # حول و حوش 3.65 L
    #     pred_fvc_val = self.random.uniform(4.30, 4.70)  # حول و حوش 4.50 L
    #     pred_ratio_val = self.random.uniform(0.79, 0.83) # حول و حوش 0.81
        
    #     # --- FEV1 Logic (80/20) ---
    #     fev1_pct_choices = [
    #         (self.random.uniform(80.0, 120.0), (2.90, 4.40), "80-120%"), # 80%
    #         (self.random.uniform(60.0, 79.0), (2.20, 2.90), "60-79%")   # 20%
    #     ]
    #     fev1_pct, fev1_range, fev1_pct_text = self.random.choices(fev1_pct_choices, weights=[80, 20], k=1)[0]
    #     meas_fev1 = self.random.uniform(fev1_range[0], fev1_range[1]) # انتخاب مقدار Measured از رنج درخواستی
        
    #     # --- FVC Logic (80/20) ---
    #     fvc_pct_choices = [
    #         (self.random.uniform(80.0, 120.0), (3.60, 5.40), "80-120%"), # 80%
    #         (self.random.uniform(60.0, 79.0), (2.70, 3.55), "60-79%")   # 20%
    #     ]
    #     fvc_pct, fvc_range, fvc_pct_text = self.random.choices(fvc_pct_choices, weights=[80, 20], k=1)[0]
    #     meas_fvc = self.random.uniform(fvc_range[0], fvc_range[1]) # انتخاب مقدار Measured از رنج درخواستی

    #     # --- Ratio Logic (100%) ---
    #     meas_ratio = self.random.uniform(0.70, 0.85)
        
    #     # در صورت وجود بیماری زمینه‌ای (Group 3)، باید این مقادیر تعدیل شوند
    #     if self.ph_group.startswith("Group 3"):
    #         if "ILD" in self.ph_group:
    #             # الگوی محدودیت (Restriction): FVC و FEV1 کاهش یافته، نسبت نرمال یا بالا
    #             meas_fvc = self.random.uniform(0.5 * pred_fvc_val, 0.79 * pred_fvc_val)
    #             meas_ratio = self.random.uniform(0.80, 0.95)
    #             meas_fev1 = meas_fvc * meas_ratio # حفظ تناسب
    #             fev1_pct_text = fvc_pct_text = "50-79%"
    #         elif "COPD" in self.ph_group:
    #             # الگوی انسداد (Obstruction): FEV1 کاهش یافته، نسبت پایین
    #             meas_ratio = self.random.uniform(0.40, 0.69)
    #             meas_fev1 = self.random.uniform(0.4 * pred_fev1_val, 0.79 * pred_fev1_val)
    #             meas_fvc = meas_fev1 / meas_ratio # حفظ تناسب
    #             fev1_pct_text = "40-79%"
    #             fvc_pct_text = "80-100%"
                
        
    #     # ساختار خروجی مطابق با جزئیات درخواستی
    #     return {
    #         "FEV1": f"Measured: {meas_fev1:.2f} L, Predicted: {pred_fev1_val:.2f} L, %Predicted: {fev1_pct_text}",
    #         "FVC": f"Measured: {meas_fvc:.2f} L, Predicted: {pred_fvc_val:.2f} L, %Predicted: {fvc_pct_text}",
    #         "FEV1/FVC_Ratio": f"Measured: {meas_ratio:.2f}, Predicted: {pred_ratio_val:.2f}, %Predicted: {(meas_ratio/pred_ratio_val)*100:.0f}%"
    #     }
    
    # در داخل کلاس PHDataGenerator
    def _gen_functional_tests(self):
        """
        تولید مقادیر عددی برای تست‌های عملکرد ریه و سایر تست‌های عملکردی.
        """
        
        # فراخوانی متد جدید برای تولید داده‌های اسپیرومتری
        # spirometry_data = self._get_spirometry_data()
        
        # فراخوانی متد DLCO (اگر آن را به یک متد مجزا تبدیل کرده باشید)
        dlco_status, dlco_value = self._get_dlco_finding() 
        
        # --- 3. Other Tests (Simple Values) ---
        pef_val = self.random.choices(
            ["Normal PEF", "Reduced PEF"], 
            weights=[80, 20], k=1
        )[0]
        
        # Plethysmography
        pleth_val = self.random.choices(
            ["Normal Lung Volumes", "Abnormal Lung Volumes"], 
            weights=[80, 20], k=1
        )[0]

        # --- Constructing the Dictionary based on your required structure ---
        return {
            # "spirometry": {
            #     "FEV1": spirometry_data["FEV1"],
            #     "FVC": spirometry_data["FVC"],
            #     "FEV1/FVC_Ratio": spirometry_data["FEV1/FVC_Ratio"]
            # }, 
            "dlco": dlco_value,
            "peak_flow": pef_val,
            "plethysmography": pleth_val
        }

    # --- 9. Paraclinic Tests ---
    def _gen_paraclinic(self):
        # CBC
        # WBC: High in Infectious, Normal/Stress in Trauma
        if self.etiology == "Infectious":
            wbc_val = self.random.randint(13000, 25000)
            wbc_str = f"{wbc_val} /µL"
        else:
            wbc_val = self.random.randint(4500, 11000)
            wbc_str = f"{wbc_val} /µL"

        # Hb: Low in Trauma
        if self.etiology == "Non-Infectious" and self.random.random() < 0.7:
             hb = round(self.random.uniform(7.0, 9.5), 1)
             hb_str = f"{hb} g/dL"
        else:
             hb = round(self.random.uniform(12.0, 15.0), 1)
             hb_str = f"{hb} g/dL"

        # VBG/ABG Logic
        # pH: Early -> Alkalosis, Late -> Acidosis
        if self.stage == "Early":
            ph = round(self.random.uniform(7.46, 7.55), 2)
            ph_str = f"{ph}"
            pco2 = self.random.randint(25, 34) # Hypocapnia
            hco3 = self.random.randint(22, 26)
        else:
            ph = round(self.random.uniform(7.15, 7.34), 2)
            ph_str = f"{ph}"
            pco2 = self.random.randint(45, 60) # Possible retention or metabolic comp failure
            hco3 = self.random.randint(15, 21) # Metabolic acidosis component

        # Sputum Logic
        if self.etiology == "Infectious":
             gram = "Positive for bacteria."
             sp_qual = "Purulent."
        else:
             gram = "Negative."
             sp_qual = "Clear/Mucoid or Bloody."

        # Renal Function (Cr)
        if self.stage == "Late":
             cr = round(self.random.uniform(1.5, 3.5), 1)
             cr_str = f"{cr} mg/dL (AKI)"
        else:
             cr = round(self.random.uniform(0.7, 1.2), 1)
             cr_str = f"{cr} mg/dL"

        return {
            "basic_blood_tests": {
                # ... (سایر تست‌های خون طبق کد اصلی) ...
                "CBC": {
                    "Hb": hb_str,
                    "WBC": wbc_str,
                    "Plt": self._generate_value([{"range": (100000, 300000), "weight": 100}], is_int=True) + " /µL"
                },
                "ESR": self._generate_value([{"range": (30, 80), "weight": 80}, {"range": (10, 29), "weight": 20}], is_int=True) + " mm/h",
                "CRP": "Elevated (> 50 mg/L).",
                "BMP": {
                    "Na": self._generate_value([{"range": (135, 145), "weight": 90}], is_int=True) + " mEq/L",
                    "BUN": self._generate_value([{"range": (20, 40), "weight": 100}], is_int=True) + " mg/dL",
                    "Cr": cr_str
                },
                "LFTs": {
                    "ALT": "Mild elevation or Shock Liver (if hypotension).",
                    "AST": "Mild elevation."
                },
                "VBG": {
                    "pH": ph_str,
                    "PaO2": f"{self.random.randint(50, 65)} mmHg",
                    "HCO3": f"{hco3} mEq/L"
                }
            },
            "specialized_lung_tests": {
                "Sputum_analysis": {
                    "Gram_Stain": gram,
                    "Sample_Quality": sp_qual
                },
                "Sputum_AFB": "Negative.",
                "a1_antitrypsin_level": "Normal.",
                "D_dimer": "Elevated.",
                "BNP_NT_proBNP": "Normal (< 100 pg/mL) - Rules out CHF."
            },
            "immunity_and_serology": {
                "HIV_test": "Negative",
                "Autoimmune_pannel_ANA_ANCA": "Negative"
            },
            "simple_imaging": {
                "Chest_X_Ray": {
                    "PA_Lateral_Findings_and_Effusion": "Bilateral Diffuse Opacities. Costophrenic angles spared."
                }
            },
            "advanced_imaging": {
                "Chest_CT_CTPA": {
                    "Lung_Parenchyma_and_Pleura": "Diffuse ground-glass opacification and dependent consolidation."
                }
            },
            "functional_tests": self._gen_functional_tests(),
            "procedures": {
                "Bronchoscopy": "Not routinely performed.",
                "torachonthesis": "Not indicated (No significant effusion)."
            }
        }

    def generate_paraclinic_case(self):
        # 1. Personal Info
        personal_info = self._generate_personal_information()
        
        # 2. Vitals
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
