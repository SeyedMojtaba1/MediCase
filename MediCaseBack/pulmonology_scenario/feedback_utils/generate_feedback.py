import json
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from .asthma import *
from .pte import *
from .ph import *
from .copd import *
from .ipf import *
from .pneumenia import *

from .feedback import ClinicalEvaluator

SCENARIO_MAP = {
    "Asthma": {
        "exercise_induced": ASTHMA_EXERCISE_INDUCED,
        "mild_allergic": ASTHMA_MILD_ALLERGIC,
        "severe_uncontrolled": ASTHMA_SEVERE_UNCONTROLLED
    },
    "PTE": {
        "massive_pte": PTE_MASSIVE_PTE,
        "peripheral_infarct": PTE_PERIPHERAL_INFARCT,
        "submassive_pte": PTE_SUBMASSIVE_PTE
    },
    "PH": {
        "idiopathic_pah": PH_IDIOPATHIC_PAH,
        "ph_left_heart": PH_LEFT_HEART,
        "ph_lung_disease": PH_LUNG_DISEASE
    },
    "COPD": {
        "chronic_bronchitis": COPD_CHRONIC_BRONCHITIS,
        "copd_cor_pulmonale": COPD_COR_PULMONALE,
        "emphysema": COPD_EMPHYSEMA
    },
    "IPF": {
        "acute_ipf_exacerbation": IPF_ACUTE_IPF_EXACERBATION,
        "rheumatoid_ild": IPF_RHEUMATOID_ILD,
        "stable_ipf": IPF_STABLE_IPF
    },
    "Pneumonia": {
        "atypical_walking": PNEUMENIA_ATYPICAL_WALKING,
        "complicated_effusion": PNEUMENIA_COMPLICATED_EFFUSION,
        "typical_lobar": PNEUMENIA_TYPICAL_LOBAR
    }
}

