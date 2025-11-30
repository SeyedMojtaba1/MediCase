import {ChangeDetectorRef, Component, signal} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {APP_CONFIG} from '../../config/app.config';
import {NgClass} from '@angular/common';
import {Router, RouterLink} from '@angular/router';
import {Master} from '../../core/services/master';
import Questions from '../../../../public/json/senario.json'
import Log from '../../../../public/json/student_log.json'
import confetti from 'canvas-confetti';

interface Disease {
  name: string;
  checked: boolean;
}

interface Section {
  id: number;
  title: string;
  icon: string;
}

interface Question {
  id: string;
  title: string;
  answer: string;
  open: boolean;
  visible: boolean;
  answer_time: string;
}


@Component({
  selector: 'app-scenario',
  imports: [
    FormsModule,
    NgClass,
    RouterLink,
  ],
  templateUrl: './scenario.html',
  styleUrl: './scenario.css'
})
export class Scenario {

  diseaseCodeMap: Record<string, string> = {
    "Asthma": "disease1",
    "Pneumonia": "disease2",
    "COPD": "disease3",
    "PTE": "disease4",
    "IPF": "disease5",
    "PH": "disease6",
    "Pleural_Effusion": "disease7",
    "ARDS": "disease8"
  };

  imageUrl = signal('https://elmkhah.ir/wp-content/uploads/2025/11/photo_2025-11-28_16-52-45.jpg')

  timer = signal('15:00')
  logo = APP_CONFIG.logoURL;
  backgroundImage = 'assets/bg.jpg';
  diseases: Disease[] = [];
  sections: Section[] = [];
  activeSection: number | null = 1
  clickSound = new Audio('sounds/click.mp3');
  successSound = new Audio('sounds/success.mp3');
  isVideoLoading = signal(false)
  questions: Question[] = [];
  // لیست متن سوالا
  questionText: any = Questions
  //لیست دیتا های ai
  data: any
  //لیست دیتایی که قراره بفرستیم
  log: any = Log
  physicalExamBySection: Record<string, Question[]> = {};
  questionsBySection: Record<string, Question[]> = {};
  paraclinicBySection: Record<string, Question[]> = {};
  showDifferentialDiagnosisModal: boolean = false;
  differentialDiagnosisStage: number = 1;
  selectedDifferentialDiseases: Disease[] = [];
  finalDiagnosis: string | null = null;
  sectionMedia: any = {
    cardiovascular_system: {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/11/video_2025-11-29_14-11-16.mp4'
    },
    head_and_neck: {
      type: 'image',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/11/photo_2025-11-28_16-52-45.jpg'
    },
  };

  mediaType: 'image' | 'video' = 'image';
  mediaUrl: string = 'images/default.jpg';

  protected readonly APP_CONFIG = APP_CONFIG;
  protected readonly sessionStorage = sessionStorage;
  protected readonly Log = Log;
  protected readonly console = console;
  private timeLeft = 15 * 60;
  private intervalId: any;

  constructor(public router: Router, public changeDetectorRef: ChangeDetectorRef, public master: Master) {
  }

  ngOnInit() {
    this.loadDiseases();
    this.loadSections();
    this.startTimer();


    this.master.pulmonologyScenarioRetrieve('XU42DWT9ZX').subscribe({
      next: data => {
        localStorage.setItem('data', JSON.stringify(data));
      },
      complete: () => {
        const raw = localStorage.getItem('data');

        if (raw) {
          const parsed = JSON.parse(raw);
          this.data = parsed.scenario || '';
        } else {
          this.data = '';
        }

        this.buildQuestions()
        this.buildPhysicalExamQuestions()
        this.buildParaclinicQuestions()
        this.changeDetectorRef.detectChanges();
      }
    })
  }

  playClick() {
    this.clickSound.currentTime = 0;
    this.clickSound.play();
  }

  playSuccess() {
    this.successSound.currentTime = 0;
    this.successSound.play();
  }

  loadDiseases() {
    this.diseases = [
      {name: 'Asthma', checked: false},
      {name: 'Pneumonia', checked: false},
      {name: 'COPD', checked: false},
      {name: 'PTE', checked: false},
      {name: 'IPF', checked: false},
      {name: 'PH', checked: false},
      {name: 'Pleural_Effusion', checked: false},
      {name: 'ARDS', checked: false},
    ];
  }

