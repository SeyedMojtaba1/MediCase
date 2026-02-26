import json

class ClinicalEvaluator:
    def __init__(self, optimal, student_log, total_time_minutes=15):
        self.optimal = optimal
        self.student = student_log
        self.total_time_seconds = total_time_minutes * 60
        self.score = 0
        self.max_possible_score = 0
        self.actions_report = [] 
        self.timestamps = []
        self.final_diag_timestamp = None
        
        self.weights = {
            "default": 1,
            "history_taking": 7,
            "physical_exam": 7,
            "paraclinic": 20,
            "diagnosis": 300,
            "differential_diagnosis": 20,
            "pleural_assessment": 50,
            "noise_penalty": 10
        }

    def _parse_time_to_seconds(self, time_str):
        if not time_str or str(time_str).lower() in ["false", "true", "none"]:
            return None
        try:
            parts = list(map(int, time_str.split(':')))
            if len(parts) == 2:
                return parts[0] * 60 + parts[1]
            elif len(parts) == 3:
                return parts[0] * 3600 + parts[1] * 60 + parts[2]
            return None
        except:
            return None

    def _flatten_dict(self, d, parent_key='', sep='.'):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def calculate_duration(self):
        if not self.timestamps:
            return 0, self.total_time_seconds
        
        start_time_seconds = max(self.timestamps)
        
        end_time_seconds = self.final_diag_timestamp
        
        if end_time_seconds is None:
            end_time_seconds = min(self.timestamps) if self.timestamps else 0
            
        duration = start_time_seconds - end_time_seconds
        return max(0, duration), start_time_seconds

    def evaluate_diagnosis_accuracy(self):
        optimal_diff = self.optimal.get("differential_diagnosis", {})
        correct_differentials = [d for d, val in optimal_diff.items() if val == "true"]
        
        correct_final = self.optimal.get("final_diagnosis", {}).get("disease", "")
        
        student_diff_dict = self.student.get("differential_diagnosis", {})
        student_diff = list(student_diff_dict.keys()) if isinstance(student_diff_dict, dict) else self.student.get("student_selected_differentials", [])
        
        student_final = self.student.get("final_diagnosis", {}).get("disease", self.student.get("student_final_diagnosis", ""))

        is_final_correct = (student_final.lower() == correct_final.lower())
        
        missed_diffs = [d for d in correct_differentials if d not in student_diff]
        extra_diffs = [d for d in student_diff if d not in correct_differentials]

        return {
            "is_final_correct": is_final_correct,
            "correct_final_answer": correct_final,
            "student_final_answer": student_final,
            "correct_differentials": correct_differentials,
            "missed_differentials": missed_diffs,
            "extra_differentials": extra_diffs
        }
        
    def evaluate_performance(self):
        flat_optimal = self._flatten_dict(self.optimal)
        flat_student = self._flatten_dict(self.student)
        
        all_actions = set(flat_optimal.keys()).union(set(flat_student.keys()))
        
        for action in all_actions:
            opt_val = flat_optimal.get(action)
            is_required = str(opt_val).lower() == "true"
            
            weight = self.weights['default']
            if 'differential_diagnosis' in action: weight = self.weights['differential_diagnosis']
            elif 'diagnosis' in action: weight = self.weights['diagnosis']
            elif 'physical_exam' in action: weight = self.weights['physical_exam']
            elif 'paraclinic' in action: weight = self.weights['paraclinic']
            elif 'history_taking' in action: weight = self.weights['history_taking']

            if is_required:
                self.max_possible_score += weight

            stud_val = flat_student.get(action)
            is_performed = False
            
            if stud_val and str(stud_val).lower() not in ["false", "none", ""]:
                is_performed = True
                ts = self._parse_time_to_seconds(stud_val)
                if ts is not None:
                    self.timestamps.append(ts)
                    if "final_diagnosis" in action:
                        self.final_diag_timestamp = ts

            if is_required and is_performed:
                self.score += weight
                self.actions_report.append({"action": action, "status": "correct"})
            
            elif is_required and not is_performed:
                self.actions_report.append({"action": action, "status": "missed"})
            
            elif not is_required and is_performed:
                if 'paraclinic' in action or 'differential_diagnosis' in action:
                    self.score -= self.weights.get('noise_penalty', 0)
                self.actions_report.append({"action": action, "status": "noise"})
            

        final_percentage = (self.score / self.max_possible_score * 100) if self.max_possible_score > 0 else 0
        return min(100, max(0, final_percentage))

    def evaluate_pleural_effusion(self):
        optimal_pleural = self.optimal.get("pleural_effusion_assessment", {})
        # اینجا نام کلید اصلاح شد:
        student_pleural = self.student.get("pleural_effusion_assessment", {})

        is_correct = (
            student_pleural.get("has_effusion") == optimal_pleural.get("has_effusion") and
            student_pleural.get("need_aspiration") == optimal_pleural.get("need_aspiration") and
            student_pleural.get("effusion_type") == optimal_pleural.get("effusion_type")
        )
        
        return {
            "is_correct": is_correct,
            "optimal": optimal_pleural,
            "student": student_pleural
        }
    
    def get_category(self, percentage):
        if percentage >= 95: return {"label": "ممتاز / استادانه", "color": "#6A1B9A", "eng": "Mastery"}
        if percentage >= 85: return {"label": "بسیار خوب", "color": "#2E7D32", "eng": "Proficient"}
        if percentage >= 75: return {"label": "خوب", "color": "#43A047", "eng": "Competent"}
        if percentage >= 60: return {"label": "قابل قبول (مرزی)", "color": "#F9A825", "eng": "Borderline"}
        if percentage >= 40: return {"label": "نیازمند بازنگری", "color": "#EF6C00", "eng": "Needs Improvement"}
        return {"label": "غیر ایمن / بحرانی", "color": "#C62828", "eng": "Critical"}

    def format_time(self, seconds):
        m = int(seconds // 60)
        s = int(seconds % 60)
        return f"{m:02}:{s:02}"
    
    def analyze_time_performance(self, duration_seconds, total_seconds):
        if total_seconds == 0: return {}
        usage_ratio = duration_seconds / total_seconds
        if usage_ratio > 1.0: return {"level": "اتمام وقت", "color": "#D32F2F", "message": "زمان تمام شد."}
        elif usage_ratio >= 0.60: return {"level": "مطلوب", "color": "#43A047", "message": "زمان‌بندی عالی."}
        else: return {"level": "سریع", "color": "#1E88E5", "message": "بسیار سریع."}


# فرض کنید متغیرهای OPTIMAL_SCENARIO_COPD و STUDENT_LOG وجود دارند
# evaluator = ClinicalEvaluator(OPTIMAL_SCENARIO, STUDENT_LOG)

# # اجرای ارزیابی (فقط یک متد کافی است)
# final_score_percent = evaluator.evaluate_performance()

# # محاسبات زمان
# duration_seconds, total_seconds = evaluator.calculate_duration()
# time_analysis = evaluator.analyze_time_performance(duration_seconds, total_seconds)
# category = evaluator.get_category(final_score_percent)

# output = {
#     "overall_result": {
#         "title": category['label'],
#         "english_title": category['eng'],
#         "color_code": category['color'],
#         "is_passed": final_score_percent >= 60
#     },
#     "score": {
#         "obtained": round(final_score_percent),
#         "total": 100
#     },
#     "time_management": {
#         "duration_formatted": f"{evaluator.format_time(duration_seconds)}",
#         "total_allowed_formatted": "15:00",
#         "analysis": time_analysis
#     }
# }
