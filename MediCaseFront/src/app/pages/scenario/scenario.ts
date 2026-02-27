import {ChangeDetectorRef, Component, ElementRef, signal, ViewChild} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {APP_CONFIG} from '../../config/app.config';
import {NgClass} from '@angular/common';
import {ActivatedRoute, Router, RouterLink} from '@angular/router';
import {Master} from '../../core/services/master';
import Questions from '../../../../public/json/senario.json'
import Log from '../../../../public/json/student_log.json'
import Data from '../../../../public/json/t.json'
import confetti from 'canvas-confetti';
import {VIDEO_MAPPING} from './assets'

interface Disease {
  name: string;
  checked: boolean;
}

interface Section {
  id: number;
  title: string;
  icon: string;
}

interface ParaclinicResult {
  title: string;
  answer: string;
  normalValue?: string;
}

interface Question {
  id: string;
  title: string;
  answer: any;
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

  first_name = signal('')
  last_name = signal('')
  avatar = 'images/jpg/avatar.jpg';
  diseaseCodeMap: Record<string, string> = {
    "Asthma": "disease1",
    "Pneumonia": "disease2",
    "COPD": "disease3",
    "PTE": "disease4",
    "IPF": "disease5",
    "PH": "disease6",
  };
  @ViewChild('videoPlayer') videoElementRef!: ElementRef<HTMLVideoElement>;
  imageUrl = signal('https://elmkhah.ir/wp-content/uploads/2025/11/photo_2025-11-28_16-52-45.jpg')
  isMuted = signal(false);
  timer = signal('15:00')
  logo = APP_CONFIG.logoURL;
  backgroundImage = 'assets/bg.jpg';
  diseases: Disease[] = [];
  sections: Section[] = [];
  activeSection: number | null = 1
  clickSound = new Audio('sounds/click.mp3');
  successSound = new Audio('sounds/success.mp3');
  bgsound = new Audio('sounds/bg.mp3');
  isVideoLoading = signal(false)
  sectionOpenState: Record<string, boolean> = {};
  questionText: any = Questions
  data: any
  log: any = Log
  physicalExamBySection: Record<string, Question[]> = {};
  questionsBySection: Record<string, Question[]> = {};
  paraclinicBySection: Record<string, Question[]> = {};
  showExitModal: boolean = false;
  sectionMedia: any = VIDEO_MAPPING
  mediaType: 'image' | 'video' = 'image';
  mediaUrl: string = "https://elmkhah.ir/wp-content/uploads/2025/11/photo_2025-11-28_16-52-45.jpg";
  public code: any;
  public trackingCode: any;
  currentCharacter = signal('young_male');

  showDifferentialDiagnosisModal: boolean = false;
  differentialDiagnosisStage: number = 1;
  finalDiagnosis: string | null = null;
  selectedDifferentialDiseases: any[] = []; // لیستی که بیماری‌های مرحله اول در آن ذخیره می‌شوند
  pleuralAssessmentData = {
    has_effusion: 'false',
    need_aspiration: 'false',
    effusion_type: 'none'
  };
  protected readonly APP_CONFIG = APP_CONFIG;
  protected readonly sessionStorage = sessionStorage;
  protected readonly localStorage = localStorage;
  private timeLeft = 60 * 15;
  private intervalId: any;

  constructor(public router: Router, public changeDetectorRef: ChangeDetectorRef, public master: Master, public route: ActivatedRoute) {
  }

  get filteredInitialDiseases() {
    return this.diseases.filter(d => d.name !== 'Pleural_Effusion');
  }

  get defaultCharacterImage(): string {
    const character = this.currentCharacter();
    return this.sectionMedia[character]?.default_image || 'https://elmkhah.ir/wp-content/uploads/2025/11/photo_2025-11-28_16-52-45.jpg';
  }

