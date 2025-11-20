from typing import Dict

Asthma: Dict[str, Dict[str, bool]] = {
  "history_taking": {
    "present_illness": {
      "question1": "True",
      "question2": "True",
      "question3": "True",
      "question4": "True",
      "question5": "True",
      "question6": "False",
      "question7": "False",
      "question8": "False",
      "question9": "True",
      "question10": "False"
    },
    "past_medical_history": {
      "question1": {
        "question1a": "True",
        "question1b": "True"
      },
      "question2": {
        "question2a": "False",
        "question2b": "False"
      },
      "question3": "True",
      "question4": "False",
      "question5": "False",
      "question6": "False"
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
        "question1a": "True",
        "question1b": "True"
      }
    },
    "family_history": {
      "question1": {
        "question1a": "True",
        "question1b": "True"
      },
      "question2": "False",
      "question3": {
        "question3a": "False",
        "question3b": "False"
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
      "question1": "False",
      "question2": "True",
      "question3": "False",
      "question4": "False",
      "question5": "True",
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
        "nutritional_status": "False"
      },
      "cardiopulmonary_and_circulatory_clues": {
        "cyanosis": "True",
        "dyspnea": "True",
        "edema": "False"
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
        "septum_and_discharge": "True",
        "sinus_tenderness": "True"
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
        "tactile_fremitus": "False"
      },
      "percussion": "True",
      "auscultation": {
        "breath_sounds_intensity": "True",
        "adventitious_sounds": "True"
      }
    },
    "cardiovascular_system": {
      "JVP_assessment": "False",
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
        "extremities_color_and_trophic_changes": "True",
        "extremities_temperature_and_cap_refill": "False",
        "extremities_edema": "False"
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
      "CBC": ["True", "True", "False"],
      "ESR/CRP": "True",
      "BMP": "False",
      "LFTs": "False",
      "VBG": "True"
    },
    "specialized_lung_tests": {
      "Sputum_analysis": "False",
      "Sputum_AFB": "False",
      "a1_antitrypsin_level": "False",
      "D_dimer": "False",
      "BNP/NT_proBNP": "False"
    },
    "immunity_and_serology": {
      "HIV_test": "False",
      "Autoimmune_pannel_ANA_ANCA": "True"
    },
    "simple_imaging": {
      "Chest_X_Ray": {
        "PA": "True",
        "Lateral": "True"
      }
    },
    "advanced_imaging": {
      "Chest_CT_CTPA": "False",
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
    "disease2": "True",
    "disease3": "True",
    "disease4": "False",
    "disease5": "False",
    "disease6": "True",
    "disease7": "False",
    "disease8": "False"
  }
}

