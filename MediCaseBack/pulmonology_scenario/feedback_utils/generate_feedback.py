import json
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from .asthma import *
from .pte import *
from .ph import *
from .copd import *
from .ipf import *
from .pneumenia import *

from .feedback import ClinicalEvaluator

SCENARIO_MAP = {
    "Asthma": {
        "exercise_induced": ASTHMA_EXERCISE_INDUCED,
        "mild_allergic": ASTHMA_MILD_ALLERGIC,
        "severe_uncontrolled": ASTHMA_SEVERE_UNCONTROLLED
    },
    "PTE": {
        "massive_pte": PTE_MASSIVE_PTE,
        "peripheral_infarct": PTE_PERIPHERAL_INFARCT,
        "submassive_pte": PTE_SUBMASSIVE_PTE
    },
    "PH": {
        "idiopathic_pah": PH_IDIOPATHIC_PAH,
        "ph_lung_disease": PH_LUNG_DISEASE
    },
    "COPD": {
        "chronic_bronchitis": COPD_CHRONIC_BRONCHITIS,
        "copd_cor_pulmonale": COPD_COR_PULMONALE,
        "emphysema": COPD_EMPHYSEMA
    },
    "IPF": {
        "acute_ipf_exacerbation": IPF_ACUTE_IPF_EXACERBATION,
        "rheumatoid_ild": IPF_RHEUMATOID_ILD,
        "stable_ipf": IPF_STABLE_IPF
    },
    "Pneumonia": {
        "atypical_walking": PNEUMENIA_ATYPICAL_WALKING,
        "complicated_effusion": PNEUMENIA_COMPLICATED_EFFUSION,
        "typical_lobar": PNEUMENIA_TYPICAL_LOBAR
    }
}

