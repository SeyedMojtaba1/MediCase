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
            "history_taking": 1,
            "physical_exam": 2,
            "paraclinic": 3,
            "diagnosis": 15,
            "noise_penalty": 0 # می‌توانید اینجا جریمه نمره منفی برای نویز تعیین کنید
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
        
        # پیدا کردن آخرین زمانی که دانشجو فعالیت کرده (شروع سناریو)
        start_time_seconds = max(self.timestamps)
        
        # پیدا کردن زمان تشخیص نهایی (پایان سناریو)
        end_time_seconds = self.final_diag_timestamp
        
        # اگر تشخیص نهایی نداده، کمترین زمان ثبت شده را به عنوان پایان در نظر می‌گیریم
        if end_time_seconds is None:
            end_time_seconds = min(self.timestamps) if self.timestamps else 0
            
        duration = start_time_seconds - end_time_seconds
        # هندل کردن حالتی که زمان‌ها معکوس باشند (بسته به منطق سیستم شما که زمان باقی‌مانده است یا زمان گذشته)
        return max(0, duration), start_time_seconds

    # --- متد اصلی: ارزیابی جامع (Comprehensive Evaluation) ---
    def evaluate_performance(self):
        """
        این متد تمام کلیدها را بررسی می‌کند و در یکی از سه دسته قرار می‌دهد:
        1. Correct: لازم بود و انجام شد.
        2. Missed: لازم بود و انجام نشد.
        3. Noise: لازم نبود (False یا نبود در لیست) ولی انجام شد.
        """
        flat_optimal = self._flatten_dict(self.optimal)
        flat_student = self._flatten_dict(self.student)
        
        # گام ۱: ایجاد لیستی از تمام اقدامات ممکن (اجتماع کلیدهای بهینه و دانشجو)
        all_actions = set(flat_optimal.keys()).union(set(flat_student.keys()))
        
        for action in all_actions:
            # تعیین وضعیت در سناریوی بهینه (آیا لازم است؟)
            opt_val = flat_optimal.get(action)
            is_required = str(opt_val).lower() == "true"
            
            # تعیین وزن بر اساس نوع اقدام
            weight = self.weights['default']
            if 'diagnosis' in action: weight = self.weights['diagnosis']
            elif 'physical_exam' in action: weight = self.weights['physical_exam']
            elif 'paraclinic' in action: weight = self.weights['paraclinic']

            # اگر اکشن واجب باشد، به نمره کل ممکن اضافه می‌شود
            if is_required:
                self.max_possible_score += weight

            # تعیین وضعیت در لاگ دانشجو (آیا انجام شده؟)
            stud_val = flat_student.get(action)
            is_performed = False
            
            # بررسی اینکه مقدار معتبر است و "False" نیست
            if stud_val and str(stud_val).lower() not in ["false", "none", ""]:
                is_performed = True
                # ثبت زمان
                ts = self._parse_time_to_seconds(stud_val)
                if ts is not None:
                    self.timestamps.append(ts)
                    if "final_diagnosis" in action:
                        self.final_diag_timestamp = ts

            # --- منطق دسته‌بندی ---
            
            # حالت ۱: درست (Correct)
            if is_required and is_performed:
                self.score += weight
                self.actions_report.append({"action": action, "status": "correct"})
            
            # حالت ۲: جاافتاده (Missed)
            elif is_required and not is_performed:
                self.actions_report.append({"action": action, "status": "missed"})
            
            # حالت ۳: نویز / غیرضروری (Noise)
            elif not is_required and is_performed:
                # اینجا می‌توانید امتیاز کسر کنید
                self.score -= self.weights.get('noise_penalty', 0)
                self.actions_report.append({"action": action, "status": "noise"})
            
            # حالت ۴: (Irrelevant) نه لازم بود و نه انجام شد -> کاری نداریم (نادیده گرفته می‌شود)

        # محاسبه درصد نهایی
        final_percentage = (self.score / self.max_possible_score * 100) if self.max_possible_score > 0 else 0
        return min(100, max(0, final_percentage))

    # ... (متدهای get_category, format_time, analyze_time_performance ثابت می‌مانند) ...
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
        # ... (همان منطق قبلی) ...
        if usage_ratio > 1.0: return {"level": "اتمام وقت", "color": "#D32F2F", "message": "زمان تمام شد."}
        elif usage_ratio >= 0.60: return {"level": "مطلوب", "color": "#43A047", "message": "زمان‌بندی عالی."}
        else: return {"level": "سریع", "color": "#1E88E5", "message": "بسیار سریع."}

# ==========================================
# اجرای کد
# ==========================================

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
