import random
import json

class PTEDataGenerator:
    """
    کلاسی برای تولید داده‌های شبیه‌سازی شده PTE (آمبولی ریه) بر اساس فایل PTE (2).txt.
    
    Scenarios:
    1. massive_pte (10%)
    2. peripheral_infarct (65%)
    3. submassive_pte (25%)
    """
    
    # --- داده‌های دموگرافیک (مشابه فایل‌های قبلی) ---
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
            "بازنشسته", "راننده کامیون", "کارمند اداری", "خانه‌دار", "پرستار", 
            "معلم", "کارگر ساختمانی", "مهندس نرم‌افزار", "فروشنده"
        ],
        "famous_cities_sample_30": [
            "تهران", "مشهد", "اصفهان", "شیراز", "تبریز", "اهواز", "کرج", "رشت", "کرمان", "یزد",
            "ساری", "بندرعباس", "کرمانشاه", "ارومیه", "زاهدان", "همدان", "قزوین", "اردبیل", "زنجان", "گرگان"
        ]
    }
    
    # --- داده‌های استخراج شده از PTE (2).txt ---
    DATA_SOURCE = {
      "physical_exam": {
        "vital_signs": {
          "BP": {
            "massive_pte": [{"min": 70, "max": 85}, {"min": 40, "max": 55}],
            "peripheral_infarct": [{"min": 115, "max": 135}, {"min": 70, "max": 85}],
            "submassive_pte": [{"min": 110, "max": 130}, {"min": 70, "max": 80}]
          },
          "T": {
            "massive_pte": [{"min": 36.0, "max": 37.0}],
            "peripheral_infarct": [{"min": 37.2, "max": 37.8}],
            "submassive_pte": [{"min": 36.8, "max": 37.5}]
          },
          "PR": {
            "massive_pte": [{"min": 110, "max": 140}],
            "peripheral_infarct": [{"min": 95, "max": 110}],
            "submassive_pte": [{"min": 100, "max": 125}]
          },
          "RR": {
            "massive_pte": [{"min": 28, "max": 40}],
            "peripheral_infarct": [{"min": 20, "max": 26}],
            "submassive_pte": [{"min": 22, "max": 30}]
          },
          "SpO2": {
            "massive_pte": [{"min": 80, "max": 88}],
            "peripheral_infarct": [{"min": 92, "max": 95}],
            "submassive_pte": [{"min": 88, "max": 92}]
          },
          "GCS": {
            "massive_pte": [{"min": 13, "max": 14}],
            "peripheral_infarct": [{"min": 15, "max": 15}],
            "submassive_pte": [{"min": 15, "max": 15}]
          }
        },
        "general_appearance": {
          "mood_and_behavior": {
            "massive_pte": ["Lethargic or drowsy", "Anxious and restless"],
            "peripheral_infarct": ["Mildly distressed due to pain", "Alert and cooperative"],
            "submassive_pte": ["Anxious and restless", "Alert and cooperative"]
          },
          "overall_appearance": {
            "massive_pte": ["Diaphoretic", "Pale"],
            "peripheral_infarct": ["Well-nourished and well-developed"],
            "submassive_pte": ["Well-nourished and well-developed"]
          },
          "posture_and_position": {
            "massive_pte": ["Unable to lie flat", "Supine with no distress"],
            "peripheral_infarct": ["Splinting to one side"],
            "submassive_pte": ["Sitting upright in tripod position", "Supine with no distress"]
          },
          "level_of_consciousness": {
            "massive_pte": ["Confused or disoriented", "Somnolent but rousable"],
            "peripheral_infarct": ["Alert and oriented x3"],
            "submassive_pte": ["Alert and oriented x3"]
          },
          "cardiopulmonary_and_circulatory_clues": {
            "edema": {
              "massive_pte": ["No edema"],
              "peripheral_infarct": ["Unilateral leg swelling with tenderness", "No edema"],
              "submassive_pte": ["Unilateral leg swelling with tenderness", "No edema"]
            },
            "dyspnea": {
              "massive_pte": ["Dyspnea at rest", "Speaking in short phrases or single words"],
              "peripheral_infarct": ["Dyspnea on exertion", "Speaking in full sentences"],
              "submassive_pte": ["Dyspnea at rest", "Dyspnea on exertion"]
            },
            "cyanosis": {
              "massive_pte": ["Central cyanosis", "Perioral cyanosis"],
              "peripheral_infarct": ["No cyanosis"],
              "submassive_pte": ["No cyanosis", "Peripheral cyanosis"]
            }
          }
        },
        "head_and_neck": {
          "head_and_face": {
            "symmetry_and_lesions": {
              "massive_pte": ["Symmetric with no lesions"],
              "peripheral_infarct": ["Symmetric with no lesions"],
              "submassive_pte": ["Symmetric with no lesions"]
            },
            "tenderness": {
              "massive_pte": ["Non-tender"],
              "peripheral_infarct": ["Non-tender"],
              "submassive_pte": ["Non-tender"]
            }
          },
          "eyes": {
            "sclera_and_conjunctiva": {
              "massive_pte": ["Normal sclera and pink conjunctiva"],
              "peripheral_infarct": ["Normal sclera and pink conjunctiva"],
              "submassive_pte": ["Normal sclera and pink conjunctiva"]
            },
            "pupils_reaction": {
              "massive_pte": ["PERRLA"],
              "peripheral_infarct": ["PERRLA"],
              "submassive_pte": ["PERRLA"]
            },
            "extraocular_movements": {
              "massive_pte": ["Intact"],
              "peripheral_infarct": ["Intact"],
              "submassive_pte": ["Intact"]
            }
          },
          "ears": {
            "external_and_tenderness": {
              "massive_pte": ["Normal external ear, no tenderness"],
              "peripheral_infarct": ["Normal external ear, no tenderness"],
              "submassive_pte": ["Normal external ear, no tenderness"]
            },
            "eardrum_appearance": {
              "massive_pte": ["Intact pearly gray tympanic membrane"],
              "peripheral_infarct": ["Intact pearly gray tympanic membrane"],
              "submassive_pte": ["Intact pearly gray tympanic membrane"]
            }
          },
          "nose_and_sinuses": {
            "septum_and_discharge": {
              "massive_pte": ["Midline septum, no discharge"],
              "peripheral_infarct": ["Midline septum, no discharge"],
              "submassive_pte": ["Midline septum, no discharge"]
            },
            "sinus_tenderness": {
              "massive_pte": ["Non-tender"],
              "peripheral_infarct": ["Non-tender"],
              "submassive_pte": ["Non-tender"]
            }
          },
          "mouth_and_pharynx": {
            "oral_mucosa_and_lesions": {
              "massive_pte": ["Dry mucous membranes", "Central cyanosis under the tongue"],
              "peripheral_infarct": ["Moist and pink"],
              "submassive_pte": ["Moist and pink"]
            },
            "pharynx_and_tonsils": {
              "massive_pte": ["Non-erythematous, no exudates"],
              "peripheral_infarct": ["Non-erythematous, no exudates"],
              "submassive_pte": ["Non-erythematous, no exudates"]
            }
          },
          "neck_and_lymphatics": {
            "inspection": {
              "massive_pte": ["Trachea midline"],
              "peripheral_infarct": ["Trachea midline"],
              "submassive_pte": ["Trachea midline"]
            },
            "tracheal_position": {
              "massive_pte": ["Trachea midline"],
              "peripheral_infarct": ["Trachea midline"],
              "submassive_pte": ["Trachea midline"]
            },
            "thyroid_gland": {
              "massive_pte": ["Non-palpable"],
              "peripheral_infarct": ["Non-palpable"],
              "submassive_pte": ["Non-palpable"]
            },
            "carotid_bruit": {
              "massive_pte": ["No bruits"],
              "peripheral_infarct": ["No bruits"],
              "submassive_pte": ["No bruits"]
            },
            "lymph_nodes_size_consistency": {
              "massive_pte": ["No lymphadenopathy"],
              "peripheral_infarct": ["No lymphadenopathy"],
              "submassive_pte": ["No lymphadenopathy"]
            },
            "lymph_nodes_mobility_tenderness": {
              "massive_pte": ["No lymphadenopathy"],
              "peripheral_infarct": ["No lymphadenopathy"],
              "submassive_pte": ["No lymphadenopathy"]
            }
          }
        },
        "respiratory_system": {
          "inspection": {
            "accessory_muscles": {
              "massive_pte": ["Use of sternocleidomastoid muscles", "Intercostal retractions"],
              "peripheral_infarct": ["No accessory muscle use"],
              "submassive_pte": ["Supraclavicular retractions", "No accessory muscle use"]
            },
            "chest_shape_and_symmetry": {
              "massive_pte": ["Symmetric chest rise"],
              "peripheral_infarct": ["Asymmetric chest expansion", "Symmetric chest rise"],
              "submassive_pte": ["Symmetric chest rise"]
            }
          },
          "palpation": {
            "chest_expansion": {
              "massive_pte": ["Symmetric expansion"],
              "peripheral_infarct": ["Decreased expansion on the right side", "Decreased expansion on the left side"],
              "submassive_pte": ["Symmetric expansion"]
            },
            "tactile_fremitus": {
              "massive_pte": ["Normal tactile fremitus"],
              "peripheral_infarct": ["Decreased tactile fremitus", "Absent tactile fremitus"],
              "submassive_pte": ["Normal tactile fremitus"]
            }
          },
          "percussion": {
            "massive_pte": ["Resonant"],
            "peripheral_infarct": ["Dull", "Stony Dull"],
            "submassive_pte": ["Resonant"]
          },
          "auscultation": {
            "breath_sounds_intensity": {
              "massive_pte": ["Vesicular sounds, normal intensity", "Decreased breath sounds"],
              "peripheral_infarct": ["Decreased breath sounds", "Absent breath sounds at bases"],
              "submassive_pte": ["Vesicular sounds, normal intensity"]
            },
            "adventitious_sounds": {
              "massive_pte": ["No adventitious sounds"],
              "peripheral_infarct": ["Pleural Friction Rub", "No adventitious sounds"],
              "submassive_pte": ["No adventitious sounds", "Fine Crackles"]
            }
          }
        },
        "cardiovascular_system": {
          "JVP_assessment": {
            "massive_pte": ["Distended neck veins", "Elevated JVP"],
            "peripheral_infarct": ["JVP not elevated"],
            "submassive_pte": ["Elevated JVP", "JVP not elevated"]
          },
          "palpation": {
            "precordial_palpation_heave_thrill": {
              "massive_pte": ["Right Ventricular Heave", "Parasternal lift"],
              "peripheral_infarct": ["No heaves or thrills"],
              "submassive_pte": ["Parasternal lift", "No heaves or thrills"]
            },
            "pmi_assessment": {
              "massive_pte": ["PMI strictly unpalpable", "PMI at 5th ICS MCL"],
              "peripheral_infarct": ["PMI at 5th ICS MCL"],
              "submassive_pte": ["PMI at 5th ICS MCL"]
            }
          },
          "auscultation": {
            "heart_sounds_s1_s2": {
              "massive_pte": ["Loud P2", "Fixed split S2"],
              "peripheral_infarct": ["Normal S1, S2"],
              "submassive_pte": ["Loud P2", "Normal S1, S2"]
            },
            "extra_sounds_s3_s4_murmurs": {
              "massive_pte": ["S3 Gallop", "Holosystolic murmur at left lower sternal border"],
              "peripheral_infarct": ["No extra sounds or murmurs"],
              "submassive_pte": ["No extra sounds or murmurs"]
            }
          },
          "2_pulses_and_extremities": {
            "peripheral_pulses_symmetry_and_quality": {
              "massive_pte": ["Weak or thready pulses"],
              "peripheral_infarct": ["Pulses 2+ and symmetric"],
              "submassive_pte": ["Pulses 2+ and symmetric", "Bounding pulses"]
            },
            "extremities_color_and_trophic_changes": {
              "massive_pte": ["No trophic changes"],
              "peripheral_infarct": ["No trophic changes"],
              "submassive_pte": ["No trophic changes"]
            },
            "extremities_temperature_and_cap_refill": {
              "massive_pte": ["Cool extremities, delayed capillary refill"],
              "peripheral_infarct": ["Warm, Capillary refill < 2 sec"],
              "submassive_pte": ["Warm, Capillary refill < 2 sec"]
            },
            "extremities_edema": {
              "massive_pte": ["No edema"],
              "peripheral_infarct": ["Unilateral leg swelling with tenderness", "No edema"],
              "submassive_pte": ["Unilateral leg swelling with tenderness", "No edema"]
            }
          }
        },
        "abdominal_system": {
          "inspection": {
            "massive_pte": ["Flat, non-distended"],
            "peripheral_infarct": ["Flat, non-distended"],
            "submassive_pte": ["Flat, non-distended"]
          },
          "auscultation": {
            "bowel_sounds": {
              "massive_pte": ["Hypoactive bowel sounds"],
              "peripheral_infarct": ["Normoactive bowel sounds"],
              "submassive_pte": ["Normoactive bowel sounds"]
            },
            "vascular_bruits": {
              "massive_pte": ["No bruits"],
              "peripheral_infarct": ["No bruits"],
              "submassive_pte": ["No bruits"]
            }
          },
          "percussion": {
            "general": {
              "massive_pte": ["Resonant"],
              "peripheral_infarct": ["Resonant"],
              "submassive_pte": ["Resonant"]
            },
            "organ_borders": {
              "massive_pte": ["Hepatomegaly", "Normal liver span"],
              "peripheral_infarct": ["Normal liver span"],
              "submassive_pte": ["Normal liver span"]
            }
          },
          "palpation": {
            "superficial_tenderness": {
              "massive_pte": ["Right upper quadrant tenderness", "Soft, non-tender"],
              "peripheral_infarct": ["Soft, non-tender"],
              "submassive_pte": ["Soft, non-tender"]
            },
            "deep_masses_and_organs": {
              "massive_pte": ["Pulsatile liver edge", "No masses or organomegaly"],
              "peripheral_infarct": ["No masses or organomegaly"],
              "submassive_pte": ["No masses or organomegaly"]
            }
          },
          "peritoneal_signs": {
            "massive_pte": ["None"],
            "peripheral_infarct": ["None"],
            "submassive_pte": ["None"]
          }
        },
        "neurological": {
          "mental_status_and_LOC": {
            "massive_pte": ["Confused or disoriented", "Agitated"],
            "peripheral_infarct": ["Alert and Oriented"],
            "submassive_pte": ["Alert and Oriented", "Agitated"]
          },
          "cranial_nerves": {
            "massive_pte": ["Intact"],
            "peripheral_infarct": ["Intact"],
            "submassive_pte": ["Intact"]
          },
          "motor_strength_and_tone": {
            "massive_pte": ["Generalized weakness"],
            "peripheral_infarct": ["5/5 strength globally"],
            "submassive_pte": ["5/5 strength globally"]
          },
          "involuntary_movements": {
            "massive_pte": ["None"],
            "peripheral_infarct": ["None"],
            "submassive_pte": ["None"]
          },
          "sensory_light_touch_and_pain": {
            "massive_pte": ["Intact"],
            "peripheral_infarct": ["Intact"],
            "submassive_pte": ["Intact"]
          },
          "deep_tendon_reflexes": {
            "massive_pte": ["2+"],
            "peripheral_infarct": ["2+"],
            "submassive_pte": ["2+"]
          },
          "coordination_and_gait": {
            "massive_pte": ["N/A"],
            "peripheral_infarct": ["Intact"],
            "submassive_pte": ["Intact"]
          }
        },
        "musculoskeletal_system": {
          "inspection": {
            "joints": {
              "massive_pte": ["Normal joints"],
              "peripheral_infarct": ["Normal joints"],
              "submassive_pte": ["Normal joints"]
            },
            "muscles": {
              "massive_pte": ["Normal bulk"],
              "peripheral_infarct": ["Normal bulk"],
              "submassive_pte": ["Normal bulk"]
            }
          },
          "palpation": {
            "tenderness_and_crepitus": {
              "massive_pte": ["No tenderness"],
              "peripheral_infarct": ["Chest wall tenderness", "Calf tenderness"],
              "submassive_pte": ["Calf tenderness", "No tenderness"]
            }
          },
          "range_of_motion_active_passive": {
            "massive_pte": ["Stable"],
            "peripheral_infarct": ["Stable"],
            "submassive_pte": ["Stable"]
          },
          "stability_and_function": {
            "massive_pte": ["Stable"],
            "peripheral_infarct": ["Stable"],
            "submassive_pte": ["Stable"]
          }
        }
      },
      "paraclinic": {
        "basic_blood_tests": {
          "BMP": {
            "Na": {
              "massive_pte": [{"min": 135, "max": 145}],
              "peripheral_infarct": [{"min": 135, "max": 145}],
              "submassive_pte": [{"min": 135, "max": 145}]
            },
            "BUN": {
              "massive_pte": [{"min": 15, "max": 30}],
              "peripheral_infarct": [{"min": 7, "max": 20}],
              "submassive_pte": [{"min": 7, "max": 20}]
            },
            "Cr": {
              "massive_pte": [{"min": 1.0, "max": 1.5}],
              "peripheral_infarct": [{"min": 0.7, "max": 1.2}],
              "submassive_pte": [{"min": 0.7, "max": 1.2}]
            }
          },
          "CBC": {
            "WBC": {
              "massive_pte": [{"min": 10000, "max": 15000}],
              "peripheral_infarct": [{"min": 6000, "max": 11000}],
              "submassive_pte": [{"min": 5000, "max": 11000}]
            },
            "Hb": {
              "massive_pte": [{"min": 12.0, "max": 16.0}],
              "peripheral_infarct": [{"min": 12.0, "max": 16.0}],
              "submassive_pte": [{"min": 12.0, "max": 16.0}]
            },
            "Plt": {
              "massive_pte": [{"min": 150000, "max": 400000}],
              "peripheral_infarct": [{"min": 150000, "max": 400000}],
              "submassive_pte": [{"min": 150000, "max": 400000}]
            }
          },
          "ESR": {
            "massive_pte": [{"min": 10, "max": 30}],
            "peripheral_infarct": [{"min": 10, "max": 40}],
            "submassive_pte": [{"min": 0, "max": 20}]
          },
          "CRP": {
            "massive_pte": [{"min": 5, "max": 20}],
            "peripheral_infarct": [{"min": 10, "max": 30}],
            "submassive_pte": [{"min": 0, "max": 15}]
          },
          "VBG": {
            "pH": {
              "massive_pte": [{"min": 7.25, "max": 7.35}],
              "peripheral_infarct": [{"min": 7.38, "max": 7.45}],
              "submassive_pte": [{"min": 7.45, "max": 7.50}]
            },
            "PCO2": {
              "massive_pte": [{"min": 25, "max": 35}],
              "peripheral_infarct": [{"min": 35, "max": 40}],
              "submassive_pte": [{"min": 30, "max": 35}]
            },
            "HCO3": {
              "massive_pte": [{"min": 18, "max": 22}],
              "peripheral_infarct": [{"min": 22, "max": 26}],
              "submassive_pte": [{"min": 22, "max": 26}]
            }
          },
          "LFTs": {
            "ALT": {
              "massive_pte": [{"min": 40, "max": 100}],
              "peripheral_infarct": [{"min": 10, "max": 40}],
              "submassive_pte": [{"min": 10, "max": 40}]
            },
            "AST": {
              "massive_pte": [{"min": 40, "max": 100}],
              "peripheral_infarct": [{"min": 10, "max": 40}],
              "submassive_pte": [{"min": 10, "max": 40}]
            }
          }
        },
        "specialized_lung_tests": {
          "D_dimer": {
            "massive_pte": ["Elevated"],
            "peripheral_infarct": ["Elevated"],
            "submassive_pte": ["Elevated"]
          },
          "Sputum_AFB": {
            "massive_pte": ["Negative"],
            "peripheral_infarct": ["Negative"],
            "submassive_pte": ["Negative"]
          },
          "BNP_NT_proBNP": {
            "massive_pte": ["Significantly Elevated"],
            "peripheral_infarct": ["Normal"],
            "submassive_pte": ["Elevated"]
          },
          "Sputum_analysis": {
            "Gram_Stain": {
              "massive_pte": ["N/A"],
              "peripheral_infarct": ["N/A"],
              "submassive_pte": ["N/A"]
            },
            "Sample_Quality": {
              "massive_pte": ["N/A"],
              "peripheral_infarct": ["N/A"],
              "submassive_pte": ["N/A"]
            }
          },
          "a1_antitrypsin_level": {
            "massive_pte": ["Normal range"],
            "peripheral_infarct": ["Normal range"],
            "submassive_pte": ["Normal range"]
          }
        },
        "immunity_and_serology": {
          "HIV_test": {
            "massive_pte": ["Negative"],
            "peripheral_infarct": ["Negative"],
            "submassive_pte": ["Negative"]
          },
          "Autoimmune_pannel_ANA_ANCA": {
            "massive_pte": ["Negative"],
            "peripheral_infarct": ["Negative"],
            "submassive_pte": ["Negative"]
          }
        },
        "simple_imaging": {
          "Chest_X_Ray": {
            "PA_Lateral_Findings_and_Effusion": {
              "massive_pte": ["Normal", "Enlarged pulmonary artery"],
              "peripheral_infarct": ["Pleural effusion", "Wedge-shaped opacity"],
              "submassive_pte": ["Normal", "Minor atelectasis"]
            }
          }
        },
        "advanced_imaging": {
          "Chest_CT_CTPA": {
            "Lung_Parenchyma_and_Pleura": {
              "massive_pte": ["Large saddle embolus", "RV strain"],
              "peripheral_infarct": ["Peripheral filling defect", "Small pleural effusion"],
              "submassive_pte": ["Segmental filling defect"]
            }
          }
        },
        "functional_tests": {
          "dlco": {
            "massive_pte": ["N/A"],
            "peripheral_infarct": ["N/A"],
            "submassive_pte": ["N/A"]
          },
          "peak_flow": {
            "massive_pte": ["N/A"],
            "peripheral_infarct": ["N/A"],
            "submassive_pte": ["N/A"]
          },
          "Spirometry": {
            "Result": {
              "FEV1": {
                "massive_pte": ["N/A"],
                "peripheral_infarct": ["N/A"],
                "submassive_pte": ["N/A"]
              },
              "FVC": {
                "massive_pte": ["N/A"],
                "peripheral_infarct": ["N/A"],
                "submassive_pte": ["N/A"]
              },
              "FEV1/FVC": {
                "massive_pte": ["N/A"],
                "peripheral_infarct": ["N/A"],
                "submassive_pte": ["N/A"]
              }
            },
            "reversibility": {
              "massive_pte": ["N/A"],
              "peripheral_infarct": ["N/A"],
              "submassive_pte": ["N/A"]
            }
          },
          "plethysmography": {
            "massive_pte": ["N/A"],
            "peripheral_infarct": ["N/A"],
            "submassive_pte": ["N/A"]
          }
        },
        "procedures": {
          "Bronchoscopy": {
            "massive_pte": ["N/A"],
            "peripheral_infarct": ["N/A"],
            "submassive_pte": ["N/A"]
          },
          "torachonthesis": {
            "Serum": {
              "Protein": {
                "massive_pte": ["N/A"],
                "peripheral_infarct": [{"min": 6.0, "max": 8.0}],
                "submassive_pte": ["N/A"]
              },
              "LDH": {
                "massive_pte": ["N/A"],
                "peripheral_infarct": [{"min": 150, "max": 250}],
                "submassive_pte": ["N/A"]
              },
              "Albumin": {
                "massive_pte": ["N/A"],
                "peripheral_infarct": [{"min": 3.5, "max": 5.0}],
                "submassive_pte": ["N/A"]
              }
            },
            "Fluid": {
              "Protein": {
                "massive_pte": ["N/A"],
                "peripheral_infarct": [{"min": 3.5, "max": 5.0}],
                "submassive_pte": ["N/A"]
              },
              "LDH": {
                "massive_pte": ["N/A"],
                "peripheral_infarct": [{"min": 200, "max": 400}],
                "submassive_pte": ["N/A"]
              },
              "Albumin": {
                "massive_pte": ["N/A"],
                "peripheral_infarct": [{"min": 2.0, "max": 3.0}],
                "submassive_pte": ["N/A"]
              }
            }
          }
        }
      }
    }
    
    def __init__(self):
        self.random = random
        
        # 1. SCENARIO SELECTION
        # massive_pte (10%), peripheral_infarct (65%), submassive_pte (25%)
        self.scenario = self.random.choices(
            ["massive_pte", "peripheral_infarct", "submassive_pte"], 
            weights=[10, 65, 25], k=1
        )[0]

    # --- Helper to extract data from DATA_SOURCE ---
    def _get_val(self, category, system, key, subkey=None, subsubkey=None):
        try:
            node = self.DATA_SOURCE[category][system][key]
            if subkey:
                node = node[subkey]
            if subsubkey:
                node = node[subsubkey]
                
            scenario_data = node[self.scenario]
            
            # Simple String
            if isinstance(scenario_data, str):
                return scenario_data

            # List Handling
            if isinstance(scenario_data, list):
                if not scenario_data:
                    return "N/A"
                
                first_item = scenario_data[0]
                
                # Range Logic: [{"min": x, "max": y}]
                if isinstance(first_item, dict) and "min" in first_item:
                    # Special case for BP which might have 2 ranges [Sys, Dia]
                    if len(scenario_data) > 1 and "min" in scenario_data[1]:
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
        age_num = self.random.randint(30, 80)
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
        
        # Spirometry (Usually N/A for PTE)
        fev1 = self._get_val(cat, sys, "Spirometry", "Result", "FEV1")
        fvc = self._get_val(cat, sys, "Spirometry", "Result", "FVC")
        ratio = self._get_val(cat, sys, "Spirometry", "Result", "FEV1/FVC")
        reversibility = self._get_val(cat, sys, "Spirometry", "reversibility")
        
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
                        "FEV1": fev1,
                        "FVC": fvc,
                        "FEV1/FVC_Ratio": ratio
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
        
        return data

# --- Testing Block ---
if __name__ == "__main__":
    generator = PTEDataGenerator()
    case = generator.generate_paraclinic_case()
    print(json.dumps(case, indent=4, ensure_ascii=False))