PH_IDIOPATHIC_PAH_DETAILED = {
  "history_taking": {
    "present_illness": {
      "question1": {
        "question": "علائم از چه زمانی شروع شده و در این مدت چه تغییراتی داشته است؟",
        "analysis": "بررسی سیر پیشرونده تنگی نفس در PAH حیاتی است. این بیماری معمولاً موذی و تدریجی شروع می‌شود و تشخیص آن اغلب با تاخیر صورت می‌گیرد."
      },
      "question2": {
        "question": "آیا شروع بیماری ناگهانی بود یا تدریجی، و آیا بعد از یک اتفاق خاص مانند عفونت یا ... شروع شد؟",
        "analysis": "شروع ناگهانی بیشتر به نفع آمبولی حاد ریه (PE) است تا PAH. در ایدیوپاتیک PAH، شروع علائم معمولاً تدریجی و بدون یک ماشه (Trigger) مشخص است."
      },
      "question3": {
        "question": "آیا تنگی نفس شما مداوم است یا موقتی است و آیا با فعالیت یا در حالت استراحت بدتر می‌شود؟",
        "analysis": "تنگی نفس کوششی (Dyspnea on Exertion) شایع‌ترین شکایت اولیه است. تعیین کلاس عملکردی (WHO-FC) بر اساس میزان فعالیت برای تعیین پروگنوز و درمان ضروری است."
      },
      "question4": {
        "question": "آیا سرفه دارید؟ اگر بله، آیا خشک است یا خلط‌ دار، و رنگ و مقدار خلط چقدر است؟",
        "analysis": "در PAH خالص (گروه ۱)، سرفه علامت شایعی نیست. وجود سرفه مداوم یا خلط‌دار باید ذهن شما را به سمت بیماری‌های پارانشیم ریه (گروه ۳) یا عفونت‌ها منحرف کند."
      },
      "question5": {
        "question": "آیا خس خس سینه یا تنفس پر سر و صدا دارید؟",
        "analysis": "خس‌خس (Wheezing) نشانه درگیری راه‌های هوایی (مثل آسم یا COPD) است. اگر بیمار خس‌خس دارد، تشخیص PAH ایدیوپاتیک دورتر می‌شود."
      },
      "question6": {
        "question": "آیا درد یا گرفتگی قفسه سینه دارید؟ آیا با تنفس یا حرکت تغییر می‌کند؟",
        "analysis": "درد قفسه سینه کوششی در PAH نشانه ایسکمی بطن راست (آنژین RV) است که به دلیل فشار بالای دیواره و کاهش خونرسانی کرونر رخ می‌دهد. علامت مهمی است."
      },
      "question7": {
        "question": "آیا اخیراً تب، لرز یا تعریق شبانه داشته‌اید؟",
        "analysis": "تب و لرز نشانگر عفونت یا بدخیمی است. PAH ایدیوپاتیک به خودی خود تب‌زا نیست. این سوال برای رد علل عفونی (مثل پنومونی) پرسیده می‌شود."
      },
      "question8": {
        "question": "آیا دچار تورم در پاها، تپش قلب یا سرگیجه شده‌اید؟",
        "analysis": "سنکوپ یا سرگیجه هنگام فعالیت یک پرچم قرمز (Red Flag) خطرناک در PAH است و نشان‌دهنده ناتوانی قلب در افزایش برون‌ده است. ادم پا هم نشانه نارسایی قلب راست است."
      },
      "question9": {
        "question": "آیا قبلاً هم مشکل مشابهی داشته‌اید و چه درمانی به شما کمک کرده است؟",
        "analysis": "دانستن سابقه حملات قبلی به افتراق بین یک مشکل حاد (مثل آمبولی مکرر) و یک مشکل مزمن پیشرونده کمک می‌کند."
      },
      "question10": {
        "question": "آیا دچار کاهش وزن، خستگی یا از دست دادن اشتها شده‌اید؟",
        "analysis": "خستگی (Fatigue) در PAH بسیار شایع است اما غیراختصاصی. کاهش وزن شدید می‌تواند نشانه بدخیمی یا نارسایی قلبی پیشرفته (کاکسکی قلبی) باشد."
      }
    },
    "past_medical_history": {
      "question1": {
        "question1a": {
          "question": "آیا بیماری طولانی مدت (مزمن) مثل قند (دیابت)، فشار خون، آسم، مشکل تیروئید، یا بیماری جدی کلیوی/کبدی دارید؟",
          "analysis": "برای تشخیص ایدیوپاتیک (IPAH)، باید تمام علل ثانویه را رد کنید. بیماری کبد (Portopulmonary) و تیروئید از علل شناخته شده هستند."
        },
        "question1b": {
          "question": "اگر بله، تشخیص این بیماری از چه موقع بوده است؟",
          "analysis": "طول مدت بیماری‌های زمینه‌ای به ما کمک می‌کند تا بفهمیم آیا PAH عارضه آن‌هاست یا خیر."
        }
      },
      "question2": {
        "question2a": {
          "question": "آیا تا به حال عمل جراحی (بزرگ یا کوچک) داشته‌اید؟ و آیا تا به حال در بیمارستان بستری شده‌اید؟",
          "analysis": "سابقه جراحی‌ها (مثل اسپلنکتومی که ریسک ترومبوز را بالا می‌برد) یا شنت‌های قلبی در کودکی برای تشخیص افتراقی مهم است."
        },
        "question2b": {
          "question": "اگر بله، دلیلش چه بوده و در چه سالی؟ همچنین، آیا تا به حال انتقال خون داشته‌اید؟",
          "analysis": "سابقه انتقال خون ممکن است ریسک عفونت‌های خونی (مثل HIV یا هپاتیت) را که خودشان علت PAH هستند، مطرح کند، اما به عنوان سوال روتین اولویت کمتری دارد."
        }
      },
      "question3": {
        "question": "آیا سابقه بیماری های قلبی، ریوی و مغزی را دارید؟",
        "analysis": "حیاتی است! بیماری‌های قلب چپ (گروه ۲) و بیماری‌های ریوی (گروه ۳) شایع‌ترین علل فشار خون ریوی هستند و باید قبل از تشخیص IPAH رد شوند."
      },
      "question4": {
        "question": "آیا در حال حاظر یا در گذشته سرطان فعال داشته‌اید؟",
        "analysis": "سرطان‌ها می‌توانند باعث آمبولی‌های مکرر (CTEPH) یا فشار روی عروق ریوی شوند که تقلیدکننده PAH است."
      },
      "question5": {
        "question": "در دوران کودکی، آیا بیماری‌های خاصی (مثل تب روماتیسمی، سرخک شدید) گرفتید یا به دلیل بیماری بستری شدید؟",
        "analysis": "معمولاً بیماری‌های کودکی (به جز بیماری‌های مادرزادی قلب) ارتباط مستقیمی با ایجاد IPAH در بزرگسالی ندارند."
      },
      "question6": {
        "question": "برنامه واکسن‌ها (مثل کزاز و آنفولانزا) شما کامل و به روز است؟",
        "analysis": "اگرچه برای سلامت عمومی مهم است، اما وضعیت واکسیناسیون به طور مستقیم در تشخیص افتراقی یا تایید PAH نقشی ندارد."
      }
    },
    "drug_history": {
      "question1": {
        "question1a": {
          "question": "لطفاً لیست تمام داروهایی که در حال حاضر به صورت مرتب (روزانه، هفتگی یا ماهانه) مصرف می‌کنید را به من بگویید.",
          "analysis": "برخی داروها مستقیماً باعث PAH می‌شوند (مثل داروهای ضد اشتها، مت‌آمفتامین). بررسی دقیق دارویی الزامی است."
        },
        "question1b": {
          "question": "دوز هر دارو چقدر است و چند بار در روز مصرف می‌کنید؟",
          "analysis": "دوز دارو برای بررسی شدت مواجهه با توکسین‌های احتمالی اهمیت دارد."
        },
        "question1c": {
          "question": "آیا در چند روز گذشته، دوز یا زمان مصرف هیچ‌کدام از این داروها را تغییر داده‌اید؟",
          "analysis": "تغییرات اخیر دارویی ممکن است تشدید علائم را توجیه کند (مثلاً قطع دیورتیک‌ها)، اما علت اصلی بیماری نیست."
        }
      },
      "question2": {
        "question": "به صورت منظم داروهای بدون نسخه (OTC) (مثل داروهای سرماخوردگی، مسکن‌ها، آنتی‌اسیدها)، مکمل‌های غذایی، داروهای گیاهی یا خواب آور مصرف می‌کنید؟",
        "analysis": "برخی داروهای گیاهی و مکمل‌های کاهش وزن غیرمجاز حاوی موادی هستند که محرک ایجاد PAH می‌باشند."
      }
    },
    "allergies": {
      "question1": {
        "question1a": {
          "question": "آیا به دارو، غذا، یا ماده خاصی آلرژی (حساسیت) دارید؟",
          "analysis": "برای ایمنی تجویز داروهای بعدی مهم است، اما نقش تشخیصی در علت‌شناسی PAH ندارد."
        },
        "question1b": {
          "question": "اگر بله، دقیقاً چه دارو یا ماده‌ای است؟ و واکنش شما (مثل کهیر یا تنگی نفس) چگونه بوده است؟",
          "analysis": "اطلاعات ایمنی برای مدیریت بیمار."
        }
      }
    },
    "family_history": {
      "question1": {
        "question1a": {
          "question": "آیا در خانواده درجه یک (پدر، مادر، خواهر یا برادر) شما، سابقه ابتلا به بیماری‌های مزمن و شایع زیر وجود دارد؟",
          "analysis": "سابقه خانوادگی PAH (فرم Heritable) بسیار مهم است. جهش‌هایی مثل BMPR2 موروثی هستند."
        },
        "question1b": {
          "question": "اگر بله، چه کسی و در چه سنی به آن مبتلا شده است؟",
          "analysis": "الگوی وراثت و سن شروع در اعضای خانواده به تشخیص فرم‌های ژنتیک کمک می‌کند."
        }
      },
      "question2": {
        "question": "آیا در خانواده درجه یک شما، سابقه حمله قلبی (سکته قلبی)، سکته مغزی، یا نارسایی قلبی وجود دارد؟",
        "analysis": "این سوال بیشتر برای بیماری‌های شایع قلبی (ایسکمیک) است و ارتباط اختصاصی کمی با PAH ایدیوپاتیک دارد."
      },
      "question3": {
        "question3a": {
          "question": "آیا سابقه سرطان خاصی در خانواده درجه یک شما وجود دارد؟",
          "analysis": "سابقه سرطان فامیلیال معمولاً در ورک‌آپ PAH جایگاه روتین ندارد."
        },
        "question3b": {
          "question": "اگر بله، نوع سرطان چه بوده و در چه سنی تشخیص داده شده است؟",
          "analysis": "کمک تشخیصی خاصی نمی‌کند."
        }
      }
    },
    "social_history": {
      "question1": {
        "question1a": {
          "question": "آیا تا به حال سیگار، قلیان، پیپ، یا هر نوع محصول نیکوتینی مصرف کرده‌اید؟",
          "analysis": "مصرف سیگار به شدت احتمال COPD و بیماری‌های پارانشیم ریه (گروه ۳) را مطرح می‌کند که باید از IPAH افتراق داده شوند."
        },
        "question1b": {
          "question": "اگر قبلاً مصرف می‌کردید، چه زمانی ترک کرده‌اید؟",
          "analysis": "محاسبه Pack-Year برای ارزیابی ریسک COPD ضروری است."
        }
      },
      "question2": {
        "question": "آیا الکل مصرف می‌کنید؟ اگر بله، نوع و میزان مصرف آن در هفته چقدر است؟",
        "analysis": "مصرف الکل می‌تواند منجر به سیروز کبدی و سپس پورتوپالمونری هایپرتنشن (Portopulmonary HTN) شود."
      },
      "question3": {
        "question3a": {
          "question": "آیا تا به حال مواد مخدر مصرف کرده‌اید؟",
          "analysis": "تزریق مواد مخدر (ریسک HIV و هپاتیت) و مصرف محرک‌ها (کوکائین، مت‌آمفتامین) از علل شناخته شده PAH هستند."
        },
        "question3b": {
          "question": "اگر مصرف داشته‌اید، نوع آن و آخرین باری که مصرف کرده‌اید چه زمانی بوده است؟",
          "analysis": "زمان مصرف برای ارتباط دادن آن با شروع علائم مهم است."
        }
      },
      "question4": {
        "question": "در خانه همراه چه کسانی زندگی می‌کنید؟",
        "analysis": "اطلاعات اجتماعی برای حمایت از بیمار مهم است اما ارزش تشخیصی ندارد."
      }
    },
    "ros": {
      "question1": {
        "question": "آیا اخیراً دچار تب، لرز، کاهش یا افزایش وزن ناخواسته، یا خستگی شدید و غیرمعمول شده‌اید؟",
        "analysis": "خستگی (Fatigue) یک علامت شایع اما غیراختصاصی در PAH است که ناشی از کاهش برون‌ده قلبی است."
      },
      "question2": {
        "question": "آیا سابقه راش، خارش، زخم‌های طولانی‌مدت، تغییر در رنگ یا بافت پوست/مو/ناخن، یا کبودی غیرعادی دارید؟",
        "analysis": "برای بررسی علائم اسکلرودرمی (Scleroderma) و بیماری‌های بافت همبند (CTD) که علت شایع PAH هستند، حیاتی است. به پدیده رینود و سفتی پوست دقت کنید."
      },
      "question3": {
        "question": "آیا اخیراً دچار سردرد، سرگیجه، سفتی گردن، یا بزرگ شدن غدد لنفاوی در گردن شده‌اید؟",
        "analysis": "معمولاً در PAH ایدیوپاتیک دیده نمی‌شود، مگر اینکه عفونت همزمان وجود داشته باشد."
      },
      "question4": {
        "question": "آیا دچار تاری دید، دوبینی، درد چشم، قرمزی، یا کاهش دید ناگهانی شده‌اید؟",
        "analysis": "ارتباط خاصی با PAH ندارد."
      },
      "question5": {
        "question": "آیا دچار وزوز گوش، کاهش شنوایی، خونریزی بینی، گرفتگی مزمن بینی، گلودرد مزمن، مشکل در بلع (دیسفاژی)، یا آفت و زخم‌های دهانی مکرر هستید؟",
        "analysis": "دیسفاژی می‌تواند در بیماری CREST (نوعی اسکلرودرمی) دیده شود، اما به تنهایی مارکر قوی نیست."
      },
      "question6": {
        "question": "آیا سابقه درد قفسه سینه، تپش قلب، تنگی نفس با فعالیت، تنگی نفس در حالت خوابیده (ارتوپنه)، یا تورم پاها (ادم) دارید؟",
        "analysis": "بخش کلیدی ROS در این بیماران است. درد قفسه سینه، تپش قلب و ادم اندام تحتانی همگی علائم نارسایی قلب راست و فشار بالای پولمونر هستند."
      },
      "question7": {
        "question": "آیا سابقه سرفه، خس‌خس سینه، خلط خونی (هموپتیزی)، یا تنگی نفس (به جز تنگی نفس مرتبط با فعالیت شدید) دارید؟",
        "analysis": "هموپتیزی می‌تواند در موارد شدید PAH رخ دهد (پارگی عروق برونشیال)، اما سرفه و خس‌خس معمولاً نشانگر بیماری‌های راه هوایی هستند."
      },
      "question8": {
        "question": "آیا دچار حالت تهوع، استفراغ، سوزش سر دل، درد شکم، تغییر در عادات اجابت مزاج (اسهال یا یبوست)، خونریزی از مقعد، یا زردی پوست و چشم (یرقان) هستید؟",
        "analysis": "احتقان کبد ناشی از نارسایی قلب راست می‌تواند باعث درد RUQ، سیری زودرس و تهوع شود."
      },
      "question9": {
        "question": "آیا دچار درد یا سوزش حین ادرار کردن، تکرر ادرار، خون در ادرار (هماچوری)، مشکل در کنترل ادرار، یا ترشحات غیرعادی هستید؟",
        "analysis": "در تشخیص PAH جایگاه خاصی ندارد."
      },
      "question10": {
        "question": "آیا دچار درد مفاصل، سفتی صبحگاهی، تورم مفاصل، درد یا ضعف عضلانی، یا کمردرد مزمن هستید؟",
        "analysis": "درد و تورم مفاصل می‌تواند نشانگر بیماری‌های روماتولوژیک (مثل لوپوس یا RA) باشد که PAH ثانویه ایجاد می‌کنند."
      },
      "question11": {
        "question": "آیا سابقه سردرد شدید یا جدید، تشنج، ضعف یا بی‌حسی در دست‌ها/پاها، مشکل در تعادل/هماهنگی، یا تغییر در حافظه دارید؟",
        "analysis": "ارتباط مستقیم کمی دارد."
      },
      "question12": {
        "question": "آیا اخیراً احساس افسردگی، اضطراب، تغییرات شدید خلقی، یا مشکل در خواب (بی‌خوابی/پرخوابی) داشته‌اید؟",
        "analysis": "مشکلات خواب ممکن است ناشی از آپنه خواب (OSA) باشد که علت هایپرتنشن ریوی (گروه ۳) است، اما خود اضطراب علت نیست."
      },
      "question13": {
        "question": "آیا دچار افزایش تشنگی، افزایش گرسنگی، افزایش ادرار (پلی اوری)، یا عدم تحمل گرما/سرما شده‌اید؟",
        "analysis": "بیماری تیروئید (هایپر/هایپو) با PAH مرتبط است، اما این سوالات اولویت کمتری نسبت به علائم قلبی دارند."
      },
      "question14": {
        "question": "آیا سابقه کبودی آسان، خونریزی طولانی‌مدت، بزرگ شدن غدد لنفاوی، یا کم‌خونی شدید دارید؟",
        "analysis": "در تشخیص افتراقی‌های خونی و بدخیمی‌ها کاربرد دارد، اما در IPAH تیپیک نیست."
      }
    }
  },
  "physical_exam": {
    "vital_signs": {
      "BP": {
        "question": "BP",
        "analysis": "فشار خون سیستمیک معمولاً نرمال یا پایین است. افت فشار خون نشانه کاهش برون‌ده قلبی است."
      },
      "T": {
        "question": "T",
        "analysis": "برای رد علل عفونی باید چک شود."
      },
      "PR": {
        "question": "PR",
        "analysis": "تاکیکاردی (ضربان بالا) مکانیسم جبرانی قلب برای حفظ برون‌ده قلبی در حضور حجم ضربه‌ای پایین است."
      },
      "RR": {
        "question": "RR",
        "analysis": "تاکی‌پنه (تنفس سریع) در بیماران PAH شایع است."
      },
      "SpO2": {
        "question": "SpO2",
        "analysis": "افت اکسیژن خون، به خصوص هنگام فعالیت، در PAH دیده می‌شود."
      },
      "GCS": {
        "question": "GCS",
        "analysis": "ارزیابی کلی وضعیت هوشیاری."
      }
    },
    "general_appearance": {
      "mood_and_behavior": {
        "question": "mood_and_behavior",
        "analysis": "اضطراب ناشی از تنگی نفس شایع است."
      },
      "overall_appearance": {
        "question": "overall_appearance",
        "analysis": "آیا بیمار دیسترس تنفسی دارد؟ آیا لاغر و کاکتیک است؟"
      },
      "posture_and_position": {
        "question": "posture_and_position",
        "analysis": "آیا بیمار می‌تواند صاف دراز بکشد یا ارتوپنه دارد؟ (بیشتر در بیماری‌های قلب چپ دیده می‌شود)."
      },
      "level_of_consciousness": {
        "question": "level_of_consciousness",
        "analysis": "کاهش پرفیوژن مغزی در مراحل پیشرفته می‌تواند هوشیاری را تحت تاثیر قرار دهد."
      },
      "cardiopulmonary_and_circulatory_clues": {
        "edema": {
          "question": "edema",
          "analysis": "ادم اندام تحتانی نشانه نارسایی قلب راست (Cor Pulmonale) است."
        },
        "dyspnea": {
          "question": "dyspnea",
          "analysis": "تنگی نفس در حالت استراحت نشانه کلاس عملکردی بالا (FC IV) است."
        },
        "cyanosis": {
          "question": "cyanosis",
          "analysis": "سیانوز محیطی به دلیل استخراج بالای اکسیژن بافتی و کاهش برون‌ده قلبی رخ می‌دهد."
        }
      }
    },
    "head_and_neck": {
      "head_and_face": {
        "symmetry_and_lesions": {
          "question": "symmetry_and_lesions",
          "analysis": "تلانژکتازی روی صورت می‌تواند نشانه سندرم CREST باشد."
        },
        "tenderness": {
          "question": "tenderness",
          "analysis": "کاربرد کمی دارد."
        }
      },
      "eyes": {
        "sclera_and_conjunctiva": {
          "question": "sclera_and_conjunctiva",
          "analysis": "رنگ‌پریدگی ملتحمه (آنمی) یا زردی صلبیه (مشکل کبدی) باید بررسی شود."
        },
        "pupils_reaction": {
          "question": "pupils_reaction",
          "analysis": "کاربرد کمی دارد."
        },
        "extraocular_movements": {
          "question": "extraocular_movements",
          "analysis": "کاربرد کمی دارد."
        }
      },
      "ears": {
        "external_and_tenderness": {
          "question": "external_and_tenderness",
          "analysis": "کاربرد کمی دارد."
        },
        "eardrum_appearance": {
          "question": "eardrum_appearance",
          "analysis": "کاربرد کمی دارد."
        }
      },
      "nose_and_sinuses": {
        "septum_and_discharge": {
          "question": "septum_and_discharge",
          "analysis": "کاربرد کمی دارد."
        },
        "sinus_tenderness": {
          "question": "sinus_tenderness",
          "analysis": "کاربرد کمی دارد."
        }
      },
      "mouth_and_pharynx": {
        "oral_mucosa_and_lesions": {
          "question": "oral_mucosa_and_lesions",
          "analysis": "سیانوز مرکزی در مخاط دهان قابل مشاهده است."
        },
        "pharynx_and_tonsils": {
          "question": "pharynx_and_tonsils",
          "analysis": "بزرگی لوزه‌ها می‌تواند عامل آپنه خواب و PAH ثانویه باشد."
        }
      },
      "neck_and_lymphatics": {
        "inspection": {
          "question": "inspection",
          "analysis": "اتساع وریدهای گردن (JVD) کلید تشخیص نارسایی قلب راست است."
        },
        "tracheal_position": {
          "question": "tracheal_position",
          "analysis": "انحراف تراشه در پنوموتوراکس یا توده‌های مدیاستن دیده می‌شود."
        },
        "thyroid_gland": {
          "question": "thyroid_gland",
          "analysis": "بزرگی تیروئید (گواتر) نیاز به بررسی عملکرد تیروئید دارد."
        },
        "carotid_bruit": {
          "question": "carotid_bruit",
          "analysis": "بیشتر مربوط به بیماری‌های آترواسکلروتیک است."
        },
        "lymph_nodes_size_consistency": {
          "question": "lymph_nodes_size_consistency",
          "analysis": "لنفادنوپاتی می‌تواند نشانه بدخیمی یا عفونت (مثل HIV) باشد."
        },
        "lymph_nodes_mobility_tenderness": {
          "question": "lymph_nodes_mobility_tenderness",
          "analysis": "بررسی ویژگی‌های لنف‌نودها."
        }
      }
    },
    "respiratory_system": {
      "inspection": {
        "accessory_muscles": {
          "question": "accessory_muscles",
          "analysis": "استفاده از عضلات فرعی نشانه دیسترس تنفسی است."
        },
        "chest_shape_and_symmetry": {
          "question": "chest_shape_and_symmetry",
          "analysis": "دفورمیتی قفسه سینه (مثل کیفواسکولیوز) می‌تواند علت PAH گروه ۳ باشد."
        }
      },
      "palpation": {
        "chest_expansion": {
          "question": "chest_expansion",
          "analysis": "کاهش انبساط در بیماری‌های محدودکننده ریه دیده می‌شود."
        },
        "tactile_fremitus": {
          "question": "tactile_fremitus",
          "analysis": "معمولاً در PAH نرمال است."
        }
      },
      "percussion": {
        "question": "percussion",
        "analysis": "در PAH ایدیوپاتیک معمولاً نرمال (رزونانت) است. ماتیته نشانه افیوژن یا پنومونی است."
      },
      "auscultation": {
        "breath_sounds_intensity": {
          "question": "breath_sounds_intensity",
          "analysis": "در IPAH صداهای ریوی معمولاً شفاف (Clear) هستند. وجود کراکل یا ویزینگ به نفع بیماری‌های پارانشیم یا راه هوایی است."
        },
        "adventitious_sounds": {
          "question": "adventitious_sounds",
          "analysis": "نبود صداهای اضافی (مثل رال) به تشخیص IPAH کمک می‌کند."
        }
      }
    },
    "cardiovascular_system": {
      "JVP_assessment": {
        "question": "JVP_assessment",
        "analysis": "افزایش JVP، به ویژه وجود موج a بلند (ناشی از انقباض دهلیز راست علیه فشار بالا) و موج v (در نارسایی تری‌کوسپید) بسیار تشخیصی است."
      },
      "palpation": {
        "precordial_palpation_heave_thrill": {
          "question": "precordial_palpation_heave_thrill",
          "analysis": "لمس ضربان قوی در کنار جناغ (Left Parasternal Heave) نشانه هایپرتروفی بطن راست (RVH) است."
        },
        "pmi_assessment": {
          "question": "pmi_assessment",
          "analysis": "معمولاً نرمال است، مگر اینکه بطن راست آنقدر بزرگ شود که بطن چپ را جابجا کند."
        }
      },
      "auscultation": {
        "heart_sounds_s1_s2": {
          "question": "heart_sounds_s1_s2",
          "analysis": "جزء دوم صدای دوم قلب (P2) در ناحیه ریوی بسیار بلند و کوبنده شنیده می‌شود. این نشانه کلاسیک هایپرتنشن ریوی است."
        },
        "extra_sounds_s3_s4_murmurs": {
          "question": "extra_sounds_s3_s4_murmurs",
          "analysis": "سوفل پان‌سیستولیک نارسایی تری‌کوسپید (TR) و صدای چهارم قلب (S4) راست (ناشی از RVH) یافته‌های شایعی هستند."
        }
      },
      "2_pulses_and_extremities": {
        "peripheral_pulses_symmetry_and_quality": {
          "question": "peripheral_pulses_symmetry_and_quality",
          "analysis": "نبض‌ها ممکن است ضعیف و نخی‌شکل باشند (به دلیل کاهش Stroke Volume)."
        },
        "extremities_color_and_trophic_changes": {
          "question": "extremities_color_and_trophic_changes",
          "analysis": "سردی انتهای اندام‌ها نشانه کاهش پرفیوژن است."
        },
        "extremities_temperature_and_cap_refill": {
          "question": "extremities_temperature_and_cap_refill",
          "analysis": "زمان پرشدگی مویرگی (Capillary Refill) ممکن است طولانی شود."
        },
        "extremities_edema": {
          "question": "extremities_edema",
          "analysis": "ادم گوده گذار اندام تحتانی نشانه احتباس مایع و نارسایی قلب راست است."
        }
      }
    },
    "abdominal_system": {
      "inspection": {
        "question": "inspection",
        "analysis": "اتساع شکم ممکن است ناشی از آسیت باشد."
      },
      "auscultation": {
        "bowel_sounds": {
          "question": "bowel_sounds",
          "analysis": "معمولاً نرمال است."
        },
        "vascular_bruits": {
          "question": "vascular_bruits",
          "analysis": "برای بررسی تنگی شریان کلیوی (علت فشار خون سیستمیک) کاربرد دارد."
        }
      },
      "percussion": {
        "general": {
          "question": "general",
          "analysis": "بررسی آسیت."
        },
        "organ_borders": {
          "question": "organ_borders",
          "analysis": "هپاتومگالی (بزرگی کبد) ناشی از احتقان وریدی شایع است."
        }
      },
      "palpation": {
        "superficial_tenderness": {
          "question": "superficial_tenderness",
          "analysis": "حساسیت در ربع فوقانی راست (RUQ) به دلیل کشیدگی کپسول کبد محتمل است."
        },
        "deep_masses_and_organs": {
          "question": "deep_masses_and_organs",
          "analysis": "لمس لبه کبد و ضربان‌دار بودن آن (Pulsatile Liver) در نارسایی تری‌کوسپید شدید دیده می‌شود."
        }
      },
      "peritoneal_signs": {
        "question": "peritoneal_signs",
        "analysis": "کاربرد ندارد."
      }
    },
    "neurological": {
      "mental_status_and_LOC": {
        "question": "mental_status_and_LOC",
        "analysis": "بررسی اختلال هوشیاری ناشی از هیپوکسی یا کاهش برون‌ده قلبی."
      },
      "cranial_nerves": {
        "question": "cranial_nerves",
        "analysis": "معمولاً نرمال است."
      },
      "motor_strength_and_tone": {
        "question": "motor_strength_and_tone",
        "analysis": "ضعف عمومی (Asthenia) شایع است اما یافته فوکال عصبی نادر است."
      },
      "involuntary_movements": {
        "question": "involuntary_movements",
        "analysis": "آستریکسی ممکن است در نارسایی کبدی یا هایپرکاپنیک دیده شود."
      },
      "sensory_light_touch_and_pain": {
        "question": "sensory_light_touch_and_pain",
        "analysis": "نرمال است."
      },
      "deep_tendon_reflexes": {
        "question": "deep_tendon_reflexes",
        "analysis": "نرمال است."
      },
      "coordination_and_gait": {
        "question": "coordination_and_gait",
        "analysis": "نرمال است."
      }
    },
    "musculoskeletal_system": {
      "inspection": {
        "joints": {
          "question": "joints",
          "analysis": "تورم مفاصل در بیماری‌های بافت همبند (CTD) دیده می‌شود."
        },
        "muscles": {
          "question": "muscles",
          "analysis": "تحلیل عضلات در موارد مزمن و کاکتیک."
        }
      },
      "palpation": {
        "tenderness_and_crepitus": {
          "question": "tenderness_and_crepitus",
          "analysis": "کاربرد کمی دارد."
        }
      },
      "range_of_motion_active_passive": {
        "question": "range_of_motion_active_passive",
        "analysis": "محدودیت حرکتی در اسکلرودرمی (سفتی پوست) مهم است."
      },
      "stability_and_function": {
        "question": "stability_and_function",
        "analysis": "کاربرد کمی دارد."
      }
    }
  },
  "paraclinic": {
    "basic_blood_tests": {
      "BMP": {
        "question": "BMP",
        "analysis": "چک کردن الکترولیت‌ها و عملکرد کلیه (Cr/BUN) حیاتی است. کاهش برون‌ده قلبی می‌تواند باعث نارسایی کلیوی شود و مصرف دیورتیک‌ها هم الکترولیت‌ها را به هم می‌ریزد."
      },
      "CBC": {
        "question": "CBC",
        "analysis": "برای بررسی کم‌خونی (که تنگی نفس را تشدید می‌کند) و رد کردن اختلالات میلوپرولیفراتیو ضروری است."
      },
      "ESR": {
        "question": "ESR",
        "analysis": "به عنوان مارکر التهابی برای بررسی بیماری‌های بافت همبند (CTD) مفید است."
      },
      "CRP": {
        "question": "CRP",
        "analysis": "هرچند التهاب نقش دارد، اما CRP به صورت روتین برای تشخیص یا پایش IPAH استفاده نمی‌شود."
      },
      "VBG": {
        "question": "VBG",
        "analysis": "گازهای خون وریدی اطلاعات دقیقی از وضعیت اکسیژناسیون شریانی نمی‌دهند و ABG ارجح است، لذا در بررسی اولیه IPAH جایگاه اصلی ندارد."
      },
      "LFTs": {
        "question": "LFTs",
        "analysis": "بسیار مهم است! هم برای بررسی احتقان کبد ناشی از نارسایی قلب راست و هم برای رد کردن بیماری‌های کبدی که باعث پورتوپالمونری هایپرتنشن می‌شوند."
      }
    },
    "specialized_lung_tests": {
      "D_dimer": {
        "question": "D_dimer",
        "analysis": "دایمر برای رد آمبولی حاد است. در بررسی PAH مزمن (برای رد CTEPH) دایمر کمک‌کننده نیست و باید از اسکن V/Q استفاده کرد."
      },
      "Sputum_AFB": {
        "question": "Sputum_AFB",
        "analysis": "فقط در صورت شک به سل (TB) انجام می‌شود و تست روتین PAH نیست."
      },
      "BNP_NT_proBNP": {
        "question": "BNP_NT_proBNP",
        "analysis": "این تست طلایی برای ارزیابی استرس دیواره بطن راست است. سطح آن با شدت بیماری و پروگنوز رابطه مستقیم دارد."
      },
      "Sputum_analysis": {
        "question": "Sputum_analysis",
        "analysis": "در غیاب علائم عفونی، کاربردی ندارد."
      },
      "a1_antitrypsin_level": {
        "question": "a1_antitrypsin_level",
        "analysis": "مربوط به آمفیزم (COPD) است و تست روتین برای IPAH نیست."
      }
    },
    "immunity_and_serology": {
      "HIV_test": {
        "question": "HIV_test",
        "analysis": "تست HIV برای تمام بیماران با تشخیص جدید PAH توصیه می‌شود، زیرا HIV یکی از علل مهم و قابل درمان PAH است."
      },
      "Autoimmune_pannel_ANA_ANCA": {
        "question": "Autoimmune_pannel_ANA_ANCA",
        "analysis": "ضروری است! بیماری‌های بافت همبند (مثل اسکلرودرمی) شایع‌ترین علت PAH همراه هستند و باید حتماً بررسی شوند."
      }
    },
    "simple_imaging": {
      "Chest_X_Ray": {
        "question": "Chest_X_Ray",
        "analysis": "اولین قدم تصویربرداری است. بزرگی شریان‌های ریوی مرکزی و پاک بودن محیط ریه (Pruning) یافته‌های کلاسیک IPAH هستند."
      }
    },
    "advanced_imaging": {
      "Chest_CT_CTPA": {
        "question": "Chest_CT_CTPA",
        "analysis": "High-Resolution CT برای بررسی دقیق پارانشیم ریه و رد کردن بیماری‌های ریوی (گروه ۳) و همچنین بررسی عروق ریوی ضروری است."
      }
    },
    "functional_tests": {
      "dlco": {
        "question": "dlco",
        "analysis": "تست انتشار گازها (DLCO) در PAH کاهش می‌یابد اما در بیماری‌های پارانشیم ریه هم کم می‌شود. نرمال بودن حجم‌های ریوی همراه با کاهش DLCO الگوی کلاسیک بیماری عروقی ریه است."
      },
      "peak_flow": {
        "question": "peak_flow",
        "analysis": "برای تشخیص آسم است و در PAH کاربرد ندارد."
      },
      "Spirometry": {
        "question": "Spirometry",
        "analysis": "برای رد کردن بیماری‌های انسدادی (COPD) و محدودکننده ریه که علل شایع فشار خون ریوی هستند (گروه ۳) انجام می‌شود."
      },
      "plethysmography": {
        "question": "plethysmography",
        "analysis": "برای اندازه‌گیری دقیق حجم‌های ریوی و رد کردن بیماری‌های محدودکننده (Restrictive) کاربرد دارد."
      }
    },
    "procedures": {
      "Bronchoscopy": {
        "question": "Bronchoscopy",
        "analysis": "تست روتین نیست، مگر اینکه شک به توده یا بیماری‌های مجاری هوایی وجود داشته باشد."
      },
      "torachonthesis": {
        "question": "torachonthesis",
        "analysis": "فقط اگر افیوژن پلورال قابل توجه وجود داشته باشد انجام می‌شود، که در IPAH معمولاً کم‌حجم است و نیاز به تپ ندارد."
      }
    }
  },
  "differential_diagnosis": {
    "disease1": {
      "question": "Asthma",
      "analysis": "معمولاً آسم با خس‌خس سینه (Wheezing) و حملات عودکننده همراه است، در حالی که در PAH تنگی نفس مداوم و پیشرونده داریم. اسپیرومتری نرمال یا الگوی محدودکننده خفیف در PAH، به راحتی آسم را رد می‌کند، بنابراین در لیست تشخیص‌های افتراقی دشوار قرار نمی‌گیرد."
    },
    "disease2": {
      "question": "Pneumonia",
      "analysis": "پنومونی یک فرآیند حاد عفونی با تب و سرفه خلط‌دار است، در حالی که PAH یک بیماری مزمن عروقی است. تابلوی بالینی این دو کاملاً متفاوت است و معمولاً با هم اشتباه گرفته نمی‌شوند، مگر اینکه بیمار دچار پنومونی همزمان شده باشد."
    },
    "disease3": {
      "question": "COPD",
      "analysis": "حیاتی! بیماری‌های انسدادی ریه (گروه ۳) از شایع‌ترین علل افزایش فشار ریوی هستند. چون درمان PH ناشی از COPD کاملاً متفاوت است (تمرکز بر اکسیژن و برونکودیلاتور)، باید حتماً با تست‌های عملکرد ریه (PFT) و سی‌تی‌اسکن دقیقاً بررسی و رد شود."
    },
    "disease4": {
      "question": "PTE",
      "analysis": "مهم‌ترین تشخیص افتراقی! همیشه باید نگران CTEPH (فشار خون ریوی ناشی از لخته‌های مزمن - گروه ۴) باشیم، چون این تنها نوع PH است که با جراحی قابل درمان قطعی است. هیچ‌وقت بدون انجام اسکن V/Q یا سی‌تی آنژیوگرافی دقیق، برچسب «ایدیوپاتیک» به بیمار نزنید."
    },
    "disease5": {
      "question": "IPF",
      "analysis": "فیبروز ریه (IPF) معمولاً نشانه‌های واضحی مثل صدای کراکل در سمع ریه و نمای لانه زنبوری در سی‌تی‌اسکن دارد. اگر معاینه ریه و تصویربرداری اولیه پاک باشد، این تشخیص کنار می‌رود و نیاز به ورک‌آپ پیچیده‌ای برای رد کردنش نیست."
    },
    "disease6": {
      "question": "PH",
      "analysis": "هدف نهایی ما! بعد از اینکه بیماری‌های شایع ریوی (COPD/IPF)، قلبی (نارسایی چپ) و لخته‌های مزمن (CTEPH) را رد کردیم، به تشخیص فشار خون شریان ریوی اولیه (PAH) می‌رسیم."
    }
  },
  "final_diagnosis": {
    "disease": "PH"
  }
}

