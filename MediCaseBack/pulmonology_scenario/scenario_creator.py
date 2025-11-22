import getpass
import os
from langchain.chat_models import init_chat_model
# from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json
import random

from typing import List, Optional
from pydantic import BaseModel, Field

class PersonalInformation(BaseModel):
    first_name: str = Field(..., description="First Name")
    last_name: str = Field(..., description="Last Name")
    age: str = Field(..., description="Age (appropriate for disease prevalence)")
    gender: str = Field(..., description="Gender")
    occupation: str = Field(..., description="Occupation")
    place_of_birth: str = Field(..., description="Place Of Birth")
    place_of_residence: str = Field(..., description="Place Of Residence")
    marital_status: str = Field(..., description="Marital Status")

class VitalSign(BaseModel):
    BP: str = Field(..., description="Blood Pressure")
    T: str = Field(..., description="Temperature")
    PR: str = Field(..., description="Pulse Rate")
    RR: str = Field(..., description="Respiratory Rate")
    SpO2: str = Field(..., description="Saturation of O2")
    GCS: str = Field(..., description="Level of Consciousness")

class PatientProfile(BaseModel):
    personal_information: PersonalInformation
    chief_complaint: str = Field(..., description="Chief Complaint")
    vital_sign: VitalSign

class PresentIllness(BaseModel):
    question1: str
    question2: str
    question3: str
    question4: str
    question5: str
    question6: str
    question7: str
    question8: str
    question9: str
    question10: str

# --- Sub-models for nested questions ---
class PMHQuestion1(BaseModel):
    question1a: str
    question1b: str

class PMHQuestion2(BaseModel):
    question2a: str
    question2b: str

class PastMedicalHistory(BaseModel):
    question1: PMHQuestion1
    question2: PMHQuestion2
    question3: str
    question4: str
    question5: str
    question6: str

class DrugHistoryQuestion1(BaseModel):
    question1a: str
    question1b: str
    question1c: str

class DrugHistory(BaseModel):
    question1: DrugHistoryQuestion1
    question2: str

class AllergyQuestion1(BaseModel):
    question1a: str
    question1b: str

class Allergies(BaseModel):
    question1: AllergyQuestion1

class FHQuestion1(BaseModel):
    question1a: str
    question1b: str

class FHQuestion3(BaseModel):
    question3a: str
    question3b: str

class FamilyHistory(BaseModel):
    question1: FHQuestion1
    question2: str
    question3: FHQuestion3

class SHQuestion1(BaseModel):
    question1a: str
    question1b: str

class SHQuestion3(BaseModel):
    question3a: str
    question3b: str

class SocialHistory(BaseModel):
    question1: SHQuestion1
    question2: str
    question3: SHQuestion3
    question4: str

class ROS(BaseModel):
    question1: str
    question2: str
    question3: str
    question4: str
    question5: str
    question6: str
    question7: str
    question8: str
    question9: str
    question10: str
    question11: str
    question12: str
    question13: str
    question14: str

class HistoryTaking(BaseModel):
    present_illness: PresentIllness
    past_medical_history: PastMedicalHistory
    drug_history: DrugHistory
    allergies: Allergies
    family_history: FamilyHistory
    social_history: SocialHistory
    ros: ROS

class LevelOfConsciousnessMoodAndBehavior(BaseModel):
    level_of_consciousness: str
    mood: str
    behavior: str

class PostureAndPosition(BaseModel):
    position_of_comfort: str

class OverallAppearance(BaseModel):
    nutritional_status: str

class CardiopulmonaryAndCirculatoryClues(BaseModel):
    cyanosis: str
    dyspnea: str
    edema: str

class GeneralAppearance(BaseModel):
    level_of_consciousness_mood_and_behavior: LevelOfConsciousnessMoodAndBehavior
    posture_and_position: PostureAndPosition
    overall_appearance: OverallAppearance
    cardiopulmonary_and_circulatory_clues: CardiopulmonaryAndCirculatoryClues

class HeadAndFace(BaseModel):
    symmetry_and_lesions: str
    tenderness: str

class Eyes(BaseModel):
    sclera_and_conjunctiva: str
    pupils_reaction: str
    extraocular_movements: str

class Ears(BaseModel):
    external_and_tenderness: str
    eardrum_appearance: str

