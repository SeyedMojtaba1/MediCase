import getpass
import os
from langchain.chat_models import init_chat_model
# from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json
import random

from typing import List, Optional
from pydantic import BaseModel, Field

class PersonalInformation(BaseModel):
    first_name: str = Field(..., description="First Name")
    last_name: str = Field(..., description="Last Name")
    age: str = Field(..., description="Age (appropriate for disease prevalence)")
    gender: str = Field(..., description="Gender")
    occupation: str = Field(..., description="Occupation")
    place_of_birth: str = Field(..., description="Place Of Birth")
    place_of_residence: str = Field(..., description="Place Of Residence")
    marital_status: str = Field(..., description="Marital Status")

class VitalSign(BaseModel):
    BP: str = Field(..., description="Blood Pressure")
    T: str = Field(..., description="Temperature")
    PR: str = Field(..., description="Pulse Rate")
    RR: str = Field(..., description="Respiratory Rate")
    SpO2: str = Field(..., description="Saturation of O2")
    GCS: str = Field(..., description="Level of Consciousness")

class PatientProfile(BaseModel):
    personal_information: PersonalInformation
    chief_complaint: str = Field(..., description="Chief Complaint")
    vital_sign: VitalSign

class PresentIllness(BaseModel):
    question1: str = Field(..., description="علائم از چه زمانی شروع شدند و در طول زمان چه تغییری کردند؟")
    question2: str = Field(..., description="شروع علائم ناگهانی بوده یا تدریجی؟ بعد از اتفاق خاصی مثل عفونت یا تماس خاصی شروع شد؟")
    question3: str = Field(..., description="آیا تنگی نفس دارید؟ اگر بله تنگی نفستون دائمیه یا دوره‌ای؟ و با فعالیت بدتر میشه یا در حالت استراحت هم وجود داره؟")
    question4: str = Field(..., description="سرفه دارید؟ اگر بله، خشک است یا همراه با خلط؟ رنگ و حجم خلط چطور است؟")
    question5: str = Field(..., description="تا حالا خس‌خس یا صدای غیرعادی در تنفس شنیدید؟")
    question6: str = Field(..., description="احساس درد یا فشار در قفسه سینه دارید؟ با تنفس یا حرکت تغییر می‌کنه؟")
    question7: str = Field(..., description="در روزهای اخیر تب، لرز یا تعریق شبانه داشتید؟ وجود یا عدم وجود تب باید با زمینهٔ بالینی هماهنگ باشد. در بیماری‌های مزمن پایدار معمولاً تب وجود ندارد، اما در تشدید حاد یا عفونت‌ها ممکن است تب و لرز مشاهده شود. پاسخ 'بله' یا 'خیر' را بر اساس ماهیت بیماری و مرحله آن تولید کن.")
    question8: str = Field(..., description="تورم پا، تپش قلب یا احساس سبکی سر دارید؟")
    question9: str = Field(..., description="قبلاً هم چنین حمله یا علائمی داشتید؟ چه درمانی کمکتون کرده؟")
    question10: str = Field(..., description="احساس کاهش وزن، خستگی یا بی‌اشتهایی داشتید؟")

# --- Sub-models for nested questions ---
class PMHQuestion1(BaseModel):
    question1a: str = Field(..., description="آیا بیماری طولانی مدت (مزمن) مثل قند (دیابت)، فشار خون، آسم، مشکل تیروئید، یا بیماری جدی کلیوی/کبدی دارید؟")
    question1b: str = Field(..., description="اگر پاسخ question1a بله بود، تشخیص این بیماری از چه موقع بوده است؟")

class PMHQuestion2(BaseModel):
    question2a: str = Field(..., description="آیا تا به حال عمل جراحی (بزرگ یا کوچک) داشته‌اید؟ و آیا تا به حال در بیمارستان بستری شده‌اید؟")
    question2b: str = Field(..., description="اگر پاسخ question2a بله بود، دلیلش چه بوده و دقیقا چند وقت پیش بوده است؟(چند سال و چند ماه) همچنین، آیا تا به حال انتقال خون داشته‌اید؟")