  loadSections() {
    this.sections = [
      {id: 1, title: 'اطلاعات بیمار', icon: 'pi pi-id-card'},
      {id: 2, title: 'شرح حال', icon: 'pi pi-list'},
      {id: 3, title: 'معاینه فیزیکی', icon: 'pi pi-heart'},
      {id: 4, title: 'پاراکلینیک', icon: 'pi pi-folder'},
      {id: 5, title: 'تشخیص افتراقی', icon: 'pi pi-pencil'},
      {id: 6, title: 'درمان', icon: 'pi pi-lock'},
    ];
  }


  // ... داخل کلاس Scenario

// ...
  selectSection(section: Section) {
    if (section.id === 5) {
      this.showDifferentialDiagnosisModal = true;
      this.differentialDiagnosisStage = 1; // همیشه از مرحله ۱ شروع می‌شود
      this.playClick();
      return;
    }

    // ... (سایر منطق‌ها برای ID 6 و غیره)
    // ...

    this.activeSection = section.id;
    // this.playSuccess();
  }

  // مدیریت انتخاب/حذف بیماری در مرحله ۱
  toggleDiseaseSelection(disease: Disease) {
    const index = this.selectedDifferentialDiseases.findIndex(d => d.name === disease.name);

    if (index > -1) {
      // حذف بیماری اگر از قبل انتخاب شده بود
      this.selectedDifferentialDiseases.splice(index, 1);
    } else if (this.selectedDifferentialDiseases.length < 4) {
      // افزودن بیماری اگر کمتر از ۴ مورد انتخاب شده بود
      this.selectedDifferentialDiseases.push(disease);
    }
  }

  // رفتن از مرحله ۱ به مرحله ۲
  goToFinalDiagnosisStage() {
    if (this.selectedDifferentialDiseases.length >= 2 && this.selectedDifferentialDiseases.length <= 4) {
      this.differentialDiagnosisStage = 2;
      this.playClick();
    } else {
      alert('لطفاً 2-4 بیماری را انتخاب کنید.');
    }
  }

  // انتخاب تشخیص نهایی در مرحله ۲
  setFinalDiagnosis(diseaseName: string) {
    this.finalDiagnosis = diseaseName;
    this.playClick();
  }

// ...

  // بستن پاپ‌آپ (به همراه ریست کردن مرحله)
  closeDifferentialDiagnosisModal() {
    this.showDifferentialDiagnosisModal = false;
    this.differentialDiagnosisStage = 1;
    this.selectedDifferentialDiseases = [];
    this.finalDiagnosis = null;
    this.playClick();
  }

  startTimer() {
    this.intervalId = setInterval(() => {
      if (this.timeLeft <= 0) {
        clearInterval(this.intervalId);
        this.timer.set('00:00')
        return;
      }

      this.timeLeft--;

      const minutes = Math.floor(this.timeLeft / 60);
      const seconds = this.timeLeft % 60;

      this.timer.set(`${this.pad(minutes)}:${this.pad(seconds)}`);
    }, 1000);
  }

// ... داخل کلاس Scenario

  setTime(path: any) {
    path = this.timer();
    this.playClick()
  }

  pad(val: number) {
    return val < 10 ? "0" + val : val.toString();
  }

  buildQuestions() {
    const history = this.questionText["history_taking"]; // سؤالات (عنوان‌ها)
    const answers = this.data.history_taking;            // پاسخ‌ها
    const logs = this.log.history_taking;                // زمان مشاهده

    this.questionsBySection = {}; // initialize

    for (const sectionName in history) {

      const sectionQuestions = history[sectionName];
      const aiSection = answers[sectionName];
      const logSection = logs[sectionName];

      this.questionsBySection[sectionName] = [];

      for (const key in sectionQuestions) {
        const title = sectionQuestions[key];
        const answer = aiSection ? aiSection[key] : '';
        const log = logSection ? logSection[key] : 'False'; // 👈 استخراج لاگ برای سطح 2

        if (typeof answer === 'object' && answer !== null && !Array.isArray(answer)) {
          // حالت تو در تو (مثل question1)
          for (const subKey in answer) {
            const subTitle = sectionQuestions[key][subKey];
            // 👈 استخراج لاگ برای سطح 3
            const subLog = (typeof log === 'object' && log !== null) ? log[subKey] : 'False';

            this.questionsBySection[sectionName].push({
              id: `${key}-${subKey}`,
              title: subTitle,
              answer: answer[subKey],
              answer_time: subLog, // استفاده از لاگ سطح 3
              open: false,
              visible: true
            });
          }

        } else {
          // حالت تک سطحی (مثل question6 در Past Medical History)
          this.questionsBySection[sectionName].push({
            id: key,
            title: title,
            answer: Array.isArray(answer) ? answer.join(' | ') : answer,
            answer_time: log, // استفاده از لاگ سطح 2
            open: false,
            visible: true
          });
        }
      }
    }
  }

