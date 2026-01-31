ASTHMA_EXERCISE_INDUCED = {
    "history_taking": {
      "present_illness": {
        "question1": "true",
        "question2": "true",
        "question3": "true",
        "question4": "true",
        "question5": "true",
        "question6": "true",
        "question7": "false",
        "question8": "false",
        "question9": "false",
        "question10": "false"
      },
      "past_medical_history": {
        "question1": { "question1a": "true", "question1b": "false" },
        "question2": { "question2a": "false", "question2b": "false" },
        "question3": "false",
        "question4": "false",
        "question5": "false",
        "question6": "false"
      },
      "drug_history": {
        "question1": {
          "question1a": "true",
          "question1b": "false",
          "question1c": "false"
        },
        "question2": "false"
      },
      "allergies": {
        "question1": { "question1a": "true", "question1b": "true" }
      },
      "family_history": {
        "question1": { "question1a": "true", "question1b": "false" },
        "question2": "false",
        "question3": { "question3a": "false", "question3b": "false" }
      },
      "social_history": {
        "question1": { "question1a": "true", "question1b": "true" },
        "question2": "false",
        "question3": { "question3a": "false", "question3b": "false" },
        "question4": "true"
      },
      "ros": {
        "question1": "false",
        "question2": "false",
        "question3": "false",
        "question4": "false",
        "question5": "false",
        "question6": "true",
        "question7": "true",
        "question8": "false",
        "question9": "false",
        "question10": "false",
        "question11": "false",
        "question12": "false",
        "question13": "false",
        "question14": "false"
      }
    },
    "physical_exam": {
      "vital_signs": {
        "BP": "true",
        "T": "true",
        "PR": "true",
        "RR": "true",
        "SpO2": "true",
        "GCS": "true"
      },
      "general_appearance": {
        "mood_and_behavior": "true",
        "overall_appearance": "true",
        "posture_and_position": "false",
        "level_of_consciousness": "true",
        "cardiopulmonary_and_circulatory_clues": {
          "edema": "false",
          "dyspnea": "true",
          "cyanosis": "false"
        }
      },
      "head_and_neck": {
        "head_and_face": {
          "symmetry_and_lesions": "false",
          "tenderness": "false"
        },
        "eyes": {
          "sclera_and_conjunctiva": "false",
          "pupils_reaction": "false",
          "extraocular_movements": "false"
        },
        "ears": {
          "external_and_tenderness": "false",
          "eardrum_appearance": "false"
        },
        "nose_and_sinuses": {
          "septum_and_discharge": "false",
          "sinus_tenderness": "false"
        },
        "mouth_and_pharynx": {
          "oral_mucosa_and_lesions": "false",
          "pharynx_and_tonsils": "false"
        },
        "neck_and_lymphatics": {
          "inspection": "true",
          "tracheal_position": "false",
          "thyroid_gland": "false",
          "carotid_bruit": "false",
          "lymph_nodes_size_consistency": "false",
          "lymph_nodes_mobility_tenderness": "false"
        }
      },
      "respiratory_system": {
        "inspection": {
          "accessory_muscles": "false",
          "chest_shape_and_symmetry": "true"
        },
        "palpation": { "chest_expansion": "true", "tactile_fremitus": "false" },
        "percussion": "true",
        "auscultation": {
          "breath_sounds_intensity": "true",
          "adventitious_sounds": "true"
        }
      },
      "cardiovascular_system": {
        "JVP_assessment": "false",
        "palpation": {
          "precordial_palpation_heave_thrill": "false",
          "pmi_assessment": "false"
        },
        "auscultation": {
          "heart_sounds_s1_s2": "true",
          "extra_sounds_s3_s4_murmurs": "false"
        },
        "2_pulses_and_extremities": {
          "peripheral_pulses_symmetry_and_quality": "true",
          "extremities_color_and_trophic_changes": "false",
          "extremities_temperature_and_cap_refill": "true",
          "extremities_edema": "false"
        }
      },
      "abdominal_system": {
        "inspection": "false",
        "auscultation": { "bowel_sounds": "false", "vascular_bruits": "false" },
        "percussion": { "general": "false", "organ_borders": "false" },
        "palpation": {
          "superficial_tenderness": "false",
          "deep_masses_and_organs": "false"
        },
        "peritoneal_signs": "false"
      },
      "neurological": {
        "mental_status_and_LOC": "true",
        "cranial_nerves": "false",
        "motor_strength_and_tone": "false",
        "involuntary_movements": "false",
        "sensory_light_touch_and_pain": "false",
        "deep_tendon_reflexes": "false",
        "coordination_and_gait": "false"
      },
      "musculoskeletal_system": {
        "inspection": { "joints": "false", "muscles": "false" },
        "palpation": { "tenderness_and_crepitus": "false" },
        "range_of_motion_active_passive": "false",
        "stability_and_function": "false"
      }
    },
    "paraclinic": {
      "basic_blood_tests": {
        "BMP": { "Na": "true", "BUN": "true", "Cr": "true" },
        "CBC": { "WBC": "false", "Hb": "true", "Plt": "false" },
        "ESR": "false",
        "CRP": "false",
        "VBG": { "pH": "false", "PCO2": "false", "HCO3": "false" },
        "LFTs": { "ALT": "false", "AST": "false" }
      },
      "specialized_lung_tests": {
        "D_dimer": "false",
        "Sputum_AFB": "false",
        "BNP_NT_proBNP": "false",
        "Sputum_analysis": { "Gram_Stain": "false", "Sample_Quality": "false" },
        "a1_antitrypsin_level": "false"
      },
      "immunity_and_serology": {
        "HIV_test": "false",
        "Autoimmune_pannel_ANA_ANCA": "false"
      },
      "simple_imaging": {
        "Chest_X_Ray": { "PA_Lateral_Findings_and_Effusion": "true" }
      },
      "advanced_imaging": {
        "Chest_CT_CTPA": { "Lung_Parenchyma_and_Pleura": "false" }
      },
      "functional_tests": {
        "dlco": "false",
        "peak_flow": "true",
        "Spirometry": {
          "Result": { "FEV1": "true", "FVC": "true", "FEV1/FVC": "true" },
          "reversibility": "true"
        },
        "plethysmography": "false"
      },
      "procedures": {
        "Bronchoscopy": "false",
        "torachonthesis": {
          "Serum": { "Protein": "false", "LDH": "false", "Albumin": "false" },
          "Fluid": { "Protein": "false", "LDH": "false", "Albumin": "false" }
        }
      }
    },
    "differential_diagnosis": {
      "disease1": "true",
      "disease2": "false",
      "disease3": "false",
      "disease4": "false",
      "disease5": "false",
      "disease6": "false"
    },
    "final_diagnosis": {
      "disease": "Asthma"
    }
  }