DETAILED_SCENARIO_MAP = {
    "Asthma": {
        "exercise_induced": ASTHMA_EXERCISE_INDUCED_DETAILED,
        "mild_allergic": ASTHMA_MILD_ALLERGIC_DETAILED,
        "severe_uncontrolled": ASTHMA_SEVERE_UNCONTROLLED_DETAILED
    },
    "PTE": {
        "massive_pte": PTE_MASSIVE_PTE_DETAILED,
        "peripheral_infarct": PTE_PERIPHERAL_INFARCT_DETAILED,
        "submassive_pte": PTE_SUBMASSIVE_PTE_DETAILED
    },
    "PH": {
        "idiopathic_pah": PH_IDIOPATHIC_PAH_DETAILED,
        "ph_lung_disease": PH_LUNG_DISEASE_DETAILED
    },
    "COPD": {
        "chronic_bronchitis": COPD_CHRONIC_BRONCHITIS_DETAILED,
        "copd_cor_pulmonale": COPD_COR_PULMONALE_DETAILED,
        "emphysema": COPD_EMPHYSEMA_DETAILED
    },
    "IPF": {
        "acute_ipf_exacerbation": IPF_ACUTE_IPF_EXACERBATION_DETAILED,
        "rheumatoid_ild": IPF_RHEUMATOID_ILD_DETAILED,
        "stable_ipf": IPF_STABLE_IPF_DETAILED
    },
    "Pneumonia": {
        "atypical_walking": PNEUMENIA_ATYPICAL_WALKING_DETAILED,
        "complicated_effusion": PNEUMENIA_COMPLICATED_EFFUSION_DETAILED,
        "typical_lobar": PNEUMENIA_TYPICAL_LOBAR_DETAILED
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
      "question7": "در روزهای اخیر تب، لرز یا تعریق شبانه داشتید؟",
      "question8": "تورم پا، تپش قلب یا احساس سبکی سر دارید؟",
      "question9": "قبلاً هم چنین حمله یا علائمی داشتید؟ چه درمانی کمکتون کرده؟",
      "question10": "احساس کاهش وزن، خستگی یا بی‌اشتهایی داشتید؟"
    },
    "past_medical_history": {
      "question1": {
        "question1a": "آیا بیماری طولانی مدت (مزمن) مثل قند (دیابت)، فشار خون، آسم، مشکل تیروئید، یا بیماری جدی کلیوی/کبدی دارید؟",
        "question1b": "اگر پاسخ بله بود، تشخیص این بیماری از چه موقع بوده است؟"
      },
      "question2": {
        "question2a": "آیا تا به حال عمل جراحی (بزرگ یا کوچک) داشته‌اید؟ و آیا تا به حال در بیمارستان بستری شده‌اید؟",
        "question2b": "اگر بله، دلیلش چه بوده و در چه سالی؟ همچنین، آیا تا به حال انتقال خون داشته‌اید؟"
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
        "question1b": "اگر پاسخ بله بود، دقیقاً چه دارو یا ماده‌ای است؟ و واکنش شما چگونه بوده است؟"
      }
    },
    "family_history": {
      "question1": {
        "question1a": "آیا در خانواده درجه یک شما، سابقه ابتلا به بیماری‌های مزمن و شایع زیر وجود دارد؟",
        "question1b": "اگر بله، چه کسی و در چه سنی به آن مبتلا شده است؟"
      },
      "question2": "آیا در خانواده درجه یک شما، سابقه حمله قلبی (سکته قلبی)، سکته مغزی، یا نارسایی قلبی وجود دارد؟",
      "question3": {
        "question3a": "آیا سابقه سرطان خاصی در خانواده درجه یک شما وجود دارد؟",
        "question3b": "اگر بله، نوع سرطان چه بوده و در چه سنی تشخیص داده شده است؟"
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
    "ros": {
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
        "level_of_consciousness": "آیا بیمار هوشیار، گیج، خواب‌آلود است؟",
        "mood": "آیا بیمار به نظر بیمار، مضطرب، یا در درد شدید است؟",
        "behavior": "آیا بیمار همکاری می‌کند؟"
      },
      "posture_and_position": {
        "position_of_comfort": "آیا بیمار وضعیتی را برای کاهش درد یا تنگی نفس انتخاب کرده است؟"
      },
      "overall_appearance": {
        "nutritional_status": "آیا بیمار لاغر (Cachectic)، چاق (Obese)، یا در وضعیت وزن طبیعی است؟"
      },
      "cardiopulmonary_and_circulatory_clues": {
        "cyanosis": "بررسی کبودی.",
        "dyspnea": "تلاش تنفسی.",
        "edema": "وجود تورم در پاها."
      }
    },
    "head_and_neck": {
      "head_and_face": {
        "symmetry_and_lesions": "تقارن و ضایعات صورت.",
        "tenderness": "تندرنس جمجمه."
      },
      "eyes": {
        "sclera_and_conjunctiva": "یرقان یا رنگ پریدگی.",
        "pupils_reaction": "رفلکس مردمک.",
        "extraocular_movements": "حرکات چشمی."
      },
      "ears": {
        "external_and_tenderness": "حساسیت گوش خارجی.",
        "eardrum_appearance": "پرده صماخ."
      },
      "nose_and_sinuses": {
        "septum_and_discharge": "انحراف تیغه و ترشحات.",
        "sinus_tenderness": "حساسیت سینوس."
      },
      "mouth_and_pharynx": {
        "oral_mucosa_and_lesions": "مخاط دهان.",
        "pharynx_and_tonsils": "لوزه‌ها و حلق."
      },
      "neck_and_lymphatics": {
        "inspection": "مشاهدات گردن.",
        "tracheal_position": "موقعیت نای.",
        "thyroid_gland": "غده تیروئید.",
        "carotid_bruit": "برویی کاروتید.",
        "lymph_nodes_size_consistency": "اندازه غدد لنفاوی.",
        "lymph_nodes_mobility_tenderness": "حساسیت غدد لنفاوی."
      }
    },
    "respiratory_system": {
      "inspection": {
        "accessory_muscles": "استفاده از عضلات کمکی.",
        "chest_shape_and_symmetry": "شکل قفسه سینه."
      },
      "palpation": {
        "chest_expansion": "توسعه قفسه سینه.",
        "tactile_fremitus": "لرزش‌های صوتی."
      },
      "percussion": "صدای دق ریه.",
      "auscultation": {
        "breath_sounds_intensity": "شدت صداهای تنفسی.",
        "adventitious_sounds": "صداهای اضافی (کراکل/ویزینگ)."
      }
    },
    "cardiovascular_system": {
      "JVP_assessment": "فشار وریدی ژوگولار.",
      "palpation": {
        "precordial_palpation_heave_thrill": "لیفت، هیو، تریل.",
        "pmi_assessment": "ضربان نوک قلب."
      },
      "auscultation": {
        "heart_sounds_s1_s2": "صداهای قلب.",
        "extra_sounds_s3_s4_murmurs": "صداهای اضافی قلب."
      },
      "peripheral_pulses_and_extremities": {
        "peripheral_pulses_symmetry_and_quality": "قدرت نبض‌های محیطی.",
        "extremities_color_and_trophic_changes": "رنگ و تغییرات تروفیک اندام‌ها.",
        "extremities_temperature_and_cap_refill": "دمای اندام‌ها و بازگشت مویرگی.",
        "extremities_edema": "ادم اندام‌ها."
      }
    },
    "abdominal_system": {
      "inspection": "شکل شکم.",
      "auscultation": {
        "bowel_sounds": "صداهای روده.",
        "vascular_bruits": "صداهای عروقی."
      },
      "percussion": {
        "general": "دق شکم.",
        "organ_borders": "حدود ارگان‌ها."
      },
      "palpation": {
        "superficial_tenderness": "تندرنس سطحی.",
        "deep_masses_and_organs": "توده‌های عمقی."
      },
      "peritoneal_signs": "علائم صفاقی."
    },
    "neurological": {
      "mental_status_and_LOC": "هوشیاری.",
      "cranial_nerves": "اعصاب کرانیال.",
      "motor_strength_and_tone": "قدرت حرکتی.",
      "involuntary_movements": "حرکات غیرارادی.",
      "sensory_light_touch_and_pain": "حواس.",
      "deep_tendon_reflexes": "رفلکس‌های عمقی.",
      "coordination_and_gait": "تعادل و راه رفتن."
    },
    "musculoskeletal_system": {
      "inspection": {
        "joints": "مفاصل.",
        "muscles": "عضلات."
      },
      "palpation": {
        "tenderness_and_crepitus": "تندرنس عضلانی اسکلتی."
      },
      "range_of_motion_active_passive": "دامنه حرکتی.",
      "stability_and_function": "پایداری مفاصل."
    }
  },
  "paraclinic": {
    "basic_blood_tests": {
      "CBC": "نتایج CBC",
      "ESR": "نتیجه ESR",
      "CRP": "نتیجه CRP",
      "BMP": "نتایج BMP",
      "LFTs": "نتایج LFTs",
      "VBG": "نتایج VBG"
    },
    "specialized_lung_tests": {
      "Sputum_analysis": "نتایج آنالیز خلط",
      "Sputum_AFB": "نتیجه AFB خلط",
      "a1_antitrypsin_level": "سطح آلفا 1 آنتی تریپسین",
      "D_dimer": "سطح دی دایمر",
      "BNP_NT_proBNP": "سطح BNP"
    },
    "immunity_and_serology": {
      "HIV_test": "تست HIV",
      "Autoimmune_pannel_ANA_ANCA": "پنل اتوایمیون"
    },
    "simple_imaging": {
      "Chest_X_Ray": "در صورت Diagnostic بودن تفسیر عکس قفسه سینه را ارائه بده و در غیر این صورت نتایج نرمال اعلام شود."
    },
    "advanced_imaging": {
      "Chest_CT_CTPA": "تفسیر سی تی اسکن ریه",
      "MRI_chest": "تفسیر MRI",
      "Pet_scan": "تفسیر پت اسکن"
    },
    "functional_tests": {
      "Spirometry": "تفسیر اسپیرومتری",
      "peak_flow": "تفسیر پیک فلو",
      "plethysmography": "تفسیر پلتیسموگرافی"
    },
    "procedures": {
      "Bronchoscopy": "نتیجه برونکوسکوپی",
      "torachonthesis": "نتیجه توراسنتز"
    }
  },
  "differential_diagnosis": {
    "disease1": "بیماری اول",
    "disease2": "بیماری دوم",
    "disease3": "بیماری سوم",
    "disease4": "بیماری چهارم",
    "disease5": "بیماری پنجم",
    "disease6": "بیماری ششم",
    "disease7": "بیماری هفتم",
    "disease8": "بیماری هشتم"
  },
  "final_diagnosis": {
    "disease": "تشخیص نهایی بیماری"
  },
  "pleural_effusion_assessment": {
    "has_effusion": "آیا بیمار افیوژن دارد؟ (بله/خیر)",
    "need_aspiration": "آیا نیاز به کشیدن مایع (توراسنتز) هست؟ (بله/خیر)",
    "effusion_type": "نوع مایع چیست؟ (اگزودا/ترانسودا)"
  }
}

