import random
import json

class PHDataGenerator:
    """
    کلاسی برای تولید داده‌های شبیه‌سازی شده Pulmonary Hypertension بر اساس فایل pulmonary hypertension.txt.
    
    Scenarios:
    1. idiopathic_pah (5%)
    2. ph_left_heart (75%)
    3. ph_lung_disease (20%)
    """
    
    # --- داده‌های دموگرافیک (ثابت) ---
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

    # --- داده‌های استخراج شده از فایل متنی ---
    DATA_SOURCE = {
      "physical_exam": {
        "vital_signs": {
          "BP": {
            "idiopathic_pah": [{"min": 110, "max": 130}, {"min": 70, "max": 85}],
            "ph_left_heart": [{"min": 130, "max": 160}, {"min": 80, "max": 100}],
            "ph_lung_disease": [{"min": 110, "max": 135}, {"min": 70, "max": 85}]
          },
          "T": {
            "idiopathic_pah": [{"min": 36.5, "max": 37.2}],
            "ph_left_heart": [{"min": 36.5, "max": 37.2}],
            "ph_lung_disease": [{"min": 36.5, "max": 37.2}]
          },
          "PR": {
            "idiopathic_pah": [{"min": 80, "max": 100}],
            "ph_left_heart": [{"min": 85, "max": 110}],
            "ph_lung_disease": [{"min": 85, "max": 105}]
          },
          "RR": {
            "idiopathic_pah": [{"min": 16, "max": 22}],
            "ph_left_heart": [{"min": 20, "max": 28}],
            "ph_lung_disease": [{"min": 20, "max": 26}]
          },
          "SpO2": {
            "idiopathic_pah": [{"min": 92, "max": 96}],
            "ph_left_heart": [{"min": 88, "max": 94}],
            "ph_lung_disease": [{"min": 85, "max": 92}]
          },
          "GCS": {
            "idiopathic_pah": [{"min": 15, "max": 15}],
            "ph_left_heart": [{"min": 15, "max": 15}],
            "ph_lung_disease": [{"min": 14, "max": 15}]
          }
        },
        "general_appearance": {
          "mood_and_behavior": {
            "idiopathic_pah": ["Alert and cooperative", "Calm with no acute distress"],
            "ph_left_heart": ["Anxious and restless"],
            "ph_lung_disease": ["Lethargic or drowsy", "Calm with no acute distress"]
          },
          "overall_appearance": {
            "idiopathic_pah": ["Well-nourished and well-developed"],
            "ph_left_heart": ["Well-nourished and well-developed"],
            "ph_lung_disease": ["Cachectic and thin", "Cyanosis"]
          },
          "posture_and_position": {
            "idiopathic_pah": ["Supine with no distress"],
            "ph_left_heart": ["Orthopnea", "Unable to lie flat"],
            "ph_lung_disease": ["Sitting upright in tripod position"]
          },
          "level_of_consciousness": {
            "idiopathic_pah": ["Alert and oriented x3"],
            "ph_left_heart": ["Alert and oriented x3"],
            "ph_lung_disease": ["Alert and oriented x3", "Confused or disoriented"]
          },
          "cardiopulmonary_and_circulatory_clues": {
            "edema": {
              "idiopathic_pah": ["No edema", "Trace pedal edema"],
              "ph_left_heart": ["Pitting edema in lower extremities"],
              "ph_lung_disease": ["No edema", "Trace pedal edema"]
            },
            "dyspnea": {
              "idiopathic_pah": ["Dyspnea on exertion"],
              "ph_left_heart": ["Paroxysmal nocturnal dyspnea", "Dyspnea at rest"],
              "ph_lung_disease": ["Dyspnea at rest", "Dyspnea on exertion"]
            },
            "cyanosis": {
              "idiopathic_pah": ["No cyanosis"],
              "ph_left_heart": ["No cyanosis"],
              "ph_lung_disease": ["Central cyanosis", "Peripheral cyanosis"]
            }
          }
        },
        "head_and_neck": {
          "head_and_face": {
            "symmetry_and_lesions": {
              "idiopathic_pah": ["Symmetric with no lesions"],
              "ph_left_heart": ["Symmetric with no lesions"],
              "ph_lung_disease": ["Symmetric with no lesions"]
            },
            "tenderness": {
              "idiopathic_pah": ["Non-tender"],
              "ph_left_heart": ["Non-tender"],
              "ph_lung_disease": ["Non-tender"]
            }
          },
          "eyes": {
            "sclera_and_conjunctiva": {
              "idiopathic_pah": ["Normal sclera and pink conjunctiva"],
              "ph_left_heart": ["Normal sclera and pink conjunctiva"],
              "ph_lung_disease": ["Injected or red conjunctiva"]
            },
            "pupils_reaction": {
              "idiopathic_pah": ["PERRLA"],
              "ph_left_heart": ["PERRLA"],
              "ph_lung_disease": ["PERRLA"]
            },
            "extraocular_movements": {
              "idiopathic_pah": ["Intact"],
              "ph_left_heart": ["Intact"],
              "ph_lung_disease": ["Intact"]
            }
          },
          "ears": {
            "external_and_tenderness": {
              "idiopathic_pah": ["Normal external ear, no tenderness"],
              "ph_left_heart": ["Normal external ear, no tenderness"],
              "ph_lung_disease": ["Normal external ear, no tenderness"]
            },
            "eardrum_appearance": {
              "idiopathic_pah": ["Intact pearly gray tympanic membrane"],
              "ph_left_heart": ["Intact pearly gray tympanic membrane"],
              "ph_lung_disease": ["Intact pearly gray tympanic membrane"]
            }
          },
          "nose_and_sinuses": {
            "septum_and_discharge": {
              "idiopathic_pah": ["Midline septum, no discharge"],
              "ph_left_heart": ["Midline septum, no discharge"],
              "ph_lung_disease": ["Midline septum, no discharge"]
            },
            "sinus_tenderness": {
              "idiopathic_pah": ["Non-tender"],
              "ph_left_heart": ["Non-tender"],
              "ph_lung_disease": ["Non-tender"]
            }
          },
          "mouth_and_pharynx": {
            "oral_mucosa_and_lesions": {
              "idiopathic_pah": ["Moist and pink"],
              "ph_left_heart": ["Moist and pink"],
              "ph_lung_disease": ["Central cyanosis under the tongue"]
            },
            "pharynx_and_tonsils": {
              "idiopathic_pah": ["Non-erythematous, no exudates"],
              "ph_left_heart": ["Non-erythematous, no exudates"],
              "ph_lung_disease": ["Non-erythematous, no exudates"]
            }
          },
          "neck_and_lymphatics": {
            "inspection": {
              "idiopathic_pah": ["Trachea midline"],
              "ph_left_heart": ["Trachea midline"],
              "ph_lung_disease": ["Trachea midline"]
            },
            "tracheal_position": {
              "idiopathic_pah": ["Trachea midline"],
              "ph_left_heart": ["Trachea midline"],
              "ph_lung_disease": ["Trachea midline"]
            },
            "thyroid_gland": {
              "idiopathic_pah": ["Non-palpable"],
              "ph_left_heart": ["Non-palpable"],
              "ph_lung_disease": ["Non-palpable"]
            },
            "carotid_bruit": {
              "idiopathic_pah": ["No bruits"],
              "ph_left_heart": ["Bruit present"],
              "ph_lung_disease": ["No bruits"]
            },
            "lymph_nodes_size_consistency": {
              "idiopathic_pah": ["No lymphadenopathy"],
              "ph_left_heart": ["No lymphadenopathy"],
              "ph_lung_disease": ["No lymphadenopathy"]
            },
            "lymph_nodes_mobility_tenderness": {
              "idiopathic_pah": ["No lymphadenopathy"],
              "ph_left_heart": ["No lymphadenopathy"],
              "ph_lung_disease": ["No lymphadenopathy"]
            }
          }
        },
        "respiratory_system": {
          "inspection": {
            "accessory_muscles": {
              "idiopathic_pah": ["No accessory muscle use"],
              "ph_left_heart": ["No accessory muscle use"],
              "ph_lung_disease": ["Use of sternocleidomastoid muscles"]
            },
            "chest_shape_and_symmetry": {
              "idiopathic_pah": ["Symmetric chest rise"],
              "ph_left_heart": ["Symmetric chest rise"],
              "ph_lung_disease": ["Barrel chest", "Kyphoscoliosis"]
            }
          },
          "palpation": {
            "chest_expansion": {
              "idiopathic_pah": ["Symmetric expansion"],
              "ph_left_heart": ["Symmetric expansion"],
              "ph_lung_disease": ["Globally decreased expansion"]
            },
            "tactile_fremitus": {
              "idiopathic_pah": ["Normal tactile fremitus"],
              "ph_left_heart": ["Normal tactile fremitus"],
              "ph_lung_disease": ["Decreased tactile fremitus"]
            }
          },
          "percussion": {
            "idiopathic_pah": ["Resonant"],
            "ph_left_heart": ["Dull"],
            "ph_lung_disease": ["Hyper-resonant"]
          },
          "auscultation": {
            "breath_sounds_intensity": {
              "idiopathic_pah": ["Vesicular sounds, normal intensity"],
              "ph_left_heart": ["Vesicular sounds, normal intensity", "Decreased breath sounds"],
              "ph_lung_disease": ["Decreased breath sounds"]
            },
            "adventitious_sounds": {
              "idiopathic_pah": ["No adventitious sounds"],
              "ph_left_heart": ["Fine Crackles", "Coarse Crackles"],
              "ph_lung_disease": ["Wheezing", "Rhonchi"]
            }
          }
        },
        "cardiovascular_system": {
          "JVP_assessment": {
            "idiopathic_pah": ["Elevated JVP"],
            "ph_left_heart": ["Elevated JVP", "Distended neck veins"],
            "ph_lung_disease": ["Elevated JVP"]
          },
          "palpation": {
            "precordial_palpation_heave_thrill": {
              "idiopathic_pah": ["Right Ventricular Heave", "Palpable thrill"],
              "ph_left_heart": ["No heaves or thrills"],
              "ph_lung_disease": ["Right Ventricular Heave"]
            },
            "pmi_assessment": {
              "idiopathic_pah": ["PMI at 5th ICS MCL"],
              "ph_left_heart": ["PMI displaced laterally"],
              "ph_lung_disease": ["PMI strictly unpalpable"]
            }
          },
          "auscultation": {
            "heart_sounds_s1_s2": {
              "idiopathic_pah": ["Loud P2", "Fixed split S2"],
              "ph_left_heart": ["Normal S1, S2"],
              "ph_lung_disease": ["Loud P2"]
            },
            "extra_sounds_s3_s4_murmurs": {
              "idiopathic_pah": ["Holosystolic murmur at left lower sternal border"],
              "ph_left_heart": ["S3 Gallop", "Holosystolic murmur at left lower sternal border"],
              "ph_lung_disease": ["Holosystolic murmur at left lower sternal border"]
            }
          },
          "2_pulses_and_extremities": {
            "peripheral_pulses_symmetry_and_quality": {
              "idiopathic_pah": ["Pulses 2+ and symmetric"],
              "ph_left_heart": ["Pulses 2+ and symmetric"],
              "ph_lung_disease": ["Pulses 2+ and symmetric"]
            },
            "extremities_color_and_trophic_changes": {
              "idiopathic_pah": ["No trophic changes"],
              "ph_left_heart": ["No trophic changes"],
              "ph_lung_disease": ["Clubbing of fingers"]
            },
            "extremities_temperature_and_cap_refill": {
              "idiopathic_pah": ["Warm extremities"],
              "ph_left_heart": ["Cool extremities, delayed capillary refill"],
              "ph_lung_disease": ["Warm extremities"]
            },
            "extremities_edema": {
              "idiopathic_pah": ["Trace pedal edema"],
              "ph_left_heart": ["Bilateral pitting edema"],
              "ph_lung_disease": ["Trace pedal edema"]
            }
          }
        },
        "abdominal_system": {
          "inspection": {
            "idiopathic_pah": ["Flat, non-distended"],
            "ph_left_heart": ["Distended"],
            "ph_lung_disease": ["Flat, non-distended"]
          },
          "auscultation": {
            "bowel_sounds": {
              "idiopathic_pah": ["Normoactive bowel sounds"],
              "ph_left_heart": ["Normoactive bowel sounds"],
              "ph_lung_disease": ["Normoactive bowel sounds"]
            },
            "vascular_bruits": {
              "idiopathic_pah": ["No bruits"],
              "ph_left_heart": ["No bruits"],
              "ph_lung_disease": ["No bruits"]
            }
          },
          "percussion": {
            "general": {
              "idiopathic_pah": ["Resonant"],
              "ph_left_heart": ["Resonant"],
              "ph_lung_disease": ["Resonant"]
            },
            "organ_borders": {
              "idiopathic_pah": ["Hepatomegaly"],
              "ph_left_heart": ["Hepatomegaly"],
              "ph_lung_disease": ["Hepatomegaly"]
            }
          },
          "palpation": {
            "superficial_tenderness": {
              "idiopathic_pah": ["Right upper quadrant tenderness"],
              "ph_left_heart": ["Right upper quadrant tenderness"],
              "ph_lung_disease": ["Soft, non-tender"]
            },
            "deep_masses_and_organs": {
              "idiopathic_pah": ["Pulsatile liver edge"],
              "ph_left_heart": ["Pulsatile liver edge"],
              "ph_lung_disease": ["No masses or organomegaly"]
            }
          },
          "peritoneal_signs": {
            "idiopathic_pah": ["None"],
            "ph_left_heart": ["None"],
            "ph_lung_disease": ["None"]
          }
        },
        "neurological": {
          "mental_status_and_LOC": {
            "idiopathic_pah": ["Alert and Oriented"],
            "ph_left_heart": ["Alert and Oriented"],
            "ph_lung_disease": ["Alert and Oriented"]
          },
          "cranial_nerves": {
            "idiopathic_pah": ["Intact"],
            "ph_left_heart": ["Intact"],
            "ph_lung_disease": ["Intact"]
          },
          "motor_strength_and_tone": {
            "idiopathic_pah": ["5/5 strength globally"],
            "ph_left_heart": ["5/5 strength globally"],
            "ph_lung_disease": ["5/5 strength globally"]
          },
          "involuntary_movements": {
            "idiopathic_pah": ["None"],
            "ph_left_heart": ["None"],
            "ph_lung_disease": ["None"]
          },
          "sensory_light_touch_and_pain": {
            "idiopathic_pah": ["Intact"],
            "ph_left_heart": ["Intact"],
            "ph_lung_disease": ["Intact"]
          },
          "deep_tendon_reflexes": {
            "idiopathic_pah": ["2+"],
            "ph_left_heart": ["2+"],
            "ph_lung_disease": ["2+"]
          },
          "coordination_and_gait": {
            "idiopathic_pah": ["Intact"],
            "ph_left_heart": ["Intact"],
            "ph_lung_disease": ["Intact"]
          }
        },
        "musculoskeletal_system": {
          "inspection": {
            "joints": {
              "idiopathic_pah": ["Normal joints"],
              "ph_left_heart": ["Normal joints"],
              "ph_lung_disease": ["Normal joints"]
            },
            "muscles": {
              "idiopathic_pah": ["Normal bulk"],
              "ph_left_heart": ["Normal bulk"],
              "ph_lung_disease": ["Normal bulk"]
            }
          },
          "palpation": {
            "tenderness_and_crepitus": {
              "idiopathic_pah": ["No tenderness"],
              "ph_left_heart": ["No tenderness"],
              "ph_lung_disease": ["No tenderness"]
            }
          },
          "range_of_motion_active_passive": {
            "idiopathic_pah": ["Full"],
            "ph_left_heart": ["Full"],
            "ph_lung_disease": ["Full"]
          },
          "stability_and_function": {
            "idiopathic_pah": ["Stable"],
            "ph_left_heart": ["Stable"],
            "ph_lung_disease": ["Stable"]
          }
        }
      },
      "paraclinic": {
        "basic_blood_tests": {
          "BMP": {
            "Na": {
              "idiopathic_pah": [{"min": 135, "max": 145}],
              "ph_left_heart": [{"min": 130, "max": 145}],
              "ph_lung_disease": [{"min": 135, "max": 145}]
            },
            "BUN": {
              "idiopathic_pah": [{"min": 10, "max": 20}],
              "ph_left_heart": [{"min": 20, "max": 40}],
              "ph_lung_disease": [{"min": 10, "max": 25}]
            },
            "Cr": {
              "idiopathic_pah": [{"min": 0.7, "max": 1.1}],
              "ph_left_heart": [{"min": 1.0, "max": 1.5}],
              "ph_lung_disease": [{"min": 0.8, "max": 1.2}]
            }
          },
          "CBC": {
            "WBC": {
              "idiopathic_pah": [{"min": 4500, "max": 10000}],
              "ph_left_heart": [{"min": 4500, "max": 10000}],
              "ph_lung_disease": [{"min": 5000, "max": 12000}]
            },
            "Hb": {
              "idiopathic_pah": [{"min": 12.0, "max": 15.0}],
              "ph_left_heart": [{"min": 12.0, "max": 15.0}],
              "ph_lung_disease": [{"min": 15.0, "max": 18.0}]
            },
            "Plt": {
              "idiopathic_pah": [{"min": 150000, "max": 400000}],
              "ph_left_heart": [{"min": 150000, "max": 400000}],
              "ph_lung_disease": [{"min": 150000, "max": 400000}]
            }
          },
          "ESR": {
            "idiopathic_pah": [{"min": 0, "max": 15}],
            "ph_left_heart": [{"min": 0, "max": 20}],
            "ph_lung_disease": [{"min": 0, "max": 15}]
          },
          "CRP": {
            "idiopathic_pah": [{"min": 0, "max": 5}],
            "ph_left_heart": [{"min": 0, "max": 5}],
            "ph_lung_disease": [{"min": 0, "max": 5}]
          },
          "VBG": {
            "pH": {
              "idiopathic_pah": [{"min": 7.35, "max": 7.45}],
              "ph_left_heart": [{"min": 7.35, "max": 7.45}],
              "ph_lung_disease": [{"min": 7.35, "max": 7.42}]
            },
            "PCO2": {
              "idiopathic_pah": [{"min": 30, "max": 40}],
              "ph_left_heart": [{"min": 35, "max": 45}],
              "ph_lung_disease": [{"min": 45, "max": 55}]
            },
            "HCO3": {
              "idiopathic_pah": [{"min": 22, "max": 26}],
              "ph_left_heart": [{"min": 22, "max": 26}],
              "ph_lung_disease": [{"min": 26, "max": 30}]
            }
          },
          "LFTs": {
            "ALT": {
              "idiopathic_pah": [{"min": 20, "max": 50}],
              "ph_left_heart": [{"min": 20, "max": 60}],
              "ph_lung_disease": [{"min": 20, "max": 50}]
            },
            "AST": {
              "idiopathic_pah": [{"min": 20, "max": 50}],
              "ph_left_heart": [{"min": 20, "max": 60}],
              "ph_lung_disease": [{"min": 20, "max": 50}]
            }
          }
        },
        "specialized_lung_tests": {
          "D_dimer": {
            "idiopathic_pah": ["Negative"],
            "ph_left_heart": ["Negative"],
            "ph_lung_disease": ["Negative"]
          },
          "Sputum_AFB": {
            "idiopathic_pah": ["Negative"],
            "ph_left_heart": ["Negative"],
            "ph_lung_disease": ["Negative"]
          },
          "BNP_NT_proBNP": {
            "idiopathic_pah": ["Elevated"],
            "ph_left_heart": ["Elevated"],
            "ph_lung_disease": ["Elevated"]
          },
          "Sputum_analysis": {
            "Gram_Stain": {
              "idiopathic_pah": ["Normal flora"],
              "ph_left_heart": ["Normal flora"],
              "ph_lung_disease": ["Normal flora"]
            },
            "Sample_Quality": {
              "idiopathic_pah": ["Adequate"],
              "ph_left_heart": ["Adequate"],
              "ph_lung_disease": ["Adequate"]
            }
          },
          "a1_antitrypsin_level": {
            "idiopathic_pah": ["Normal range"],
            "ph_left_heart": ["Normal range"],
            "ph_lung_disease": ["Normal range"]
          }
        },
        "immunity_and_serology": {
          "HIV_test": {
            "idiopathic_pah": ["Negative"],
            "ph_left_heart": ["Negative"],
            "ph_lung_disease": ["Negative"]
          },
          "Autoimmune_pannel_ANA_ANCA": {
            "idiopathic_pah": ["Negative"],
            "ph_left_heart": ["Negative"],
            "ph_lung_disease": ["Negative"]
          }
        },
        "simple_imaging": {
          "Chest_X_Ray": {
            "PA_Lateral_Findings_and_Effusion": {
              "idiopathic_pah": ["Enlarged pulmonary arteries", "Clear lung fields"],
              "ph_left_heart": ["Cardiomegaly", "Pulmonary edema", "Pleural effusion"],
              "ph_lung_disease": ["Hyperinflation", "Fibrosis"]
            }
          }
        },
        "advanced_imaging": {
          "Chest_CT_CTPA": {
            "Lung_Parenchyma_and_Pleura": {
              "idiopathic_pah": ["Enlarged pulmonary arteries"],
              "ph_left_heart": ["Interlobular septal thickening", "Pleural effusion"],
              "ph_lung_disease": ["Emphysema", "Fibrosis"]
            }
          }
        },
        "functional_tests": {
          "dlco": {
            "idiopathic_pah": ["Normal"],
            "ph_left_heart": ["Normal"],
            "ph_lung_disease": ["Decreased"]
          },
          "peak_flow": {
            "idiopathic_pah": ["Normal range"],
            "ph_left_heart": ["Normal range"],
            "ph_lung_disease": ["Reduced"]
          },
          "Spirometry": {
            "Result": {
              "FEV1": {
                "idiopathic_pah": [{"min": 80, "max": 100}],
                "ph_left_heart": [{"min": 70, "max": 90}],
                "ph_lung_disease": [{"min": 40, "max": 70}]
              },
              "FVC": {
                "idiopathic_pah": [{"min": 80, "max": 100}],
                "ph_left_heart": [{"min": 70, "max": 90}],
                "ph_lung_disease": [{"min": 50, "max": 80}]
              },
              "FEV1/FVC": {
                "idiopathic_pah": [{"min": 75, "max": 85}],
                "ph_left_heart": [{"min": 75, "max": 85}],
                "ph_lung_disease": [{"min": 50, "max": 80}]
              }
            },
            "reversibility": {
              "idiopathic_pah": ["No significant reversibility"],
              "ph_left_heart": ["No significant reversibility"],
              "ph_lung_disease": ["No significant reversibility"]
            }
          },
          "plethysmography": {
            "idiopathic_pah": ["Normal lung volumes"],
            "ph_left_heart": ["Normal lung volumes"],
            "ph_lung_disease": ["Normal lung volumes"]
          }
        },
        "procedures": {
          "Bronchoscopy": {
            "idiopathic_pah": ["N/A"],
            "ph_left_heart": ["N/A"],
            "ph_lung_disease": ["N/A"]
          },
          "torachonthesis": {
            "Serum": {
              "Protein": {
                "idiopathic_pah": ["N/A"],
                "ph_left_heart": [{"min": 6.0, "max": 8.0}],
                "ph_lung_disease": ["N/A"]
              },
              "LDH": {
                "idiopathic_pah": ["N/A"],
                "ph_left_heart": [{"min": 140, "max": 200}],
                "ph_lung_disease": ["N/A"]
              },
              "Albumin": {
                "idiopathic_pah": ["N/A"],
                "ph_left_heart": [{"min": 3.5, "max": 5.0}],
                "ph_lung_disease": ["N/A"]
              }
            },
            "Fluid": {
              "Protein": {
                "idiopathic_pah": ["N/A"],
                "ph_left_heart": [{"min": 1.0, "max": 2.5}],
                "ph_lung_disease": ["N/A"]
              },
              "LDH": {
                "idiopathic_pah": ["N/A"],
                "ph_left_heart": [{"min": 50, "max": 100}],
                "ph_lung_disease": ["N/A"]
              },
              "Albumin": {
                "idiopathic_pah": ["N/A"],
                "ph_left_heart": [{"min": 1.5, "max": 3.0}],
                "ph_lung_disease": ["N/A"]
              }
            }
          }
        }
      }
    }
    
    def __init__(self):
        self.random = random
        
        # 1. SCENARIO SELECTION
        # idiopathic_pah (5%), ph_left_heart (75%), ph_lung_disease (20%)
        self.scenario = self.random.choices(
            ["idiopathic_pah", "ph_left_heart", "ph_lung_disease"], 
            weights=[20, 0, 80], k=1
        )[0]

    # --- Helper to extract data from DATA_SOURCE ---
    def _get_val(self, category, system, key, subkey=None, subsubkey=None):
        """
        Extracts data for the current scenario from DATA_SOURCE.
        Handles:
        1. Lists of strings (Choice)
        2. Lists of dicts (Ranges)
        3. Single strings ("N/A", "Elevated")
        """
        try:
            node = self.DATA_SOURCE[category][system][key]
            if subkey:
                node = node[subkey]
            if subsubkey:
                node = node[subsubkey]
                
            scenario_data = node[self.scenario]
            
            # Simple String (e.g., "N/A" or "Elevated")
            if isinstance(scenario_data, str):
                return scenario_data

            # List Handling
            if isinstance(scenario_data, list):
                if not scenario_data:
                    return "N/A"
                
                first_item = scenario_data[0]
                
                # Range Logic: [{"min": x, "max": y}]
                if isinstance(first_item, dict) and "min" in first_item:
                    # Special case for BP which might have 2 ranges [Sys, Dia] or just one
                    if len(scenario_data) > 1 and "min" in scenario_data[1]:
                        # Return list of generated values
                        results = []
                        for r in scenario_data:
                            val = self.random.uniform(r["min"], r["max"])
                            if isinstance(r["min"], int) and isinstance(r["max"], int):
                                results.append(int(val))
                            else:
                                results.append(round(val, 1))
                        return results
                    else:
                        # Single range
                        r = scenario_data[0]
                        val = self.random.uniform(r["min"], r["max"])
                        if isinstance(r["min"], int) and isinstance(r["max"], int):
                            return int(val)
                        return round(val, 1)

                # String Choice Logic: ["A", "B"]
                elif isinstance(first_item, str):
                    return self.random.choice(scenario_data)

            return str(scenario_data)

        except Exception as e:
            return f"Error ({key}): {str(e)}"

    # --- Demographic Helpers ---
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

    # ==========================================
    # 1. PHYSICAL EXAM GENERATION
    # ==========================================
    def _gen_vitals(self):
        cat = "physical_exam"
        sys = "vital_signs"
        
        bp_raw = self._get_val(cat, sys, "BP") # [Sys, Dia]
        temp = self._get_val(cat, sys, "T")
        pr = self._get_val(cat, sys, "PR")
        rr = self._get_val(cat, sys, "RR")
        spo2 = self._get_val(cat, sys, "SpO2")
        gcs = self._get_val(cat, sys, "GCS")
        
        if isinstance(bp_raw, list) and len(bp_raw) == 2:
            bp_str = f"{bp_raw[0]}/{bp_raw[1]} mmHg"
        else:
            bp_str = str(bp_raw)

        return {
            "BP": bp_str,
            "T": f"{temp} °C",
            "PR": f"{pr} bpm",
            "RR": f"{rr} breaths/min",
            "SpO2": f"{spo2}% (Room Air)",
            "GCS": str(gcs)
        }

    def _gen_general_appearance(self):
        cat = "physical_exam"
        sys = "general_appearance"
        
        return {
            "mood_and_behavior": self._get_val(cat, sys, "mood_and_behavior"),
            "overall_appearance": self._get_val(cat, sys, "overall_appearance"),
            "posture_and_position": self._get_val(cat, sys, "posture_and_position"),
            "level_of_consciousness": self._get_val(cat, sys, "level_of_consciousness"),
            "cardiopulmonary_and_circulatory_clues": {
                "edema": self._get_val(cat, sys, "cardiopulmonary_and_circulatory_clues", "edema"),
                "dyspnea": self._get_val(cat, sys, "cardiopulmonary_and_circulatory_clues", "dyspnea"),
                "cyanosis": self._get_val(cat, sys, "cardiopulmonary_and_circulatory_clues", "cyanosis")
            }
        }

    def _gen_head_neck(self):
        cat = "physical_exam"
        sys = "head_and_neck"
        
        return {
            "head_and_face": {
                "symmetry_and_lesions": self._get_val(cat, sys, "head_and_face", "symmetry_and_lesions"),
                "tenderness": self._get_val(cat, sys, "head_and_face", "tenderness")
            },
            "eyes": {
                "sclera_and_conjunctiva": self._get_val(cat, sys, "eyes", "sclera_and_conjunctiva"),
                "pupils_reaction": self._get_val(cat, sys, "eyes", "pupils_reaction"),
                "extraocular_movements": self._get_val(cat, sys, "eyes", "extraocular_movements")
            },
            "ears": {
                "external_and_tenderness": self._get_val(cat, sys, "ears", "external_and_tenderness"),
                "eardrum_appearance": self._get_val(cat, sys, "ears", "eardrum_appearance")
            },
            "nose_and_sinuses": {
                "septum_and_discharge": self._get_val(cat, sys, "nose_and_sinuses", "septum_and_discharge"),
                "sinus_tenderness": self._get_val(cat, sys, "nose_and_sinuses", "sinus_tenderness")
            },
            "mouth_and_pharynx": {
                "oral_mucosa_and_lesions": self._get_val(cat, sys, "mouth_and_pharynx", "oral_mucosa_and_lesions"),
                "pharynx_and_tonsils": self._get_val(cat, sys, "mouth_and_pharynx", "pharynx_and_tonsils")
            },
            "neck_and_lymphatics": {
                "inspection": self._get_val(cat, sys, "neck_and_lymphatics", "inspection"),
                "tracheal_position": self._get_val(cat, sys, "neck_and_lymphatics", "tracheal_position"),
                "thyroid_gland": self._get_val(cat, sys, "neck_and_lymphatics", "thyroid_gland"),
                "carotid_bruit": self._get_val(cat, sys, "neck_and_lymphatics", "carotid_bruit"),
                "lymph_nodes_size_consistency": self._get_val(cat, sys, "neck_and_lymphatics", "lymph_nodes_size_consistency"),
                "lymph_nodes_mobility_tenderness": self._get_val(cat, sys, "neck_and_lymphatics", "lymph_nodes_mobility_tenderness")
            }
        }

    def _gen_respiratory(self):
        cat = "physical_exam"
        sys = "respiratory_system"
        
        return {
            "inspection": {
                "accessory_muscles": self._get_val(cat, sys, "inspection", "accessory_muscles"),
                "chest_shape_and_symmetry": self._get_val(cat, sys, "inspection", "chest_shape_and_symmetry")
            },
            "palpation": {
                "chest_expansion": self._get_val(cat, sys, "palpation", "chest_expansion"),
                "tactile_fremitus": self._get_val(cat, sys, "palpation", "tactile_fremitus")
            },
            "percussion": self._get_val(cat, sys, "percussion"),
            "auscultation": {
                "breath_sounds_intensity": self._get_val(cat, sys, "auscultation", "breath_sounds_intensity"),
                "adventitious_sounds": self._get_val(cat, sys, "auscultation", "adventitious_sounds")
            }
        }

    def _gen_cardio(self):
        cat = "physical_exam"
        sys = "cardiovascular_system"
        
        return {
            "JVP_assessment": self._get_val(cat, sys, "JVP_assessment"),
            "palpation": {
                "precordial_palpation_heave_thrill": self._get_val(cat, sys, "palpation", "precordial_palpation_heave_thrill"),
                "pmi_assessment": self._get_val(cat, sys, "palpation", "pmi_assessment")
            },
            "auscultation": {
                "heart_sounds_s1_s2": self._get_val(cat, sys, "auscultation", "heart_sounds_s1_s2"),
                "extra_sounds_s3_s4_murmurs": self._get_val(cat, sys, "auscultation", "extra_sounds_s3_s4_murmurs")
            },
            "peripheral_pulses_and_extremities": {
                "peripheral_pulses_symmetry_and_quality": self._get_val(cat, sys, "2_pulses_and_extremities", "peripheral_pulses_symmetry_and_quality"),
                "extremities_color_and_trophic_changes": self._get_val(cat, sys, "2_pulses_and_extremities", "extremities_color_and_trophic_changes"),
                "extremities_temperature_and_cap_refill": self._get_val(cat, sys, "2_pulses_and_extremities", "extremities_temperature_and_cap_refill"),
                "extremities_edema": self._get_val(cat, sys, "2_pulses_and_extremities", "extremities_edema")
            }
        }

    def _gen_abdominal(self):
        cat = "physical_exam"
        sys = "abdominal_system"
        
        return {
            "inspection": self._get_val(cat, sys, "inspection"),
            "auscultation": {
                "bowel_sounds": self._get_val(cat, sys, "auscultation", "bowel_sounds"),
                "vascular_bruits": self._get_val(cat, sys, "auscultation", "vascular_bruits")
            },
            "percussion": {
                "general": self._get_val(cat, sys, "percussion", "general"),
                "organ_borders": self._get_val(cat, sys, "percussion", "organ_borders")
            },
            "palpation": {
                "superficial_tenderness": self._get_val(cat, sys, "palpation", "superficial_tenderness"),
                "deep_masses_and_organs": self._get_val(cat, sys, "palpation", "deep_masses_and_organs")
            },
            "peritoneal_signs": self._get_val(cat, sys, "peritoneal_signs")
        }

    def _gen_neuro(self):
        cat = "physical_exam"
        sys = "neurological"
        
        return {
            "mental_status_and_LOC": self._get_val(cat, sys, "mental_status_and_LOC"),
            "cranial_nerves": self._get_val(cat, sys, "cranial_nerves"),
            "motor_strength_and_tone": self._get_val(cat, sys, "motor_strength_and_tone"),
            "involuntary_movements": self._get_val(cat, sys, "involuntary_movements"),
            "sensory_light_touch_and_pain": self._get_val(cat, sys, "sensory_light_touch_and_pain"),
            "deep_tendon_reflexes": self._get_val(cat, sys, "deep_tendon_reflexes"),
            "coordination_and_gait": self._get_val(cat, sys, "coordination_and_gait")
        }

    def _gen_msk(self):
        cat = "physical_exam"
        sys = "musculoskeletal_system"
        
        return {
            "inspection": {
                "joints": self._get_val(cat, sys, "inspection", "joints"),
                "muscles": self._get_val(cat, sys, "inspection", "muscles")
            },
            "palpation": {
                "tenderness_and_crepitus": self._get_val(cat, sys, "palpation", "tenderness_and_crepitus")
            },
            "range_of_motion_active_passive": self._get_val(cat, sys, "range_of_motion_active_passive"),
            "stability_and_function": self._get_val(cat, sys, "stability_and_function")
        }

    # ==========================================
    # 2. PARACLINIC GENERATION
    # ==========================================
    def _gen_paraclinic(self):
        cat = "paraclinic"
        
        # --- Basic Blood Tests ---
        sys = "basic_blood_tests"
        
        na = self._get_val(cat, sys, "BMP", "Na")
        bun = self._get_val(cat, sys, "BMP", "BUN")
        cr = self._get_val(cat, sys, "BMP", "Cr")
        
        wbc = self._get_val(cat, sys, "CBC", "WBC")
        hb = self._get_val(cat, sys, "CBC", "Hb")
        plt = self._get_val(cat, sys, "CBC", "Plt")
        
        esr = self._get_val(cat, sys, "ESR")
        crp = self._get_val(cat, sys, "CRP")
        
        ph = self._get_val(cat, sys, "VBG", "pH")
        pco2 = self._get_val(cat, sys, "VBG", "PCO2")
        hco3 = self._get_val(cat, sys, "VBG", "HCO3")
        
        alt = self._get_val(cat, sys, "LFTs", "ALT")
        ast = self._get_val(cat, sys, "LFTs", "AST")
        
        # --- Specialized Lung Tests ---
        sys = "specialized_lung_tests"
        d_dimer = self._get_val(cat, sys, "D_dimer")
        afb = self._get_val(cat, sys, "Sputum_AFB")
        bnp = self._get_val(cat, sys, "BNP_NT_proBNP")
        gram = self._get_val(cat, sys, "Sputum_analysis", "Gram_Stain")
        quality = self._get_val(cat, sys, "Sputum_analysis", "Sample_Quality")
        a1 = self._get_val(cat, sys, "a1_antitrypsin_level")
        
        # --- Immunity ---
        sys = "immunity_and_serology"
        hiv = self._get_val(cat, sys, "HIV_test")
        ana = self._get_val(cat, sys, "Autoimmune_pannel_ANA_ANCA")
        
        # --- Imaging ---
        cxr = self._get_val(cat, "simple_imaging", "Chest_X_Ray", "PA_Lateral_Findings_and_Effusion")
        ct = self._get_val(cat, "advanced_imaging", "Chest_CT_CTPA", "Lung_Parenchyma_and_Pleura")
        
        # --- Functional ---
        sys = "functional_tests"
        dlco = self._get_val(cat, sys, "dlco")
        peak_flow = self._get_val(cat, sys, "peak_flow")
        pleth = self._get_val(cat, sys, "plethysmography")
        
        # Spirometry Calculation
        P_FEV1 = 3.50
        P_FVC = 4.00
        
        fev1_pct = self._get_val(cat, sys, "Spirometry", "Result", "FEV1")
        fvc_pct = self._get_val(cat, sys, "Spirometry", "Result", "FVC")
        ratio_pct = self._get_val(cat, sys, "Spirometry", "Result", "FEV1/FVC")
        reversibility = self._get_val(cat, sys, "Spirometry", "reversibility")
        
        if isinstance(fev1_pct, (int, float)):
             fev1_meas = round(P_FEV1 * (fev1_pct / 100), 2)
             fev1_out = f"Measured: {fev1_meas} L, Predicted: {P_FEV1} L, %Predicted: {fev1_pct}%"
        else:
             fev1_out = str(fev1_pct)
             
        if isinstance(fvc_pct, (int, float)):
             fvc_meas = round(P_FVC * (fvc_pct / 100), 2)
             fvc_out = f"Measured: {fvc_meas} L, Predicted: {P_FVC} L, %Predicted: {fvc_pct}%"
        else:
             fvc_out = str(fvc_pct)
             
        if isinstance(ratio_pct, (int, float)):
             ratio_meas = round(ratio_pct / 100, 2)
             ratio_out = f"Value: {ratio_meas} ({ratio_pct}%)"
        else:
             ratio_out = str(ratio_pct)

        # --- Procedures (Thoracentesis) ---
        sys = "procedures"
        bronch = self._get_val(cat, sys, "Bronchoscopy")
        
        try:
            serum_prot = self._get_val(cat, sys, "torachonthesis", "Serum", "Protein")
            # If the first value is N/A, assume whole procedure is N/A
            if serum_prot == "N/A":
                thora_result = "Not Indicated"
            else:
                serum_ldh = self._get_val(cat, sys, "torachonthesis", "Serum", "LDH")
                serum_alb = self._get_val(cat, sys, "torachonthesis", "Serum", "Albumin")
                
                fluid_prot = self._get_val(cat, sys, "torachonthesis", "Fluid", "Protein")
                fluid_ldh = self._get_val(cat, sys, "torachonthesis", "Fluid", "LDH")
                fluid_alb = self._get_val(cat, sys, "torachonthesis", "Fluid", "Albumin")
                
                thora_result = {
                    "Serum": {"Protein": f"{serum_prot} g/dL", "LDH": f"{serum_ldh} U/L", "Albumin": f"{serum_alb} g/dL"},
                    "Fluid": {"Protein": f"{fluid_prot} g/dL", "LDH": f"{fluid_ldh} U/L", "Albumin": f"{fluid_alb} g/dL"}
                }
        except Exception:
            thora_result = "N/A"

        return {
            "basic_blood_tests": {
                "CBC": {
                    "Hb": f"{hb} g/dL",
                    "WBC": f"{wbc} /µL",
                    "Plt": f"{plt} /µL"
                },
                "ESR": f"{esr} mm/h",
                "CRP": f"{crp} mg/L",
                "BMP": {
                    "Na": f"{na} mEq/L",
                    "BUN": f"{bun} mg/dL",
                    "Cr": f"{cr} mg/dL"
                },
                "LFTs": {
                    "ALT": f"{alt} U/L",
                    "AST": f"{ast} U/L"
                },
                "VBG": {
                    "pH": f"{ph}",
                    "PCO2": f"{pco2} mmHg",
                    "HCO3": f"{hco3} mEq/L"
                }
            },
            "specialized_lung_tests": {
                "Sputum_analysis": {
                    "Gram_Stain": gram,
                    "Sample_Quality": quality
                },
                "Sputum_AFB": afb,
                "a1_antitrypsin_level": a1,
                "D_dimer": d_dimer,
                "BNP_NT_proBNP": bnp
            },
            "immunity_and_serology": {
                "HIV_test": hiv,
                "Autoimmune_pannel_ANA_ANCA": ana
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
                    "result": {
                        "FEV1": fev1_out,
                        "FVC": fvc_out,
                        "FEV1/FVC_Ratio": ratio_out
                    },
                    "reversibility": reversibility
                },
                "dlco": dlco,
                "peak_flow": peak_flow,
                "plethysmography": pleth
            },
            "procedures": {
                "Bronchoscopy": bronch,
                "torachonthesis": thora_result
            }
        }

    def generate_paraclinic_case(self):
        personal_info = self._generate_personal_information()
        personal_info["Scenario"] = self.scenario
        
        vitals = self._gen_vitals()
        gen_app = self._gen_general_appearance()
        head_neck = self._gen_head_neck()
        respiratory = self._gen_respiratory()
        cardio = self._gen_cardio()
        abdominal = self._gen_abdominal()
        neuro = self._gen_neuro()
        msk = self._gen_msk()
        paraclinic = self._gen_paraclinic()

        data = {
            "patient_profile": {
                "personal_information": personal_info
            },
            "physical_exam": {
                "vital_signs": vitals,
                "general_appearance": gen_app,
                "head_and_neck": head_neck,
                "respiratory_system": respiratory,
                "cardiovascular_system": cardio,
                "abdominal_system": abdominal,
                "neurological": neuro,
                "musculoskeletal_system": msk
            },
            "paraclinic": paraclinic
        }
        
        return data, self.scenario
