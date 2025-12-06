import random
import json

class IPFDataGenerator:
    """
    کلاسی برای تولید داده‌های شبیه‌سازی شده IPF (فیبروز ریوی ایدیوپاتیک).
    نسخه اصلاح شده: بخش General Appearance دقیقاً بر اساس قواعد آماری و ساختار درخواستی به روز رسانی شده است.
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
        # SpO2 Logic
        spo2_at_rest = self.random.choices(
            ["Mild", "Moderate", "Severe"],
            weights=[30, 45, 25], k=1
        )[0]
        
        if spo2_at_rest == "Mild":
            self.simulated_spo2_val = self.random.randint(95, 98)
        elif spo2_at_rest == "Moderate":
            self.simulated_spo2_val = self.random.randint(90, 94)
        else:
            self.simulated_spo2_val = self.random.randint(84, 89)

        # Severity Logic
        if self.simulated_spo2_val >= 95:
            self.severity = "Mild"
        elif 90 <= self.simulated_spo2_val < 95:
            self.severity = "Moderate"
        else:
            self.severity = "Severe"
            
        # Cor Pulmonale Logic
        if self.severity == "Severe":
            self.cor_pulmonale = self.random.choices(["Present", "Absent"], weights=[60, 40])[0]
        elif self.severity == "Moderate":
            self.cor_pulmonale = self.random.choices(["Present", "Absent"], weights=[10, 90])[0]
        else:
            self.cor_pulmonale = "Absent"

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
        bp_choice = self.random.choices(["Normal", "High"], weights=[90, 10])[0]
        if bp_choice == "Normal":
            sys, dia = self.random.randint(110, 139), self.random.randint(70, 89)
        else:
            sys, dia = self.random.randint(140, 160), self.random.randint(90, 100)
            
        t_choice = self.random.choices(["Normal", "Low Grade"], weights=[95, 5])[0]
        temp = round(self.random.uniform(36.1, 37.2), 1) if t_choice == "Normal" else round(self.random.uniform(37.3, 38.0), 1)

        if self.cor_pulmonale == "Present" or self.severity == "Severe":
             pr_val = self.random.randint(95, 115) 
        else:
             pr_val = self.random.randint(60, 95)

        if self.severity == "Mild":
             rr_val = self.random.randint(14, 20)
        else:
             rr_val = self.random.randint(22, 32)
        
        return {
            "BP": f"{sys}/{dia} mmHg",
            "T": f"{temp} °C",
            "PR": f"{pr_val} bpm",
            "RR": f"{rr_val} breaths/min",
            "SpO2": f"{self.simulated_spo2_val}% (Room Air)",
            "GCS": "15"
        }

    # --- 2. General Appearance (CORRECTED & UPDATED) ---
    def _gen_general_appearance(self):
        """
        Modified to strictly follow the provided statistical rules and text values.
        """
        
        # 1. Mood and Behavior
        # Rules: 50% Anxious/Concerned, 50% Calm/Cooperative
        mood_behavior = self.random.choices(
            ["Anxious or Concerned", "Calm and Cooperative"],
            weights=[50, 50], k=1
        )[0]

        # 2. Overall Appearance
        # Rules: 30% Cachectic/Frail, 70% Well-nourished
        overall = self.random.choices(
            ["Cachectic or Frail", "Well-nourished"],
            weights=[30, 70], k=1
        )[0]

        # 3. Posture and Position
        # Rules: 20% Tripod/Upright, 80% No specific preference
        posture = self.random.choices(
            ["Tripod or Sitting Upright", "No specific preference"],
            weights=[20, 80], k=1
        )[0]

        # 4. Level of Consciousness
        # Rules: 95% Alert, 5% Drowsy/Confused
        loc = self.random.choices(
            ["Alert and Oriented", "Drowsy or Confused"],
            weights=[95, 5], k=1
        )[0]

        # 5. Cardiopulmonary Clues (Edema, Dyspnea, Cyanosis)
        
        # Edema: 20% Pitting, 80% No Edema
        edema = self.random.choices(
            ["Pitting Edema", "No Edema"],
            weights=[20, 80], k=1
        )[0]

        # Dyspnea: 60% Visible, 40% Not visible
        dyspnea = self.random.choices(
            ["Visible dyspnea at rest or minimal exertion", "No visible dyspnea at rest"],
            weights=[60, 40], k=1
        )[0]

        # Cyanosis: 30% Central, 70% No Cyanosis
        cyanosis = self.random.choices(
            ["Central Cyanosis", "No Cyanosis"],
            weights=[30, 70], k=1
        )[0]

        # Structured return matching the requested JSON format
        return {
            "mood_and_behavior": mood_behavior,
            "overall_appearance": overall,
            "posture_and_position": posture,
            "level_of_consciousness": loc,
            "cardiopulmonary_and_circulatory_clues": {
                "edema": edema,
                "dyspnea": dyspnea,
                "cyanosis": cyanosis
            }
        }

    # --- 3. Head and Neck (Simplified) ---
    def _gen_head_neck(self):
        return {
            "head_and_face": {"symmetry_and_lesions": "Normal.", "tenderness": "None."},
            "eyes": {"sclera_and_conjunctiva": "Normal.", "pupils_reaction": "PERRLA."},
            "ears": {"external_and_tenderness": "Normal."},
            "nose_and_sinuses": {"septum_and_discharge": "Normal."},
            "mouth_and_pharynx": {"oral_mucosa_and_lesions": "Normal."},
            "neck_and_lymphatics": {"inspection": "Normal.", "thyroid_gland": "Non-palpable."}
        }

    # --- 4. Respiratory System ---
    def _gen_respiratory(self):
        acc = "Accessory Muscle Use." if self.severity in ["Moderate", "Severe"] else "No Accessory Muscle Use."
        exp = "Reduced Bilateral Chest Expansion." if self.severity != "Mild" else "Normal Chest Expansion."
        
        # Velcro Rales logic
        has_crackles = self.random.choices([True, False], weights=[90, 10])[0]
        adv = "Bilateral Basilar Fine Crackles (Velcro Rales)." if has_crackles else "No Adventitious Sounds."

        return {
            "inspection": { "accessory_muscles": acc, "chest_shape_and_symmetry": "Normal AP Diameter." },
            "palpation": { "chest_expansion": exp, "tactile_fremitus": "Normal Tactile Fremitus." },
            "percussion": "Normal Resonance.",
            "auscultation": { "breath_sounds": "Normal Intensity or Mildly Decreased Basilar.", "adventitious_sounds": adv }
        }

    # --- 5. Cardiovascular System ---
    def _gen_cardio(self):
        if self.cor_pulmonale == "Present":
            return {
                "JVP_assessment": "Elevated JVP (> 3 cm).",
                "palpation": { "precordial_palpation_heave_thrill": "Right Ventricular Heave Palpable.", "pmi_assessment": "PMI Non-displaced." },
                "auscultation": { "heart_sounds_s1_s2": "Loud P2 component of S2.", "extra_sounds_s3_s4_murmurs": self.random.choices(["Tricuspid Regurgitation Murmur", "No Murmur"], weights=[70, 30])[0] },
                "peripheral_pulses_and_extremities": { "extremities_edema": "Pitting Edema Present." }
            }
        else:
            return {
                "JVP_assessment": "Normal JVP.",
                "palpation": { "precordial_palpation_heave_thrill": "No Heave or Thrill.", "pmi_assessment": "PMI Normal." },
                "auscultation": { "heart_sounds_s1_s2": "Normal S1 and S2.", "extra_sounds_s3_s4_murmurs": "No Murmurs." },
                "peripheral_pulses_and_extremities": { "extremities_edema": "No Edema." }
            }

    # --- 6. Abdominal & 7. Neuro & 8. MSK ---
    def _gen_abdominal(self):
        organ = "Mild Hepatomegaly." if (self.cor_pulmonale == "Present" and self.random.random() < 0.5) else "Liver/Spleen non-palpable."
        return { "inspection": "Flat.", "percussion": {"organ_borders": organ}, "palpation": { "deep_masses_and_organs": "No masses." } }

    def _gen_neuro(self):
        return { "mental_status_and_LOC": "Alert and Oriented.", "motor_strength_and_tone": "5/5, Normal." }

    def _gen_msk(self):
        clubbing = self.random.choices(["Digital Clubbing Present", "No Clubbing"], weights=[60, 40])[0] if self.severity in ["Moderate", "Severe"] else "No Digital Clubbing"
        return { "inspection": { "joints": clubbing }, "range_of_motion_active_passive": "Full ROM." }

    # --- SPIROMETRY LOGIC ---
    def _gen_spirometry_logic(self):
        PRED_FEV1 = 3.50
        PRED_FVC = 4.00
        PRED_RATIO = 0.80

        scenario = self.random.choices(["Restricted", "Normal"], weights=[80, 20])[0]
        
        while True:
            if scenario == "Restricted":
                meas_fvc = round(self.random.uniform(1.80, 3.20), 2)
                meas_fev1 = round(self.random.uniform(1.50, 2.80), 2)
            else:
                meas_fvc = round(self.random.uniform(3.25, 4.40), 2)
                meas_fev1 = round(self.random.uniform(2.85, 3.85), 2)

            meas_ratio = round(meas_fev1 / meas_fvc, 2)
            if 0.75 <= meas_ratio <= 0.95:
                break
        
        fev1_pct = int((meas_fev1 / PRED_FEV1) * 100)
        fvc_pct = int((meas_fvc / PRED_FVC) * 100)
        ratio_pct = int((meas_ratio / PRED_RATIO) * 100)

        return {
            "result": {
                "FEV1": f"Measured: {meas_fev1} L, Predicted: {PRED_FEV1} L, %Predicted: {fev1_pct}%",
                "FVC": f"Measured: {meas_fvc} L, Predicted: {PRED_FVC} L, %Predicted: {fvc_pct}%",
                "FEV1/FVC_Ratio": f"Measured: {meas_ratio}, Predicted: {PRED_RATIO}, %Predicted: {ratio_pct}%"
            },
            "reversibility": "FEV1 increase < 12% AND < 200 mL"
        }

    # --- 9. Paraclinic Tests ---
    def _gen_paraclinic(self):
        hb = "18.0 g/dL (Polycythemia)" if self.simulated_spo2_val < 92 and self.random.random() < 0.4 else "15.0 g/dL"
        if self.severity == "Severe" and self.random.random() < 0.2:
             pco2, ph = "50 mmHg", "7.32"
        else:
             pco2, ph = "32 mmHg", "7.48"
        
        bnp = "Elevated" if self.cor_pulmonale == "Present" else "Normal"

        hrct_res = self.random.choices(
            [
                "Definite UIP Pattern: Subpleural, Basilar-predominant Honeycombing.",
                "Probable UIP Pattern: Reticulation without Honeycombing.",
                "Indeterminate UIP Pattern."
            ],
            weights=[70, 20, 10]
        )[0]

        spiro_data = self._gen_spirometry_logic()
        tlc = "Reduced (< 80% Predicted)" if "Restricted" in spiro_data["result"]["FVC"] else "Normal"
        dlco = "Reduced (< 60% Predicted)"

        return {
            "basic_blood_tests": {
                "CBC": {"Hb": hb, "WBC": "8500 /uL", "Plt": "250,000 /uL"},
                "ESR": "< 20 mm/hr", "CRP": "< 5 mg/L",
                "BMP": {"Na": "140", "BUN": "15", "Cr": "0.9"},
                "LFTs": {"ALT": "30", "AST": "30"},
                "VBG": {"pH": ph, "PCO2": pco2, "HCO3": "24"}
            },
            "specialized_lung_tests": {
                "Sputum_analysis": {"Gram_Stain": "Negative"},
                "Sputum_AFB": "Negative",
                "a1_antitrypsin_level": "Normal", "D_dimer": "Normal", "BNP_NT_proBNP": bnp
            },
            "immunity_and_serology": { "HIV_test": "Negative", "Autoimmune_pannel_ANA_ANCA": "Negative" },
            "simple_imaging": { "Chest_X_Ray": {"PA_Lateral_Findings_and_Effusion": "Bilateral Reticular Opacities, Lower Lobe Volume Loss."} },
            "advanced_imaging": { "Chest_CT_CTPA": {"Lung_Parenchyma_and_Pleura": hrct_res} },
            "functional_tests": {
                "Spirometry": spiro_data,
                "peak_flow": "Reduced",
                "plethysmography": f"TLC: {tlc}",
                "dlco": dlco
            },
            "procedures": { "Bronchoscopy": "BAL: Mild Neutrophilia, No Malignancy.", "torachonthesis": "Not Indicated" }
        }

    def generate_paraclinic_case(self):
        return {
            "patient_profile": { "personal_information": self._generate_personal_information() },
            "physical_exam": {
                "vital_signs": self._gen_vitals(),
                "general_appearance": self._gen_general_appearance(),
                "head_and_neck": self._gen_head_neck(),
                "respiratory_system": self._gen_respiratory(),
                "cardiovascular_system": self._gen_cardio(),
                "abdominal_system": self._gen_abdominal(),
                "neurological": self._gen_neuro(),
                "musculoskeletal_system": self._gen_msk()
            },
            "paraclinic": self._gen_paraclinic()
        }
    