class PastMedicalHistory(BaseModel):
    question1: PMHQuestion1
    question2: PMHQuestion2
    question3: str = Field(..., description="آیا سابقه بیماری های قلبی، ریوی و مغزی را دارید؟")
    question4: str = Field(..., description="آیا در حال حاظر یا در گذشته سرطان فعال داشته‌اید؟")
    question5: str = Field(..., description="در دوران کودکی، آیا بیماری‌های خاصی (مثل تب روماتیسمی، سرخک شدید) گرفتید یا به دلیل بیماری بستری شدید؟")
    question6: str = Field(..., description="در دوران کودکی، آیا بیماری‌های خاصی (مثل تب روماتیسمی، سرخک شدید) گرفتید یا به دلیل بیماری بستری شدید؟")

class DrugHistoryQuestion1(BaseModel):
    question1a: str = Field(..., description="لطفاً لیست تمام داروهایی که در حال حاضر به صورت مرتب (روزانه، هفتگی یا ماهانه) مصرف می‌کنید را به من بگویید.")
    question1b: str = Field(..., description="دوز هر دارو چقدر است و چند بار در روز مصرف می‌کنید؟")
    question1c: str = Field(..., description="آیا در چند روز گذشته، دوز یا زمان مصرف هیچ‌کدام از این داروها را تغییر داده‌اید؟")

class DrugHistory(BaseModel):
    question1: DrugHistoryQuestion1
    question2: str = Field(..., description="به صورت منظم داروهای بدون نسخه (OTC) (مثل داروهای سرماخوردگی، مسکن‌ها، آنتی‌اسیدها)، مکمل‌های غذایی، داروهای گیاهی یا خواب آور مصرف می‌کنید؟")

class AllergyQuestion1(BaseModel):
    question1a: str = Field(..., description="آیا به دارو، غذا، یا ماده خاصی آلرژی (حساسیت) دارید؟")
    question1b: str = Field(..., description="اگر پاسخ question1a بله بود، دقیقاً چه دارو یا ماده‌ای است؟ و واکنش شما (مثل کهیر یا تنگی نفس) چگونه بوده است؟")

class Allergies(BaseModel):
    question1: AllergyQuestion1

class FHQuestion1(BaseModel):
    question1a: str = Field(..., description="آیا در خانواده درجه یک (پدر، مادر، خواهر یا برادر) شما، سابقه ابتلا به بیماری‌های مزمن و شایع وجود دارد؟")
    question1b: str = Field(..., description="اگر پاسخ question1a بله بود، چه کسی و در چه سنی به آن مبتلا شده است؟")

class FHQuestion3(BaseModel):
    question3a: str = Field(..., description="آیا سابقه سرطان خاصی در خانواده درجه یک شما وجود دارد؟")
    question3b: str = Field(..., description="اگر پاسخ question3a بله بود، نوع سرطان چه بوده و در چه سنی تشخیص داده شده است؟")

class FamilyHistory(BaseModel):
    question1: FHQuestion1
    question2: str = Field(..., description="آیا در خانواده درجه یک شما، سابقه حمله قلبی (سکته قلبی)، سکته مغزی، یا نارسایی قلبی وجود دارد؟")
    question3: FHQuestion3

class SHQuestion1(BaseModel):
    question1a: str = Field(..., description="آیا تا به حال سیگار، قلیان، پیپ، یا هر نوع محصول نیکوتینی مصرف کرده‌اید؟")
    question1b: str = Field(..., description="اگر قبلاً مصرف می‌کردید، چه زمانی ترک کرده‌اید؟")

class SHQuestion3(BaseModel):
    question3a: str = Field(..., description="آیا تا به حال مواد مخدر مصرف کرده‌اید؟")
    question3b: str = Field(..., description="اگر مصرف داشته‌اید، نوع آن و آخرین باری که مصرف کرده‌اید چه زمانی بوده است؟")

class SocialHistory(BaseModel):
    question1: SHQuestion1
    question2: str = Field(..., description="آیا الکل مصرف می‌کنید؟ اگر بله، نوع و میزان مصرف آن در هفته چقدر است؟")
    question3: SHQuestion3
    question4: str = Field(..., description="در خانه همراه چه کسانی زندگی می‌کنید؟")