  buildPhysicalExamQuestions() {
    // بررسی وجود داده
    if (!this.data || !this.data.physical_exam || !this.log || !this.log.physical_exam) return;

    const examText = this.questionText["physical_exam"]; // عناوین معاینه (از senario.json)
    const examAnswers = this.data.physical_exam;        // پاسخ‌ها (از AI)
    const examLogs = this.log.physical_exam;            // زمان مشاهده

    this.physicalExamBySection = {};

    for (const systemName in examAnswers) {

      const systemText = examText[systemName];
      const systemAnswers = examAnswers[systemName];
      const systemLogs = examLogs[systemName];

      this.physicalExamBySection[systemName] = [];

      for (const sectionKey in systemAnswers) {

        const answerL2 = systemAnswers[sectionKey];
        const logL2 = systemLogs ? systemLogs[sectionKey] : 'False'; // لاگ در سطح 2

        if (typeof answerL2 === 'object' && answerL2 !== null && !Array.isArray(answerL2)) {

          const textL2 = systemText[sectionKey];

          for (const itemKey in answerL2) {

            const titleL3 = textL2 ? textL2[itemKey] : itemKey;
            const answerL3 = answerL2[itemKey];

            const logL3 = (typeof logL2 === 'object' && logL2 !== null) ? logL2[itemKey] : 'False';

            this.physicalExamBySection[systemName].push({
              id: `${sectionKey}-${itemKey}`,
              title: titleL3,
              answer: Array.isArray(answerL3) ? answerL3.join(' | ') : answerL3,
              answer_time: logL3,
              open: false,
              visible: true
            });
          }
        } else {

          const textL2 = systemText ? systemText[sectionKey] : sectionKey; // عنوان سطح 2

          this.physicalExamBySection[systemName].push({
            id: sectionKey,
            title: textL2,
            answer: Array.isArray(answerL2) ? answerL2.join(' | ') : answerL2,
            answer_time: logL2,
            open: false,
            visible: true
          });
        }
      }
    }
  }

  buildParaclinicQuestions() {
    if (!this.data || !this.data.paraclinic || !this.log || !this.log.paraclinic) return;

    const paraclinicText = this.questionText["paraclinic"]; // عناوین (از senario.json)
    const paraclinicAnswers = this.data.paraclinic;        // پاسخ‌ها (از AI)
    const paraclinicLogs = this.log.paraclinic;            // زمان مشاهده

    this.paraclinicBySection = {}; // مقداردهی اولیه

    // سطح ۱: دسته‌بندی‌ها (مثل basic_blood_tests، functional_tests)
    for (const categoryName in paraclinicAnswers) {

      const categoryText = paraclinicText[categoryName];
      const categoryAnswers = paraclinicAnswers[categoryName];
      const categoryLogs = paraclinicLogs[categoryName];

      this.paraclinicBySection[categoryName] = [];

      // سطح ۲: تست‌های اصلی (مثل CBC، Spirometry، Bronchoscopy)
      for (const testKey in categoryAnswers) {

        const answerL2 = categoryAnswers[testKey]; // پاسخ در سطح 2
        const logL2 = categoryLogs ? categoryLogs[testKey] : 'False'; // لاگ در سطح 2

        // **حالت تو در تو (سطح ۳ - تست‌های عملکردی یا Thoracocentesis)**
        if (typeof answerL2 === 'object' && answerL2 !== null && !Array.isArray(answerL2)) {

          const textL2 = categoryText[testKey]; // زیربخش‌های عنوان (مثلاً: FEV1, FVC)

          // پیمایش آیتم‌های سطح ۳ (کلیدهای داخلی)
          for (const itemKey in answerL2) {

            // تلاش برای پیدا کردن عنوان فارسی، در غیر این صورت از کلید انگلیسی استفاده کن
            const titleL3 = textL2 ? textL2[itemKey] : itemKey;
            const answerL3 = answerL2[itemKey];

            // لاگ سطح ۳: لاگ والد (logL2) باید یک شیء باشد تا بتوان به زیرکلید آن دسترسی داشت
            const logL3 = (typeof logL2 === 'object' && logL2 !== null) ? logL2[itemKey] : 'False';

            this.paraclinicBySection[categoryName].push({
              id: `${testKey}-${itemKey}`, // مثال: torachocenthesis-serum
              title: titleL3,
              answer: Array.isArray(answerL3) ? answerL3.join(' | ') : answerL3,
              answer_time: logL3,
              open: false,
              visible: true
            });
          }
        }
        // **حالت مستقیم (سطح ۲ - تست‌های ساده مانند BMP یا Bronchoscopy)**
        else {

          const textL2 = categoryText ? categoryText[testKey] : testKey; // عنوان سطح 2

          this.paraclinicBySection[categoryName].push({
            id: testKey,
            title: textL2,
            answer: Array.isArray(answerL2) ? answerL2.join(' | ') : answerL2,
            answer_time: logL2,
            open: false,
            visible: true
          });
        }
      }
    }
  }