Pneumonia: Dict[str, Dict[str, bool]] = {
  "history_taking": {
    "present_illness": {
      "question1": "True",
      "question2": "True",
      "question3": "True",
      "question4": "True",
      "question5": "False",
      "question6": "True",
      "question7": "True",
      "question8": "False",
      "question9": "False",
      "question10": "True"
    },
    "past_medical_history": {
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
        "question1a": "True",
        "question1b": "True"
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
        "question1a": "True",
        "question1b": "True"
      },
      "question2": "True",
      "question3": {
        "question3a": "False",
        "question3b": "False"
      },
      "question4": "False"
    },
    "ROS": {
      "question1": "True",
      "question2": "False",
      "question3": "True",
      "question4": "False",
      "question5": "True",
      "question6": "True",
      "question7": "True",
      "question8": "True",
      "question9": "False",
      "question10": "True",
      "question11": "True",
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
        "nutritional_status": "False"
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
        "pharynx_and_tonsils": "True"
      },
      "neck_and_lymphatics": {
        "inspection": "False",
        "tracheal_position": "False",
        "thyroid_gland": "False",
        "carotid_bruit": "False",
        "lymph_nodes_size_consistency": "True",
        "lymph_nodes_mobility_tenderness": "True"
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
        "extremities_temperature_and_cap_refill": "True",
        "extremities_edema": "True"
      }
    },
    "abdominal_system": {
      "inspection": "True",
      "auscultation": {
        "bowel_sounds": "True",
        "vascular_bruits": "False"
      },
      "percussion": {
        "general": "False",
        "organ_borders": "True"
      },
      "palpation": {
        "superficial_tenderness": "True",
        "deep_masses_and_organs": "True",
        "peritoneal_signs": "False"
      }
    },
    "neurological": {
      "mental_status_and_LOC": "True",
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
      "CBC": [
        "True",
        "True",
        "True"
      ],
      "ESR/CRP": "True",
      "BMP": "True",
      "LFTs": "True",
      "VBG": "True"
    },
    "specialized_lung_tests": {
      "Sputum_analysis": "True",
      "Sputum_AFB": "True",
      "a1_antitrypsin_level": "False",
      "D_dimer": "False",
      "BNP/NT_proBNP": "True"
    },
    "immunity_and_serology": {
      "HIV_test": "True",
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
      "Spirometry": "False",
      "peak_flow": "False",
      "plethysmography": "False"
    },
    "procedures": {
      "Bronchoscopy": "True",
      "torachonthesis": "True"
   }
  },
  "differential_diagnosis": {
    "disease1": "False",
    "disease2": "True",
    "disease3": "True",
    "disease4": "False",
    "disease5": "False",
    "disease6": "False",
    "disease7": "True",
    "disease8": "True"
  }
}

COPD: Dict[str, Dict[str, bool]] = {
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

PTE: Dict[str, Dict[str, bool]] = {
  "history_taking": {
    "present_illness": {
      "question1": "True",
      "question2": "True",
      "question3": "True",
      "question4": "True",
      "question5": "False",
      "question6": "True",
      "question7": "True",
      "question8": "True",
      "question9": "True",
      "question10": "False"
    },
    "past_medical_history": {
      "question1": {
        "question1a": "True",
        "question1b": "True"
      },
      "question2": {
        "question2a": "True",
        "question2b": "True"
      },
      "question3": "True",
      "question4": "True",
      "question5": "False",
      "question6": "False"
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
        "question1a": "True",
        "question1b": "True"
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
      "question10": "True",
      "question11": "True",
      "question12": "False",
      "question13": "False",
      "question14": "True"
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
        "nutritional_status": "False"
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
        "chest_expansion": "False",
        "tactile_fremitus": "False"
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
        "precordial_palpation_heave_thrill": "True",
        "pmi_assessment": "False"
      },
      "auscultation": {
        "heart_sounds_s1_s2": "True",
        "extra_sounds_s3_s4_murmurs": "True"
      },
      "peripheral_pulses_and_extremities": {
        "peripheral_pulses_symmetry_and_quality": "True",
        "extremities_color_and_trophic_changes": "True",
        "extremities_temperature_and_cap_refill": "True",
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
      "mental_status_and_LOC": "True",
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
      "CBC": [
        "True",
        "True",
        "True"
      ],
      "ESR/CRP": "True",
      "BMP": "True",
      "LFTs": "True",
      "VBG": "True"
    },
    "specialized_lung_tests": {
      "Sputum_analysis": "False",
      "Sputum_AFB": "False",
      "a1_antitrypsin_level": "False",
      "D_dimer": "True",
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
      "Spirometry": "False",
      "peak_flow": "False",
      "plethysmography": "False"
    },
    "procedures": {
      "Bronchoscopy": "False",
      "torachonthesis": "False"
}
  },
  "differential_diagnosis": {
    "disease1": "False",
    "disease2": "True",
    "disease3": "False",
    "disease4": "True",
    "disease5": "False",
    "disease6": "True",
    "disease7": "False",
    "disease8": "True"
  }
}

IPF: Dict[str, Dict[str, bool]] = {
  "history_taking": {
    "present_illness": {
      "question1": "True",
      "question2": "True",
      "question3": "True",
      "question4": "True",
      "question5": "False",
      "question6": "False",
      "question7": "False",
      "question8": "True",
      "question9": "True",
      "question10": "False"
    },
    "past_medical_history": {
      "question1": {
        "question1a": "True",
        "question1b": "True"
      },
      "question2": {
        "question2a": "True",
        "question2b": "True"
      },
      "question3": "False",
      "question4": "False",
      "question5": "True",
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
        "question3a": "False",
        "question3b": "False"
      }
    },
    "social_history": {
      "question1": {
        "question1a": "True",
        "question1b": "True"
      },
      "question2": "False",
      "question3": {
        "question3a": "True",
        "question3b": "True"
      },
      "question4": "False"
    },
    "ROS": {
      "question1": "False",
      "question2": "False",
      "question3": "False",
      "question4": "True",
      "question5": "True",
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
        "chest_shape_and_symmetry": "False"
      },
      "palpation": {
        "chest_expansion": "True",
        "tactile_fremitus": "False"
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
        "precordial_palpation_heave_thrill": "True",
        "pmi_assessment": "False"
      },
      "auscultation": {
        "heart_sounds_s1_s2": "True",
        "extra_sounds_s3_s4_murmurs": "True"
      },
      "peripheral_pulses_and_extremities": {
        "peripheral_pulses_symmetry_and_quality": "False",
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
      "CBC": [
        "True",
        "True",
        "False"
      ],
      "ESR/CRP": "True",
      "BMP": "True",
      "LFTs": "True",
      "VBG": "True"
    },
    "specialized_lung_tests": {
      "Sputum_analysis": "False",
      "Sputum_AFB": "False",
      "a1_antitrypsin_level": "False",
      "D_dimer": "False",
      "BNP/NT_proBNP": "True"
    },
    "immunity_and_serology": {
      "HIV_test": "False",
      "Autoimmune_pannel_ANA_ANCA": "True"
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
      "peak_flow": "False",
      "plethysmography": "True"
    },
    "procedures": {
      "Bronchoscopy": "True",
      "torachonthesis": "False"
}
  },
  "differential_diagnosis": {
    "disease1": "False",
    "disease2": "True",
    "disease3": "True",
    "disease4": "False",
    "disease5": "True",
    "disease6": "True",
    "disease7": "False",
    "disease8": "False"
  }
}

