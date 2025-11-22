from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from .feedback_utils.S1_identifying_sets import calculate_set_metrics
from .feedback_utils.S3_stage_score import calculate_stage_order_error
from .feedback_utils.optimal_pulmonology_scenarios import OPTIMAL_SCENARIO
from .feedback_utils.escape_json_braces import escape_json_braces
import json

json_schema = {
    "title": "Clinical_Case_Feedback_Schema",
    "type": "object",
    "properties": {
    "total": {
        "type": "object",
        "properties": {
        "strengths": {
            "type": "string",
            "description": "از اطلاعات ارائه شده در evaluation (در بخش C و C_items) و transition استفاده کن در صورت نیاز به آنها اشاره کن و یک توضیح از نقاط قوت عملکرد دانشجو با ذکر اقدامات کلیدی که منجر به تشخیص دقیق و بهینه شده‌اند."
        },
        "weaknesses": {
            "type": "object",
            "properties": {
              "M": {
                "title": "M",
                "type": "string",
                "description": "از اطلاعات ارائه شده در evaluation (در بخش M و M_items) و transition استفاده کن در صورت نیاز به آنها اشاره کن و یک توضیح از مهم‌ترین نقاط ضعف شامل (بخش های اشتباها انجام شده) که منجر به تأخیر در تشخیص یا اتلاف منابع شده‌اند."
              },
              "E": {
                "title": "E",
                "type": "string",
                "description": "از اطلاعات ارائه شده در evaluation (در بخش E و E_items) و transition استفاده کن در صورت نیاز به آنها اشاره کن و یک توضیح از مهم‌ترین نقاط ضعف شامل (بخش‌های حیاتی انجام نشده) که منجر به تأخیر در تشخیص یا اتلاف منابع شده‌اند."
              }
            }
        },
        "educational_feedback": {
            "type": "string",
            "description": "از اطلاعات ارائه شده در evaluation و transition استفاده کن در صورت نیاز به آنها اشاره کن و یک توضیح از توصیه‌های کلی برای بهبود مهارت‌های تریاژ و استدلال بالینی بر اساس تحلیل عملکرد"
        }
        },
        "required": [
        "strengths",
        "weaknesses",
        "educational_feedback"
        ]
    },
    "history_taking": {
        "type": "object",
        "properties": {
        "strengths": {
            "type": "string",
            "description": "از اطلاعات ارائه شده در evaluation (در قسمت history_taking بخش C و C_items) و transition استفاده کن در صورت نیاز به آنها اشاره کن و لیستی از اقدامات صحیح دانشجو (C) در مرحله شرح حال."
        },
        "weaknesses": {
            "type": "object",
            "properties": {
              "M": {
                "title": "M",
                "type": "string",
                "description": "از اطلاعات ارائه شده در evaluation (در قسمت history_taking بخش M و M_items) و transition استفاده کن در صورت نیاز به آنها اشاره کن و لیستی از (بخش های اشتباها انجام شده) دانشجو در مرحله شرح حال."
              },
              "E": {
                "title": "E",
                "type": "string",
                "description": "از اطلاعات ارائه شده در evaluation (در قسمت history_taking بخش E و E_items) و transition استفاده کن در صورت نیاز به آنها اشاره کن و لیستی از (بخش‌های حیاتی انجام نشده) دانشجو در مرحله شرح حال."
              }
            }
        },
        "educational_feedback": {
            "type": "object",
            "properties": {
              "why_M_was_important": {
                "title": "why_M_was_important",
                "type": "string",
                "description": " توضیح دلایل اهمیت حیاتی هر یک از (بخش‌های حیاتی انجام نشده) در تشخیص بیماری {disease}از اطلاعات ارائه شده در evaluation (در قسمت history_taking بخش M و M_items) و transition استفاده کن در صورت نیاز به آنها اشاره کن و به صورت علمی و با نگاه بالینی."
              },
              "why_E_was_unnecessary": {
                "title": "why_E_was_unnecessary",
                "type": "string",
                "description": "توضیح دلایل غیرمهم بودن یا اضافی بودن هر یک از (بخش های اشتباها انجام شده) و اینکه چگونه منجر به اتلاف زمان شده‌اند و ما را از تشخیص بیماری {disease}از اطلاعات ارائه شده در evaluation (در قسمت history_taking بخش E و E_items) و transition استفاده کن در صورت نیاز به آنها اشاره کن و دور می کنند. به صورت علمی و با نگاه بالینی."
              },
              "sequence_advice": {
                "title": "sequence_advice",
                "type": "string",
                "description": "از اطلاعات ارائه شده در evaluation در قسمت history_taking و transition استفاده کن در صورت نیاز به آنها اشاره کن و در صورت وجود خطای توالی، دلیل اشتباه بودن آن و توصیه‌هایی برای رعایت توالی منطقی."
              }
            }
        }
        },
        "required": [
        "strengths",
        "weaknesses",
        "educational_feedback"
        ]
    },
    "physical_exam": {
        "type": "object",
        "properties": {
        "strengths": {
            "type": "string",
            "description": "لیستی ازاقدامات صحیح دانشجو (C) در مرحله معاینه فیزیکی."
        },
        "weaknesses": {
            "type": "object",
            "properties": {
              "M": {
                "title": "M",
                "type": "string",
                "description": "لیستی از (بخش های اشتباها انجام شده) دانشجو در مرحله معاینه فیزیکی."
              },
              "E": {
                "title": "E",
                "type": "string",
                "description": "لیستی از (بخش‌های حیاتی انجام نشده) دانشجو در مرحله معاینه فیزیکی."
              }
            }
        },
        "educational_feedback": {
            "type": "object",
            "properties": {
              "why_M_was_important": {
                "title": "why_M_was_important",
                "type": "string",
                "description": " توضیح دلایل اهمیت حیاتی هر یک از (بخش‌های حیاتی انجام نشده) در تشخیص بیماری {disease} به صورت علمی و با نگاه بالینی."
              },
              "why_E_was_unnecessary": {
                "title": "why_E_was_unnecessary",
                "type": "string",
                "description": "توضیح دلایل غیرمهم بودن یا اضافی بودن هر یک از (بخش های اشتباها انجام شده) و اینکه چگونه منجر به اتلاف زمان شده‌اند و ما را از تشخیص بیماری {disease} دور می کنند. به صورت علمی و با نگاه بالینی. و تأکید بر معاینه هدفمند."
              },
              "sequence_advice": {
                "title": "sequence_advice",
                "type": "string",
                "description": "در صورت وجود خطای توالی، دلیل اشتباه بودن آن و توصیه‌هایی برای جلوگیری از آن."
              }
            }
          }
        },
        "required": [
        "strengths",
        "weaknesses",
        "educational_feedback"
        ]
    },
    "paraclinic": {
        "type": "object",
        "properties": {
        "strengths": {
            "type": "string",
            "description": "لیستی ازاقدامات صحیح دانشجو (C)، با تأکید بر تست‌های طلایی یا تست‌های ردکننده که منجر به تأیید نهایی یا کاهش ریسک شده‌اند."
        },
        "weaknesses": {
            "type": "object",
            "properties": {
              "M": {
                "title": "M",
                "type": "string",
                "description": "لیستی از (بخش های اشتباها انجام شده) دانشجو در مرحله پاراکلینیک."
              },
              "E": {
                "title": "E",
                "type": "string",
                "description": "لیستی از (بخش‌های حیاتی انجام نشده) دانشجو در مرحله پاراکلینیک."
              }
            }
        },
        "educational_feedback": {
            "type": "object",
            "properties": {
              "why_M_was_important": {
                "title": "why_M_was_important",
                "type": "string",
                "description": " توضیح دلایل اهمیت حیاتی هر یک از (بخش‌های حیاتی انجام نشده) در تشخیص بیماری {disease} به صورت علمی و با نگاه بالینی."
              },
              "why_E_was_unnecessary": {
                "title": "why_E_was_unnecessary",
                "type": "string",
                "description": "توضیح دلایل غیرمهم بودن یا اضافی بودن هر یک از (بخش های اشتباها انجام شده) و اینکه چگونه منجر به اتلاف زمان شده‌اند و ما را از تشخیص بیماری {disease} دور می کنند. به صورت علمی و با نگاه بالینی. و تأکید بر اصل «کمترین تهاجم و بیشترین ارزش تشخیصی»."
              },
              "sequence_advice": {
                "title": "sequence_advice",
                "type": "string",
                "description": "در صورت وجود خطای توالی، دلیل اشتباه بودن آن و توصیه‌هایی برای رعایت توالی منطقی."
              }
            }
          }
        },
        "required": [
        "strengths",
        "weaknesses",
        "educational_feedback"
        ]
    },
    "diffrential_diagnosis": {
        "type": "object",
        "properties": {
        "strengths": {
            "type": "string",
            "description": "بیماری‌هایی که به درستی انتخاب (لیست اولیه) و/یا به درستی فیلتر (شواهد) شده‌اند."
        },
        "weaknesses": {
            "type": "object",
            "properties": {
              "M": {
                "title": "M",
                "type": "string",
                "description": "اشتباهات در لیست اولیه (حذفیات M) و یا ضعف در فیلتر شواهد (حذف بیماری محتمل)."
              },
              "E": {
                "title": "E",
                "type": "string",
                "description": "اشتباهات در لیست اولیه (انتخاب E) و یا ضعف در فیلتر شواهد (حفظ بیماری رد شده)."
              }
            }
        },
        "educational_feedback": {
            "type": "object",
            "properties": {
              "why_M_was_important": {
                "title": "why_M_was_important",
                "type": "string",
                "description": "توضیح دلایل غیرمرتبط بودن بیماری‌های اضافی (بخش های اشتباه انجام شده) و اینکه چگونه نتایج پاراکلینیک باید برای رد قاطع آن‌ها استفاده می‌شد."
              },
              "why_E_was_unnecessary": {
                "title": "why_E_was_unnecessary",
                "type": "string",
                "description": "توضیح دلایل غیرمرتبط بودن بیماری‌های اضافی (بخش های اشتباه انجام شده) و اینکه چگونه نتایج پاراکلینیک باید برای رد قاطع آن‌ها استفاده می‌شد."
              }
            }
        }
        },
        "required": [
        "strengths",
        "weaknesses",
        "educational_feedback"
        ]
    }
    },
    "required": [
    "total",
    "history_taking",
    "physical_exam",
    "paraclinic",
    "diffrential_diagnosis"
    ]
}


