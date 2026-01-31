import random
import json

class PneumoniaDataGenerator:
    """
    کلاسی برای تولید داده‌های شبیه‌سازی شده پنومونی بر اساس فایل پنومونی.txt.
    
    Scenarios:
    1. typical_lobar (70%)
    2. complicated_effusion (20%)
    3. atypical_walking (10%)
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
            "راننده تاکسی", "مهندس نرم‌افزار", "کارمند بانک", "کارگر ساده", "نقاش ساختمان",
            "تکنسین برق", "پزشک عمومی", "فروشنده بازار", "وکیل", "معمار", "استاد دانشگاه"
        ],
        "occupations_female": [
            "خانه‌دار", "معلم بازنشسته", "پرستار", "آرایشگر", "حسابدار شرکت خصوصی",
            "پزشک عمومی", "فروشنده بازار", "وکیل", "خیاط", "استاد دانشگاه"
        ],
        "occupations_retirement": [
            "معلم بازنشسته", "بازنشسته نیروهای مسلح", "بازنشسته تأمین اجتماعی"
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
    
    # --- داده‌های استخراج شده از پنومونی.txt ---
    DATA_SOURCE = {
      "physical_exam": {
        "vital_signs": {
          "BP": {
            "typical_lobar": [{"min": 110, "max": 130}, {"min": 70, "max": 85}],
            "complicated_effusion": [{"min": 100, "max": 125}, {"min": 65, "max": 80}],
            "atypical_walking": [{"min": 110, "max": 130}, {"min": 70, "max": 85}]
          },
          "T": {
            "typical_lobar": [{"min": 38.5, "max": 40.0}],
            "complicated_effusion": [{"min": 38.0, "max": 39.5}],
            "atypical_walking": [{"min": 37.5, "max": 38.5}]
          },
          "PR": {
            "typical_lobar": [{"min": 100, "max": 120}],
            "complicated_effusion": [{"min": 100, "max": 125}],
            "atypical_walking": [{"min": 80, "max": 100}]
          },
          "RR": {
            "typical_lobar": [{"min": 20, "max": 28}],
            "complicated_effusion": [{"min": 22, "max": 30}],
            "atypical_walking": [{"min": 16, "max": 22}]
          },
          "SpO2": {
            "typical_lobar": [{"min": 90, "max": 94}],
            "complicated_effusion": [{"min": 88, "max": 93}],
            "atypical_walking": [{"min": 95, "max": 98}]
          },
          "GCS": {
            "typical_lobar": [{"min": 14, "max": 15}],
            "complicated_effusion": [{"min": 14, "max": 15}],
            "atypical_walking": [{"min": 15, "max": 15}]
          }
        },
        "general_appearance": {
          "mood_and_behavior": {
            "typical_lobar": ["Toxic and ill-appearing", "Anxious and restless"],
            "complicated_effusion": ["Mildly distressed due to pain", "Toxic and ill-appearing"],
            "atypical_walking": ["Calm with no acute distress", "Alert and cooperative"]
          },
          "overall_appearance": {
            "typical_lobar": ["Plethoric or ruddy complexion", "Diaphoretic"],
            "complicated_effusion": ["Pale", "Diaphoretic"],
            "atypical_walking": ["Well-nourished and well-developed"]
          },
          "posture_and_position": {
            "typical_lobar": ["Supine with no distress"],
            "complicated_effusion": ["Splinting to one side", "Unable to lie flat"],
            "atypical_walking": ["Supine with no distress"]
          },
          "level_of_consciousness": {
            "typical_lobar": ["Alert and oriented x3", "Confused or disoriented"],
            "complicated_effusion": ["Alert and oriented x3"],
            "atypical_walking": ["Alert and oriented x3"]
          },
          "cardiopulmonary_and_circulatory_clues": {
            "edema": {
              "typical_lobar": ["No edema"],
              "complicated_effusion": ["No edema"],
              "atypical_walking": ["No edema"]
            },
            "dyspnea": {
              "typical_lobar": ["Speaking in short phrases or single words", "Dyspnea at rest"],
              "complicated_effusion": ["Dyspnea at rest", "Speaking in short phrases or single words"],
              "atypical_walking": ["Speaking in full sentences"]
            },
            "cyanosis": {
              "typical_lobar": ["No cyanosis", "Central cyanosis"],
              "complicated_effusion": ["No cyanosis"],
              "atypical_walking": ["No cyanosis"]
            }
          }
        },
        "head_and_neck": {
          "head_and_face": {
            "symmetry_and_lesions": {
              "typical_lobar": ["Facial flushing"],
              "complicated_effusion": ["Symmetric with no lesions"],
              "atypical_walking": ["Symmetric with no lesions"]
            },
            "tenderness": {
              "typical_lobar": ["Non-tender"],
              "complicated_effusion": ["Non-tender"],
              "atypical_walking": ["Sinus tenderness on percussion", "Non-tender"]
            }
          },
          "eyes": {
            "sclera_and_conjunctiva": {
              "typical_lobar": ["Injected or red conjunctiva"],
              "complicated_effusion": ["Normal sclera and pink conjunctiva"],
              "atypical_walking": ["Normal sclera and pink conjunctiva"]
            },
            "pupils_reaction": {
              "typical_lobar": ["PERRLA"],
              "complicated_effusion": ["PERRLA"],
              "atypical_walking": ["PERRLA"]
            },
            "extraocular_movements": {
              "typical_lobar": ["Intact"],
              "complicated_effusion": ["Intact"],
              "atypical_walking": ["Intact"]
            }
          },
          "ears": {
            "external_and_tenderness": {
              "typical_lobar": ["Normal external ear, no tenderness"],
              "complicated_effusion": ["Normal external ear, no tenderness"],
              "atypical_walking": ["Normal external ear, no tenderness"]
            },
            "eardrum_appearance": {
              "typical_lobar": ["Intact pearly gray tympanic membrane"],
              "complicated_effusion": ["Intact pearly gray tympanic membrane"],
              "atypical_walking": ["Intact pearly gray tympanic membrane"]
            }
          },
          "nose_and_sinuses": {
            "septum_and_discharge": {
              "typical_lobar": ["Midline septum, no discharge"],
              "complicated_effusion": ["Midline septum, no discharge"],
              "atypical_walking": ["Clear rhinorrhea", "Midline septum, no discharge"]
            },
            "sinus_tenderness": {
              "typical_lobar": ["Non-tender"],
              "complicated_effusion": ["Non-tender"],
              "atypical_walking": ["Sinus tenderness on percussion", "Non-tender"]
            }
          },
          "mouth_and_pharynx": {
            "oral_mucosa_and_lesions": {
              "typical_lobar": ["Dry mucous membranes"],
              "complicated_effusion": ["Dry mucous membranes"],
              "atypical_walking": ["Moist and pink"]
            },
            "pharynx_and_tonsils": {
              "typical_lobar": ["Non-erythematous, no exudates"],
              "complicated_effusion": ["Non-erythematous, no exudates"],
              "atypical_walking": ["Erythematous pharynx", "Non-erythematous, no exudates"]
            }
          },
          "neck_and_lymphatics": {
            "inspection": {
              "typical_lobar": ["Trachea midline"],
              "complicated_effusion": ["Trachea deviated to the healthy side", "Trachea midline"],
              "atypical_walking": ["Trachea midline"]
            },
            "tracheal_position": {
              "typical_lobar": ["Trachea midline"],
              "complicated_effusion": ["Trachea deviated to the healthy side", "Trachea midline"],
              "atypical_walking": ["Trachea midline"]
            },
            "thyroid_gland": {
              "typical_lobar": ["Non-palpable"],
              "complicated_effusion": ["Non-palpable"],
              "atypical_walking": ["Non-palpable"]
            },
            "carotid_bruit": {
              "typical_lobar": ["No bruits"],
              "complicated_effusion": ["No bruits"],
              "atypical_walking": ["No bruits"]
            },
            "lymph_nodes_size_consistency": {
              "typical_lobar": ["No lymphadenopathy"],
              "complicated_effusion": ["No lymphadenopathy"],
              "atypical_walking": ["Tender cervical lymphadenopathy", "No lymphadenopathy"]
            },
            "lymph_nodes_mobility_tenderness": {
              "typical_lobar": ["No lymphadenopathy"],
              "complicated_effusion": ["No lymphadenopathy"],
              "atypical_walking": ["Tender cervical lymphadenopathy", "No lymphadenopathy"]
            }
          }
        },
        "respiratory_system": {
          "inspection": {
            "accessory_muscles": {
              "typical_lobar": ["Intercostal retractions", "No accessory muscle use"],
              "complicated_effusion": ["Intercostal retractions"],
              "atypical_walking": ["No accessory muscle use"]
            },
            "chest_shape_and_symmetry": {
              "typical_lobar": ["Symmetric chest rise"],
              "complicated_effusion": ["Asymmetric chest expansion"],
              "atypical_walking": ["Symmetric chest rise"]
            }
          },
          "palpation": {
            "chest_expansion": {
              "typical_lobar": ["Symmetric expansion"],
              "complicated_effusion": ["Decreased expansion on the right side", "Decreased expansion on the left side"],
              "atypical_walking": ["Symmetric expansion"]
            },
            "tactile_fremitus": {
              "typical_lobar": ["Increased tactile fremitus"],
              "complicated_effusion": ["Absent tactile fremitus", "Decreased tactile fremitus"],
              "atypical_walking": ["Normal tactile fremitus"]
            }
          },
          "percussion": {
            "typical_lobar": ["Dull"],
            "complicated_effusion": ["Stony Dull"],
            "atypical_walking": ["Resonant"]
          },
          "auscultation": {
            "breath_sounds_intensity": {
              "typical_lobar": ["Bronchial breath sounds"],
              "complicated_effusion": ["Absent breath sounds at bases", "Decreased breath sounds"],
              "atypical_walking": ["Vesicular sounds, normal intensity"]
            },
            "adventitious_sounds": {
              "typical_lobar": ["Coarse Crackles", "Fine Crackles"],
              "complicated_effusion": ["Pleural Friction Rub", "No adventitious sounds"],
              "atypical_walking": ["Fine Crackles", "No adventitious sounds"]
            }
          }
        },
        "cardiovascular_system": {
          "JVP_assessment": {
            "typical_lobar": ["JVP not elevated"],
            "complicated_effusion": ["JVP not elevated"],
            "atypical_walking": ["JVP not elevated"]
          },
          "palpation": {
            "precordial_palpation_heave_thrill": {
              "typical_lobar": ["No heaves or thrills"],
              "complicated_effusion": ["No heaves or thrills"],
              "atypical_walking": ["No heaves or thrills"]
            },
            "pmi_assessment": {
              "typical_lobar": ["PMI at 5th ICS MCL"],
              "complicated_effusion": ["PMI at 5th ICS MCL", "PMI displaced laterally"],
              "atypical_walking": ["PMI at 5th ICS MCL"]
            }
          },
          "auscultation": {
            "heart_sounds_s1_s2": {
              "typical_lobar": ["Normal S1, S2"],
              "complicated_effusion": ["Normal S1, S2"],
              "atypical_walking": ["Normal S1, S2"]
            },
            "extra_sounds_s3_s4_murmurs": {
              "typical_lobar": ["No extra sounds or murmurs"],
              "complicated_effusion": ["No extra sounds or murmurs"],
              "atypical_walking": ["No extra sounds or murmurs"]
            }
          },
          "2_pulses_and_extremities": {
            "peripheral_pulses_symmetry_and_quality": {
              "typical_lobar": ["Bounding pulses"],
              "complicated_effusion": ["Pulses 2+ and symmetric"],
              "atypical_walking": ["Pulses 2+ and symmetric"]
            },
            "extremities_color_and_trophic_changes": {
              "typical_lobar": ["No trophic changes"],
              "complicated_effusion": ["No trophic changes"],
              "atypical_walking": ["No trophic changes"]
            },
            "extremities_temperature_and_cap_refill": {
              "typical_lobar": ["Warm extremities"],
              "complicated_effusion": ["Warm extremities"],
              "atypical_walking": ["Warm, Capillary refill < 2 sec"]
            },
            "extremities_edema": {
              "typical_lobar": ["No edema"],
              "complicated_effusion": ["No edema"],
              "atypical_walking": ["No edema"]
            }
          }
        },
        "abdominal_system": {
          "inspection": {
            "typical_lobar": ["Flat, non-distended"],
            "complicated_effusion": ["Flat, non-distended"],
            "atypical_walking": ["Flat, non-distended"]
          },
          "auscultation": {
            "bowel_sounds": {
              "typical_lobar": ["Normoactive bowel sounds"],
              "complicated_effusion": ["Normoactive bowel sounds"],
              "atypical_walking": ["Normoactive bowel sounds"]
            },
            "vascular_bruits": {
              "typical_lobar": ["No bruits"],
              "complicated_effusion": ["No bruits"],
              "atypical_walking": ["No bruits"]
            }
          },
          "percussion": {
            "general": {
              "typical_lobar": ["Resonant"],
              "complicated_effusion": ["Resonant"],
              "atypical_walking": ["Resonant"]
            },
            "organ_borders": {
              "typical_lobar": ["Normal liver span"],
              "complicated_effusion": ["Normal liver span"],
              "atypical_walking": ["Normal liver span"]
            }
          },
          "palpation": {
            "superficial_tenderness": {
              "typical_lobar": ["Soft, non-tender"],
              "complicated_effusion": ["Soft, non-tender"],
              "atypical_walking": ["Soft, non-tender"]
            },
            "deep_masses_and_organs": {
              "typical_lobar": ["No masses or organomegaly"],
              "complicated_effusion": ["No masses or organomegaly"],
              "atypical_walking": ["No masses or organomegaly"]
            }
          },
          "peritoneal_signs": {
            "typical_lobar": ["None"],
            "complicated_effusion": ["None"],
            "atypical_walking": ["None"]
          }
        },
        "neurological": {
          "mental_status_and_LOC": {
            "typical_lobar": ["Confused or disoriented", "Alert and Oriented"],
            "complicated_effusion": ["Alert and Oriented"],
            "atypical_walking": ["Alert and Oriented"]
          },
          "cranial_nerves": {
            "typical_lobar": ["Intact"],
            "complicated_effusion": ["Intact"],
            "atypical_walking": ["Intact"]
          },
          "motor_strength_and_tone": {
            "typical_lobar": ["5/5 strength globally"],
            "complicated_effusion": ["5/5 strength globally"],
            "atypical_walking": ["5/5 strength globally"]
          },
          "involuntary_movements": {
            "typical_lobar": ["None"],
            "complicated_effusion": ["None"],
            "atypical_walking": ["None"]
          },
          "sensory_light_touch_and_pain": {
            "typical_lobar": ["Intact"],
            "complicated_effusion": ["Intact"],
            "atypical_walking": ["Intact"]
          },
          "deep_tendon_reflexes": {
            "typical_lobar": ["2+"],
            "complicated_effusion": ["2+"],
            "atypical_walking": ["2+"]
          },
          "coordination_and_gait": {
            "typical_lobar": ["Intact"],
            "complicated_effusion": ["Intact"],
            "atypical_walking": ["Intact"]
          }
        },
        "musculoskeletal_system": {
          "inspection": {
            "joints": {
              "typical_lobar": ["Normal joints"],
              "complicated_effusion": ["Normal joints"],
              "atypical_walking": ["Normal joints"]
            },
            "muscles": {
              "typical_lobar": ["Normal bulk"],
              "complicated_effusion": ["Normal bulk"],
              "atypical_walking": ["Normal bulk"]
            }
          },
          "palpation": {
            "tenderness_and_crepitus": {
              "typical_lobar": ["No tenderness"],
              "complicated_effusion": ["Chest wall tenderness"],
              "atypical_walking": ["No tenderness"]
            }
          },
          "range_of_motion_active_passive": {
            "typical_lobar": ["Full"],
            "complicated_effusion": ["Full"],
            "atypical_walking": ["Full"]
          },
          "stability_and_function": {
            "typical_lobar": ["Stable"],
            "complicated_effusion": ["Stable"],
            "atypical_walking": ["Stable"]
          }
        }
      },
      "paraclinic": {
        "basic_blood_tests": {
          "BMP": {
            "Na": {
              "typical_lobar": [{"min": 133, "max": 145}],
              "complicated_effusion": [{"min": 135, "max": 145}],
              "atypical_walking": [{"min": 135, "max": 145}]
            },
            "BUN": {
              "typical_lobar": [{"min": 15, "max": 35}],
              "complicated_effusion": [{"min": 10, "max": 25}],
              "atypical_walking": [{"min": 7, "max": 20}]
            },
            "Cr": {
              "typical_lobar": [{"min": 0.8, "max": 1.4}],
              "complicated_effusion": [{"min": 0.7, "max": 1.2}],
              "atypical_walking": [{"min": 0.7, "max": 1.1}]
            }
          },
          "CBC": {
            "WBC": {
              "typical_lobar": [{"min": 14000, "max": 25000}],
              "complicated_effusion": [{"min": 12000, "max": 20000}],
              "atypical_walking": [{"min": 4500, "max": 11000}]
            },
            "Hb": {
              "typical_lobar": [{"min": 13.0, "max": 16.0}],
              "complicated_effusion": [{"min": 12.0, "max": 15.0}],
              "atypical_walking": [{"min": 13.0, "max": 16.0}]
            },
            "Plt": {
              "typical_lobar": [{"min": 150000, "max": 450000}],
              "complicated_effusion": [{"min": 200000, "max": 500000}],
              "atypical_walking": [{"min": 150000, "max": 400000}]
            }
          },
          "ESR": {
            "typical_lobar": [{"min": 40, "max": 90}],
            "complicated_effusion": [{"min": 50, "max": 100}],
            "atypical_walking": [{"min": 10, "max": 30}]
          },
          "CRP": {
            "typical_lobar": [{"min": 50, "max": 200}],
            "complicated_effusion": [{"min": 60, "max": 250}],
            "atypical_walking": [{"min": 5, "max": 20}]
          },
          "VBG": {
            "pH": {
              "typical_lobar": [{"min": 7.30, "max": 7.45}],
              "complicated_effusion": [{"min": 7.30, "max": 7.42}],
              "atypical_walking": [{"min": 7.35, "max": 7.45}]
            },
            "PCO2": {
              "typical_lobar": [{"min": 30, "max": 40}],
              "complicated_effusion": [{"min": 32, "max": 42}],
              "atypical_walking": [{"min": 35, "max": 45}]
            },
            "HCO3": {
              "typical_lobar": [{"min": 20, "max": 24}],
              "complicated_effusion": [{"min": 20, "max": 24}],
              "atypical_walking": [{"min": 22, "max": 26}]
            }
          },
          "LFTs": {
            "ALT": {
              "typical_lobar": [{"min": 20, "max": 60}],
              "complicated_effusion": [{"min": 15, "max": 45}],
              "atypical_walking": [{"min": 10, "max": 40}]
            },
            "AST": {
              "typical_lobar": [{"min": 20, "max": 60}],
              "complicated_effusion": [{"min": 15, "max": 45}],
              "atypical_walking": [{"min": 10, "max": 40}]
            }
          }
        },
        "specialized_lung_tests": {
          "D_dimer": {
            "typical_lobar": ["Negative"],
            "complicated_effusion": ["Negative"],
            "atypical_walking": ["Negative"]
          },
          "Sputum_AFB": {
            "typical_lobar": ["Negative"],
            "complicated_effusion": ["Negative"],
            "atypical_walking": ["Negative"]
          },
          "BNP_NT_proBNP": {
            "typical_lobar": ["Normal"],
            "complicated_effusion": ["Normal"],
            "atypical_walking": ["Normal"]
          },
          "Sputum_analysis": {
            "Gram_Stain": {
              "typical_lobar": ["Positive for Gram-positive cocci"],
              "complicated_effusion": ["Positive for Gram-positive cocci"],
              "atypical_walking": ["Normal flora"]
            },
            "Sample_Quality": {
              "typical_lobar": ["Adequate"],
              "complicated_effusion": ["Adequate"],
              "atypical_walking": ["Adequate"]
            }
          },
          "a1_antitrypsin_level": {
            "typical_lobar": ["Normal range"],
            "complicated_effusion": ["Normal range"],
            "atypical_walking": ["Normal range"]
          }
        },
        "immunity_and_serology": {
          "HIV_test": {
            "typical_lobar": ["Negative"],
            "complicated_effusion": ["Negative"],
            "atypical_walking": ["Negative"]
          },
          "Autoimmune_pannel_ANA_ANCA": {
            "typical_lobar": ["Negative"],
            "complicated_effusion": ["Negative"],
            "atypical_walking": ["Negative"]
          }
        },
        "simple_imaging": {
          "Chest_X_Ray": {
            "PA_Lateral_Findings_and_Effusion": {
              "typical_lobar": ["Lobar consolidation"],
              "complicated_effusion": ["Pleural effusion", "Lobar consolidation"],
              "atypical_walking": ["Patchy infiltrates"]
            }
          }
        },
        "advanced_imaging": {
          "Chest_CT_CTPA": {
            "Lung_Parenchyma_and_Pleura": {
              "typical_lobar": ["Air bronchogram", "Consolidation"],
              "complicated_effusion": ["Pleural effusion", "Consolidation"],
              "atypical_walking": ["Ground glass opacities"]
            }
          }
        },
        "functional_tests": {
          "dlco": {
            "typical_lobar": ["N/A"],
            "complicated_effusion": ["N/A"],
            "atypical_walking": ["N/A"]
          },
          "peak_flow": {
            "typical_lobar": ["N/A"],
            "complicated_effusion": ["N/A"],
            "atypical_walking": ["N/A"]
          },
          "Spirometry": {
            "Result": {
              "FEV1": {
                "typical_lobar": [{"min": 70, "max": 90}],
                "complicated_effusion": [{"min": 60, "max": 80}],
                "atypical_walking": [{"min": 80, "max": 100}]
              },
              "FVC": {
                "typical_lobar": [{"min": 70, "max": 90}],
                "complicated_effusion": [{"min": 60, "max": 80}],
                "atypical_walking": [{"min": 80, "max": 100}]
              },
              "FEV1/FVC": {
                "typical_lobar": [{"min": 75, "max": 85}],
                "complicated_effusion": [{"min": 75, "max": 85}],
                "atypical_walking": [{"min": 75, "max": 85}]
              }
            },
            "reversibility": {
              "typical_lobar": ["No significant reversibility"],
              "complicated_effusion": ["No significant reversibility"],
              "atypical_walking": ["No significant reversibility"]
            }
          },
          "plethysmography": {
            "typical_lobar": ["N/A"],
            "complicated_effusion": ["N/A"],
            "atypical_walking": ["N/A"]
          }
        },
        "procedures": {
          "Bronchoscopy": {
            "typical_lobar": ["N/A"],
            "complicated_effusion": ["N/A"],
            "atypical_walking": ["N/A"]
          },
          "torachonthesis": {
            "Serum": {
              "Protein": {
                "typical_lobar": ["N/A"],
                "complicated_effusion": [{"min": 6.0, "max": 8.0}],
                "atypical_walking": ["N/A"]
              },
              "LDH": {
                "typical_lobar": ["N/A"],
                "complicated_effusion": [{"min": 140, "max": 200}],
                "atypical_walking": ["N/A"]
              },
              "Albumin": {
                "typical_lobar": ["N/A"],
                "complicated_effusion": [{"min": 3.5, "max": 5.0}],
                "atypical_walking": ["N/A"]
              }
            },
            "Fluid": {
              "Protein": {
                "typical_lobar": ["N/A"],
                "complicated_effusion": [{"min": 3.5, "max": 6.0}],
                "atypical_walking": ["N/A"]
              },
              "LDH": {
                "typical_lobar": ["N/A"],
                "complicated_effusion": [{"min": 1000, "max": 3000}],
                "atypical_walking": ["N/A"]
              },
              "Albumin": {
                "typical_lobar": ["N/A"],
                "complicated_effusion": [{"min": 2.0, "max": 3.0}],
                "atypical_walking": ["N/A"]
              }
            }
          }
        }
      }
    }
    
    def __init__(self):
        self.random = random
        
        # 1. SCENARIO SELECTION
        # typical_lobar (70%), complicated_effusion (20%), atypical_walking (10%)
        self.scenario = self.random.choices(
            ["typical_lobar", "complicated_effusion", "atypical_walking"], 
            weights=[70, 10, 20], k=1
        )[0]

    # --- Helper to extract data from DATA_SOURCE ---
    def _get_val(self, category, system, key, subkey=None, subsubkey=None):
        """
        این متد داده مربوط به سناریوی جاری را از دیکشنری استخراج می‌کند.
        اگر داده لیست رشته باشد -> random.choice
        اگر داده لیست بازه عددی باشد -> random between min/max
        اگر داده دیکشنری باشد (مثل BP) -> کل لیست دیکشنری را برمی‌گرداند تا تابع فراخوان هندل کند
        """
        try:
            node = self.DATA_SOURCE[category][system][key]
            if subkey:
                node = node[subkey]
            if subsubkey:
                node = node[subsubkey]
                
            # دسترسی به سناریوی خاص
            scenario_data = node[self.scenario]
            
            # اگر داده رشته ساده (مثل N/A) باشد
            if isinstance(scenario_data, str):
                return scenario_data

            # اگر لیست نباشد (مثلا N/A نبود اما دیکشنری هم نیست - بعید است در این ساختار)
            if not isinstance(scenario_data, list):
                return str(scenario_data)

            # اگر لیست خالی باشد
            if not scenario_data:
                return "N/A"

            # بررسی آیتم اول برای تشخیص نوع
            first_item = scenario_data[0]
            
            # حالت بازه عددی: [{"min": x, "max": y}]
            if isinstance(first_item, dict) and "min" in first_item:
                if len(scenario_data) == 1:
                    r = scenario_data[0]
                    val = self.random.uniform(r["min"], r["max"])
                    # اگر اعداد صحیح هستند، int کن
                    if isinstance(r["min"], int) and isinstance(r["max"], int):
                        return int(val)
                    return round(val, 1) # برای دما و ... 
                else:
                    # برای BP که دو تا دیکشنری دارد، لیست را برمی‌گردانیم تا caller هندل کند
                    results = []
                    for r in scenario_data:
                        val = self.random.uniform(r["min"], r["max"])
                        if isinstance(r["min"], int) and isinstance(r["max"], int):
                            results.append(int(val))
                        else:
                            results.append(round(val, 1))
                    return results

            # حالت انتخاب رشته: ["Option A", "Option B"]
            elif isinstance(first_item, str):
                return self.random.choice(scenario_data)
                
            return "Unknown Format"

        except Exception as e:
            return f"Error ({key}): {str(e)}"

    # --- Demographic Helpers ---
    def _select_occupation(self, gender, age_str):
        age = int(age_str.split()[0])
        if age > 65: return self.random.choice(self.RANDOM_DATA_LISTS["occupations_retirement"])
        if 55 <= age <= 65:
            return self.random.choice(self.RANDOM_DATA_LISTS["occupations_retirement"]) if self.random.random() < 0.5 else (self.random.choice(self.RANDOM_DATA_LISTS["occupations_male"]) if gender == "مرد" else self.random.choice(self.RANDOM_DATA_LISTS["occupations_female"]))
        return self.random.choice(self.RANDOM_DATA_LISTS["occupations_male"]) if gender == "مرد" else self.random.choice(self.RANDOM_DATA_LISTS["occupations_female"])

    def _select_place_of_residence(self, place_of_birth):
        if self.random.random() < 0.7:
            nearby_cities = self.RANDOM_DATA_LISTS["city_proximity"].get(place_of_birth, [])
            if nearby_cities: return self.random.choice(nearby_cities)
        return self.random.choice(self.RANDOM_DATA_LISTS["famous_cities_sample_30"])

    def _select_marital_status(self, gender, age_str):
        age = int(age_str.split()[0])
        prob_married = 0
        if gender == "مرد": prob_married = 0.8 if age >= 45 else 0.5
        elif gender == "زن": prob_married = 0.9 if age >= 35 else 0.6
        return self.random.choices(["متأهل", "همسر متوفی"], weights=[90, 10], k=1)[0] if self.random.random() < prob_married else self.random.choices(["مجرد", "مطلقه"], weights=[70, 30], k=1)[0]

    def _generate_personal_information(self):
        gender = self.random.choice(["مرد", "زن"])
        age_num = self.random.randint(40, 75)
        age_str = f"{age_num} ساله"
        name_key = "MALE" if gender == "مرد" else "FEMALE"
        return {
            "first_name": self.random.choice(self.RANDOM_DATA_LISTS["first_names_sample_100"][name_key]),
            "last_name": self.random.choice(self.RANDOM_DATA_LISTS["last_names_sample_100"]),
            "age": age_str, "gender": gender,
            "occupation": self._select_occupation(gender, age_str),
            "place_of_birth": (birth := self.random.choice(self.RANDOM_DATA_LISTS["famous_cities_sample_30"])),
            "place_of_residence": self._select_place_of_residence(birth),
            "marital_status": self._select_marital_status(gender, age_str)
        }

    # ==========================================
    # 1. PHYSICAL EXAM GENERATION
    # ==========================================
    def _gen_vitals(self):
        cat = "physical_exam"
        sys = "vital_signs"
        
        bp_raw = self._get_val(cat, sys, "BP") # Returns [sys, dia] list
        temp = self._get_val(cat, sys, "T")
        pr = self._get_val(cat, sys, "PR")
        rr = self._get_val(cat, sys, "RR")
        spo2 = self._get_val(cat, sys, "SpO2")
        gcs = self._get_val(cat, sys, "GCS")
        
        # Format BP
        if isinstance(bp_raw, list) and len(bp_raw) == 2:
            bp_str = f"{bp_raw[0]}/{bp_raw[1]} mmHg"
        else:
            bp_str = str(bp_raw)

        return {
            "BP": bp_str,
            "T": f"{temp} °C",
            "PR": f"{pr} bpm",
            "RR": f"{rr} breaths/min",
            "SpO2": f"{spo2}% on Room Air",
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
                "breath_sounds": self._get_val(cat, sys, "auscultation", "breath_sounds_intensity"),
                "adventitious_sounds": self._get_val(cat, sys, "auscultation", "adventitious_sounds")
            }
        }

    def _gen_cardio(self):
        cat = "physical_exam"
        sys = "cardiovascular_system"
        
        # Note: input key is "2_pulses_and_extremities", output key "peripheral_pulses_and_extremities"
        
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
        # The text file provides %Predicted ranges. We simulate "Measured" based on that.
        # Predicted Values (Constants for simulation)
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
             fev1_out = fev1_pct # N/A case
             
        if isinstance(fvc_pct, (int, float)):
             fvc_meas = round(P_FVC * (fvc_pct / 100), 2)
             fvc_out = f"Measured: {fvc_meas} L, Predicted: {P_FVC} L, %Predicted: {fvc_pct}%"
        else:
             fvc_out = fvc_pct
             
        if isinstance(ratio_pct, (int, float)):
             ratio_meas = round(ratio_pct / 100, 2)
             ratio_out = f"Value: {ratio_meas} ({ratio_pct}%)"
        else:
             ratio_out = ratio_pct

        # --- Procedures (Thoracentesis) ---
        sys = "procedures"
        bronch = self._get_val(cat, sys, "Bronchoscopy")
        
        # Thoracentesis Nested Logic
        try:
            serum_prot = self._get_val(cat, sys, "torachonthesis", "Serum", "Protein")
            serum_ldh = self._get_val(cat, sys, "torachonthesis", "Serum", "LDH")
            serum_alb = self._get_val(cat, sys, "torachonthesis", "Serum", "Albumin")
            
            fluid_prot = self._get_val(cat, sys, "torachonthesis", "Fluid", "Protein")
            fluid_ldh = self._get_val(cat, sys, "torachonthesis", "Fluid", "LDH")
            fluid_alb = self._get_val(cat, sys, "torachonthesis", "Fluid", "Albumin")
            
            if serum_prot == "N/A":
                thora_result = "Not Indicated"
            else:
                thora_result = {
                    "Serum": {"Protein": f"{serum_prot} g/dL", "LDH": f"{serum_ldh} U/L", "Albumin": f"{serum_alb} g/dL"},
                    "Fluid": {"Protein": f"{fluid_prot} g/dL", "LDH": f"{fluid_ldh} U/L", "Albumin": f"{fluid_alb} g/dL"}
                }
        except:
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

    # ==========================================
    # MAIN GENERATION METHOD
    # ==========================================
    def generate_paraclinic_case(self):
        
        # 1. Personal Info
        personal_info = self._generate_personal_information()
        personal_info["Scenario"] = self.scenario # Tag for validation
        
        # 2. Physical Exam
        vitals = self._gen_vitals()
        gen_app = self._gen_general_appearance()
        head_neck = self._gen_head_neck()
        respiratory = self._gen_respiratory()
        cardio = self._gen_cardio()
        abdominal = self._gen_abdominal()
        neuro = self._gen_neuro()
        msk = self._gen_msk()

        # 3. Paraclinic
        paraclinic = self._gen_paraclinic()

        # 4. Assembly
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