class ROS(BaseModel):
    question1: str = Field(..., description="آیا اخیراً دچار تب، لرز، کاهش یا افزایش وزن ناخواسته، یا خستگی شدید و غیرمعمول شده‌اید؟")
    question2: str = Field(..., description="آیا سابقه راش، خارش، زخم‌های طولانی‌مدت، تغییر در رنگ یا بافت پوست/مو/ناخن، یا کبودی غیرعادی دارید؟")
    question3: str = Field(..., description="آیا اخیراً دچار سردرد، سرگیجه، سفتی گردن، یا بزرگ شدن غدد لنفاوی در گردن شده‌اید؟")
    question4: str = Field(..., description="آیا دچار تاری دید، دوبینی، درد چشم، قرمزی، یا کاهش دید ناگهانی شده‌اید؟")
    question5: str = Field(..., description="آیا دچار وزوز گوش، کاهش شنوایی، خونریزی بینی، گرفتگی مزمن بینی، گلودرد مزمن، مشکل در بلع (دیسفاژی)، یا آفت و زخم‌های دهانی مکرر هستید؟")
    question6: str = Field(..., description="آیا سابقه درد قفسه سینه، تپش قلب، تنگی نفس با فعالیت، تنگی نفس در حالت خوابیده ، یا تورم پاها دارید؟")
    question7: str = Field(..., description="آیا سابقه سرفه، خس‌خس سینه، خلط خونی ، یا تنگی نفس (به جز تنگی نفس مرتبط با فعالیت شدید) دارید؟")
    question8: str = Field(..., description="آیا دچار حالت تهوع، استفراغ، سوزش سر دل، درد شکم، تغییر در عادات اجابت مزاج (اسهال یا یبوست)، خونریزی از مقعد، یا زردی پوست و چشم هستید؟")
    question9: str = Field(..., description="آیا دچار درد یا سوزش حین ادرار کردن، تکرر ادرار، خون در ادرار، مشکل در کنترل ادرار، یا ترشحات غیرعادی هستید؟")
    question10: str = Field(..., description="آیا دچار درد مفاصل، سفتی صبحگاهی، تورم مفاصل، درد یا ضعف عضلانی، یا کمردرد مزمن هستید؟")
    question11: str = Field(..., description="آیا سابقه سردرد شدید یا جدید، تشنج، ضعف یا بی‌حسی در دست‌ها/پاها، مشکل در تعادل/هماهنگی، یا تغییر در حافظه دارید؟")
    question12: str = Field(..., description="آیا اخیراً احساس افسردگی، اضطراب، تغییرات شدید خلقی، یا مشکل در خواب (بی‌خوابی/پرخوابی) داشته‌اید؟")
    question13: str = Field(..., description="آیا دچار افزایش تشنگی، افزایش گرسنگی، افزایش ادرار (پلی اوری)، یا عدم تحمل گرما/سرما شده‌اید؟")
    question14: str = Field(..., description="آیا سابقه کبودی آسان، خونریزی طولانی‌مدت، بزرگ شدن غدد لنفاوی، یا کم‌خونی شدید دارید؟")

class HistoryTaking(BaseModel):
    present_illness: PresentIllness
    past_medical_history: PastMedicalHistory
    drug_history: DrugHistory
    allergies: Allergies
    family_history: FamilyHistory
    social_history: SocialHistory
    ros: ROS

class LevelOfConsciousnessMoodAndBehavior(BaseModel):
    level_of_consciousness: str = Field(..., description="آیا بیمار هوشیار، گیج، خواب‌آلود (لتارژیک)، یا در حالت اغما (Comatose) است؟ آیا دستورات ساده را اجرا می‌کند؟")
    mood: str = Field(..., description="آیا بیمار به نظر بیمار، مضطرب، یا در درد شدید است؟")
    behavior: str = Field(..., description="آیا بیمار همکاری می‌کند؟ آیا مضطرب، افسرده، یا پرخاشگر است؟ آیا از نظر روانی وضعیت طبیعی دارد؟")

class PostureAndPosition(BaseModel):
    position_of_comfort: str = Field(..., description="آیا بیمار وضعیتی را برای کاهش درد یا تنگی نفس انتخاب کرده است؟")

