from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json

OPTIMAL_SCENARIO = {
  "history_taking": {
    "present_illness": {
      "question1": "True",
      "question2": "True",
      "question3": "True",
      "question4": "True",
      "question5": "True",
      "question6": "False",
      "question7": "False",
      "question8": "True",
      "question9": "True",
      "question10": "True"
    },
    "medical_history": {
      "question1": {
        "question1a": "True",
        "question1b": "True"
      },
      "question2": {
        "question2a": "False",
        "question2b": "False"
      },
      "question3": "True",
      "question4": "True",
      "question5": "False",
      "question6": "True"
    },
    "drug_history": {
      "question1": {
        "question1a": "True",
        "question1b": "True",
        "question1c": "True"
      },
      "question2": "False"
    },
    "allergies": {
      "question1": {
        "question1a": "False",
        "question1b": "False"
      }
    },
    "family_history": {
      "question1": {
        "question1a": "True",
        "question1b": "True"
      },
      "question2": "True",
      "question3": {
        "question3a": "True",
        "question3b": "True"
      }
    },
    "social_history": {
      "question1": {
        "question1a": "True",
        "question1b": "True"
      },
      "question2": "False",
      "question3": {
        "question3a": "False",
        "question3b": "False"
      },
      "question4": "False"
    },
    "ROS": {
      "question1": "True",
      "question2": "False",
      "question3": "False",
      "question4": "False",
      "question5": "False",
      "question6": "True",
      "question7": "True",
      "question8": "False",
      "question9": "False",
      "question10": "False",
      "question11": "False",
      "question12": "False",
      "question13": "False",
      "question14": "False"
    }
  },
  "physical_exam": {
    "general_appearance": {
      "level_of_consciousness_mood_and_behavior": {
        "level_of_consciousness": "True",
        "mood": "True",
        "behavior": "True"
      },
      "posture_and_position": {
        "position_of_comfort": "True"
      },
      "overall_appearance": {
        "nutritional_status": "True"
      },
      "cardiopulmonary_and_circulatory_clues": {
        "cyanosis": "True",
        "dyspnea": "True",
        "edema": "True"
      }
    },
    "head_and_neck": {
      "head_and_face": {
        "symmetry_and_lesions": "False",
        "tenderness": "False"
      },
      "eyes": {
        "sclera_and_conjunctiva": "False",
        "pupils_reaction": "False",
        "extraocular_movements": "False"
      },
      "ears": {
        "external_and_tenderness": "False",
        "eardrum_appearance": "False"
      },
      "nose_and_sinuses": {
        "septum_and_discharge": "False",
        "sinus_tenderness": "False"
      },
      "mouth_and_pharynx": {
        "oral_mucosa_and_lesions": "False",
        "pharynx_and_tonsils": "False"
      },
      "neck_and_lymphatics": {
        "inspection": "False",
        "tracheal_position": "False",
        "thyroid_gland": "False",
        "carotid_bruit": "False",
        "lymph_nodes_size_consistency": "False",
        "lymph_nodes_mobility_tenderness": "False"
      }
    },
    "respiratory_system": {
      "inspection": {
        "accessory_muscles": "True",
        "chest_shape_and_symmetry": "True"
      },
      "palpation": {
        "chest_expansion": "True",
        "tactile_fremitus": "True"
      },
      "percussion": "True",
      "auscultation": {
        "breath_sounds_intensity": "True",
        "adventitious_sounds": "True"
      }
    },
    "cardiovascular_system": {
      "JVP_assessment": "True",
      "palpation": {
        "precordial_palpation_heave_thrill": "False",
        "pmi_assessment": "False"
      },
      "auscultation": {
        "heart_sounds_s1_s2": "True",
        "extra_sounds_s3_s4_murmurs": "False"
      },
      "peripheral_pulses_and_extremities": {
        "peripheral_pulses_symmetry_and_quality": "True",
        "extremities_color_and_trophic_changes": "True",
        "extremities_temperature_and_cap_refill": "False",
        "extremities_edema": "True"
      }
    },
    "abdominal_system": {
      "inspection": "False",
      "auscultation": {
        "bowel_sounds": "False",
        "vascular_bruits": "False"
      },
      "percussion": {
        "general": "False",
        "organ_borders": "False"
      },
      "palpation": {
        "superficial_tenderness": "False",
        "deep_masses_and_organs": "False",
        "peritoneal_signs": "False"
      }
    },
    "neurological": {
      "mental_status_and_LOC": "False",
      "cranial_nerves": "False",
      "motor_strength_and_tone": "False",
      "involuntary_movements": "False",
      "sensory_light_touch_and_pain": "False",
      "deep_tendon_reflexes": "False",
      "coordination_and_gait": "False"
    },
    "musculoskeletal_system": {
      "inspection": {
        "joints": "False",
        "muscles": "False"
      },
      "palpation": {
        "tenderness_and_crepitus": "False"
      },
      "range_of_motion_active_passive": "False",
      "stability_and_function": "False"
    }
  },
  "paraclinic": {
    "basic_blood_tests": {
      "CBC": "True",
      "ESR/CRP": "True",
      "BMP": "False",
      "LFTs": "False",
      "VBG": "True"
    },
    "specialized_lung_tests": {
      "Sputum_analysis": "False",
      "Sputum_AFB": "False",
      "a1_antitrypsin_level": "True",
      "D_dimer": "False",
      "BNP/NT_proBNP": "True"
    },
    "immunity_and_serology": {
      "HIV_test": "False",
      "Autoimmune_pannel_ANA_ANCA": "False"
    },
    "simple_imaging": {
      "Chest_X_Ray": {
        "PA": "True",
        "Lateral": "True"
      }
    },
    "advanced_imaging": {
      "Chest_CT_CTPA": "True",
      "MRI_chest": "False",
      "Pet_scan": "False"
    },
    "functional_tests": {
      "Spirometry": "True",
      "peak_flow": "True",
      "plethysmography": "True"
    },
    "procedures": {
      "Bronchoscopy": "False",
      "torachonthesis": "False"
    }
  },
  "differential_diagnosis": {
    "disease1": "True",
    "disease2": "False",
    "disease3": "True",
    "disease4": "False",
    "disease5": "True",
    "disease6": "True",
    "disease7": "False",
    "disease8": "False"
  }
}

