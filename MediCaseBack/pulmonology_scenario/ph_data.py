import random

class PHDataGenerator:
    """
    کلاسی برای تولید داده‌های شبیه‌سازی شده فشار خون ریوی (PH).
    
    Logic Drivers (متغیرهای اصلی برای حفظ سازگاری بالینی):
    1. RV_DYSFUNCTION: (None/Mild/Severe) - مهم‌ترین عامل تعیین‌کننده یافته‌های قلبی (JVD, Edema, P2).
    2. FUNCTIONAL_CLASS: (FC I-II vs FC III-IV) - مهم‌ترین عامل تعیین‌کننده علائم حیاتی و تنگی نفس.
    3. PH_GROUP: (Group 1 PAH, Group 3-ILD, Group 3-COPD) - مهم‌ترین عامل تعیین‌کننده PFT.
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
        
        # PH Group (Source: PH.txt PFT distribution and general knowledge)
        # Group 1 (PAH): 60%, Group 3 (ILD-PH): 20%, Group 3 (COPD-PH): 20%
        self.ph_group = self.random.choices(
            ["Group 1 (PAH)", "Group 3 (ILD-PH)", "Group 3 (COPD-PH)"], 
            weights=[60, 20, 20], k=1
        )[0]
        
        # Functional Class (Source: PH.txt Tachycardia and Hypotension are common in FC III-IV)
        # FC I-II (Mild/Moderate): 40%, FC III-IV (Severe): 60%
        self.functional_class = self.random.choices(
            ["FC I-II", "FC III-IV"], 
            weights=[40, 60], k=1
        )[0]

        # RV Dysfunction Severity (Cor Pulmonale) - Driven by Functional Class
        if self.functional_class == "FC III-IV":
            # 70% Severe Dysfunction/Cor Pulmonale
            self.rv_dysfunction = self.random.choices(["Severe", "Mild/None"], weights=[70, 30])[0]
        else:
            # 85% Mild/None
            self.rv_dysfunction = self.random.choices(["Severe", "Mild/None"], weights=[15, 85])[0]

        # Holders for consistency checks
        self.simulated_spo2_val = 95
        self.simulated_rr_val = 20
        self.simulated_bp_systolic = 120

    # --- Helper Methods ---
    def _generate_value(self, distributions, is_int=False, precision=2):
        # Generates a value based on weighted ranges (simplified)
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
        # PH often presents in middle to older age groups
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
        # BP Logic: Driven by RV Dysfunction/FC (Source: PH.txt)
        if self.rv_dysfunction == "Severe": # Hypotension (reduced cardiac output)
            sys = self.random.randint(85, 99) # 15% < 100 mmHg
            dia = self.random.randint(50, 65)
        else:
            bp_choice = self.random.choices(["Normal", "High"], weights=[70, 30])[0] # 60% Normal, 25% High
            if bp_choice == "Normal":
                sys = self.random.randint(110, 139)
                dia = self.random.randint(70, 89)
            else:
                sys = self.random.randint(141, 165)
                dia = self.random.randint(90, 105)
        
        self.simulated_bp_systolic = sys

        # PR Logic: Tachycardia is compensatory (Source: PH.txt)
        if self.functional_class == "FC III-IV": # 60% Tachy (100-120)
            pr = self.random.randint(100, 120)
        else:
            pr = self.random.randint(65, 99) # 30% Normal

        # RR Logic: Tachypnea common due to increased drive (Source: PH.txt)
        if self.functional_class == "FC III-IV" or self.simulated_bp_systolic < 100: # 70% > 20
            rr = self.random.randint(22, 30)
        else:
            rr = self.random.randint(14, 20)
        
        self.simulated_rr_val = rr

        # SpO2 Logic: Hypoxemia common, especially in Group 3 (Source: PH.txt)
        if self.rv_dysfunction == "Severe": # Severe Hypoxemia (<88%)
            spo2 = self.random.randint(83, 87)
        elif self.ph_group.startswith("Group 3"): # Mild/Moderate Hypoxemia (88-94%)
            spo2 = self.random.randint(88, 94)
        else: # Group 1 PAH (often better SpO2)
            spo2 = self.random.randint(95, 98) 
        
        self.simulated_spo2_val = spo2

        # Temperature: 95% Normal (Source: PH.txt)
        temp = round(self.random.uniform(36.5, 37.5), 1)

        return {
            "BP": f"{sys}/{dia} mmHg",
            "T": f"{temp} °C",
            "PR": f"{pr} bpm",
            "RR": f"{rr} breaths/min",
            "SpO2": f"{spo2}% (Room Air)",
            "GCS": "15"
        }

    # --- 2. General Appearance ---
    def _gen_general_appearance(self):
        # Dyspnea (Tنگی نفس) driven by Functional Class
        if self.functional_class == "FC III-IV":
            dyspnea_val = "Dyspnea at rest or minimal exertion."
        else:
            dyspnea_val = "Dyspnea with moderate to strenuous exertion."

        # Cyanosis: Driven by SpO2
        cyanosis = "Central Cyanosis Present." if self.simulated_spo2_val < 90 else "No Cyanosis."

        # Edema: Driven by RV Dysfunction
        if self.rv_dysfunction == "Severe":
            edema = "Pitting Edema (Bilateral, Dependent)."
        else:
            edema = "No Peripheral Edema."

        return {
            "level_of_consciousness_mood_and_behavior": {
                "level_of_consciousness": "Alert and Oriented.",
                "mood": "Anxious or Distressed.",
                "behavior": "Cooperative."
            },
            "posture_and_position": {
                "position_of_comfort": "Orthopnea/Semi-Fowler's position may be preferred."
            },
            "overall_appearance": {
                "nutritional_status": "Normal."
            },
            "cardiopulmonary_and_circulatory_clues": {
                "cyanosis": cyanosis,
                "dyspnea": dyspnea_val,
                "edema": edema
            }
        }

    # --- 3. Head and Neck (Mostly Normal) ---
    def _gen_head_neck(self):
        # JVP Logic: Driven by RV Dysfunction
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
        # Findings based on PH Group (Group 3 shows primary lung disease findings)
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
                "breath_sounds_intensity": "Normal Intensity.",
                "adventitious_sounds": adventitious
            }
        }

    # --- 5. Cardiovascular System (Crucial Section) ---
    def _gen_cardio(self):
        # Heart Sounds: P2 Loudness and Murmurs driven by RV Dysfunction
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

        # Peripheral Pulses (Weak if Hypotensive/Shock)
        pulse_qual = "Weak and Thready" if self.simulated_bp_systolic < 100 else "Peripheral Pulses Symmetric and 2+."
        extremities = "Cool and Pale with Capillary Refill > 2 seconds." if self.simulated_bp_systolic < 100 else "Extremities Warm, Capillary Refill < 2 seconds."
        
        # NOTE: JVP is already generated in Head and Neck section for structural consistency.

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
        # Hepatomegaly (جگر بزرگ) due to right heart failure
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

    # --- 7. Neurological (Normal) ---
    def _gen_neuro(self):
        return {
            "mental_status_and_LOC": "Mental Status: Alert and Oriented.",
            "motor_strength_and_tone": "Motor Strength 5/5 Bilaterally."
        }

    # --- 8. Musculoskeletal ---
    def _gen_msk(self):
        # Clubbing (چماقی شدن انگشتان) is only present if PH is secondary to a chronic lung disease (Group 3-ILD)
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
        """
        تولید یافته‌های CT سینه (Lung Parenchyma and Pleura) بر اساس درصد‌های جهانی درخواستی 
        و وابستگی‌های بالینی برای یافتن PA Enlargement.
        """
        
        # 1. تعریف یافته‌های پارانشیم ریه (مجموع درصدها: 10% + 3% + 2% + 5% = 20%)
        # اینها یافته‌هایی هستند که به نوع PH Group وابسته هستند، اما درصد آن‌ها در جمعیت کلی PH کم است.
        parenchymal_findings_choices = [
            "Mosaic perfusion pattern",  # CTEPH (Group 4) - 10%
            "Fibrotic changes",          # Group 3 PH (ILD-PH) - 3%
            "Emphysematous changes",     # Group 3 PH (COPD-PH) - 2%
            "Normal parenchyma"          # Group 1 (PAH) - 5%
        ]
        parenchymal_weights = [10, 3, 2, 5]
        
        # 2. تعریف یافته اصلی عروقی (PA Enlargement)
        # این یافته در 80% کل موارد PH وجود دارد.
        pa_enlargement_finding = "PA diameter > Aorta diameter" 
        
        # 3. انتخاب تصادفی وضعیت کلی: آیا یافته اصلی عروقی وجود دارد یا نه؟ (80% در مقابل 20%)
        # 80% احتمال دارد که PA Enlargement وجود داشته باشد.
        # 20% احتمال دارد که یکی از یافته‌های پارانشیمال/نرمال (که در بالا تعریف شد) رخ دهد.
        
        overall_choice = self.random.choices(
            ["PA_ENLARGEMENT", "PARENCHYMAL_OR_NORMAL"], 
            weights=[80, 20], 
            k=1
        )[0]
        
        final_output = []
        
        # --- ساختار خروجی بر اساس انتخاب ---
        
        if overall_choice == "PA_ENLARGEMENT":
            final_output=f"{pa_enlargement_finding}"
            
        else:
            # اگر یکی از 20% باقیمانده (یافته‌های پارانشیمال/نرمال) انتخاب شد.
            # یکی از موارد 10%، 3%، 2%، یا 5% را انتخاب می‌کنیم.
            chosen_parenchymal = self.random.choices(
                parenchymal_findings_choices, 
                weights=parenchymal_weights, 
                k=1
            )[0]
            
            # بر اساس یافته انتخاب شده، قاعده و خروجی مربوطه را تولید می‌کنیم.
            if chosen_parenchymal == "Mosaic perfusion pattern":
                final_output=f"{chosen_parenchymal}"
            elif chosen_parenchymal == "Fibrotic changes":
                final_output=f"{chosen_parenchymal}"
            elif chosen_parenchymal == "Emphysematous changes":
                final_output=f"{chosen_parenchymal}"
            elif chosen_parenchymal == "Normal parenchyma":
                final_output=f"{chosen_parenchymal}"

        return final_output
    
    # در داخل کلاس PHDataGenerator
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

    def _get_spirometry_data(self):
        """
        تولید داده‌های FEV1, FVC و FEV1/FVC Ratio بر اساس وابستگی‌های اعلام شده.
        این داده‌ها عمدتاً برای Group 1 PAH (بیماری عروقی خالص) معتبر هستند.
        """
        
        # مقادیر مرجع (Predicted) را با اندکی تغییر در رنج‌های شما تعریف می‌کنیم
        # این مقادیر فقط برای محاسبه 'Measured' استفاده می‌شوند.
        pred_fev1_val = self.random.uniform(3.50, 3.80) # حول و حوش 3.65 L
        pred_fvc_val = self.random.uniform(4.30, 4.70)  # حول و حوش 4.50 L
        pred_ratio_val = self.random.uniform(0.79, 0.83) # حول و حوش 0.81
        
        # --- FEV1 Logic (80/20) ---
        fev1_pct_choices = [
            (self.random.uniform(80.0, 120.0), (2.90, 4.40), "80-120%"), # 80%
            (self.random.uniform(60.0, 79.0), (2.20, 2.90), "60-79%")   # 20%
        ]
        fev1_pct, fev1_range, fev1_pct_text = self.random.choices(fev1_pct_choices, weights=[80, 20], k=1)[0]
        meas_fev1 = self.random.uniform(fev1_range[0], fev1_range[1]) # انتخاب مقدار Measured از رنج درخواستی
        
        # --- FVC Logic (80/20) ---
        fvc_pct_choices = [
            (self.random.uniform(80.0, 120.0), (3.60, 5.40), "80-120%"), # 80%
            (self.random.uniform(60.0, 79.0), (2.70, 3.55), "60-79%")   # 20%
        ]
        fvc_pct, fvc_range, fvc_pct_text = self.random.choices(fvc_pct_choices, weights=[80, 20], k=1)[0]
        meas_fvc = self.random.uniform(fvc_range[0], fvc_range[1]) # انتخاب مقدار Measured از رنج درخواستی

        # --- Ratio Logic (100%) ---
        meas_ratio = self.random.uniform(0.70, 0.85)
        
        # در صورت وجود بیماری زمینه‌ای (Group 3)، باید این مقادیر تعدیل شوند
        if self.ph_group.startswith("Group 3"):
            if "ILD" in self.ph_group:
                # الگوی محدودیت (Restriction): FVC و FEV1 کاهش یافته، نسبت نرمال یا بالا
                meas_fvc = self.random.uniform(0.5 * pred_fvc_val, 0.79 * pred_fvc_val)
                meas_ratio = self.random.uniform(0.80, 0.95)
                meas_fev1 = meas_fvc * meas_ratio # حفظ تناسب
                fev1_pct_text = fvc_pct_text = "50-79%"
            elif "COPD" in self.ph_group:
                # الگوی انسداد (Obstruction): FEV1 کاهش یافته، نسبت پایین
                meas_ratio = self.random.uniform(0.40, 0.69)
                meas_fev1 = self.random.uniform(0.4 * pred_fev1_val, 0.79 * pred_fev1_val)
                meas_fvc = meas_fev1 / meas_ratio # حفظ تناسب
                fev1_pct_text = "40-79%"
                fvc_pct_text = "80-100%"
                
        
        # ساختار خروجی مطابق با جزئیات درخواستی
        return {
            "FEV1": f"Measured: {meas_fev1:.2f} L, Predicted: {pred_fev1_val:.2f} L, %Predicted: {fev1_pct_text}",
            "FVC": f"Measured: {meas_fvc:.2f} L, Predicted: {pred_fvc_val:.2f} L, %Predicted: {fvc_pct_text}",
            "FEV1/FVC_Ratio": f"Measured: {meas_ratio:.2f}, Predicted: {pred_ratio_val:.2f}, %Predicted: {(meas_ratio/pred_ratio_val)*100:.0f}%"
        }
    
    # در داخل کلاس PHDataGenerator
    def _gen_functional_tests(self):
        """
        تولید مقادیر عددی برای تست‌های عملکرد ریه و سایر تست‌های عملکردی.
        """
        
        # فراخوانی متد جدید برای تولید داده‌های اسپیرومتری
        spirometry_data = self._get_spirometry_data()
        
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
            "spirometry": {
                "result": {
                    "FEV1": spirometry_data["FEV1"],
                    "FVC": spirometry_data["FVC"],
                    "FEV1/FVC_Ratio": spirometry_data["FEV1/FVC_Ratio"]
                },
                "Reversibility": "FEV1 increase < 12% AND < 200 mL"
            }, 
            "dlco": dlco_value,
            "peak_flow": pef_val,
            "plethysmography": pleth_val
        }

    # --- 9. Paraclinic Tests (Crucial Section) ---
    def _gen_paraclinic(self):
        
        # 1. BNP/Troponin: Driven by RV Dysfunction
        if self.rv_dysfunction == "Severe":
            bnp = "Severely Elevated."
            trop = "Borderline/Positive Troponin."
        else:
            bnp = "Normal or Mildly Elevated."
            trop = "Negative Troponin."

        # 2. CBC: Polycythemia if chronic hypoxemia (Group 3)
        if self.ph_group.startswith("Group 3") and self.simulated_spo2_val < 92:
            hb = "17.0 g/dL."
        else:
            hb = "14.0 g/dL."

        # 3. ABG: Respiratory Alkalosis if Tachypnea (RR > 22)
        if self.simulated_rr_val > 22:
            ph = "7.47"
            paco2 = "32 mmHg"
            
            # --- HCO3 Logic for Chronic Respiratory Alkalosis (40/60) ---
            # اگر آلکالوز تنفسی حاد باشد، بدن سعی می‌کند با کاهش HCO3 جبران کند.
            hco3_scenario = self.random.choices(
                ["Compensatory decrease", "Normal"], 
                weights=[40, 60], 
                k=1
            )[0]

            if hco3_scenario == "Compensatory decrease":
                num = random.randint(18, 21)
                hco3 = f"{num} mEq/L"
            else:
                num = random.randint(22, 26)
                hco3 = f"{num} mEq/L"
                
        else:
            ph = "7.40"
            paco2 = "40 mmHg"
            num = random.randint(22, 26)
            hco3 = f"{num} mEq/L"

        cxr = "Prominent Main Pulmonary Arteries and Enlarged Right Heart Border."

        return {
            "basic_blood_tests": {
                "CBC": {"Hb": hb, "WBC": "9000 /uL", "Plt": "250,000 /uL"},
                "BMP": {"Na": "138", "BUN": "20", "Cr": "1.1"},
                "VBG": {"pH": ph, "PaCO2": paco2, "HCO3": hco3}
            },
            "specialized_lung_tests": {
                "D_dimer": "Normal",
                "BNP_NT_proBNP": bnp,
                "Troponin": trop
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
