from langchain_core.documents import Document

PNEUMONIA_PROFILE_REF = """
disease: Pneumonia
chief_complaint: Acute onset of fever, cough (productive or dry), dyspnea, and 20% of times pleuritic chest pain
"""

PNEUMONIA_HISTORY_REF = """
disease: Pneumonia
present_illness:
    question1: Symptoms typically start acutely over 1 to 7 days
    question2: Onset is usually relatively sudden, 50% of times following a viral URI. 50% of times there is no URI
    question3: Shortness of breath is 55% of times present, 15% of times is present at rest or exertion.there is no shortness of breath at 45% of times
    question4: Cough is 95% of times present. Sputum is 40% of times purulent (yellow/green), rusty (pneumococcal), or currant jelly (Klebsiella)
    question5: Wheezing sound is 5% of times present (if underlying comorbidity like asthma). 95% of times is not present
    question6: Pleuritic chest pain is 20% of times prsent
    question7: Fever, chills (rigors), and night sweats are classic systemic symptoms.(Fever and Chills are 80% of times present. night sweats are 30% of times present)
    question8: Leg swelling is not typical unless there is comorbid heart failure in 40% of over 55y old patients. 60% of times is not present
    question9: Recurrent episodes are 30% of times present (suggesting aspiration or immunodeficiency)
    question10: Fatigue and anorexia are 80% of times present. 20% of time none of them are present
    
past_medical_history:
    question1:
        question1a: Risk factors include COPD, asthma, diabetes, heart failure and one is randomly present in 45% of times
        question1b: Duration of comorbidities is between 2-5 years
    question2: 
        question2a: History of splenectomy is 5% of times present. 85% of times there is no former surgery. 10% of times one of these surgeries is present:Appendectomy, Cholecystectomy, Hernia Repair, Cataract Surgery, CABG, Knee/Hip Replacement, Mastectomy, Hysterectomy, Tonsillectomy, Laminectomy
        question2b: Hospitalization history is present if surgery is present, or 10% of times for other reasons (like infection)
    question3: History of lung/heart disease is present in 40% of over 55y old patients
    question4: Active cancer or chemotherapy is 2% of times present. 98% of times is not present
    question5: Childhood history is 2% of times present. 98% of times is not present
    question6: Vaccination status (Influenza, Pneumococcal) is negative 70% of times. 30% of times vaccination has been done

drug_history:
    question1:
        question1a: Immunosuppressants (steroids, biologic agents) are present in 5-10% of cases (high risk). Regular medications for comorbidities are present in 45% of cases
        question1b: Recent antibiotic use is present in 15% of cases (increases risk of resistant organisms)
        question1c: Change in regular medication (e.g., stopping a dose) is present in 5% of cases
    question2: Use of OTC medications (e.g., Tylenol, cough suppressants) for flu-like symptoms is present in 50% of cases
    
allergies:
    question1:
        question1a: Drug allergy (e.g., Penicillin) is reported in 10% of cases
        question1b: The reported reaction severity determines alternative empiric antibiotic choices

family_history:
    question1: 
        question1a: Irrelevant for acute infection in 99% of cases. Unless immunodeficiency runs in family (rare, <1%)
        question1b: Details of family history are generally non-contributory for acute CAP
    question2: Family history of heart/lung disease is present in 40% of cases (as general context)
    question3: 
        question3a: Family history of cancer is 20% of times present
        question3b: Details are usually non-contributory for acute infection

social_history:
    question1:
        question1a: Smoking history (current or former) is present in 60% of adult patients (a significant risk factor)
        question1b: If former, duration since quitting is relevant for risk assessment
    question2: Heavy alcohol use (risk factor for aspiration) is present in 25% of cases
    question3: 
        question3a: IV drug use (risk factor for Staph aureus pneumonia) is present in 2% of cases
        question3b: Last use date is critical if positive
    question4: Living in crowded settings (e.g., nursing home, dormitory) is present in 15% of cases (risk for Mycoplasma, TB)
    
ROS:
    question1: Fever, chills, fatigue are positive in 80% of cases
    question2: Rash (e.g., erythema multiforme) is seen in <5% of cases (Atypical Pneumonia)
    question3: Headache is present in 20-30% of cases (Atypical Pneumonia)
    question4: Eye symptoms (e.g., conjunctivitis) are seen in <5% of cases (Atypical)
    question5: Sore throat or otitis media is seen in 10-20% of cases (Atypical/Viral)
    question6: Pleuritic Chest Pain (20%), Palpitations (10%). Edema is not typical (90% negative)
    question7: Cough, dyspnea, sputum are positive in 95% of cases. Hemoptysis is rare (2-5%)
    question8: GI symptoms (Nausea, Vomiting, Diarrhea) are present in 20% of cases (especially Legionella/Viral)
    question9: Urinary symptoms are not typical (95% negative)
    question10: Myalgias/arthralgias are present in 30% of cases (Viral/Atypical)
    question11: Confusion/LOC change is a red flag (CURB-65), present in 30% of cases (elderly/severe)
    question12: Mood changes are not typical (95% negative)
    question13: Endocrine symptoms are not typical (95% negative)
    question14: Hematologic symptoms are not typical (95% negative)
"""

COPD_PROFILE_REF = """
disease: COPD (Stable/Chronic Phase)
chief_complaint: Chronic progressive dyspnea (worsening over years) in 90% of cases, exercise intolerance in 80% of cases, or chronic productive cough in 70% of cases for routine checkup
"""

