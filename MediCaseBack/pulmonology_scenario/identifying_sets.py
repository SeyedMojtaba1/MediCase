import json
from typing import Dict, Any, Tuple, Union

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
        count_C = 0
        count_E = 0
        count_M = 0
        count_O = 0
        count_A = 0
        
        count_O = count_true_values(optimal_actions, "True")
        count_UnO = count_true_values(optimal_actions, "False")
        count_A = (count_O + count_UnO) - count_true_values(student_log[stage_name], "False")
        count_C = recursive_count_C(optimal_actions, student_log[stage_name])
        count_M = count_O - count_C
        count_E = count_A - count_C
        results[stage_name] = {
            "C": count_C,
            "E": count_E,
            "M": count_M,
            "O": count_O,
            "A": count_A,
            "Success_Rate_C_div_O": f"{count_C / count_O * 100:.2f}%" if count_O > 0 else "N/A"
        }
        
    return results
