import json
import sys

# 1. Import Disease Scenarios
# (فرض بر این است که فایل‌ها در همین پوشه قرار دارند)
from .asthma import *
from .pte import *
from .ph import *
from .copd import *
from .ipf import *
from .pneumenia import *

# 2. Import Evaluator Class
from .feedback import ClinicalEvaluator

# 3. Create a Lookup Dictionary
# این دیکشنری کمک می‌کند تا با داشتن نام بیماری به صورت رشته متنی، دیکشنری متناظر آن را پیدا کنیم
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
        "ph_left_heart": PH_LEFT_HEART,
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
    "Pneumonia": { # توجه: نام فایل pneumenia.py است اما اینجا اصلاح شده خوانده میشود
        "atypical_walking": PNEUMENIA_ATYPICAL_WALKING,
        "complicated_effusion": PNEUMENIA_COMPLICATED_EFFUSION,
        "typical_lobar": PNEUMENIA_TYPICAL_LOBAR
    }
}

# 4. The Student Log (داده‌های ورودی شما)
STUDENT_LOG = {
  "history_taking": {
    "present_illness": {
      "question1": "14:55",
      "question2": "14:50",
      "question3": "14:45",
      "question4": "14:40",
      "question5": "14:35",
      "question6": "14:30",
      "question7": "14:25",
      "question8": "14:20" 
    },
    "past_medical_history": {
      "question1": { "question1a": "14:10", "question1b": "14:05" },
      "question2": { "question2a": "14:00" },
      "question3": "13:50"
    },
    "drug_history": {
      "question1": {
        "question1a": "13:40",
        "question1b": "13:35"
      }
    },
    "allergies": { "question1": { "question1a": "13:30" } },
    "family_history": {
      "question1": { "question1a": "13:20" }
    },
    "social_history": {
      "question1": { "question1a": "13:10" },
      "question2": "13:00" 
    },
    "ros": {
      "question1": "12:50", 
      "question6": "12:40",
      "question7": "12:30"
    }
  },
  "physical_exam": {
    "vital_signs": {
      "BP": "11:00",
      "T": "10:50",
      "PR": "10:45",
      "RR": "10:40",
      "SpO2": "10:35"
    },
    "general_appearance": {
      "mood_and_behavior": "10:20",
      "overall_appearance": "10:15",
      "cardiopulmonary_and_circulatory_clues": { 
        "dyspnea": "10:10", 
        "cyanosis": "10:05" 
      }
    },
    "head_and_neck": {
      "neck_and_lymphatics": {
        "inspection": "09:45"
      }
    },
    "respiratory_system": {
      "inspection": { "chest_shape_and_symmetry": "09:30" },
      "palpation": { "chest_expansion": "09:20" }, 
      "percussion": "09:10",
      "auscultation": { 
        "breath_sounds_intensity": "09:00", 
        "adventitious_sounds": "08:50" 
      }
    },
    "cardiovascular_system": {
      "auscultation": { "heart_sounds_s1_s2": "08:30" }
    },
    "abdominal_system": {
      "inspection": "08:00",
      "palpation": { "superficial_tenderness": "07:50" } 
    }
  },
  "paraclinic": {
    "basic_blood_tests": {
      "BMP": { "Na": "06:30", "BUN": "06:30", "Cr": "06:30" },
      "CBC": { "Hb": "06:15", "WBC": "06:15", "Plt": "06:15" },
      "ESR": "06:00",
      "VBG": { "pH": "05:45" }
    },
    "specialized_lung_tests": {
      "D_dimer": "05:30",
      "BNP_NT_proBNP": "05:15" 
    },
    "simple_imaging": {
      "Chest_X_Ray": { "PA_Lateral_Findings_and_Effusion": "04:30" }
    },
    "advanced_imaging": {
      "Chest_CT_CTPA": { "Lung_Parenchyma_and_Pleura": "04:15" } 
    },
    "functional_tests": {
      "peak_flow": "04:00"
    }
  }
}

def generate_feedback(disease_category, specific_scenario_key, student_log):
    # 1. Fetch the optimal scenario dictionary
    try:
        optimal_scenario = SCENARIO_MAP[disease_category][specific_scenario_key]
    except KeyError:
        return {"error": f"Scenario {disease_category} -> {specific_scenario_key} not found."}

    # 2. Instantiate the Evaluator
    evaluator = ClinicalEvaluator(optimal_scenario, student_log)

    # 3. Run Evaluation Logic
    final_score_percent = evaluator.evaluate_performance()
    duration_seconds, start_time = evaluator.calculate_duration()
    time_analysis = evaluator.analyze_time_performance(duration_seconds, evaluator.total_time_seconds)
    category = evaluator.get_category(final_score_percent)

    # 4. Construct the Final Output JSON
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
            "total": 100
        },
        "time_management": {
            "duration_formatted": evaluator.format_time(duration_seconds),
            "total_allowed_formatted": "15:00",
            "analysis": time_analysis
        }
    }
    
    return output