  // ... داخل کلاس Scenario

// ...
  handleQuestionClick(question: Question, systemName: string, sectionCategory: 'history_taking' | 'physical_exam' | 'paraclinic') {
    this.playClick();

    const media = this.sectionMedia[systemName];
    if (media) {
      this.mediaType = media.type;
      this.mediaUrl = media.url;
      if (this.mediaType == 'video')
        this.isVideoLoading.set(true)
    }

    if (!question.open) {

      const currentTime = this.timer();
      question.answer_time = currentTime;

      // --- به‌روزرسانی JSON نهایی (this.log) ---
      const [key, subKey] = question.id.split('-');

      // 1. اطمینان از وجود دسته اصلی (history_taking یا physical_exam)
      const logCategory = this.log[sectionCategory];

      // 2. اطمینان از وجود زیربخش (مثلاً past_medical_history، ROS)
      if (logCategory && !logCategory[systemName]) {
        logCategory[systemName] = {}; // اگر زیربخش در لاگ وجود ندارد، آن را به عنوان یک شیء خالی تعریف کن.
      }

      const logSection = logCategory[systemName]; // حالا مطمئنیم که یک شیء است

      if (subKey) {
        // حالت زیرسوال (مثال: question1-question1a)

        // 3. اطمینان از وجود شیء والد (question1)
        if (!logSection[key] || typeof logSection[key] !== 'object') {
          // اگر question1 وجود ندارد یا مقدار False دارد، آن را به شیء تبدیل کن
          logSection[key] = {};
        }

        logSection[key][subKey] = currentTime;

      } else {
        // حالت سوال عادی (مثال: question6 یا question10)

        if (logSection) {
          logSection[key] = currentTime;
        }
      }
    }

    question.open = true;
    this.changeDetectorRef.detectChanges();
  }

  finishScenario() {
    if (!this.finalDiagnosis) {
      alert('لطفاً تشخیص نهایی را انتخاب کنید.');
      return;
    }

    const currentTime = this.timer(); // زمان فعلی سناریو

    // --- ۱. Differential Diagnosis با ۸ کلید ثابت ---
    this.log.differential_diagnosis = {};

    // اول همه ۸ بیماری را به false مقداردهی کن
    Object.values(this.diseaseCodeMap).forEach(code => {
      this.log.differential_diagnosis[code] = false;
    });

    // برای بیماری‌هایی که انتخاب شده‌اند → زمان درج کن
    this.selectedDifferentialDiseases.forEach(disease => {
      const code = this.diseaseCodeMap[disease.name];
      if (code) {
        this.log.differential_diagnosis[code] = currentTime;
      }
    });

// --- ۲. Final Diagnosis ---
    this.log.final_diagnosis = {};

    const finalCode = this.diseaseCodeMap[this.finalDiagnosis];

// خروجی نهایی:  { "disease4": "12:20" }
    if (finalCode) {
      this.log.final_diagnosis[finalCode] = currentTime;
    }

    // --- ۳. اقدامات بعد ---
    alert(`سناریو به پایان رسید. تشخیص نهایی: ${this.finalDiagnosis}`);

    const treatmentSection = this.sections.find(s => s.id === 6);
    if (treatmentSection) {
      treatmentSection.title = 'درمان (پایان یافته)';
      this.activeSection = 5;
    }

    this.master.pulmonologyScenarioFeedbackCreate("BP3NOKL8YF", this.log).subscribe({});

    this.showDifferentialDiagnosisModal = false;
    this.fireConfetti();
    this.router.navigateByUrl('/scenarioinit');
    this.playSuccess();
    this.changeDetectorRef.detectChanges();
  }

  fireConfetti() {
    confetti({
      particleCount: 150,
      spread: 80,
      origin: {y: 0.6}
    });
  }
}
