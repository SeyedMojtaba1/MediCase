import random
import json

class IPFDataGenerator:
    """
    کلاسی برای تولید داده‌های شبیه‌سازی شده IPF بر اساس فایل IPF (2).txt.
    
    Scenarios:
    1. stable_ipf (85%)
    2. acute_ipf_exacerbation (5%)
    3. rheumatoid_ild (10%)
    """
    
    # --- داده‌های دموگرافیک (حفظ شده از کد قبلی) ---
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
    
    # --- داده‌های استخراج شده از IPF (2).txt ---
    DATA_SOURCE = {
      "physical_exam": {
        "vital_signs": {
          "BP": {
            "stable_ipf": [{"min": 120, "max": 140}, {"min": 75, "max": 90}],
            "acute_ipf_exacerbation": [{"min": 130, "max": 150}, {"min": 85, "max": 100}],
            "rheumatoid_ild": [{"min": 110, "max": 130}, {"min": 70, "max": 85}]
          },
          "T": {
            "stable_ipf": [{"min": 36.5, "max": 37.2}],
            "acute_ipf_exacerbation": [{"min": 37.5, "max": 38.5}],
            "rheumatoid_ild": [{"min": 36.8, "max": 37.5}]
          },
          "PR": {
            "stable_ipf": [{"min": 80, "max": 100}],
            "acute_ipf_exacerbation": [{"min": 100, "max": 125}],
            "rheumatoid_ild": [{"min": 80, "max": 100}]
          },
          "RR": {
            "stable_ipf": [{"min": 20, "max": 26}],
            "acute_ipf_exacerbation": [{"min": 28, "max": 40}],
            "rheumatoid_ild": [{"min": 18, "max": 24}]
          },
          "SpO2": {
            "stable_ipf": [{"min": 92, "max": 95}],
            "acute_ipf_exacerbation": [{"min": 80, "max": 88}],
            "rheumatoid_ild": [{"min": 93, "max": 97}]
          },
          "GCS": {
            "stable_ipf": [{"min": 15, "max": 15}],
            "acute_ipf_exacerbation": [{"min": 13, "max": 15}],
            "rheumatoid_ild": [{"min": 15, "max": 15}]
          }
        },
        "general_appearance": {
          "mood_and_behavior": {
            "stable_ipf": ["Alert and cooperative"],
            "acute_ipf_exacerbation": ["Anxious and restless", "Lethargic or drowsy"],
            "rheumatoid_ild": ["Calm with no acute distress"]
          },
          "overall_appearance": {
            "stable_ipf": ["Cachectic and thin"],
            "acute_ipf_exacerbation": ["Diaphoretic", "Pale"],
            "rheumatoid_ild": ["Well-nourished and well-developed"]
          },
          "posture_and_position": {
            "stable_ipf": ["Sitting upright in tripod position"],
            "acute_ipf_exacerbation": ["Unable to lie flat"],
            "rheumatoid_ild": ["Supine with no distress"]
          },
          "level_of_consciousness": {
            "stable_ipf": ["Alert and oriented x3"],
            "acute_ipf_exacerbation": ["Confused or disoriented"],
            "rheumatoid_ild": ["Alert and oriented x3"]
          },
          "cardiopulmonary_and_circulatory_clues": {
            "edema": {
              "stable_ipf": ["No edema"],
              "acute_ipf_exacerbation": ["No edema"],
              "rheumatoid_ild": ["No edema"]
            },
            "dyspnea": {
              "stable_ipf": ["Dyspnea on exertion"],
              "acute_ipf_exacerbation": ["Dyspnea at rest", "Speaking in short phrases or single words"],
              "rheumatoid_ild": ["Dyspnea on exertion"]
            },
            "cyanosis": {
              "stable_ipf": ["Peripheral cyanosis", "No cyanosis"],
              "acute_ipf_exacerbation": ["Central cyanosis"],
              "rheumatoid_ild": ["No cyanosis"]
            }
          }
        },
        "head_and_neck": {
          "head_and_face": {
            "symmetry_and_lesions": {
              "stable_ipf": ["Symmetric with no lesions"],
              "acute_ipf_exacerbation": ["Symmetric with no lesions"],
              "rheumatoid_ild": ["Malar rash"]
            },
            "tenderness": {
              "stable_ipf": ["Non-tender"],
              "acute_ipf_exacerbation": ["Non-tender"],
              "rheumatoid_ild": ["Non-tender"]
            }
          },
          "eyes": {
            "sclera_and_conjunctiva": {
              "stable_ipf": ["Normal sclera and pink conjunctiva"],
              "acute_ipf_exacerbation": ["Normal sclera and pink conjunctiva"],
              "rheumatoid_ild": ["Pale conjunctiva"]
            },
            "pupils_reaction": {
              "stable_ipf": ["PERRLA"],
              "acute_ipf_exacerbation": ["PERRLA"],
              "rheumatoid_ild": ["PERRLA"]
            },
            "extraocular_movements": {
              "stable_ipf": ["Intact"],
              "acute_ipf_exacerbation": ["Intact"],
              "rheumatoid_ild": ["Intact"]
            }
          },
          "ears": {
            "external_and_tenderness": {
              "stable_ipf": ["Normal external ear, no tenderness"],
              "acute_ipf_exacerbation": ["Normal external ear, no tenderness"],
              "rheumatoid_ild": ["Normal external ear, no tenderness"]
            },
            "eardrum_appearance": {
              "stable_ipf": ["Intact pearly gray tympanic membrane"],
              "acute_ipf_exacerbation": ["Intact pearly gray tympanic membrane"],
              "rheumatoid_ild": ["Intact pearly gray tympanic membrane"]
            }
          },
          "nose_and_sinuses": {
            "septum_and_discharge": {
              "stable_ipf": ["Midline septum, no discharge"],
              "acute_ipf_exacerbation": ["Midline septum, no discharge"],
              "rheumatoid_ild": ["Midline septum, no discharge"]
            },
            "sinus_tenderness": {
              "stable_ipf": ["Non-tender"],
              "acute_ipf_exacerbation": ["Non-tender"],
              "rheumatoid_ild": ["Non-tender"]
            }
          },
          "mouth_and_pharynx": {
            "oral_mucosa_and_lesions": {
              "stable_ipf": ["Moist and pink"],
              "acute_ipf_exacerbation": ["Central cyanosis under the tongue"],
              "rheumatoid_ild": ["Dry mucous membranes"]
            },
            "pharynx_and_tonsils": {
              "stable_ipf": ["Non-erythematous, no exudates"],
              "acute_ipf_exacerbation": ["Non-erythematous, no exudates"],
              "rheumatoid_ild": ["Non-erythematous, no exudates"]
            }
          },
          "neck_and_lymphatics": {
            "inspection": {
              "stable_ipf": ["Trachea midline"],
              "acute_ipf_exacerbation": ["Trachea midline"],
              "rheumatoid_ild": ["Trachea midline"]
            },
            "tracheal_position": {
              "stable_ipf": ["Trachea midline"],
              "acute_ipf_exacerbation": ["Trachea midline"],
              "rheumatoid_ild": ["Trachea midline"]
            },
            "thyroid_gland": {
              "stable_ipf": ["Non-palpable"],
              "acute_ipf_exacerbation": ["Non-palpable"],
              "rheumatoid_ild": ["Non-palpable"]
            },
            "carotid_bruit": {
              "stable_ipf": ["No bruits"],
              "acute_ipf_exacerbation": ["No bruits"],
              "rheumatoid_ild": ["No bruits"]
            },
            "lymph_nodes_size_consistency": {
              "stable_ipf": ["No lymphadenopathy"],
              "acute_ipf_exacerbation": ["No lymphadenopathy"],
              "rheumatoid_ild": ["No lymphadenopathy"]
            },
            "lymph_nodes_mobility_tenderness": {
              "stable_ipf": ["No lymphadenopathy"],
              "acute_ipf_exacerbation": ["No lymphadenopathy"],
              "rheumatoid_ild": ["No lymphadenopathy"]
            }
          }
        },
        "respiratory_system": {
          "inspection": {
            "accessory_muscles": {
              "stable_ipf": ["No accessory muscle use"],
              "acute_ipf_exacerbation": ["Use of sternocleidomastoid muscles", "Intercostal retractions"],
              "rheumatoid_ild": ["No accessory muscle use"]
            },
            "chest_shape_and_symmetry": {
              "stable_ipf": ["Symmetric chest rise"],
              "acute_ipf_exacerbation": ["Symmetric chest rise"],
              "rheumatoid_ild": ["Symmetric chest rise"]
            }
          },
          "palpation": {
            "chest_expansion": {
              "stable_ipf": ["Symmetric expansion"],
              "acute_ipf_exacerbation": ["Symmetric expansion"],
              "rheumatoid_ild": ["Symmetric expansion"]
            },
            "tactile_fremitus": {
              "stable_ipf": ["Normal tactile fremitus"],
              "acute_ipf_exacerbation": ["Normal tactile fremitus"],
              "rheumatoid_ild": ["Normal tactile fremitus", "Decreased tactile fremitus"]
            }
          },
          "percussion": {
            "stable_ipf": ["Resonant"],
            "acute_ipf_exacerbation": ["Resonant"],
            "rheumatoid_ild": ["Resonant", "Dull"]
          },
          "auscultation": {
            "breath_sounds_intensity": {
              "stable_ipf": ["Vesicular sounds, normal intensity"],
              "acute_ipf_exacerbation": ["Vesicular sounds, normal intensity"],
              "rheumatoid_ild": ["Decreased breath sounds", "Vesicular sounds, normal intensity"]
            },
            "adventitious_sounds": {
              "stable_ipf": ["Velcro Crackles"],
              "acute_ipf_exacerbation": ["Velcro Crackles", "Fine Crackles"],
              "rheumatoid_ild": ["Velcro Crackles", "Pleural Friction Rub"]
            }
          }
        },
        "cardiovascular_system": {
          "JVP_assessment": {
            "stable_ipf": ["JVP not elevated"],
            "acute_ipf_exacerbation": ["JVP not elevated"],
            "rheumatoid_ild": ["JVP not elevated"]
          },
          "palpation": {
            "precordial_palpation_heave_thrill": {
              "stable_ipf": ["No heaves or thrills"],
              "acute_ipf_exacerbation": ["No heaves or thrills"],
              "rheumatoid_ild": ["No heaves or thrills"]
            },
            "pmi_assessment": {
              "stable_ipf": ["PMI at 5th ICS MCL"],
              "acute_ipf_exacerbation": ["PMI at 5th ICS MCL"],
              "rheumatoid_ild": ["PMI at 5th ICS MCL"]
            }
          },
          "auscultation": {
            "heart_sounds_s1_s2": {
              "stable_ipf": ["Normal S1, S2"],
              "acute_ipf_exacerbation": ["Normal S1, S2"],
              "rheumatoid_ild": ["Normal S1, S2"]
            },
            "extra_sounds_s3_s4_murmurs": {
              "stable_ipf": ["No extra sounds or murmurs"],
              "acute_ipf_exacerbation": ["No extra sounds or murmurs"],
              "rheumatoid_ild": ["No extra sounds or murmurs"]
            }
          },
          "2_pulses_and_extremities": {
            "peripheral_pulses_symmetry_and_quality": {
              "stable_ipf": ["Pulses 2+ and symmetric"],
              "acute_ipf_exacerbation": ["Pulses 2+ and symmetric"],
              "rheumatoid_ild": ["Pulses 2+ and symmetric"]
            },
            "extremities_color_and_trophic_changes": {
              "stable_ipf": ["Clubbing of fingers"],
              "acute_ipf_exacerbation": ["Clubbing of fingers"],
              "rheumatoid_ild": ["No trophic changes"]
            },
            "extremities_temperature_and_cap_refill": {
              "stable_ipf": ["Warm extremities"],
              "acute_ipf_exacerbation": ["Warm extremities"],
              "rheumatoid_ild": ["Warm extremities"]
            },
            "extremities_edema": {
              "stable_ipf": ["No edema"],
              "acute_ipf_exacerbation": ["No edema"],
              "rheumatoid_ild": ["No edema"]
            }
          }
        },
        "abdominal_system": {
          "inspection": {
            "stable_ipf": ["Flat, non-distended"],
            "acute_ipf_exacerbation": ["Flat, non-distended"],
            "rheumatoid_ild": ["Flat, non-distended"]
          },
          "auscultation": {
            "bowel_sounds": {
              "stable_ipf": ["Normoactive bowel sounds"],
              "acute_ipf_exacerbation": ["Normoactive bowel sounds"],
              "rheumatoid_ild": ["Normoactive bowel sounds"]
            },
            "vascular_bruits": {
              "stable_ipf": ["No bruits"],
              "acute_ipf_exacerbation": ["No bruits"],
              "rheumatoid_ild": ["No bruits"]
            }
          },
          "percussion": {
            "general": {
              "stable_ipf": ["Resonant"],
              "acute_ipf_exacerbation": ["Resonant"],
              "rheumatoid_ild": ["Resonant"]
            },
            "organ_borders": {
              "stable_ipf": ["Normal liver span"],
              "acute_ipf_exacerbation": ["Normal liver span"],
              "rheumatoid_ild": ["Normal liver span"]
            }
          },
          "palpation": {
            "superficial_tenderness": {
              "stable_ipf": ["Soft, non-tender"],
              "acute_ipf_exacerbation": ["Soft, non-tender"],
              "rheumatoid_ild": ["Soft, non-tender"]
            },
            "deep_masses_and_organs": {
              "stable_ipf": ["No masses or organomegaly"],
              "acute_ipf_exacerbation": ["No masses or organomegaly"],
              "rheumatoid_ild": ["No masses or organomegaly"]
            }
          },
          "peritoneal_signs": {
            "stable_ipf": ["None"],
            "acute_ipf_exacerbation": ["None"],
            "rheumatoid_ild": ["None"]
          }
        },
        "neurological": {
          "mental_status_and_LOC": {
            "stable_ipf": ["Alert and Oriented"],
            "acute_ipf_exacerbation": ["Confused or disoriented"],
            "rheumatoid_ild": ["Alert and Oriented"]
          },
          "cranial_nerves": {
            "stable_ipf": ["Intact"],
            "acute_ipf_exacerbation": ["Intact"],
            "rheumatoid_ild": ["Intact"]
          },
          "motor_strength_and_tone": {
            "stable_ipf": ["5/5 strength globally"],
            "acute_ipf_exacerbation": ["5/5 strength globally"],
            "rheumatoid_ild": ["5/5 strength globally"]
          },
          "involuntary_movements": {
            "stable_ipf": ["None"],
            "acute_ipf_exacerbation": ["None"],
            "rheumatoid_ild": ["None"]
          },
          "sensory_light_touch_and_pain": {
            "stable_ipf": ["Intact"],
            "acute_ipf_exacerbation": ["Intact"],
            "rheumatoid_ild": ["Intact"]
          },
          "deep_tendon_reflexes": {
            "stable_ipf": ["2+"],
            "acute_ipf_exacerbation": ["2+"],
            "rheumatoid_ild": ["2+"]
          },
          "coordination_and_gait": {
            "stable_ipf": ["Intact"],
            "acute_ipf_exacerbation": ["Intact"],
            "rheumatoid_ild": ["Intact"]
          }
        },
        "musculoskeletal_system": {
          "inspection": {
            "joints": {
              "stable_ipf": ["Normal joints"],
              "acute_ipf_exacerbation": ["Normal joints"],
              "rheumatoid_ild": ["Swollen, tender joints"]
            },
            "muscles": {
              "stable_ipf": ["Normal bulk"],
              "acute_ipf_exacerbation": ["Normal bulk"],
              "rheumatoid_ild": ["Normal bulk"]
            }
          },
          "palpation": {
            "tenderness_and_crepitus": {
              "stable_ipf": ["No tenderness"],
              "acute_ipf_exacerbation": ["No tenderness"],
              "rheumatoid_ild": ["No tenderness"]
            }
          },
          "range_of_motion_active_passive": {
            "stable_ipf": ["Full"],
            "acute_ipf_exacerbation": ["Full"],
            "rheumatoid_ild": ["Full"]
          },
          "stability_and_function": {
            "stable_ipf": ["Stable"],
            "acute_ipf_exacerbation": ["Stable"],
            "rheumatoid_ild": ["Stable"]
          }
        }
      },
      "paraclinic": {
        "basic_blood_tests": {
          "BMP": {
            "Na": {
              "stable_ipf": [{"min": 135, "max": 145}],
              "acute_ipf_exacerbation": [{"min": 135, "max": 145}],
              "rheumatoid_ild": [{"min": 135, "max": 145}]
            },
            "BUN": {
              "stable_ipf": [{"min": 10, "max": 25}],
              "acute_ipf_exacerbation": [{"min": 15, "max": 30}],
              "rheumatoid_ild": [{"min": 10, "max": 25}]
            },
            "Cr": {
              "stable_ipf": [{"min": 0.7, "max": 1.1}],
              "acute_ipf_exacerbation": [{"min": 0.8, "max": 1.3}],
              "rheumatoid_ild": [{"min": 0.7, "max": 1.1}]
            }
          },
          "CBC": {
            "WBC": {
              "stable_ipf": [{"min": 4500, "max": 10000}],
              "acute_ipf_exacerbation": [{"min": 10000, "max": 18000}],
              "rheumatoid_ild": [{"min": 4500, "max": 11000}]
            },
            "Hb": {
              "stable_ipf": [{"min": 13.0, "max": 16.0}],
              "acute_ipf_exacerbation": [{"min": 13.0, "max": 16.0}],
              "rheumatoid_ild": [{"min": 10.0, "max": 13.0}]
            },
            "Plt": {
              "stable_ipf": [{"min": 150000, "max": 400000}],
              "acute_ipf_exacerbation": [{"min": 150000, "max": 400000}],
              "rheumatoid_ild": [{"min": 150000, "max": 400000}]
            }
          },
          "ESR": {
            "stable_ipf": [{"min": 10, "max": 40}],
            "acute_ipf_exacerbation": [{"min": 30, "max": 80}],
            "rheumatoid_ild": [{"min": 50, "max": 100}]
          },
          "CRP": {
            "stable_ipf": [{"min": 0, "max": 10}],
            "acute_ipf_exacerbation": [{"min": 50, "max": 150}],
            "rheumatoid_ild": [{"min": 20, "max": 80}]
          },
          "VBG": {
            "pH": {
              "stable_ipf": [{"min": 7.35, "max": 7.45}],
              "acute_ipf_exacerbation": [{"min": 7.30, "max": 7.40}],
              "rheumatoid_ild": [{"min": 7.35, "max": 7.45}]
            },
            "PCO2": {
              "stable_ipf": [{"min": 35, "max": 45}],
              "acute_ipf_exacerbation": [{"min": 35, "max": 50}],
              "rheumatoid_ild": [{"min": 35, "max": 45}]
            },
            "HCO3": {
              "stable_ipf": [{"min": 22, "max": 26}],
              "acute_ipf_exacerbation": [{"min": 22, "max": 28}],
              "rheumatoid_ild": [{"min": 22, "max": 26}]
            }
          },
          "LFTs": {
            "ALT": {
              "stable_ipf": [{"min": 10, "max": 40}],
              "acute_ipf_exacerbation": [{"min": 10, "max": 40}],
              "rheumatoid_ild": [{"min": 10, "max": 40}]
            },
            "AST": {
              "stable_ipf": [{"min": 10, "max": 40}],
              "acute_ipf_exacerbation": [{"min": 10, "max": 40}],
              "rheumatoid_ild": [{"min": 10, "max": 40}]
            }
          }
        },
        "specialized_lung_tests": {
          "D_dimer": {
            "stable_ipf": ["Negative"],
            "acute_ipf_exacerbation": ["Negative"],
            "rheumatoid_ild": ["Negative"]
          },
          "Sputum_AFB": {
            "stable_ipf": ["Negative"],
            "acute_ipf_exacerbation": ["Negative"],
            "rheumatoid_ild": ["Negative"]
          },
          "BNP_NT_proBNP": {
            "stable_ipf": ["Normal"],
            "acute_ipf_exacerbation": ["Normal"],
            "rheumatoid_ild": ["Normal"]
          },
          "Sputum_analysis": {
            "Gram_Stain": {
              "stable_ipf": ["Normal flora"],
              "acute_ipf_exacerbation": ["Normal flora"],
              "rheumatoid_ild": ["Normal flora"]
            },
            "Sample_Quality": {
              "stable_ipf": ["Adequate"],
              "acute_ipf_exacerbation": ["Adequate"],
              "rheumatoid_ild": ["Adequate"]
            }
          },
          "a1_antitrypsin_level": {
            "stable_ipf": ["Normal range"],
            "acute_ipf_exacerbation": ["Normal range"],
            "rheumatoid_ild": ["Normal range"]
          }
        },
        "immunity_and_serology": {
          "HIV_test": {
            "stable_ipf": ["Negative"],
            "acute_ipf_exacerbation": ["Negative"],
            "rheumatoid_ild": ["Negative"]
          },
          "Autoimmune_pannel_ANA_ANCA": {
            "stable_ipf": ["Negative"],
            "acute_ipf_exacerbation": ["Negative"],
            "rheumatoid_ild": ["Positive"]
          }
        },
        "simple_imaging": {
          "Chest_X_Ray": {
            "PA_Lateral_Findings_and_Effusion": {
              "stable_ipf": ["Reticular opacities"],
              "acute_ipf_exacerbation": ["Ground glass opacities", "Reticular opacities"],
              "rheumatoid_ild": ["Pleural effusion", "Reticular opacities"]
            }
          }
        },
        "advanced_imaging": {
          "Chest_CT_CTPA": {
            "Lung_Parenchyma_and_Pleura": {
              "stable_ipf": ["Honeycombing", "Traction bronchiectasis"],
              "acute_ipf_exacerbation": ["New ground glass opacities"],
              "rheumatoid_ild": ["Pleural effusion", "Fibrosis"]
            }
          }
        },
        "functional_tests": {
          "dlco": {
            "stable_ipf": ["Decreased"],
            "acute_ipf_exacerbation": ["Significantly reduced"],
            "rheumatoid_ild": ["Decreased"]
          },
          "peak_flow": {
            "stable_ipf": ["Reduced"],
            "acute_ipf_exacerbation": ["Significantly reduced"],
            "rheumatoid_ild": ["Reduced"]
          },
          "Spirometry": {
            "Result": {
              "FEV1": {
                "stable_ipf": [{"min": 50, "max": 70}],
                "acute_ipf_exacerbation": [{"min": 30, "max": 50}],
                "rheumatoid_ild": [{"min": 50, "max": 70}]
              },
              "FVC": {
                "stable_ipf": [{"min": 50, "max": 70}],
                "acute_ipf_exacerbation": [{"min": 30, "max": 50}],
                "rheumatoid_ild": [{"min": 50, "max": 70}]
              },
              "FEV1/FVC": {
                "stable_ipf": [{"min": 80, "max": 95}],
                "acute_ipf_exacerbation": [{"min": 80, "max": 95}],
                "rheumatoid_ild": [{"min": 80, "max": 95}]
              }
            },
            "reversibility": {
              "stable_ipf": ["No significant reversibility"],
              "acute_ipf_exacerbation": ["No significant reversibility"],
              "rheumatoid_ild": ["No significant reversibility"]
            }
          },
          "plethysmography": {
            "stable_ipf": ["Decreased TLC"],
            "acute_ipf_exacerbation": ["Decreased TLC"],
            "rheumatoid_ild": ["Decreased TLC"]
          }
        },
        "procedures": {
          "Bronchoscopy": {
            "stable_ipf": ["N/A"],
            "acute_ipf_exacerbation": ["N/A"],
            "rheumatoid_ild": ["N/A"]
          },
          "torachonthesis": {
            "Serum": {
              "Protein": {
                "stable_ipf": ["N/A"],
                "acute_ipf_exacerbation": ["N/A"],
                "rheumatoid_ild": [{"min": 6.0, "max": 8.0}]
              },
              "LDH": {
                "stable_ipf": ["N/A"],
                "acute_ipf_exacerbation": ["N/A"],
                "rheumatoid_ild": [{"min": 140, "max": 200}]
              },
              "Albumin": {
                "stable_ipf": ["N/A"],
                "acute_ipf_exacerbation": ["N/A"],
                "rheumatoid_ild": [{"min": 3.5, "max": 5.0}]
              }
            },
            "Fluid": {
              "Protein": {
                "stable_ipf": ["N/A"],
                "acute_ipf_exacerbation": ["N/A"],
                "rheumatoid_ild": [{"min": 3.5, "max": 5.5}]
              },
              "LDH": {
                "stable_ipf": ["N/A"],
                "acute_ipf_exacerbation": ["N/A"],
                "rheumatoid_ild": [{"min": 500, "max": 1500}]
              },
              "Albumin": {
                "stable_ipf": ["N/A"],
                "acute_ipf_exacerbation": ["N/A"],
                "rheumatoid_ild": [{"min": 2.0, "max": 3.0}]
              }
            }
          }
        }
      }
    }
    
    def __init__(self):
        self.random = random
        
        # 1. SCENARIO SELECTION
        # stable_ipf (85%), acute_ipf_exacerbation (5%), rheumatoid_ild (10%)
        self.scenario = self.random.choices(
            ["stable_ipf", "acute_ipf_exacerbation", "rheumatoid_ild"], 
            weights=[85, 5, 10], k=1
        )[0]

    # --- Helper to extract data from DATA_SOURCE ---
    def _get_val(self, category, system, key, subkey=None, subsubkey=None):
        """
        Extracts data for the current scenario from DATA_SOURCE.
        Handles:
        1. Lists of strings (Choice)
        2. Lists of dicts (Ranges)
        3. Single strings ("N/A")
        """
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
        age_num = self.random.randint(55, 85) # IPF usually older
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
             # Ratio usually expressed as percentage (e.g., 80) but can be fraction (0.8)
             # The source gives 80-95 etc, so these are percentages.
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
        
        return data

# --- Testing Block ---
if __name__ == "__main__":
    generator = IPFDataGenerator()
    case = generator.generate_paraclinic_case()
    print(json.dumps(case, indent=4, ensure_ascii=False))