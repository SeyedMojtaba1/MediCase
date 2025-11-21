import getpass
import os
from langchain.chat_models import init_chat_model
# from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json
import random

json_schema = {
  "title": "MedicalCase",
  "type": "object",
  "properties": {
    "patient_profile": {
      "title": "Patient Profile",
      "description": "patient_profile",
      "type": "object",
      "properties": {
        "personal_information": {
          "title": "Personal Information",
          "description": "personal_information",
          "type": "object",
          "properties": {
            "first_name": {
              "title": "First Name",
              "type": "string",
              "description": ""
            },
            "last_name": {
              "title": "Last Name",
              "type": "string",
              "description": ""
            },
            "age": {
              "title": "Age",
              "type": "string",
              "description": "سن بیمار باید متناسب با شیوع بیماری انتخاب شود. در بیماری‌های مزمن تنفسی و قلبی معمولاً میانسالی تا سالمندی (حدود 45 تا 80 سال)، در بیماری‌های حاد یا ارثی ممکن است سن پایین‌تر باشد. برای تنوع، سن را در بازه منطقی بیماری انتخاب کن، نه مقدار ثابت."
            },
            "gender": {
              "title": "Gender",
              "type": "string",
              "description": ""
            },
            "occupation": {
              "title": "Occupation",
              "type": "string",
              "description": "شغل بیمار بیان شود و درصورت بازنشسته بودن بیمار شغلی که از آن بازنشسته شده است را بیان کن."
            },
            "place_of_birth": {
              "title": "Place Of Birth",
              "type": "string",
              "description": ""
            },
            "place_of_residence": {
              "title": "Place Of Residence",
              "type": "string",
              "description": ""
            },
            "marital_status": {
              "title": "Marital Status",
              "type": "string",
              "description": ""
            }
          },
          "required": [
            "first_name",
            "last_name",
            "age",
            "gender",
            "occupation",
            "place_of_birth",
            "place_of_residence",
            "marital_status"
          ]
        },
        "chief_complaint": {
          "title": "Chief Complaint",
          "type": "string",
          "description": "شامل دلیل اصلی مراجعه بیمار و زمان شروع آن است"
        },
        "vital_sign": {
          "title": "Vital Sign",
          "description": "vital_sign",
          "type": "object",
          "properties": {
            "BP": {
              "title": "Bp",
              "type": "string",
              "description": "Blood Pressure"
            },
            "T": {
              "title": "T",
              "type": "string",
              "description": "Temprature"
            },
            "PR": {
              "title": "Pr",
              "type": "string",
              "description": "Pulse Rate"
            },
            "RR": {
              "title": "Rr",
              "type": "string",
              "description": "Respiratory Rate"
            },
            "SpO2": {
              "title": "Spo2",
              "type": "string",
              "description": "Saturation of O2"
            },
            "GCS": {
              "title": "Gcs",
              "type": "string",
              "description": "Level of Consiousness"
            }
          },
          "required": [
            "BP",
            "T",
            "PR",
            "RR",
            "SpO2",
            "GCS"
          ]
        }
      },
      "required": [
        "personal_information",
        "chief_complaint",
        "vital_sign"
      ]
    },
    "history_taking": {
      "title": "History Taking",
      "description": "history_taking",
      "type": "object",
      "properties": {
        "present_illness": {
          "title": "Present Illness",
          "description": "present_illness",
          "type": "object",
          "properties": {
            "question1": {
              "title": "Question1",
              "type": "string",
              "description": "علائم از چه زمانی شروع شدند و در طول زمان چه تغییری کردند؟"
            },
            "question2": {
              "title": "Question2",
              "type": "string",
              "description": "شروع علائم ناگهانی بوده یا تدریجی؟ بعد از اتفاق خاصی مثل عفونت یا تماس خاصی شروع شد؟"
            },
            "question3": {
              "title": "Question3",
              "type": "string",
              "description": "آیا تنگی نفس دارید؟ اگر بله تنگی نفستون دائمیه یا دوره‌ای؟ و با فعالیت بدتر میشه یا در حالت استراحت هم وجود داره؟"
            },
            "question4": {
              "title": "Question4",
              "type": "string",
              "description": "سرفه دارید؟ اگر بله، خشک است یا همراه با خلط؟ رنگ و حجم خلط چطور است؟"
            },
            "question5": {
              "title": "Question5",
              "type": "string",
              "description": "تا حالا خس‌خس یا صدای غیرعادی در تنفس شنیدید؟"
            },
            "question6": {
              "title": "Question6",
              "type": "string",
              "description": "احساس درد یا فشار در قفسه سینه دارید؟ با تنفس یا حرکت تغییر می‌کنه؟"
            },
            "question7": {
              "title": "Question7",
              "type": "string",
              "description": "در روزهای اخیر تب، لرز یا تعریق شبانه داشتید؟ وجود یا عدم وجود تب باید با زمینهٔ بالینی هماهنگ باشد. در بیماری‌های مزمن پایدار معمولاً تب وجود ندارد، اما در تشدید حاد یا عفونت‌ها ممکن است تب و لرز مشاهده شود. پاسخ 'بله' یا 'خیر' را بر اساس ماهیت بیماری و مرحله آن تولید کن."
            },
            "question8": {
              "title": "Question8",
              "type": "string",
              "description": "تورم پا، تپش قلب یا احساس سبکی سر دارید؟"
            },
            "question9": {
              "title": "Question9",
              "type": "string",
              "description": "قبلاً هم چنین حمله یا علائمی داشتید؟ چه درمانی کمکتون کرده؟"
            },
            "question10": {
              "title": "Question10",
              "type": "string",
              "description": "احساس کاهش وزن، خستگی یا بی‌اشتهایی داشتید؟"
            }
          },
          "required": [
            "question1",
            "question2",
            "question3",
            "question4",
            "question5",
            "question6",
            "question7",
            "question8",
            "question9",
            "question10"
          ]
        },
        "past_medical_history": {
          "title": "Past Medical History",
          "description": "past_medical_history",
          "type": "object",
          "properties": {
            "question1": {
              "title": "Question1",
              "description": "question1",
              "type": "object",
              "properties": {
                "question1a": {
                  "title": "Question1a",
                  "type": "string",
                  "description": "آیا بیماری طولانی مدت (مزمن) مثل قند (دیابت)، فشار خون، آسم، مشکل تیروئید، یا بیماری جدی کلیوی/کبدی دارید؟"
                },
                "question1b": {
                  "title": "Question1b",
                  "type": "string",
                  "description": "اگر پاسخ question1a بله بود، تشخیص این بیماری از چه موقع بوده است؟"
                }
              },
              "required": [
                "question1a",
                "question1b"
              ]
            },
            "question3": {
              "title": "Question3",
              "type": "string",
              "description": "آیا سابقه بیماری های قلبی، ریوی و مغزی را دارید؟"
            },
            "question4": {
              "title": "Question4",
              "type": "string",
              "description": "آیا در حال حاظر یا در گذشته سرطان فعال داشته‌اید؟"
            },
            "question5": {
              "title": "Question5",
              "type": "string",
              "description": "در دوران کودکی، آیا بیماری‌های خاصی (مثل تب روماتیسمی، سرخک شدید) گرفتید یا به دلیل بیماری بستری شدید؟"
            },
            "question6": {
              "title": "Question6",
              "type": "string",
              "description": "برنامه واکسن‌ها (مثل کزاز و آنفولانزا) شما کامل و به روز است؟"
            },
            "question2": {
              "title": "Question2",
              "description": "question2",
              "type": "object",
              "properties": {
                "question2a": {
                  "title": "Question2a",
                  "type": "string",
                  "description": "آیا تا به حال عمل جراحی (بزرگ یا کوچک) داشته‌اید؟ و آیا تا به حال در بیمارستان بستری شده‌اید؟"
                },
                "question2b": {
                  "title": "Question2b",
                  "type": "string",
                  "description": "اگر پاسخ question2a بله بود، دلیلش چه بوده و دقیقا چند وقت پیش بوده است؟(چند سال و چند ماه) همچنین، آیا تا به حال انتقال خون داشته‌اید؟"
                }
              },
              "required": [
                "question2a",
                "question2b"
              ]
            }
          },
          "required": [
            "question1",
            "question3",
            "question4",
            "question5",
            "question6",
            "question2"
          ]
        },
        "drug_history": {
          "title": "Drug History",
          "description": "drug_history",
          "type": "object",
          "properties": {
            "question1": {
              "title": "Question1",
              "description": "question1",
              "type": "object",
              "properties": {
                "question1a": {
                  "title": "Question1a",
                  "type": "string",
                  "description": "لطفاً لیست تمام داروهایی که در حال حاضر به صورت مرتب (روزانه، هفتگی یا ماهانه) مصرف می‌کنید را به من بگویید."
                },
                "question1b": {
                  "title": "Question1b",
                  "type": "string",
                  "description": "دوز هر دارو چقدر است و چند بار در روز مصرف می‌کنید؟"
                },
                "question1c": {
                  "title": "Question1c",
                  "type": "string",
                  "description": "آیا در چند روز گذشته، دوز یا زمان مصرف هیچ‌کدام از این داروها را تغییر داده‌اید؟"
                }
              },
              "required": [
                "question1a",
                "question1b",
                "question1c"
              ]
            },
            "question2": {
              "title": "Question2",
              "type": "string",
              "description": "به صورت منظم داروهای بدون نسخه (OTC) (مثل داروهای سرماخوردگی، مسکن‌ها، آنتی‌اسیدها)، مکمل‌های غذایی، داروهای گیاهی یا خواب آور مصرف می‌کنید؟"
            }
          },
          "required": [
            "question1",
            "question2"
          ]
        },
        "allergies": {
          "title": "Allergies",
          "description": "allergies",
          "type": "object",
          "properties": {
            "question1": {
              "title": "Question1",
              "description": "question1",
              "type": "object",
              "properties": {
                "question1a": {
                  "title": "Question1a",
                  "type": "string",
                  "description": "آیا به دارو، غذا، یا ماده خاصی آلرژی (حساسیت) دارید؟"
                },
                "question1b": {
                  "title": "Question1b",
                  "type": "string",
                  "description": "اگر پاسخ question1a بله بود، دقیقاً چه دارو یا ماده‌ای است؟ و واکنش شما (مثل کهیر یا تنگی نفس) چگونه بوده است؟"
                }
              },
              "required": [
                "question1a",
                "question1b"
              ]
            }
          },
          "required": [
            "question1"
          ]
        },
        "family_history": {
          "title": "Family History",
          "description": "family_history",
          "type": "object",
          "properties": {
            "question2": {
              "title": "Question2",
              "type": "string",
              "description": "آیا در خانواده درجه یک شما، سابقه حمله قلبی (سکته قلبی)، سکته مغزی، یا نارسایی قلبی وجود دارد؟"
            },
            "question1": {
              "title": "Question1",
              "description": "question1",
              "type": "object",
              "properties": {
                "question1a": {
                  "title": "Question1a",
                  "type": "string",
                  "description": "آیا در خانواده درجه یک (پدر، مادر، خواهر یا برادر) شما، سابقه ابتلا به بیماری‌های مزمن و شایع وجود دارد؟"
                },
                "question1b": {
                  "title": "Question1b",
                  "type": "string",
                  "description": "اگر پاسخ question1a بله بود، چه کسی و در چه سنی به آن مبتلا شده است؟"
                }
              },
              "required": [
                "question1a",
                "question1b"
              ]
            },
            "question3": {
              "title": "Question3",
              "description": "question3",
              "type": "object",
              "properties": {
                "question3a": {
                  "title": "Question3a",
                  "type": "string",
                  "description": "آیا سابقه سرطان خاصی در خانواده درجه یک شما وجود دارد؟"
                },
                "question3b": {
                  "title": "Question3b",
                  "type": "string",
                  "description": "اگر پاسخ question3a بله بود، نوع سرطان چه بوده و در چه سنی تشخیص داده شده است؟"
                }
              },
              "required": [
                "question3a",
                "question3b"
              ]
            }
          },
          "required": [
            "question2",
            "question1",
            "question3"
          ]
        },
        "social_history": {
          "title": "Social History",
          "description": "social_history",
          "type": "object",
          "properties": {
            "question1": {
              "title": "Question1",
              "description": "question1",
              "type": "object",
              "properties": {
                "question1a": {
                  "title": "Question1a",
                  "type": "string",
                  "description": "آیا تا به حال سیگار، قلیان، پیپ، یا هر نوع محصول نیکوتینی مصرف کرده‌اید؟"
                },
                "question1b": {
                  "title": "Question1b",
                  "type": "string",
                  "description": "اگر قبلاً مصرف می‌کردید، چه زمانی ترک کرده‌اید؟"
                }
              },
              "required": [
                "question1a",
                "question1b"
              ]
            },
            "question2": {
              "title": "Question2",
              "type": "string",
              "description": "آیا الکل مصرف می‌کنید؟ اگر بله، نوع و میزان مصرف آن در هفته چقدر است؟"
            },
            "question3": {
              "title": "Question3",
              "description": "question3",
              "type": "object",
              "properties": {
                "question3a": {
                  "title": "Question3a",
                  "type": "string",
                  "description": "آیا تا به حال مواد مخدر مصرف کرده‌اید؟"
                },
                "question3b": {
                  "title": "Question3b",
                  "type": "string",
                  "description": "اگر مصرف داشته‌اید، نوع آن و آخرین باری که مصرف کرده‌اید چه زمانی بوده است؟"
                }
              },
              "required": [
                "question3a",
                "question3b"
              ]
            },
            "question4": {
              "title": "Question4",
              "type": "string",
              "description": "در خانه همراه چه کسانی زندگی می‌کنید؟"
            }
          },
          "required": [
            "question1",
            "question2",
            "question3",
            "question4"
          ]
        },
        "ros": {
          "title": "Ros",
          "description": "ROS",
          "type": "object",
          "properties": {
            "question1": {
              "title": "Question1",
              "type": "string",
              "description": "آیا اخیراً دچار تب، لرز، کاهش یا افزایش وزن ناخواسته، یا خستگی شدید و غیرمعمول شده‌اید؟"
            },
            "question2": {
              "title": "Question2",
              "type": "string",
              "description": "آیا سابقه راش، خارش، زخم‌های طولانی‌مدت، تغییر در رنگ یا بافت پوست/مو/ناخن، یا کبودی غیرعادی دارید؟"
            },
            "question3": {
              "title": "Question3",
              "type": "string",
              "description": "آیا اخیراً دچار سردرد، سرگیجه، سفتی گردن، یا بزرگ شدن غدد لنفاوی در گردن شده‌اید؟"
            },
            "question4": {
              "title": "Question4",
              "type": "string",
              "description": "آیا دچار تاری دید، دوبینی، درد چشم، قرمزی، یا کاهش دید ناگهانی شده‌اید؟"
            },
            "question5": {
              "title": "Question5",
              "type": "string",
              "description": "آیا دچار وزوز گوش، کاهش شنوایی، خونریزی بینی، گرفتگی مزمن بینی، گلودرد مزمن، مشکل در بلع (دیسفاژی)، یا آفت و زخم‌های دهانی مکرر هستید؟"
            },
            "question6": {
              "title": "Question6",
              "type": "string",
              "description": "آیا سابقه درد قفسه سینه، تپش قلب، تنگی نفس با فعالیت، تنگی نفس در حالت خوابیده ، یا تورم پاها دارید؟"
            },
            "question7": {
              "title": "Question7",
              "type": "string",
              "description": "آیا سابقه سرفه، خس‌خس سینه، خلط خونی ، یا تنگی نفس (به جز تنگی نفس مرتبط با فعالیت شدید) دارید؟"
            },
            "question8": {
              "title": "Question8",
              "type": "string",
              "description": "آیا دچار حالت تهوع، استفراغ، سوزش سر دل، درد شکم، تغییر در عادات اجابت مزاج (اسهال یا یبوست)، خونریزی از مقعد، یا زردی پوست و چشم هستید؟"
            },
            "question9": {
              "title": "Question9",
              "type": "string",
              "description": "آیا دچار درد یا سوزش حین ادرار کردن، تکرر ادرار، خون در ادرار، مشکل در کنترل ادرار، یا ترشحات غیرعادی هستید؟"
            },
            "question10": {
              "title": "Question10",
              "type": "string",
              "description": "آیا دچار درد مفاصل، سفتی صبحگاهی، تورم مفاصل، درد یا ضعف عضلانی، یا کمردرد مزمن هستید؟"
            },
            "question11": {
              "title": "Question11",
              "type": "string",
              "description": "آیا سابقه سردرد شدید یا جدید، تشنج، ضعف یا بی‌حسی در دست‌ها/پاها، مشکل در تعادل/هماهنگی، یا تغییر در حافظه دارید؟"
            },
            "question12": {
              "title": "Question12",
              "type": "string",
              "description": "آیا اخیراً احساس افسردگی، اضطراب، تغییرات شدید خلقی، یا مشکل در خواب (بی‌خوابی/پرخوابی) داشته‌اید؟"
            },
            "question13": {
              "title": "Question13",
              "type": "string",
              "description": "آیا دچار افزایش تشنگی، افزایش گرسنگی، افزایش ادرار (پلی اوری)، یا عدم تحمل گرما/سرما شده‌اید؟"
            },
            "question14": {
              "title": "Question14",
              "type": "string",
              "description": "آیا سابقه کبودی آسان، خونریزی طولانی‌مدت، بزرگ شدن غدد لنفاوی، یا کم‌خونی شدید دارید؟"
            }
          },
          "required": [
            "question1",
            "question2",
            "question3",
            "question4",
            "question5",
            "question6",
            "question7",
            "question8",
            "question9",
            "question10",
            "question11",
            "question12",
            "question13",
            "question14"
          ]
        }
      },
      "required": [
        "present_illness",
        "past_medical_history",
        "drug_history",
        "allergies",
        "family_history",
        "social_history",
        "ros"
      ]
    },
    "physical_exam": {
      "title": "Physical Exam",
      "description": "physical_exam",
      "type": "object",
      "properties": {
        "general_appearance": {
          "title": "General Appearance",
          "description": "general_appearance",
          "type": "object",
          "properties": {
            "level_of_consciousness_mood_and_behavior": {
              "title": "Level Of Consciousness Mood And Behavior",
              "description": "level_of_consciousness_mood_and_behavior",
              "type": "object",
              "properties": {
                "level_of_consciousness": {
                  "title": "Level Of Consciousness",
                  "type": "string",
                  "description": "آیا بیمار هوشیار، گیج، خواب‌آلود (لتارژیک)، یا در حالت اغما (Comatose) است؟ آیا دستورات ساده را اجرا می‌کند؟"
                },
                "mood": {
                  "title": "Mood",
                  "type": "string",
                  "description": "آیا بیمار به نظر بیمار، مضطرب، یا در درد شدید است؟"
                },
                "behavior": {
                  "title": "Behavior",
                  "type": "string",
                  "description": "آیا بیمار همکاری می‌کند؟ آیا مضطرب، افسرده، یا پرخاشگر است؟ آیا از نظر روانی وضعیت طبیعی دارد؟"
                }
              },
              "required": [
                "level_of_consciousness",
                "mood",
                "behavior"
              ]
            },
            "posture_and_position": {
              "title": "Posture And Position",
              "description": "posture_and_position",
              "type": "object",
              "properties": {
                "position_of_comfort": {
                  "title": "Position Of Comfort",
                  "type": "string",
                  "description": "آیا بیمار وضعیتی را برای کاهش درد یا تنگی نفس انتخاب کرده است؟"
                }
              },
              "required": [
                "position_of_comfort"
              ]
            },
            "overall_appearance": {
              "title": "Overall Appearance",
              "description": "overall_appearance",
              "type": "object",
              "properties": {
                "nutritional_status": {
                  "title": "Nutritional Status",
                  "type": "string",
                  "description": "آیا بیمار لاغر (Cachectic)، چاق (Obese)، یا در وضعیت وزن طبیعی است؟"
                }
              },
              "required": [
                "nutritional_status"
              ]
            },
            "cardiopulmonary_and_circulatory_clues": {
              "title": "Cardiopulmonary And Circulatory Clues",
              "description": "cardiopulmonary_and_circulatory_clues",
              "type": "object",
              "properties": {
                "cyanosis": {
                  "title": "Cyanosis",
                  "type": "string",
                  "description": "بررسی لب‌ها، زبان و بستر ناخن برای علائم کبودی."
                },
                "dyspnea": {
                  "title": "Dyspnea",
                  "type": "string",
                  "description": "آیا بیمار به سختی نفس می‌کشد؟"
                },
                "edema": {
                  "title": "Edema",
                  "type": "string",
                  "description": "وجود تورم در پاها، مچ پا یا اطراف چشم."
                }
              },
              "required": [
                "cyanosis",
                "dyspnea",
                "edema"
              ]
            }
          },
          "required": [
            "level_of_consciousness_mood_and_behavior",
            "posture_and_position",
            "overall_appearance",
            "cardiopulmonary_and_circulatory_clues"
          ]
        },
        "head_and_neck": {
          "title": "Head And Neck",
          "description": "head_and_neck",
          "type": "object",
          "properties": {
            "head_and_face": {
              "title": "Head And Face",
              "description": "head_and_face",
              "type": "object",
              "properties": {
                "symmetry_and_lesions": {
                  "title": "Symmetry And Lesions",
                  "type": "string",
                  "description": "آیا سر و صورت بیمار متقارن است و شواهدی از زخم، توده یا ضایعات پوستی وجود دارد؟"
                },
                "tenderness": {
                  "title": "Tenderness",
                  "type": "string",
                  "description": "آیا در لمس جمجمه حساسیت به لمس یا درد وجود دارد؟"
                }
              },
              "required": [
                "symmetry_and_lesions",
                "tenderness"
              ]
            },
            "eyes": {
              "title": "Eyes",
              "description": "eyes",
              "type": "object",
              "properties": {
                "sclera_and_conjunctiva": {
                  "title": "Sclera And Conjunctiva",
                  "type": "string",
                  "description": "آیا در صلبیه (سفیدی چشم) زردی (یرقان) یا در ملتحمه (پلک پایین) رنگ‌پریدگی شدید (کم‌خونی) مشاهده می‌شود؟"
                },
                "pupils_reaction": {
                  "title": "Pupils Reaction",
                  "type": "string",
                  "description": "آیا مردمک‌ها متقارن هستند و به نور واکنش طبیعی نشان می‌دهند؟"
                },
                "extraocular_movements": {
                  "title": "Extraocular Movements",
                  "type": "string",
                  "description": "آیا حرکات چشمی در جهات مختلف کامل و هماهنگ هستند؟"
                }
              },
              "required": [
                "sclera_and_conjunctiva",
                "pupils_reaction",
                "extraocular_movements"
              ]
            },
            "ears": {
              "title": "Ears",
              "description": "ears",
              "type": "object",
              "properties": {
                "external_and_tenderness": {
                  "title": "External And Tenderness",
                  "type": "string",
                  "description": "آیا لاله گوش یا ناحیه ماستوئید (پشت گوش) متورم، قرمز یا دردناک هستند؟"
                },
                "eardrum_appearance": {
                  "title": "Eardrum Appearance",
                  "type": "string",
                  "description": "آیا پرده صماخ در اتوسکوپی ظاهر طبیعی دارد (شفاف، بدون التهاب یا پارگی)؟"
                }
              },
              "required": [
                "external_and_tenderness",
                "eardrum_appearance"
              ]
            },
            "nose_and_sinuses": {
              "title": "Nose And Sinuses",
              "description": "nose_and_sinuses",
              "type": "object",
              "properties": {
                "septum_and_discharge": {
                  "title": "Septum And Discharge",
                  "type": "string",
                  "description": "آیا تیغه بینی انحراف شدید دارد و آیا ترشحات غیرعادی (چرکی یا خونی) مشاهده می‌شود؟"
                },
                "sinus_tenderness": {
                  "title": "Sinus Tenderness",
                  "type": "string",
                  "description": "آیا در لمس یا دق بر روی سینوس‌های پیشانی و فکی (فرونتال و ماگزیلاری) درد وجود دارد؟"
                }
              },
              "required": [
                "septum_and_discharge",
                "sinus_tenderness"
              ]
            },
            "mouth_and_pharynx": {
              "title": "Mouth And Pharynx",
              "description": "mouth_and_pharynx",
              "type": "object",
              "properties": {
                "oral_mucosa_and_lesions": {
                  "title": "Oral Mucosa And Lesions",
                  "type": "string",
                  "description": "آیا مخاط دهان (لثه‌ها، زیر زبان) مرطوب و بدون ضایعات غیرعادی (زخم یا آفت) است؟"
                },
                "pharynx_and_tonsils": {
                  "title": "Pharynx And Tonsils",
                  "type": "string",
                  "description": "آیا حلق (گلو) قرمز یا متورم است و آیا لوزتین‌ها (Tonsils) بزرگ شده‌اند یا دارای ترشحات چرکی هستند؟"
                }
              },
              "required": [
                "oral_mucosa_and_lesions",
                "pharynx_and_tonsils"
              ]
            },
            "neck_and_lymphatics": {
              "title": "Neck And Lymphatics",
              "description": "neck_and_lymphatics",
              "type": "object",
              "properties": {
                "inspection": {
                  "title": "Inspection",
                  "type": "string",
                  "description": "آیا در معاینه ظاهری گردن، تورم، قرمزی، توده، یا زخم قابل مشاهده‌ای وجود دارد؟"
                },
                "tracheal_position": {
                  "title": "Tracheal Position",
                  "type": "string",
                  "description": "آیا نای (Trachea) در خط وسط قرار دارد؟ آیا در لمس، انحراف یا جابه‌جایی نای (Tracheal Deviation) احساس می‌شود؟"
                },
                "thyroid_gland": {
                  "title": "Thyroid Gland",
                  "type": "string",
                  "description": "آیا غده تیروئید (از پشت بیمار) بزرگ است (گواتر)؟ آیا در لمس، ندول (توده)، سفتی، یا حساسیت به لمس وجود دارد؟"
                },
                "carotid_bruit": {
                  "title": "Carotid Bruit",
                  "type": "string",
                  "description": "آیا در سمع شریان‌های کاروتید، صدای وزوز (Bruit) شنیده می‌شود؟ (نشانه‌ی احتمالی تنگی شریان)"
                },
                "lymph_nodes_size_consistency": {
                  "title": "Lymph Nodes Size Consistency",
                  "type": "string",
                  "description": "آیا غدد لنفاوی در نواحی مختلف (سرویکال، ساب‌ماندیبولار، سوپراکلاویکولار) بزرگ شده‌اند؟ (اندازه، قوام: نرم/سفت/لاستیکی)"
                },
                "lymph_nodes_mobility_tenderness": {
                  "title": "Lymph Nodes Mobility Tenderness",
                  "type": "string",
                  "description": "آیا غدد لنفاوی لمس شده، متحرک هستند یا ثابت و چسبیده به بافت زیرین؟ آیا در لمس، درد (Tenderness) دارند؟"
                }
              },
              "required": [
                "inspection",
                "tracheal_position",
                "thyroid_gland",
                "carotid_bruit",
                "lymph_nodes_size_consistency",
                "lymph_nodes_mobility_tenderness"
              ]
            }
          },
          "required": [
            "head_and_face",
            "eyes",
            "ears",
            "nose_and_sinuses",
            "mouth_and_pharynx",
            "neck_and_lymphatics"
          ]
        },
        "respiratory_system": {
          "title": "Respiratory System",
          "description": "respiratory_system",
          "type": "object",
          "properties": {
            "inspection": {
              "title": "Inspection",
              "description": "inspection",
              "type": "object",
              "properties": {
                "accessory_muscles": {
                  "title": "Accessory Muscles",
                  "type": "string",
                  "description": "آیا از عضلات کمکی تنفس استفاده می‌کند؟"
                },
                "chest_shape_and_symmetry": {
                  "title": "Chest Shape And Symmetry",
                  "type": "string",
                  "description": "آیا شکل قفسه سینه طبیعی است (بدون Barrel Chest یا کیفواسکولیوز) و حرکت قفسه سینه در دم و بازدم متقارن است؟"
                }
              },
              "required": [
                "accessory_muscles",
                "chest_shape_and_symmetry"
              ]
            },
            "palpation": {
              "title": "Palpation",
              "description": "palpation",
              "type": "object",
              "properties": {
                "chest_expansion": {
                  "title": "Chest Expansion",
                  "type": "string",
                  "description": "آیا توسعه قفسه سینه در هنگام دم عمیق، متقارن و کامل است؟"
                },
                "tactile_fremitus": {
                  "title": "Tactile Fremitus",
                  "type": "string",
                  "description": "آیا لرزش‌های صوتی (Tactile Fremitus) در دو طرف قفسه سینه متقارن و طبیعی هستند؟ اسم علمی نوع لرزش ها رو به فارسی ترجمه نکن."
                }
              },
              "required": [
                "chest_expansion",
                "tactile_fremitus"
              ]
            },
            "percussion": {
              "title": "Percussion",
              "type": "string",
              "description": "در بیماری‌های ریوی بسته به نوع درگیری، الگوی صدای پرکاشن متفاوت است: در انسداد مزمن یا افزایش حجم هوا، صدا معمولاً hyperresonant است؛ در تراکم یا فیبروز، صدا dull می‌شود؛ و در حالت طبیعی صدای رزونانس معمول دارد. پاسخ باید بر اساس فیزیولوژی بیماری انتخاب شود، نه همیشه طبیعی. در پاسخ نام صدا ها رو به فارسی ترجمه نکن."
            },
            "auscultation": {
              "title": "Auscultation",
              "description": "auscultation",
              "type": "object",
              "properties": {
                "breath_sounds_intensity": {
                  "title": "Breath Sounds Intensity",
                  "type": "string",
                  "description": "آیا شدت صداهای تنفسی پایه طبیعی است یا کاهش یا عدم وجود صدا وجود دارد؟"
                },
                "adventitious_sounds": {
                  "title": "Adventitious Sounds",
                  "type": "string",
                  "description": "آیا صداهای اضافی (Adventitious Sounds) مانند کراکل (Crackles)، ویزینگ (Wheezing)، رونکای (Rhonchi) یا اصطکاک پلورال (Pleural Rub) شنیده می‌شوند؟"
                }
              },
              "required": [
                "breath_sounds_intensity",
                "adventitious_sounds"
              ]
            }
          },
          "required": [
            "inspection",
            "palpation",
            "percussion",
            "auscultation"
          ]
        },
        "cardiovascular_system": {
          "title": "Cardiovascular System",
          "description": "cardiovascular_system",
          "type": "object",
          "properties": {
            "JVP_assessment": {
              "title": "Jvp Assessment",
              "type": "string",
              "description": "آیا فشار وریدی ژوگولار (JVP) در وضعیت نیمه نشسته، بالا و غیرطبیعی است؟"
            },
            "palpation": {
              "title": "Palpation",
              "description": "palpation",
              "type": "object",
              "properties": {
                "precordial_palpation_heave_thrill": {
                  "title": "Precordial Palpation Heave Thrill",
                  "type": "string",
                  "description": "آیا در لمس ناحیه پره‌کوردیوم، لیفت (Lift)، هیو (Heave)، یا تریل (Thrill) احساس می‌شود؟"
                },
                "pmi_assessment": {
                  "title": "Pmi Assessment",
                  "type": "string",
                  "description": "ضربان نوک قلب (PMI) در کجا لمس می‌شود (محل دقیق) و آیا اندازه و قدرت آن طبیعی است؟"
                }
              },
              "required": [
                "precordial_palpation_heave_thrill",
                "pmi_assessment"
              ]
            },
            "auscultation": {
              "title": "Auscultation",
              "description": "auscultation",
              "type": "object",
              "properties": {
                "heart_sounds_s1_s2": {
                  "title": "Heart Sounds S1 S2",
                  "type": "string",
                  "description": "آیا صداهای اصلی قلب (S1 و S2) شنیده می‌شوند و از نظر شدت، اسپلیت و کیفیت، طبیعی هستند؟"
                },
                "extra_sounds_s3_s4_murmurs": {
                  "title": "Extra Sounds S3 S4 Murmurs",
                  "type": "string",
                  "description": "آیا صداهای اضافی مانند S3، S4، مارمار (Murmur) یا صدای اصطکاک پریکاردیال شنیده می‌شود؟"
                }
              },
              "required": [
                "heart_sounds_s1_s2",
                "extra_sounds_s3_s4_murmurs"
              ]
            },
            "peripheral_pulses_and_extremities": {
              "title": "Peripheral Pulses And Extremities",
              "description": "peripheral_pulses_and_extremities",
              "type": "object",
              "properties": {
                "peripheral_pulses_symmetry_and_quality": {
                  "title": "Peripheral Pulses Symmetry And Quality",
                  "type": "string",
                  "description": "آیا تمام نبض‌های محیطی (مانند رادیال، فمورال، دورسالیس پدیس) در دو طرف بدن متقارن، منظم، و با کیفیت (قدرت) طبیعی لمس می‌شوند؟"
                },
                "extremities_color_and_trophic_changes": {
                  "title": "Extremities Color And Trophic Changes",
                  "type": "string",
                  "description": "آیا در اندام‌های انتهایی، شواهدی از سیانوز (کبودی)، رنگ‌پریدگی، ریزش مو اندام، \tکلابینگ (Clubbing)، یا تغییرات تروفیک (مانند ریزش مو، نازکی پوست) مشاهده می‌شود؟"
                },
                "extremities_temperature_and_cap_refill": {
                  "title": "Extremities Temperature And Cap Refill",
                  "type": "string",
                  "description": "آیا اندام‌های انتهایی دمای طبیعی دارند و زمان پر شدن مجدد مویرگی (Capillary Refill Time) \tچند ثانیه است؟"
                },
                "extremities_edema": {
                  "title": "Extremities Edema",
                  "type": "string",
                  "description": "آیا در اندام‌های تحتانی، شواهدی از ادم (تورم) و به ویژه ادم گوده‌گذار (Pitting Edema) وجود \tدارد؟ اگر بله چند + است؟"
                }
              },
              "required": [
                "peripheral_pulses_symmetry_and_quality",
                "extremities_color_and_trophic_changes",
                "extremities_temperature_and_cap_refill",
                "extremities_edema"
              ]
            }
          },
          "required": [
            "JVP_assessment",
            "palpation",
            "auscultation",
            "peripheral_pulses_and_extremities"
          ]
        },
        "abdominal_system": {
          "title": "Abdominal System",
          "description": "abdominal_system",
          "type": "object",
          "properties": {
            "inspection": {
              "title": "Inspection",
              "type": "string",
              "description": "آیا شکم از نظر شکل (Flat, Rounded, Protuberant)، تقارن و وجود زخم/اسکار جراحی غیرطبیعی است؟"
            },
            "auscultation": {
              "title": "Auscultation",
              "description": "auscultation",
              "type": "object",
              "properties": {
                "bowel_sounds": {
                  "title": "Bowel Sounds",
                  "type": "string",
                  "description": "آیا صداهای روده (Bowel Sounds) در سمع حضور دارند و فرکانس و شدت آن‌ها طبیعی است (Normoactive)؟ (یا Hyperactive/Hypoactive)"
                },
                "vascular_bruits": {
                  "title": "Vascular Bruits",
                  "type": "string",
                  "description": "آیا در سمع آئورت یا شریان‌های کلیوی، صدای وزوز (Bruit) شنیده می‌شود؟"
                }
              },
              "required": [
                "bowel_sounds",
                "vascular_bruits"
              ]
            },
            "percussion": {
              "title": "Percussion",
              "description": "percussion",
              "type": "object",
              "properties": {
                "general": {
                  "title": "General",
                  "type": "string",
                  "description": " یا dulness وجود داردآیا صدای غالب دق، تیمپانی (Tympany) است؟"
                },
                "organ_borders": {
                  "title": "Organ Borders",
                  "type": "string",
                  "description": "آیا حدود کبد یا طحال در دق، غیرعادی است؟"
                }
              },
              "required": [
                "general",
                "organ_borders"
              ]
            },
            "palpation": {
              "title": "Palpation",
              "description": "palpation",
              "type": "object",
              "properties": {
                "superficial_tenderness": {
                  "title": "Superficial Tenderness",
                  "type": "string",
                  "description": "آیا در لمس سطحی، حساسیت به لمس (Tenderness) موضعی یا عمومی وجود دارد؟"
                },
                "deep_masses_and_organs": {
                  "title": "Deep Masses And Organs",
                  "type": "string",
                  "description": "آیا در لمس عمقی، توده (Mass) غیرعادی، بزرگی کبد (Hepatomegaly) یا طحال (Splenomegaly) احساس می‌شود؟"
                }
              },
              "required": [
                "superficial_tenderness",
                "deep_masses_and_organs"
              ]
            },
            "peritoneal_signs": {
              "title": "Peritoneal Signs",
              "type": "string",
              "description": "آیا علائم پریتونیت (مانند ریفاند تندرنس - Rebound Tenderness، یا سفتی غیرارادی عضلات - Guarding) وجود دارد؟"
            }
          },
          "required": [
            "inspection",
            "auscultation",
            "percussion",
            "palpation",
            "peritoneal_signs"
          ]
        },
        "neurological": {
          "title": "Neurological",
          "description": "neurological",
          "type": "object",
          "properties": {
            "mental_status_and_LOC": {
              "title": "Mental Status And Loc",
              "type": "string",
              "description": "آیا سطح هوشیاری بیمار طبیعی است و از نظر زمان، مکان و شخص جهت‌یابی (Orientation) دارد؟"
            },
            "cranial_nerves": {
              "title": "Cranial Nerves",
              "type": "string",
              "description": "آیا عملکرد اعصاب کرانیال اصلی (مانند تقارن حرکات صورت، حرکات چشم و بلع) طبیعی است؟"
            },
            "motor_strength_and_tone": {
              "title": "Motor Strength And Tone",
              "type": "string",
              "description": "قدرت عضلانی در اندام‌های فوقانی و تحتانی چقدر است(با استفاده از مقیاس 0 تا 5)؟ و آیا تون عضلانی (سفتی/شلی) طبیعی است؟"
            },
            "involuntary_movements": {
              "title": "Involuntary Movements",
              "type": "string",
              "description": "آیا حرکات غیرارادی (مانند ترمور، تیک) یا آتروفی (Atrophy) عضلانی مشاهده می‌شود؟"
            },
            "sensory_light_touch_and_pain": {
              "title": "Sensory Light Touch And Pain",
              "type": "string",
              "description": "آیا حس‌های لمس سبک و درد/دما در اندام‌ها، متقارن و بدون نقص هستند؟"
            },
            "deep_tendon_reflexes": {
              "title": "Deep Tendon Reflexes",
              "type": "string",
              "description": "آیا رفلکس‌های عمیق تاندونی (DTRs) در تمام اندام‌ها وجود دارند، متقارن هستند و شدت آن‌ها طبیعی است؟ (0 تا 4+)"
            },
            "coordination_and_gait": {
              "title": "Coordination And Gait",
              "type": "string",
              "description": "آیا تست‌های هماهنگی (مانند انگشت به بینی) نرمال هستند؟ و آیا الگوی راه رفتن (Gait) و تعادل بیمار طبیعی است و در غیر این صورت الگوی Gait \tبیمار چگونه است؟"
            }
          },
          "required": [
            "mental_status_and_LOC",
            "cranial_nerves",
            "motor_strength_and_tone",
            "involuntary_movements",
            "sensory_light_touch_and_pain",
            "deep_tendon_reflexes",
            "coordination_and_gait"
          ]
        },
        "musculoskeletal_system": {
          "title": "Musculoskeletal System",
          "description": "musculoskeletal_system",
          "type": "object",
          "properties": {
            "inspection": {
              "title": "Inspection",
              "description": "inspection",
              "type": "object",
              "properties": {
                "joints": {
                  "title": "Joints",
                  "type": "string",
                  "description": "آیا مفاصل از نظر تورم، قرمزی، بدشکلی (Deformity) یا آتروفی، ظاهر طبیعی دارند؟"
                },
                "muscles": {
                  "title": "Muscles",
                  "type": "string",
                  "description": "آیا عضلات از نظر تورم، قرمزی، بدشکلی (Deformity) یا آتروفی، ظاهر طبیعی دارند؟"
                }
              },
              "required": [
                "joints",
                "muscles"
              ]
            },
            "palpation": {
              "title": "Palpation",
              "description": "palpation",
              "type": "object",
              "properties": {
                "tenderness_and_crepitus": {
                  "title": "Tenderness And Crepitus",
                  "type": "string",
                  "description": "آیا در لمس مفاصل و عضلات، حساسیت به لمس (Tenderness)، گرما، یا صدای ساییده شدن (Crepitus) احساس می‌شود؟"
                }
              },
              "required": [
                "tenderness_and_crepitus"
              ]
            },
            "range_of_motion_active_passive": {
              "title": "Range Of Motion Active Passive",
              "type": "string",
              "description": "آیا دامنه حرکتی (ROM) فعال و غیرفعال مفاصل اصلی (مانند شانه، زانو و هیپ) کامل و بدون درد است؟"
            },
            "stability_and_function": {
              "title": "Stability And Function",
              "type": "string",
              "description": "آیا مفاصل از نظر پایداری (Stability) طبیعی هستند و بیمار می‌تواند عملکرد حرکتی خود را به خوبی انجام دهد؟"
            }
          },
          "required": [
            "inspection",
            "palpation",
            "range_of_motion_active_passive",
            "stability_and_function"
          ]
        }
      },
      "required": [
        "general_appearance",
        "head_and_neck",
        "respiratory_system",
        "cardiovascular_system",
        "abdominal_system",
        "neurological",
        "musculoskeletal_system"
      ]
    },
    "paraclinic": {
      "title": "Paraclinic",
      "description": "paraclinic",
      "type": "object",
      "properties": {
        "basic_blood_tests": {
          "title": "Basic Blood Tests",
          "description": "عدد نتایج نمایش داده شود و تفسیری وجود نداشته باشد.",
          "type": "object",
          "properties": {
            "CBC": {
              "title": "Cbc",
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Hb, WBC, Plt"
            },
            "ESR_CRP": {
              "title": "Esr Crp",
              "type": "string",
              "description": "نتایج تست بر اساس بیماری {disease} داده شود."
            },
            "BMP": {
              "title": "Bmp",
              "type": "string",
              "description": "نتایج تست na, k, ca, bun, cr بر اساس بیماری {disease} داده شود."
            },
            "LFTs": {
              "title": "Lfts",
              "type": "string",
              "description": "نتایج تست alt, ast, alp, bilirubin, inr بر اساس بیماری {disease} داده شود."
            },
            "VBG": {
              "title": "Vbg",
              "type": "string",
              "description": "نتایج تست PH, HCO3, PaCO2 بر اساس بیماری {disease} داده شود."
            }
          },
          "required": [
            "CBC",
            "ESR_CRP",
            "BMP",
            "LFTs",
            "VBG"
          ]
        },
        "specialized_lung_tests": {
          "title": "Specialized Lung Tests",
          "description": "عدد نتایج نمایش داده شود و تفسیری وجود نداشته باشد.",
          "type": "object",
          "properties": {
            "Sputum_analysis": {
              "title": "Sputum Analysis",
              "type": "string",
              "description": "Comprehensive sputum analysis findings including: 1) Macroscopic appearance (color, consistency), 2) Microscopic/Gram stain (WBC count, Epithelial cells, bacteria type), 3) Culture results (specific organism or normal flora), and 4) AFB/TB smear status if reported."
            },
            "Sputum_AFB": {
              "title": "Sputum Afb",
              "type": "string",
              "description": "نتایج تست بر اساس بیماری {disease} و به صورت عددی نمایش داده شود و تفسیری وجود نداشته باشد."
            },
            "a1_antitrypsin_level": {
              "title": "A1 Antitrypsin Level",
              "type": "string",
              "description": "نتایج تست بر اساس بیماری {disease} و به صورت عددی نمایش داده شود و تفسیری وجود نداشته باشد."
            },
            "D_dimer": {
              "title": "D Dimer",
              "type": "string",
              "description": "نتایج تست بر اساس بیماری {disease} و به صورت عددی نمایش داده شود و تفسیری وجود نداشته باشد."
            },
            "BNP_NT_proBNP": {
              "title": "Bnp Nt Pro Bnp",
              "type": "string",
              "description": "D-dimer test result. Extract the quantitative value (e.g., 500, 0.5) AND the unit (e.g., ng/mL, mg/L, ug/mL FEU)."
            }
          },
          "required": [
            "Sputum_analysis",
            "Sputum_AFB",
            "a1_antitrypsin_level",
            "D_dimer",
            "BNP_NT_proBNP"
          ]
        },
        "immunity_and_serology": {
          "title": "Immunity And Serology",
          "description": "immunity_and_serology",
          "type": "object",
          "properties": {
            "HIV_test": {
              "title": "Hiv Test",
              "type": "string",
              "description": "نتایج تست بر اساس بیماری {disease} داده شود."
            },
            "Autoimmune_pannel_ANA_ANCA": {
              "title": "Autoimmune Pannel Ana Anca",
              "type": "string",
              "description": "Extract the complete Autoimmune Panel results. For the ANA test, extract three vital components: the qualitative result (Positive/Negative), the precise Titer (e.g., 1:160, 1:320), and the Immunofluorescence Pattern (e.g., Homogeneous, Speckled). For the ANCA test, ensure to report the status of c-ANCA and p-ANCA, along with the values of specific antibodies, Anti-MPO and Anti-PR3."
            }
          },
          "required": [
            "HIV_test",
            "Autoimmune_pannel_ANA_ANCA"
          ]
        },
        "functional_tests": {
          "title": "Functional Tests",
          "description": "عدد نتایج نمایش داده شود و تفسیری وجود نداشته باشد.",
          "type": "object",
          "properties": {
            "Spirometry": {
              "title": "Spirometry",
              "type": "object",
              "fev1": {
                "title": "FEV1",
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "Measured_Value, Predicted, % Predicted"
              },
              "fvc": {
                "title": "FVC",
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "Measured_Value, Predicted, % Predicted"
              },
              "fev1/fvc": {
                "title": "FEV1/FVC",
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "Measured_Value, Predicted, % Predicted"
              },
            },
            "dlco": {
              "title": "DLCO",
              "type": "object",
              "dlco": {
                "title": "DLCO",
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "Measured_Value, % Predicted"
              },
              "dlco/va_ratio": {
                "title": "DLCO/VA_Ratio",
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "Measured_Value, % Predicted"
              }
            },
            "plethysmography": {
              "title": "Plethysmography",
              "type": "object",
              "tls": {
                "title": "TLC",
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "Measured_Value, % Predicted"
              },
              "rv": {
                "title": "RV",
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "Measured_Value, % Predicted"
              },
              "frc": {
                "title": "FRC",
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "Measured_Value, % Predicted"
              },
              "rv/tlc_ratio": {
                "title": "RV/TLC Ratio",
                "type": "string",
                "description": "extract the RV/TLC Ratio."
              }
            }
          },
          "required": [
            "Spirometry",
            "peak_flow",
            "plethysmography"
          ]
        },
        "procedures": {
          "title": "Procedures",
          "description": "procedures",
          "type": "object",
          "properties": {
            "Bronchoscopy": {
              "title": "Bronchoscopy",
              "type": "string",
              "description": "Extract the complete Bronchoscopy Report. Separate findings into three essential components: 1) **Visual/Endoscopic Findings** (location and detailed description of any mass, stricture, inflammation, or bleeding observed); 2) **Procedural Details** (which samples were taken: BAL, Biopsy, Brushings, TBNA, etc.); and 3) **Specimen Results** (the final pathology/histology diagnosis, cytology results, and culture/infection status from all retrieved samples)."
            },
            "torachocenthesis": {
              "title": "Torachocenthesis",
              "type": "object",
              "properties": {
                "pleural_fluid": {
                  "title": "Pleural Fluid",
                  "type": "array",
                  "items": {
                    "type": "string"
                  },
                  "description": "LDH, Protein, Albumin, Glucose"
                },
                "serum": {
                  "title": "Serum",
                  "type": "array",
                  "items": {
                    "type": "string"
                  },
                  "description": "LDH, Protein, Albumin"
                }
              },
            },
          },
          "required": [
            "Bronchoscopy",
            "torachonthesis"
          ]
        }
      },
      "required": [
        "basic_blood_tests",
        "specialized_lung_tests",
        "immunity_and_serology",
        "simple_imaging",
        "advanced_imaging",
        "functional_tests",
        "procedures"
      ]
    }
  },
  "required": [
    "patient_profile",
    "history_taking",
    "physical_exam",
    "paraclinic"
  ]
}

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
  target_disease = random.choice(OPTIMAL_SCENARIO)
  
  prompt_template = PromptTemplate(
    template="مطابق json زیر با در نظر گرفتن اینکه این موارد در رابطه با بیماری {disease} می‌باشند جوری کامل کن که یک پزشک بتواند با استفاده از این یافته‌ها به تشخیص برسد. به فارسی روان پاسخ یده اما اصطلاخات علمی را ترجمه نکن و به صورت انگلیسی در متن فارسی قرار بده.",
    input_variables=["disease"]
  )
  
  final_prompt = prompt_template.format(disease=target_disease)

  structured_chat_model = model.with_structured_output(json_schema)
  output = structured_chat_model.invoke(final_prompt)
  
  return output