  ngOnInit() {

    this.code = this.route.snapshot.paramMap.get('code')!;
    this.trackingCode = this.code
    this.loadProfile();

    this.loadDiseases();
    this.loadSections();
    this.startTimer();

    this.setSectionsName();

    document.addEventListener('click', () => {
      if (this.bgsound.paused) {
        this.bgsound.loop = true;
        this.bgsound.muted = this.isMuted();
        this.bgsound.volume = 0.6;
        this.bgsound.play().catch(err => console.log(err));
      }
    }, {once: true});


    this.master.pulmonologyScenarioRetrieve(this.trackingCode).subscribe({
      next: data => {
        localStorage.setItem('data', JSON.stringify(data));
        this.updateCharacterType(data);
      },
      error: err => {
        this.data = Data
        console.log(this.data);
        this.buildQuestions()
        this.buildPhysicalExamQuestions()
        this.buildParaclinicQuestions()
        this.changeDetectorRef.detectChanges();
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

  updateCharacterType(apiData: any) {
    const profile = apiData.scenario.patient_profile.personal_information;

    // ۱. استخراج عدد از رشته سن (مثلا تبدیل "39 ساله" به 39)
    const ageNumber = parseInt(profile.age.replace(/[^0-9]/g, ''));

    // ۲. تشخیص جنسیت (مرد یا زن)
    const gender = profile.gender; // "مرد" یا "زن"

    let type = '';

    if (gender === 'مرد') {
      type = ageNumber < 50 ? 'young_male' : 'old_male';
    } else if (gender === 'زن') {
      type = ageNumber < 50 ? 'young_female' : 'old_female';
    } else {
      // مقدار پیش‌فرض در صورت بروز خطا
      type = 'young_male';
    }

    // ۳. آپدیت کردن وضعیت برنامه
    this.currentCharacter.set(type);


    this.mediaUrl = this.defaultCharacterImage;
    this.mediaType = 'image';
    this.changeDetectorRef.detectChanges();

    console.log(`Character set to: ${type} based on Age: ${ageNumber} and Gender: ${gender}`);
  }

  setHasEffusion(value: boolean) {
    this.pleuralAssessmentData.has_effusion = value ? 'true' : 'false';
    if (value) {
      this.differentialDiagnosisStage = 4;
    } else {
      this.pleuralAssessmentData.need_aspiration = 'false';
      this.pleuralAssessmentData.effusion_type = 'none';
      this.finishAndSaveLog();
    }
  }

  setNeedAspiration(value: boolean) {
    this.pleuralAssessmentData.need_aspiration = value ? 'true' : 'false';
    if (value) {
      this.differentialDiagnosisStage = 5;
    } else {
      this.pleuralAssessmentData.effusion_type = 'none';
      this.finishAndSaveLog();
    }
  }

  setEffusionType(type: string) {
    this.pleuralAssessmentData.effusion_type = type;
    this.finishAndSaveLog();
  }

  finishAndSaveLog() {
    this.log.final_diagnosis = {
      "disease": this.finalDiagnosis
    };
    this.log.pleural_effusion_assessment = {
      "has_effusion": this.pleuralAssessmentData.has_effusion,
      "need_aspiration": this.pleuralAssessmentData.need_aspiration,
      "effusion_type": this.pleuralAssessmentData.effusion_type
    };

    console.log("Log Saved:", this.log);
    this.showDifferentialDiagnosisModal = false;
    console.log(this.log);
    this.master.pulmonologyScenarioFeedbackCreate(this.trackingCode, this.log).subscribe({
      next: data => {
        this.router.navigateByUrl('/dashboard/s/stat');
      },
      error: err => {
        alert("خطایی وجود داشت. مجددا تلاش کنید")
      }
    })
  }

  closeDifferentialDiagnosisModal() {
    this.showDifferentialDiagnosisModal = false;
    this.differentialDiagnosisStage = 1;
  }

  selectFinalAndNext(diseaseName: string) {
    this.finalDiagnosis = diseaseName;
    this.differentialDiagnosisStage = 3; // مرحله ۳: سوال "آیا افیوژن دارد؟"
  }

  toggleDisease(disease: any) {
    const index = this.selectedDifferentialDiseases.indexOf(disease);
    if (index > -1) {
      this.selectedDifferentialDiseases.splice(index, 1);
    } else {
      if (this.selectedDifferentialDiseases.length < 4) {
        this.selectedDifferentialDiseases.push(disease);
      }
    }
  }

  playClick() {
    this.clickSound.currentTime = 0;
    this.clickSound.volume = 0.3
    this.clickSound.play();
  }

  isArray(obj: any): boolean {
    return Array.isArray(obj);
  }

  playSuccess() {
    this.clickSound.currentTime = 0;
    this.clickSound.volume = 0.3
    this.clickSound.play();
  }

  setSectionsName() {
    const allSections = [
      'present_illness',
      'past_medical_history',
      'drug_history',
      'allergies',
      'family_history',
      'social_history',
      'ros',

      'general_appearance',
      'vital_signs',
      'head_and_neck',
      'respiratory_system',
      'cardiovascular_system',
      'abdominal_system',
      'neurological',
      'musculoskeletal_system',

      'basic_blood_tests',
      'specialized_lung_tests',
      'immunity_and_serology',
      'functional_tests',
      'simple_imaging',
      'advanced_imaging',
      'procedures'
    ];

    allSections.forEach(key => {
      this.sectionOpenState[key] = false;
    });
  }

  toggleSection(sectionKey: string) {
    this.sectionOpenState[sectionKey] = !this.sectionOpenState[sectionKey];
    this.playSuccess()
  }

  loadDiseases() {
    this.diseases = [
      {name: 'Asthma', checked: false},
      {name: 'Pneumonia', checked: false},
      {name: 'COPD', checked: false},
      {name: 'PTE', checked: false},
      {name: 'IPF', checked: false},
      {name: 'PH', checked: false},
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
      {id: 7, title: 'بازگشت', icon: 'pi pi-sign-out'}

    ];
  }

  toggleMute() {
    this.isMuted.set(!this.isMuted());

    // اعمال روی تمام صداها
    this.bgsound.muted = this.isMuted();
    // this.clickSound.muted = this.isMuted();
    // this.successSound.muted = this.isMuted();

    // اعمال روی ویدیو (در صورت وجود)
    if (this.videoElementRef?.nativeElement) {
      this.videoElementRef.nativeElement.muted = this.isMuted();
    }
  }

  selectSection(section: Section) {
    if (section.id === 5) {
      this.showDifferentialDiagnosisModal = true;
      this.differentialDiagnosisStage = 1;
      this.playClick();
      return;
    } else if (section.id === 7) {
      this.showExitModal = true;
      this.playClick();
      return;
    }

    this.activeSection = section.id;

    // ۱. پیدا کردن مدیا بر اساس تنظیمات assets.ts
    this.setSectionMedia(section);

    // ۲. فقط اگر مدیایی پیدا نشد یا برای اطمینان از بخش‌های خاص، مقداردهی شود
    // این بلوک را حذف یا اصلاح کنید تا ویدیوهای پروفایل (بخش ۱) حذف نشوند
    if (!this.mediaUrl || this.mediaUrl === 'https://elmkhah.ir/wp-content/uploads/2025/11/photo_2025-11-28_16-52-45.jpg') {
      if (section.id === 1 || section.id === 4) {
        this.mediaType = 'image';
        this.mediaUrl = this.defaultCharacterImage;
      }
    }

    this.changeDetectorRef.detectChanges();

    // کنترل صدای ویدیو
    setTimeout(() => {
      if (this.videoElementRef?.nativeElement) {
        this.videoElementRef.nativeElement.muted = this.isMuted();
      }
    }, 100);
  }

  setSectionMedia(section: Section) {

    let media;
    const defaultImageUrl = 'https://elmkhah.ir/wp-content/uploads/2025/11/photo_2025-11-28_16-52-45.jpg';

    // نگاشت id بخش به کلیدهای media
    const sectionMediaMap: Record<number, string> = {
      1: 'patient_profile', // اطلاعات بیمار
      2: 'history_taking', // شرح حال
      3: 'physical_exam', // معاینه فیزیکی
      4: 'paraclinic', // پاراکلینیک
      5: 'differential_diagnosis', // تشخیص افتراقی
      6: 'treatment' // درمان
    };

    // برای بخش‌هایی که مدیا ندارند از پیش‌فرض استفاده کن
    const mediaKey = sectionMediaMap[section.id];

    const characterMedia = this.sectionMedia[this.currentCharacter()];
    if (characterMedia && mediaKey) {
      media = characterMedia[mediaKey];
    }


    // --- مدیریت URL و نوع مدیا ---
    let newMediaUrl = media ? media.url : defaultImageUrl;
    let newMediaType = media ? media.type : 'image';

    // منطق لودینگ برای ویدیو
    const mediaIsChangingToNewVideo = (newMediaType === 'video' && newMediaUrl !== this.mediaUrl);

    if (newMediaType === 'video') {
      if (mediaIsChangingToNewVideo) {
        this.isVideoLoading.set(true);
      }
    } else {
      this.isVideoLoading.set(false);
    }

    // به‌روزرسانی پراپرتی‌ها
    this.mediaType = newMediaType as 'image' | 'video';
    this.mediaUrl = newMediaUrl;

    // مدیریت ویدیو
    if (mediaIsChangingToNewVideo && this.videoElementRef) {
      this.changeDetectorRef.detectChanges();
      this.videoElementRef.nativeElement.load();
    }

    this.playSuccess();
  }

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

  goToFinalDiagnosisStage() {
    if (this.selectedDifferentialDiseases.length >= 2 && this.selectedDifferentialDiseases.length <= 4) {
      this.differentialDiagnosisStage = 2;
      this.playClick();
    } else {
      alert('لطفاً 2-4 بیماری را انتخاب کنید.');
    }
  }

  setFinalDiagnosis(diseaseName: string) {
    this.finalDiagnosis = diseaseName;
    this.playClick();
  }

  closeExitModal() {
    this.showExitModal = false;
    this.playClick();
  }

  startTimer() {
    this.intervalId = setInterval(() => {

      if (this.timeLeft <= 0) {
        clearInterval(this.intervalId);
        this.timeLeft = 0;
        this.timer.set('00:00');

        this.showDifferentialDiagnosisModal = true;
        this.changeDetectorRef.detectChanges();
        return;
      }

      this.timeLeft--;

      const minutes = Math.floor(this.timeLeft / 60);
      const seconds = this.timeLeft % 60;

      this.timer.set(`${this.pad(minutes)}:${this.pad(seconds)}`);

    }, 1000);
  }

  pad(val: number) {
    return val < 10 ? "0" + val : val.toString();
  }

  buildQuestions() {
    const history = this.questionText["history_taking"];
    const answers = this.data.history_taking;
    const logs = this.log.history_taking;

    this.questionsBySection = {};

    for (const sectionName in history) {
      const sectionQuestions = history[sectionName];
      const aiSection = answers[sectionName];
      const logSection = logs ? logs[sectionName] : null;

      this.questionsBySection[sectionName] = [];

      for (const key in sectionQuestions) {
        const title = sectionQuestions[key];
        const answer = aiSection ? aiSection[key] : '';
        const logValue = logSection ? logSection[key] : 'False';

        if (typeof answer === 'object' && answer !== null && !Array.isArray(answer)) {
          for (const subKey in answer) {
            const subTitle = sectionQuestions[key][subKey];
            // بررسی اینکه آیا لاگ هم ساختار درختی دارد یا در فایل جدید تخت شده است
            const subLog = (typeof logValue === 'object' && logValue !== null)
              ? logValue[subKey]
              : logValue;

            this.questionsBySection[sectionName].push({
              id: `${key}-${subKey}`,
              title: subTitle,
              answer: answer[subKey],
              answer_time: subLog || 'False',
              open: false,
              visible: true
            });
          }
        } else {
          this.questionsBySection[sectionName].push({
            id: key,
            title: title,
            answer: Array.isArray(answer) ? answer.join(' | ') : answer,
            answer_time: typeof logValue === 'string' ? logValue : 'False',
            open: false,
            visible: true
          });
        }
      }
    }
  }

  buildPhysicalExamQuestions() {
    if (!this.data || !this.data.physical_exam || !this.log || !this.log.physical_exam) return;

    const examText = this.questionText["physical_exam"];
    const examAnswers = this.data.physical_exam;
    const examLogs = this.log.physical_exam;

    this.physicalExamBySection = {};

    for (const systemName in examAnswers) {
      const systemText = examText[systemName];
      const systemAnswers = examAnswers[systemName];
      const systemLogs = examLogs ? examLogs[systemName] : null;

      this.physicalExamBySection[systemName] = [];

      for (const sectionKey in systemAnswers) {
        const answerL2 = systemAnswers[sectionKey];
        const logL2 = systemLogs ? systemLogs[sectionKey] : 'False';

        if (typeof answerL2 === 'object' && answerL2 !== null && !Array.isArray(answerL2)) {
          const textL2 = systemText[sectionKey];
          for (const itemKey in answerL2) {
            const titleL3 = textL2 ? textL2[itemKey] : itemKey;
            const answerL3 = answerL2[itemKey];

            // مدیریت ساختار جدید: اگر لاگ تخت شده باشد از همان logL2 استفاده می‌کند
            const logL3 = (typeof logL2 === 'object' && logL2 !== null) ? logL2[itemKey] : logL2;

            this.physicalExamBySection[systemName].push({
              id: `${sectionKey}-${itemKey}`,
              title: titleL3,
              answer: Array.isArray(answerL3) ? answerL3.join(' | ') : answerL3,
              answer_time: logL3 || 'False',
              open: false,
              visible: true
            });
          }
        } else {
          const textL2 = systemText ? systemText[sectionKey] : sectionKey;
          this.physicalExamBySection[systemName].push({
            id: sectionKey,
            title: textL2,
            answer: Array.isArray(answerL2) ? answerL2.join(' | ') : answerL2,
            answer_time: typeof logL2 === 'string' ? logL2 : 'False',
            open: false,
            visible: true
          });
        }
      }
    }
  }

  handleQuestionClick(question: Question, systemName: string, sectionCategory: 'history_taking' | 'physical_exam' | 'paraclinic') {
    this.playClick();

    // ۱. مدیریت مدیا (بدون تغییر نسبت به نسخه سالم قبلی شما)
    const currentCharacter = this.currentCharacter();
    const characterMedia = (VIDEO_MAPPING as any)[currentCharacter];
    let media = characterMedia ? (characterMedia[`${systemName}-${question.id}`] || characterMedia[systemName]) : null;
    if (media) {
      this.mediaUrl = media.url;
      this.mediaType = media.type || 'video';
      if (this.mediaType === 'video' && this.videoElementRef) this.videoElementRef.nativeElement.load();
    }

    // ۲. اصلاح ثبت زمان در لاگ - منطق جدید و دقیق
    if (question.answer_time === 'False' || question.answer_time === 'false') {
      const currentTime = this.timer();
      question.answer_time = currentTime;

      // پیدا کردن بخش مربوطه در فایل لاگ
      const section = this.log[sectionCategory];
      if (section && section[systemName]) {
        const logTarget = section[systemName];

        // الف) اگر ID سوال ترکیبی است (مثل torachonthesis-Fluid یا question1-question1a)
        if (question.id.includes('-')) {
          const parts = question.id.split('-');
          let current = logTarget;

          // پیمایش تا یک مرحله قبل از کلید نهایی
          for (let i = 0; i < parts.length - 1; i++) {
            if (current[parts[i]] && typeof current[parts[i]] === 'object') {
              current = current[parts[i]];
            }
          }

          // آپدیت کلید نهایی
          const lastKey = parts[parts.length - 1];
          if (current.hasOwnProperty(lastKey)) {
            current[lastKey] = currentTime;
          } else {
            // اگر پیدا نشد، شاید آیدی سوال فقط شامل کلید نهایی بوده (مثل Fluid-LDH که LDH هدف است)
            this.updateValueInObject(logTarget, lastKey, currentTime);
          }
        }
        // ب) اگر ID ساده است
        else {
          if (logTarget.hasOwnProperty(question.id)) {
            logTarget[question.id] = currentTime;
          } else {
            // جستجوی عمیق فقط در همان شاخه خاص برای اطمینان
            this.updateValueInObject(logTarget, question.id, currentTime);
          }
        }
      }
    }

    question.open = true;
    this.changeDetectorRef.detectChanges();
  }

  getQuestionB(sectionName: string, currentId: string): Question | null {
    if (!currentId.endsWith('a')) return null;

    const baseId = currentId.slice(0, -1); // حذف 'a' از انتهای ID
    const nextId = baseId + 'b';

    return this.questionsBySection[sectionName]?.find(q => q.id === nextId) || null;
  }

  finishScenario() {
    if (!this.finalDiagnosis) {
      alert('لطفاً تشخیص نهایی را انتخاب کنید.');
      return;
    }

    this.playClick();
    this.changeDetectorRef.detectChanges();

  }

  isAnswerArray(answer: any): answer is ParaclinicResult[] {
    return Array.isArray(answer);
  }

  buildParaclinicQuestions() {
    if (!this.data || !this.data.paraclinic || !this.log || !this.log.paraclinic) return;

    const paraclinicText = this.questionText["paraclinic"];
    const paraclinicAnswers = this.data.paraclinic;
    const paraclinicLogs = this.log.paraclinic;

    this.paraclinicBySection = {};

    for (const categoryName in paraclinicAnswers) {
      const categoryText = paraclinicText[categoryName];
      const categoryAnswers = paraclinicAnswers[categoryName];
      const categoryLogs = paraclinicLogs ? paraclinicLogs[categoryName] : null;

      this.paraclinicBySection[categoryName] = [];

      for (const testKey in categoryAnswers) {
        const answerL2 = categoryAnswers[testKey];
        const logL2 = categoryLogs ? categoryLogs[testKey] : 'False';

        let finalTitle = (categoryText && categoryText[testKey]) ?
          (typeof categoryText[testKey] === 'string' ? categoryText[testKey] : testKey) :
          testKey.replace(/_/g, ' ');

        let finalAnswer: any;

        // تشخیص اینکه آیا داده باید به صورت جدولی نمایش داده شود یا خیر
        if (typeof answerL2 === 'object' && answerL2 !== null) {
          if (categoryName === 'basic_blood_tests') {
            finalAnswer = this.processBasicBloodTests(answerL2, categoryText[testKey], testKey);
          } else {
            // برای سایر موارد تودرتو مثل Imaging و Procedures
            finalAnswer = this.processFlattenedObject(answerL2, categoryText ? categoryText[testKey] : null);
          }
        } else {
          finalAnswer = answerL2;
        }

        this.paraclinicBySection[categoryName].push({
          id: testKey,
          title: finalTitle,
          answer: finalAnswer,
          answer_time: typeof logL2 === 'string' ? logL2 : 'False',
          open: false,
          visible: true
        });
      }
    }
  }

  fireConfetti() {
    confetti({
      particleCount: 150,
      spread: 80,
      origin: {y: 0.6}
    });
  }

  loadProfile() {
    this.master.profile().subscribe({
      next: data => {
        const user = data.body;
        if (user) {
          sessionStorage.setItem('first_name', user.first_name || '');
          sessionStorage.setItem('last_name', user.last_name || '');
          sessionStorage.setItem('personal_number', user.personal_number || '');
          localStorage.setItem('personal_number', user.personal_number || '');
          sessionStorage.setItem('avatar', user.profile_image ?? '');

          this.first_name.set(user.first_name || '');
          this.last_name.set(user.last_name || '');
          this.avatar = user.profile_image
            ? user.profile_image
            : 'images/jpg/avatar.jpg';
        }
      },
      error: err => {
        console.log(err);
      }
    });
  }

  confirmExit() {
    this.router.navigate(['/dashboard/s/stat']);
  }

// تابع کمکی برای آپدیت مقدار در یک شاخه خاص
  private updateValueInObject(obj: any, targetKey: string, newValue: string): boolean {
    if (obj.hasOwnProperty(targetKey)) {
      obj[targetKey] = newValue;
      return true;
    }
    for (const key in obj) {
      if (typeof obj[key] === 'object' && obj[key] !== null) {
        if (this.updateValueInObject(obj[key], targetKey, newValue)) return true;
      }
    }
    return false;
  }

// متد کمکی برای پردازش داده‌های Spirometry
  private processSpirometryData(spirometryData: any, textL2: any): string | ParaclinicResult[] {

    if (!spirometryData.result && !spirometryData.reversibility) {
      return 'داده‌ای موجود نیست';
    }

    let resultString = '';

    if (spirometryData.result && typeof spirometryData.result === 'object') {
      resultString += 'نتایج اسپیرومتری:\n';
      for (const key in spirometryData.result) {
        const value = spirometryData.result[key];
        const label = key.replace('_', ' '); // تبدیل FEV1/FVC_Ratio به FEV1/FVC Ratio
        resultString += `${label}: ${value}\n`;
      }
    }

    // پردازش بخش reversibility
    if (spirometryData.reversibility) {
      resultString += `\nقابلیت برگشت‌پذیری: ${spirometryData.reversibility}`;
    }

    return resultString.trim();
  }

// متد کمکی برای پردازش داده‌های basic_blood_tests
  private processBasicBloodTests(data: any, textL2: any, qId: string): ParaclinicResult[] {
    const results: ParaclinicResult[] = [];
    const normalRanges: { [key: string]: string } = {
      'WBC': '4.0 - 11.0 x10³/µL',
      'RBC': '4.5 - 5.5 (M) / 4.0 - 5.0 (F)',
      'Hb': '13 - 17 (M) / 12 - 15 (F)',
      'HCT': '40% - 50% (M) / 36% - 46% (F)',
      'MCV': '80 - 100 fL',
      'MCH': '27 - 32 pg',
      'Plt': '150,000 - 450,000',
      'FBS': '70 - 100 mg/dL',
      'BUN': '7 - 20 mg/dL',
      'Cr': '0.6 - 1.3 mg/dL',
      'Na': '135 - 145 mEq/L',
      'Potassium': '3.5 - 5.0 mEq/L',
      'ESR': '0 - 20 mm/hr',
      'CRP': 'Below 3.0 mg/L',
      'esr': '0 - 20 mm/hr', // برای اطمینان از حروف کوچک
      'crp': 'Below 3.0 mg/L',
      'ALT': '7-56 U/L',
      'AST': '10-40 U/L',
      'ph': '7.31-7.41',
      'HCO3': '22-28 mEq/L',
      'PCO2': '40-50 mmHg'
    };

    if (typeof data === 'object' && !Array.isArray(data)) {
      for (const itemKey in data) {
        let title = (textL2 && textL2[itemKey]) ? textL2[itemKey] : itemKey;
        results.push({
          title: title,
          answer: Array.isArray(data[itemKey]) ? data[itemKey].join(' | ') : data[itemKey],
          normalValue: normalRanges[itemKey] || '-'
        });
      }
    } else if (typeof data === 'string' || typeof data === 'number') {
      // حالا qId از ورودی تابع گرفته می‌شود
      const title = (textL2 && textL2[qId]) ? textL2[qId] : qId;
      results.push({
        title: title,
        answer: data.toString(),
        normalValue: normalRanges[qId] || '-'
      });
    }

    return results;
  }

// متد کمکی برای پردازش سایر اشیاء تودرتو
  private processFlattenedObject(data: any, textL2: any): ParaclinicResult[] {
    const results: ParaclinicResult[] = [];

    const flatten = (obj: any, parentText: any) => {
      for (const key in obj) {
        const value = obj[key];
        const title = (parentText && parentText[key]) ? parentText[key] : key.replace(/_/g, ' ');

        if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
          // اگر باز هم تودرتو بود (مثل torachonthesis -> Fluid -> LDH)
          flatten(value, parentText ? parentText[key] : null);
        } else {
          results.push({
            title: title,
            answer: Array.isArray(value) ? value.join(' | ') : value.toString(),
            normalValue: '-' // می‌توانید مقادیر نرمال را اینجا اضافه کنید
          });
        }
      }
    };

    flatten(data, textL2);
    return results;
  }
}



