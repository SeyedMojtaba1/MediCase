import getpass
import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json

json_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Clinical_Case_Feedback_Schema",
    "type": "object",
    "properties": {
    "total": {
        "type": "object",
        "properties": {
        "strengths": {
            "type": "string",
            "description": ""
        },
        "weaknesses": {
            "type": "string",
            "description": ""
        },
        "educational_feedback": {
            "type": "string",
            "description": ""
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
            "description": "بگو که انتخابات درستش (C)، چطور اون رو در تشخیص بیماری یاری دادن.\n"
        },
        "weaknesses": {
            "type": "string",
            "description": "اقدامات M (حذفیات) که موجب تأخیر در تشخیص شده‌اند و اقدامات E (اضافی) که منجر به اتلاف زمان یا انحراف از مسیر منطقی شده‌اند، ذکر بشن.\nاگر نقض توالی در گذار ۱←۲ رخ داده باشد، در این بخش تذکر داده می‌شود."
        },
        "educational_feedback": {
            "type": "string",
            "description": "دلایل اهمیت و یا عدم اهمیت هر یک از اقدامات M (حذفیات) و اقدامات E (اضافی) \u00a0ذکر شود.\nتوصیه هایی برای رخ ندادن اشتباهات M و E در آینده داده شود.\nچنانچه نقص توالی وجود داشت، دلیل اشتباه بودن آن شرح داده میشود و توصیه هایی برای رخ ندادن این اشتباهات در آینده داده شود."
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
            "description": "بگو که انتخابات درستش (C)، چطور اون رو در تشخیص بیماری یاری دادن."
        },
        "weaknesses": {
            "type": "string",
            "description": "اقدامات M (حذفیات) که موجب تأخیر در تشخیص شده‌اند و اقدامات E (اضافی) که منجر به اتلاف زمان یا انحراف از مسیر منطقی شده‌اند، ذکر بشن.\nنقض توالی در گذار ۲←۳ به عنوان خطای توالی در این بخش تذکر داده می‌شود.\n"
        },
        "educational_feedback": {
            "type": "string",
            "description": "دلایل اهمیت و یا عدم اهمیت هر یک از اقدامات M (حذفیات) و اقدامات E (اضافی) \u00a0ذکر شود.\nتوصیه هایی برای رخ ندادن اشتباهات M و E در آینده داده شود.\nچنانچه نقص توالی وجود داشت، دلیل اشتباه بودن آن شرح داده میشود و توصیه هایی برای رخ ندادن این اشتباهات در آینده داده شود"
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
            "description": "بگو که انتخابات درستش (C)، چطور اون رو در تشخیص بیماری یاری دادن و هزینه های بیمار رو کاهش دادن.\n"
        },
        "weaknesses": {
            "type": "string",
            "description": "اقدامات M (حذفیات) که موجب تأخیر در تشخیص شده‌اند و اقدامات E (اضافی) که منجر به اتلاف زمان، پول یا انحراف از مسیر منطقی شده‌اند، ذکر بشن"
        },
        "educational_feedback": {
            "type": "string",
            "description": "دلایل اهمیت و یا عدم اهمیت هر یک از اقدامات M (حذفیات) و اقدامات E (اضافی) \u00a0ذکر شود.\nتوصیه هایی برای رخ ندادن اشتباهات M و E در آینده داده شود.\n"
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
            "description": "دانشجو را تشویق کن و بهش بگو که قدم‌های تو از اول تا به انتها داره به تشخیص درست رسونده. ازش تعریف کن و بگو که این یک گام بزرگ در ارتقای مهارت‌های بالینیش بود بهش بگو که این نشون می‌ده که فیلتر نهایی رو بر اساس داده‌های [مهم‌ترین یافته پاراکلینیک] به‌درستی انجام داده و منطق بالینیش قاطع بوده."
        },
        "weaknesses": {
            "type": "string",
            "description": "نقاط ضعف را با توجه به این سه حالت بررسی کن و متناسب با حالت درست جواب بده:\n\u00a0 \u00a0 خطا در نتیجه‌گیری: با ابراز تاسف بگو که تشخیصی که در نهایت داده اشتباه بوده و در مدیریت این بیمار موفق ظاهر نشده اً بهش توصیه‌هایی بکن که چطور می‌تونه روی این بیماری مسلط‌تر بشه.\n\u00a0 \u00a0 یماری اصلی هرگز در لیست نبوده: با ابراز تاسف شدید بگو که بیماری که باید تشخیص داده می‌شده هیچ وقت در لیست تشخیص افتراقی‌هاش قرار نگرفته و این یعنی اینکه ز اون اول منطق فرضیه‌سازی و تحلیل بالینیش مشکل داشته و نیازمند تلاش و مطالعه بیشتری هست.\n\u00a0 \u00a0 خطا در فیلتر کردن: بهش بگو که بیماری‌هایی را در لیست تشخیص افتراقی‌ها داشتی که ارتباطی با بیماری اصلی مریضت نداشتند و باعث گمراه شدن تو در مسیر تشخیص بیماری می‌تونستن بشن بهش گوشزد کن که باید همیشه بر اساس شواهد تشخیص‌های افتراقی بزاریم و یازه که تسلط خودمون رو روی بیماری‌های مختلف افزایش بدیم."
        },
        "educational_feedback": {
            "type": "string",
            "description": "بر اساس ایراداتی که در این مرحله داشته بهش بازخوردهای عملی و توصیه‌های شخصی بکن که بتونه با استفاده از اون‌ها ر مدیریت بیماری‌ها پیشرفت بکنه[۱] تشخیص افتراقی‌ها باید مثل فیلتر عمل کنن، نه مثل لیست خرید. [۲] هر یافته‌ی جدید باید بتونه حداقل یه بیماری رو با قاطعیت حذف کنه. اگه حذف نمی‌کنی، داری آزمایش‌ها رو بیهوده انجام می‌دی. [۳] سؤال آخر: اگه می‌تونستی یه آزمایش رو دوباره تفسیر کنی، کدوم بیماری رو حذف می‌کردی تا به تشخیص نهایی برسی؟"
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



student log: 
{{
  "history_taking": {{
    "present_illness": {{
      "question1": "15:00",
      "question3": "14:00",
      "question8": "13:00"
    }},
    "past_medical_history": {{
      "question1.question1a": "14:30",
      "question1.question1b": "14:15",
      "question3": "12:30"
    }},
    "drug_history": {{
      "question1.question1a": "13:30",
      "question1.question1b": "13:15",
    }}
  }},
  "physical_exam": {{
    "respiratory_system": {{
      "inspection.chest_shape_and_accessory_muscles": "12:00",
      "auscultation.adventitious_sounds": "11:30"
    }},
    "cardiovascular_system": {{
      "JVP_assessment": "11:00"
    }}
  }},
  "paraclinic": {{
    "basic_blood_tests": {{
      "VBG": "10:30",
      "CBC": "09:30"
    }},
    "specialized_lung_tests": {{
      "BNP_NT_proBNP": "10:15",
      "a1_antitrypsin_level": "06:15"
    }},
    "simple_imaging": {{
      "Chest_X_Ray.PA_Lateral": "10:00"
    }},
    "interpretation": {{
      "VBG_BNP_CXR": "09:00"
    }},
    "functional_tests": {{
      "Spirometry": "08:00",
      "plethysmography": "07:00"
    }}
  }},
  "differential_diagnosis": {{
      "disease3": "05:30",
      "disease2": "05:15",
      "disease5": "05:10",
      "disease7": "05:00"
  }},
  {{
    "final_diagnosis": {{
      "disease3": "02:00"
    }}
  }}
}}

optimal scenario: 
{{
  "history_taking": {{
    "present_illness": {{
      "question1": "True",
      "question2": "True",
      "question3": "True",
      "question4": "True",
      "question5": "True",
      "question6": "False",
      "question7": "False",
      "question8": "True",
      "question9": "True",
      "question10": "True"
    }},
    "medical_history": {{
      "question1": {{
        "question1a": "True",
        "question1b": "True"
      }},
      "question2": {{
        "question2a": "False",
        "question2b": "False"
      }},
      "question3": "True",
      "question4": "True",
      "question5": "False",
      "question6": "True"
    }},
    "drug_history": {{
      "question1": {{
        "question1a": "True",
        "question1b": "True",
        "question1c": "True"
      }},
      "question2": "False"
    }},
    "allergies": {{
      "question1": {{
        "question1a": "False",
        "question1b": "False"
      }}
    }},
    "family_history": {{
      "question1": {{
        "question1a": "True",
        "question1b": "True"
      }},
      "question2": "True",
      "question3": {{
        "question3a": "True",
        "question3b": "True"
      }}
    }},
    "social_history": {{
      "question1": {{
        "question1a": "True",
        "question1b": "True"
      }},
      "question2": "False",
      "question3": {{
        "question3a": "False",
        "question3b": "False"
      }},
      "question4": "False"
    }},
    "ROS": {{
      "question1": "True",
      "question2": "False",
      "question3": "False",
      "question4": "False",
      "question5": "False",
      "question6": "True",
      "question7": "True",
      "question8": "False",
      "question9": "False",
      "question10": "False",
      "question11": "False",
      "question12": "False",
      "question13": "False",
      "question14": "False"
    }}
  }},
  "physical_exam": {{
    "general_appearance": {{
      "level_of_consciousness_mood_and_behavior": {{
        "level_of_consciousness": "True",
        "mood": "True",
        "behavior": "True"
      }},
      "posture_and_position": {{
        "position_of_comfort": "True"
      }},
      "overall_appearance": {{
        "nutritional_status": "True"
      }},
      "cardiopulmonary_and_circulatory_clues": {{
        "cyanosis": "True",
        "dyspnea": "True",
        "edema": "True"
      }}
    }},
    "head_and_neck": {{
      "head_and_face": {{
        "symmetry_and_lesions": "False",
        "tenderness": "False"
      }},
      "eyes": {{
        "sclera_and_conjunctiva": "False",
        "pupils_reaction": "False",
        "extraocular_movements": "False"
      }},
      "ears": {{
        "external_and_tenderness": "False",
        "eardrum_appearance": "False"
      }},
      "nose_and_sinuses": {{
        "septum_and_discharge": "False",
        "sinus_tenderness": "False"
      }},
      "mouth_and_pharynx": {{
        "oral_mucosa_and_lesions": "False",
        "pharynx_and_tonsils": "False"
      }},
      "neck_and_lymphatics": {{
        "inspection": "False",
        "tracheal_position": "False",
        "thyroid_gland": "False",
        "carotid_bruit": "False",
        "lymph_nodes_size_consistency": "False",
        "lymph_nodes_mobility_tenderness": "False"
      }}
    }},
    "respiratory_system": {{
      "inspection": {{
        "accessory_muscles": "True",
        "chest_shape_and_symmetry": "True"
      }},
      "palpation": {{
        "chest_expansion": "True",
        "tactile_fremitus": "True"
      }},
      "percussion": "True",
      "auscultation": {{
        "breath_sounds_intensity": "True",
        "adventitious_sounds": "True"
      }}
    }},
    "cardiovascular_system": {{
      "JVP_assessment": "True",
      "palpation": {{
        "precordial_palpation_heave_thrill": "False",
        "pmi_assessment": "False"
      }},
      "auscultation": {{
        "heart_sounds_s1_s2": "True",
        "extra_sounds_s3_s4_murmurs": "False"
      }},
      "peripheral_pulses_and_extremities": {{
        "peripheral_pulses_symmetry_and_quality": "True",
        "extremities_color_and_trophic_changes": "True",
        "extremities_temperature_and_cap_refill": "False",
        "extremities_edema": "True"
      }}
    }},
    "abdominal_system": {{
      "inspection": "False",
      "auscultation": {{
        "bowel_sounds": "False",
        "vascular_bruits": "False"
      }},
      "percussion": {{
        "general": "False",
        "organ_borders": "False"
      }},
      "palpation": {{
        "superficial_tenderness": "False",
        "deep_masses_and_organs": "False",
        "peritoneal_signs": "False"
      }}
    }},
    "neurological": {{
      "mental_status_and_LOC": "False",
      "cranial_nerves": "False",
      "motor_strength_and_tone": "False",
      "involuntary_movements": "False",
      "sensory_light_touch_and_pain": "False",
      "deep_tendon_reflexes": "False",
      "coordination_and_gait": "False"
    }},
    "musculoskeletal_system": {{
      "inspection": {{
        "joints": "False",
        "muscles": "False"
      
      }},
      "palpation": {{
        "tenderness_and_crepitus": "False"
      }},
      "range_of_motion_active_passive": "False",
      "stability_and_function": "False"
    }}
  }},
  "paraclinic": {{
    "basic_blood_tests": {{
      "CBC": [
        "True",
        "True",
        "False"
      ],
      "ESR/CRP": "True",
      "BMP": "False",
      "LFTs": "False",
      "VBG": "True"
    }},
    "specialized_lung_tests": {{
      "Sputum_analysis": "False",
      "Sputum_AFB": "False",
      "a1_antitrypsin_level": "True",
      "D_dimer": "False",
      "BNP/NT_proBNP": "True"
    }},
    "immunity_and_serology": {{
      "HIV_test": "False",
      "Autoimmune_pannel_ANA_ANCA": "False"
    }},
    "simple_imaging": {{
      "Chest_X_Ray": {{
        "PA": "True",
        "Lateral": "True"
      }}
    }},
    "advanced_imaging": {{
      "Chest_CT_CTPA": "True",
      "MRI_chest": "False",
      "Pet_scan": "False"
    }},
    "functional_tests": {{
      "Spirometry": "True",
      "peak_flow": "True",
      "plethysmography": "True"
    }},
    "procedures": {{
      "Bronchoscopy": "False",
      "torachonthesis": "False"
    }}
  }},
  "differential_diagnosis": {{
        "disease1": "True",
        "disease2": "False",
        "disease3": "True",
        "disease4": "False",
        "disease5": "True",
        "disease6": "True",
        "disease7": "False",
        "disease8": "False"
    }}
}}


 خروجی ها بر اساس لاگ اطلاعات دانشجو که در آن زمان از دقیقه 15 شروع و تا دقیقه 0 پایان می یابد، آپشن های سناریو و موارد بهینه انتخابی بیماری {disease} با لحنی دوستانه، مودب و صمیمی داده میشود.
گام اول: شناسایی مجموعه‌ها
در هر مرحله از فرآیند تشخیص، مجموعه‌ها به صورت زیر تعریف می‌شوند:

O: مجموعه اقدامات بهینه (استاندارد طلایی در آن مرحله)
A: مجموعه اقدامات انتخابی دانشجو در همان مرحله
C = A ∩ O: اقدامات صحیح انتخاب‌شده (منطبق با استاندارد)
E = A / O: اقدامات اضافی و غیرضروری (انتخاب‌های نادرست)
M = O / A: اقدامات بهینه‌ای که انجام نشده‌اند (حذفیات)

این چهار مجموعه پایه‌ی محاسبه امتیاز، تحلیل منطق عملکرد دانشجو، و تولید بازخورد آموزشی هستند.

 گام دوم: محاسبه نمره مرحله
نمره هر مرحله بر اساس فرمول وزن‌دهی R، P_M، P_E محاسبه می‌شود تا دقت، پوشش و منطق بالینی ارزیابی شود.
وزن هر مرحله متناسب با ارزش تشخیصی آن تعیین می‌گردد.

 گام سوم: ارزیابی ترتیب مراحل
اصل بنیادین:
توالی مراحل باید دقیقاً به‌صورت شرح حال → معاینه فیزیکی → پاراکلینیک رعایت شود.
عبور زودهنگام از هر مرحله بدون تکمیل حداقل ۵۰٪ از مرحله قبل، خطای تریاژ محسوب می‌شود.

 قانون توالی:
1. گذار ۱ → ۲ (شرح حال به معاینه):

 اولین اقدام دانشجو در مرحله ۲ را شناسایی کنید.
 تعداد اقدامات مرحله ۱ (|A₁|) تا آن لحظه را بشمارید.
 اگر |A₁| < ۵۰٪ از |O₁| باشد → دانشجو قبل از تکمیل شرح حال کافی وارد معاینه شده است.
 ثبت به عنوان Stage Order Error – شرح حال ناقص.

2. گذار ۲ → ۳ (معاینه به پاراکلینیک):

 اولین اقدام دانشجو در مرحله ۳ را شناسایی کنید
 تعداد اقدامات مرحله ۲ (|A₂|) تا آن لحظه را بشمارید.
اگر |A₂| < ۵۰٪ از |O₂| باشد → دانشجو قبل از انجام معاینه کافی وارد پاراکلینیک شده است.
ثبت به عنوان Stage Order Error – معاینه ناقص (با جریمه بیشتر).

پیامد ارزیابی:
هر نقض توالی باید در دو بخش ذکر شود:

 در «نقاط ضعف» مرحله‌ای که زود شروع شده است
در «بازخورد کلی» به‌عنوان تذکر شدید در اولویت‌بندی بالینی.
""",
    input_variables=["disease"]
)

final_prompt = prompt_template.format(disease=target_disease)

structured_chat_model = model.with_structured_output(json_schema)
output = structured_chat_model.invoke(final_prompt)
json_output = json.dumps(output, indent=4, ensure_ascii=False)

print(json_output)