class OverallAppearance(BaseModel):
    nutritional_status: str = Field(..., description="آیا بیمار لاغر (Cachectic)، چاق (Obese)، یا در وضعیت وزن طبیعی است؟")

class CardiopulmonaryAndCirculatoryClues(BaseModel):
    cyanosis: str = Field(..., description="بررسی لب‌ها، زبان و بستر ناخن برای علائم کبودی.")
    dyspnea: str = Field(..., description="آیا بیمار به سختی نفس می‌کشد؟")
    edema: str = Field(..., description="وجود تورم در پاها، مچ پا یا اطراف چشم.")

class GeneralAppearance(BaseModel):
    level_of_consciousness_mood_and_behavior: LevelOfConsciousnessMoodAndBehavior
    posture_and_position: PostureAndPosition
    overall_appearance: OverallAppearance
    cardiopulmonary_and_circulatory_clues: CardiopulmonaryAndCirculatoryClues

class HeadAndFace(BaseModel):
    symmetry_and_lesions: str = Field(..., description="آیا سر و صورت بیمار متقارن است و شواهدی از زخم، توده یا ضایعات پوستی وجود دارد؟")
    tenderness: str = Field(..., description="آیا در لمس جمجمه حساسیت به لمس یا درد وجود دارد؟")

class Eyes(BaseModel):
    sclera_and_conjunctiva: str = Field(..., description="آیا در صلبیه (سفیدی چشم) زردی (یرقان) یا در ملتحمه (پلک پایین) رنگ‌پریدگی شدید (کم‌خونی) مشاهده می‌شود؟")
    pupils_reaction: str = Field(..., description="آیا مردمک‌ها متقارن هستند و به نور واکنش طبیعی نشان می‌دهند؟")
    extraocular_movements: str = Field(..., description="آیا حرکات چشمی در جهات مختلف کامل و هماهنگ هستند؟")

class Ears(BaseModel):
    external_and_tenderness: str = Field(..., description="آیا لاله گوش یا ناحیه ماستوئید (پشت گوش) متورم، قرمز یا دردناک هستند؟")
    eardrum_appearance: str = Field(..., description="آیا پرده صماخ در اتوسکوپی ظاهر طبیعی دارد (شفاف، بدون التهاب یا پارگی)؟")

class NoseAndSinuses(BaseModel):
    septum_and_discharge: str = Field(..., description="آیا تیغه بینی انحراف شدید دارد و آیا ترشحات غیرعادی (چرکی یا خونی) مشاهده می‌شود؟")
    sinus_tenderness: str = Field(..., description="آیا تیغه بینی انحراف شدید دارد و آیا ترشحات غیرعادی (چرکی یا خونی) مشاهده می‌شود؟")

class MouthAndPharynx(BaseModel):
    oral_mucosa_and_lesions: str = Field(..., description="آیا مخاط دهان (لثه‌ها، زیر زبان) مرطوب و بدون ضایعات غیرعادی (زخم یا آفت) است؟")
    pharynx_and_tonsils: str = Field(..., description="آیا حلق (گلو) قرمز یا متورم است و آیا لوزتین‌ها (Tonsils) بزرگ شده‌اند یا دارای ترشحات چرکی هستند؟")

class NeckAndLymphatics(BaseModel):
    inspection: str = Field(..., description="آیا در معاینه ظاهری گردن، تورم، قرمزی، توده، یا زخم قابل مشاهده‌ای وجود دارد؟")
    tracheal_position: str = Field(..., description="آیا نای (Trachea) در خط وسط قرار دارد؟ آیا در لمس، انحراف یا جابه‌جایی نای (Tracheal Deviation) احساس می‌شود؟")
    thyroid_gland: str = Field(..., description="آیا غده تیروئید (از پشت بیمار) بزرگ است (گواتر)؟ آیا در لمس، ندول (توده)، سفتی، یا حساسیت به لمس وجود دارد؟")
    carotid_bruit: str = Field(..., description="آیا غده تیروئید (از پشت بیمار) بزرگ است (گواتر)؟ آیا در لمس، ندول (توده)، سفتی، یا حساسیت به لمس وجود دارد؟")
    lymph_nodes_size_consistency: str = Field(..., description="آیا غدد لنفاوی در نواحی مختلف (سرویکال، ساب‌ماندیبولار، سوپراکلاویکولار) بزرگ شده‌اند؟ (اندازه، قوام: نرم/سفت/لاستیکی)")
    lymph_nodes_mobility_tenderness: str = Field(..., description="آیا غدد لنفاوی لمس شده، متحرک هستند یا ثابت و چسبیده به بافت زیرین؟ آیا در لمس، درد (Tenderness) دارند؟")

