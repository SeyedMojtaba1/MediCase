import random

class AsthmaDataGenerator:
    """
    کلاسی برای تولید داده‌های شبیه‌سازی شده Asthma بر اساس فایل Asthma.txt.
    
    Scenarios:
    1. mild_allergic (80%)
    2. severe_uncontrolled (10%)
    3. exercise_induced (10%)
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
            "دانشجو", "مهندس نرم‌افزار", "کارمند بانک", "معلم", "نقاش ساختمان",
            "تکنسین برق", "ورزشکار", "فروشنده", "وکیل", "معمار", "استاد دانشگاه"
        ],
        "occupations_female": [
            "خانه دار", "معلم", "پرستار", "خیاط", "حسابدار",
            "فروشنده", "کارمند اداری", "استاد دانشگاه", "دانشجو"
        ],
        "famous_cities_sample_30": [
            "تهران", "مشهد", "اصفهان", "شیراز", "تبریز", "اهواز", "کرج", "قم", "کرمان", "یزد",
            "رشت", "ساری", "بندرعباس", "کرمانشاه", "ارومیه", "زاهدان", "همدان", "قزوین", "اردبیل", "زنجان",
            "گرگان", "سنندج", "بیرجند", "بوشهر", "سمنان", "خرم آباد", "ایلام", "یاسوج", "شهرکرد", "سیرجان"
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
            "bوشهر": ["شیراز", "اهواز"],
            "سمنان": ["تهران", "مشهد"],
            "خرم‌آباد": ["اهواز", "ایلام"],
            "ایلام": ["کرمانشاه", "خرم‌آباد"],
            "یاسوج": ["شیراز", "شهرکرد"],
            "شهرکرد": ["اصفهان", "یاسوج"],
            "سیرجان": ["کرمان"]
        }
    }

    # --- داده‌های دیکشنری استخراج شده از آسم.txt ---
    DATA_SOURCE = {
        "physical_exam": {
            "vital_signs": {
                "BP": {
                    "mild_allergic": [{"min": 110, "max": 130}, {"min": 70, "max": 85}],
                    "severe_uncontrolled": [{"min": 130, "max": 145}, {"min": 80, "max": 95}],
                    "exercise_induced": [{"min": 110, "max": 125}, {"min": 65, "max": 80}]
                },
                "T": {
                    "mild_allergic": [{"min": 36.5, "max": 37.2}],
                    "severe_uncontrolled": [{"min": 36.6, "max": 37.3}],
                    "exercise_induced": [{"min": 36.5, "max": 37.0}]
                },
                "PR": {
                    "mild_allergic": [{"min": 65, "max": 85}],
                    "severe_uncontrolled": [{"min": 95, "max": 115}],
                    "exercise_induced": [{"min": 55, "max": 75}]
                },
                "RR": {
                    "mild_allergic": [{"min": 12, "max": 16}],
                    "severe_uncontrolled": [{"min": 22, "max": 28}],
                    "exercise_induced": [{"min": 12, "max": 16}]
                },
                "SpO2": {
                    "mild_allergic": [{"min": 97, "max": 99}],
                    "severe_uncontrolled": [{"min": 91, "max": 94}],
                    "exercise_induced": [{"min": 98, "max": 100}]
                },
                "GCS": {
                    "mild_allergic": [{"min": 15, "max": 15}],
                    "severe_uncontrolled": [{"min": 15, "max": 15}],
                    "exercise_induced": [{"min": 15, "max": 15}]
                }
            },
            "general_appearance": {
                "mood_and_behavior": {
                    "mild_allergic": ["Alert and cooperative", "Calm with no acute distress"],
                    "severe_uncontrolled": ["Anxious and restless", "Irritable"],
                    "exercise_induced": ["Alert and cooperative", "Calm with no acute distress"]
                },
                "overall_appearance": {
                    "mild_allergic": ["Well-nourished and well-developed"],
                    "severe_uncontrolled": ["Pale", "Diaphoretic", "Well-nourished and well-developed"],
                    "exercise_induced": ["Well-nourished and well-developed"]
                },
                "posture_and_position": {
                    "mild_allergic": ["Supine with no distress", "Sitting upright in tripod position"],
                    "severe_uncontrolled": ["Sitting upright in tripod position", "Leaning forward", "Unable to lie flat"],
                    "exercise_induced": ["Supine with no distress"]
                },
                "level_of_consciousness": {
                    "mild_allergic": ["Alert and oriented x3"],
                    "severe_uncontrolled": ["Alert and oriented x3", "Agitated"],
                    "exercise_induced": ["Alert and oriented x3"]
                },
                "cardiopulmonary_and_circulatory_clues": {
                    "edema": {
                        "mild_allergic": ["No edema"],
                        "severe_uncontrolled": ["No edema"],
                        "exercise_induced": ["No edema"]
                    },
                    "dyspnea": {
                        "mild_allergic": ["Speaking in full sentences"],
                        "severe_uncontrolled": ["Speaking in short phrases or single words", "Dyspnea at rest", "Pursed-lip breathing"],
                        "exercise_induced": ["Speaking in full sentences"]
                    },
                    "cyanosis": {
                        "mild_allergic": ["No cyanosis"],
                        "severe_uncontrolled": ["No cyanosis", "Perioral cyanosis"],
                        "exercise_induced": ["No cyanosis"]
                    }
                }
            },
            "head_and_neck": {
                "head_and_face": {
                    "symmetry_and_lesions": {
                        "mild_allergic": ["Symmetric with no lesions", "Facial flushing"],
                        "severe_uncontrolled": ["Symmetric with no lesions", "Facial flushing"],
                        "exercise_induced": ["Symmetric with no lesions"]
                    },
                    "tenderness": {
                        "mild_allergic": ["Non-tender", "Sinus tenderness on percussion"],
                        "severe_uncontrolled": ["Sinus tenderness on percussion", "Non-tender"],
                        "exercise_induced": ["Non-tender"]
                    }
                },
                "eyes": {
                    "sclera_and_conjunctiva": {
                        "mild_allergic": ["Injected or red conjunctiva", "Normal sclera and pink conjunctiva"],
                        "severe_uncontrolled": ["Normal sclera and pink conjunctiva"],
                        "exercise_induced": ["Normal sclera and pink conjunctiva"]
                    },
                    "pupils_reaction": {
                        "mild_allergic": ["PERRLA"],
                        "severe_uncontrolled": ["PERRLA"],
                        "exercise_induced": ["PERRLA"]
                    },
                    "extraocular_movements": {
                        "mild_allergic": ["Intact"],
                        "severe_uncontrolled": ["Intact"],
                        "exercise_induced": ["Intact"]
                    }
                },
                "ears": {
                    "external_and_tenderness": {
                        "mild_allergic": ["Normal external ear, no tenderness"],
                        "severe_uncontrolled": ["Normal external ear, no tenderness"],
                        "exercise_induced": ["Normal external ear, no tenderness"]
                    },
                    "eardrum_appearance": {
                        "mild_allergic": ["Intact pearly gray tympanic membrane"],
                        "severe_uncontrolled": ["Intact pearly gray tympanic membrane"],
                        "exercise_induced": ["Intact pearly gray tympanic membrane"]
                    }
                },
                "nose_and_sinuses": {
                    "septum_and_discharge": {
                        "mild_allergic": ["Clear rhinorrhea", "Midline septum, no discharge"],
                        "severe_uncontrolled": ["Nasal polyps", "Midline septum, no discharge"],
                        "exercise_induced": ["Midline septum, no discharge"]
                    },
                    "sinus_tenderness": {
                        "mild_allergic": ["Sinus tenderness on percussion", "Non-tender"],
                        "severe_uncontrolled": ["Sinus tenderness on percussion", "Non-tender"],
                        "exercise_induced": ["Non-tender"]
                    }
                },
                "mouth_and_pharynx": {
                    "oral_mucosa_and_lesions": {
                        "mild_allergic": ["Moist and pink"],
                        "severe_uncontrolled": ["Dry mucous membranes", "Moist and pink"],
                        "exercise_induced": ["Moist and pink"]
                    },
                    "pharynx_and_tonsils": {
                        "mild_allergic": ["Cobblestoning of posterior pharynx", "Non-erythematous, no exudates"],
                        "severe_uncontrolled": ["Non-erythematous, no exudates"],
                        "exercise_induced": ["Non-erythematous, no exudates"]
                    }
                },
                "neck_and_lymphatics": {
                    "inspection": {
                        "mild_allergic": ["Trachea midline"],
                        "severe_uncontrolled": ["Trachea midline"],
                        "exercise_induced": ["Trachea midline"]
                    },
                    "tracheal_position": {
                        "mild_allergic": ["Trachea midline"],
                        "severe_uncontrolled": ["Trachea midline"],
                        "exercise_induced": ["Trachea midline"]
                    },
                    "thyroid_gland": {
                        "mild_allergic": ["Non-palpable"],
                        "severe_uncontrolled": ["Non-palpable"],
                        "exercise_induced": ["Non-palpable"]
                    },
                    "carotid_bruit": {
                        "mild_allergic": ["No bruits"],
                        "severe_uncontrolled": ["No bruits"],
                        "exercise_induced": ["No bruits"]
                    },
                    "lymph_nodes_size_consistency": {
                        "mild_allergic": ["No lymphadenopathy"],
                        "severe_uncontrolled": ["No lymphadenopathy"],
                        "exercise_induced": ["No lymphadenopathy"]
                    },
                    "lymph_nodes_mobility_tenderness": {
                        "mild_allergic": ["No lymphadenopathy"],
                        "severe_uncontrolled": ["No lymphadenopathy"],
                        "exercise_induced": ["No lymphadenopathy"]
                    }
                }
            },
            "respiratory_system": {
                "inspection": {
                    "accessory_muscles": {
                        "mild_allergic": ["No accessory muscle use"],
                        "severe_uncontrolled": ["Supraclavicular retractions", "Intercostal retractions", "Use of sternocleidomastoid muscles"],
                        "exercise_induced": ["No accessory muscle use"]
                    },
                    "chest_shape_and_symmetry": {
                        "mild_allergic": ["Symmetric chest rise"],
                        "severe_uncontrolled": ["Barrel chest", "Symmetric chest rise"],
                        "exercise_induced": ["Symmetric chest rise"]
                    }
                },
                "palpation": {
                    "chest_expansion": {
                        "mild_allergic": ["Symmetric expansion"],
                        "severe_uncontrolled": ["Symmetric expansion", "Globally decreased expansion"],
                        "exercise_induced": ["Symmetric expansion"]
                    },
                    "tactile_fremitus": {
                        "mild_allergic": ["Normal tactile fremitus"],
                        "severe_uncontrolled": ["Decreased tactile fremitus", "Normal tactile fremitus"],
                        "exercise_induced": ["Normal tactile fremitus"]
                    }
                },
                "percussion": {
                    "mild_allergic": ["Resonant"],
                    "severe_uncontrolled": ["Hyper-resonant", "Resonant"],
                    "exercise_induced": ["Resonant"]
                },
                "auscultation": {
                    "breath_sounds_intensity": {
                        "mild_allergic": ["Vesicular sounds, normal intensity"],
                        "severe_uncontrolled": ["Decreased breath sounds", "Vesicular sounds, normal intensity"],
                        "exercise_induced": ["Vesicular sounds, normal intensity"]
                    },
                    "adventitious_sounds": {
                        "mild_allergic": ["No adventitious sounds", "Wheezing"],
                        "severe_uncontrolled": ["Wheezing", "Rhonchi"],
                        "exercise_induced": ["No adventitious sounds"]
                    }
                }
            },
            "cardiovascular_system": {
                "JVP_assessment": {
                    "mild_allergic": ["JVP not elevated"],
                    "severe_uncontrolled": ["JVP not elevated"],
                    "exercise_induced": ["JVP not elevated"]
                },
                "palpation": {
                    "precordial_palpation_heave_thrill": {
                        "mild_allergic": ["No heaves or thrills"],
                        "severe_uncontrolled": ["No heaves or thrills"],
                        "exercise_induced": ["No heaves or thrills"]
                    },
                    "pmi_assessment": {
                        "mild_allergic": ["PMI at 5th ICS MCL"],
                        "severe_uncontrolled": ["PMI at 5th ICS MCL", "PMI strictly unpalpable"],
                        "exercise_induced": ["PMI at 5th ICS MCL"]
                    }
                },
                "auscultation": {
                    "heart_sounds_s1_s2": {
                        "mild_allergic": ["Normal S1, S2"],
                        "severe_uncontrolled": ["Normal S1, S2"],
                        "exercise_induced": ["Normal S1, S2"]
                    },
                    "extra_sounds_s3_s4_murmurs": {
                        "mild_allergic": ["No extra sounds or murmurs"],
                        "severe_uncontrolled": ["No extra sounds or murmurs"],
                        "exercise_induced": ["No extra sounds or murmurs"]
                    }
                },
                "peripheral_pulses_and_extremities": {
                    "peripheral_pulses_symmetry_and_quality": {
                        "mild_allergic": ["Pulses 2+ and symmetric"],
                        "severe_uncontrolled": ["Pulses 2+ and symmetric", "Bounding pulses"],
                        "exercise_induced": ["Pulses 2+ and symmetric"]
                    },
                    "extremities_color_and_trophic_changes": {
                        "mild_allergic": ["No trophic changes"],
                        "severe_uncontrolled": ["No trophic changes"],
                        "exercise_induced": ["No trophic changes"]
                    },
                    "extremities_temperature_and_cap_refill": {
                        "mild_allergic": ["Warm, Capillary refill < 2 sec"],
                        "severe_uncontrolled": ["Warm, Capillary refill < 2 sec"],
                        "exercise_induced": ["Warm, Capillary refill < 2 sec"]
                    },
                    "extremities_edema": {
                        "mild_allergic": ["No edema"],
                        "severe_uncontrolled": ["No edema"],
                        "exercise_induced": ["No edema"]
                    }
                }
            },
            "abdominal_system": {
                "inspection": {
                    "mild_allergic": ["Flat, non-distended"],
                    "severe_uncontrolled": ["Flat, non-distended"],
                    "exercise_induced": ["Flat, non-distended"]
                },
                "auscultation": {
                    "bowel_sounds": {
                        "mild_allergic": ["Normoactive bowel sounds"],
                        "severe_uncontrolled": ["Normoactive bowel sounds"],
                        "exercise_induced": ["Normoactive bowel sounds"]
                    },
                    "vascular_bruits": {
                        "mild_allergic": ["No bruits"],
                        "severe_uncontrolled": ["No bruits"],
                        "exercise_induced": ["No bruits"]
                    }
                },
                "percussion": {
                    "general": {
                        "mild_allergic": ["Resonant"],
                        "severe_uncontrolled": ["Resonant"],
                        "exercise_induced": ["Resonant"]
                    },
                    "organ_borders": {
                        "mild_allergic": ["Normal liver span"],
                        "severe_uncontrolled": ["Normal liver span"],
                        "exercise_induced": ["Normal liver span"]
                    }
                },
                "palpation": {
                    "superficial_tenderness": {
                        "mild_allergic": ["Soft, non-tender"],
                        "severe_uncontrolled": ["Soft, non-tender"],
                        "exercise_induced": ["Soft, non-tender"]
                    },
                    "deep_masses_and_organs": {
                        "mild_allergic": ["No masses or organomegaly"],
                        "severe_uncontrolled": ["No masses or organomegaly"],
                        "exercise_induced": ["No masses or organomegaly"]
                    }
                },
                "peritoneal_signs": {
                    "mild_allergic": ["None"],
                    "severe_uncontrolled": ["None"],
                    "exercise_induced": ["None"]
                }
            },
            "neurological": {
                "mental_status_and_LOC": {
                    "mild_allergic": ["Alert and Oriented"],
                    "severe_uncontrolled": ["Alert and Oriented", "Agitated"],
                    "exercise_induced": ["Alert and Oriented"]
                },
                "cranial_nerves": {
                    "mild_allergic": ["Intact"],
                    "severe_uncontrolled": ["Intact"],
                    "exercise_induced": ["Intact"]
                },
                "motor_strength_and_tone": {
                    "mild_allergic": ["5/5 strength globally"],
                    "severe_uncontrolled": ["5/5 strength globally"],
                    "exercise_induced": ["5/5 strength globally"]
                },
                "involuntary_movements": {
                    "mild_allergic": ["None"],
                    "severe_uncontrolled": ["None", "Flapping tremor"],
                    "exercise_induced": ["None"]
                },
                "sensory_light_touch_and_pain": {
                    "mild_allergic": ["Intact"],
                    "severe_uncontrolled": ["Intact"],
                    "exercise_induced": ["Intact"]
                },
                "deep_tendon_reflexes": {
                    "mild_allergic": ["2+"],
                    "severe_uncontrolled": ["2+"],
                    "exercise_induced": ["2+"]
                },
                "coordination_and_gait": {
                    "mild_allergic": ["Intact"],
                    "severe_uncontrolled": ["Intact"],
                    "exercise_induced": ["Intact"]
                }
            },
            "musculoskeletal_system": {
                "inspection": {
                    "joints": {
                        "mild_allergic": ["Normal joints"],
                        "severe_uncontrolled": ["Normal joints"],
                        "exercise_induced": ["Normal joints"]
                    },
                    "muscles": {
                        "mild_allergic": ["Normal bulk"],
                        "severe_uncontrolled": ["Normal bulk", "Muscle wasting"],
                        "exercise_induced": ["Normal bulk"]
                    }
                },
                "palpation": {
                    "tenderness_and_crepitus": {
                        "mild_allergic": ["No tenderness"],
                        "severe_uncontrolled": ["No tenderness", "Chest wall tenderness"],
                        "exercise_induced": ["No tenderness"]
                    }
                },
                "range_of_motion_active_passive": {
                    "mild_allergic": ["Full"],
                    "severe_uncontrolled": ["Full"],
                    "exercise_induced": ["Full"]
                },
                "stability_and_function": {
                    "mild_allergic": ["Stable"],
                    "severe_uncontrolled": ["Stable"],
                    "exercise_induced": ["Stable"]
                }
            }
            },
        "paraclinic": {
            "basic_blood_tests": {
                "BMP": {
                    "Na": {
                        "mild_allergic": [{"min": 135, "max": 145}],
                        "severe_uncontrolled": [{"min": 135, "max": 145}],
                        "exercise_induced": [{"min": 135, "max": 145}]
                    },
                    "BUN": {
                        "mild_allergic": [{"min": 7, "max": 20}],
                        "severe_uncontrolled": [{"min": 7, "max": 20}],
                        "exercise_induced": [{"min": 7, "max": 20}]
                    },
                    "Cr": {
                        "mild_allergic": [{"min": 0.7, "max": 1.1}],
                        "severe_uncontrolled": [{"min": 0.7, "max": 1.1}],
                        "exercise_induced": [{"min": 0.7, "max": 1.1}]
                    }
                },
                "CBC": {
                    "WBC": {
                        "mild_allergic": [{"min": 4500, "max": 10000}],
                        "severe_uncontrolled": [{"min": 5000, "max": 11000}],
                        "exercise_induced": [{"min": 4500, "max": 10000}]
                    },
                    "Hb": {
                        "mild_allergic": [{"min": 13.5, "max": 16.5}],
                        "severe_uncontrolled": [{"min": 14.0, "max": 17.0}],
                        "exercise_induced": [{"min": 13.5, "max": 16.5}]
                    },
                    "Plt": {
                        "mild_allergic": [{"min": 150000, "max": 400000}],
                        "severe_uncontrolled": [{"min": 150000, "max": 400000}],
                        "exercise_induced": [{"min": 150000, "max": 400000}]
                    }
                },
                "ESR": {
                    "mild_allergic": [{"min": 0, "max": 15}],
                    "severe_uncontrolled": [{"min": 5, "max": 25}],
                    "exercise_induced": [{"min": 0, "max": 15}]
                },
                "CRP": {
                    "mild_allergic": [{"min": 0, "max": 3}],
                    "severe_uncontrolled": [{"min": 0, "max": 10}],
                    "exercise_induced": [{"min": 0, "max": 3}]
                },
                "VBG": {
                    "pH": {
                        "mild_allergic": [{"min": 7.35, "max": 7.45}],
                        "severe_uncontrolled": [{"min": 7.42, "max": 7.48}],
                        "exercise_induced": [{"min": 7.35, "max": 7.45}]
                    },
                    "PCO2": {
                        "mild_allergic": [{"min": 35, "max": 45}],
                        "severe_uncontrolled": [{"min": 32, "max": 38}],
                        "exercise_induced": [{"min": 35, "max": 45}]
                    },
                    "HCO3": {
                        "mild_allergic": [{"min": 22, "max": 26}],
                        "severe_uncontrolled": [{"min": 22, "max": 26}],
                        "exercise_induced": [{"min": 22, "max": 26}]
                    }
                },
                "LFTs": {
                    "ALT": {
                        "mild_allergic": [{"min": 10, "max": 40}],
                        "severe_uncontrolled": [{"min": 10, "max": 40}],
                        "exercise_induced": [{"min": 10, "max": 40}]
                    },
                    "AST": {
                        "mild_allergic": [{"min": 10, "max": 40}],
                        "severe_uncontrolled": [{"min": 10, "max": 40}],
                        "exercise_induced": [{"min": 10, "max": 40}]
                    }
                }
            },
            "specialized_lung_tests": {
                "D_dimer": {
                    "mild_allergic": ["Negative"],
                    "severe_uncontrolled": ["Negative"],
                    "exercise_induced": ["Negative"]
                },
                "Sputum_AFB": {
                    "mild_allergic": ["Negative"],
                    "severe_uncontrolled": ["Negative"],
                    "exercise_induced": ["Negative"]
                },
                "BNP_NT_proBNP": {
                    "mild_allergic": ["Normal"],
                    "severe_uncontrolled": ["Normal"],
                    "exercise_induced": ["Normal"]
                },
                "Sputum_analysis": {
                    "Gram_Stain": {
                        "mild_allergic": ["Normal flora", "Mixed flora"],
                        "severe_uncontrolled": ["Normal flora", "Mixed flora"],
                        "exercise_induced": ["Normal flora"]
                    },
                    "Sample_Quality": {
                        "mild_allergic": ["Adequate"],
                        "severe_uncontrolled": ["Adequate"],
                        "exercise_induced": ["Adequate"]
                    }
                },
                "a1_antitrypsin_level": {
                    "mild_allergic": ["Normal range"],
                    "severe_uncontrolled": ["Normal range"],
                    "exercise_induced": ["Normal range"]
                }
            },
            "immunity_and_serology": {
                "HIV_test": {
                    "mild_allergic": ["Negative"],
                    "severe_uncontrolled": ["Negative"],
                    "exercise_induced": ["Negative"]
                },
                "Autoimmune_pannel_ANA_ANCA": {
                    "mild_allergic": ["Negative"],
                    "severe_uncontrolled": ["Negative"],
                    "exercise_induced": ["Negative"]
                }
            },
            "simple_imaging": {
                "Chest_X_Ray": {
                    "PA_Lateral_Findings_and_Effusion": {
                        "mild_allergic": ["Normal"],
                        "severe_uncontrolled": ["Hyperinflation", "Bronchial wall thickening"],
                        "exercise_induced": ["Normal"]
                    }
                }
            },
            "advanced_imaging": {
                "Chest_CT_CTPA": {
                    "Lung_Parenchyma_and_Pleura": {
                        "mild_allergic": ["Normal"],
                        "severe_uncontrolled": ["Air trapping", "Bronchial thickening", "Normal"],
                        "exercise_induced": ["Normal"]
                    }
                }
            },
            "functional_tests": {
                "dlco": {
                    "mild_allergic": ["Normal"],
                    "severe_uncontrolled": ["Normal"],
                    "exercise_induced": ["Normal"]
                },
                "peak_flow": {
                    "mild_allergic": ["Normal range", "Mild reduction"],
                    "severe_uncontrolled": ["Reduced", "Significantly reduced"],
                    "exercise_induced": ["Normal range"]
                },
                "Spirometry": {
                    "Result": {
                        "FEV1": {
                            "mild_allergic": [{"min": 80, "max": 95}],
                            "severe_uncontrolled": [{"min": 50, "max": 65}],
                            "exercise_induced": [{"min": 85, "max": 100}]
                        },
                        "FVC": {
                            "mild_allergic": [{"min": 80, "max": 100}],
                            "severe_uncontrolled": [{"min": 75, "max": 90}],
                            "exercise_induced": [{"min": 85, "max": 100}]
                        },
                        "FEV1/FVC": {
                            "mild_allergic": [{"min": 70, "max": 80}],
                            "severe_uncontrolled": [{"min": 55, "max": 69}],
                            "exercise_induced": [{"min": 75, "max": 85}]
                        }
                    },
                    "reversibility": {
                        "mild_allergic": ["Significant reversibility"],
                        "severe_uncontrolled": ["Significant reversibility"],
                        "exercise_induced": ["No significant reversibility at rest"]
                    }
                },
                "plethysmography": {
                    "mild_allergic": ["Normal lung volumes"],
                    "severe_uncontrolled": ["Increased TLC and RV"],
                    "exercise_induced": ["Normal lung volumes"]
                }
            },
            "procedures": {
                "Bronchoscopy": {
                    "mild_allergic": ["N/A"],
                    "severe_uncontrolled": ["N/A"],
                    "exercise_induced": ["N/A"]
                },
                "torachonthesis": {
                    "Serum": {
                        "Protein": {
                            "mild_allergic": ["N/A"],
                            "severe_uncontrolled": ["N/A"],
                            "exercise_induced": ["N/A"]
                        },
                        "LDH": {
                            "mild_allergic": ["N/A"],
                            "severe_uncontrolled": ["N/A"],
                            "exercise_induced": ["N/A"]
                        },
                        "Albumin": {
                            "mild_allergic": ["N/A"],
                            "severe_uncontrolled": ["N/A"],
                            "exercise_induced": ["N/A"]
                        }
                    },
                    "Fluid": {
                        "Protein": {
                            "mild_allergic": ["N/A"],
                            "severe_uncontrolled": ["N/A"],
                            "exercise_induced": ["N/A"]
                        },
                        "LDH": {
                            "mild_allergic": ["N/A"],
                            "severe_uncontrolled": ["N/A"],
                            "exercise_induced": ["N/A"]
                        },
                        "Albumin": {
                            "mild_allergic": ["N/A"],
                            "severe_uncontrolled": ["N/A"],
                            "exercise_induced": ["N/A"]
                        }
                    }
                }
            }
        }
        }
    
    
    def __init__(self):
        self.random = random
        
        # 1. SCENARIO SELECTION
        # mild_allergic (80%), severe_uncontrolled (10%), exercise_induced (10%)
        self.scenario = self.random.choices(
            ["mild_allergic", "severe_uncontrolled", "exercise_induced"], 
            weights=[80, 10, 10], k=1
        )[0]
        
    # --- Helper to extract data from DATA_SOURCE ---
    def _get_val(self, category, system, key, subkey=None, subsubkey=None):
        """
        این متد داده مربوط به سناریوی جاری را از دیکشنری استخراج می‌کند.
        اگر داده لیست رشته باشد -> random.choice
        اگر داده لیست بازه عددی باشد -> random between min/max
        """
        try:
            node = self.DATA_SOURCE[category][system][key]
            if subkey:
                node = node[subkey]
            if subsubkey:
                node = node[subsubkey]
                
            # دسترسی به سناریوی خاص
            scenario_data = node[self.scenario]
            
            # اگر لیست خالی یا رشته ساده است
            if not isinstance(scenario_data, list):
                return scenario_data
            
            # بررسی نوع داده داخل لیست
            first_item = scenario_data[0]
            
            if isinstance(first_item, dict) and "min" in first_item:
                # حالت بازه عددی: [{"min": x, "max": y}]
                # اگر لیست چندتایی باشد (مثل BP که دو بازه دارد)، یکی را برنمی‌گردانیم، بلکه لیست را برمی‌گردانیم تا caller مدیریت کند
                # اما معمولا در این ساختار caller انتظار مقدار دارد. 
                # برای BP منطق جداگانه می‌نویسیم یا اینجا هندل می‌کنیم.
                # فرض: اگر یک آیتم باشد -> مقدار برگردان. اگر بیشتر -> لیست برگردان
                if len(scenario_data) == 1:
                    r = scenario_data[0]
                    val = self.random.uniform(r["min"], r["max"])
                    # اگر اعداد صحیح هستند (مثل ضربان قلب)، int کن
                    if isinstance(r["min"], int) and isinstance(r["max"], int):
                        return int(val)
                    return round(val, 1)
                else:
                    # برای BP که دو تا دیکشنری دارد
                    results = []
                    for r in scenario_data:
                        val = self.random.uniform(r["min"], r["max"])
                        if isinstance(r["min"], int) and isinstance(r["max"], int):
                            results.append(int(val))
                        else:
                            results.append(round(val, 1))
                    return results

            elif isinstance(first_item, str):
                # حالت انتخاب رشته: ["A", "B"]
                return self.random.choice(scenario_data)
                
        except Exception as e:
            return f"Error: {str(e)}"

    # --- Demographic Helpers (No changes) ---
    def _select_occupation(self, gender, age_str):
        age = int(age_str.split()[0])
        if age > 60:
            return "بازنشسته"
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
        age_num = self.random.randint(20, 55) 
        age_str = f"{age_num}"
        
        name_key = "MALE" if gender == "مرد" else "FEMALE"
        first_name = self.random.choice(self.RANDOM_DATA_LISTS["first_names_sample_100"][name_key])
        last_name = self.random.choice(self.RANDOM_DATA_LISTS["last_names_sample_100"])
        
        occupation = self._select_occupation(gender, age_str)
        birth = self.random.choice(self.RANDOM_DATA_LISTS["famous_cities_sample_30"])
        residence = self._select_place_of_residence(birth)
        marital = self.random.choices(["متأهل", "مجرد"], weights=[60, 40], k=1)[0]
        
        return {
            "first_name": first_name, "last_name": last_name, "age": age_str,
            "gender": gender, "occupation": occupation,
            "place_of_birth": birth, "place_of_residence": residence,
            "marital_status": marital
        }

    # --- 1. Vital Signs ---
    def _gen_vitals(self):
        cat = "physical_exam"
        sys = "vital_signs"
        
        bp_raw = self._get_val(cat, sys, "BP") # Returns [sys, dia]
        temp = self._get_val(cat, sys, "T")
        pr = self._get_val(cat, sys, "PR")
        rr = self._get_val(cat, sys, "RR")
        spo2 = self._get_val(cat, sys, "SpO2")
        gcs = self._get_val(cat, sys, "GCS")

        return {
            "BP": f"{bp_raw[0]}/{bp_raw[1]} mmHg",
            "T": f"{temp} °C",
            "PR": f"{pr} bpm",
            "RR": f"{rr} breaths/min",
            "SpO2": f"{spo2}% (Room Air)",
            "GCS": str(gcs)
        }

    # --- 2. General Appearance ---
    def _gen_general_appearance(self):
        cat = "physical_exam"
        sys = "general_appearance"
        
        mood = self._get_val(cat, sys, "mood_and_behavior")
        overall = self._get_val(cat, sys, "overall_appearance")
        posture = self._get_val(cat, sys, "posture_and_position")
        loc = self._get_val(cat, sys, "level_of_consciousness")
        
        # Cardio/Pulm Clues Sub-dict
        edema = self._get_val(cat, sys, "cardiopulmonary_and_circulatory_clues", "edema")
        dyspnea = self._get_val(cat, sys, "cardiopulmonary_and_circulatory_clues", "dyspnea")
        cyanosis = self._get_val(cat, sys, "cardiopulmonary_and_circulatory_clues", "cyanosis")

        return {
            "mood_and_behavior": mood,
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

    # --- 4. Respiratory System ---
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

    # --- 5. Cardiovascular System ---
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
                "peripheral_pulses_symmetry_and_quality": self._get_val(cat, sys, "peripheral_pulses_and_extremities", "peripheral_pulses_symmetry_and_quality"),
                "extremities_color_and_trophic_changes": self._get_val(cat, sys, "peripheral_pulses_and_extremities", "extremities_color_and_trophic_changes"),
                "extremities_temperature_and_cap_refill": self._get_val(cat, sys, "peripheral_pulses_and_extremities", "extremities_temperature_and_cap_refill"),
                "extremities_edema": self._get_val(cat, sys, "peripheral_pulses_and_extremities", "extremities_edema")
            }
        }

    # --- 6. Abdominal System ---
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
                "deep_masses_and_organs": self._get_val(cat, sys, "palpation", "deep_masses_and_organs"),
                "peritoneal_signs": self._get_val(cat, sys, "peritoneal_signs")
            }
        }

    # --- 7. Neurological ---
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

    # --- 8. Musculoskeletal ---
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

    # --- 9. Paraclinic Tests ---
    def _gen_paraclinic(self):
        cat = "paraclinic"
        
        # --- Basic Blood Tests ---
        sys = "basic_blood_tests"
        
        # BMP
        na = self._get_val(cat, sys, "BMP", "Na")
        bun = self._get_val(cat, sys, "BMP", "BUN")
        cr = self._get_val(cat, sys, "BMP", "Cr")
        
        # CBC
        wbc = self._get_val(cat, sys, "CBC", "WBC")
        hb = self._get_val(cat, sys, "CBC", "Hb")
        plt = self._get_val(cat, sys, "CBC", "Plt")
        
        esr = self._get_val(cat, sys, "ESR")
        crp = self._get_val(cat, sys, "CRP")
        
        # VBG
        ph = self._get_val(cat, sys, "VBG", "pH")
        pco2 = self._get_val(cat, sys, "VBG", "PCO2")
        hco3 = self._get_val(cat, sys, "VBG", "HCO3")
        
        # LFTs
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
        # The text file provides %Predicted ranges. We need to format it nicely.
        # Predicted Values (Constants for simulation)
        P_FEV1 = 3.50
        P_FVC = 4.00
        
        fev1_pct = self._get_val(cat, sys, "Spirometry", "Result", "FEV1")
        fvc_pct = self._get_val(cat, sys, "Spirometry", "Result", "FVC")
        ratio_pct = self._get_val(cat, sys, "Spirometry", "Result", "FEV1/FVC")
        
        # Calculate Measured based on random %Predicted
        fev1_meas = round(P_FEV1 * (fev1_pct / 100), 2)
        fvc_meas = round(P_FVC * (fvc_pct / 100), 2)
        # Ratio is a percentage in itself in the source (e.g., 70-80), so we use it directly as the value
        ratio_meas = round(ratio_pct / 100, 2)
        
        fev1_out = f"Measured: {fev1_meas} L, Predicted: {P_FEV1} L, %Predicted: {fev1_pct}%"
        fvc_out = f"Measured: {fvc_meas} L, Predicted: {P_FVC} L, %Predicted: {fvc_pct}%"
        ratio_out = f"Value: {ratio_meas} ({ratio_pct}%)"
        
        reversibility = self._get_val(cat, sys, "Spirometry", "reversibility")

        # --- Procedures ---
        sys = "procedures"
        bronch = self._get_val(cat, sys, "Bronchoscopy")
        # Thoracentesis is  for all, so just hardcoding or generic fetch
        thorac_serum_prot = self._get_val(cat, sys, "torachonthesis", "Serum", "Protein")

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
                "torachonthesis": {
                    "result": "Not Indicated",
                    "Serum": {
                        "Protein": "N/A",
                        "LDH": "N/A",
                        "Albumin": "N/A"
                    },
                    "Fluid": {
                        "Protein": "N/A",
                        "LDH": "N/A",
                        "Albumin": "N/A"
                    }
                }
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
        
        return data, self.scenario
    