STUDENT_LOG = {
    "history_taking": {
        "present_illness": {
            "question1": "15:00",
            "question2": "False",
            "question3": "14:00",
            "question4": "False",
            "question5": "False",
            "question6": "False",
            "question7": "False",
            "question8": "13:00",
            "question9": "False",
            "question10": "False"
        },
        "medical_history": {
            "question1": {
                    "question1a": "14:30",
                    "question1b": "14:35"
                },
            "question2": {
                    "question2a": "False",
                    "question2b": "False"
                },
            "question3": "12:30",
            "question4": "False",
            "question5": "False",
            "question6": "False"
        },
        "drug_history": {
            "question1": {
                    "question1a": "False",
                    "question1b": "False",
                    "question1c": "False"
                },
            "question2": "False"
        },
        "allergies": {
            "question1": {
                "question1a": "False",
                "question1b": "False"
            }
        },
        "family_history": {
            "question1": {
                    "question1a": "False",
                    "question1b": "False"
                },
            "question2": "False",
            "question3": {
                "question3a": "False",
                "question3b": "False"
            }
        },
        "social_history": {
            "question1": {
                    "question1a": "False",
                    "question1b": "False"
                },
            "question2": "False",
            "question3": {
                    "question3a": "False",
                    "question3b": "False"
                },
            "question4": "False"
        },
        "ROS": {
            "question1": "False",
            "question2": "False",
            "question3": "False",
            "question4": "False",
            "question5": "False",
            "question6": "False",
            "question7": "False",
            "question8": "False",
            "question9": "False",
            "question10": "False",
            "question11": "False",
            "question12": "False",
            "question13": "False",
            "question14": "False"
        }
    },
    "physical_exam": {
        "general_appearance": {
            "level_of_consciousness_mood_and_behavior": {
                "level_of_consciousness": "False",
                "mood": "False",
                "behavior": "False"
            },
            "posture_and_position": {
                "position_of_comfort": "False"
            },
            "overall_appearance": {
                "nutritional_status": "False"
            },
            "cardiopulmonary_and_circulatory_clues": {
                "cyanosis": "False",
                "dyspnea": "False",
                "edema": "False"
            }
        },
        "head_and_neck": {
            "head_and_face": {
                "symmetry_and_lesions": "False",
                "tenderness": "ّFalse"
            },
            "eyes": {
                "sclera_and_conjunctiva": "False",
                "pupils_reaction": "ّFalse",
                "extraocular_movements": "False"
            },
            "ears": {
                "external_and_tenderness": "False",
                "eardrum_appearance": "ّFalse"
            },
            "nose_and_sinuses": {
                "septum_and_discharge": "False",
                "sinus_tenderness": "False"
            },
            "mouth_and_pharynx": {
                "oral_mucosa_and_lesions": "False",
                "pharynx_and_tonsils": "False"
            },
            "neck_and_lymphatics": {
                "inspection": "False",
                "tracheal_position": "False",
                "thyroid_gland": "False",
                "carotid_bruit": "False",
                "lymph_nodes_size_consistency": "False",
                "lymph_nodes_mobility_tenderness": "False"
            }
        },
        "respiratory_system": {
            "inspection": {
                "accessory_muscles": "12:00",
                "chest_shape_and_symmetry": "12:05"
            },
            "palpation": {
                "chest_expansion": "False",
                "tactile_fremitus": "False"
            },
            "percussion": "False",
            "auscultation": {
                "breath_sounds_intensity": "False",
                "adventitious_sounds": "11:30"
            }
        },
        "cardiovascular_system": {
            "JVP_assessment": "11:00",
            "palpation": {
                "precordial_palpation_heave_thrill": "False",
                "pmi_assessment": "False"
            },
            "auscultation": {
                "heart_sounds_s1_s2": "False",
                "extra_sounds_s3_s4_murmurs": "False"
            },
            "peripheral_pulses_and_extremities": {
                "peripheral_pulses_symmetry_and_quality": "False",
                "extremities_color_and_trophic_changes": "False",
                "extremities_temperature_and_cap_refill": "False",
                "extremities_edema": "False"
            },
            "abdominal_system": {
                "inspection": "False",
                "auscultation": {
                    "bowel_sounds": "False",
                    "vascular_bruits": "False"
                },
                "percussion": {
                    "general": "False",
                    "organ_borders": "False"
                },
                "palpation": {
                    "superficial_tenderness": "False",
                    "deep_masses_and_organs": "False"
                },
                "peritoneal_signs": "False"
            }
        },
        "neurological": {
            "mental_status_and_LOC": "False",
            "cranial_nerves": "False",
            "motor_strength_and_tone": "False",
            "involuntary_movements": "False",
            "sensory_light_touch_and_pain": "False",
            "deep_tendon_reflexes": "False",
            "coordination_and_gait": "False"
        },
        "musculoskeletal_system": {
            "inspection": {
                "joints": "False",
                "muscles": "False"
            },
            "palpation": {
                "tenderness_and_crepitus": "False"
            },
            "range_of_motion_active_passive": "False",
            "stability_and_function": "False"
        }
    },
    "paraclinic": {
        "basic_blood_tests": {
            "CBC": {
                "Hb": "9:30", 
                "WBC": "False", 
                "Plt": "False"
            },
            "ESR/CRP": "False",
            "BMP": "False",
            "LFTs": "False",
            "VBG": "10:30"
        },
        "specialized_lung_tests": {
            "Sputum_analysis": "False",
            "Sputum_AFB": "False",
            "a1_antitrypsin_level": "06:15",
            "D_dimer": "False",
            "BNP_NT_proBNP": "10:15"
        },
        "immunity_and_serology": {
            "HIV_test": "False",
            "Autoimmune_pannel_ANA_ANCA": "False"
        },
        "simple_imaging": {
            "Chest_X_Ray": {
                "PA": "10:00",
                "Lateral": "10:05"
            }
        },
        "advanced_imaging": {
            "Chest_CT_CTPA": "False",
            "MRI_chest": "False",
            "Pet_scan": "False"
        },
        "functional_tests": {
            "Spirometry": "08:00",
            "peak_flow": "False",
            "plethysmography": "07:00"
        },
        "procedures": {
            "Bronchoscopy": "False",
            "torachonthesis": "False"
        }
    },
    "differential_diagnosis": {
        "disease1": "False",
        "disease2": "05:15",
        "disease3": "05:30",
        "disease4": "False",
        "disease5": "05:10",
        "disease6": "False",
        "disease7": "05:00",
        "disease8": "False"
    },
    "final_diagnosis": {
        "disease3": "02:00"
    }
}

