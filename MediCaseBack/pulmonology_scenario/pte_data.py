import random

class PTEDataGenerator:
    """
    کلاسی برای تولید داده‌های شبیه‌سازی شده PTE (آمبولی ریه) بر اساس فایل PTE.txt و منطق PTE.docx.
    
    Logic Drivers (متغیرهای اصلی برای حفظ سازگاری بالینی):
    1. SEVERITY: Massive (Hemodynamically Unstable) vs Non-Massive (Stable)
       - بر اساس فایل: 40% هیپوتانسیون (Massive)، 60% فشار خون نرمال (Non-Massive/Sub-massive).
    2. RV_DYSFUNCTION: نارسایی بطن راست
       - همبستگی قوی با Massive PTE (JVD, High BNP, Loud P2).
    3. DVT_SOURCE: وجود علائم ترومبوز وریدی عمقی
       - در 40% موارد (تورم یک‌طرفه پا).
    """
    
    # لیست‌های داده‌های دموگرافیک (مشابه فایل COPD برای بومی‌سازی)
    RANDOM_DATA_LISTS = {
        "first_names_sample_100": {
            "MALE": [
                "محمد", "علی", "رضا", "حسین", "امیر", "مهدی", "سجاد", "آریا", "کیان", "پویا",
                "محسن", "جواد", "مجید", "بهنام", "فرهاد", "کوروش", "فرزاد", "سامان", "سعید", "یوسف",
                "اشکان", "داریوش", "کسری", "هومن", "آرمین", "مانی", "پارسا", "میلاد", "یاسر", "ناصر",
                "احمد", "جمال", "وحید", "مازیار", "حامد", "سینا", "عرفان", "شهرام", "مرتضی", "مصطفی"
            ],
            "FEMALE": [
                "فاطمه", "زهرا", "مریم", "سارا", "آزاده", "نگار", "لیلا", "نازنین", "مهسا", "زینب",
                "الناز", "آتوسا", "پریسا", "نسترن", "شبنم", "فریبا", "سودابه", "ژاله", "آرزو", "مهناز",
                "رویا", "محبوبه", "نسرین", "آیلین", "پگاه", "عاطفه", "حدیث", "میترا", "درسا", "هانیه"
            ]
        },
        "last_names_sample_100": [
            "محمدی", "احمدی", "کریمی", "حسینی", "رضایی", "موسوی", "فرهادی", "هاشمی", "نوری", "زارعی",
            "باقری", "صادقی", "میرزایی", "جلیلی", "افشار", "نجفی", "سلیمانی", "شریفی", "قاسمی", "ملکی",
            "رحمتی", "یزدانی", "کمالی", "طاهری", "دهقان", "اکبری", "شفیعی", "کاظمی", "فلاح", "مرادی",
            "عباسی", "یاراحمدی", "مهاجر", "نعمتی", "حیدری", "لطفی", "آذری", "صفری", "خسروی", "پورحسن"
        ],
        "occupations_male": [
            "راننده ترانزیت", "کارمند اداری (پشت میز نشین)", "بازنشسته", "مهندس عمران", 
            "آشپز", "نگهبان", "کارگر کارخانه", "معلم"
        ],
        "occupations_female": [
            "خانه‌دار", "معلم", "پرستار", "منشی", "آرایشگر", 
            "کارمند بانک", "دانشجو", "خیاط"
        ],
        "famous_cities_sample_30": [
            "تهران", "مشهد", "اصفهان", "شیراز", "تبریز", "اهواز", "کرج", "رشت", "کرمان", "یزد",
            "ساری", "بندرعباس", "کرمانشاه", "ارومیه", "زاهدان", "همدان", "قزوین", "اردبیل", "زنجان", "گرگان"
        ]
    }
    
    def __init__(self):
        self.random = random
        
        # 1. CORE LOGIC INITIALIZATION
        
        # Severity / Hemodynamic Stability
        # بر اساس فایل PTE.txt: هیپوتانسیون در 40% موارد دیده می‌شود.
        # Massive = Hypotensive + High Risk
        self.severity = self.random.choices(
            ["Massive", "Non-Massive"], 
            weights=[40, 60], k=1
        )[0]
        
        # DVT Signs (Source of Emboli)
        # بر اساس فایل: 40% تورم یا تندرنس ساق پا دارند.
        self.has_dvt = self.random.choices(
            [True, False],
            weights=[40, 60], k=1
        )[0]

        # Holders for consistency checks
        self.simulated_spo2_val = 95
        self.simulated_rr_val = 20
        self.simulated_bp_systolic = 120
        self.simulated_hr_val = 90
        # تعیین RV Dysfunction برای منطق Light's Criteria
        # Massive تقریباً همیشه RV Dysfunction دارد
        self.has_rv_dysfunction = (self.severity == "Massive") or (self.random.random() < 0.4 and self.severity != "Massive")

    # --- Helper Methods ---
    def _generate_value(self, distributions, is_int=False, precision=2):
        ranges = [d["range"] for d in distributions]
        weights = [d["weight"] for d in distributions]
        chosen_range = self.random.choices(ranges, weights=weights, k=1)[0]
        if is_int:
            val = self.random.randint(chosen_range[0], chosen_range[1])
            return str(val)
        val = self.random.uniform(chosen_range[0], chosen_range[1])
        return str(round(val, precision))

    def _generate_personal_information(self):
        gender = self.random.choice(["مرد", "زن"])
        age_num = self.random.randint(30, 85) # PTE can happen younger too, but often older
        age_str = f"{age_num} ساله"
        
        name_key = "MALE" if gender == "مرد" else "FEMALE"
        first_name = self.random.choice(self.RANDOM_DATA_LISTS["first_names_sample_100"][name_key])
        last_name = self.random.choice(self.RANDOM_DATA_LISTS["last_names_sample_100"])
        
        occ_list = self.RANDOM_DATA_LISTS["occupations_male"] if gender == "مرد" else self.RANDOM_DATA_LISTS["occupations_female"]
        occupation = self.random.choice(occ_list)
        
        birth = self.random.choice(self.RANDOM_DATA_LISTS["famous_cities_sample_30"])
        
        return {
            "first_name": first_name, "last_name": last_name, "age": age_str,
            "gender": gender, "occupation": occupation,
            "place_of_birth": birth, "place_of_residence": birth, # Simplified
            "marital_status": "متاهل"
        }

    # --- 1. Vital Signs ---
    def _gen_vitals(self):
        # BP Logic: Driven by Severity (Massive vs Non-Massive)
        # Source: "In 40% of times BP is Hypotensive (Systolic < 90)"
        if self.severity == "Massive":
            sys = self.random.randint(70, 89)
            dia = self.random.randint(40, 60)
            bp_str = f"{sys}/{dia} mmHg (Hypotensive)"
        else:
            # Non-Massive: Often normal or elevated due to pain/anxiety
            # Source: "In 60% of times BP is < 140/90 mmHg" (Normal range)
            sys = self.random.randint(110, 139)
            dia = self.random.randint(70, 89)
            bp_str = f"{sys}/{dia} mmHg"
        
        self.simulated_bp_systolic = sys

        # PR Logic: Tachycardia is main sign (80%)
        # Source: "In 80% of times > 100 bpm"
        if self.severity == "Massive":
            # Massive almost always has tachycardia to compensate CO
            pr = self.random.randint(110, 140)
        else:
            # Stable cases: 80% Tachy, 20% Normal
            pr_choice = self.random.choices(["Tachy", "Normal"], weights=[70, 30])[0]
            if pr_choice == "Tachy":
                pr = self.random.randint(101, 125)
            else:
                pr = self.random.randint(60, 99)
        
        self.simulated_hr_val = pr

        # RR Logic: Tachypnea is VERY common (95%)
        # Source: "In 95% of times > 20 breaths/min"
        rr_choice = self.random.choices(["Tachypnea", "Normal"], weights=[95, 5])[0]
        if rr_choice == "Tachypnea":
            rr = self.random.randint(22, 35) # High RR due to V/Q mismatch
        else:
            rr = self.random.randint(12, 20)
        
        self.simulated_rr_val = rr

        # SpO2 Logic: Hypoxemia
        # Source: 25% Severe (<90), 45% Moderate (90-94), 30% Normal (>94)
        # Correlation: Massive PTE usually has lower SpO2
        if self.severity == "Massive":
            spo2 = self.random.randint(80, 91)
        else:
            # Stable: Can be normal or mild
            spo2_choice = self.random.choices(["Normal", "Mild Hypoxemia"], weights=[40, 60])[0]
            if spo2_choice == "Normal":
                spo2 = self.random.randint(95, 98)
            else:
                spo2 = self.random.randint(90, 94)
        
        self.simulated_spo2_val = spo2

        # Temperature: Usually normal or low grade
        # Source: 70% Normal, 30% Low-grade fever
        temp_choice = self.random.choices(["Normal", "Low-grade"], weights=[70, 30])[0]
        if temp_choice == "Normal":
            temp = round(self.random.uniform(36.5, 37.5), 1)
        else:
            temp = round(self.random.uniform(37.6, 38.0), 1)

        # GCS: 90% Normal, 10% Altered (Shock)
        if self.severity == "Massive" and self.random.random() < 0.25: # Check if shock affects brain
            gcs = self.random.randint(13, 14)
        else:
            gcs = 15

        return {
            "BP": bp_str,
            "T": f"{temp} °C",
            "PR": f"{pr} bpm",
            "RR": f"{rr} breaths/min",
            "SpO2": f"{spo2}% (Room Air)",
            "GCS": str(gcs)
        }

    # --- 2. General Appearance ---
    def _gen_general_appearance(self):
        # LOC
        if self.simulated_bp_systolic < 90:
             loc = self.random.choices(
                 ["Alert and Oriented", "Mildly confused/Lethargic due to hypotension"], 
                 weights=[75, 25]
             )[0]
        else:
             loc = "Alert and Oriented"

        # Mood & Behavior: Anxiety is common (80%)
        mood = self.random.choices(
            ["Anxious and Distressed", "Calm/Euthymic"], 
            weights=[80, 20]
        )[0]
        
        behavior = "Restless, seeking position of comfort." if mood == "Anxious and Distressed" else "Cooperative."

        # Cyanosis: Only if severe hypoxemia
        if self.simulated_spo2_val < 90:
            cyanosis = "Central Cyanosis or Acrocyanosis present."
        elif self.simulated_bp_systolic < 90:
            cyanosis = "Pale, cool skin (Shock signs)." # Acrocyanosis
        else:
            cyanosis = "No Central or Peripheral Cyanosis."

        # Dyspnea: Very common (90%)
        dyspnea_val = "Dyspnea at rest." if self.simulated_rr_val > 20 else "No obvious dyspnea at rest."

        # Edema (General): Typically absent unless DVT or HF
        if self.has_dvt:
            edema = "Unilateral lower extremity swelling/edema."
        elif self.severity == "Massive":
            edema = "No peripheral edema (Acute event)." # RV failure acute doesn't cause instant massive edema usually, but DVT does.
        else:
            edema = "No Peripheral Edema."

        return {
            "level_of_consciousness_mood_and_behavior": {
                "level_of_consciousness": loc,
                "mood": mood,
                "behavior": behavior
            },
            "posture_and_position": {
                "position_of_comfort": "Sitting Upright/Semi-Fowler's Position (Orthopnea)."
            },
            "overall_appearance": {
                "nutritional_status": "Normal nutritional status."
            },
            "cardiopulmonary_and_circulatory_clues": {
                "cyanosis": cyanosis,
                "dyspnea": dyspnea_val,
                "edema": edema
            }
        }

    # --- 3. Head and Neck ---
    def _gen_head_neck(self):
        # Normal findings mostly
        return {
            "head_and_face": {
                "symmetry_and_lesions": "Normal and Symmetric.",
                "tenderness": "No Tenderness."
            },
            "eyes": {
                "sclera_and_conjunctiva": "Sclera White, Conjunctiva Pink.",
                "pupils_reaction": "PERRLA.",
                "extraocular_movements": "Intact."
            },
            "ears": {
                "external_and_tenderness": "Normal.",
                "eardrum_appearance": "Intact."
            },
            "nose_and_sinuses": {
                "septum_and_discharge": "Normal.",
                "sinus_tenderness": "None."
            },
            "mouth_and_pharynx": {
                "oral_mucosa_and_lesions": "Mucosa Pink and Moist.",
                "pharynx_and_tonsils": "Normal."
            },
            "neck_and_lymphatics": {
                "inspection": "Supple.",
                "tracheal_position": "Midline.",
                "thyroid_gland": "Non-palpable.",
                "carotid_bruit": "No Bruit.",
                "lymph_nodes_size_consistency": "Not Palpable.",
                "lymph_nodes_mobility_tenderness": "Not Palpable."
            }
        }

    # --- 4. Respiratory System ---
    def _gen_respiratory(self):
        # Inspection
        acc_muscles = "Accessory Muscle Use." if self.simulated_rr_val > 24 else "No Accessory Muscle Use."
        
        # Auscultation: IMPORTANT LOGIC
        # Source: "Lungs are often clear (90%)."
        # Source: "Friction rub (15%)" or "Localized crackles (10%)"
        
        lung_sounds_choice = self.random.choices(
            ["Clear to Auscultation", "Pleural Friction Rub", "Localized Crackles"],
            weights=[85, 10, 5]
        )[0]

        return {
            "inspection": {
                "accessory_muscles": acc_muscles,
                "chest_shape_and_symmetry": "Symmetrical, Normal AP Diameter."
            },
            "palpation": {
                "chest_expansion": "Normal Chest Expansion.",
                "tactile_fremitus": "Normal Tactile Fremitus."
            },
            "percussion": "Normal Resonance.",
            "auscultation": {
                "breath_sounds_intensity": "Normal Intensity.",
                "adventitious_sounds": lung_sounds_choice
            }
        }

    # --- 5. Cardiovascular System ---
    def _gen_cardio(self):
        # JVP Logic: Elevated in Massive PTE (RV Failure)
        # Source: 50% Elevated, 50% Normal
        if self.severity == "Massive":
            jvp = "Elevated JVP (> 4 cm above sternal angle) due to RV strain."
        else:
            jvp = "Normal JVP."

        # Heart Sounds: Loud P2 in Pulmonary HTN (30% total, high correlation with massive)
        if self.severity == "Massive" or self.has_rv_dysfunction:
             s2_desc = "Loud P2 component of S2 (Pulmonary Hypertension)."
             heave = "Right Ventricular Heave Palpable."
             extra = self.random.choices(["S3 Gallop (Right-sided).", "No extra sounds."], weights=[60, 40])[0]
        else:
             s2_desc = "Normal S1 and S2."
             heave = "No Heave or Thrill."
             extra = "No S3, S4, or Murmurs."

        # Peripheral Pulses
        if self.simulated_bp_systolic < 90:
            pulse_qual = "Weak/Thready Pulses."
            extremities = "Cool extremities, Capillary Refill > 2 seconds (Shock)."
        else:
            pulse_qual = "Peripheral Pulses Symmetric and 2+."
            extremities = "Extremities Warm, Capillary Refill < 2 seconds."

        # DVT Signs in Extremities (Redundant check but good for consistency)
        if self.has_dvt:
            edema_ext = "Unilateral calf swelling and tenderness (Suggests DVT)."
        else:
            edema_ext = "No lower extremity edema."

        return {
            "JVP_assessment": jvp,
            "palpation": {
                "precordial_palpation_heave_thrill": heave,
                "pmi_assessment": "PMI Non-displaced."
            },
            "auscultation": {
                "heart_sounds_s1_s2": s2_desc,
                "extra_sounds_s3_s4_murmurs": extra
            },
            "peripheral_pulses_and_extremities": {
                "peripheral_pulses_symmetry_and_quality": pulse_qual,
                "extremities_color_and_trophic_changes": "Normal color, no trophic changes.",
                "extremities_temperature_and_cap_refill": extremities,
                "extremities_edema": edema_ext
            }
        }

    # --- 6. Abdominal System ---
    def _gen_abdominal(self):
        # Hepatomegaly: Possible in RV Failure (10%)
        if (self.severity == "Massive" or self.has_rv_dysfunction) and self.random.random() < 0.3:
            liver = "Mild Hepatomegaly (due to hepatic congestion)."
        else:
            liver = "Liver Span Normal, Spleen Non-palpable."

        return {
            "inspection": "Abdomen Flat and Symmetric.",
            "auscultation": {
                "bowel_sounds": "Normoactive Bowel Sounds.",
                "vascular_bruits": "No Abdominal Vascular Bruits."
            },
            "percussion": {
                "general": "Tympanitic to Percussion.",
                "organ_borders": liver
            },
            "palpation": {
                "superficial_tenderness": "No Superficial Tenderness.",
                "deep_masses_and_оргаns": "No Deep Masses.",
                "peritoneal_signs": "No Rebound or Guarding."
            }
        }

    # --- 7. Neurological ---
    def _gen_neuro(self):
        # Consistent with General Appearance
        status = "Alert and Oriented" if self.simulated_bp_systolic >= 90 else "Mild Confusion/Disorientation"
        return {
            "mental_status_and_LOC": f"Mental Status: {status}.",
            "cranial_nerves": "Cranial Nerves II-XII Intact.",
            "motor_strength_and_tone": "Motor Strength 5/5 Bilaterally.",
            "involuntary_movements": "No Involuntary Movements.",
            "sensory_light_touch_and_pain": "Sensation Intact.",
            "deep_tendon_reflexes": "DTRs 2+ Bilaterally.",
            "coordination_and_gait": "Normal."
        }

    # --- 8. Musculoskeletal ---
    def _gen_msk(self):
        # DVT Signs focus
        if self.has_dvt:
            calf = "Calf Tenderness and Swelling."
            rom = "Full ROM, but pain on dorsiflexion of affected foot."
        else:
            calf = "No Tenderness or Swelling."
            rom = "Full Active and Passive ROM."

        return {
            "inspection": {
                "joints": "No Joint Abnormalities.",
                "muscles": "Normal Muscle Bulk."
            },
            "palpation": {
                "tenderness_and_crepitus": calf
            },
            "range_of_motion_active_passive": rom,
            "stability_and_function": "Joints Stable."
        }
        
    # --- 9. Thoracentesis Logic ---
    def _gen_thoracentesis(self):
        """
        تولید خروجی توراسنتز بر اساس منطق احتمالی (95% بدون اندیکاسیون، 3% ترانسودا، 2% اگزودا).
        """
        
        # تعیین نوع خروجی بر اساس وزن‌های 95، 3 و 2 درصد
        choice = self.random.choices(
            ["Not Indicated", "Transudate", "Exudate"], 
            weights=[95, 3, 2], k=1
        )[0]
        
        if choice == "Not Indicated":
            return "Not Indicated"
            
        elif choice == "Transudate":
            fluid_protein = round(random.uniform(0.0, 3.0), 1)
            serum_protein = round(random.uniform(6.0, 8.3), 1)
            fluid_LDH = random.randint(60, 180)
            serum_LDH = random.randint(200, 500)
            fluid_albumin = round(random.uniform(0.5, 1.5), 1)
            serum_albumin = round(random.uniform(3.5, 5.5), 1)
            return {"fluid_protein": f"{fluid_protein} g/dL", "serum_protein": f"{serum_protein} g/dL", "fluid_LDH": f"{fluid_LDH} U/L", "serum_LDH": f"{serum_LDH} U/L", "fluid_albumin": f"{fluid_albumin} g/dL", "serum_albumin": f"{serum_albumin} g/dL"}
            
        elif choice == "Exudate":
            fluid_protein = round(random.uniform(3.0, 5.5), 1)
            serum_protein = round(random.uniform(6.0, 8.3), 1)
            fluid_LDH = random.randint(210, 600)
            serum_LDH = random.randint(200, 500)
            fluid_albumin = round(random.uniform(1.6, 3.4), 1)
            serum_albumin = round(random.uniform(3.5, 5.5), 1)
            return {"fluid_protein": f"{fluid_protein} g/dL", "serum_protein": f"{serum_protein} g/dL", "fluid_LDH": f"{fluid_LDH} U/L", "serum_LDH": f"{serum_LDH} U/L", "fluid_albumin": f"{fluid_albumin} g/dL", "serum_albumin": f"{serum_albumin} g/dL"}
        
        

    def _gen_paraclinic(self):
        wbc = self._generate_value([{"range": (4500, 11000), "weight": 80}, {"range": (11000, 16000), "weight": 20}], is_int=True)
        
        ddimer_choice = self.random.choices(["> 500 ng/mL", "< 500 ng/mL"], weights=[95, 5])[0]

        if self.severity == "Massive" or self.has_rv_dysfunction:
            bnp = "Elevated."
            troponin = "Mildly Elevated." if self.random.random() < 0.6 else "Normal."
        else:
            bnp = self.random.choices(["Normal", "Mildly Elevated"], weights=[60, 40])[0]
            troponin = "Normal."

        
        if self.simulated_rr_val > 20:
            ph = str(round(self.random.uniform(7.46, 7.55), 2))
            paco2 = str(self.random.randint(25, 34))
            
            hco3_scenario = self.random.choices(
                ["Compensatory decrease", "Normal"], 
                weights=[20, 80], 
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
            paco2 = str(self.random.randint(35, 45))
            num = random.randint(22, 26)
            hco3 = f"{num} mEq/L"

        cxr = self.random.choices(
            ["Normal", "Small Pleural Effusion", "Hampton's Hump", "Westermark Sign (Oligemia)"],
            weights=[60, 25, 10, 5]
        )[0]

        ctpa = "Filling Defect."
        
        thoracentesis_result = self._gen_thoracentesis()

        return {
            "basic_blood_tests": {
                "CBC": {
                    "Hb": "14.0 g/dL",
                    "WBC": f"{wbc} /uL",
                    "Plt": "250,000 /uL"
                },
                "ESR": "< 30 mm/hr",
                "CRP": "< 10 mg/L",
                "BMP": {
                    "Na": "140 mmol/L",
                    "BUN": "15 mg/dL",
                    "Cr": "1.0 mg/dL"
                },
                "LFTs": {
                    "ALT": "30 U/L",
                    "AST": "30 U/L"
                },
                "VBG": {
                    "pH": ph,
                    "PaCO2": f"{paco2} mmHg",
                    "HCO3": f"{hco3}",
                }
            },
            "specialized_lung_tests": {
                "Sputum_analysis": {
                    "Gram_Stain": "Not Indicated",
                    "Sample_Quality": "Not Applicable"
                },
                "Sputum_AFB": "Not Applicable",
                "a1_antitrypsin_level": "Not Applicable",
                "D_dimer": ddimer_choice,
                "BNP_NT_proBNP": bnp,
                "Troponin": troponin # Added Troponin for completeness
            },
            "immunity_and_serology": {
                "HIV_test": "Not Applicable",
                "Autoimmune_pannel_ANA_ANCA": "Not Applicable"
            },
            "simple_imaging": {
                "Chest_X_Ray": {
                    "PA_Lateral_Findings_and_Effusion": cxr
                }
            },
            "advanced_imaging": {
                "Chest_CT_CTPA": {
                    "Lung_Parenchyma_and_Pleura": ctpa
                }
            },
            "functional_tests": {
                "Spirometry": {
                    "result": "Not Indicated",
                    "Reversibility": "FEV1 increase < 12% AND < 200 mL"    
                },
                "peak_flow": "Not Indicated",
                "plethysmography": "Not Indicated",
                "dlco": "Disproportionately low compared to lung volumes."
            },
            "procedures": {
                "Bronchoscopy": "Not Indicated",
                "torachonthesis": thoracentesis_result
            }
        }

    def generate_paraclinic_case(self):
        # 1. Personal Info
        personal_info = self._generate_personal_information()
        
        # 2. Vitals (Sets internal simulation state)
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
    generator = PTEDataGenerator()
    print(json.dumps(generator.generate_paraclinic_case(), ensure_ascii=False, indent=4))