def flatten_scenario(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            if "question" in v and "analysis" in v:
                items.append((new_key, True))
            else:
                items.extend(flatten_scenario(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def flatten_student(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_student(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def preprocess_student_log(student_log, optimal_scenario):
    """
    این تابع پیش‌پردازنده، لاگ دریافتی از فرانت‌اند را با ساختار دقیق بک‌اند تطبیق می‌دهد:
    ۱. اصلاح نام‌های قدیمی (مثل 2_pulses_and_extremities به peripheral_pulses...)
    ۲. بسط دادن سوالات کلی (مثل question1) به زیرسوالات (question1a, 1b) در صورت وجود در سناریوی بهینه.
    """
    log_str = json.dumps(student_log)
    log_str = log_str.replace('"2_pulses_and_extremities"', '"peripheral_pulses_and_extremities"')
    fixed_log = json.loads(log_str)
    
    flat_opt = flatten_scenario(optimal_scenario)
    flat_stud = flatten_student(fixed_log)
    
    expanded_flat_stud = {}
    for stud_k, stud_v in flat_stud.items():
        expanded = False
        for opt_k in flat_opt.keys():
            if opt_k.startswith(stud_k + "."):
                expanded_flat_stud[opt_k] = stud_v
                expanded = True
        
        if not expanded:
            expanded_flat_stud[stud_k] = stud_v
            
    def unflatten(flat_dict):
        result = {}
        for k, v in flat_dict.items():
            parts = k.split('.')
            d = result
            for part in parts[:-1]:
                if part not in d:
                    d[part] = {}
                d = d[part]
            d[parts[-1]] = v
        return result
        
    return unflatten(expanded_flat_stud)

def calculate_metrics(optimal, processed_student):
    flat_optimal = flatten_scenario(optimal)
    flat_student = flatten_student(processed_student)
    
    categorized = {
        "correct": [],
        "missed": [],
        "noise": []
    }
    
    all_keys = set(flat_optimal.keys()) | set(flat_student.keys())
    
    for key in all_keys:
        if key.startswith("final_diagnosis") or key.startswith("pleural_effusion_assessment"):
            continue
            
        is_required = str(flat_optimal.get(key, "False")).lower() == "true"
        
        stud_val = flat_student.get(key, "False")
        clean_stud_val = str(stud_val).strip().replace("ّ", "").lower()
        is_performed = stud_val is not None and clean_stud_val not in ["false", "none", "", "0"]
        
        if is_required and is_performed:
            categorized["correct"].append(key)
        elif is_required and not is_performed:
            categorized["missed"].append(key)
        elif not is_required and is_performed:
            categorized["noise"].append(key)
            
    correct_count = len(categorized["correct"])
    noise_count = len(categorized["noise"])
    missed_count = len(categorized["missed"])
    total_performed = correct_count + noise_count
    
    efficiency_score = int((correct_count / total_performed) * 100) if total_performed > 0 else 0
        
    return {
        "counts": {
            "signal": correct_count,
            "noise": noise_count,
            "missed": missed_count,
            "total_performed": total_performed
        },
        "score": efficiency_score,
        "details": categorized
    }

def extract_nested_data(node, key_to_extract):
    results = []
    if isinstance(node, dict):
        if key_to_extract in node:
            results.append(node[key_to_extract])
        else:
            for v in node.values():
                results.extend(extract_nested_data(v, key_to_extract))
    elif isinstance(node, str) and key_to_extract == "question":
        results.append(node)
    return results

def get_action_details(key, detailed_scenario, full_scenario):
    parts = key.split('.')
    
    curr_det = detailed_scenario
    found_detailed = True
    for p in parts:
        if isinstance(curr_det, dict) and p in curr_det:
            curr_det = curr_det[p]
        else:
            if isinstance(curr_det, dict) and ("analysis" in curr_det or "question" in curr_det):
                pass 
            else:
                found_detailed = False
            break

    full_curr = full_scenario
    found_full = True
    for p in parts:
        if isinstance(full_curr, dict) and p in full_curr:
            full_curr = full_curr[p]
        else:
            if isinstance(full_curr, dict) and "question" in full_curr:
                pass
            else:
                found_full = False
            break

    question_text = parts[-1] 
    analysis_text = "این اقدام در این سناریوی خاص غیرضروری یا فاقد اولویت بود."
    
    if found_detailed:
        if isinstance(curr_det, dict):
            if "question" in curr_det:
                question_text = curr_det["question"]
            else:
                qs = extract_nested_data(curr_det, "question")
                if qs: question_text = " / ".join(qs)
                
            if "analysis" in curr_det and curr_det["analysis"]:
                analysis_text = curr_det["analysis"]
            else:
                ans = extract_nested_data(curr_det, "analysis")
                valid_ans = [a for a in ans if a]
                if valid_ans:
                    analysis_text = " | ".join(valid_ans)
                elif "question" not in curr_det:
                    analysis_text = "بدون تحلیل اختصاصی."
                    
        elif isinstance(curr_det, str):
            question_text = curr_det
            analysis_text = "بدون تحلیل اختصاصی."

    elif found_full:
        if isinstance(full_curr, dict) and "question" in full_curr:
            question_text = full_curr["question"]
        elif isinstance(full_curr, str):
            question_text = full_curr
        else:
            qs = extract_nested_data(full_curr, "question")
            if qs: question_text = " / ".join(qs)

    return {
        "id": key,
        "question": question_text,
        "analysis": analysis_text
    }

def generate_ai_analysis(metrics_data, full_scenario_ref):
    def list_to_str(lst):
        limit = 20
        items = lst[:limit]
        text = "\n".join([f"- {item}" for item in items])
        if len(lst) > limit:
            text += f"\n... و {len(lst)-limit} مورد دیگر."
        return text if items else "موردی یافت نشد"

    correct_str = list_to_str(metrics_data["details"]["correct"])
    missed_str = list_to_str(metrics_data["details"]["missed"])
    noise_str = list_to_str(metrics_data["details"]["noise"])
    
    full_scenario_str = json.dumps(full_scenario_ref, ensure_ascii=False)
    
    parser = JsonOutputParser()

    template_text = """
    Role: Senior Clinical Professor evaluating a medical student in Iran.
    
    ---
    ### CONTEXT MAP (Reference for questions/tests meanings)
    {full_scenario_reference}
    ---
    
    ### STUDENT PERFORMANCE DATA
    - **Efficiency Score:** {efficiency_score}% (Higher is better)
    
    - **CORRECT Actions (Signal - Good Judgment):**
    {correct_list}
    
    - **MISSED Actions (Gap - Dangerous Omissions):**
    {missed_list}
    
    - **NOISE Actions (Waste - Unnecessary/Wrong Actions):**
    {noise_list}
    
    ### INSTRUCTIONS
    Analyze the student's clinical reasoning.
    Return a valid JSON object with exactly these 4 keys in **PERSIAN (Farsi)**:
    1. "strengths": (Text) Praise their correct critical decisions.
    2. "missed_criticals": (Text) Explain the medical risk/consequence of missing the specific items in the 'MISSED' list.
    3. "inefficiencies": (Text) Explain why the specific items in 'NOISE' list were unnecessary for this specific case (cost/radiation/irrelevant).
    4. "conclusion": (Text) A brief, professional final verdict for the student.
    
    {format_instructions}
    """
    
    prompt = PromptTemplate(
        template=template_text,
        input_variables=["full_scenario_reference", "correct_list", "missed_list", "noise_list", "efficiency_score"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    try:
        model = init_chat_model(
            base_url="https://api.avalai.ir/v1", 
            api_key="aa-o3nQicuKCc2ND0IuSOHDXouISJ0GQHvK1cqQmtGgBvORi2FH",
            model="gpt-4o-mini"
        )
        chain = prompt | model | parser
        
        return chain.invoke({
            "full_scenario_reference": full_scenario_str,
            "correct_list": correct_str,
            "missed_list": missed_str,
            "noise_list": noise_str,
            "efficiency_score": metrics_data["score"]
        })
    except Exception as e:
        return {
            "strengths": "سیستم قادر به تولید تحلیل هوشمند نیست.",
            "missed_criticals": "بررسی اتصال به اینترنت یا سرویس هوش مصنوعی.",
            "inefficiencies": str(e),
            "conclusion": "خطا در پردازش هوش مصنوعی."
        }

def calculate_matrix_position(score_percent, duration_seconds, total_time=900):
    SCORE_THRESHOLD = 60.0 
    TIME_THRESHOLD_SECONDS = total_time * 0.85 
    
    is_accurate = score_percent >= SCORE_THRESHOLD
    is_fast = duration_seconds <= TIME_THRESHOLD_SECONDS
    
    result = {
        "quadrant_code": "", "label_fa": "", "label_en": "", "description": "", "color": ""
    }
    
    if is_accurate and is_fast:
        result.update({"quadrant_code": "Q1_MASTER", "label_fa": "مسلط / استادانه", "label_en": "Master / Efficient", "description": "عالی. تعادل ایده‌آل بین سرعت عمل و دقت علمی.", "color": "#2E7D32"})
    elif is_accurate and not is_fast:
        result.update({"quadrant_code": "Q2_CAUTIOUS", "label_fa": "محتاط / دقیق", "label_en": "Cautious", "description": "تشخیص صحیح با سرعت پایین. نیاز به تمرین برای افزایش سرعت تصمیم‌گیری.", "color": "#FBC02D"})
    elif not is_accurate and is_fast:
        result.update({"quadrant_code": "Q3_RASH", "label_fa": "عجول / شتاب‌زده", "label_en": "Rash / Impulsive", "description": "هشدار: سرعت بالا بدون دقت علمی. این الگو در بالین خطرناک است.", "color": "#C62828"})
    else:
        result.update({"quadrant_code": "Q4_NOVICE", "label_fa": "نیازمند آموزش پایه", "label_en": "Novice", "description": "نیاز به مطالعه بیشتر و تمرین سناریوها برای بهبود دقت و سرعت.", "color": "#757575"})

    result["coordinates"] = {
        "x": duration_seconds, "y": score_percent,
        "x_threshold": TIME_THRESHOLD_SECONDS, "y_threshold": SCORE_THRESHOLD
    }
    return result

def generate_feedback(disease_category, specific_scenario_key, student_log):
    try:
        optimal_scenario = SCENARIO_MAP[disease_category][specific_scenario_key]
        detailed_scenario = DETAILED_SCENARIO_MAP[disease_category][specific_scenario_key]
    except KeyError:
        return {"error": f"Scenario {disease_category} -> {specific_scenario_key} not found."}

    # 1. پیش‌پردازش دیتای دانشجو برای حل اختلافات ساختاری با فرانت‌اند
    processed_student_log = preprocess_student_log(student_log, optimal_scenario)

    # 2. محاسبه نمرات با استفاده از لاگ پردازش شده
    evaluator = ClinicalEvaluator(optimal_scenario, processed_student_log)
    final_score_percent = evaluator.evaluate_performance()
    
    duration_seconds, start_time = evaluator.calculate_duration()
    time_analysis = evaluator.analyze_time_performance(duration_seconds, evaluator.total_time_seconds)
    category = evaluator.get_category(final_score_percent)

    metrics = calculate_metrics(optimal_scenario, processed_student_log)
    
    enriched_correct = [get_action_details(k, detailed_scenario, FULL_SCENARIO) for k in metrics["details"]["correct"]]
    enriched_missed = [get_action_details(k, detailed_scenario, FULL_SCENARIO) for k in metrics["details"]["missed"]]
    enriched_noise = [get_action_details(k, detailed_scenario, FULL_SCENARIO) for k in metrics["details"]["noise"]]
    
    ai_metrics_data = {
        "score": metrics["score"],
        "details": {
            "correct": [item["question"] for item in enriched_correct],
            "missed": [item["question"] for item in enriched_missed],
            "noise": [item["question"] for item in enriched_noise]
        }
    }
    ai_analysis = generate_ai_analysis(ai_metrics_data, FULL_SCENARIO)
    
    matrix_data = calculate_matrix_position(final_score_percent, duration_seconds, evaluator.total_time_seconds)
    diagnosis_results = evaluator.evaluate_diagnosis_accuracy()
    pleural_results = evaluator.evaluate_pleural_effusion()
    
    output = {
        "meta": {
            "disease": disease_category,
            "scenario": specific_scenario_key
        },
        "overall_result": {
            "title": category['label'],
            "english_title": category['eng'],
            "color_code": category['color'],
            "is_passed": final_score_percent >= 60
        },
        "score": {
            "obtained": round(final_score_percent, 2),
            "total": 100,
            "efficiency_score": metrics["score"]
        },
        "time_management": {
            "duration_formatted": evaluator.format_time(duration_seconds),
            "total_allowed_formatted": "15:00",
            "analysis": time_analysis
        },
        "chart_data": {
            "signal_value": metrics["counts"]["signal"],
            "noise_value": metrics["counts"]["noise"],  
            "missed_value": metrics["counts"]["missed"],
            "total_actions": metrics["counts"]["total_performed"]
        },
        "performance_matrix": {
            "title": "تحلیل سرعت در برابر دقت",
            "status": matrix_data["label_fa"],
            "status_en": matrix_data["label_en"],
            "description": matrix_data["description"],
            "color_code": matrix_data["color"],
            "quadrant": matrix_data["quadrant_code"],
            "chart_coordinates": matrix_data["coordinates"]
        },
        "diagnosis_section": {
            "user_final_diagnosis": diagnosis_results["student_final_answer"],
            "correct_final_diagnosis": diagnosis_results["correct_final_answer"],
            "is_correct": diagnosis_results["is_final_correct"],
            "differential_analysis": {
                "correct_items": diagnosis_results["correct_differentials"],
                "missed_items": diagnosis_results["missed_differentials"]
            },
            "feedback_message": f"تشخیص نهایی شما {'صحیح بود' if diagnosis_results['is_final_correct'] else 'نادرست بود'}."
        },
        "pleural_effusion_section": {
          "title": "ارزیابی پلورال افیوژن",
          "is_correct": pleural_results["is_correct"],
          "user_assessment": pleural_results["student"],
          "correct_assessment": pleural_results["optimal"],
          "feedback_message": "تشخیص وضعیت مایع پلور صحیح بود." if pleural_results["is_correct"] else "در تشخیص وضعیت مایع پلور اشتباه داشتید."
        },
        "detailed_lists": {
            "missed_items": enriched_missed,
            "noise_items": enriched_noise,
            "correct_items": enriched_correct
        },
        "ai_analysis": ai_analysis
    }
    
    return output

# sample_student_log = {
#   "history_taking": {
#     "present_illness": {
#       "question1": "14:50",
#       "question3": "14:35",
#       "question4": "14:20",
#       "question6": "14:05",
#       "question8": "13:50" 
#     },
#     "past_medical_history": {
#       "question3": "13:20" 
#     },
#     "drug_history": {
#       "question1": "13:00" 
#     },
#     "social_history": {
#       "question1": "12:45",
#       "question3": "12:30" 
#     },
#     "ros": {
#       "question6": "12:00" 
#     }
#   },
#   "physical_exam": {
#     "vital_signs": {
#       "BP": "11:45",
#       "PR": "11:40",
#       "SpO2": "11:35"
#     },
#     "general_appearance": {
#       "cardiopulmonary_and_circulatory_clues": {
#         "edema": "11:15",
#         "cyanosis": "11:10"
#       }
#     },
#     "cardiovascular_system": {
#       "JVP_assessment": "10:50",
#       "auscultation": {
#         "heart_sounds_s1_s2": "10:30"
#       },
#       "2_pulses_and_extremities": {     
#         "extremities_edema": "10:15"
#       }
#     },
#     "respiratory_system": {
#       "auscultation": {
#         "breath_sounds_intensity": "09:50"
#       }
#     }
#   },
#   "paraclinic": {
#     "basic_blood_tests": {
#       "BMP": "09:20",
#       "CBC": "09:18",
#       "LFTs": "09:15"
#     },
#     "specialized_lung_tests": {
#       "BNP_NT_proBNP": "08:50",
#       "D_dimer": "08:45"   
#     },
#     "immunity_and_serology": {
#       "Autoimmune_pannel_ANA_ANCA": "08:20"
#     },
#     "simple_imaging": {
#       "Chest_X_Ray": "08:00"
#     },
#     "advanced_imaging": {
#       "Chest_CT_CTPA": "07:30"
#     },
#     "functional_tests": {
#       "Spirometry": "07:00"
#     }
#   },
#   "differential_diagnosis": {
#     "disease3": "06:30", 
#     "disease4": "06:20",  
#     "disease6": "06:10"   
#   },
#   "final_diagnosis": {
#     "disease": "PH" 
#   },
#   "pleural_effusion_assessment": {
#     "has_effusion": "false",
#     "need_aspiration": "false",
#     "effusion_type": "none"
#   }
# }

# if __name__ == "__main__":
#     print("در حال تولید بازخورد. لطفاً منتظر بمانید...\n")
    
#     result = generate_feedback(
#         disease_category="PH", 
#         specific_scenario_key="idiopathic_pah", 
#         student_log=sample_student_log
#     )
    
#     print("نتیجه ارزیابی:")
#     print(json.dumps(result, ensure_ascii=False, indent=4))