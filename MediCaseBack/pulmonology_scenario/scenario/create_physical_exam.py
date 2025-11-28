import random
from typing import Dict, Any, Tuple

def get_random_bp(sys_range: Tuple[int, int], dia_range: Tuple[int, int]) -> str:
    """تولید فشار خون تصادفی (سیستول/دیاستول)."""
    systolic = random.randint(sys_range[0], sys_range[1])
    diastolic = random.randint(dia_range[0], dia_range[1])
    return f"{systolic}/{diastolic} mmHg"

def get_random_temp(temp_range: Tuple[float, float]) -> str:
    """تولید دمای تصادفی."""
    # تولید عدد با دقت یک رقم اعشار
    temp = round(random.uniform(temp_range[0], temp_range[1]), 1)
    return f"{temp} °C"

def get_random_pr(pr_range: Tuple[int, int]) -> str:
    """تولید ضربان قلب تصادفی (PR)."""
    pr = random.randint(pr_range[0], pr_range[1])
    return f"{pr} bpm and regular rhythm"

def get_random_rr(rr_range: Tuple[int, int]) -> str:
    """تولید تعداد تنفس تصادفی (RR)."""
    rr = random.randint(rr_range[0], rr_range[1])
    return f"{rr} breaths/min"

def get_random_spo2(spo2_range: Tuple[int, int]) -> str:
    """تولید اشباع اکسیژن تصادفی (SpO2)."""
    spo2 = random.randint(spo2_range[0], spo2_range[1])
    return f"{spo2}% (RA)"

def get_random_gcs(gcs_range: Tuple[int, int]) -> str:
    """تولید نمره GCS تصادفی."""
    gcs = random.randint(gcs_range[0], gcs_range[1])
    return f"{gcs}"


# --- توابع اصلی تولید علائم حیاتی ---

def generate_BP() -> Dict[str, Any]:
    """
    تولید فشار خون (BP) بر اساس توزیع درصدی.
    """
    options = [
        ("Normal to Mildly Elevated", (100, 140), (60, 90), 0.80), # (سیستول، دیاستول), 80%
        ("Hypotension/Shock", (70, 89), (40, 59), 0.20)          # (سیستول، دیاستول), 20%
    ]
    
    # انتخاب تصادفی بر اساس وزن (درصد)
    choice = random.choices(options, weights=[opt[3] for opt in options], k=1)[0]
    
    status = choice[0]
    sys_range = choice[1]
    dia_range = choice[2]
    
    return {
        "status": status,
        "value": get_random_bp(sys_range, dia_range)
    }

def generate_T() -> Dict[str, Any]:
    """
    تولید دما (T) بر اساس توزیع درصدی.
    """
    options = [
        ("Afebrile to Low-Grade Fever", (37.0, 38.0), 0.40), # 40%
        ("Moderate to High-Grade Fever", (38.1, 40.0), 0.60) # 60%
    ]

    choice = random.choices(options, weights=[opt[2] for opt in options], k=1)[0]
    
    status = choice[0]
    temp_range = choice[1]
    
    return {
        "status": status,
        "value": get_random_temp(temp_range)
    }

def generate_PR() -> Dict[str, Any]:
    """
    تولید ضربان قلب (PR) بر اساس توزیع درصدی.
    """
    options = [
        ("Normal to Mild Tachycardia", (60, 100), 0.70), # 70%
        ("Moderate to Severe Tachycardia", (101, 140), 0.30) # 30%
    ]

    choice = random.choices(options, weights=[opt[2] for opt in options], k=1)[0]
    
    status = choice[0]
    pr_range = choice[1]
    
    return {
        "status": status,
        "value": get_random_pr(pr_range)
    }

def generate_RR() -> Dict[str, Any]:
    """
    تولید تعداد تنفس (RR) بر اساس توزیع درصدی.
    """
    options = [
        ("Normal", (12, 20), 0.40), # 40%
        ("Mild Tachypnea", (21, 24), 0.35), # 35%
        ("Moderate to Severe Tachypnea", (25, 35), 0.25) # 25%
    ]

    choice = random.choices(options, weights=[opt[2] for opt in options], k=1)[0]
    
    status = choice[0]
    rr_range = choice[1]
    
    return {
        "status": status,
        "value": get_random_rr(rr_range)
    }

def generate_SpO2() -> Dict[str, Any]:
    """
    تولید اشباع اکسیژن (SpO2) بر اساس توزیع درصدی.
    """
    options = [
        ("Normal Saturation (on Room Air)", (95, 100), 0.60), # 60%
        ("Mild to Moderate Hypoxemia", (90, 94), 0.30),       # 30%
        ("Severe Hypoxemia", (75, 89), 0.10)                  # 10%
    ]

    choice = random.choices(options, weights=[opt[2] for opt in options], k=1)[0]
    
    status = choice[0]
    spo2_range = choice[1]
    
    return {
        "status": status,
        "value": get_random_spo2(spo2_range)
    }

def generate_GCS() -> Dict[str, Any]:
    """
    تولید نمره GCS بر اساس توزیع درصدی.
    """
    options = [
        ("Fully Conscious (A&Ox3)", (15, 15), 0.80), # 80%
        ("Mild Impairment", (13, 14), 0.20)          # 20%
    ]

    choice = random.choices(options, weights=[opt[2] for opt in options], k=1)[0]
    
    status = choice[0]
    gcs_range = choice[1]
    
    return {
        "status": status,
        "value": get_random_gcs(gcs_range)
    }