PH: Dict[str, Dict[str, bool]] = {
  "history_taking": {
    "present_illness": {
      "question1": "True",
      "question2": "False",
      "question3": "True",
      "question4": "False",
      "question5": "False",
      "question6": "True",
      "question7": "False",
      "question8": "False",
      "question9": "True",
      "question10": "True"
    },
    "past_medical_history": {
      "question1": {
        "question1a": "True",
        "question1b": "True"
      },
      "question2": {
        "question2a": "True",
        "question2b": "True"
      },
      "question3": "True",
      "question4": "False",
      "question5": "True",
      "question6": "False"
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
        "question3a": "False",
        "question3b": "False"
      }
    },
    "social_history": {
      "question1": {
        "question1a": "True",
        "question1b": "True"
      },
      "question2": "True",
      "question3": {
        "question3a": "False",
        "question3b": "False"
      },
      "question4": "False"
    },
    "ROS": {
      "question1": "False",
      "question2": "True",
      "question3": "False",
      "question4": "True",
      "question5": "True",
      "question6": "True",
      "question7": "True",
      "question8": "True",
      "question9": "False",
      "question10": "True",
      "question11": "True",
      "question12": "True",
      "question13": "False",
      "question14": "True"
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
        "chest_expansion": "False",
        "tactile_fremitus": "False"
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
        "precordial_palpation_heave_thrill": "True",
        "pmi_assessment": "True"
      },
      "auscultation": {
        "heart_sounds_s1_s2": "True",
        "extra_sounds_s3_s4_murmurs": "True"
      },
      "peripheral_pulses_and_extremities": {
        "peripheral_pulses_symmetry_and_quality": "False",
        "extremities_color_and_trophic_changes": "True",
        "extremities_temperature_and_cap_refill": "True",
        "extremities_edema": "True"
      }
    },
    "abdominal_system": {
      "inspection": "True",
      "auscultation": {
        "bowel_sounds": "False",
        "vascular_bruits": "False"
      },
      "percussion": {
        "general": "True",
        "organ_borders": "True"
      },
      "palpation": {
        "superficial_tenderness": "True",
        "deep_masses_and_organs": "True",
        "peritoneal_signs": "True"
      }
    },
    "neurological": {
      "mental_status_and_LOC": "True",
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
      "CBC": [
        "True",
        "True",
        "True"
      ],
      "ESR/CRP": "True",
      "BMP": "True",
      "LFTs": "True",
      "VBG": "True"
    },
    "specialized_lung_tests": {
      "Sputum_analysis": "False",
      "Sputum_AFB": "False",
      "a1_antitrypsin_level": "True",
      "D_dimer": "True",
      "BNP/NT_proBNP": "True"
    },
    "immunity_and_serology": {
      "HIV_test": "True",
      "Autoimmune_pannel_ANA_ANCA": "True"
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
    "disease1": "False",
    "disease2": "False",
    "disease3": "True",
    "disease4": "True",
    "disease5": "True",
    "disease6": "True",
    "disease7": "False",
    "disease8": "False"
  }
}