class HeadAndNeck(BaseModel):
    head_and_face: HeadAndFace
    eyes: Eyes
    ears: Ears
    nose_and_sinuses: NoseAndSinuses
    mouth_and_pharynx: MouthAndPharynx
    neck_and_lymphatics: NeckAndLymphatics

class RespiratoryInspection(BaseModel):
    accessory_muscles: str = Field(..., description="آیا از عضلات کمکی تنفس استفاده می‌کند؟")
    chest_shape_and_symmetry: str = Field(..., description="آیا شکل قفسه سینه طبیعی است (بدون Barrel Chest یا کیفواسکولیوز) و حرکت قفسه سینه در دم و بازدم متقارن است؟")

class RespiratoryPalpation(BaseModel):
    chest_expansion: str = Field(..., description="آیا توسعه قفسه سینه در هنگام دم عمیق، متقارن و کامل است؟")
    tactile_fremitus: str = Field(..., description="آیا لرزش‌های صوتی (Tactile Fremitus) در دو طرف قفسه سینه متقارن و طبیعی هستند؟ اسم علمی نوع لرزش ها رو به فارسی ترجمه نکن.")

class RespiratoryAuscultation(BaseModel):
    breath_sounds_intensity: str = Field(..., description="آیا شدت صداهای تنفسی پایه طبیعی است یا کاهش یا عدم وجود صدا وجود دارد؟")
    adventitious_sounds: str = Field(..., description="آیا صداهای اضافی (Adventitious Sounds) مانند کراکل (Crackles)، ویزینگ (Wheezing)، رونکای (Rhonchi) یا اصطکاک پلورال (Pleural Rub) شنیده می‌شوند؟")

class RespiratorySystem(BaseModel):
    inspection: RespiratoryInspection
    palpation: RespiratoryPalpation
    percussion: str = Field(..., description="در بیماری‌های ریوی بسته به نوع درگیری، الگوی صدای پرکاشن متفاوت است: در انسداد مزمن یا افزایش حجم هوا، صدا معمولاً hyperresonant است؛ در تراکم یا فیبروز، صدا dull می‌شود؛ و در حالت طبیعی صدای رزونانس معمول دارد. پاسخ باید بر اساس فیزیولوژی بیماری انتخاب شود، نه همیشه طبیعی. در پاسخ نام صدا ها رو به فارسی ترجمه نکن.")
    auscultation: RespiratoryAuscultation

class CardiovascularPalpation(BaseModel):
    precordial_palpation_heave_thrill: str = Field(..., description="آیا در لمس ناحیه پره‌کوردیوم، لیفت (Lift)، هیو (Heave)، یا تریل (Thrill) احساس می‌شود؟")
    pmi_assessment: str = Field(..., description="ضربان نوک قلب (PMI) در کجا لمس می‌شود (محل دقیق) و آیا اندازه و قدرت آن طبیعی است؟")

class CardiovascularAuscultation(BaseModel):
    heart_sounds_s1_s2: str = Field(..., description="آیا صداهای اصلی قلب (S1 و S2) شنیده می‌شوند و از نظر شدت، اسپلیت و کیفیت، طبیعی هستند؟")
    extra_sounds_s3_s4_murmurs: str = Field(..., description="آیا صداهای اضافی مانند S3، S4، مارمار (Murmur) یا صدای اصطکاک پریکاردیال شنیده می‌شود؟")