ASTHMA_MILD_ALLERGIC = {
    "history_taking": {
      "present_illness": {
        "question1": "true",
        "question2": "true",
        "question3": "true",
        "question4": "true",
        "question5": "true",
        "question6": "true",
        "question7": "false",
        "question8": "false",
        "question9": "true",
        "question10": "false"
      },
      "past_medical_history": {
        "question1": { "question1a": "true", "question1b": "true" },
        "question2": { "question2a": "true", "question2b": "false" },
        "question3": "true",
        "question4": "false",
        "question5": "true",
        "question6": "false"
      },
      "drug_history": {
        "question1": {
          "question1a": "true",
          "question1b": "true",
          "question1c": "true"
        },
        "question2": "true"
      },
      "allergies": { "question1": { "question1a": "true", "question1b": "true" } },
      "family_history": {
        "question1": { "question1a": "true", "question1b": "true" },
        "question2": "false",
        "question3": { "question3a": "false", "question3b": "false" }
      },
      "social_history": {
        "question1": { "question1a": "true", "question1b": "true" },
        "question2": "false",
        "question3": { "question3a": "false", "question3b": "false" },
        "question4": "true"
      },
      "ros": {
        "question1": "false",
        "question2": "true",
        "question3": "false",
        "question4": "true",
        "question5": "true",
        "question6": "true",
        "question7": "true",
        "question8": "false",
        "question9": "false",
        "question10": "false",
        "question11": "false",
        "question12": "false",
        "question13": "false",
        "question14": "false"
      }
    },
    "physical_exam": {
      "vital_signs": {
        "BP": "true",
        "T": "true",
        "PR": "true",
        "RR": "true",
        "SpO2": "true",
        "GCS": "true"
      },
      "general_appearance": {
        "mood_and_behavior": "true",
        "overall_appearance": "true",
        "posture_and_position": "false",
        "level_of_consciousness": "true",
        "cardiopulmonary_and_circulatory_clues": {
          "edema": "false",
          "dyspnea": "true",
          "cyanosis": "false"
        }
      },
      "head_and_neck": {
        "head_and_face": { "symmetry_and_lesions": "false", "tenderness": "true" },
        "eyes": {
          "sclera_and_conjunctiva": "true",
          "pupils_reaction": "false",
          "extraocular_movements": "false"
        },
        "ears": {
          "external_and_tenderness": "false",
          "eardrum_appearance": "true"
        },
        "nose_and_sinuses": {
          "septum_and_discharge": "true",
          "sinus_tenderness": "true"
        },
        "mouth_and_pharynx": {
          "oral_mucosa_and_lesions": "true",
          "pharynx_and_tonsils": "true"
        },
        "neck_and_lymphatics": {
          "inspection": "true",
          "tracheal_position": "false",
          "thyroid_gland": "false",
          "carotid_bruit": "false",
          "lymph_nodes_size_consistency": "false",
          "lymph_nodes_mobility_tenderness": "false"
        }
      },
      "respiratory_system": {
        "inspection": {
          "accessory_muscles": "true",
          "chest_shape_and_symmetry": "true"
        },
        "palpation": { "chest_expansion": "true", "tactile_fremitus": "false" },
        "percussion": "true",
        "auscultation": {
          "breath_sounds_intensity": "true",
          "adventitious_sounds": "true"
        }
      },
      "cardiovascular_system": {
        "JVP_assessment": "false",
        "palpation": {
          "precordial_palpation_heave_thrill": "false",
          "pmi_assessment": "false"
        },
        "auscultation": {
          "heart_sounds_s1_s2": "true",
          "extra_sounds_s3_s4_murmurs": "false"
        },
        "2_pulses_and_extremities": {
          "peripheral_pulses_symmetry_and_quality": "true",
          "extremities_color_and_trophic_changes": "false",
          "extremities_temperature_and_cap_refill": "true",
          "extremities_edema": "false"
        }
      },
      "abdominal_system": {
        "inspection": "false",
        "auscultation": { "bowel_sounds": "false", "vascular_bruits": "false" },
        "percussion": { "general": "false", "organ_borders": "false" },
        "palpation": {
          "superficial_tenderness": "false",
          "deep_masses_and_organs": "false"
        },
        "peritoneal_signs": "false"
      },
      "neurological": {
        "mental_status_and_LOC": "true",
        "cranial_nerves": "false",
        "motor_strength_and_tone": "false",
        "involuntary_movements": "false",
        "sensory_light_touch_and_pain": "false",
        "deep_tendon_reflexes": "false",
        "coordination_and_gait": "false"
      },
      "musculoskeletal_system": {
        "inspection": { "joints": "false", "muscles": "false" },
        "palpation": { "tenderness_and_crepitus": "false" },
        "range_of_motion_active_passive": "false",
        "stability_and_function": "false"
      }
    },
    "paraclinic": {
      "basic_blood_tests": {
        "BMP": { "Na": "true", "BUN": "true", "Cr": "true" },
        "CBC": { "WBC": "true", "Hb": "true", "Plt": "true" },
        "ESR": "false",
        "CRP": "false",
        "VBG": { "pH": "false", "PCO2": "false", "HCO3": "false" },
        "LFTs": { "ALT": "false", "AST": "false" }
      },
      "specialized_lung_tests": {
        "D_dimer": "false",
        "Sputum_AFB": "false",
        "BNP_NT_proBNP": "false",
        "Sputum_analysis": { "Gram_Stain": "false", "Sample_Quality": "false" },
        "a1_antitrypsin_level": "false"
      },
      "immunity_and_serology": {
        "HIV_test": "false",
        "Autoimmune_pannel_ANA_ANCA": "false"
      },
      "simple_imaging": {
        "Chest_X_Ray": { "PA_Lateral_Findings_and_Effusion": "true" }
      },
      "advanced_imaging": {
        "Chest_CT_CTPA": { "Lung_Parenchyma_and_Pleura": "false" }
      },
      "functional_tests": {
        "dlco": "false",
        "peak_flow": "true",
        "Spirometry": {
          "Result": { "FEV1": "true", "FVC": "true", "FEV1/FVC": "true" },
          "reversibility": "true"
        },
        "plethysmography": "false"
      },
      "procedures": {
        "Bronchoscopy": "false",
        "torachonthesis": {
          "Serum": { "Protein": "false", "LDH": "false", "Albumin": "false" },
          "Fluid": { "Protein": "false", "LDH": "false", "Albumin": "false" }
        }
      }
    },
    "differential_diagnosis": {
      "disease1": "true",
      "disease2": "false",
      "disease3": "true",
      "disease4": "false",
      "disease5": "false",
      "disease6": "false"
    },
    "final_diagnosis": {
      "disease": "Asthma"
    }
  }