Pleural_Effusion: Dict[str, Dict[str, bool]] = {
  "history_taking": {
    "present_illness": {
      "question1": "True",
      "question2": "True",
      "question3": "True",
      "question4": "True",
      "question5": "False",
      "question6": "True",
      "question7": "True",
      "question8": "True",
      "question9": "True",
      "question10": "True"
    },
    "past_medical_history": {
      "question1": {
        "question1a": "True",
        "question1b": "True"
      },
      "question2": {
        "question2a": "True",
        "question2b": "True"
      },
      "question3": "True",
      "question4": "True",
      "question5": "False",
      "question6": "False"
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
        "question1a": "False",
        "question1b": "False"
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
      "question2": "True",
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
      "question8": "True",
      "question9": "True",
      "question10": "True",
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
        "sclera_and_conjunctiva": "True",
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
        "tracheal_position": "True",
        "thyroid_gland": "False",
        "carotid_bruit": "False",
        "lymph_nodes_size_consistency": "True",
        "lymph_nodes_mobility_tenderness": "True"
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
        "extra_sounds_s3_s4_murmurs": "True"
      },
      "peripheral_pulses_and_extremities": {
        "peripheral_pulses_symmetry_and_quality": "True",
        "extremities_color_and_trophic_changes": "False",
        "extremities_temperature_and_cap_refill": "False",
        "extremities_edema": "True"
      }
    },
    "abdominal_system": {
      "inspection": "True",
      "auscultation": {
        "bowel_sounds": "False",
        "vascular_bruits": "False"
      },
      "percussion": {
        "general": "True",
        "organ_borders": "True"
      },
      "palpation": {
        "superficial_tenderness": "True",
        "deep_masses_and_organs": "True",
        "peritoneal_signs": "False"
      }
    },
    "neurological": {
      "mental_status_and_LOC": "True",
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
      "CBC": [
        "True",
        "True",
        "True"
      ],
      "ESR/CRP": "True",
      "BMP": "True",
      "LFTs": "True",
      "VBG": "True"
    },
    "specialized_lung_tests": {
      "Sputum_analysis": "True",
      "Sputum_AFB": "True",
      "a1_antitrypsin_level": "False",
      "D_dimer": "True",
      "BNP/NT_proBNP": "True"
    },
    "immunity_and_serology": {
      "HIV_test": "True",
      "Autoimmune_pannel_ANA_ANCA": "True"
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
      "Pet_scan": "True"
    },
    "functional_tests": {
      "Spirometry": "False",
      "peak_flow": "False",
      "plethysmography": "False"
    },
    "procedures": {
      "Bronchoscopy": "False",
      "torachonthesis": "True"
}
  },
  "differential_diagnosis": {
    "disease1": "False",
    "disease2": "True",
    "disease3": "False",
    "disease4": "True",
    "disease5": "False",
    "disease6": "True",
    "disease7": "True",
    "disease8": "False"
  }
}