model = init_chat_model(
        model="gpt-4o-mini",
        base_url="https://api.avalai.ir/v1",
        api_key="aa-bFHSFoxDcvBLcr9tEpySz5SIjvlHGBAmJ3nqgKALEgt5w8YH",
)

target_disease = 'COPD'

prompt_template = PromptTemplate(
    template="""
    scenario: 
    {{
  "patient_profile": {{
    "personal_information": {{
      "first_name": "",
      "last_name": "",
      "age": "سن بیمار باید متناسب با شیوع بیماری انتخاب شود. در بیماری‌های مزمن تنفسی و قلبی معمولاً میانسالی تا سالمندی (حدود 45 تا 80 سال)، در بیماری‌های حاد یا ارثی ممکن است سن پایین‌تر باشد. برای تنوع، سن را در بازه منطقی بیماری انتخاب کن، نه مقدار ثابت.",
      "gender": "",
      "occupation": "",
      "place_of_birth": "",
      "place_of_residence": "",
      "marital_status": ""
    }},
    "chief_complaint": "contains patient's main reason of visit and its onset time",
    "vital_sign": {{
      "BP": "Blood Pressure",
      "T": "Temprature",
      "PR": "Pulse Rate",
      "RR": "Respiratory Rate",
      "SpO2": "Saturation of O2",
      "GCS": "Level of Consiousness"
    }}
  }},
  "history_taking": {{
    "present_illness": {{
      "question1": "علائم از چه زمانی شروع شدند و در طول زمان چه تغییری کردند؟",
      "question2": "شروع علائم ناگهانی بوده یا تدریجی؟ بعد از اتفاق خاصی مثل عفونت یا تماس خاصی شروع شد؟",
      "question3": "تنگی نفستون دائمیه یا دوره‌ای؟ و با فعالیت بدتر میشه یا در حالت استراحت هم وجود داره؟",
      "question4": "سرفه دارید؟ اگر بله، خشک است یا همراه با خلط؟ رنگ و حجم خلط چطور است؟",
      "question5": "تا حالا خس‌خس یا صدای غیرعادی در تنفس شنیدید؟",
      "question6": "احساس درد یا فشار در قفسه سینه دارید؟ با تنفس یا حرکت تغییر می‌کنه؟",
      "question7": "در روزهای اخیر تب، لرز یا تعریق شبانه داشتید؟ وجود یا عدم وجود تب باید با زمینهٔ بالینی هماهنگ باشد. در بیماری‌های مزمن پایدار معمولاً تب وجود ندارد، اما در تشدید حاد یا عفونت‌ها ممکن است تب و لرز مشاهده شود. پاسخ 'بله' یا 'خیر' را بر اساس ماهیت بیماری و مرحله آن تولید کن.",
      "question8": "تورم پا، تپش قلب یا احساس سبکی سر دارید؟",
      "question9": "قبلاً هم چنین حمله یا علائمی داشتید؟ چه درمانی کمکتون کرده؟",
      "question10": "احساس کاهش وزن، خستگی یا بی‌اشتهایی داشتید؟"
    }},
    "medical_history": {{
      "question1": {{
        "question1a": "آیا بیماری طولانی مدت (مزمن) مثل قند (دیابت)، فشار خون، آسم، مشکل تیروئید، یا بیماری جدی کلیوی/کبدی دارید؟",
        "question1b": "اگر پاسخ question1a بله بود، تشخیص این بیماری از چه موقع بوده است؟"
      }},
      "question2": {{
        "question2a": "آیا تا به حال عمل جراحی (بزرگ یا کوچک) داشته‌اید؟ و آیا تا به حال در بیمارستان بستری شده‌اید؟",
        "question2b": "اگر پاسخ question2a بله بود، دلیلش چه بوده و در چه سالی؟ همچنین، آیا تا به حال انتقال خون داشته‌اید؟"
      }},
      "question3": "آیا سابقه بیماری های قلبی، ریوی و مغزی را دارید؟",
      "question4": "آیا در حال حاظر یا در گذشته سرطان فعال داشته‌اید؟",
      "question5": "در دوران کودکی، آیا بیماری‌های خاصی (مثل تب روماتیسمی، سرخک شدید) گرفتید یا به دلیل بیماری بستری شدید؟",
      "question6": "برنامه واکسن‌ها (مثل کزاز و آنفولانزا) شما کامل و به روز است؟"
    }},
    "drug_history": {{
      "question1": {{
        "question1a": "لطفاً لیست تمام داروهایی که در حال حاضر به صورت مرتب (روزانه، هفتگی یا ماهانه) مصرف می‌کنید را به من بگویید.",
        "question1b": "دوز هر دارو چقدر است و چند بار در روز مصرف می‌کنید؟",
        "question1c": "آیا در چند روز گذشته، دوز یا زمان مصرف هیچ‌کدام از این داروها را تغییر داده‌اید؟"
      }},
      "question2": "به صورت منظم داروهای بدون نسخه (OTC) (مثل داروهای سرماخوردگی، مسکن‌ها، آنتی‌اسیدها)، مکمل‌های غذایی، داروهای گیاهی یا خواب آور مصرف می‌کنید؟"
    }},
    "allergies": {{
      "question1": {{
        "question1a": "آیا به دارو، غذا، یا ماده خاصی آلرژی (حساسیت) دارید؟",
        "question1b": "اگر پاسخ question1a بله بود، دقیقاً چه دارو یا ماده‌ای است؟ و واکنش شما (مثل کهیر یا تنگی نفس) چگونه بوده است؟"
      }}
    }},
    "family_history": {{
      "question1": {{
        "question1a": "آیا در خانواده درجه یک (پدر، مادر، خواهر یا برادر) شما، سابقه ابتلا به بیماری‌های مزمن و شایع زیر وجود دارد؟",
        "question1b": "اگر پاسخ question1a بله بود، چه کسی و در چه سنی به آن مبتلا شده است؟"
      }},
      "question2": "آیا در خانواده درجه یک شما، سابقه حمله قلبی (سکته قلبی)، سکته مغزی، یا نارسایی قلبی وجود دارد؟",
      "question3": {{
        "question3a": "آیا سابقه سرطان خاصی در خانواده درجه یک شما وجود دارد؟",
        "question3b": "اگر پاسخ question3a بله بود، نوع سرطان چه بوده و در چه سنی تشخیص داده شده است؟"
      }}
    }},
    "social_history": {{
      "question1": {{
        "question1a": "آیا تا به حال سیگار، قلیان، پیپ، یا هر نوع محصول نیکوتینی مصرف کرده‌اید؟",
        "question1b": "اگر قبلاً مصرف می‌کردید، چه زمانی ترک کرده‌اید؟"
      }},
      "question2": "آیا الکل مصرف می‌کنید؟ اگر بله، نوع و میزان مصرف آن در هفته چقدر است؟",
      "question3": {{
        "question3a": "آیا تا به حال مواد مخدر مصرف کرده‌اید؟",
        "question3b": "اگر مصرف داشته‌اید، نوع آن و آخرین باری که مصرف کرده‌اید چه زمانی بوده است؟"
      }},
      "question4": "در خانه همراه چه کسانی زندگی می‌کنید؟"
    }},
    "ROS": {{
      "question1": "آیا اخیراً دچار تب، لرز، کاهش یا افزایش وزن ناخواسته، یا خستگی شدید و غیرمعمول شده‌اید؟",
      "question2": "آیا سابقه راش، خارش، زخم‌های طولانی‌مدت، تغییر در رنگ یا بافت پوست/مو/ناخن، یا کبودی غیرعادی دارید؟",
      "question3": "آیا اخیراً دچار سردرد، سرگیجه، سفتی گردن، یا بزرگ شدن غدد لنفاوی در گردن شده‌اید؟",
      "question4": "آیا دچار تاری دید، دوبینی، درد چشم، قرمزی، یا کاهش دید ناگهانی شده‌اید؟",
      "question5": "آیا دچار وزوز گوش، کاهش شنوایی، خونریزی بینی، گرفتگی مزمن بینی، گلودرد مزمن، مشکل در بلع (دیسفاژی)، یا آفت و زخم‌های دهانی مکرر هستید؟",
      "question6": "آیا سابقه درد قفسه سینه، تپش قلب، تنگی نفس با فعالیت، تنگی نفس در حالت خوابیده (ارتوپنه)، یا تورم پاها (ادم) دارید؟",
      "question7": "آیا سابقه سرفه، خس‌خس سینه، خلط خونی (هموپتیزی)، یا تنگی نفس (به جز تنگی نفس مرتبط با فعالیت شدید) دارید؟",
      "question8": "آیا دچار حالت تهوع، استفراغ، سوزش سر دل، درد شکم، تغییر در عادات اجابت مزاج (اسهال یا یبوست)، خونریزی از مقعد، یا زردی پوست و چشم (یرقان) هستید؟",
      "question9": "آیا دچار درد یا سوزش حین ادرار کردن، تکرر ادرار، خون در ادرار (هماچوری)، مشکل در کنترل ادرار، یا ترشحات غیرعادی هستید؟",
      "question10": "آیا دچار درد مفاصل، سفتی صبحگاهی، تورم مفاصل، درد یا ضعف عضلانی، یا کمردرد مزمن هستید؟",
      "question11": "آیا سابقه سردرد شدید یا جدید، تشنج، ضعف یا بی‌حسی در دست‌ها/پاها، مشکل در تعادل/هماهنگی، یا تغییر در حافظه دارید؟",
      "question12": "آیا اخیراً احساس افسردگی، اضطراب، تغییرات شدید خلقی، یا مشکل در خواب (بی‌خوابی/پرخوابی) داشته‌اید؟",
      "question13": "آیا دچار افزایش تشنگی، افزایش گرسنگی، افزایش ادرار (پلی اوری)، یا عدم تحمل گرما/سرما شده‌اید؟",
      "question14": "آیا سابقه کبودی آسان، خونریزی طولانی‌مدت، بزرگ شدن غدد لنفاوی، یا کم‌خونی شدید دارید؟"
    }}
  }},
  "physical_exam": {{
    "general_appearance": {{
      "level_of_consciousness_mood_and_behavior": {{
        "level_of_consciousness": "آیا بیمار هوشیار، گیج، خواب‌آلود (لتارژیک)، یا در حالت اغما (Comatose) است؟ آیا دستورات ساده را اجرا می‌کند؟",
        "mood": "آیا بیمار به نظر بیمار، مضطرب، یا در درد شدید است؟",
        "behavior": "آیا بیمار همکاری می‌کند؟ آیا مضطرب، افسرده، یا پرخاشگر است؟ آیا از نظر روانی وضعیت طبیعی دارد؟"
      }},
      "posture_and_position": {{
        "position_of_comfort": "آیا بیمار وضعیتی را برای کاهش درد یا تنگی نفس انتخاب کرده است؟"
      }},
      "overall_appearance": {{
        "nutritional_status": "آیا بیمار لاغر (Cachectic)، چاق (Obese)، یا در وضعیت وزن طبیعی است؟"
      }},
      "cardiopulmonary_and_circulatory_clues": {{
        "cyanosis": "بررسی لب‌ها، زبان و بستر ناخن برای علائم کبودی.",
        "dyspnea": "آیا بیمار به سختی نفس می‌کشد؟",
        "edema": "وجود تورم در پاها، مچ پا یا اطراف چشم."
      }}
    }},
    "head_and_neck": {{
      "head_and_face": {{
        "symmetry_and_lesions": "آیا سر و صورت بیمار متقارن است و شواهدی از زخم، توده یا ضایعات پوستی وجود دارد؟",
        "tenderness": "آیا در لمس جمجمه حساسیت به لمس یا درد وجود دارد؟"
      }},
      "eyes": {{
        "sclera_and_conjunctiva": "آیا در صلبیه (سفیدی چشم) زردی (یرقان) یا در ملتحمه (پلک پایین) رنگ‌پریدگی شدید (کم‌خونی) مشاهده می‌شود؟",
        "pupils_reaction": "آیا مردمک‌ها متقارن هستند و به نور واکنش طبیعی نشان می‌دهند؟",
        "extraocular_movements": "آیا حرکات چشمی در جهات مختلف کامل و هماهنگ هستند؟"
      }},
      "ears": {{
        "external_and_tenderness": "آیا لاله گوش یا ناحیه ماستوئید (پشت گوش) متورم، قرمز یا دردناک هستند؟",
        "eardrum_appearance": "آیا پرده صماخ در اتوسکوپی ظاهر طبیعی دارد (شفاف، بدون التهاب یا پارگی)؟"
      }},
      "nose_and_sinuses": {{
        "septum_and_discharge": "آیا تیغه بینی انحراف شدید دارد و آیا ترشحات غیرعادی (چرکی یا خونی) مشاهده می‌شود؟",
        "sinus_tenderness": "آیا در لمس یا دق بر روی سینوس‌های پیشانی و فکی (فرونتال و ماگزیلاری) درد وجود دارد؟"
      }},
      "mouth_and_pharynx": {{
        "oral_mucosa_and_lesions": "آیا مخاط دهان (لثه‌ها، زیر زبان) مرطوب و بدون ضایعات غیرعادی (زخم یا آفت) است؟",
        "pharynx_and_tonsils": "آیا حلق (گلو) قرمز یا متورم است و آیا لوزتین‌ها (Tonsils) بزرگ شده‌اند یا دارای ترشحات چرکی هستند؟"
      }},
      "neck_and_lymphatics": {{
        "inspection": "آیا در معاینه ظاهری گردن، تورم، قرمزی، توده، یا زخم قابل مشاهده‌ای وجود دارد؟",
        "tracheal_position": "آیا نای (Trachea) در خط وسط قرار دارد؟ آیا در لمس، انحراف یا جابه‌جایی نای (Tracheal Deviation) احساس می‌شود؟",
        "thyroid_gland": "آیا غده تیروئید (از پشت بیمار) بزرگ است (گواتر)؟ آیا در لمس، ندول (توده)، سفتی، یا حساسیت به لمس وجود دارد؟",
        "carotid_bruit": "آیا در سمع شریان‌های کاروتید، صدای وزوز (Bruit) شنیده می‌شود؟ (نشانه‌ی احتمالی تنگی شریان)",
        "lymph_nodes_size_consistency": "آیا غدد لنفاوی در نواحی مختلف (سرویکال، ساب‌ماندیبولار، سوپراکلاویکولار) بزرگ شده‌اند؟ (اندازه، قوام: نرم/سفت/لاستیکی)",
        "lymph_nodes_mobility_tenderness": "آیا غدد لنفاوی لمس شده، متحرک هستند یا ثابت و چسبیده به بافت زیرین؟ آیا در لمس، درد (Tenderness) دارند؟"
      }}
    }},
    "respiratory_system": {{
      "inspection": {{
        "accessory_muscles": "آیا از عضلات کمکی تنفس استفاده می‌کند؟",
        "chest_shape_and_symmetry": "آیا شکل قفسه سینه طبیعی است (بدون Barrel Chest یا کیفواسکولیوز) و حرکت قفسه سینه در دم و بازدم متقارن است؟"
      }},
      "palpation": {{
        "chest_expansion": "آیا توسعه قفسه سینه در هنگام دم عمیق، متقارن و کامل است؟",
        "tactile_fremitus": "آیا لرزش‌های صوتی (Tactile Fremitus) در دو طرف قفسه سینه متقارن و طبیعی هستند؟"
      }},
      "percussion": "آیا صدای دق در تمام نواحی ریه رزونانس (طبیعی) است یا در برخی نواحی dullness یا hyperresonanse است؟ اگر بله در چه نواحی؟",
      "auscultation": {{
        "breath_sounds_intensity": "آیا شدت صداهای تنفسی پایه طبیعی است یا کاهش یا عدم وجود صدا وجود دارد؟",
        "adventitious_sounds": "آیا صداهای اضافی (Adventitious Sounds) مانند کراکل (Crackles)، ویزینگ (Wheezing)، رونکای (Rhonchi) یا اصطکاک پلورال (Pleural Rub) شنیده می‌شوند؟"
      }}
    }},
    "cardiovascular_system": {{
      "JVP_assessment": "آیا فشار وریدی ژوگولار (JVP) در وضعیت نیمه نشسته، بالا و غیرطبیعی است؟",
      "palpation": {{
        "precordial_palpation_heave_thrill": "آیا در لمس ناحیه پره‌کوردیوم، لیفت (Lift)، هیو (Heave)، یا تریل (Thrill) احساس می‌شود؟",
        "pmi_assessment": "ضربان نوک قلب (PMI) در کجا لمس می‌شود (محل دقیق) و آیا اندازه و قدرت آن طبیعی است؟"
      }},
      "auscultation": {{
        "heart_sounds_s1_s2": "آیا صداهای اصلی قلب (S1 و S2) شنیده می‌شوند و از نظر شدت، اسپلیت و کیفیت، طبیعی هستند؟",
        "extra_sounds_s3_s4_murmurs": "آیا صداهای اضافی مانند S3، S4، مارمار (Murmur) یا صدای اصطکاک پریکاردیال شنیده می‌شود؟"
      }},
      "peripheral_pulses_and_extremities": {{
        "peripheral_pulses_symmetry_and_quality": "آیا تمام نبض‌های محیطی (مانند رادیال، فمورال، دورسالیس پدیس) در دو طرف بدن متقارن، منظم، و با کیفیت (قدرت) طبیعی لمس می‌شوند؟",
        "extremities_color_and_trophic_changes": "آیا در اندام‌های انتهایی، شواهدی از سیانوز (کبودی)، رنگ‌پریدگی، ریزش مو اندام، کلابینگ (Clubbing)، یا تغییرات تروفیک (مانند ریزش مو، نازکی پوست) مشاهده می‌شود؟",
        "extremities_temperature_and_cap_refill": "آیا اندام‌های انتهایی دمای طبیعی دارند و زمان پر شدن مجدد مویرگی (Capillary Refill Time) چند ثانیه است؟",
        "extremities_edema": "آیا در اندام‌های تحتانی، شواهدی از ادم (تورم) و به ویژه ادم گوده‌گذار (Pitting Edema) وجود دارد؟ اگر بله چند + است؟"
      }}
    }},
    "abdominal_system": {{
      "inspection": "آیا شکم از نظر شکل (Flat, Rounded, Protuberant)، تقارن و وجود زخم/اسکار جراحی غیرطبیعی است؟",
      "auscultation": {{
        "bowel_sounds": "آیا صداهای روده (Bowel Sounds) در سمع حضور دارند و فرکانس و شدت آن‌ها طبیعی است (Normoactive)؟ (یا Hyperactive/Hypoactive)",
        "vascular_bruits": "آیا در سمع آئورت یا شریان‌های کلیوی، صدای وزوز (Bruit) شنیده می‌شود؟"
      }},
      "percussion": {{
        "general": " یا dulness وجود داردآیا صدای غالب دق، تیمپانی (Tympany) است؟",
        "organ_borders": "آیا حدود کبد یا طحال در دق، غیرعادی است؟"
      }},
      "palpation": {{
        "superficial_tenderness": "آیا در لمس سطحی، حساسیت به لمس (Tenderness) موضعی یا عمومی وجود دارد؟",
        "deep_masses_and_organs": "آیا در لمس عمقی، توده (Mass) غیرعادی، بزرگی کبد (Hepatomegaly) یا طحال (Splenomegaly) احساس می‌شود؟"
      }},
      "peritoneal_signs": "آیا علائم پریتونیت (مانند ریفاند تندرنس - Rebound Tenderness، یا سفتی غیرارادی عضلات - Guarding) وجود دارد؟"
    }},
    "neurological": {{
      "mental_status_and_LOC": "آیا سطح هوشیاری بیمار طبیعی است و از نظر زمان، مکان و شخص جهت‌یابی (Orientation) دارد؟",
      "cranial_nerves": "آیا عملکرد اعصاب کرانیال اصلی (مانند تقارن حرکات صورت، حرکات چشم و بلع) طبیعی است؟",
      "motor_strength_and_tone": "قدرت عضلانی در اندام‌های فوقانی و تحتانی چقدر است(با استفاده از مقیاس 0 تا 5)؟ و آیا تون عضلانی (سفتی/شلی) طبیعی است؟",
      "involuntary_movements": "آیا حرکات غیرارادی (مانند ترمور، تیک) یا آتروفی (Atrophy) عضلانی مشاهده می‌شود؟",
      "sensory_light_touch_and_pain": "آیا حس‌های لمس سبک و درد/دما در اندام‌ها، متقارن و بدون نقص هستند؟",
      "deep_tendon_reflexes": "آیا رفلکس‌های عمیق تاندونی (DTRs) در تمام اندام‌ها وجود دارند، متقارن هستند و شدت آن‌ها طبیعی است؟ (0 تا 4+)",
      "coordination_and_gait": "آیا تست‌های هماهنگی (مانند انگشت به بینی) نرمال هستند؟ و آیا الگوی راه رفتن (Gait) و تعادل بیمار طبیعی است و در غیر این صورت الگوی Gait بیمار چگونه است؟"
    }},
    "musculoskeletal_system": {{
      "inspection": {{
        "joints": "آیا مفاصل از نظر تورم، قرمزی، بدشکلی (Deformity) یا آتروفی، ظاهر طبیعی دارند؟",
        "muscles": "آیا عضلات از نظر تورم، قرمزی، بدشکلی (Deformity) یا آتروفی، ظاهر طبیعی دارند؟"
      }},
      "palpation": {{
        "tenderness_and_crepitus": "آیا در لمس مفاصل و عضلات، حساسیت به لمس (Tenderness)، گرما، یا صدای ساییده شدن (Crepitus) احساس می‌شود؟"
      }},
      "range_of_motion_active_passive": "آیا دامنه حرکتی (ROM) فعال و غیرفعال مفاصل اصلی (مانند شانه، زانو و هیپ) کامل و بدون درد است؟",
      "stability_and_function": "آیا مفاصل از نظر پایداری (Stability) طبیعی هستند و بیمار می‌تواند عملکرد حرکتی خود را به خوبی انجام دهد؟"
    }}
  }},
  "paraclinic": {{
    "basic_blood_tests": {{
      "CBC": ["Hb", "WBC", "Plt"],
      "ESR/CRP": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "BMP": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "LFTs": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "VBG": "نتایج تست بر اساس بیماری {disease} داده شود."
    }},
    "specialized_lung_tests": {{
      "Sputum_analysis": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "Sputum_AFB": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "a1_antitrypsin_level": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "D_dimer": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "BNP/NT_proBNP": "نتایج تست بر اساس بیماری {disease} داده شود."
    }},
    "immunity_and_serology": {{
      "HIV_test": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "Autoimmune_pannel_ANA_ANCA": "نتایج تست بر اساس بیماری {disease} داده شود."
    }},
    "simple_imaging": {{
      "Chest_X_Ray": {{
        "PA": "در صورت diagnostic نبودن برای بیماری {disease}: رادیولوژیست نمی داند شما چرا درخواست CXR داده اید! با این حال نتایج نرمال هستند. در صورت diagnostic بودن تفسیر یک CXR تیپیک برای بیماری {disease} را خروجی بده.",
        "Lateral": "در صورت diagnostic نبودن برای بیماری {disease}: رادیولوژیست نمی داند شما چرا درخواست CXR داده اید! با این حال نتایج نرمال هستند. در صورت diagnostic بودن تفسیر یک CXR تیپیک برای بیماری {disease} را خروجی بده."
      }}
    }},
    "advanced_imaging": {{
      "Chest_CT_CTPA": "در صورت diagnostic نبودن برای بیماری {disease}: رادیولوژیست نمی داند شما چرا درخواست CT داده اید! با این حال نتایج نرمال هستند. در صورت diagnostic بودن تفسیر یک CT تیپیک برای بیماری {disease} را خروجی بده.",
      "MRI_chest": "در صورت diagnostic نبودن برای بیماری {disease}: رادیولوژیست نمی داند شما چرا درخواست MRI داده اید! با این حال نتایج نرمال هستند. در صورت diagnostic بودن تفسیر یک MRI تیپیک برای بیماری {disease} را خروجی بده.",
      "Pet_scan": "در صورت diagnostic نبودن برای بیماری {disease}: رادیولوژیست نمی داند شما چرا درخواست Pet scan داده اید! با این حال نتایج نرمال هستند. در صورت diagnostic بودن تفسیر یک Pet scan تیپیک برای بیماری {disease} را خروجی بده."
    }},
    "functional_tests": {{
      "Spirometry": "در صورت diagnostic بودن تفسیر یک Spirometry تیپیک برای بیماری {disease} را خروجی بده.",
      "peak_flow": "در صورت diagnostic بودن تفسیر یک peak flow تیپیک برای بیماری {disease} را خروجی بده.",
      "plethysmography": "در صورت diagnostic بودن تفسیر یک plethysmography تیپیک برای بیماری {disease} را خروجی بده."
    }},
    "procedures": {{
      "Bronchoscopy": "در صورت diagnostic نبودن نتایج را نشان بده با این حال اخطاری مبنی بر خطرات انجام این پروسیجر در نبود اندیکاسیون آن بده.",
      "torachonthesis": "در صورت diagnostic نبودن نتایج را نشان بده با این حال اخطاری مبنی بر خطرات انجام این پروسیجر در نبود اندیکاسیون آن بده."
    }}
  }},
  "differential_diagnosis": {{
    "disease1": "Asthma",
    "disease2": "Pneumonia",
    "disease3": "COPD",
    "disease4": "PTE",
    "disease5": "IPF",
    "disease6": "PH",
    "disease7": "Pleural Effusion",
    "disease8": "ARDS"
  }}
}}

evaluation:
{evaluation}

transition:
{transition}

تو یک تحلیل کننده و بازخورددهنده به عملکرد یک دانشجوی پزشکی در یک اپلیکیشن شبیه ساز سناریو تشخیص بیماری های بخش ریه هستی.
برای دادن این بازخورد به چندین اطلاعات نیاز داری که در اختیار تو قرار گرفته است. بخش اول اطلاعات scenario است که شامل سوالاتی است که دانشجو می تواند از بیمار بپرسد تا بیماری او را تشخیص دهد.
بخش دوم اطلاعات evaluation می باشد که در اون تحلیلی از سوالاتی که دانشجو از بیمار پرسیده به تو داده شده. در این بخش A نشان دهنده تعداد سوالاتی است که دانشجو پرسیده است، O نشان دهنده تعداد سوالات بهینه و optimal است که دانشجو باید می پرسیده، C نشان دهنده تعداد سوالاتی که دانشجو از بین سوالات بهینه پرسیده و انتخاب درستی بوده، M تعداد سوالات بهینه ای است که از سوالات بهینه از دست داده و نپرسیده است و همچنین E نشان دهنده سوالاتی است که دانشجو از بین سوالات نامطلوب و غیربهینه انتخاب کرده و باید انتخاب نمی کرده. به علاوه در این بخش سوالاتی که در مجموعه های C و M و E قرار داشتند در C_items و M_items و E_items آمده تا بتوانی در بازخورد به آن ها اشاره کنی و توضیح بدی که دانشجو باید چه کاری انجام می داده که باعث تشخیص دقیق تر و بهتر میشده و کدام سوالات رو درست پرسیده و تشویق کنی.
در بخش سوم اطلاعات یعنی بخش transition این موضوع که دانشجو چه موقع از مرحله گرفتن شرح حال به معاینه فیزیکی رفته و همینطور چه موقع از مرحله معاینه فیزیکی به پاراکلینیک وارد شده بررسی شده است. دانشجو باید حداقل 50 درصد سوالات بهینه را پرسیده باشد تا بتواند وارد بخش بعد شود و اگر قبل از آن چنین کاری انجام دهد به این معناست که زود قضاوت کرده است و این احتمال خطا در تشخیص بیماری را افزایش می دهد. تو می توانی در این اطلاعات در دادن بازخورد نهایی استفاده کنی و به او گوشزد کنی که عملکرد درست چیست.
""",
    input_variables=["disease", "evaluation", "transition"]
)

def feedback_generator(target_disease, STUDENT_LOG):
  evaluation = calculate_set_metrics(OPTIMAL_SCENARIO[f"{target_disease}"], STUDENT_LOG)
  transition = calculate_stage_order_error(OPTIMAL_SCENARIO[f"{target_disease}"], STUDENT_LOG)
  
  evaluation = escape_json_braces(evaluation)
  transition = escape_json_braces(transition)
  
  final_prompt = prompt_template.format(disease=target_disease, evaluation=evaluation, transition=transition)

  structured_chat_model = model.with_structured_output(json_schema)
  output = structured_chat_model.invoke(final_prompt)

  return output