ASTHMA_SEVERE_UNCONTROLLED = {
    "history_taking": {
      "present_illness": {
        "question1": "true", "question2": "true", "question3": "true", "question4": "true", "question5": "true",
        "question6": "true", "question7": "true", "question8": "true", "question9": "true", "question10": "false"
      },
      "past_medical_history": {
        "question1": { "question1a": "true", "question1b": "true" },
        "question2": { "question2a": "true", "question2b": "true" },
        "question3": "true", "question4": "false", "question5": "false", "question6": "false"
      },
      "drug_history": {
        "question1": { "question1a": "true", "question1b": "true", "question1c": "true" },
        "question2": "true"
      },
      "allergies": { "question1": { "question1a": "true", "question1b": "true" } },
      "family_history": {
        "question1": { "question1a": "true", "question1b": "false" },
        "question2": "false", "question3": { "question3a": "false", "question3b": "false" }
      },
      "social_history": {
        "question1": { "question1a": "true", "question1b": "true" },
        "question2": "false",
        "question3": { "question3a": "true", "question3b": "false" }, "question4": "false"
      },
      "ros": {
        "question1": "true", "question2": "false", "question3": "false", "question4": "false", "question5": "false",
        "question6": "true", "question7": "true", "question8": "false", "question9": "false", "question10": "false",
        "question11": "false", "question12": "true", "question13": "false", "question14": "false"
      }
    },
    "physical_exam": {
      "vital_signs": {
        "BP": "true", "T": "true", "PR": "true", "RR": "true", "SpO2": "true", "GCS": "true"
      },
      "general_appearance": {
        "mood_and_behavior": "true", "overall_appearance": "true", "posture_and_position": "true", "level_of_consciousness": "true",
        "cardiopulmonary_and_circulatory_clues": { "edema": "false", "dyspnea": "true", "cyanosis": "true" }
      },
      "head_and_neck": {
        "head_and_face": { "symmetry_and_lesions": "false", "tenderness": "false" },
        "eyes": { "sclera_and_conjunctiva": "false", "pupils_reaction": "false", "extraocular_movements": "false" },
        "ears": { "external_and_tenderness": "false", "eardrum_appearance": "false" },
        "nose_and_sinuses": { "septum_and_discharge": "false", "sinus_tenderness": "false" },
        "mouth_and_pharynx": { "oral_mucosa_and_lesions": "false", "pharynx_and_tonsils": "true" },
        "neck_and_lymphatics": {
          "inspection": "true", "tracheal_position": "true", "thyroid_gland": "false", "carotid_bruit": "false",
          "lymph_nodes_size_consistency": "false", "lymph_nodes_mobility_tenderness": "false"
        }
      },
      "respiratory_system": {
        "inspection": { "accessory_muscles": "true", "chest_shape_and_symmetry": "true" },
        "palpation": { "chest_expansion": "true", "tactile_fremitus": "true" },
        "percussion": "true",
        "auscultation": { "breath_sounds_intensity": "true", "adventitious_sounds": "true" }
      },
      "cardiovascular_system": {
        "JVP_assessment": "true",
        "palpation": { "precordial_palpation_heave_thrill": "false", "pmi_assessment": "false" },
        "auscultation": { "heart_sounds_s1_s2": "true", "extra_sounds_s3_s4_murmurs": "false" },
        "2_pulses_and_extremities": {
          "peripheral_pulses_symmetry_and_quality": "true", "extremities_color_and_trophic_changes": "false",
          "extremities_temperature_and_cap_refill": "true", "extremities_edema": "false"
        }
      },
      "abdominal_system": {
        "inspection": "false", "auscultation": { "bowel_sounds": "false", "vascular_bruits": "false" },
        "percussion": { "general": "false", "organ_borders": "false" },
        "palpation": { "superficial_tenderness": "false", "deep_masses_and_organs": "false" },
        "peritoneal_signs": "false"
      },
      "neurological": {
        "mental_status_and_LOC": "true", "cranial_nerves": "false", "motor_strength_and_tone": "false",
        "involuntary_movements": "false", "sensory_light_touch_and_pain": "false", "deep_tendon_reflexes": "false",
        "coordination_and_gait": "false"
      },
      "musculoskeletal_system": {
        "inspection": { "joints": "false", "muscles": "false" },
        "palpation": { "tenderness_and_crepitus": "false" },
        "range_of_motion_active_passive": "false", "stability_and_function": "false"
      }
    },
    "paraclinic": {
      "basic_blood_tests": {
        "BMP": { "Na": "true", "BUN": "true", "Cr": "true" },
        "CBC": { "WBC": "true", "Hb": "true", "Plt": "true" },
        "ESR": "false", "CRP": "true",
        "VBG": { "pH": "true", "PCO2": "true", "HCO3": "true" },
        "LFTs": { "ALT": "false", "AST": "false" }
      },
      "specialized_lung_tests": {
        "D_dimer": "true", "Sputum_AFB": "false", "BNP_NT_proBNP": "true",
        "Sputum_analysis": { "Gram_Stain": "false", "Sample_Quality": "false" },
        "a1_antitrypsin_level": "false"
      },
      "immunity_and_serology": { "HIV_test": "false", "Autoimmune_pannel_ANA_ANCA": "false" },
      "simple_imaging": { "Chest_X_Ray": { "PA_Lateral_Findings_and_Effusion": "true" } },
      "advanced_imaging": { "Chest_CT_CTPA": { "Lung_Parenchyma_and_Pleura": "false" } },
      "functional_tests": {
        "dlco": "false", "peak_flow": "true",
        "Spirometry": { "Result": { "FEV1": "true", "FVC": "true", "FEV1/FVC": "true" }, "reversibility": "true" },
        "plethysmography": "false"
      },
      "procedures": {
        "Bronchoscopy": "false",
        "torachonthesis": {
          "Serum": { "Protein": "false", "LDH": "false", "Albumin": "false" },
          "Fluid": { "Protein": "false", "LDH": "false", "Albumin": "false" }
        }
      }
    },
    "differential_diagnosis": {
      "disease1": "true",
      "disease2": "true",
      "disease3": "true",
      "disease4": "true",
      "disease5": "false",
      "disease6": "false"
    },
    "final_diagnosis": {
      "disease": "Asthma"
    }
  }
