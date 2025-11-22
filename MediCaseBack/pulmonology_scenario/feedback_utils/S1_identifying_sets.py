import json
from typing import Dict, Any, Tuple, List

OPTIMAL_SCENARIO: Dict[str, Dict[str, bool]] = {
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
      "CBC": {
            "Hb": "True", 
            "WBC": "True", 
            "Plt": "False"
        },
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

def count_true_values(data, which):
    count = 0
    
    if isinstance(data, dict):
        for value in data.values():
            count += count_true_values(value, which)
    
    elif isinstance(data, str) and data == which:
        count += 1
    
    elif isinstance(data, list):
        for item in data:
            count += count_true_values(item, which)
    
    return count

def recursive_count_C(optimal_data: Any, student_data: Any) -> int:
    
    C = 0
    
    if isinstance(optimal_data, dict) and isinstance(student_data, dict):
    
        common_keys = set(optimal_data.keys()) & set(student_data.keys())
    
        for key in common_keys:
            C += recursive_count_C(optimal_data[key], student_data[key])
    
    elif isinstance(optimal_data, list) and isinstance(student_data, list):
        min_len = min(len(optimal_data), len(student_data))
        for i in range(min_len):
            C += recursive_count_C(optimal_data[i], student_data[i])
    
    elif isinstance(optimal_data, str) and isinstance(student_data, str):
    
        is_optimal = optimal_data == "True"
        is_student_action = student_data != "False"
    
        if is_optimal and is_student_action:
            C += 1
    
    return C

def identify_set_items(optimal_data: Any, student_data: Any) -> Tuple[List[str], List[str], List[str]]:
    c_list = []
    e_list = []
    m_list = []

    def _recurse(opt, stu, current_path):
        if isinstance(opt, dict) and isinstance(stu, dict):
            common_keys = set(opt.keys()) & set(stu.keys())
            for key in common_keys:
                new_path = f"{current_path}.{key}" if current_path else key
                _recurse(opt[key], stu[key], new_path)
                
        elif isinstance(opt, list) and isinstance(stu, list):
            min_len = min(len(opt), len(stu))
            for i in range(min_len):
                new_path = f"{current_path}[{i}]"
                _recurse(opt[i], stu[i], new_path)
                
        elif isinstance(opt, str) and isinstance(stu, str):
            is_optimal = (opt == "True")
            is_student_action = (stu != "False")
            
            if is_optimal and is_student_action:
                c_list.append(current_path)  
            elif is_optimal and not is_student_action:
                m_list.append(current_path)  
            elif not is_optimal and is_student_action:
                e_list.append(current_path)  

    _recurse(optimal_data, student_data, "")
    return c_list, e_list, m_list

def calculate_set_metrics(
    optimal_log: Dict[str, Dict[str, bool]],
    student_log: Dict[str, Dict[str, str]]
) -> Dict[str, Dict[str, Any]]:
    
    results: Dict[str, Dict[str, Any]] = {}
    
    for stage_name, optimal_actions in optimal_log.items():
        
        if stage_name not in student_log:
            print(f"هشدار: مرحله '{stage_name}' در لاگ دانشجو وجود ندارد.")
            continue
            
        student_actions = student_log[stage_name]
        
        c_items, e_items, m_items = identify_set_items(optimal_actions, student_actions)
        
        count_O = count_true_values(optimal_actions, "True")
        count_UnO = count_true_values(optimal_actions, "False")
        count_A = (count_O + count_UnO) - count_true_values(student_actions, "False")
        count_C = len(c_items)
        count_M = len(m_items)
        count_E = len(e_items)
        
        results[stage_name] = {
            "C": count_C,
            "E": count_E,
            "M": count_M,
            "O": count_O,
            "A": count_A,
            "Success_Rate_C_div_O": f"{count_C / count_O * 100:.2f}%" if count_O > 0 else "N/A",
            "C_items": c_items,
            "E_items": e_items,
            "M_items": m_items
        }
        
    return results
  
  