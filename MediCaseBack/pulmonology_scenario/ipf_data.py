import random

class IPFDataGenerator:
    """
    کلاسی برای تولید داده‌های شبیه‌سازی شده IPF (فیبروز ریوی ایدیوپاتیک).
    
    Logic Drivers (بر اساس فایل منطق IPF.docx و IPF.txt):
    1. DISEASE_SEVERITY: 
       - Mild (Early): SpO2 > 94%, FVC > 80%
       - Moderate: SpO2 90-94%, FVC 50-80%
       - Severe (Advanced): SpO2 < 90%, FVC < 50%
    2. COR_PULMONALE:
       - عارضه مراحل پیشرفته (Severe) که منجر به JVD و ادم می‌شود.
    """
    
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
            "بازنشسته", "نجار", "کشاورز", "کارگر ساختمانی", "معلم بازنشسته", 
            "راننده کامیون", "مهندس معدن (بازنشسته)", "آهنگر"
        ],
        "occupations_female": [
            "خانه‌دار", "معلم بازنشسته", "خیاط", "فرشباف", "پرستار بازنشسته", 
            "آشپز", "کشاورز"
        ],
        "famous_cities_sample_30": [
            "تهران", "مشهد", "اصفهان", "شیراز", "تبریز", "اهواز", "کرج", "رشت", "کرمان", "یزد",
            "ساری", "بندرعباس", "کرمانشاه", "ارومیه", "زاهدان", "همدان", "قزوین", "اردبیل", "زنجان", "گرگان"
        ]
    }
    
    def __init__(self):
        self.random = random
        
        # 1. CORE LOGIC INITIALIZATION
        # --- NEW SPO2-BASED SEVERITY DISTRIBUTION ---
        # SpO2 > 94% (Mild/Early): 30%
        # SpO2 90-94% (Moderate): 45%
        # SpO2 < 90% (Severe/Advanced): 25%
        spo2_at_rest = self.random.choices(
            ["Mild", "Moderate", "Severe"],
            weights=[30, 45, 25], k=1
        )[0]
        
        if spo2_at_rest == "Mild":
            self.simulated_spo2_val = self.random.randint(95, 98) # >94%
        elif spo2_at_rest == "Moderate":
            self.simulated_spo2_val = self.random.randint(90, 94)
        else:
            self.simulated_spo2_val = self.random.randint(84, 89) # <90%

        # FVC % based on Severity
        if spo2_at_rest == "Mild":
             fvc_pct = self.random.randint(80, 95)
        elif spo2_at_rest == "Moderate":
             fvc_pct = self.random.randint(50, 79)
        else: # Severe
             fvc_pct = self.random.randint(30, 49)
             
        # Determine Severity based on the FVC/SpO2 combination
        if fvc_pct >= 80:
            self.severity = "Mild"
        elif 50 <= fvc_pct < 80:
            self.severity = "Moderate"
        else:
            self.severity = "Severe"
            
        self.simulated_fvc_pct = fvc_pct
        
        # Cor Pulmonale Logic (Secondary to Pulmonary HTN in advanced disease) 
        if self.severity == "Severe":
            self.cor_pulmonale = self.random.choices(["Present", "Absent"], weights=[60, 40])[0]
        elif self.severity == "Moderate":
            self.cor_pulmonale = self.random.choices(["Present", "Absent"], weights=[10, 90])[0]
        else:
            self.cor_pulmonale = "Absent"

        # Holders for consistency checks
        self.simulated_rr_val = 18

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
        # IPF is disease of older adults (usually > 50) [cite: 1]
        age_num = self.random.randint(55, 85)
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
            "place_of_birth": birth, "place_of_residence": birth,
            "marital_status": "متاهل"
        }

    # --- 1. Vital Signs ---
    def _gen_vitals(self):
        # BP: 90% Normal, 10% High [cite: 1]
        bp_choice = self.random.choices(["Normal", "High"], weights=[90, 10])[0]
        if bp_choice == "Normal":
            sys = self.random.randint(110, 139)
            dia = self.random.randint(70, 89)
        else:
            sys = self.random.randint(140, 160)
            dia = self.random.randint(90, 100)
            
        # T: 95% Normal [cite: 2]
        t_choice = self.random.choices(["Normal", "Low Grade"], weights=[95, 5])[0]
        temp = round(self.random.uniform(36.1, 37.2), 1) if t_choice == "Normal" else round(self.random.uniform(37.3, 38.0), 1)

        # PR: 90% Normal [cite: 3]
        if self.cor_pulmonale == "Present" or self.severity == "Severe":
             pr_val = self.random.randint(95, 115) 
        else:
             pr_val = self.random.randint(60, 95)

        # RR: Driven by Severity [cite: 4]
        if self.severity == "Mild":
             rr_val = self.random.randint(14, 20)
        else:
             rr_val = self.random.randint(22, 32)
        
        self.simulated_rr_val = rr_val

        # SpO2: Uses pre-generated value [cite: 5]
        spo2_val = self.simulated_spo2_val

        return {
            "BP": f"{sys}/{dia} mmHg",
            "T": f"{temp} °C",
            "PR": f"{pr_val} bpm",
            "RR": f"{rr_val} breaths/min",
            "SpO2": f"{spo2_val}% (Room Air)",
            "GCS": "15" # [cite: 6]
        }

    # --- 2. General Appearance ---
    def _gen_general_appearance(self):
        # Mood: Anxiety common (70%) [cite: 8]
        mood = self.random.choices(["Anxious/Concerned", "Euthymic"], weights=[70, 30])[0]
        
        # Position: Tripod if Dyspneic (Mod/Severe) [cite: 9]
        if self.severity in ["Moderate", "Severe"]:
             pos = "Comfortable in Tripod Position (Upright)."
        else:
             pos = "Comfortable in Any Position."

        # Nutrition: Cachexia rare (15%) [cite: 10, 11]
        if self.severity == "Severe" and self.random.random() < 0.6:
            nutr = "Mild to Moderate Cachexia."
        else:
            nutr = "Normal Nutritional Status."

        # Cyanosis [cite: 12]
        if self.simulated_spo2_val < 90:
            cyan = "Central Cyanosis Present."
        elif self.simulated_spo2_val <= 94:
            cyan = "Mild Acrocyanosis."
        else:
            cyan = "No Cyanosis."

        # Dyspnea [cite: 13]
        if self.simulated_spo2_val < 90:
            dysp = "Dyspnea at Rest."
        elif self.simulated_spo2_val <= 94:
            dysp = "Dyspnea with Mild to Moderate Exertion."
        else:
            dysp = "Dyspnea only with Heavy Exertion."

        # Edema [cite: 14]
        if self.cor_pulmonale == "Present":
            edema = "Pitting Edema Present (Bilateral)."
        else:
            edema = "No Peripheral Edema."

        return {
            "level_of_consciousness_mood_and_behavior": {
                "level_of_consciousness": "Alert and Oriented.",
                "mood": mood,
                "behavior": "Cooperative."
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
                "eardrum_appearance": "Normal."
            },
            "nose_and_sinuses": {
                "septum_and_discharge": "Normal.",
                "sinus_tenderness": "None."
            },
            "mouth_and_pharynx": {
                "oral_mucosa_and_lesions": "Normal.",
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
        # Inspection [cite: 25, 27]
        acc = "Accessory Muscle Use." if self.severity in ["Moderate", "Severe"] else "No Accessory Muscle Use."
        chest_shape = "Normal AP Diameter." 
        
        # Palpation [cite: 28]
        exp = "Reduced Bilateral Chest Expansion." if self.severity != "Mild" else "Normal Chest Expansion."
        
        # Auscultation: Velcro Rales [cite: 31]
        has_crackles = self.random.choices([True, False], weights=[90, 10])[0]
        if has_crackles:
            adv = "Bilateral Basilar Fine Crackles (Velcro Rales)."
        else:
            adv = "No Adventitious Sounds."

        return {
            "inspection": {
                "accessory_muscles": acc,
                "chest_shape_and_symmetry": chest_shape
            },
            "palpation": {
                "chest_expansion": exp,
                "tactile_fremitus": "Normal Tactile Fremitus."
            },
            "percussion": ["Normal Resonance."],
            "auscultation": {
                "breath_sounds_intensity": "Normal Intensity or Mildly Decreased Basilar.",
                "adventitious_sounds": adv
            }
        }

    # --- 5. Cardiovascular System ---
    def _gen_cardio(self):
        # Driven by Cor Pulmonale [cite: 32, 33, 34, 35]
        if self.cor_pulmonale == "Present":
            jvp = "Elevated JVP (> 3 cm)."
            heave = "Right Ventricular Heave Palpable."
            p2 = "Loud P2 component of S2."
            murmur = self.random.choices(["Tricuspid Regurgitation Murmur", "No Murmur"], weights=[70, 30])[0]
        else:
            jvp = "Normal JVP."
            heave = "No Heave or Thrill."
            p2 = "Normal S1 and S2."
            murmur = "No Murmurs."

        return {
            "JVP_assessment": jvp,
            "palpation": {
                "precordial_palpation_heave_thrill": heave,
                "pmi_assessment": "PMI Non-displaced."
            },
            "auscultation": {
                "heart_sounds_s1_s2": p2,
                "extra_sounds_s3_s4_murmurs": murmur
            },
            "peripheral_pulses_and_extremities": {
                "peripheral_pulses_symmetry_and_quality": "Symmetric and 2+.",
                "extremities_color_and_trophic_changes": "Normal.",
                "extremities_temperature_and_cap_refill": "Warm, < 2 sec.",
                "extremities_edema": "Pitting Edema Present." if self.cor_pulmonale == "Present" else "No Edema."
            }
        }

    # --- 6. Abdominal System ---
    def _gen_abdominal(self):
        # Hepatic congestion if Cor Pulmonale [cite: 41]
        if self.cor_pulmonale == "Present" and self.random.random() < 0.5:
             organ = "Mild Hepatomegaly."
        else:
             organ = "Liver/Spleen non-palpable."

        return {
            "inspection": "Flat and Symmetric.",
            "auscultation": {
                "bowel_sounds": "Normoactive.",
                "vascular_bruits": "Absent."
            },
            "percussion": {
                "general": "Tympanitic.",
                "organ_borders": organ
            },
            "palpation": {
                "superficial_tenderness": "No Tenderness.",
                "deep_masses_and_оргаns": "No masses.",
                "peritoneal_signs": "Negative."
            }
        }

    # --- 7. Neurological ---
    def _gen_neuro(self):
        return {
            "mental_status_and_LOC": "Alert and Oriented.",
            "cranial_nerves": "Intact.",
            "motor_strength_and_tone": "5/5, Normal.",
            "involuntary_movements": "None.",
            "sensory_light_touch_and_pain": "Intact.",
            "deep_tendon_reflexes": "2+ Bilaterally.",
            "coordination_and_gait": "Normal."
        }

    # --- 8. Musculoskeletal ---
    def _gen_msk(self):
        # Clubbing Logic: 40% overall [cite: 47]
        if self.severity in ["Moderate", "Severe"]:
             clubbing = self.random.choices(["Digital Clubbing Present", "No Clubbing"], weights=[60, 40])[0]
        else:
             clubbing = "No Digital Clubbing"

        return {
            "inspection": {
                "joints": clubbing,
                "muscles": "Normal Muscle Bulk."
            },
            "palpation": {
                "tenderness_and_crepitus": "No tenderness."
            },
            "range_of_motion_active_passive": "Full ROM.",
            "stability_and_function": "Stable."
        }

    def _generate_pao2_from_spo2(self, spo2_val):
        """Calculates PaO2 based on SpO2 approximation."""
        if spo2_val >= 95:
            pao2 = self.random.randint(85, 100)
        elif 90 <= spo2_val <= 94:
            pao2 = self.random.randint(65, 80) 
        else: 
            pao2 = self.random.randint(50, 64)
        return f"{pao2} mmHg"
    
    # --- 9. Paraclinic Tests ---
    def _gen_paraclinic(self):
        # CBC: Polycythemia if Hypoxemic [cite: 50]
        if self.simulated_spo2_val < 92:
             hb_w = [60, 40] 
        else:
             hb_w = [90, 10]
        hb_choice = self.random.choices(["Normal", "High"], weights=hb_w)[0]
        hb = "15.0 g/dL" if hb_choice == "Normal" else "18.0 g/dL (Polycythemia)"

        # ESR/CRP [cite: 53, 54]
        esr = "< 20 mm/hr"
        crp = "< 5 mg/L"

        # ABG [cite: 58, 59]
        if self.severity == "Severe" and self.random.random() < 0.2:
             paco2 = "50 mmHg" # Hypercapnia
             ph = "7.32" # Acidosis
        else:
             paco2 = "32 mmHg" # Hyperventilation
             ph = "7.48" # Alkalosis
             
        simulated_pao2 = self._generate_pao2_from_spo2(self.simulated_spo2_val)
        bnp = "Elevated" if self.cor_pulmonale == "Present" else "Normal"

        # --- CORRECTED SPIROMETRY LOGIC START ---
        # Based on sources: [cite: 72, 73, 75, 76, 77]
        
        # 1. Pattern: 95% Restrictive, 5% Normal 
        is_restrictive = self.random.choices([True, False], weights=[95, 5])[0]
        
        # 2. Predicted Values (Reference ranges for adults) 
        pred_fev1_val = round(self.random.uniform(3.0, 4.0), 2) # 3.0-4.0L
        pred_fvc_val = round(self.random.uniform(3.5, 5.0), 2)  # 3.5-5.0L
        pred_ratio_val = round(self.random.uniform(0.70, 0.85), 2) # 0.70-0.85

        if is_restrictive:
            pattern_result = "Restrictive Pattern (FEV1/FVC Ratio Normal/High with Low FEV1 and FVC)"
            
            # Use the consistent FVC% generated in __init__ (matches severity)
            fvc_pct = self.simulated_fvc_pct
            
            # Measured FVC
            meas_fvc = round(pred_fvc_val * (fvc_pct / 100.0), 2)
            
            # Ratio is preserved/high in IPF [cite: 72, 77]
            meas_ratio = round(self.random.uniform(0.75, 0.85), 2)
            
            # Calculate FEV1
            meas_fev1 = round(meas_fvc * meas_ratio, 2)
            
        else: # Normal (Early disease)
            pattern_result = "Normal Spirometry"
            fvc_pct = self.random.randint(80, 110)
            meas_fvc = round(pred_fvc_val * (fvc_pct / 100.0), 2)
            meas_ratio = round(self.random.uniform(0.70, 0.80), 2)
            meas_fev1 = round(meas_fvc * meas_ratio, 2)

        # Calculate current percentages for display
        current_fev1_pct = int((meas_fev1 / pred_fev1_val) * 100)
        current_ratio_pct = int((meas_ratio / pred_ratio_val) * 100)

        # 3. Reversibility: 90% Negative 
        rev_choice = self.random.choices(["Negative", "Positive"], weights=[90, 10])[0]
        if rev_choice == "Negative":
            rev_text = "In 90% of times FEV1 increase < 12% OR < 200 mL"
        else:
            rev_text = "In 10% of times FEV1 increase > 12% AND > 200 mL"

        # 4. Formatted Strings [cite: 74, 76, 78]
        fev1_pct_str = f"In 30% of times > 80%; In 40% of times 50-80%; In 30% of times < 50% (Current: {current_fev1_pct}%)"
        fvc_pct_str = f"In 30% of times > 80%; In 40% of times 50-80%; In 30% of times < 50% (Current: {fvc_pct}%)"
        ratio_pct_str = f"In 90% of times > 70%; In 10% of times < 70% (Current: {current_ratio_pct}%)"

        # TLC and DLCO Logic
        tlc = f"Reduced (< 80% Predicted)" if is_restrictive else "Normal"
        dlco = "Reduced (< 60% Predicted)" #

        # --- CORRECTED SPIROMETRY LOGIC END ---

        # --- IMAGING ---
        hrct_weights = [70, 20, 10] 
        hrct_res = self.random.choices(
            [
                "Definite UIP Pattern: Subpleural, Basilar-predominant Honeycombing.", # [cite: 70]
                "Probable UIP Pattern: Reticulation without Honeycombing.", # [cite: 70]
                "Indeterminate UIP Pattern." # [cite: 71]
            ],
            weights=hrct_weights
        )[0]
        
        cxr = "Bilateral Reticular Opacities, Lower Lobe Volume Loss." # [cite: 68]

        # --- Final Return Structure ---
        return {
            "basic_blood_tests": {
                "CBC": {"Hb": hb, "WBC": "8500 /uL", "Plt": "250,000 /uL"},
                "ESR": esr,
                "CRP": crp,
                "BMP": {"Na": "140", "BUN": "15", "Cr": "0.9"},
                "LFTs": {"ALT": "30", "AST": "30"},
                "VBG": {"pH": ph, "PaCO2": f"{paco2}", "HCO3": "24", "PaO2": simulated_pao2}
            },
            "specialized_lung_tests": {
                "Sputum_analysis": {"Gram_Stain": "Negative"},
                "Sputum_AFB": "Negative",
                "a1_antitrypsin_level": "Normal",
                "D_dimer": "Normal",
                "BNP_NT_proBNP": bnp
            },
            "immunity_and_serology": {
                "HIV_test": "Negative",
                "Autoimmune_pannel_ANA_ANCA": "Negative"
            },
            "simple_imaging": {
                "Chest_X_Ray": {"PA_Lateral_Findings_and_Effusion": cxr}
            },
            "advanced_imaging": {
                "Chest_CT_CTPA": {"Lung_Parenchyma_and_Pleura": hrct_res}
            },
            "functional_tests": {
                "Spirometry": {
                    "result": {
                            "FEV1": {
                            "Measured": f"{meas_fev1} L",
                            "Predicted": f"{pred_fev1_val} L",
                            "Predicted%": fev1_pct_str,
                            "Reversibility_Improvement": rev_text
                        },
                        "FVC": {
                            "Measured": f"{meas_fvc} L",
                            "Predicted": f"{pred_fvc_val} L",
                            "Predicted%": fvc_pct_str,
                            "CONSISTENCY_RULE": "FVC decline is the primary marker of disease progression."
                        },
                        "FEV1/FVC_Ratio": {
                            "Measured": f"{meas_ratio}",
                            "Predicted": f"{pred_ratio_val}",
                            "Predicted%": ratio_pct_str
                        }
                    },
                    "Reversibility": "FEV1 increase < 12% AND < 200 mL"
                },
                "peak_flow": "Reduced",
                "plethysmography": f"TLC: {tlc}",
                "DLCO": dlco
            },
            "procedures": {
                "Bronchoscopy": "BAL: Mild Neutrophilia, No Malignancy.",
                "torachonthesis": "Not Indicated"
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