class PeripheralPulsesAndExtremities(BaseModel):
    peripheral_pulses_symmetry_and_quality: str = Field(..., description="آیا تمام نبض‌های محیطی (مانند رادیال، فمورال، دورسالیس پدیس) در دو طرف بدن متقارن، منظم، و با کیفیت (قدرت) طبیعی لمس می‌شوند؟")
    extremities_color_and_trophic_changes: str = Field(..., description="آیا در اندام‌های انتهایی، شواهدی از سیانوز (کبودی)، رنگ‌پریدگی، ریزش مو اندام، کلابینگ (Clubbing)، یا تغییرات تروفیک (مانند ریزش مو، نازکی پوست) مشاهده می‌شود؟")
    extremities_temperature_and_cap_refill: str = Field(..., description="آیا اندام‌های انتهایی دمای طبیعی دارند و زمان پر شدن مجدد مویرگی (Capillary Refill Time) چند ثانیه است؟")
    extremities_edema: str = Field(..., description="آیا در اندام‌های تحتانی، شواهدی از ادم (تورم) و به ویژه ادم گوده‌گذار (Pitting Edema) وجود دارد؟ اگر بله چند + است؟")

class CardiovascularSystem(BaseModel):
    JVP_assessment: str = Field(..., description="آیا فشار وریدی ژوگولار (JVP) در وضعیت نیمه نشسته، بالا و غیرطبیعی است؟")
    palpation: CardiovascularPalpation
    auscultation: CardiovascularAuscultation
    peripheral_pulses_and_extremities: PeripheralPulsesAndExtremities

class AbdominalAuscultation(BaseModel):
    bowel_sounds: str = Field(..., description="آیا صداهای روده (Bowel Sounds) در سمع حضور دارند و فرکانس و شدت آن‌ها طبیعی است (Normoactive)؟ (یا Hyperactive/Hypoactive)")
    vascular_bruits: str = Field(..., description="آیا در سمع آئورت یا شریان‌های کلیوی، صدای وزوز (Bruit) شنیده می‌شود؟")

class AbdominalPercussion(BaseModel):
    general: str = Field(..., description=" یا dulness وجود داردآیا صدای غالب دق، تیمپانی (Tympany) است؟")
    organ_borders: str = Field(..., description="آیا حدود کبد یا طحال در دق، غیرعادی است؟")

class AbdominalPalpation(BaseModel):
    superficial_tenderness: str = Field(..., description="آیا در لمس سطحی، حساسیت به لمس (Tenderness) موضعی یا عمومی وجود دارد؟")
    deep_masses_and_organs: str = Field(..., description="آیا در لمس عمقی، توده (Mass) غیرعادی، بزرگی کبد (Hepatomegaly) یا طحال (Splenomegaly) احساس می‌شود؟")

class AbdominalSystem(BaseModel):
    inspection: str = Field(..., description="آیا شکم از نظر شکل (Flat, Rounded, Protuberant)، تقارن و وجود زخم/اسکار جراحی غیرطبیعی است؟")
    auscultation: AbdominalAuscultation
    percussion: AbdominalPercussion
    palpation: AbdominalPalpation
    peritoneal_signs: str = Field(..., description="آیا علائم پریتونیت (مانند ریفاند تندرنس - Rebound Tenderness، یا سفتی غیرارادی عضلات - Guarding) وجود دارد؟")

class Neurological(BaseModel):
    mental_status_and_LOC: str = Field(..., description="آیا سطح هوشیاری بیمار طبیعی است و از نظر زمان، مکان و شخص جهت‌یابی (Orientation) دارد؟")
    cranial_nerves: str = Field(..., description="آیا عملکرد اعصاب کرانیال اصلی (مانند تقارن حرکات صورت، حرکات چشم و بلع) طبیعی است؟")
    motor_strength_and_tone: str = Field(..., description="قدرت عضلانی در اندام‌های فوقانی و تحتانی چقدر است(با استفاده از مقیاس 0 تا 5)؟ و آیا تون عضلانی (سفتی/شلی) طبیعی است؟")
    involuntary_movements: str = Field(..., description="آیا حرکات غیرارادی (مانند ترمور، تیک) یا آتروفی (Atrophy) عضلانی مشاهده می‌شود؟")
    sensory_light_touch_and_pain: str = Field(..., description="آیا حس‌های لمس سبک و درد/دما در اندام‌ها، متقارن و بدون نقص هستند؟")
    deep_tendon_reflexes: str = Field(..., description="آیا رفلکس‌های عمیق تاندونی (DTRs) در تمام اندام‌ها وجود دارند، متقارن هستند و شدت آن‌ها طبیعی است؟ (0 تا 4+)")
    coordination_and_gait: str = Field(..., description="آیا تست‌های هماهنگی (مانند انگشت به بینی) نرمال هستند؟ و آیا الگوی راه رفتن (Gait) و تعادل بیمار طبیعی است و در غیر این صورت الگوی Gait بیمار چگونه است؟")