FULL_SCENARIO = {
  "patient_profile": {
    "personal_information": {
      "first_name": "",
      "last_name": "",
      "age": "سن بیمار باید متناسب با شیوع بیماری انتخاب شود. در بیماری‌های مزمن تنفسی و قلبی معمولاً میانسالی تا سالمندی (حدود 45 تا 80 سال)، در بیماری‌های حاد یا ارثی ممکن است سن پایین‌تر باشد. برای تنوع، سن را در بازه منطقی بیماری انتخاب کن، نه مقدار ثابت.",
      "gender": "",
      "occupation": "",
      "place_of_birth": "",
      "place_of_residence": "",
      "marital_status": ""
    },
    "chief_complaint": "contains patient's main reason of visit and its onset time",
    "vital_sign": {
      "BP": "Blood Pressure",
      "T": "Temprature",
      "PR": "Pulse Rate",
      "RR": "Respiratory Rate",
      "SpO2": "Saturation of O2",
      "GCS": "Level of Consiousness"
    }
  },
  "history_taking": {
    "present_illness": {
      "question1": "علائم از چه زمانی شروع شدند و در طول زمان چه تغییری کردند؟",
      "question2": "شروع علائم ناگهانی بوده یا تدریجی؟ بعد از اتفاق خاصی مثل عفونت یا تماس خاصی شروع شد؟",
      "question3": "تنگی نفستون دائمیه یا دوره‌ای؟ و با فعالیت بدتر میشه یا در حالت استراحت هم وجود داره؟",
      "question4": "سرفه دارید؟ اگر بله، خشک است یا همراه با خلط؟ رنگ و حجم خلط چطور است؟",
      "question5": "تا حالا خس‌خس یا صدای غیرعادی در تنفس شنیدید؟",
      "question6": "احساس درد یا فشار در قفسه سینه دارید؟ با تنفس یا حرکت تغییر می‌کنه؟",
      "question7": "در روزهای اخیر تب، لرز یا تعریق شبانه داشتید؟ وجود یا عدم وجود تب باید با زمینهٔ بالینی هماهنگ باشد. در بیماری‌های مزمن پایدار معمولاً تب وجود ندارد، اما در تشدید حاد یا عفونت‌ها ممکن است تب و لرز مشاهده شود. پاسخ 'بله' یا 'خیر' را بر اساس ماهیت بیماری و مرحله آن تولید کن.",
      "question8": "تورم پا، تپش قلب یا احساس سبکی سر دارید؟",
      "question9": "قبلاً هم چنین حمله یا علائمی داشتید؟ چه درمانی کمکتون کرده؟",
      "question10": "احساس کاهش وزن، خستگی یا بی‌اشتهایی داشتید؟"
    },
    "medical_history": {
      "question1": {
        "question1a": "آیا بیماری طولانی مدت (مزمن) مثل قند (دیابت)، فشار خون، آسم، مشکل تیروئید، یا بیماری جدی کلیوی/کبدی دارید؟",
        "question1b": "اگر پاسخ question1a بله بود، تشخیص این بیماری از چه موقع بوده است؟"
      },
      "question2": {
        "question2a": "آیا تا به حال عمل جراحی (بزرگ یا کوچک) داشته‌اید؟ و آیا تا به حال در بیمارستان بستری شده‌اید؟",
        "question2b": "اگر پاسخ question2a بله بود، دلیلش چه بوده و در چه سالی؟ همچنین، آیا تا به حال انتقال خون داشته‌اید؟"
      },
      "question3": "آیا سابقه بیماری های قلبی، ریوی و مغزی را دارید؟",
      "question4": "آیا در حال حاظر یا در گذشته سرطان فعال داشته‌اید؟",
      "question5": "در دوران کودکی، آیا بیماری‌های خاصی (مثل تب روماتیسمی، سرخک شدید) گرفتید یا به دلیل بیماری بستری شدید؟",
      "question6": "برنامه واکسن‌ها (مثل کزاز و آنفولانزا) شما کامل و به روز است؟"
    },
    "drug_history": {
      "question1": {
        "question1a": "لطفاً لیست تمام داروهایی که در حال حاضر به صورت مرتب (روزانه، هفتگی یا ماهانه) مصرف می‌کنید را به من بگویید.",
        "question1b": "دوز هر دارو چقدر است و چند بار در روز مصرف می‌کنید؟",
        "question1c": "آیا در چند روز گذشته، دوز یا زمان مصرف هیچ‌کدام از این داروها را تغییر داده‌اید؟"
      },
      "question2": "به صورت منظم داروهای بدون نسخه (OTC) (مثل داروهای سرماخوردگی، مسکن‌ها، آنتی‌اسیدها)، مکمل‌های غذایی، داروهای گیاهی یا خواب آور مصرف می‌کنید؟"
    },
    "allergies": {
      "question1": {
        "question1a": "آیا به دارو، غذا، یا ماده خاصی آلرژی (حساسیت) دارید؟",
        "question1b": "اگر پاسخ question1a بله بود، دقیقاً چه دارو یا ماده‌ای است؟ و واکنش شما (مثل کهیر یا تنگی نفس) چگونه بوده است؟"
      }
    },
    "family_history": {
      "question1": {
        "question1a": "آیا در خانواده درجه یک (پدر، مادر، خواهر یا برادر) شما، سابقه ابتلا به بیماری‌های مزمن و شایع زیر وجود دارد؟",
        "question1b": "اگر پاسخ question1a بله بود، چه کسی و در چه سنی به آن مبتلا شده است؟"
      },
      "question2": "آیا در خانواده درجه یک شما، سابقه حمله قلبی (سکته قلبی)، سکته مغزی، یا نارسایی قلبی وجود دارد؟",
      "question3": {
        "question3a": "آیا سابقه سرطان خاصی در خانواده درجه یک شما وجود دارد؟",
        "question3b": "اگر پاسخ question3a بله بود، نوع سرطان چه بوده و در چه سنی تشخیص داده شده است؟"
      }
    },
    "social_history": {
      "question1": {
        "question1a": "آیا تا به حال سیگار، قلیان، پیپ، یا هر نوع محصول نیکوتینی مصرف کرده‌اید؟",
        "question1b": "اگر قبلاً مصرف می‌کردید، چه زمانی ترک کرده‌اید؟"
      },
      "question2": "آیا الکل مصرف می‌کنید؟ اگر بله، نوع و میزان مصرف آن در هفته چقدر است؟",
      "question3": {
        "question3a": "آیا تا به حال مواد مخدر مصرف کرده‌اید؟",
        "question3b": "اگر مصرف داشته‌اید، نوع آن و آخرین باری که مصرف کرده‌اید چه زمانی بوده است؟"
      },
      "question4": "در خانه همراه چه کسانی زندگی می‌کنید؟"
    },
    "ROS": {
      "question1": "آیا اخیراً دچار تب، لرز، کاهش یا افزایش وزن ناخواسته، یا خستگی شدید و غیرمعمول شده‌اید؟",
      "question2": "آیا سابقه راش، خارش، زخم‌های طولانی‌مدت، تغییر در رنگ یا بافت پوست/مو/ناخن، یا کبودی غیرعادی دارید؟",
      "question3": "آیا اخیراً دچار سردرد، سرگیجه، سفتی گردن، یا بزرگ شدن غدد لنفاوی در گردن شده‌اید؟",
      "question4": "آیا دچار تاری دید، دوبینی، درد چشم، قرمزی، یا کاهش دید ناگهانی شده‌اید؟",
      "question5": "آیا دچار وزوز گوش، کاهش شنوایی، خونریزی بینی، گرفتگی مزمن بینی، گلودرد مزمن، مشکل در بلع (دیسفاژی)، یا آفت و زخم‌های دهانی مکرر هستید؟",
      "question6": "آیا سابقه درد قفسه سینه، تپش قلب، تنگی نفس با فعالیت، تنگی نفس در حالت خوابیده (ارتوپنه)، یا تورم پاها (ادم) دارید؟",
      "question7": "آیا سابقه سرفه، خس‌خس سینه، خلط خونی (هموپتیزی)، یا تنگی نفس (به جز تنگی نفس مرتبط با فعالیت شدید) دارید؟",
      "question8": "آیا دچار حالت تهوع، استفراغ، سوزش سر دل، درد شکم، تغییر در عادات اجابت مزاج (اسهال یا یبوست)، خونریزی از مقعد، یا زردی پوست و چشم (یرقان) هستید؟",
      "question9": "آیا دچار درد یا سوزش حین ادرار کردن، تکرر ادرار، خون در ادرار (هماچوری)، مشکل در کنترل ادرار، یا ترشحات غیرعادی هستید؟",
      "question10": "آیا دچار درد مفاصل، سفتی صبحگاهی، تورم مفاصل، درد یا ضعف عضلانی، یا کمردرد مزمن هستید؟",
      "question11": "آیا سابقه سردرد شدید یا جدید، تشنج، ضعف یا بی‌حسی در دست‌ها/پاها، مشکل در تعادل/هماهنگی، یا تغییر در حافظه دارید؟",
      "question12": "آیا اخیراً احساس افسردگی، اضطراب، تغییرات شدید خلقی، یا مشکل در خواب (بی‌خوابی/پرخوابی) داشته‌اید؟",
      "question13": "آیا دچار افزایش تشنگی، افزایش گرسنگی، افزایش ادرار (پلی اوری)، یا عدم تحمل گرما/سرما شده‌اید؟",
      "question14": "آیا سابقه کبودی آسان، خونریزی طولانی‌مدت، بزرگ شدن غدد لنفاوی، یا کم‌خونی شدید دارید؟"
    }
  },
  "physical_exam": {
    "general_appearance": {
      "level_of_consciousness_mood_and_behavior": {
        "level_of_consciousness": "آیا بیمار هوشیار، گیج، خواب‌آلود (لتارژیک)، یا در حالت اغما (Comatose) است؟ آیا دستورات ساده را اجرا می‌کند؟",
        "mood": "آیا بیمار به نظر بیمار، مضطرب، یا در درد شدید است؟",
        "behavior": "آیا بیمار همکاری می‌کند؟ آیا مضطرب، افسرده، یا پرخاشگر است؟ آیا از نظر روانی وضعیت طبیعی دارد؟"
      },
      "posture_and_position": {
        "position_of_comfort": "آیا بیمار وضعیتی را برای کاهش درد یا تنگی نفس انتخاب کرده است؟"
      },
      "overall_appearance": {
        "nutritional_status": "آیا بیمار لاغر (Cachectic)، چاق (Obese)، یا در وضعیت وزن طبیعی است؟"
      },
      "cardiopulmonary_and_circulatory_clues": {
        "cyanosis": "بررسی لب‌ها، زبان و بستر ناخن برای علائم کبودی.",
        "dyspnea": "آیا بیمار به سختی نفس می‌کشد؟",
        "edema": "وجود تورم در پاها، مچ پا یا اطراف چشم."
      }
    },
    "head_and_neck": {
      "head_and_face": {
        "symmetry_and_lesions": "آیا سر و صورت بیمار متقارن است و شواهدی از زخم، توده یا ضایعات پوستی وجود دارد؟",
        "tenderness": "آیا در لمس جمجمه حساسیت به لمس یا درد وجود دارد؟"
      },
      "eyes": {
        "sclera_and_conjunctiva": "آیا در صلبیه (سفیدی چشم) زردی (یرقان) یا در ملتحمه (پلک پایین) رنگ‌پریدگی شدید (کم‌خونی) مشاهده می‌شود؟",
        "pupils_reaction": "آیا مردمک‌ها متقارن هستند و به نور واکنش طبیعی نشان می‌دهند؟",
        "extraocular_movements": "آیا حرکات چشمی در جهات مختلف کامل و هماهنگ هستند؟"
      },
      "ears": {
        "external_and_tenderness": "آیا لاله گوش یا ناحیه ماستوئید (پشت گوش) متورم، قرمز یا دردناک هستند؟",
        "eardrum_appearance": "آیا پرده صماخ در اتوسکوپی ظاهر طبیعی دارد (شفاف، بدون التهاب یا پارگی)؟"
      },
      "nose_and_sinuses": {
        "septum_and_discharge": "آیا تیغه بینی انحراف شدید دارد و آیا ترشحات غیرعادی (چرکی یا خونی) مشاهده می‌شود؟",
        "sinus_tenderness": "آیا در لمس یا دق بر روی سینوس‌های پیشانی و فکی (فرونتال و ماگزیلاری) درد وجود دارد؟"
      },
      "mouth_and_pharynx": {
        "oral_mucosa_and_lesions": "آیا مخاط دهان (لثه‌ها، زیر زبان) مرطوب و بدون ضایعات غیرعادی (زخم یا آفت) است؟",
        "pharynx_and_tonsils": "آیا حلق (گلو) قرمز یا متورم است و آیا لوزتین‌ها (Tonsils) بزرگ شده‌اند یا دارای ترشحات چرکی هستند؟"
      },
      "neck_and_lymphatics": {
        "inspection": "آیا در معاینه ظاهری گردن، تورم، قرمزی، توده، یا زخم قابل مشاهده‌ای وجود دارد؟",
        "tracheal_position": "آیا نای (Trachea) در خط وسط قرار دارد؟ آیا در لمس، انحراف یا جابه‌جایی نای (Tracheal Deviation) احساس می‌شود؟",
        "thyroid_gland": "آیا غده تیروئید (از پشت بیمار) بزرگ است (گواتر)؟ آیا در لمس، ندول (توده)، سفتی، یا حساسیت به لمس وجود دارد؟",
        "carotid_bruit": "آیا در سمع شریان‌های کاروتید، صدای وزوز (Bruit) شنیده می‌شود؟ (نشانه‌ی احتمالی تنگی شریان)",
        "lymph_nodes_size_consistency": "آیا غدد لنفاوی در نواحی مختلف (سرویکال، ساب‌ماندیبولار، سوپراکلاویکولار) بزرگ شده‌اند؟ (اندازه، قوام: نرم/سفت/لاستیکی)",
        "lymph_nodes_mobility_tenderness": "آیا غدد لنفاوی لمس شده، متحرک هستند یا ثابت و چسبیده به بافت زیرین؟ آیا در لمس، درد (Tenderness) دارند؟"
      }
    },
    "respiratory_system": {
      "inspection": {
        "accessory_muscles": "آیا از عضلات کمکی تنفس استفاده می‌کند؟",
        "chest_shape_and_symmetry": "آیا شکل قفسه سینه طبیعی است (بدون Barrel Chest یا کیفواسکولیوز) و حرکت قفسه سینه در دم و بازدم متقارن است؟"
      },
      "palpation": {
        "chest_expansion": "آیا توسعه قفسه سینه در هنگام دم عمیق، متقارن و کامل است؟",
        "tactile_fremitus": "آیا لرزش‌های صوتی (Tactile Fremitus) در دو طرف قفسه سینه متقارن و طبیعی هستند؟"
      },
      "percussion": "آیا صدای دق در تمام نواحی ریه رزونانس (طبیعی) است یا در برخی نواحی dullness یا hyperresonanse است؟ اگر بله در چه نواحی؟",
      "auscultation": {
        "breath_sounds_intensity": "آیا شدت صداهای تنفسی پایه طبیعی است یا کاهش یا عدم وجود صدا وجود دارد؟",
        "adventitious_sounds": "آیا صداهای اضافی (Adventitious Sounds) مانند کراکل (Crackles)، ویزینگ (Wheezing)، رونکای (Rhonchi) یا اصطکاک پلورال (Pleural Rub) شنیده می‌شوند؟"
      }
    },
    "cardiovascular_system": {
      "JVP_assessment": "آیا فشار وریدی ژوگولار (JVP) در وضعیت نیمه نشسته، بالا و غیرطبیعی است؟",
      "palpation": {
        "precordial_palpation_heave_thrill": "آیا در لمس ناحیه پره‌کوردیوم، لیفت (Lift)، هیو (Heave)، یا تریل (Thrill) احساس می‌شود؟",
        "pmi_assessment": "ضربان نوک قلب (PMI) در کجا لمس می‌شود (محل دقیق) و آیا اندازه و قدرت آن طبیعی است؟"
      },
      "auscultation": {
        "heart_sounds_s1_s2": "آیا صداهای اصلی قلب (S1 و S2) شنیده می‌شوند و از نظر شدت، اسپلیت و کیفیت، طبیعی هستند؟",
        "extra_sounds_s3_s4_murmurs": "آیا صداهای اضافی مانند S3، S4، مارمار (Murmur) یا صدای اصطکاک پریکاردیال شنیده می‌شود؟"
      },
      "peripheral_pulses_and_extremities": {
        "peripheral_pulses_symmetry_and_quality": "آیا تمام نبض‌های محیطی (مانند رادیال، فمورال، دورسالیس پدیس) در دو طرف بدن متقارن، منظم، و با کیفیت (قدرت) طبیعی لمس می‌شوند؟",
        "extremities_color_and_trophic_changes": "آیا در اندام‌های انتهایی، شواهدی از سیانوز (کبودی)، رنگ‌پریدگی، ریزش مو اندام، کلابینگ (Clubbing)، یا تغییرات تروفیک (مانند ریزش مو، نازکی پوست) مشاهده می‌شود؟",
        "extremities_temperature_and_cap_refill": "آیا اندام‌های انتهایی دمای طبیعی دارند و زمان پر شدن مجدد مویرگی (Capillary Refill Time) چند ثانیه است؟",
        "extremities_edema": "آیا در اندام‌های تحتانی، شواهدی از ادم (تورم) و به ویژه ادم گوده‌گذار (Pitting Edema) وجود دارد؟ اگر بله چند + است؟"
      }
    },
    "abdominal_system": {
      "inspection": "آیا شکم از نظر شکل (Flat, Rounded, Protuberant)، تقارن و وجود زخم/اسکار جراحی غیرطبیعی است؟",
      "auscultation": {
        "bowel_sounds": "آیا صداهای روده (Bowel Sounds) در سمع حضور دارند و فرکانس و شدت آن‌ها طبیعی است (Normoactive)؟ (یا Hyperactive/Hypoactive)",
        "vascular_bruits": "آیا در سمع آئورت یا شریان‌های کلیوی، صدای وزوز (Bruit) شنیده می‌شود؟"
      },
      "percussion": {
        "general": " یا dulness وجود داردآیا صدای غالب دق، تیمپانی (Tympany) است؟",
        "organ_borders": "آیا حدود کبد یا طحال در دق، غیرعادی است؟"
      },
      "palpation": {
        "superficial_tenderness": "آیا در لمس سطحی، حساسیت به لمس (Tenderness) موضعی یا عمومی وجود دارد؟",
        "deep_masses_and_organs": "آیا در لمس عمقی، توده (Mass) غیرعادی، بزرگی کبد (Hepatomegaly) یا طحال (Splenomegaly) احساس می‌شود؟"
      },
      "peritoneal_signs": "آیا علائم پریتونیت (مانند ریفاند تندرنس - Rebound Tenderness، یا سفتی غیرارادی عضلات - Guarding) وجود دارد؟"
    },
    "neurological": {
      "mental_status_and_LOC": "آیا سطح هوشیاری بیمار طبیعی است و از نظر زمان، مکان و شخص جهت‌یابی (Orientation) دارد؟",
      "cranial_nerves": "آیا عملکرد اعصاب کرانیال اصلی (مانند تقارن حرکات صورت، حرکات چشم و بلع) طبیعی است؟",
      "motor_strength_and_tone": "قدرت عضلانی در اندام‌های فوقانی و تحتانی چقدر است(با استفاده از مقیاس 0 تا 5)؟ و آیا تون عضلانی (سفتی/شلی) طبیعی است؟",
      "involuntary_movements": "آیا حرکات غیرارادی (مانند ترمور، تیک) یا آتروفی (Atrophy) عضلانی مشاهده می‌شود؟",
      "sensory_light_touch_and_pain": "آیا حس‌های لمس سبک و درد/دما در اندام‌ها، متقارن و بدون نقص هستند؟",
      "deep_tendon_reflexes": "آیا رفلکس‌های عمیق تاندونی (DTRs) در تمام اندام‌ها وجود دارند، متقارن هستند و شدت آن‌ها طبیعی است؟ (0 تا 4+)",
      "coordination_and_gait": "آیا تست‌های هماهنگی (مانند انگشت به بینی) نرمال هستند؟ و آیا الگوی راه رفتن (Gait) و تعادل بیمار طبیعی است و در غیر این صورت الگوی Gait بیمار چگونه است؟"
    },
    "musculoskeletal_system": {
      "inspection": {
        "joints": "آیا مفاصل از نظر تورم، قرمزی، بدشکلی (Deformity) یا آتروفی، ظاهر طبیعی دارند؟",
        "muscles": "آیا عضلات از نظر تورم، قرمزی، بدشکلی (Deformity) یا آتروفی، ظاهر طبیعی دارند؟"
      },
      "palpation": {
        "tenderness_and_crepitus": "آیا در لمس مفاصل و عضلات، حساسیت به لمس (Tenderness)، گرما، یا صدای ساییده شدن (Crepitus) احساس می‌شود؟"
      },
      "range_of_motion_active_passive": "آیا دامنه حرکتی (ROM) فعال و غیرفعال مفاصل اصلی (مانند شانه، زانو و هیپ) کامل و بدون درد است؟",
      "stability_and_function": "آیا مفاصل از نظر پایداری (Stability) طبیعی هستند و بیمار می‌تواند عملکرد حرکتی خود را به خوبی انجام دهد؟"
    }
  },
  "paraclinic": {
    "basic_blood_tests": {
      "CBC": ["Hb", "WBC", "Plt"],
      "ESR/CRP": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "BMP": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "LFTs": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "VBG": "نتایج تست بر اساس بیماری {disease} داده شود."
    },
    "specialized_lung_tests": {
      "Sputum_analysis": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "Sputum_AFB": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "a1_antitrypsin_level": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "D_dimer": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "BNP/NT_proBNP": "نتایج تست بر اساس بیماری {disease} داده شود."
    },
    "immunity_and_serology": {
      "HIV_test": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "Autoimmune_pannel_ANA_ANCA": "نتایج تست بر اساس بیماری {disease} داده شود."
    },
    "simple_imaging": {
      "Chest_X_Ray": {
        "PA": "در صورت diagnostic نبودن برای بیماری {disease}: رادیولوژیست نمی داند شما چرا درخواست CXR داده اید! با این حال نتایج نرمال هستند. در صورت diagnostic بودن تفسیر یک CXR تیپیک برای بیماری {disease} را خروجی بده.",
        "Lateral": "در صورت diagnostic نبودن برای بیماری {disease}: رادیولوژیست نمی داند شما چرا درخواست CXR داده اید! با این حال نتایج نرمال هستند. در صورت diagnostic بودن تفسیر یک CXR تیپیک برای بیماری {disease} را خروجی بده."
      }
    },
    "advanced_imaging": {
      "Chest_CT_CTPA": "در صورت diagnostic نبودن برای بیماری {disease}: رادیولوژیست نمی داند شما چرا درخواست CT داده اید! با این حال نتایج نرمال هستند. در صورت diagnostic بودن تفسیر یک CT تیپیک برای بیماری {disease} را خروجی بده.",
      "MRI_chest": "در صورت diagnostic نبودن برای بیماری {disease}: رادیولوژیست نمی داند شما چرا درخواست MRI داده اید! با این حال نتایج نرمال هستند. در صورت diagnostic بودن تفسیر یک MRI تیپیک برای بیماری {disease} را خروجی بده.",
      "Pet_scan": "در صورت diagnostic نبودن برای بیماری {disease}: رادیولوژیست نمی داند شما چرا درخواست Pet scan داده اید! با این حال نتایج نرمال هستند. در صورت diagnostic بودن تفسیر یک Pet scan تیپیک برای بیماری {disease} را خروجی بده."
    },
    "functional_tests": {
      "Spirometry": "در صورت diagnostic بودن تفسیر یک Spirometry تیپیک برای بیماری {disease} را خروجی بده.",
      "peak_flow": "در صورت diagnostic بودن تفسیر یک peak flow تیپیک برای بیماری {disease} را خروجی بده.",
      "plethysmography": "در صورت diagnostic بودن تفسیر یک plethysmography تیپیک برای بیماری {disease} را خروجی بده."
    },
    "procedures": {
      "Bronchoscopy": "در صورت diagnostic نبودن نتایج را نشان بده با این حال اخطاری مبنی بر خطرات انجام این پروسیجر در نبود اندیکاسیون آن بده.",
      "torachonthesis": "در صورت diagnostic نبودن نتایج را نشان بده با این حال اخطاری مبنی بر خطرات انجام این پروسیجر در نبود اندیکاسیون آن بده."
    }
  },
  "differential_diagnosis": {
    "disease1": "Asthma",
    "disease2": "Pneumonia",
    "disease3": "COPD",
    "disease4": "PTE",
    "disease5": "IPF",
    "disease6": "PH",
    "disease7": "Pleural Effusion",
    "disease8": "ARDS"
  }
}