DETAILED_SCENARIO_MAP = {
    "Asthma": {
        # "exercise_induced": ASTHMA_EXERCISE_INDUCED_DETAILED,
        # "mild_allergic": ASTHMA_MILD_ALLERGIC_DETAILED,
        # "severe_uncontrolled": ASTHMA_SEVERE_UNCONTROLLED_DETAILED
    },
    "PTE": {
        # "massive_pte": PTE_MASSIVE_PTE_DETAILED,
        # "peripheral_infarct": PTE_PERIPHERAL_INFARCT_DETAILED,
        # "submassive_pte": PTE_SUBMASSIVE_PTE_DETAILED
    },
    "PH": {
        "idiopathic_pah": PH_IDIOPATHIC_PAH_DETAILED,
        # "ph_left_heart": PH_LEFT_HEART_DETAILED,
        # "ph_lung_disease": PH_LUNG_DISEASE_DETAILED
    },
    "COPD": {
        # "chronic_bronchitis": COPD_CHRONIC_BRONCHITIS_DETAILED,
        # "copd_cor_pulmonale": COPD_COR_PULMONALE_DETAILED,
        # "emphysema": COPD_EMPHYSEMA_DETAILED
    },
    "IPF": {
        # "acute_ipf_exacerbation": IPF_ACUTE_IPF_EXACERBATION_DETAILED,
        # "rheumatoid_ild": IPF_RHEUMATOID_ILD_DETAILED,
        # "stable_ipf": IPF_STABLE_IPF_DETAILED
    },
    "Pneumonia": {
        # "atypical_walking": PNEUMENIA_ATYPICAL_WALKING_DETAILED,
        # "complicated_effusion": PNEUMENIA_COMPLICATED_EFFUSION_DETAILED,
        # "typical_lobar": PNEUMENIA_TYPICAL_LOBAR_DETAILED
    }
}