class MusculoskeletalInspection(BaseModel):
    joints: str = Field(..., description="آیا مفاصل از نظر تورم، قرمزی، بدشکلی (Deformity) یا آتروفی، ظاهر طبیعی دارند؟")
    muscles: str = Field(..., description="آیا عضلات از نظر تورم، قرمزی، بدشکلی (Deformity) یا آتروفی، ظاهر طبیعی دارند؟")

class MusculoskeletalPalpation(BaseModel):
    tenderness_and_crepitus: str = Field(..., description="آیا در لمس مفاصل و عضلات، حساسیت به لمس (Tenderness)، گرما، یا صدای ساییده شدن (Crepitus) احساس می‌شود؟")

class MusculoskeletalSystem(BaseModel):
    inspection: MusculoskeletalInspection
    palpation: MusculoskeletalPalpation
    range_of_motion_active_passive: str = Field(..., description="آیا دامنه حرکتی (ROM) فعال و غیرفعال مفاصل اصلی (مانند شانه، زانو و هیپ) کامل و بدون درد است؟")
    stability_and_function: str = Field(..., description="آیا مفاصل از نظر پایداری (Stability) طبیعی هستند و بیمار می‌تواند عملکرد حرکتی خود را به خوبی انجام دهد؟")

class PhysicalExam(BaseModel):
    general_appearance: GeneralAppearance
    head_and_neck: HeadAndNeck
    respiratory_system: RespiratorySystem
    cardiovascular_system: CardiovascularSystem
    abdominal_system: AbdominalSystem
    neurological: Neurological
    musculoskeletal_system: MusculoskeletalSystem

class BasicBloodTests(BaseModel):
    CBC: List[str] = Field(..., description="Hb, WBC, Plt")
    ESR_CRP: str = Field(..., description="نتایج تست بر اساس بیماری {disease} داده شود.")
    BMP: str = Field(..., description="نتایج تست na, k, ca, bun, cr بر اساس بیماری {disease} داده شود.")
    LFTs: str = Field(..., description="نتایج تست alt, ast, alp, bilirubin, inr بر اساس بیماری {disease} داده شود.")
    VBG: str = Field(..., description="نتایج تست PH, HCO3, PaCO2 بر اساس بیماری {disease} داده شود.")

class SpecializedLungTests(BaseModel):
    Sputum_analysis: str = Field(..., description="Comprehensive sputum analysis findings including: 1) Macroscopic appearance (color, consistency), 2) Microscopic/Gram stain (WBC count, Epithelial cells, bacteria type), 3) Culture results (specific organism or normal flora), and 4) AFB/TB smear status if reported.")
    Sputum_AFB: str = Field(..., description="نتایج تست بر اساس بیماری {disease} و به صورت عددی نمایش داده شود و تفسیری وجود نداشته باشد.")
    a1_antitrypsin_level: str = Field(..., description="نتایج تست بر اساس بیماری {disease} و به صورت عددی نمایش داده شود و تفسیری وجود نداشته باشد.")
    D_dimer: str = Field(..., description="نتایج تست بر اساس بیماری {disease} و به صورت عددی نمایش داده شود و تفسیری وجود نداشته باشد.")
    BNP_NT_proBNP: str = Field(..., description="D-dimer test result. Extract the quantitative value (e.g., 500, 0.5) AND the unit (e.g., ng/mL, mg/L, ug/mL FEU).")

class ImmunityAndSerology(BaseModel):
    HIV_test: str = Field(..., description="نتایج تست بر اساس بیماری {disease} داده شود.")
    Autoimmune_pannel_ANA_ANCA: str = Field(..., description="Extract the complete Autoimmune Panel results. For the ANA test, extract three vital components: the qualitative result (Positive/Negative), the precise Titer (e.g., 1:160, 1:320), and the Immunofluorescence Pattern (e.g., Homogeneous, Speckled). For the ANCA test, ensure to report the status of c-ANCA and p-ANCA, along with the values of specific antibodies, Anti-MPO and Anti-PR3.")

