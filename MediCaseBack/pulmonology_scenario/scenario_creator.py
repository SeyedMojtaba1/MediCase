from .pneumonia_data import PneumoniaDataGenerator
from .copd_data import COPDDataGenerator
from .asthma_data import AsthmaDataGenerator
from .pte_data import PTEDataGenerator
from .ipf_data import IPFDataGenerator
from .ph_data import PHDataGenerator
# from .ards_data import ARDSDataGenerator
from .history_taking_creator import history_taking_creator
import random
import json

def create_full_pneumonia_case(target_disease):
    paraclinic_generator = PneumoniaDataGenerator()
    paraclinic_output, type_disease = paraclinic_generator.generate_paraclinic_case()
    history_data = history_taking_creator(target_disease)
    final_patient_profile = paraclinic_output["patient_profile"]

    if "patient_profile" in history_data and "chief_complaint" in history_data["patient_profile"]:
        final_patient_profile["chief_complaint"] = history_data["patient_profile"]["chief_complaint"]
        final_history_taking = history_data["history_taking"]
        final_physical_exam = paraclinic_output["physical_exam"]
        final_paraclinic = paraclinic_output["paraclinic"]

    final_case = {
        "patient_profile": final_patient_profile,
        "history_taking": final_history_taking,
        "physical_exam": final_physical_exam,
        "paraclinic": final_paraclinic
    }
    return final_case, type_disease



def create_full_copd_case(target_disease):
    paraclinic_generator = COPDDataGenerator()
    paraclinic_output, type_disease = paraclinic_generator.generate_paraclinic_case()
    history_data= history_taking_creator(target_disease)
    final_patient_profile = paraclinic_output["patient_profile"]

    if "patient_profile" in history_data and "chief_complaint" in history_data["patient_profile"]:
        final_patient_profile["chief_complaint"] = history_data["patient_profile"]["chief_complaint"]
        final_history_taking = history_data["history_taking"]
        final_physical_exam = paraclinic_output["physical_exam"]
        final_paraclinic = paraclinic_output["paraclinic"]

    final_case = {
        "patient_profile": final_patient_profile,
        "history_taking": final_history_taking,
        "physical_exam": final_physical_exam,
        "paraclinic": final_paraclinic
    }
    return final_case, type_disease



def create_full_asthma_case(target_disease):
    paraclinic_generator = AsthmaDataGenerator()
    paraclinic_output, type_disease = paraclinic_generator.generate_paraclinic_case()
    history_data= history_taking_creator(target_disease)
    final_patient_profile = paraclinic_output["patient_profile"]

    if "patient_profile" in history_data and "chief_complaint" in history_data["patient_profile"]:
        final_patient_profile["chief_complaint"] = history_data["patient_profile"]["chief_complaint"]
        final_history_taking = history_data["history_taking"]
        final_physical_exam = paraclinic_output["physical_exam"]
        final_paraclinic = paraclinic_output["paraclinic"]

    final_case = {
        "patient_profile": final_patient_profile,
        "history_taking": final_history_taking,
        "physical_exam": final_physical_exam,
        "paraclinic": final_paraclinic
    }
    return final_case, type_disease



def create_full_pte_case(target_disease):
    paraclinic_generator = PTEDataGenerator()
    paraclinic_output, type_disease = paraclinic_generator.generate_paraclinic_case()
    history_data= history_taking_creator(target_disease)
    final_patient_profile = paraclinic_output["patient_profile"]

    if "patient_profile" in history_data and "chief_complaint" in history_data["patient_profile"]:
        final_patient_profile["chief_complaint"] = history_data["patient_profile"]["chief_complaint"]
        final_history_taking = history_data["history_taking"]
        final_physical_exam = paraclinic_output["physical_exam"]
        final_paraclinic = paraclinic_output["paraclinic"]

    final_case = {
        "patient_profile": final_patient_profile,
        "history_taking": final_history_taking,
        "physical_exam": final_physical_exam,
        "paraclinic": final_paraclinic
    }
    return final_case, type_disease



def create_full_ipf_case(target_disease):
    paraclinic_generator = IPFDataGenerator()
    paraclinic_output, type_disease = paraclinic_generator.generate_paraclinic_case()
    history_data= history_taking_creator(target_disease)
    final_patient_profile = paraclinic_output["patient_profile"]
    
    if "patient_profile" in history_data and "chief_complaint" in history_data["patient_profile"]:
        final_patient_profile["chief_complaint"] = history_data["patient_profile"]["chief_complaint"]
        final_history_taking = history_data["history_taking"]
        final_physical_exam = paraclinic_output["physical_exam"]
        final_paraclinic = paraclinic_output["paraclinic"]

    final_case = {
        "patient_profile": final_patient_profile,
        "history_taking": final_history_taking,
        "physical_exam": final_physical_exam,
        "paraclinic": final_paraclinic
    }
    return final_case, type_disease



def create_full_ph_case(target_disease):
    paraclinic_generator = PHDataGenerator()
    paraclinic_output, type_disease = paraclinic_generator.generate_paraclinic_case()
    history_data = history_taking_creator(target_disease)
    final_patient_profile = paraclinic_output["patient_profile"]   

    if "patient_profile" in history_data and "chief_complaint" in history_data["patient_profile"]:

        final_patient_profile["chief_complaint"] = history_data["patient_profile"]["chief_complaint"]
        final_history_taking = history_data["history_taking"]
        final_physical_exam = paraclinic_output["physical_exam"]
        final_paraclinic = paraclinic_output["paraclinic"]
    
    final_case = {
        "patient_profile": final_patient_profile,
        "history_taking": final_history_taking,
        "physical_exam": final_physical_exam,
        "paraclinic": final_paraclinic
    }
    return final_case, type_disease



# def create_full_ards_case(target_disease):
#     paraclinic_generator = ARDSDataGenerator()
#     paraclinic_output, type_disease = paraclinic_generator.generate_paraclinic_case()
#     history_data= history_taking_creator(target_disease)
#     final_patient_profile = paraclinic_output["patient_profile"]

#     if "patient_profile" in history_data and "chief_complaint" in history_data["patient_profile"]:
#         final_patient_profile["chief_complaint"] = history_data["patient_profile"]["chief_complaint"]
#         final_history_taking = history_data["history_taking"]
#         final_physical_exam = paraclinic_output["physical_exam"]
#         final_paraclinic = paraclinic_output["paraclinic"]

#     final_case = {
#         "patient_profile": final_patient_profile,
#         "history_taking": final_history_taking,
#         "physical_exam": final_physical_exam,
#         "paraclinic": final_paraclinic
#     }
#     return final_case

case = {
    "COPD": create_full_copd_case,
    "Pneumonia": create_full_pneumonia_case,
    "Asthma": create_full_asthma_case,
    "PTE": create_full_pte_case,
    "IPF": create_full_ipf_case,
    "PH": create_full_ph_case
    # "ARDS": create_full_ards_case
}


OPTIMAL_SCENARIO = ["Asthma", "Pneumonia", "COPD", "PTE", "IPF", "PH"]
# , "ARDS"

def scenario_creator():
    target_disease = random.choice(OPTIMAL_SCENARIO)
    case_data, type_disease = case[target_disease](target_disease)
    return case_data, target_disease, type_disease

# print(json.dumps(scenario_creator(), ensure_ascii=False))