class NoseAndSinuses(BaseModel):
    septum_and_discharge: str
    sinus_tenderness: str

class MouthAndPharynx(BaseModel):
    oral_mucosa_and_lesions: str
    pharynx_and_tonsils: str

class NeckAndLymphatics(BaseModel):
    inspection: str
    tracheal_position: str
    thyroid_gland: str
    carotid_bruit: str
    lymph_nodes_size_consistency: str
    lymph_nodes_mobility_tenderness: str

class HeadAndNeck(BaseModel):
    head_and_face: HeadAndFace
    eyes: Eyes
    ears: Ears
    nose_and_sinuses: NoseAndSinuses
    mouth_and_pharynx: MouthAndPharynx
    neck_and_lymphatics: NeckAndLymphatics

class RespiratoryInspection(BaseModel):
    accessory_muscles: str
    chest_shape_and_symmetry: str

class RespiratoryPalpation(BaseModel):
    chest_expansion: str
    tactile_fremitus: str

class RespiratoryAuscultation(BaseModel):
    breath_sounds_intensity: str
    adventitious_sounds: str

class RespiratorySystem(BaseModel):
    inspection: RespiratoryInspection
    palpation: RespiratoryPalpation
    percussion: str
    auscultation: RespiratoryAuscultation

class CardiovascularPalpation(BaseModel):
    precordial_palpation_heave_thrill: str
    pmi_assessment: str

class CardiovascularAuscultation(BaseModel):
    heart_sounds_s1_s2: str
    extra_sounds_s3_s4_murmurs: str

class PeripheralPulsesAndExtremities(BaseModel):
    peripheral_pulses_symmetry_and_quality: str
    extremities_color_and_trophic_changes: str
    extremities_temperature_and_cap_refill: str
    extremities_edema: str

class CardiovascularSystem(BaseModel):
    JVP_assessment: str
    palpation: CardiovascularPalpation
    auscultation: CardiovascularAuscultation
    peripheral_pulses_and_extremities: PeripheralPulsesAndExtremities

class AbdominalAuscultation(BaseModel):
    bowel_sounds: str
    vascular_bruits: str

class AbdominalPercussion(BaseModel):
    general: str
    organ_borders: str

class AbdominalPalpation(BaseModel):
    superficial_tenderness: str
    deep_masses_and_organs: str

class AbdominalSystem(BaseModel):
    inspection: str
    auscultation: AbdominalAuscultation
    percussion: AbdominalPercussion
    palpation: AbdominalPalpation
    peritoneal_signs: str

class Neurological(BaseModel):
    mental_status_and_LOC: str
    cranial_nerves: str
    motor_strength_and_tone: str
    involuntary_movements: str
    sensory_light_touch_and_pain: str
    deep_tendon_reflexes: str
    coordination_and_gait: str

class MusculoskeletalInspection(BaseModel):
    joints: str
    muscles: str

class MusculoskeletalPalpation(BaseModel):
    tenderness_and_crepitus: str

class MusculoskeletalSystem(BaseModel):
    inspection: MusculoskeletalInspection
    palpation: MusculoskeletalPalpation
    range_of_motion_active_passive: str
    stability_and_function: str

class PhysicalExam(BaseModel):
    general_appearance: GeneralAppearance
    head_and_neck: HeadAndNeck
    respiratory_system: RespiratorySystem
    cardiovascular_system: CardiovascularSystem
    abdominal_system: AbdominalSystem
    neurological: Neurological
    musculoskeletal_system: MusculoskeletalSystem

class BasicBloodTests(BaseModel):
    CBC: List[str]
    ESR_CRP: str
    BMP: str
    LFTs: str
    VBG: str

class SpecializedLungTests(BaseModel):
    Sputum_analysis: str
    Sputum_AFB: str
    a1_antitrypsin_level: str
    D_dimer: str
    BNP_NT_proBNP: str

class ImmunityAndSerology(BaseModel):
    HIV_test: str
    Autoimmune_pannel_ANA_ANCA: str

class Spirometry(BaseModel):
    fev1: List[str]
    fvc: List[str]
    # "fev1/fvc" needs an alias because '/' is not allowed in python variables
    fev1_fvc: List[str] = Field(..., alias="fev1/fvc")

class DLCO(BaseModel):
    dlco: List[str]
    dlco_va_ratio: List[str] = Field(..., alias="dlco/va_ratio")