FULL_SCENARIO = {
  "patient_profile": {
    "personal_information": {
      "first_name": "",
      "last_name": "",
      "age": "سن بیمار باید متناسب با شیوع بیماری انتخاب شود. در بیماری‌های مزمن تنفسی و قلبی معمولاً میانسالی تا سالمندی (حدود 45 تا 80 سال)، در بیماری‌های حاد یا ارثی ممکن است سن پایین‌تر باشد. برای تنوع، سن را در بازه منطقی بیماری انتخاب کن، نه مقدار ثابت.",
      "gender": "",
      "occupation": "",
      "place_of_birth": "",
      "place_of_residence": "",
      "marital_status": ""
    },
    "chief_complaint": "contains patient's main reason of visit and its onset time",
    "vital_sign": {
      "BP": "Blood Pressure",
      "T": "Temprature",
      "PR": "Pulse Rate",
      "RR": "Respiratory Rate",
      "SpO2": "Saturation of O2",
      "GCS": "Level of Consiousness"
    }
  },
  "history_taking": {
    "present_illness": {
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
    },
    "medical_history": {
      "question1": {
        "question1a": "آیا بیماری طولانی مدت (مزمن) مثل قند (دیابت)، فشار خون، آسم، مشکل تیروئید، یا بیماری جدی کلیوی/کبدی دارید؟",
        "question1b": "اگر پاسخ question1a بله بود، تشخیص این بیماری از چه موقع بوده است؟"
      },
      "question2": {
        "question2a": "آیا تا به حال عمل جراحی (بزرگ یا کوچک) داشته‌اید؟ و آیا تا به حال در بیمارستان بستری شده‌اید؟",
        "question2b": "اگر پاسخ question2a بله بود، دلیلش چه بوده و در چه سالی؟ همچنین، آیا تا به حال انتقال خون داشته‌اید؟"
      },
      "question3": "آیا سابقه بیماری های قلبی، ریوی و مغزی را دارید؟",
      "question4": "آیا در حال حاظر یا در گذشته سرطان فعال داشته‌اید؟",
      "question5": "در دوران کودکی، آیا بیماری‌های خاصی (مثل تب روماتیسمی، سرخک شدید) گرفتید یا به دلیل بیماری بستری شدید؟",
      "question6": "برنامه واکسن‌ها (مثل کزاز و آنفولانزا) شما کامل و به روز است؟"
    },
    "drug_history": {
      "question1": {
        "question1a": "لطفاً لیست تمام داروهایی که در حال حاضر به صورت مرتب (روزانه، هفتگی یا ماهانه) مصرف می‌کنید را به من بگویید.",
        "question1b": "دوز هر دارو چقدر است و چند بار در روز مصرف می‌کنید؟",
        "question1c": "آیا در چند روز گذشته، دوز یا زمان مصرف هیچ‌کدام از این داروها را تغییر داده‌اید؟"
      },
      "question2": "به صورت منظم داروهای بدون نسخه (OTC) (مثل داروهای سرماخوردگی، مسکن‌ها، آنتی‌اسیدها)، مکمل‌های غذایی، داروهای گیاهی یا خواب آور مصرف می‌کنید؟"
    },
    "allergies": {
      "question1": {
        "question1a": "آیا به دارو، غذا، یا ماده خاصی آلرژی (حساسیت) دارید؟",
        "question1b": "اگر پاسخ question1a بله بود، دقیقاً چه دارو یا ماده‌ای است؟ و واکنش شما (مثل کهیر یا تنگی نفس) چگونه بوده است؟"
      }
    },
    "family_history": {
      "question1": {
        "question1a": "آیا در خانواده درجه یک (پدر، مادر، خواهر یا برادر) شما، سابقه ابتلا به بیماری‌های مزمن و شایع زیر وجود دارد؟",
        "question1b": "اگر پاسخ question1a بله بود، چه کسی و در چه سنی به آن مبتلا شده است؟"
      },
      "question2": "آیا در خانواده درجه یک شما، سابقه حمله قلبی (سکته قلبی)، سکته مغزی، یا نارسایی قلبی وجود دارد؟",
      "question3": {
        "question3a": "آیا سابقه سرطان خاصی در خانواده درجه یک شما وجود دارد؟",
        "question3b": "اگر پاسخ question3a بله بود، نوع سرطان چه بوده و در چه سنی تشخیص داده شده است؟"
      }
    },
    "social_history": {
      "question1": {
        "question1a": "آیا تا به حال سیگار، قلیان، پیپ، یا هر نوع محصول نیکوتینی مصرف کرده‌اید؟",
        "question1b": "اگر قبلاً مصرف می‌کردید، چه زمانی ترک کرده‌اید؟"
      },
      "question2": "آیا الکل مصرف می‌کنید؟ اگر بله، نوع و میزان مصرف آن در هفته چقدر است؟",
      "question3": {
        "question3a": "آیا تا به حال مواد مخدر مصرف کرده‌اید؟",
        "question3b": "اگر مصرف داشته‌اید، نوع آن و آخرین باری که مصرف کرده‌اید چه زمانی بوده است؟"
      },
      "question4": "در خانه همراه چه کسانی زندگی می‌کنید؟"
    },
    "ROS": {
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
    }
  },
  "physical_exam": {
    "general_appearance": {
      "level_of_consciousness_mood_and_behavior": {
        "level_of_consciousness": "آیا بیمار هوشیار، گیج، خواب‌آلود (لتارژیک)، یا در حالت اغما (Comatose) است؟ آیا دستورات ساده را اجرا می‌کند؟",
        "mood": "آیا بیمار به نظر بیمار، مضطرب، یا در درد شدید است؟",
        "behavior": "آیا بیمار همکاری می‌کند؟ آیا مضطرب، افسرده، یا پرخاشگر است؟ آیا از نظر روانی وضعیت طبیعی دارد؟"
      },
      "posture_and_position": {
        "position_of_comfort": "آیا بیمار وضعیتی را برای کاهش درد یا تنگی نفس انتخاب کرده است؟"
      },
      "overall_appearance": {
        "nutritional_status": "آیا بیمار لاغر (Cachectic)، چاق (Obese)، یا در وضعیت وزن طبیعی است؟"
      },
      "cardiopulmonary_and_circulatory_clues": {
        "cyanosis": "بررسی لب‌ها، زبان و بستر ناخن برای علائم کبودی.",
        "dyspnea": "آیا بیمار به سختی نفس می‌کشد؟",
        "edema": "وجود تورم در پاها، مچ پا یا اطراف چشم."
      }
    },
    "head_and_neck": {
      "head_and_face": {
        "symmetry_and_lesions": "آیا سر و صورت بیمار متقارن است و شواهدی از زخم، توده یا ضایعات پوستی وجود دارد؟",
        "tenderness": "آیا در لمس جمجمه حساسیت به لمس یا درد وجود دارد؟"
      },
      "eyes": {
        "sclera_and_conjunctiva": "آیا در صلبیه (سفیدی چشم) زردی (یرقان) یا در ملتحمه (پلک پایین) رنگ‌پریدگی شدید (کم‌خونی) مشاهده می‌شود؟",
        "pupils_reaction": "آیا مردمک‌ها متقارن هستند و به نور واکنش طبیعی نشان می‌دهند؟",
        "extraocular_movements": "آیا حرکات چشمی در جهات مختلف کامل و هماهنگ هستند؟"
      },
      "ears": {
        "external_and_tenderness": "آیا لاله گوش یا ناحیه ماستوئید (پشت گوش) متورم، قرمز یا دردناک هستند؟",
        "eardrum_appearance": "آیا پرده صماخ در اتوسکوپی ظاهر طبیعی دارد (شفاف، بدون التهاب یا پارگی)؟"
      },
      "nose_and_sinuses": {
        "septum_and_discharge": "آیا تیغه بینی انحراف شدید دارد و آیا ترشحات غیرعادی (چرکی یا خونی) مشاهده می‌شود؟",
        "sinus_tenderness": "آیا در لمس یا دق بر روی سینوس‌های پیشانی و فکی (فرونتال و ماگزیلاری) درد وجود دارد؟"
      },
      "mouth_and_pharynx": {
        "oral_mucosa_and_lesions": "آیا مخاط دهان (لثه‌ها، زیر زبان) مرطوب و بدون ضایعات غیرعادی (زخم یا آفت) است؟",
        "pharynx_and_tonsils": "آیا حلق (گلو) قرمز یا متورم است و آیا لوزتین‌ها (Tonsils) بزرگ شده‌اند یا دارای ترشحات چرکی هستند؟"
      },
      "neck_and_lymphatics": {
        "inspection": "آیا در معاینه ظاهری گردن، تورم، قرمزی، توده، یا زخم قابل مشاهده‌ای وجود دارد؟",
        "tracheal_position": "آیا نای (Trachea) در خط وسط قرار دارد؟ آیا در لمس، انحراف یا جابه‌جایی نای (Tracheal Deviation) احساس می‌شود؟",
        "thyroid_gland": "آیا غده تیروئید (از پشت بیمار) بزرگ است (گواتر)؟ آیا در لمس، ندول (توده)، سفتی، یا حساسیت به لمس وجود دارد؟",
        "carotid_bruit": "آیا در سمع شریان‌های کاروتید، صدای وزوز (Bruit) شنیده می‌شود؟ (نشانه‌ی احتمالی تنگی شریان)",
        "lymph_nodes_size_consistency": "آیا غدد لنفاوی در نواحی مختلف (سرویکال، ساب‌ماندیبولار، سوپراکلاویکولار) بزرگ شده‌اند؟ (اندازه، قوام: نرم/سفت/لاستیکی)",
        "lymph_nodes_mobility_tenderness": "آیا غدد لنفاوی لمس شده، متحرک هستند یا ثابت و چسبیده به بافت زیرین؟ آیا در لمس، درد (Tenderness) دارند؟"
      }
    },
    "respiratory_system": {
      "inspection": {
        "accessory_muscles": "آیا از عضلات کمکی تنفس استفاده می‌کند؟",
        "chest_shape_and_symmetry": "آیا شکل قفسه سینه طبیعی است (بدون Barrel Chest یا کیفواسکولیوز) و حرکت قفسه سینه در دم و بازدم متقارن است؟"
      },
      "palpation": {
        "chest_expansion": "آیا توسعه قفسه سینه در هنگام دم عمیق، متقارن و کامل است؟",
        "tactile_fremitus": "آیا لرزش‌های صوتی (Tactile Fremitus) در دو طرف قفسه سینه متقارن و طبیعی هستند؟"
      },
      "percussion": "آیا صدای دق در تمام نواحی ریه رزونانس (طبیعی) است یا در برخی نواحی dullness یا hyperresonanse است؟ اگر بله در چه نواحی؟",
      "auscultation": {
        "breath_sounds_intensity": "آیا شدت صداهای تنفسی پایه طبیعی است یا کاهش یا عدم وجود صدا وجود دارد؟",
        "adventitious_sounds": "آیا صداهای اضافی (Adventitious Sounds) مانند کراکل (Crackles)، ویزینگ (Wheezing)، رونکای (Rhonchi) یا اصطکاک پلورال (Pleural Rub) شنیده می‌شوند؟"
      }
    },
    "cardiovascular_system": {
      "JVP_assessment": "آیا فشار وریدی ژوگولار (JVP) در وضعیت نیمه نشسته، بالا و غیرطبیعی است؟",
      "palpation": {
        "precordial_palpation_heave_thrill": "آیا در لمس ناحیه پره‌کوردیوم، لیفت (Lift)، هیو (Heave)، یا تریل (Thrill) احساس می‌شود؟",
        "pmi_assessment": "ضربان نوک قلب (PMI) در کجا لمس می‌شود (محل دقیق) و آیا اندازه و قدرت آن طبیعی است؟"
      },
      "auscultation": {
        "heart_sounds_s1_s2": "آیا صداهای اصلی قلب (S1 و S2) شنیده می‌شوند و از نظر شدت، اسپلیت و کیفیت، طبیعی هستند؟",
        "extra_sounds_s3_s4_murmurs": "آیا صداهای اضافی مانند S3، S4، مارمار (Murmur) یا صدای اصطکاک پریکاردیال شنیده می‌شود؟"
      },
      "peripheral_pulses_and_extremities": {
        "peripheral_pulses_symmetry_and_quality": "آیا تمام نبض‌های محیطی (مانند رادیال، فمورال، دورسالیس پدیس) در دو طرف بدن متقارن، منظم، و با کیفیت (قدرت) طبیعی لمس می‌شوند؟",
        "extremities_color_and_trophic_changes": "آیا در اندام‌های انتهایی، شواهدی از سیانوز (کبودی)، رنگ‌پریدگی، ریزش مو اندام، کلابینگ (Clubbing)، یا تغییرات تروفیک (مانند ریزش مو، نازکی پوست) مشاهده می‌شود؟",
        "extremities_temperature_and_cap_refill": "آیا اندام‌های انتهایی دمای طبیعی دارند و زمان پر شدن مجدد مویرگی (Capillary Refill Time) چند ثانیه است؟",
        "extremities_edema": "آیا در اندام‌های تحتانی، شواهدی از ادم (تورم) و به ویژه ادم گوده‌گذار (Pitting Edema) وجود دارد؟ اگر بله چند + است؟"
      }
    },
    "abdominal_system": {
      "inspection": "آیا شکم از نظر شکل (Flat, Rounded, Protuberant)، تقارن و وجود زخم/اسکار جراحی غیرطبیعی است؟",
      "auscultation": {
        "bowel_sounds": "آیا صداهای روده (Bowel Sounds) در سمع حضور دارند و فرکانس و شدت آن‌ها طبیعی است (Normoactive)؟ (یا Hyperactive/Hypoactive)",
        "vascular_bruits": "آیا در سمع آئورت یا شریان‌های کلیوی، صدای وزوز (Bruit) شنیده می‌شود؟"
      },
      "percussion": {
        "general": " یا dulness وجود داردآیا صدای غالب دق، تیمپانی (Tympany) است؟",
        "organ_borders": "آیا حدود کبد یا طحال در دق، غیرعادی است؟"
      },
      "palpation": {
        "superficial_tenderness": "آیا در لمس سطحی، حساسیت به لمس (Tenderness) موضعی یا عمومی وجود دارد؟",
        "deep_masses_and_organs": "آیا در لمس عمقی، توده (Mass) غیرعادی، بزرگی کبد (Hepatomegaly) یا طحال (Splenomegaly) احساس می‌شود؟"
      },
      "peritoneal_signs": "آیا علائم پریتونیت (مانند ریفاند تندرنس - Rebound Tenderness، یا سفتی غیرارادی عضلات - Guarding) وجود دارد؟"
    },
    "neurological": {
      "mental_status_and_LOC": "آیا سطح هوشیاری بیمار طبیعی است و از نظر زمان، مکان و شخص جهت‌یابی (Orientation) دارد؟",
      "cranial_nerves": "آیا عملکرد اعصاب کرانیال اصلی (مانند تقارن حرکات صورت، حرکات چشم و بلع) طبیعی است؟",
      "motor_strength_and_tone": "قدرت عضلانی در اندام‌های فوقانی و تحتانی چقدر است(با استفاده از مقیاس 0 تا 5)؟ و آیا تون عضلانی (سفتی/شلی) طبیعی است؟",
      "involuntary_movements": "آیا حرکات غیرارادی (مانند ترمور، تیک) یا آتروفی (Atrophy) عضلانی مشاهده می‌شود؟",
      "sensory_light_touch_and_pain": "آیا حس‌های لمس سبک و درد/دما در اندام‌ها، متقارن و بدون نقص هستند؟",
      "deep_tendon_reflexes": "آیا رفلکس‌های عمیق تاندونی (DTRs) در تمام اندام‌ها وجود دارند، متقارن هستند و شدت آن‌ها طبیعی است؟ (0 تا 4+)",
      "coordination_and_gait": "آیا تست‌های هماهنگی (مانند انگشت به بینی) نرمال هستند؟ و آیا الگوی راه رفتن (Gait) و تعادل بیمار طبیعی است و در غیر این صورت الگوی Gait بیمار چگونه است؟"
    },
    "musculoskeletal_system": {
      "inspection": {
        "joints": "آیا مفاصل از نظر تورم، قرمزی، بدشکلی (Deformity) یا آتروفی، ظاهر طبیعی دارند؟",
        "muscles": "آیا عضلات از نظر تورم، قرمزی، بدشکلی (Deformity) یا آتروفی، ظاهر طبیعی دارند؟"
      },
      "palpation": {
        "tenderness_and_crepitus": "آیا در لمس مفاصل و عضلات، حساسیت به لمس (Tenderness)، گرما، یا صدای ساییده شدن (Crepitus) احساس می‌شود؟"
      },
      "range_of_motion_active_passive": "آیا دامنه حرکتی (ROM) فعال و غیرفعال مفاصل اصلی (مانند شانه، زانو و هیپ) کامل و بدون درد است؟",
      "stability_and_function": "آیا مفاصل از نظر پایداری (Stability) طبیعی هستند و بیمار می‌تواند عملکرد حرکتی خود را به خوبی انجام دهد؟"
    }
  },
  "paraclinic": {
    "basic_blood_tests": {
      "CBC": ["Hb", "WBC", "Plt"],
      "ESR/CRP": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "BMP": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "LFTs": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "VBG": "نتایج تست بر اساس بیماری {disease} داده شود."
    },
    "specialized_lung_tests": {
      "Sputum_analysis": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "Sputum_AFB": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "a1_antitrypsin_level": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "D_dimer": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "BNP/NT_proBNP": "نتایج تست بر اساس بیماری {disease} داده شود."
    },
    "immunity_and_serology": {
      "HIV_test": "نتایج تست بر اساس بیماری {disease} داده شود.",
      "Autoimmune_pannel_ANA_ANCA": "نتایج تست بر اساس بیماری {disease} داده شود."
    },
    "simple_imaging": {
      "Chest_X_Ray": {
        "PA": "در صورت diagnostic نبودن برای بیماری {disease}: رادیولوژیست نمی داند شما چرا درخواست CXR داده اید! با این حال نتایج نرمال هستند. در صورت diagnostic بودن تفسیر یک CXR تیپیک برای بیماری {disease} را خروجی بده.",
        "Lateral": "در صورت diagnostic نبودن برای بیماری {disease}: رادیولوژیست نمی داند شما چرا درخواست CXR داده اید! با این حال نتایج نرمال هستند. در صورت diagnostic بودن تفسیر یک CXR تیپیک برای بیماری {disease} را خروجی بده."
      }
    },
    "advanced_imaging": {
      "Chest_CT_CTPA": "در صورت diagnostic نبودن برای بیماری {disease}: رادیولوژیست نمی داند شما چرا درخواست CT داده اید! با این حال نتایج نرمال هستند. در صورت diagnostic بودن تفسیر یک CT تیپیک برای بیماری {disease} را خروجی بده.",
      "MRI_chest": "در صورت diagnostic نبودن برای بیماری {disease}: رادیولوژیست نمی داند شما چرا درخواست MRI داده اید! با این حال نتایج نرمال هستند. در صورت diagnostic بودن تفسیر یک MRI تیپیک برای بیماری {disease} را خروجی بده.",
      "Pet_scan": "در صورت diagnostic نبودن برای بیماری {disease}: رادیولوژیست نمی داند شما چرا درخواست Pet scan داده اید! با این حال نتایج نرمال هستند. در صورت diagnostic بودن تفسیر یک Pet scan تیپیک برای بیماری {disease} را خروجی بده."
    },
    "functional_tests": {
      "Spirometry": "در صورت diagnostic بودن تفسیر یک Spirometry تیپیک برای بیماری {disease} را خروجی بده.",
      "peak_flow": "در صورت diagnostic بودن تفسیر یک peak flow تیپیک برای بیماری {disease} را خروجی بده.",
      "plethysmography": "در صورت diagnostic بودن تفسیر یک plethysmography تیپیک برای بیماری {disease} را خروجی بده."
    },
    "procedures": {
      "Bronchoscopy": "در صورت diagnostic نبودن نتایج را نشان بده با این حال اخطاری مبنی بر خطرات انجام این پروسیجر در نبود اندیکاسیون آن بده.",
      "torachonthesis": "در صورت diagnostic نبودن نتایج را نشان بده با این حال اخطاری مبنی بر خطرات انجام این پروسیجر در نبود اندیکاسیون آن بده."
    }
  },
  "differential_diagnosis": {
    "disease1": "Asthma",
    "disease2": "Pneumonia",
    "disease3": "COPD",
    "disease4": "PTE",
    "disease5": "IPF",
    "disease6": "PH",
    "disease7": "Pleural Effusion",
    "disease8": "ARDS"
  },
  "pleural_effusion_assessment": {
    "has_effusion": "آیا بیمار افیوژن دارد؟ (بله/خیر)",
    "need_aspiration": "آیا نیاز به کشیدن مایع (توراسنتز) هست؟ (بله/خیر)",
    "effusion_type": "نوع مایع چیست؟ (اگزودا/ترانسودا)"
  }
}