def flatten_dict(d, parent_key='', sep='.'):
    """Recursively flattens a nested dictionary."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def format_list_for_prompt(items_list):
    """Converts a list of action keys into a readable bulleted string for LLM."""
    if not items_list:
        return "None"
    return "\n".join([f"- {item}" for item in items_list])

def analyze_and_return(optimal, student):
    """
    Compares flattened dictionaries to find Correct, Missed, and Noise items.
    """
    flat_optimal = flatten_dict(optimal)
    flat_student = flatten_dict(student)
    
    results = {
        "correct": [],
        "missed": [],
        "noise": []
    }
    
    # Union of all keys ensures we check everything
    all_keys = set(flat_optimal.keys()) | set(flat_student.keys())
    
    for key in all_keys:
        # 1. Check Optimal Status
        opt_val = flat_optimal.get(key, "False")
        is_required = str(opt_val).strip().lower() == "true"
        
        # 2. Check Student Status
        stud_val = flat_student.get(key, "False")
        is_performed = stud_val is not None and str(stud_val).strip().replace("ّ", "").lower() not in ["false", "none", ""]
        
        # 3. Categorize
        if is_required and is_performed:
            results["correct"].append(key)
        elif is_required and not is_performed:
            results["missed"].append(key)
        elif not is_required and is_performed:
            results["noise"].append(key)
            
    return results

def calculate_metrics(optimal, student):
    """
    Analyzes the logs and calculates pure numbers for the chart.
    """
    flat_optimal = flatten_dict(optimal)
    flat_student = flatten_dict(student)
    
    # 1. Categorization Lists
    categorized = {
        "correct": [],
        "missed": [],
        "noise": []
    }
    
    all_keys = set(flat_optimal.keys()) | set(flat_student.keys())
    
    for key in all_keys:
        # Check Optimal Requirement
        opt_val = flat_optimal.get(key, "False")
        is_required = str(opt_val).strip().lower() == "true"
        
        # Check Student Action
        stud_val = flat_student.get(key, "False")
        is_performed = stud_val is not None and str(stud_val).strip().replace("ّ", "").lower() not in ["false", "none", ""]
        
        if is_required and is_performed:
            categorized["correct"].append(key)
        elif is_required and not is_performed:
            categorized["missed"].append(key)
        elif not is_required and is_performed:
            categorized["noise"].append(key)
            
    # 2. Calculation for Chart
    correct_count = len(categorized["correct"])
    noise_count = len(categorized["noise"])
    missed_count = len(categorized["missed"])
    
    # Total Actions Taken (Denominator for Signal-to-Noise Ratio)
    total_actions_performed = correct_count + noise_count
    
    # Efficiency Score (0 to 100)
    efficiency_score = 0
    if total_actions_performed > 0:
        efficiency_score = int((correct_count / total_actions_performed) * 100)
        
    return {
        "counts": {
            "signal": correct_count,
            "noise": noise_count,
            "missed": missed_count,
            "total_performed": total_actions_performed
        },
        "score": efficiency_score,
        "details": categorized # لیست کامل برای استفاده در پرامپت
    }

# ==========================================
# 3. AI FEEDBACK GENERATION
# ==========================================

def generate_analysis_json(metrics_data, full_scenario_ref):
    """
    Uses LLM to generate text analysis based on the metrics.
    Returns a JSON object.
    """
    
    # Preparing data strings for the prompt
    def list_to_str(lst):
        return "\n".join([f"- {item}" for item in lst]) if lst else "None"

    correct_str = list_to_str(metrics_data["details"]["correct"])
    missed_str = list_to_str(metrics_data["details"]["missed"])
    noise_str = list_to_str(metrics_data["details"]["noise"])
    
    full_scenario_str = json.dumps(full_scenario_ref, ensure_ascii=False)
    
    # Define Parser
    parser = JsonOutputParser()

    # Define Prompt
    template_text = """
    Role: Senior Clinical Professor.
    
    ---
    ### REFERENCE MAP (Scenario Content)
    {full_scenario_reference}
    ---
    
    ### STUDENT STATS
    - Efficiency Score: {efficiency_score}%
    - CORRECT Actions (Signal):
    {correct_list}
    
    - MISSED Actions (Gap):
    {missed_list}
    
    - NOISE Actions (Waste):
    {noise_list}
    
    ### TASK
    Analyze the student's "Diagnostic Efficiency".
    Return a valid JSON object (Keys: "strengths", "missed_criticals", "inefficiencies", "conclusion").
    Values must be in **Persian**.
    
    Guidelines:
    1. Look up the meaning of missed/noise keys in the REFERENCE MAP.
    2. Explain WHY a missed item is critical.
    3. Explain WHY a noise item was a waste of resources.
    
    {format_instructions}
    """
    
    prompt = PromptTemplate(
        template=template_text,
        input_variables=["full_scenario_reference", "correct_list", "missed_list", "noise_list", "efficiency_score"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    # Initialize Model (تنظیمات مدل خود را اینجا انجام دهید)
    model = init_chat_model(
    base_url="https://api.avalai.ir/v1", 
    api_key="aa-o3nQicuKCc2ND0IuSOHDXouISJ0GQHvK1cqQmtGgBvORi2FH",
    model="gpt-4o-mini"
)

    # 6. ساخت Chain (اتصال پرامپت -> مدل -> پارسر JSON)
    chain = prompt | model | parser
    
    try:
        return chain.invoke({
            "full_scenario_reference": full_scenario_str,
            "correct_list": correct_str,
            "missed_list": missed_str,
            "noise_list": noise_str,
            "efficiency_score": metrics_data["score"]
        })
    except Exception as e:
        return {
            "strengths": "خطا در تولید",
            "missed_criticals": "خطا در تولید",
            "inefficiencies": "خطا در تولید",
            "conclusion": f"Error: {str(e)}"
        }

def process_diagnostic_efficiency(optimal_scenario, student_log, full_scenario_text):
    # 1. Calculate Numbers
    metrics = calculate_metrics(optimal_scenario, student_log)
    
    # 2. Generate Analysis
    ai_analysis = generate_analysis_json(metrics, full_scenario_text)
    
    # 3. Final Response (Updated)
    response = {
        "chart_data": {
            "signal_value": metrics["counts"]["signal"],
            "noise_value": metrics["counts"]["noise"],
            "missed_value": metrics["counts"]["missed"],
            "efficiency_score": metrics["score"],
            "total_actions": metrics["counts"]["total_performed"]
        },
        "details": {
            "missed_items": metrics["details"]["missed"], # لیست سوالات پرسیده نشده (جدید)
            "noise_items": metrics["details"]["noise"],   # لیست سوالات اضافی
            "correct_items": metrics["details"]["correct"]
        },
        "analysis": ai_analysis
    }
    
    return response

# # ==========================================
# # 4. MAIN EXECUTION
# # ==========================================
# if __name__ == "__main__":
    
#     final_output = process_diagnostic_efficiency(OPTIMAL_SCENARIO, STUDENT_LOG, FULL_SCENARIO)
    
#     print(json.dumps(final_output, indent=4, ensure_ascii=False))
    