class Plethysmography(BaseModel):
    tls: List[str] = Field(..., description="Likely TLC in schema")
    rv: List[str]
    frc: List[str]
    rv_tlc_ratio: str = Field(..., alias="rv/tlc_ratio")

class FunctionalTests(BaseModel):
    Spirometry: Spirometry
    dlco: DLCO
    plethysmography: Plethysmography

class Torachocenthesis(BaseModel):
    pleural_fluid: List[str]
    serum: List[str]

class Procedures(BaseModel):
    Bronchoscopy: str
    torachocenthesis: Torachocenthesis

class Paraclinic(BaseModel):
    basic_blood_tests: BasicBloodTests
    specialized_lung_tests: SpecializedLungTests
    immunity_and_serology: ImmunityAndSerology
    functional_tests: FunctionalTests
    procedures: Procedures

# --- ROOT MODEL ---

class MedicalCase(BaseModel):
    patient_profile: PatientProfile
    history_taking: HistoryTaking
    physical_exam: PhysicalExam
    paraclinic: Paraclinic

# model = ChatVertexAI (
#   model="gemini-2.0-flash",
#   location="europe-north1",
#   base_url="https://api.avalai.ir/v1/chat/completions",
#   api_key="aa-P7j1uxWtVqqQRUoGGwZMqr8g7bI0azTMdDHhY9nNSdOYz23s",
# )

model = init_chat_model(
  model="gpt-4o-mini",
  base_url="https://api.avalai.ir/v1",
  api_key="aa-bFHSFoxDcvBLcr9tEpySz5SIjvlHGBAmJ3nqgKALEgt5w8YH",
)

OPTIMAL_SCENARIO = ["Asthma", "Pneumonia", "COPD", "PTE", "IPF", "PH", "Pleural_Effusion", "ARDS"]

def scenario_creator():
    # 1. انتخاب بیماری تصادفی
    target_disease = 'Asthma'
  
    # 2. تعریف پرامپت
    # نکته: وقتی کلاس Pydantic را به مدل می‌دهیم، خود LangChain توضیحات فیلدها (Description)
    # را به مدل زبانی منتقل می‌کند، بنابراین پرامپت می‌تواند ساده‌تر باشد.
    # اما دستورالعمل‌های "فارسی روان" و "عدم ترجمه اصطلاحات" را حفظ می‌کنیم.
    
    prompt_template = PromptTemplate(
        template="""
        شما یک متخصص پزشکی هستید. یک کیس پزشکی کامل برای بیماری {disease} تولید کنید.
        
        دستورالعمل‌های مهم:
        1. تمام فیلدها را دقیقاً مطابق ساختار خواسته شده پر کنید.
        2. پاسخ‌ها باید به زبان "فارسی روان" باشند.
        3. اصطلاحات تخصصی پزشکی (مانند نام داروها، نام صداهای ریوی مثل Crackles، نام تست‌ها) را ترجمه نکنید و به همان صورت انگلیسی بنویسید.
        4. داده‌ها (سن، علائم، نتایج آزمایش) باید با بیماری {disease} سازگاری علمی داشته باشند تا پزشک بتواند تشخیص دهد.
        """,
        input_variables=["disease"]
    )
  
    final_prompt = prompt_template.format(disease=f"{target_disease}")

    # 3. اتصال مدل به ساختار Pydantic
    # به جای دیکشنری json_schema، کلاس اصلی MedicalCase را پاس می‌دهیم
    structured_chat_model = model.with_structured_output(MedicalCase)
  
    # 4. اجرای مدل
    try:
        output_pydantic_object = structured_chat_model.invoke(final_prompt)
        
        # 5. تبدیل آبجکت Pydantic به دیکشنری پایتون (معادل JSON)
        # از model_dump() استفاده می‌کنیم تا خروجی قابل سریالایز شدن باشد
        # by_alias=True باعث می‌شود فیلدهایی مثل "fev1/fvc" که نام‌گذاری خاص داشتند درست برگردند
        output_dict = output_pydantic_object.model_dump(by_alias=True)
        
        return output_dict, target_disease

    except Exception as e:
        print(f"Error generating scenario: {e}")
        # در صورت بروز خطا می‌توانید یک مقدار پیش‌فرض یا None برگردانید
        return None, target_disease