class Spirometry(BaseModel):
    fev1: List[str] = Field(..., description="Measured_Value, Predicted, % Predicted")
    fvc: List[str] = Field(..., description="Measured_Value, Predicted, % Predicted")
    fev1_fvc: List[str] = Field(..., alias="fev1/fvc Measured_Value, Predicted, % Predicted")

class DLCO(BaseModel):
    dlco: List[str] = Field(..., description="Measured_Value, % Predicted")
    dlco_va_ratio: List[str] = Field(..., alias="dlco/va_ratio Measured_Value, % Predicted  ")

class Plethysmography(BaseModel):
    tls: List[str] = Field(..., description="Measured_Value, % Predicted")
    rv: List[str] = Field(..., description="Measured_Value, % Predicted")
    frc: List[str] = Field(..., description="Measured_Value, % Predicted")
    rv_tlc_ratio: str = Field(..., alias="extract the RV/TLC Ratio.")

class FunctionalTests(BaseModel):
    Spirometry: Spirometry
    dlco: DLCO
    plethysmography: Plethysmography

class Torachocenthesis(BaseModel):
    pleural_fluid: List[str] = Field(..., description="LDH, Protein, Albumin, Glucose")
    serum: List[str] = Field(..., description="LDH, Protein, Albumin")

class Procedures(BaseModel):
    Bronchoscopy: str = Field(..., description="Extract the complete Bronchoscopy Report. Separate findings into three essential components: 1) **Visual/Endoscopic Findings** (location and detailed description of any mass, stricture, inflammation, or bleeding observed); 2) **Procedural Details** (which samples were taken: BAL, Biopsy, Brushings, TBNA, etc.); and 3) **Specimen Results** (the final pathology/histology diagnosis, cytology results, and culture/infection status from all retrieved samples).")
    torachocenthesis: Torachocenthesis

class Paraclinic(BaseModel):
    basic_blood_tests: BasicBloodTests
    specialized_lung_tests: SpecializedLungTests
    immunity_and_serology: ImmunityAndSerology
    functional_tests: FunctionalTests
    procedures: Procedures

class MedicalCase(BaseModel):
    patient_profile: PatientProfile
    history_taking: HistoryTaking
    physical_exam: PhysicalExam
    paraclinic: Paraclinic

# model = ChatVertexAI (
#   model="gemini-2.0-flash",
#   location="europe-north1",
#   base_url="https://api.avalai.ir/v1/chat/completions",
#   api_key="aa-P7j1uxWtVqqQRUoGGwZMqr8g7bI0azTMdDHhY9nNSdOYz23s",
# )

model = init_chat_model(
  model="gpt-4o-mini",
  base_url="https://api.avalai.ir/v1",
  api_key="aa-3merXIxJbKqFQqE69uVBXvWAJXVg1OAD7e1Tqq2BttJmJoVj",
)

OPTIMAL_SCENARIO = ["Asthma", "Pneumonia", "COPD", "PTE", "IPF", "PH", "Pleural_Effusion", "ARDS"]

def scenario_creator():
    target_disease = random.choice(OPTIMAL_SCENARIO)
  
    prompt_template = PromptTemplate(
        template="مطابق json زیر با در نظر گرفتن اینکه این موارد در رابطه با بیماری {disease} می‌باشند جوری کامل کن که یک پزشک بتواند با استفاده از این یافته‌ها به تشخیص برسد. به فارسی روان پاسخ یده اما اصطلاخات علمی را ترجمه نکن و به صورت انگلیسی در متن فارسی قرار بده.",
        input_variables=["disease"]
    )
  
    final_prompt = prompt_template.format(disease=f"{target_disease}")

    structured_chat_model = model.with_structured_output(MedicalCase)
  
    try:
        output_pydantic_object = structured_chat_model.invoke(final_prompt)
        
        output_dict = output_pydantic_object.model_dump(by_alias=True)
        
        return output_dict, target_disease

    except Exception as e:
        print(f"Error generating scenario: {e}")
        return None, target_disease
