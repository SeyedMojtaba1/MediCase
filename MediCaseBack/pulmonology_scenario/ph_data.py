import random
import json

class PHDataGenerator:
    """
    کلاسی برای تولید داده‌های شبیه‌سازی شده فشار خون ریوی (PH).
    نسخه اصلاح شده: 
    1. بخش General Appearance دقیقاً بر اساس قواعد آماری و ساختار درخواستی جدید به روز رسانی شده است.
    
    Logic Drivers (متغیرهای اصلی برای حفظ سازگاری بالینی):
    1. RV_DYSFUNCTION: (None/Mild/Severe)
    2. FUNCTIONAL_CLASS: (FC I-II vs FC III-IV)
    3. PH_GROUP: (Group 1 PAH, Group 3-ILD, Group 3-COPD)
    """
    
    # لیست‌های داده‌های دموگرافیک
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
        "occupations": [
            "بازنشسته", "خانه‌دار", "کارمند", "معلم", "کشاورز", "راننده", "کارگر"
        ],
        "famous_cities_sample_30": [
            "تهران", "مشهد", "اصفهان", "شیراز", "تبریز", "اهواز", "کرج", "رشت", "کرمان", "یزد",
            "ساری", "بندرعباس", "کرمانشاه", "ارومیه", "زاهدان", "همدان", "قزوین", "اردبیل", "زنجان", "گرگان"
        ]
    }
    
    def __init__(self):
        self.random = random
        
        # 1. CORE LOGIC INITIALIZATION
        
        # PH Group
        self.ph_group = self.random.choices(
            ["Group 1 (PAH)", "Group 3 (ILD-PH)", "Group 3 (COPD-PH)"], 
            weights=[60, 20, 20], k=1
        )[0]
        
        # Functional Class
        self.functional_class = self.random.choices(
            ["FC I-II", "FC III-IV"], 
            weights=[40, 60], k=1
        )[0]

        # RV Dysfunction Severity
        if self.functional_class == "FC III-IV":
            self.rv_dysfunction = self.random.choices(["Severe", "Mild/None"], weights=[70, 30])[0]
        else:
            self.rv_dysfunction = self.random.choices(["Severe", "Mild/None"], weights=[15, 85])[0]

        # Holders for consistency checks
        self.simulated_spo2_val = 95
        self.simulated_rr_val = 20
        self.simulated_bp_systolic = 120

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
        age_num = self.random.randint(35, 75)
        age_str = f"{age_num} ساله"
        
        name_key = "MALE" if gender == "مرد" else "FEMALE"
        first_name = self.random.choice(self.RANDOM_DATA_LISTS["first_names_sample_100"][name_key])
        last_name = self.random.choice(self.RANDOM_DATA_LISTS["last_names_sample_100"])
        occupation = self.random.choice(self.RANDOM_DATA_LISTS["occupations"])
        birth = self.random.choice(self.RANDOM_DATA_LISTS["famous_cities_sample_30"])
        
        return {
            "first_name": first_name, "last_name": last_name, "age": age_str,
            "gender": gender, "occupation": occupation,
            "place_of_birth": birth, "place_of_residence": birth,
            "marital_status": "متاهل"
        }

    # --- 1. Vital Signs ---
    def _gen_vitals(self):
        if self.rv_dysfunction == "Severe": 
            sys = self.random.randint(85, 99) 
            dia = self.random.randint(50, 65)
        else:
            bp_choice = self.random.choices(["Normal", "High"], weights=[70, 30])[0]
            if bp_choice == "Normal":
                sys = self.random.randint(110, 139)
                dia = self.random.randint(70, 89)
            else:
                sys = self.random.randint(141, 165)
                dia = self.random.randint(90, 105)
        
        self.simulated_bp_systolic = sys

        if self.functional_class == "FC III-IV": 
            pr = self.random.randint(100, 120)
        else:
            pr = self.random.randint(65, 99)

        if self.functional_class == "FC III-IV" or self.simulated_bp_systolic < 100: 
            rr = self.random.randint(22, 30)
        else:
            rr = self.random.randint(14, 20)
        
        self.simulated_rr_val = rr

        if self.rv_dysfunction == "Severe": 
            spo2 = self.random.randint(83, 87)
        elif self.ph_group.startswith("Group 3"): 
            spo2 = self.random.randint(88, 94)
        else: 
            spo2 = self.random.randint(95, 98) 
        
        self.simulated_spo2_val = spo2

        temp = round(self.random.uniform(36.5, 37.5), 1)

        return {
            "BP": f"{sys}/{dia} mmHg",
            "T": f"{temp} °C",
            "PR": f"{pr} bpm",
            "RR": f"{rr} breaths/min",
            "SpO2": f"{spo2}% (Room Air)",
            "GCS": "15"
        }

    # --- 2. General Appearance (CORRECTED) ---
    def _gen_general_appearance(self):
        """
        Updated to strictly follow the provided statistical rules and structure.
        """
        
        # 1. Mood and Behavior
        # Rules: 60% Anxious/Apprehensive, 40% Calm/Cooperative
        mood_behavior = self.random.choices(
            [
                "Anxious or Apprehensive", 
                "Calm and Cooperative"
            ],
            weights=[60, 40],
            k=1
        )[0]

        # 2. Overall Appearance
        # Rules: 20% Cachectic, 80% Well-nourished
        overall = self.random.choices(
            [
                "Cachectic appearance with muscle wasting",
                "Well-nourished appearance"
            ],
            weights=[20, 80],
            k=1
        )[0]

        # 3. Posture and Position
        # Rules: 40% Tripod, 60% No specific preference
        posture = self.random.choices(
            [
                "Prefers sitting upright (Tripod position)",
                "No specific position of comfort preference"
            ],
            weights=[40, 60],
            k=1
        )[0]

        # 4. Level of Consciousness
        # Rules: 90% Alert, 10% Drowsy/Confused
        loc = self.random.choices(
            [
                "Alert and Oriented",
                "Drowsy or Confused"
            ],
            weights=[90, 10],
            k=1
        )[0]

        # 5. Cardiopulmonary Clues (Edema, Dyspnea, Cyanosis)
        
        # Edema: 60% Peripheral Edema, 40% No Edema
        edema = self.random.choices(
            ["Peripheral Edema (Lower extremities)", "No Edema"],
            weights=[60, 40],
            k=1
        )[0]

        # Dyspnea: 40% Rest, 50% Minimal Exertion, 10% None
        dyspnea = self.random.choices(
            ["Dyspnea at rest", "Dyspnea with minimal exertion", "No visible dyspnea at rest"],
            weights=[40, 50, 10],
            k=1
        )[0]

        # Cyanosis: 15% Central, 15% Peripheral, 70% None
        cyanosis = self.random.choices(
            ["Central Cyanosis present", "Peripheral Cyanosis present", "No Cyanosis"],
            weights=[15, 15, 70],
            k=1
        )[0]
        
        # Return structure matches the JSON request
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

    # --- 3. Head and Neck ---
    def _gen_head_neck(self):
        if self.rv_dysfunction == "Severe":
            jvp = "Elevated JVP (> 4 cm above sternal angle)."
        else:
            jvp = "Normal JVP."
            
        return {
            "head_and_face": {"symmetry_and_lesions": "Normal."},
            "eyes": {"sclera_and_conjunctiva": "Normal."},
            "ears": {"external_and_tenderness": "Normal."},
            "nose_and_sinuses": {"septum_and_discharge": "Normal."},
            "mouth_and_pharynx": {"oral_mucosa_and_lesions": "Normal."},
            "neck_and_lymphatics": {
                "inspection": "Supple.",
                "tracheal_position": "Midline.",
                "carotid_bruit": "No Bruit.",
                "lymph_nodes_size_consistency": "Not Palpable.",
                "JVP_assessment": jvp
            }
        }
    
    # --- 4. Respiratory System ---
    def _gen_respiratory(self):
        if self.ph_group == "Group 3 (ILD-PH)":
            adventitious = "Bilateral Basilar Fine Crackles (Velcro Rales)."
        elif self.ph_group == "Group 3 (COPD-PH)":
            adventitious = "Bilateral Expiratory Wheezes and Rhonchi."
        else:
            adventitious = "Clear to Auscultation."

        return {
            "inspection": {
                "accessory_muscles": "Accessory Muscle Use." if self.simulated_rr_val > 22 else "No Accessory Muscle Use.",
                "chest_shape_and_symmetry": "Symmetrical, Normal AP Diameter."
            },
            "palpation": {"chest_expansion": "Normal."},
            "percussion": "Normal Resonance.",
            "auscultation": {
                "breath_sounds": "Normal Intensity.",
                "adventitious_sounds": adventitious
            }
        }

    # --- 5. Cardiovascular System ---
    def _gen_cardio(self):
        if self.rv_dysfunction == "Severe":
            s2_desc = "Loud P2 component of S2 at the left sternal border."
            heave = "Right Ventricular Heave Palpable."
            extra = self.random.choices(
                ["Holosystolic Murmur (Tricuspid Regurgitation).", "Right-sided S3 Gallop."], 
                weights=[70, 30]
            )[0]
        else:
            s2_desc = "Normal S1 and S2."
            heave = "No Heave or Thrill."
            extra = "No Extra Sounds or Murmurs."

        pulse_qual = "Weak and Thready" if self.simulated_bp_systolic < 100 else "Peripheral Pulses Symmetric and 2+."
        extremities = "Cool and Pale with Capillary Refill > 2 seconds." if self.simulated_bp_systolic < 100 else "Extremities Warm, Capillary Refill < 2 seconds."
        
        return {
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
                "extremities_color_and_trophic_changes": "Normal color.",
                "extremities_temperature_and_cap_refill": extremities,
                "extremities_edema": "See General Appearance Section."
            }
        }

    # --- 6. Abdominal System ---
    def _gen_abdominal(self):
        if self.rv_dysfunction == "Severe" and self.random.random() < 0.6:
            organ = "Hepatomegaly (Tender, Pulsatile Liver) due to congestion."
        else:
            organ = "Liver/Spleen non-palpable."

        return {
            "inspection": "Abdomen Flat and Symmetric.",
            "auscultation": {"bowel_sounds": "Normoactive Bowel Sounds."},
            "percussion": {"organ_borders": organ},
            "palpation": {"superficial_tenderness": "No Superficial Tenderness."}
        }

    # --- 7. Neurological ---
    def _gen_neuro(self):
        return {
            "mental_status_and_LOC": "Mental Status: Alert and Oriented.",
            "motor_strength_and_tone": "Motor Strength 5/5 Bilaterally."
        }

    # --- 8. Musculoskeletal ---
    def _gen_msk(self):
        if self.ph_group == "Group 3 (ILD-PH)":
             clubbing = self.random.choices(["Digital Clubbing Present", "No Clubbing"], weights=[60, 40])[0]
        else:
             clubbing = "No Digital Clubbing."

        return {
            "inspection": {"joints": clubbing},
            "palpation": {"tenderness_and_crepitus": "No tenderness."},
            "range_of_motion_active_passive": "Full ROM."
        }
        
    def _get_radiology_finding(self):
        parenchymal_findings_choices = [
            "Mosaic perfusion pattern",  # CTEPH (Group 4) - 10%
            "Fibrotic changes",          # Group 3 PH (ILD-PH) - 3%
            "Emphysematous changes",     # Group 3 PH (COPD-PH) - 2%
            "Normal parenchyma"          # Group 1 (PAH) - 5%
        ]
        parenchymal_weights = [10, 3, 2, 5]
        pa_enlargement_finding = "PA diameter > Aorta diameter" 
        
        overall_choice = self.random.choices(
            ["PA_ENLARGEMENT", "PARENCHYMAL_OR_NORMAL"], 
            weights=[80, 20], k=1
        )[0]
        
        if overall_choice == "PA_ENLARGEMENT":
            final_output=f"{pa_enlargement_finding}"
        else:
            chosen_parenchymal = self.random.choices(
                parenchymal_findings_choices, 
                weights=parenchymal_weights, k=1
            )[0]
            final_output=f"{chosen_parenchymal}"
        return final_output
    
    def _get_dlco_finding(self):
        findings = ["Reduced (< 80% predicted)", "Normal"]
        weights = [90, 10]
        chosen_status = self.random.choices(findings, weights=weights, k=1)[0]
        if chosen_status == "Reduced (< 80% predicted)":
            dlco_val = self.random.randint(40, 79)
        else:
            dlco_val = self.random.randint(80, 100)
        return chosen_status, f"{dlco_val}% predicted"

    def _get_spirometry_data(self):
        pred_fev1_val = self.random.uniform(3.50, 3.80)
        pred_fvc_val = self.random.uniform(4.30, 4.70)
        pred_ratio_val = self.random.uniform(0.79, 0.83)
        
        fev1_pct_choices = [
            (self.random.uniform(80.0, 120.0), (2.90, 4.40), "80-120%"), # 80%
            (self.random.uniform(60.0, 79.0), (2.20, 2.90), "60-79%")   # 20%
        ]
        fev1_pct, fev1_range, fev1_pct_text = self.random.choices(fev1_pct_choices, weights=[80, 20], k=1)[0]
        meas_fev1 = self.random.uniform(fev1_range[0], fev1_range[1])
        
        fvc_pct_choices = [
            (self.random.uniform(80.0, 120.0), (3.60, 5.40), "80-120%"), # 80%
            (self.random.uniform(60.0, 79.0), (2.70, 3.55), "60-79%")   # 20%
        ]
        fvc_pct, fvc_range, fvc_pct_text = self.random.choices(fvc_pct_choices, weights=[80, 20], k=1)[0]
        meas_fvc = self.random.uniform(fvc_range[0], fvc_range[1])

        meas_ratio = self.random.uniform(0.70, 0.85)
        
        if self.ph_group.startswith("Group 3"):
            if "ILD" in self.ph_group:
                meas_fvc = self.random.uniform(0.5 * pred_fvc_val, 0.79 * pred_fvc_val)
                meas_ratio = self.random.uniform(0.80, 0.95)
                meas_fev1 = meas_fvc * meas_ratio
                fev1_pct_text = fvc_pct_text = "50-79%"
            elif "COPD" in self.ph_group:
                meas_ratio = self.random.uniform(0.40, 0.69)
                meas_fev1 = self.random.uniform(0.4 * pred_fev1_val, 0.79 * pred_fev1_val)
                meas_fvc = meas_fev1 / meas_ratio
                fev1_pct_text = "40-79%"
                fvc_pct_text = "80-100%"
                
        return {
            "FEV1": f"Measured: {meas_fev1:.2f} L, Predicted: {pred_fev1_val:.2f} L, %Predicted: {fev1_pct_text}",
            "FVC": f"Measured: {meas_fvc:.2f} L, Predicted: {pred_fvc_val:.2f} L, %Predicted: {fvc_pct_text}",
            "FEV1/FVC_Ratio": f"Measured: {meas_ratio:.2f}, Predicted: {pred_ratio_val:.2f}, %Predicted: {(meas_ratio/pred_ratio_val)*100:.0f}%"
        }
    
    def _gen_functional_tests(self):
        spirometry_data = self._get_spirometry_data()
        dlco_status, dlco_value = self._get_dlco_finding() 
        pef_val = self.random.choices(["Normal PEF", "Reduced PEF"], weights=[80, 20], k=1)[0]
        pleth_val = self.random.choices(["Normal Lung Volumes", "Abnormal Lung Volumes"], weights=[80, 20], k=1)[0]

        return {
            "Spirometry": {
                "result": {
                    "FEV1": spirometry_data["FEV1"],
                    "FVC": spirometry_data["FVC"],
                    "FEV1/FVC_Ratio": spirometry_data["FEV1/FVC_Ratio"]
                },
                "reversibility": "FEV1 increase < 12% AND < 200 mL"
            }, 
            "dlco": dlco_value,
            "peak_flow": pef_val,
            "plethysmography": pleth_val
        }

    # --- 9. Paraclinic Tests (UPDATED) ---
    def _gen_paraclinic(self):
        # ==================== BASIC BLOOD TESTS ====================
        
        # BMP - Na
        na_choice = self.random.choices(["Hyponatremia", "Normal"], weights=[20, 80], k=1)[0]
        if na_choice == "Hyponatremia": 
            na_val = self.random.randint(125, 134)
        else: 
            na_val = self.random.randint(135, 145)

        # BMP - BUN
        bun_choice = self.random.choices(["Elevated", "Normal"], weights=[25, 75], k=1)[0]
        if bun_choice == "Elevated": 
            bun_val = self.random.randint(21, 40)
        else: 
            bun_val = self.random.randint(7, 20)

        # BMP - Cr
        cr_choice = self.random.choices(["Elevated", "Normal"], weights=[20, 80], k=1)[0]
        if cr_choice == "Elevated": 
            cr_val = round(self.random.uniform(1.3, 2.5), 2)
        else: 
            cr_val = round(self.random.uniform(0.6, 1.2), 2)

        # CBC - WBC
        wbc_choice = self.random.choices(["Normal", "Leukocytosis"], weights=[90, 10], k=1)[0]
        if wbc_choice == "Leukocytosis":
             wbc_val = self.random.randint(11000, 16000)
        else:
             wbc_val = self.random.randint(4500, 10500)

        # CBC - Hb
        hb_choice = self.random.choices(["Polycythemia", "Anemia", "Normal"], weights=[30, 20, 50], k=1)[0]
        if hb_choice == "Polycythemia":
             hb_val = round(self.random.uniform(16.1, 18.0), 1)
        elif hb_choice == "Anemia":
             hb_val = round(self.random.uniform(9.0, 11.9), 1)
        else:
             hb_val = round(self.random.uniform(12.0, 16.0), 1)

        # CBC - Plt
        plt_choice = self.random.choices(["Thrombocytopenia", "Normal"], weights=[20, 80], k=1)[0]
        if plt_choice == "Thrombocytopenia":
             plt_val = self.random.randint(100, 149) * 1000
        else:
             plt_val = self.random.randint(150, 450) * 1000

        # ESR & CRP
        esr_choice = self.random.choices(["Elevated", "Normal"], weights=[25, 75], k=1)[0]
        esr_val = f"{self.random.randint(30, 80)} mm/hr" if esr_choice == "Elevated" else f"{self.random.randint(5, 20)} mm/hr"
        
        crp_choice = self.random.choices(["Elevated", "Normal"], weights=[30, 70], k=1)[0]
        crp_val = f"{self.random.randint(11, 40)} mg/L" if crp_choice == "Elevated" else f"{self.random.randint(1, 10)} mg/L"

        # LFTs
        lft_choice = self.random.choices(["Elevated", "Normal"], weights=[30, 70], k=1)[0]
        if lft_choice == "Elevated":
             alt_val = f"{self.random.randint(41, 100)} U/L"
             ast_val = f"{self.random.randint(41, 100)} U/L"
        else:
             alt_val = f"{self.random.randint(7, 40)} U/L"
             ast_val = f"{self.random.randint(10, 40)} U/L"

        # VBG
        ph_choice = self.random.choices(["Alkalosis", "Acidosis", "Normal"], weights=[50, 10, 40], k=1)[0]
        if ph_choice == "Alkalosis": ph_val = round(self.random.uniform(7.46, 7.55), 2)
        elif ph_choice == "Acidosis": ph_val = round(self.random.uniform(7.25, 7.34), 2)
        else: ph_val = round(self.random.uniform(7.35, 7.45), 2)

        pco2_choice = self.random.choices(["Hypocapnia", "Hypercapnia", "Normal"], weights=[60, 10, 30], k=1)[0]
        if pco2_choice == "Hypocapnia": pco2_val = self.random.randint(25, 34)
        elif pco2_choice == "Hypercapnia": pco2_val = self.random.randint(46, 60)
        else: pco2_val = self.random.randint(35, 45)

        hco3_choice = self.random.choices(["Decreased", "Normal"], weights=[40, 60], k=1)[0]
        if hco3_choice == "Decreased": hco3_val = self.random.randint(18, 21)
        else: hco3_val = self.random.randint(22, 26)

        # ==================== SPECIALIZED TESTS ====================
        
        # D-dimer
        ddimer = self.random.choices(["> 500 ng/mL (Elevated)", "< 500 ng/mL (Normal)"], weights=[30, 70], k=1)[0]
        
        # BNP/NT-proBNP
        bnp_choice = self.random.choices(["Elevated", "Normal"], weights=[90, 10], k=1)[0]
        if bnp_choice == "Elevated":
            bnp_val = "Elevated (> 100 pg/mL) or NT-proBNP (> 300 pg/mL)"
        else:
            bnp_val = "Normal Range"

        # a1-antitrypsin
        a1at = self.random.choices(["Low levels", "Normal levels"], weights=[5, 95], k=1)[0]

        # ==================== IMMUNITY & SEROLOGY ====================
        
        # HIV
        hiv = self.random.choices(["Positive", "Negative"], weights=[5, 95], k=1)[0]
        
        # Autoimmune
        auto_choice = self.random.choices(["Positive", "Negative"], weights=[25, 75], k=1)[0]
        auto_res = "Positive ANA or specific antibodies (Scl-70, Centromere)" if auto_choice == "Positive" else "Negative"

        # Imaging Placeholder Logic (Already defined or simple)
        cxr = "Prominent Main Pulmonary Arteries and Enlarged Right Heart Border."
        
        return {
            "basic_blood_tests": {
                "CBC": {
                    "Hb": f"{hb_val} g/dL", 
                    "WBC": f"{wbc_val} /uL", 
                    "Plt": f"{plt_val} /uL"
                },
                "ESR": esr_val,
                "CRP": crp_val,
                "BMP": {
                    "Na": f"{na_val} mEq/L", 
                    "BUN": f"{bun_val} mg/dL", 
                    "Cr": f"{cr_val} mg/dL"
                },
                "LFTs": {
                    "ALT": alt_val, 
                    "AST": ast_val
                },
                "VBG": {
                    "pH": str(ph_val), 
                    "PCO2": f"{pco2_val} mmHg", 
                    "HCO3": f"{hco3_val} mEq/L"
                }
            },
            "specialized_lung_tests": {
                "D_dimer": ddimer,
                "BNP_NT_proBNP": bnp_val,
                "Sputum_AFB": "Negative",
                "Sputum_analysis": {
                    "Gram_Stain": "No organisms seen",
                    "Sample_Quality": "N/A"
                },
                "a1_antitrypsin_level": a1at
            },
            "immunity_and_serology": {
                "HIV_test": hiv,
                "Autoimmune_pannel_ANA_ANCA": auto_res
            },
            "simple_imaging": {
                "Chest_X_Ray": {"PA_Lateral_Findings_and_Effusion": cxr}
            },
            "advanced_imaging": {
                "Chest_CT_CTPA": {"Lung_Parenchyma_and_Pleura": self._get_radiology_finding()}
            },
            "functional_tests": self._gen_functional_tests(),
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