ARDS: Dict[str, Dict[str, bool]] = {
  "history_taking": {
    "present_illness": {
      "question1": "True",
      "question2": "True",
      "question3": "True",
      "question4": "True",
      "question5": "False",
      "question6": "True",
      "question7": "True",
      "question8": "True",
      "question9": "False",
      "question10": "False"
    },
    "past_medical_history": {
      "question1": {
        "question1a": "True",
        "question1b": "True"
      },
      "question2": {
        "question2a": "True",
        "question2b": "True"
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
        "question1a": "False",
        "question1b": "False"
      },
      "question2": "True",
      "question3": {
        "question3a": "False",
        "question3b": "False"
      }
    },
    "social_history": {
      "question1": {
        "question1a": "True",
        "question1b": "True"
      },
      "question2": "True",
      "question3": {
        "question3a": "True",
        "question3b": "True"
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
      "question8": "True",
      "question9": "False",
      "question10": "False",
      "question11": "True",
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
        "nutritional_status": "False"
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
        "sclera_and_conjunctiva": "True",
        "pupils_reaction": "True",
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
        "lymph_nodes_size_consistency": "True",
        "lymph_nodes_mobility_tenderness": "True"
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
        "precordial_palpation_heave_thrill": "True",
        "pmi_assessment": "False"
      },
      "auscultation": {
        "heart_sounds_s1_s2": "True",
        "extra_sounds_s3_s4_murmurs": "True"
      },
      "peripheral_pulses_and_extremities": {
        "peripheral_pulses_symmetry_and_quality": "True",
        "extremities_color_and_trophic_changes": "True",
        "extremities_temperature_and_cap_refill": "True",
        "extremities_edema": "True"
      }
    },
    "abdominal_system": {
      "inspection": "True",
      "auscultation": {
        "bowel_sounds": "True",
        "vascular_bruits": "False"
      },
      "percussion": {
        "general": "True",
        "organ_borders": "True"
      },
      "palpation": {
        "superficial_tenderness": "True",
        "deep_masses_and_organs": "True",
        "peritoneal_signs": "True"
      }
    },
    "neurological": {
      "mental_status_and_LOC": "True",
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
      "CBC": [
        "True",
        "True",
        "True"
      ],
      "ESR/CRP": "True",
      "BMP": "True",
      "LFTs": "True",
      "VBG": "True"
    },
    "specialized_lung_tests": {
      "Sputum_analysis": "True",
      "Sputum_AFB": "True",
      "a1_antitrypsin_level": "False",
      "D_dimer": "True",
      "BNP/NT_proBNP": "True"
    },
    "immunity_and_serology": {
      "HIV_test": "True",
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
      "Spirometry": "False",
      "peak_flow": "False",
      "plethysmography": "False"
    },
    "procedures": {
      "Bronchoscopy": "True",
      "torachonthesis": "True"
 }
  },
  "differential_diagnosis": {
    "disease1": "False",
    "disease2": "True",
    "disease3": "False",
    "disease4": "True",
    "disease5": "False",
    "disease6": "False",
    "disease7": "True",
    "disease8": "True"
  }
}

OPTIMAL_SCENARIO = {
    "Asthma": Asthma,
    "Pneumonia": Pneumonia,
    "COPD": COPD,
    "PTE": PTE,
    "IPF": IPF,
    "PH": PH,
    "Pleural_Effusion": Pleural_Effusion,
    "ARDS": ARDS
}