COPD_HISTORY_REF = """
disease: COPD
present_illness:
    question1: In 100% of cases, symptoms have been present for years and are slowly progressive. Patients adapt their lifestyle to accommodate limitations in 85% of cases
    question2: In 100% of cases, onset is insidious and gradual. Sudden onset is 0% in the stable phase
    question3: Shortness of breath is present in 90% of cases. In 80% of cases, it is 'Dyspnea on Exertion' (DOE). In 20% of severe cases, it is present at rest or with minimal activity
    question4: Chronic cough is present in 70% of cases (Chronic Bronchitis phenotype). In 30% of cases (predominantly Emphysema), cough is minimal or absent. Sputum is clear/mucoid in 90% of stable cases
    question5: Wheezing is reported in 50% of cases, often varying day to day or with weather changes. In 50% of cases, no wheezing is reported
    question6: Chest pain is absent in 90% of cases. In 10% of cases, vague chest tightness or musculoskeletal pain from coughing is reported
    question7: Fever, chills, and night sweats are ABSENT in 95% of stable COPD cases. Their presence is 5% (suggesting a new complication)
    question8: Leg swelling (bilateral pitting edema) is present in 25% of cases (suggesting Cor Pulmonale/Right Heart Failure). In 75% of cases, it is absent
    question9: History of progressive decline is present in 100% of cases. History of previous 'bad days' or hospitalizations is present in 60% of cases
    question10: Weight loss/Cachexia is present in 30% of cases (Emphysema phenotype). Fatigue is present in 70% of cases. In 30% of cases (Chronic Bronchitis "Blue Bloater"), patients may be overweight
    
past_medical_history:
    question1:
        question1a: Comorbidities are common: Hypertension is present in 50% of cases, Ischemic Heart Disease in 30%, Diabetes in 20%, and Anxiety/Depression in 40%
        question1b: Duration of comorbidities is present for >5 years in 75% of cases
    question2: 
        question2a: History of previous hospitalizations for respiratory issues is present in 50% of moderate-to-severe cases. 80% of times no unrelated major surgery
        question2b: History of intubation is present in <10% of stable outpatients
    question3: History of heart disease is present in 40% of cases (shared smoking risk)
    question4: History of Lung Cancer (cured/remission) is present in 5% of cases. 95% of times not present
    question5: Childhood respiratory infections are reported in 30% of cases
    question6: Vaccination (Influenza/Pneumococcal) is done in 60% of cases. In 40% of cases, it is missed

drug_history:
    question1:
        question1a: In 80% of cases, patients use maintenance inhalers (LAMA, LABA/LAMA, or ICS/LABA). In 20% of mild cases, only SABA (Salbutamol) is used prn
        question1b: Inhaler technique errors are present in 40% of cases
        question1c: In stable phase, doses are unchanged in 90% of times
    question2: Use of mucolytics or antioxidants is present in 20% of cases

allergies:
    question1:
        question1a: True drug allergy is present in 10% of cases. In 30% of cases, patients may report 'hay fever' (Asthma-COPD overlap)
        question1b: Severity of reaction varies in 100% of reported cases

family_history:
    question1: 
        question1a: Alpha-1 Antitrypsin deficiency in family is present in <1% of cases. Family history of COPD is present in 20% of cases
        question1b: Details often relate to heavy smoking in parents in 80% of cases
    question2: Family history of cardiovascular disease is present in 50% of cases
    question3: 
        question3a: Family history of lung cancer is present in 15% of cases
        question3b: Details of cancer are generally non-contributory for the acute presentation in 99% of cases

social_history:
    question1:
        question1a: Smoking is the cause in 80% of cases. 40% are Current Smokers, 40% are Former Smokers. 20% are Never Smokers (Biomass/Occupational/Genetic causes)
        question1b: Pack-year history is greater than 20 pack-years in 90% of cases
    question2: Alcohol use (social) is present in 30% of cases. Heavy use is present in 10% of cases
    question3: 
        question3a: Recreational drug use is present in <5% of cases
        question3b: Last use date is critical if positive in 100% of cases
    question4: Exposure to biomass fuel or occupational dusts is present in 15% of cases (especially if non-smoker)
    
ROS:
    question1: Fatigue is positive in 60% of cases. Weight change is positive in 40% (Loss in Emphysema, Gain in Bronchitis)
    question2: Skin is normal in 70% of cases. Thin skin/bruising (steroid effect) is present in 20%. Central cyanosis is present in 10% (severe disease)
    question3: Morning headaches are present in 10% of cases (severe CO2 retention)
    question4: Eye symptoms are negative in 95% of cases
    question5: Chronic nasal congestion is present in 30% of cases
    question6: Palpitations are present in 20% of cases (often due to inhaler side effects). Chest pain is negative in 90% of cases
    question7: Dyspnea and Cough are the main positives (see HPI) in 95% of cases. Hemoptysis is present in <5% of stable COPD cases
    question8: GERD symptoms are present in 40% of cases
    question9: Urinary symptoms are present in 30% of cases (e.g., BPH in older males)
    question10: Muscle weakness/wasting is present in 30% of cases
    question11: Neurological symptoms are negative in 95% of cases unless severe hypoxia/hypercapnia exists
    question12: Anxiety/Depression symptoms are positive in 40% of cases
    question13: Joint pains (Osteoarthritis) are present in 50% of elderly COPD patients
    question14: Hematologic symptoms are negative in 85% of cases. Secondary polycythemia is present in 15% of cases (suggesting chronic hypoxemia)
"""

documents = [
    Document(page_content=PNEUMONIA_PROFILE_REF, metadata={"disease": "Pneumonia", "section": "patient_profile"}),
    Document(page_content=PNEUMONIA_HISTORY_REF, metadata={"disease": "Pneumonia", "section": "history_taking"}),
    Document(page_content=COPD_PROFILE_REF, metadata={"disease": "COPD", "section": "patient_profile"}),
    Document(page_content=COPD_HISTORY_REF, metadata={"disease": "COPD", "section": "history_taking"}),
]