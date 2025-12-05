from .S1_identifying_sets import calculate_set_metrics, count_true_values
from .S2_get_action_time import get_first_action_time_and_count
from .optimal_pulmonology_scenarios import OPTIMAL_SCENARIO
from typing import Dict, Any

STUDENT_LOG: Dict[str, Dict[str, str]] = {
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

def calculate_stage_score():    
    
    results: Dict[str, Dict[str, Any]] = {}
    
    for stage_name, optimal_actions in OPTIMAL_SCENARIO.items():
        
        if stage_name not in STUDENT_LOG:
            print(f"هشدار: مرحله '{stage_name}' در لاگ دانشجو وجود ندارد.")
            continue
    
        W_M = 0.5
        W_E = 0.3
        
        sets = calculate_set_metrics(OPTIMAL_SCENARIO, STUDENT_LOG)
        O = sets.get(stage_name)['O']
        C = sets.get(stage_name)['C']
        E = sets.get(stage_name)['E']
        M = sets.get(stage_name)['M']

        if O == 0:
            return 0.0

        term = (C / O) - ((E / O) * W_E) - ((M / O) * W_M)
        stage_score = max(0, 100 * term)

        results[stage_name] = {
            "stage_score": f"{stage_score:.2f}"
        }
    
    return results

def calculate_stage_score():
    # ... کد محاسبه نمره مرحله (گام ۲) ...
    # این تابع اکنون به صورت کامل فراخوانی می‌شود و از تابع جدید استفاده نمی‌کند.
    # من فقط گام سوم را به عنوان یک تابع جداگانه پیاده‌سازی می‌کنم.
    
    results: Dict[str, Dict[str, Any]] = {}
    
    # ... (کد calculate_stage_score برای محاسبه نمرات C, E, M, O, A و Stage Score)
    
    sets = calculate_set_metrics(OPTIMAL_SCENARIO, STUDENT_LOG)

    # گام ۲: محاسبه نمره مرحله (بازنویسی مختصر برای تکمیل)
    W_M = 0.5
    W_E = 0.3
    for stage_name, metrics in sets.items():
        O = metrics['O']
        C = metrics['C']
        E = metrics['E']
        M = metrics['M']
        
        if O == 0:
            stage_score = 0.0
        else:
            term = (C / O) - ((E / O) * W_E) - ((M / O) * W_M)
            stage_score = max(0, 100 * term)

        results[stage_name] = {
            "C": C,
            "E": E,
            "M": M,
            "O": O,
            "A": metrics['A'],
            "Success_Rate_C_div_O": metrics['Success_Rate_C_div_O'],
            "stage_score": f"{stage_score:.2f}"
        }

    return results

def calculate_stage_order_error(
    optimal_log: Dict[str, Dict[str, bool]],
    student_log: Dict[str, Dict[str, str]]
) -> Dict[str, Any]:
    """
    گام سوم: ارزیابی ترتیب مراحل (شرح حال -> معاینه فیزیکی -> پاراکلینیک).
    """
    
    stages = ["history_taking", "physical_exam", "paraclinic"]
    order_results: Dict[str, Any] = {}
    
    # 1. گذار ۱ → ۲ (شرح حال به معاینه)
    stage1_name = stages[0] # history_taking
    stage2_name = stages[1] # physical_exam
    
    if stage1_name in optimal_log and stage2_name in student_log:
        
        # O1: تعداد اقدامات بهینه در مرحله ۱
        O1 = count_true_values(optimal_log[stage1_name], "True")
        
        # اولین اقدام در مرحله ۲ (معاینه فیزیکی)
        # برای دقت بیشتر، اولین اقدام مرحله ۲ را به صورت بازگشتی پیدا می‌کنیم تا زمان آن را بدانیم
        # این به ما کمک می‌کند تا لاگ دانشجو را تا آن لحظه فیلتر کنیم.
        first_action_stage2 = get_first_action_time_and_count(student_log[stage2_name], 0)
        
        if first_action_stage2[0] is not None:
            # زمان اولین اقدام در مرحله ۲
            time_of_transition = first_action_stage2[0]
            
            # اکنون باید تعداد اقدامات انجام شده در مرحله ۱ (|A1|) تا قبل از زمان 'time_of_transition' را بشماریم.
            
            # برای ساده‌سازی، از آنجایی که 'get_first_action_time_and_count' بر اساس زمان مرتب می‌کند، 
            # اولین اقدام در مرحله ۲، 'اولین' اقدام جدید پس از مرحله ۱ است.
            # در این چارچوب موجود، ما نیاز داریم تا **کل اقدامات مرحله ۱** که در لاگ دانشجو هستند را بشماریم.
            # (چون لاگ دانشجو اقدامات را بر اساس زمان ذخیره کرده است و ما از تابع 'recursive_count_C' استفاده نمی‌کنیم)
            
            # |A1|: تعداد کل اقدامات انجام شده در مرحله ۱ (هر چیزی غیر از "False")
            A1_all = get_first_action_time_and_count(student_log[stage1_name], 0)[1]
            
            # آستانه ۵۰٪
            threshold_O1 = 0.5 * O1
            
            order_results["transition_1_to_2"] = {
                "O1": O1,
                "A1_at_transition": A1_all,
                "threshold_50_percent": threshold_O1,
                "error": False,
                "message": "Passed"
            }
            
            if O1 > 0 and A1_all < threshold_O1:
                order_results["transition_1_to_2"]["error"] = True
                order_results["transition_1_to_2"]["message"] = "Stage Order Error – شرح حال ناقص. قبل از تکمیل 50% اقدامات بهینه شرح حال، وارد معاینه فیزیکی شدید."
        else:
            order_results["transition_1_to_2"] = {"message": "معاینه فیزیکی انجام نشده است، بنابراین خطا در توالی ۱->۲ محاسبه نمی‌شود."}


    # 2. گذار ۲ → ۳ (معاینه به پاراکلینیک)
    stage2_name = stages[1] # physical_exam
    stage3_name = stages[2] # paraclinic

    if stage2_name in optimal_log and stage3_name in student_log:
        
        # O2: تعداد اقدامات بهینه در مرحله ۲
        O2 = count_true_values(optimal_log[stage2_name], "True")
        
        # اولین اقدام در مرحله ۳ (پاراکلینیک)
        first_action_stage3 = get_first_action_time_and_count(student_log[stage3_name], 0)
        
        if first_action_stage3[0] is not None:
            time_of_transition = first_action_stage3[0]
            
            # |A2|: تعداد کل اقدامات انجام شده در مرحله ۲ (هر چیزی غیر از "False")
            A2_all = get_first_action_time_and_count(student_log[stage2_name], 0)[1]
            
            # آستانه ۵۰٪
            threshold_O2 = 0.5 * O2

            order_results["transition_2_to_3"] = {
                "O2": O2,
                "A2_at_transition": A2_all,
                "threshold_50_percent": threshold_O2,
                "error": False,
                "message": "Passed"
            }

            if O2 > 0 and A2_all < threshold_O2:
                order_results["transition_2_to_3"]["error"] = True
                order_results["transition_2_to_3"]["message"] = "Stage Order Error – معاینه ناقص. قبل از تکمیل 50% اقدامات بهینه معاینه فیزیکی، وارد پاراکلینیک شدید (جریمه بیشتر)."
        else:
            order_results["transition_2_to_3"] = {"message": "پاراکلینیک انجام نشده است، بنابراین خطا در توالی ۲->۳ محاسبه نمی‌شود."}
            
    return order_results


