import random
import json

class COPDDataGenerator:
    """
    کلاسی برای تولید داده‌های شبیه‌سازی شده COPD بر اساس فایل COPD.txt.
    
    Scenarios:
    1. chronic_bronchitis (40%)
    2. emphysema (30%)
    3. copd_cor_pulmonale (30%)
    """
    
    # --- داده‌های دموگرافیک (حفظ شده از کد قبلی) ---
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
    
    # --- داده‌های استخراج شده از COPD.txt ---
    DATA_SOURCE = {
      "physical_exam": {
        "vital_signs": {
          "BP": {
            "chronic_bronchitis": [{"min": 130, "max": 150}, {"min": 80, "max": 95}],
            "emphysema": [{"min": 110, "max": 130}, {"min": 70, "max": 85}],
            "copd_cor_pulmonale": [{"min": 100, "max": 130}, {"min": 60, "max": 85}]
          },
          "T": {
            "chronic_bronchitis": [{"min": 36.5, "max": 37.2}],
            "emphysema": [{"min": 36.5, "max": 37.2}],
            "copd_cor_pulmonale": [{"min": 36.5, "max": 37.2}]
          },
          "PR": {
            "chronic_bronchitis": [{"min": 80, "max": 100}],
            "emphysema": [{"min": 85, "max": 105}],
            "copd_cor_pulmonale": [{"min": 90, "max": 110}]
          },
          "RR": {
            "chronic_bronchitis": [{"min": 18, "max": 24}],
            "emphysema": [{"min": 20, "max": 28}],
            "copd_cor_pulmonale": [{"min": 22, "max": 30}]
          },
          "SpO2": {
            "chronic_bronchitis": [{"min": 85, "max": 92}],
            "emphysema": [{"min": 90, "max": 95}],
            "copd_cor_pulmonale": [{"min": 84, "max": 90}]
          },
          "GCS": {
            "chronic_bronchitis": [{"min": 14, "max": 15}],
            "emphysema": [{"min": 15, "max": 15}],
            "copd_cor_pulmonale": [{"min": 13, "max": 15}]
          }
        },
        "general_appearance": {
          "mood_and_behavior": {
            "chronic_bronchitis": ["Lethargic or drowsy", "Calm with no acute distress"],
            "emphysema": ["Anxious and restless"],
            "copd_cor_pulmonale": ["Lethargic or drowsy", "Irritable"]
          },
          "overall_appearance": {
            "chronic_bronchitis": ["Obese or overweight", "Plethoric or ruddy complexion"],
            "emphysema": ["Cachectic and thin"],
            "copd_cor_pulmonale": ["Obese or overweight", "Plethoric or ruddy complexion"]
          },
          "posture_and_position": {
            "chronic_bronchitis": ["Supine with no distress"],
            "emphysema": ["Sitting upright in tripod position", "Leaning forward"],
            "copd_cor_pulmonale": ["Orthopnea", "Unable to lie flat"]
          },
          "level_of_consciousness": {
            "chronic_bronchitis": ["Somnolent but rousable", "Alert and oriented x3"],
            "emphysema": ["Alert and oriented x3"],
            "copd_cor_pulmonale": ["Confused or disoriented", "Somnolent but rousable"]
          },
          "cardiopulmonary_and_circulatory_clues": {
            "edema": {
              "chronic_bronchitis": ["Trace pedal edema", "No edema"],
              "emphysema": ["No edema"],
              "copd_cor_pulmonale": ["Pitting edema in lower extremities", "Generalized edema"]
            },
            "dyspnea": {
              "chronic_bronchitis": ["Dyspnea on exertion", "Dyspnea at rest"],
              "emphysema": ["Pursed-lip breathing", "Dyspnea at rest"],
              "copd_cor_pulmonale": ["Dyspnea at rest", "Dyspnea on exertion"]
            },
            "cyanosis": {
              "chronic_bronchitis": ["Central cyanosis", "Peripheral cyanosis"],
              "emphysema": ["No cyanosis"],
              "copd_cor_pulmonale": ["Central cyanosis"]
            }
          }
        },
        "head_and_neck": {
          "head_and_face": {
            "symmetry_and_lesions": {
              "chronic_bronchitis": ["Facial flushing"],
              "emphysema": ["Symmetric with no lesions"],
              "copd_cor_pulmonale": ["Facial flushing", "Symmetric with no lesions"]
            },
            "tenderness": {
              "chronic_bronchitis": ["Non-tender"],
              "emphysema": ["Non-tender"],
              "copd_cor_pulmonale": ["Non-tender"]
            }
          },
          "eyes": {
            "sclera_and_conjunctiva": {
              "chronic_bronchitis": ["Injected or red conjunctiva"],
              "emphysema": ["Normal sclera and pink conjunctiva"],
              "copd_cor_pulmonale": ["Injected or red conjunctiva"]
            },
            "pupils_reaction": {
              "chronic_bronchitis": ["PERRLA"],
              "emphysema": ["PERRLA"],
              "copd_cor_pulmonale": ["PERRLA"]
            },
            "extraocular_movements": {
              "chronic_bronchitis": ["Intact"],
              "emphysema": ["Intact"],
              "copd_cor_pulmonale": ["Intact"]
            }
          },
          "ears": {
            "external_and_tenderness": {
              "chronic_bronchitis": ["Normal external ear, no tenderness"],
              "emphysema": ["Normal external ear, no tenderness"],
              "copd_cor_pulmonale": ["Normal external ear, no tenderness"]
            },
            "eardrum_appearance": {
              "chronic_bronchitis": ["Intact pearly gray tympanic membrane"],
              "emphysema": ["Intact pearly gray tympanic membrane"],
              "copd_cor_pulmonale": ["Intact pearly gray tympanic membrane"]
            }
          },
          "nose_and_sinuses": {
            "septum_and_discharge": {
              "chronic_bronchitis": ["Midline septum, no discharge"],
              "emphysema": ["Midline septum, no discharge"],
              "copd_cor_pulmonale": ["Midline septum, no discharge"]
            },
            "sinus_tenderness": {
              "chronic_bronchitis": ["Non-tender"],
              "emphysema": ["Non-tender"],
              "copd_cor_pulmonale": ["Non-tender"]
            }
          },
          "mouth_and_pharynx": {
            "oral_mucosa_and_lesions": {
              "chronic_bronchitis": ["Central cyanosis under the tongue"],
              "emphysema": ["Moist and pink"],
              "copd_cor_pulmonale": ["Central cyanosis under the tongue"]
            },
            "pharynx_and_tonsils": {
              "chronic_bronchitis": ["Non-erythematous, no exudates"],
              "emphysema": ["Non-erythematous, no exudates"],
              "copd_cor_pulmonale": ["Non-erythematous, no exudates"]
            }
          },
          "neck_and_lymphatics": {
            "inspection": {
              "chronic_bronchitis": ["Trachea midline"],
              "emphysema": ["Trachea midline"],
              "copd_cor_pulmonale": ["Trachea midline"]
            },
            "tracheal_position": {
              "chronic_bronchitis": ["Trachea midline"],
              "emphysema": ["Trachea midline"],
              "copd_cor_pulmonale": ["Trachea midline"]
            },
            "thyroid_gland": {
              "chronic_bronchitis": ["Non-palpable"],
              "emphysema": ["Non-palpable"],
              "copd_cor_pulmonale": ["Non-palpable"]
            },
            "carotid_bruit": {
              "chronic_bronchitis": ["No bruits"],
              "emphysema": ["No bruits"],
              "copd_cor_pulmonale": ["No bruits"]
            },
            "lymph_nodes_size_consistency": {
              "chronic_bronchitis": ["No lymphadenopathy"],
              "emphysema": ["No lymphadenopathy"],
              "copd_cor_pulmonale": ["No lymphadenopathy"]
            },
            "lymph_nodes_mobility_tenderness": {
              "chronic_bronchitis": ["No lymphadenopathy"],
              "emphysema": ["No lymphadenopathy"],
              "copd_cor_pulmonale": ["No lymphadenopathy"]
            }
          }
        },
        "respiratory_system": {
          "inspection": {
            "accessory_muscles": {
              "chronic_bronchitis": ["No accessory muscle use"],
              "emphysema": ["Supraclavicular retractions", "Use of sternocleidomastoid muscles"],
              "copd_cor_pulmonale": ["No accessory muscle use", "Intercostal retractions"]
            },
            "chest_shape_and_symmetry": {
              "chronic_bronchitis": ["Symmetric chest rise"],
              "emphysema": ["Barrel chest"],
              "copd_cor_pulmonale": ["Barrel chest", "Symmetric chest rise"]
            }
          },
          "palpation": {
            "chest_expansion": {
              "chronic_bronchitis": ["Symmetric expansion"],
              "emphysema": ["Globally decreased expansion"],
              "copd_cor_pulmonale": ["Globally decreased expansion"]
            },
            "tactile_fremitus": {
              "chronic_bronchitis": ["Normal tactile fremitus"],
              "emphysema": ["Decreased tactile fremitus"],
              "copd_cor_pulmonale": ["Normal tactile fremitus", "Decreased tactile fremitus"]
            }
          },
          "percussion": {
            "chronic_bronchitis": ["Resonant"],
            "emphysema": ["Hyper-resonant"],
            "copd_cor_pulmonale": ["Resonant", "Dull"]
          },
          "auscultation": {
            "breath_sounds_intensity": {
              "chronic_bronchitis": ["Vesicular sounds, normal intensity"],
              "emphysema": ["Decreased breath sounds"],
              "copd_cor_pulmonale": ["Decreased breath sounds"]
            },
            "adventitious_sounds": {
              "chronic_bronchitis": ["Rhonchi", "Coarse Crackles"],
              "emphysema": ["No adventitious sounds", "Wheezing"],
              "copd_cor_pulmonale": ["Rhonchi", "Coarse Crackles"]
            }
          }
        },
        "cardiovascular_system": {
          "JVP_assessment": {
            "chronic_bronchitis": ["JVP not elevated"],
            "emphysema": ["JVP not elevated"],
            "copd_cor_pulmonale": ["Distended neck veins", "Elevated JVP", "Positive Hepatojugular reflux"]
          },
          "palpation": {
            "precordial_palpation_heave_thrill": {
              "chronic_bronchitis": ["No heaves or thrills"],
              "emphysema": ["No heaves or thrills"],
              "copd_cor_pulmonale": ["Right Ventricular Heave", "Parasternal lift"]
            },
            "pmi_assessment": {
              "chronic_bronchitis": ["PMI at 5th ICS MCL"],
              "emphysema": ["PMI strictly unpalpable"],
              "copd_cor_pulmonale": ["PMI displaced laterally"]
            }
          },
          "auscultation": {
            "heart_sounds_s1_s2": {
              "chronic_bronchitis": ["Normal S1, S2"],
              "emphysema": ["Normal S1, S2"],
              "copd_cor_pulmonale": ["Loud P2", "Fixed split S2"]
            },
            "extra_sounds_s3_s4_murmurs": {
              "chronic_bronchitis": ["No extra sounds or murmurs"],
              "emphysema": ["No extra sounds or murmurs"],
              "copd_cor_pulmonale": ["Holosystolic murmur at left lower sternal border", "S3 Gallop"]
            }
          },
          "2_pulses_and_extremities": {
            "peripheral_pulses_symmetry_and_quality": {
              "chronic_bronchitis": ["Pulses 2+ and symmetric"],
              "emphysema": ["Pulses 2+ and symmetric"],
              "copd_cor_pulmonale": ["Bounding pulses"]
            },
            "extremities_color_and_trophic_changes": {
              "chronic_bronchitis": ["Nicotine staining on fingers"],
              "emphysema": ["Nicotine staining on fingers"],
              "copd_cor_pulmonale": ["Clubbing of fingers", "Nicotine staining on fingers"]
            },
            "extremities_temperature_and_cap_refill": {
              "chronic_bronchitis": ["Warm extremities"],
              "emphysema": ["Warm extremities"],
              "copd_cor_pulmonale": ["Warm extremities"]
            },
            "extremities_edema": {
              "chronic_bronchitis": ["No edema"],
              "emphysema": ["No edema"],
              "copd_cor_pulmonale": ["Bilateral pitting edema"]
            }
          }
        },
        "abdominal_system": {
          "inspection": {
            "chronic_bronchitis": ["Distended", "Flat, non-distended"],
            "emphysema": ["Scaphoid"],
            "copd_cor_pulmonale": ["Distended"]
          },
          "auscultation": {
            "bowel_sounds": {
              "chronic_bronchitis": ["Normoactive bowel sounds"],
              "emphysema": ["Normoactive bowel sounds"],
              "copd_cor_pulmonale": ["Normoactive bowel sounds"]
            },
            "vascular_bruits": {
              "chronic_bronchitis": ["No bruits"],
              "emphysema": ["No bruits"],
              "copd_cor_pulmonale": ["No bruits"]
            }
          },
          "percussion": {
            "general": {
              "chronic_bronchitis": ["Resonant"],
              "emphysema": ["Resonant"],
              "copd_cor_pulmonale": ["Resonant"]
            },
            "organ_borders": {
              "chronic_bronchitis": ["Normal liver span"],
              "emphysema": ["Normal liver span"],
              "copd_cor_pulmonale": ["Hepatomegaly"]
            }
          },
          "palpation": {
            "superficial_tenderness": {
              "chronic_bronchitis": ["Soft, non-tender"],
              "emphysema": ["Soft, non-tender"],
              "copd_cor_pulmonale": ["Right upper quadrant tenderness"]
            },
            "deep_masses_and_organs": {
              "chronic_bronchitis": ["No masses or organomegaly"],
              "emphysema": ["No masses or organomegaly"],
              "copd_cor_pulmonale": ["Pulsatile liver edge"]
            }
          },
          "peritoneal_signs": {
            "chronic_bronchitis": ["None"],
            "emphysema": ["None"],
            "copd_cor_pulmonale": ["None"]
          }
        },
        "neurological": {
          "mental_status_and_LOC": {
            "chronic_bronchitis": ["Somnolent but rousable", "Alert and Oriented"],
            "emphysema": ["Alert and Oriented"],
            "copd_cor_pulmonale": ["Mild confusion", "Somnolent but rousable"]
          },
          "cranial_nerves": {
            "chronic_bronchitis": ["Intact"],
            "emphysema": ["Intact"],
            "copd_cor_pulmonale": ["Intact"]
          },
          "motor_strength_and_tone": {
            "chronic_bronchitis": ["5/5 strength globally"],
            "emphysema": ["5/5 strength globally"],
            "copd_cor_pulmonale": ["5/5 strength globally"]
          },
          "involuntary_movements": {
            "chronic_bronchitis": ["Asterixis"],
            "emphysema": ["None"],
            "copd_cor_pulmonale": ["Asterixis", "Flapping tremor"]
          },
          "sensory_light_touch_and_pain": {
            "chronic_bronchitis": ["Intact"],
            "emphysema": ["Intact"],
            "copd_cor_pulmonale": ["Intact"]
          },
          "deep_tendon_reflexes": {
            "chronic_bronchitis": ["2+"],
            "emphysema": ["2+"],
            "copd_cor_pulmonale": ["2+"]
          },
          "coordination_and_gait": {
            "chronic_bronchitis": ["Intact"],
            "emphysema": ["Intact"],
            "copd_cor_pulmonale": ["Intact"]
          }
        },
        "musculoskeletal_system": {
          "inspection": {
            "joints": {
              "chronic_bronchitis": ["Normal joints"],
              "emphysema": ["Normal joints"],
              "copd_cor_pulmonale": ["Normal joints"]
            },
            "muscles": {
              "chronic_bronchitis": ["Normal bulk"],
              "emphysema": ["Muscle wasting"],
              "copd_cor_pulmonale": ["Normal bulk"]
            }
          },
          "palpation": {
            "tenderness_and_crepitus": {
              "chronic_bronchitis": ["No tenderness"],
              "emphysema": ["No tenderness"],
              "copd_cor_pulmonale": ["No tenderness"]
            }
          },
          "range_of_motion_active_passive": {
            "chronic_bronchitis": ["Full"],
            "emphysema": ["Full"],
            "copd_cor_pulmonale": ["Full"]
          },
          "stability_and_function": {
            "chronic_bronchitis": ["Stable"],
            "emphysema": ["Stable"],
            "copd_cor_pulmonale": ["Stable"]
          }
        }
      },
      "paraclinic": {
        "basic_blood_tests": {
          "BMP": {
            "Na": {
              "chronic_bronchitis": [{"min": 135, "max": 145}],
              "emphysema": [{"min": 135, "max": 145}],
              "copd_cor_pulmonale": [{"min": 130, "max": 140}]
            },
            "BUN": {
              "chronic_bronchitis": [{"min": 10, "max": 25}],
              "emphysema": [{"min": 10, "max": 25}],
              "copd_cor_pulmonale": [{"min": 15, "max": 30}]
            },
            "Cr": {
              "chronic_bronchitis": [{"min": 0.8, "max": 1.2}],
              "emphysema": [{"min": 0.7, "max": 1.1}],
              "copd_cor_pulmonale": [{"min": 0.9, "max": 1.4}]
            }
          },
          "CBC": {
            "WBC": {
              "chronic_bronchitis": [{"min": 5000, "max": 10000}],
              "emphysema": [{"min": 5000, "max": 10000}],
              "copd_cor_pulmonale": [{"min": 5000, "max": 11000}]
            },
            "Hb": {
              "chronic_bronchitis": [{"min": 16.0, "max": 19.0}],
              "emphysema": [{"min": 13.0, "max": 16.0}],
              "copd_cor_pulmonale": [{"min": 15.0, "max": 18.0}]
            },
            "Plt": {
              "chronic_bronchitis": [{"min": 150000, "max": 400000}],
              "emphysema": [{"min": 150000, "max": 400000}],
              "copd_cor_pulmonale": [{"min": 150000, "max": 400000}]
            }
          },
          "ESR": {
            "chronic_bronchitis": [{"min": 0, "max": 20}],
            "emphysema": [{"min": 0, "max": 20}],
            "copd_cor_pulmonale": [{"min": 5, "max": 25}]
          },
          "CRP": {
            "chronic_bronchitis": [{"min": 0, "max": 5}],
            "emphysema": [{"min": 0, "max": 5}],
            "copd_cor_pulmonale": [{"min": 0, "max": 10}]
          },
          "VBG": {
            "pH": {
              "chronic_bronchitis": [{"min": 7.32, "max": 7.38}],
              "emphysema": [{"min": 7.38, "max": 7.42}],
              "copd_cor_pulmonale": [{"min": 7.30, "max": 7.40}]
            },
            "PCO2": {
              "chronic_bronchitis": [{"min": 50, "max": 65}],
              "emphysema": [{"min": 35, "max": 45}],
              "copd_cor_pulmonale": [{"min": 50, "max": 70}]
            },
            "HCO3": {
              "chronic_bronchitis": [{"min": 28, "max": 34}],
              "emphysema": [{"min": 22, "max": 26}],
              "copd_cor_pulmonale": [{"min": 26, "max": 32}]
            }
          },
          "LFTs": {
            "ALT": {
              "chronic_bronchitis": [{"min": 15, "max": 45}],
              "emphysema": [{"min": 10, "max": 40}],
              "copd_cor_pulmonale": [{"min": 30, "max": 80}]
            },
            "AST": {
              "chronic_bronchitis": [{"min": 15, "max": 45}],
              "emphysema": [{"min": 10, "max": 40}],
              "copd_cor_pulmonale": [{"min": 30, "max": 80}]
            }
          }
        },
        "specialized_lung_tests": {
          "D_dimer": {
            "chronic_bronchitis": ["Negative"],
            "emphysema": ["Negative"],
            "copd_cor_pulmonale": ["Negative"]
          },
          "Sputum_AFB": {
            "chronic_bronchitis": ["Negative"],
            "emphysema": ["Negative"],
            "copd_cor_pulmonale": ["Negative"]
          },
          "BNP_NT_proBNP": {
            "chronic_bronchitis": ["Normal"],
            "emphysema": ["Normal"],
            "copd_cor_pulmonale": ["Elevated"]
          },
          "Sputum_analysis": {
            "Gram_Stain": {
              "chronic_bronchitis": ["Mixed flora", "Normal flora"],
              "emphysema": ["Normal flora"],
              "copd_cor_pulmonale": ["Normal flora"]
            },
            "Sample_Quality": {
              "chronic_bronchitis": ["Adequate"],
              "emphysema": ["Adequate"],
              "copd_cor_pulmonale": ["Adequate"]
            }
          },
          "a1_antitrypsin_level": {
            "chronic_bronchitis": ["Normal range"],
            "emphysema": ["Low levels", "Normal range"],
            "copd_cor_pulmonale": ["Normal range"]
          }
        },
        "immunity_and_serology": {
          "HIV_test": {
            "chronic_bronchitis": ["Negative"],
            "emphysema": ["Negative"],
            "copd_cor_pulmonale": ["Negative"]
          },
          "Autoimmune_pannel_ANA_ANCA": {
            "chronic_bronchitis": ["Negative"],
            "emphysema": ["Negative"],
            "copd_cor_pulmonale": ["Negative"]
          }
        },
        "simple_imaging": {
          "Chest_X_Ray": {
            "PA_Lateral_Findings_and_Effusion": {
              "chronic_bronchitis": ["Increased bronchovascular markings"],
              "emphysema": ["Hyperinflation", "Flattened diaphragm"],
              "copd_cor_pulmonale": ["Cardiomegaly", "Pleural effusion", "Hyperinflation"]
            }
          }
        },
        "advanced_imaging": {
          "Chest_CT_CTPA": {
            "Lung_Parenchyma_and_Pleura": {
              "chronic_bronchitis": ["Bronchial wall thickening"],
              "emphysema": ["Emphysematous bullae", "Destruction of alveolar walls"],
              "copd_cor_pulmonale": ["Enlarged pulmonary arteries", "Pleural effusion"]
            }
          }
        },
        "functional_tests": {
          "dlco": {
            "chronic_bronchitis": ["Normal"],
            "emphysema": ["Decreased"],
            "copd_cor_pulmonale": ["Decreased"]
          },
          "peak_flow": {
            "chronic_bronchitis": ["Reduced"],
            "emphysema": ["Reduced"],
            "copd_cor_pulmonale": ["Significantly reduced"]
          },
          "Spirometry": {
            "Result": {
              "FEV1": {
                "chronic_bronchitis": [{"min": 50, "max": 70}],
                "emphysema": [{"min": 30, "max": 50}],
                "copd_cor_pulmonale": [{"min": 30, "max": 50}]
              },
              "FVC": {
                "chronic_bronchitis": [{"min": 80, "max": 95}],
                "emphysema": [{"min": 70, "max": 90}],
                "copd_cor_pulmonale": [{"min": 60, "max": 80}]
              },
              "FEV1/FVC": {
                "chronic_bronchitis": [{"min": 50, "max": 65}],
                "emphysema": [{"min": 40, "max": 60}],
                "copd_cor_pulmonale": [{"min": 40, "max": 60}]
              }
            },
            "reversibility": {
              "chronic_bronchitis": ["No significant reversibility"],
              "emphysema": ["No significant reversibility"],
              "copd_cor_pulmonale": ["No significant reversibility"]
            }
          },
          "plethysmography": {
            "chronic_bronchitis": ["Normal lung volumes"],
            "emphysema": ["Increased TLC and RV"],
            "copd_cor_pulmonale": ["Increased TLC and RV"]
          }
        },
        "procedures": {
          "Bronchoscopy": {
            "chronic_bronchitis": ["N/A"],
            "emphysema": ["N/A"],
            "copd_cor_pulmonale": ["N/A"]
          },
          "torachonthesis": {
            "Serum": {
              "Protein": {
                "chronic_bronchitis": ["N/A"],
                "emphysema": ["N/A"],
                "copd_cor_pulmonale": [{"min": 6.0, "max": 8.0}]
              },
              "LDH": {
                "chronic_bronchitis": ["N/A"],
                "emphysema": ["N/A"],
                "copd_cor_pulmonale": [{"min": 140, "max": 200}]
              },
              "Albumin": {
                "chronic_bronchitis": ["N/A"],
                "emphysema": ["N/A"],
                "copd_cor_pulmonale": [{"min": 3.5, "max": 5.0}]
              }
            },
            "Fluid": {
              "Protein": {
                "chronic_bronchitis": ["N/A"],
                "emphysema": ["N/A"],
                "copd_cor_pulmonale": [{"min": 1.0, "max": 2.5}]
              },
              "LDH": {
                "chronic_bronchitis": ["N/A"],
                "emphysema": ["N/A"],
                "copd_cor_pulmonale": [{"min": 50, "max": 100}]
              },
              "Albumin": {
                "chronic_bronchitis": ["N/A"],
                "emphysema": ["N/A"],
                "copd_cor_pulmonale": [{"min": 1.5, "max": 3.0}]
              }
            }
          }
        }
      }
    }
    
    def __init__(self):
        self.random = random
        
        # 1. SCENARIO SELECTION
        # chronic_bronchitis (40%), emphysema (30%), copd_cor_pulmonale (30%)
        self.scenario = self.random.choices(
            ["chronic_bronchitis", "emphysema", "copd_cor_pulmonale"], 
            weights=[40, 30, 30], k=1
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
        age_num = self.random.randint(45, 85)
        age_str = f"{age_num} ساله"
        
        name_key = "MALE" if gender == "مرد" else "FEMALE"
        first_name = self.random.choice(self.RANDOM_DATA_LISTS["first_names_sample_100"][name_key])
        last_name = self.random.choice(self.RANDOM_DATA_LISTS["last_names_sample_100"])
        
        occupation = self._select_occupation(gender, age_str)
        birth = self.random.choice(self.RANDOM_DATA_LISTS["famous_cities_sample_30"])
        residence = self._select_place_of_residence(birth)
        marital = self.random.choices(["متأهل", "همسر متوفی", "مجرد"], weights=[70, 25, 5], k=1)[0]
        
        return {
            "first_name": first_name, "last_name": last_name, "age": age_str,
            "gender": gender, "occupation": occupation,
            "place_of_birth": birth, "place_of_residence": residence,
            "marital_status": marital
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
        P_RATIO = 0.80 # Constant reference

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