def flatten_scenario(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            if "question" in v and "analysis" in v:
                items.append((new_key, True))
            else:
                items.extend(flatten_scenario(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def flatten_student(d, parent_key='', sep='.'):
    """تخت‌سازی ساده برای لاگ دانشجو"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_student(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def calculate_metrics(optimal, student):
    flat_optimal = flatten_scenario(optimal)
    flat_student = flatten_student(student)
    
    categorized = {
        "correct": [],
        "missed": [],
        "noise": []
    }
    
    all_keys = set(flat_optimal.keys()) | set(flat_student.keys())
    
    for key in all_keys:
        is_required = str(flat_optimal.get(key, "False")).lower() == "true"
        
        stud_val = flat_student.get(key, "False")
        clean_stud_val = str(stud_val).strip().replace("ّ", "").lower()
        is_performed = stud_val is not None and clean_stud_val not in ["false", "none", "", "0"]
        
        if is_required and is_performed:
            categorized["correct"].append(key)
        elif is_required and not is_performed:
            categorized["missed"].append(key)
        elif not is_required and is_performed:
            categorized["noise"].append(key)
            
    correct_count = len(categorized["correct"])
    noise_count = len(categorized["noise"])
    missed_count = len(categorized["missed"])
    total_performed = correct_count + noise_count
    
    efficiency_score = int((correct_count / total_performed) * 100) if total_performed > 0 else 0
        
    return {
        "counts": {
            "signal": correct_count,
            "noise": noise_count,
            "missed": missed_count,
            "total_performed": total_performed
        },
        "score": efficiency_score,
        "details": categorized
    }

def extract_nested_data(node, key_to_extract):
    results = []
    if isinstance(node, dict):
        if key_to_extract in node:
            results.append(node[key_to_extract])
        else:
            for v in node.values():
                results.extend(extract_nested_data(v, key_to_extract))
    elif isinstance(node, str) and key_to_extract == "question":
        results.append(node)
    return results

def get_action_details(key, detailed_scenario, full_scenario):
    parts = key.split('.')
    mapped_parts = ["past_medical_history" if p == "medical_history" else p for p in parts]
    
    curr_det = detailed_scenario
    found_detailed = True
    for p in mapped_parts:
        if isinstance(curr_det, dict) and p in curr_det:
            curr_det = curr_det[p]
        else:
            if isinstance(curr_det, dict) and ("analysis" in curr_det or "question" in curr_det):
                pass 
            else:
                found_detailed = False
            break

    full_curr = full_scenario
    found_full = True
    for p in parts:
        if isinstance(full_curr, dict) and p in full_curr:
            full_curr = full_curr[p]
        else:
            if isinstance(full_curr, dict) and "question" in full_curr:
                pass
            else:
                found_full = False
            break

    question_text = parts[-1] 
    analysis_text = "این اقدام در این سناریوی خاص غیرضروری یا فاقد اولویت بود."
    
    if found_detailed:
        if isinstance(curr_det, dict):
            if "question" in curr_det:
                question_text = curr_det["question"]
            else:
                qs = extract_nested_data(curr_det, "question")
                if qs: question_text = " / ".join(qs)
                
            if "analysis" in curr_det and curr_det["analysis"]:
                analysis_text = curr_det["analysis"]
            else:
                ans = extract_nested_data(curr_det, "analysis")
                valid_ans = [a for a in ans if a]
                if valid_ans:
                    analysis_text = " | ".join(valid_ans)
                elif "question" not in curr_det:
                    analysis_text = "بدون تحلیل اختصاصی."
                    
        elif isinstance(curr_det, str):
            question_text = curr_det
            analysis_text = "بدون تحلیل اختصاصی."

    elif found_full:
        if isinstance(full_curr, dict) and "question" in full_curr:
            question_text = full_curr["question"]
        elif isinstance(full_curr, str):
            question_text = full_curr
        else:
            qs = extract_nested_data(full_curr, "question")
            if qs: question_text = " / ".join(qs)

    return {
        "id": key,
        "question": question_text,
        "analysis": analysis_text
    }

def generate_ai_analysis(metrics_data, full_scenario_ref):
    """تولید تحلیل متنی فارسی با استفاده از LLM."""
    
    def list_to_str(lst):
        limit = 20
        items = lst[:limit]
        text = "\n".join([f"- {item}" for item in items])
        if len(lst) > limit:
            text += f"\n... و {len(lst)-limit} مورد دیگر."
        return text if items else "موردی یافت نشد"

    correct_str = list_to_str(metrics_data["details"]["correct"])
    missed_str = list_to_str(metrics_data["details"]["missed"])
    noise_str = list_to_str(metrics_data["details"]["noise"])
    
    full_scenario_str = json.dumps(full_scenario_ref, ensure_ascii=False)
    
    parser = JsonOutputParser()

    template_text = """
    Role: Senior Clinical Professor evaluating a medical student in Iran.
    
    ---
    ### CONTEXT MAP (Reference for questions/tests meanings)
    {full_scenario_reference}
    ---
    
    ### STUDENT PERFORMANCE DATA
    - **Efficiency Score:** {efficiency_score}% (Higher is better)
    
    - **CORRECT Actions (Signal - Good Judgment):**
    {correct_list}
    
    - **MISSED Actions (Gap - Dangerous Omissions):**
    {missed_list}
    
    - **NOISE Actions (Waste - Unnecessary/Wrong Actions):**
    {noise_list}
    
    ### INSTRUCTIONS
    Analyze the student's clinical reasoning.
    Return a valid JSON object with exactly these 4 keys in **PERSIAN (Farsi)**:
    1. "strengths": (Text) Praise their correct critical decisions.
    2. "missed_criticals": (Text) Explain the medical risk/consequence of missing the specific items in the 'MISSED' list.
    3. "inefficiencies": (Text) Explain why the specific items in 'NOISE' list were unnecessary for this specific case (cost/radiation/irrelevant).
    4. "conclusion": (Text) A brief, professional final verdict for the student.
    
    {format_instructions}
    """
    
    prompt = PromptTemplate(
        template=template_text,
        input_variables=["full_scenario_reference", "correct_list", "missed_list", "noise_list", "efficiency_score"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    try:
        model = init_chat_model(
            base_url="https://api.avalai.ir/v1", 
            api_key="aa-o3nQicuKCc2ND0IuSOHDXouISJ0GQHvK1cqQmtGgBvORi2FH",
            model="gpt-4o-mini"
        )
        chain = prompt | model | parser
        
        return chain.invoke({
            "full_scenario_reference": full_scenario_str,
            "correct_list": correct_str,
            "missed_list": missed_str,
            "noise_list": noise_str,
            "efficiency_score": metrics_data["score"]
        })
    except Exception as e:
        return {
            "strengths": "سیستم قادر به تولید تحلیل هوشمند نیست.",
            "missed_criticals": "بررسی اتصال به اینترنت یا سرویس هوش مصنوعی.",
            "inefficiencies": str(e),
            "conclusion": "خطا در پردازش هوش مصنوعی."
        }

def calculate_matrix_position(score_percent, duration_seconds, total_time=900):
    # کدهای این بخش تغییری نکرده است
    SCORE_THRESHOLD = 60.0 
    TIME_THRESHOLD_SECONDS = total_time * 0.85 
    
    is_accurate = score_percent >= SCORE_THRESHOLD
    is_fast = duration_seconds <= TIME_THRESHOLD_SECONDS
    
    result = {
        "quadrant_code": "", "label_fa": "", "label_en": "", "description": "", "color": ""
    }
    
    if is_accurate and is_fast:
        result.update({"quadrant_code": "Q1_MASTER", "label_fa": "مسلط / استادانه", "label_en": "Master / Efficient", "description": "عالی. تعادل ایده‌آل بین سرعت عمل و دقت علمی.", "color": "#2E7D32"})
    elif is_accurate and not is_fast:
        result.update({"quadrant_code": "Q2_CAUTIOUS", "label_fa": "محتاط / دقیق", "label_en": "Cautious", "description": "تشخیص صحیح با سرعت پایین. نیاز به تمرین برای افزایش سرعت تصمیم‌گیری.", "color": "#FBC02D"})
    elif not is_accurate and is_fast:
        result.update({"quadrant_code": "Q3_RASH", "label_fa": "عجول / شتاب‌زده", "label_en": "Rash / Impulsive", "description": "هشدار: سرعت بالا بدون دقت علمی. این الگو در بالین خطرناک است.", "color": "#C62828"})
    else:
        result.update({"quadrant_code": "Q4_NOVICE", "label_fa": "نیازمند آموزش پایه", "label_en": "Novice", "description": "نیاز به مطالعه بیشتر و تمرین سناریوها برای بهبود دقت و سرعت.", "color": "#757575"})

    result["coordinates"] = {
        "x": duration_seconds, "y": score_percent,
        "x_threshold": TIME_THRESHOLD_SECONDS, "y_threshold": SCORE_THRESHOLD
    }
    return result

def generate_feedback(disease_category, specific_scenario_key, student_log):
    try:
        # مپ اول: برای ارزیابی عملکرد و منطق نمره‌دهی
        optimal_scenario = SCENARIO_MAP[disease_category][specific_scenario_key]
        # مپ دوم: برای استخراج متون فارسی و تحلیل‌ها
        detailed_scenario = DETAILED_SCENARIO_MAP[disease_category][specific_scenario_key]
    except KeyError:
        return {"error": f"Scenario {disease_category} -> {specific_scenario_key} not found."}

    evaluator = ClinicalEvaluator(optimal_scenario, student_log)
    final_score_percent = evaluator.evaluate_performance()
    
    duration_seconds, start_time = evaluator.calculate_duration()
    time_analysis = evaluator.analyze_time_performance(duration_seconds, evaluator.total_time_seconds)
    category = evaluator.get_category(final_score_percent)

    metrics = calculate_metrics(optimal_scenario, student_log)
    
    # 🌟 استفاده از مپ دوم (detailed_scenario) برای غنی‌سازی لیست‌ها
    enriched_correct = [get_action_details(k, detailed_scenario, FULL_SCENARIO) for k in metrics["details"]["correct"]]
    enriched_missed = [get_action_details(k, detailed_scenario, FULL_SCENARIO) for k in metrics["details"]["missed"]]
    enriched_noise = [get_action_details(k, detailed_scenario, FULL_SCENARIO) for k in metrics["details"]["noise"]]
    
    # ارسال سوالات استخراج شده به هوش مصنوعی برای تولید تحلیل با کیفیت
    ai_metrics_data = {
        "score": metrics["score"],
        "details": {
            "correct": [item["question"] for item in enriched_correct],
            "missed": [item["question"] for item in enriched_missed],
            "noise": [item["question"] for item in enriched_noise]
        }
    }
    ai_analysis = generate_ai_analysis(ai_metrics_data, FULL_SCENARIO)
    
    matrix_data = calculate_matrix_position(final_score_percent, duration_seconds, evaluator.total_time_seconds)
    diagnosis_results = evaluator.evaluate_diagnosis_accuracy()
    pleural_results = evaluator.evaluate_pleural_effusion()
    
    output = {
        "meta": {
            "disease": disease_category,
            "scenario": specific_scenario_key
        },
        "overall_result": {
            "title": category['label'],
            "english_title": category['eng'],
            "color_code": category['color'],
            "is_passed": final_score_percent >= 60
        },
        "score": {
            "obtained": round(final_score_percent, 2),
            "total": 100,
            "efficiency_score": metrics["score"]
        },
        "time_management": {
            "duration_formatted": evaluator.format_time(duration_seconds),
            "total_allowed_formatted": "15:00",
            "analysis": time_analysis
        },
        "chart_data": {
            "signal_value": metrics["counts"]["signal"],
            "noise_value": metrics["counts"]["noise"],  
            "missed_value": metrics["counts"]["missed"],
            "total_actions": metrics["counts"]["total_performed"]
        },
        "performance_matrix": {
            "title": "تحلیل سرعت در برابر دقت",
            "status": matrix_data["label_fa"],
            "status_en": matrix_data["label_en"],
            "description": matrix_data["description"],
            "color_code": matrix_data["color"],
            "quadrant": matrix_data["quadrant_code"],
            "chart_coordinates": matrix_data["coordinates"]
        },
        "diagnosis_section": {
            "user_final_diagnosis": diagnosis_results["student_final_answer"],
            "correct_final_diagnosis": diagnosis_results["correct_final_answer"],
            "is_correct": diagnosis_results["is_final_correct"],
            "differential_analysis": {
                "correct_items": diagnosis_results["correct_differentials"],
                "missed_items": diagnosis_results["missed_differentials"]
            },
            "feedback_message": f"تشخیص نهایی شما {'صحیح بود' if diagnosis_results['is_final_correct'] else 'نادرست بود'}."
        },
        "pleural_effusion_section": {
          "title": "ارزیابی پلورال افیوژن",
          "is_correct": pleural_results["is_correct"],
          "user_assessment": pleural_results["student"],
          "correct_assessment": pleural_results["optimal"],
          "feedback_message": "تشخیص وضعیت مایع پلور صحیح بود." if pleural_results["is_correct"] else "در تشخیص وضعیت مایع پلور اشتباه داشتید."
        },
        "detailed_lists": {
            "missed_items": enriched_missed,
            "noise_items": enriched_noise,
            "correct_items": enriched_correct
        },
        "ai_analysis": ai_analysis
    }
    
    return output

# sample_student_log = {
#   "history_taking": {
#     "present_illness": {
#       "question1": "14:50",  # درست
#       "question3": "14:35",  # درست
#       "question4": "14:20",  # نویز (اضافی)
#       "question6": "14:05",  # درست
#       "question8": "13:50"   # درست
#     },
#     "past_medical_history": {
#       "question3": "13:20"   # درست
#     },
#     "drug_history": {
#       "question1": "13:00"   # درست
#     },
#     "social_history": {
#       "question1": "12:45",  # نویز
#       "question3": "12:30"   # درست
#     },
#     "ros": {
#       "question6": "12:00"   # درست
#     }
#   },
#   "physical_exam": {
#     "vital_signs": {
#       "BP": "11:45",
#       "PR": "11:40",
#       "SpO2": "11:35"
#     },
#     "general_appearance": {
#       "cardiopulmonary_and_circulatory_clues": {
#         "edema": "11:15",
#         "cyanosis": "11:10"
#       }
#     },
#     "cardiovascular_system": {
#       "JVP_assessment": "10:50",
#       "auscultation": {
#         "heart_sounds_s1_s2": "10:30"
#       },
#       "2_pulses_and_extremities": {     
#         "extremities_edema": "10:15"
#       }
#     },
#     "respiratory_system": {
#       "auscultation": {
#         "breath_sounds_intensity": "09:50"
#       }
#     }
#   },
#   "paraclinic": {
#     "basic_blood_tests": {
#       "BMP": "09:20",
#       "CBC": "09:18",
#       "LFTs": "09:15"
#     },
#     "specialized_lung_tests": {
#       "BNP_NT_proBNP": "08:50",
#       "D_dimer": "08:45"        # نویز
#     },
#     "immunity_and_serology": {
#       "Autoimmune_pannel_ANA_ANCA": "08:20"
#     },
#     "simple_imaging": {
#       "Chest_X_Ray": "08:00"
#     },
#     "advanced_imaging": {
#       "Chest_CT_CTPA": "07:30"
#     },
#     "functional_tests": {
#       "Spirometry": "07:00"
#     }
#   },
#   "differential_diagnosis": {
#     "disease3": "06:30", # COPD
#     "disease4": "06:20", # PTE 
#     "disease6": "06:10"  # PH 
#   },
#   "final_diagnosis": {
#     "disease": "PH" 
#   },
#   "pleural_effusion_assessment": {
#     "has_effusion": "false",
#     "need_aspiration": "false",
#     "effusion_type": "none"
#   }
# }

# if __name__ == "__main__":
#     print("در حال تولید بازخورد با دیتای زمانی. لطفاً منتظر بمانید...\n")
    
#     # فراخوانی تابع ارزیاب
#     result = generate_feedback(
#         disease_category="PH", 
#         specific_scenario_key="idiopathic_pah", 
#         student_log=sample_student_log
#     )
    
#     # نمایش خروجی نهایی
#     print("نتیجه ارزیابی:")
#     print(json.dumps(result, ensure_ascii=False, indent=4))