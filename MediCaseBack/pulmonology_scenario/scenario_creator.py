from .pneumonia_data import PneumoniaDataGenerator
from .copd_data import COPDDataGenerator
from .history_taking_creator import history_taking_creator
import random
import json

def create_full_pneumonia_case(target_disease):
    paraclinic_generator = PneumoniaDataGenerator()
    paraclinic_output = paraclinic_generator.generate_paraclinic_case()
    
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
    
    return final_case

def create_full_copd_case(target_disease):
    paraclinic_generator = COPDDataGenerator()
    paraclinic_output = paraclinic_generator.generate_paraclinic_case()
    
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
    
    return final_case


case = {
    "COPD": create_full_copd_case,
    "Pneumonia": create_full_pneumonia_case
}


OPTIMAL_SCENARIO = ["Pneumonia", "COPD"]
#["Asthma", "PTE", "IPF", "PH", "Pleural_Effusion", "ARDS"]

def scenario_creator():
    target_disease = random.choice(OPTIMAL_SCENARIO)
    return case[f"{target_disease}"](target_disease), target_disease
