import getpass
import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from document import documents
import random

from typing import List, Optional
from pydantic import BaseModel, Field

class PatientProfile(BaseModel):
    chief_complaint: str = Field(..., description="Chief Complaint")

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
    question6: Optional[str] = Field(..., description="آیا برنامه واکسن های شما (مثل کزاز و آنفولانزا) کامل و بروز است؟")

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

class MedicalCase(BaseModel):
    patient_profile: PatientProfile
    history_taking: HistoryTaking

model = init_chat_model(
  model="gpt-4o",
  base_url="https://api.avalai.ir/v1",
  api_key="aa-3merXIxJbKqFQqE69uVBXvWAJXVg1OAD7e1Tqq2BttJmJoVj",
)

embedding_model = OpenAIEmbeddings(
    api_key="aa-3merXIxJbKqFQqE69uVBXvWAJXVg1OAD7e1Tqq2BttJmJoVj",
    base_url="https://api.avalai.ir/v1",
)

vector_store = Chroma.from_documents(documents, embedding_model)

retriever = vector_store.as_retriever(
    search_kwargs={
        "k": 20,
    }
)

OPTIMAL_SCENARIO = ["Asthma", "Pneumonia", "COPD", "PTE", "IPF", "PH", "Pleural_Effusion", "ARDS"]

def scenario_creator():
    target_disease = "COPD" 
    
    retrieved_docs = retriever.invoke(
        f"اطلاعات مورد نیاز برای سناریوی کامل بیماری {target_disease}", 
        config={"configurable": {"filter": {"disease": target_disease}}}
    )
    
    context_text = "\n---\n".join([doc.page_content for doc in retrieved_docs])
        
    prompt_template = PromptTemplate(
        template=""" خروجی باید EXACTLY مطابق Schema باشد.
         تمام فیلدها باید مقدار داشته باشند.
         هیچ فیلدی نباید خالی، حذف‌شده، یا به صورت {{}} تولید شود.
         برای هر فیلد، حتی اگر پاسخ "ندارم" است، یک متن کامل و مناسب تولید کن.
         فیلدهای داخلی (nested) نیز باید کامل باشند.

        شما یک سیستم تولید سناریوی پزشکی بسیار دقیق هستید. وظیفه شما این است که بر اساس «متون رفرنس» که در اختیار شما قرار داده شده است، یک سناریوی کامل و معتبر برای بیماری {disease} تولید کنید.
        
        دستورالعمل‌های تولید:
        1.  بخش شرح حال (History Taking): پاسخ‌ها باید به -فارسی روان- ، به صورت اول شخص مفرد (از زبان بیمار) و توصیفی تولید شوند. از تکرار تحلیل‌های پزشکی، درصدها یا بازه‌های زمانی خودداری کنید.
        2.  بخش معاینه فیزیکی (Physical Exam): پاسخ‌ها باید به -انگلیسی- ، به صورت سوم شخص مفرد (از زبان معاینه‌کننده) و توصیفی/علمی تولید شوند.
        3.  بخش پاراکلینیک (Paraclinic): پاسخ‌ها باید به فارسی باشند.
        4.  حذف کامل تحلیل و درصد: به هیچ وجه هیچ‌کدام از اطلاعات آماری، درصدها (مانند 80%، 20%)، بازه‌های زمانی (مانند 1 تا 7 روز) یا تحلیل‌های پزشکی (مانند risk factor) موجود در «متون رفرنس» را در خروجی JSON تکرار نکنید.
        5.  تولید مقادیر واقعی: از داده‌های رفرنس برای انتخاب یک مقدار واقعی و قطعی برای این بیمار خاص استفاده کنید.
        
        بیماری هدف: {disease}
        
        متون رفرنس (Context):
        ---
        {context}
        ---
        
        خروجی JSON مورد انتظار (بر اساس Pydantic Schema):
        {{
  "patient_profile": {{
    "chief_complaint": ""
  }},
  "history_taking": {{
    "present_illness": {{ ... تمام ۱۰ سؤال ... }},
    "past_medical_history": {{
        "question1": {{
            "question1a": "",
            "question1b": ""
        }},
        "question2": {{
            "question2a": "",
            "question2b": ""
        }},
        "question3": "",
        "question4": "",
        "question5": "",
        "question6": ""
    }},
    "drug_history": {{ ... }},
    "allergies": {{ ... }},
    "family_history": {{ ... }},
    "social_history": {{ ... }},
    "ros": {{ ... }}
  }}
}}""",
        
        input_variables=["disease", "context"] 
    )
    
    final_prompt = prompt_template.format(disease=f"{target_disease}", context=context_text)

    structured_chat_model = model.with_structured_output(MedicalCase, strict=True)
  
    try:
        output_pydantic_object = structured_chat_model.invoke(final_prompt)
        
        output_dict = output_pydantic_object.model_dump(by_alias=True)
        
        return output_dict, target_disease

    except Exception as e:
        print(f"Error generating scenario: {e}")
        return None, target_disease
    
print(scenario_creator())