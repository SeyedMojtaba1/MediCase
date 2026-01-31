from django.db import migrations

def split_diseases_to_types(apps, schema_editor):
    PulmonologyDisease = apps.get_model('pulmonology_scenario', 'PulmonologyDisease')

    # دیکشنری مپینگ بر اساس لیستی که ارسال کردید
    # کلیدها باید دقیقاً مشابه english_name در دیتابیس (فایل 0001) باشند
    DISEASE_TYPES_MAP = {
        'Asthma': [
            'mild_allergic',
            'severe_uncontrolled',
            'exercise_induced'
        ],
        'COPD': [
            'chronic_bronchitis',
            'emphysema',
            'copd_cor_pulmonale'
        ],
        'IPF': [
            'stable_ipf',
            'acute_ipf_exacerbation',
            'rheumatoid_ild'
        ],
        # در فایل اولیه PH بود، اما شما phd نوشتید. اینجا مپ میکنیم
        'PH': [
            'idiopathic_pah',
            'ph_left_heart',
            'ph_lung_disease'
        ],
        'Pneumonia': [
            'typical_lobar',
            'complicated_effusion',
            'atypical_walking'
        ],
        'PTE': [
            'massive_pte',
            'peripheral_infarct',
            'submassive_pte'
        ]
    }

    for disease_name, types_list in DISEASE_TYPES_MAP.items():
        # پیدا کردن رکورد کلی که قبلاً ساخته شده (مثلاً Asthma)
        existing_record = PulmonologyDisease.objects.filter(english_name=disease_name).first()

        if existing_record and types_list:
            # استراتژی: رکورد موجود را به اولین تایپ تبدیل می‌کنیم
            # تا اگر جای دیگری به ID این بیماری ارجاع شده، دیتا از دست نرود.
            
            first_type = types_list[0]
            remaining_types = types_list[1:]

            # آپدیت رکورد موجود
            existing_record.type_disease = first_type
            existing_record.save()

            # ساخت رکوردهای جدید برای بقیه تایپ‌ها
            for type_val in remaining_types:
                PulmonologyDisease.objects.create(
                    english_name=disease_name,  # همان اسم اصلی (Asthma)
                    persian_name=existing_record.persian_name, # همان نام فارسی
                    type_disease=type_val
                )

class Migration(migrations.Migration):

    dependencies = [
        # حتماً چک کنید این نام با نام فایل مایگریشن قبلی شما (0007) یکی باشد
        ('pulmonology_scenario', '0007_pulmonologydisease_type_disease_and_more'),
    ]

    operations = [
        migrations.RunPython(split_diseases_to_types),
    ]