import {ChangeDetectorRef, Component, ElementRef, signal, ViewChild} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {APP_CONFIG} from '../../config/app.config';
import {NgClass} from '@angular/common';
import {ActivatedRoute, Router, RouterLink} from '@angular/router';
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
    "Pleural_Effusion": "disease7",
    "ARDS": "disease8"
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
  previousMediaUrl: string = "https://elmkhah.ir/wp-content/uploads/2025/11/photo_2025-11-28_16-52-45.jpg";
  sectionOpenState: Record<string, boolean> = {};
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
  scenarioData: any = Questions;
// در کلاس Scenario
  sectionMedia: any = {

    patient_profile: {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Realistic_Clinical_Video_Generation.mp4'
    },

    history_taking: {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/سخنگو.mp4'
    },
    present_illness: {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Patient_Cough_Animation_Generation.mp4'
    },
    past_medical_history: {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Patient_Cough_Animation_Generation.mp4'
    },

    drug_history: {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Patient_Cough_Animation_Generation.mp4'
    },

    allergies: {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Patient_Cough_Animation_Generation.mp4'
    },
    family_history: {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Patient_Cough_Animation_Generation.mp4'
    },
    social_history: {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Patient_Cough_Animation_Generation.mp4'
    },
    ros: {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Patient_Cough_Animation_Generation.mp4'

    },


    'general_appearance': {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Patient_Cough_Animation_Generation.mp4'
    },

    'vital_signs': {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Realistic_Clinical_Video_Generation2.mp4'
    },
    'vital_signs-PR': {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Camera_angle_fixed_202512232146_6acpt.mp4'
    },
    'vital_signs-SpO2': {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/video_1766436318100.mp4',
    },
    'vital_signs-T': {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/video_1766436280215.mp4',
    },
    'vital_signs-BP': {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/video_1766436259968.mp4',
    },

    'head_and_neck': {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/تبدیل_عکس_به_ویدیو_با_صدا.mp4'
    },
    'head_and_neck-eyes': {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Camera_angle_closeup_202512232155_m32tj.mp4'
    },

    'respiratory_system': {
      type: 'image',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/11/respiratory_system.jpg'
    },

    'respiratory_system-inspection': {
      type: 'video',
      url: "https://elmkhah.ir/wp-content/uploads/2025/12/Video_Editing_Camera_and_Posture.mp4"
    },

    'respiratory_system-palpation': {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/A_highly_detailed_202512022024_vusw2.mp4'
    },

    'respiratory_system-percussion': {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Animated_Chest_Percussion_Video_Generation.mp4'
    },

    'respiratory_system-auscultation': {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Create_a_short_202512021949_v8jz2.mp4'
    },

    'cardiovascular_system': {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Create_a_short_202512022036_dk5kc.mp4'
    },

    'cardiovascular_system-auscultation': {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/202512022051_zdina.mp4'
    },

    'abdominal_system': {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/202512022225_hew7q.mp4'
    },

    'abdominal_system-inspection': {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Create_a_short_202512022036_dk5kc.mp4'
    },
    'abdominal_system-auscultation': {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Camera_angle_topdown_202512022238_n3vt0.mp4'
    },
    'abdominal_system-percussion': {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/202512022225_hew7q.mp4'
    },
    'abdominal_system-palpation': {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Create_a_short_202512022036_dk5kc.mp4'
    },


    'neurological': {
      type: 'video',
      url: "https://elmkhah.ir/wp-content/uploads/2025/12/Facial_Nerve_Exam_Animation.mp4"
    },
    "neurological-motor_strength_and_DTRs": {
      type: 'video',
      url: "https://elmkhah.ir/wp-content/uploads/2025/12/Generate_Looping_Medical_Animation_Video.mp4"
    },
    "neurological-cranial_nerves": {
      type: 'video',
      url: "https://elmkhah.ir/wp-content/uploads/2025/12/Facial_Nerve_Exam_Animation.mp4"
    },

    "musculoskeletal_system": {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Generate_Looping_Medical_Animation_Video.mp4'
    },
    "musculoskeletal_system-range_of_motion": {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Camera_angle_topdown_202512022252_whtlj.mp4'
    },

    'differential_diagnosis': {
      type: 'video',
      url: 'https://elmkhah.ir/wp-content/uploads/2025/12/Reference_image_usage_202512162300_seewl.mp4',
    }

  };
  mediaType: 'image' | 'video' = 'image';
  mediaUrl: string = "https://elmkhah.ir/wp-content/uploads/2025/11/photo_2025-11-28_16-52-45.jpg";
  public code: any;
  public trackingCode: any;
  protected readonly APP_CONFIG = APP_CONFIG;
  protected readonly sessionStorage = sessionStorage;
  protected readonly Log = Log;
  protected readonly console = console;
  private timeLeft = 15 * 60;
  private intervalId: any;

  constructor(public router: Router, public changeDetectorRef: ChangeDetectorRef, public master: Master, public route: ActivatedRoute) {
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
    this.clickSound.volume = 0.3
    this.clickSound.play();
  }

  isArray(obj: any): boolean {
    return Array.isArray(obj);
  }

// در فایل scenario.ts متد setQuestion را پیدا و به این صورت اصلاح کنید:

  setQuestion(q: any) {
    this.playClick();
    q.visible = true;
    q.answer_time = new Date().toLocaleTimeString('fa-IR');

    const paraclinics = this.scenarioData.patient_info.paraclinic; // نام فیلد را طبق سناریو چک کنید
    const textL2 = this.scenarioData.text_l2.paraclinics;

    // ۱. فیلتر تست‌های خون
    if (q.id === 'crp' || q.id === 'esr' || q.id.includes('blood')) {
      q.answer = this.processBasicBloodTests(q.answer, textL2, q.id);
    }
    // ۲. مدیریت Thorachocentesis و سایر پروسیجرها که آبجکت هستند
    else if (q.id === 'thorachocentesis' || typeof q.answer === 'object') {
      const data = paraclinics[q.id];
      if (data && typeof data === 'object' && !Array.isArray(data)) {
        // استفاده از متد بازگشتی برای تبدیل آبجکت به متن خوانا
        q.answer = this.processFlattenedObject(data, textL2[q.id]);
      } else {
        q.answer = data;
      }
    } else {
      q.answer = paraclinics[q.id];
    }
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

// ...
// در کلاس Scenario
  selectSection(section: Section) {
    if (section.id === 5) {
      this.showDifferentialDiagnosisModal = true;
      this.differentialDiagnosisStage = 1;
      this.playClick();
      return;
    }

    this.activeSection = section.id;

    // نمایش مدیا بر اساس بخش انتخاب شده
    this.setSectionMedia(section);

    // اضافه کردن این بخش برای کنترل صدای ویدیوهای جدید
    setTimeout(() => {
      if (this.videoElementRef && this.videoElementRef.nativeElement) {
        this.videoElementRef.nativeElement.muted = this.isMuted();
      }
    }, 100);
  }

// متد جدید برای تنظیم مدیا بر اساس بخش
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

    if (mediaKey) {
      media = this.sectionMedia[mediaKey];
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

  handleQuestionClick(question: Question, systemName: string, sectionCategory: 'history_taking' | 'physical_exam' | 'paraclinic') {
    this.playClick();

    let media;
    const defaultImageUrl = 'https://elmkhah.ir/wp-content/uploads/2025/11/photo_2025-11-28_16-52-45.jpg';

    // ابتدا سعی کنید مدیا را بر اساس systemName و question.id پیدا کنید
    const specificKey = `${systemName}-${question.id}`;
    media = this.sectionMedia[specificKey];

    // اگر پیدا نشد، سعی کنید بر اساس systemName و بخش‌های question.id پیدا کنید
    if (!media) {
      // برای سوالاتی که id آنها شامل "-" است (مثلاً inspection-accessory_muscles)
      if (question.id.includes('-')) {
        const parts = question.id.split('-');
        if (parts.length >= 2) {
          const potentialKey = `${systemName}-${parts[0]}`;
          media = this.sectionMedia[potentialKey];
        }
      }
    }

    // اگر هنوز پیدا نشد، از systemName استفاده کنید
    if (!media) {
      media = this.sectionMedia[systemName];
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

    // منطق لاگ و باز کردن سوال (همانند قبل)
    if (!question.open) {
      const currentTime = this.timer();
      question.answer_time = currentTime;

      const logCategory = this.log[sectionCategory];

      if (logCategory && !logCategory[systemName]) {
        logCategory[systemName] = {};
      }

      const logSection = logCategory[systemName];
      const [key, subKey] = question.id.split('-');

      if (subKey) {
        if (!logSection[key] || typeof logSection[key] !== 'object') {
          logSection[key] = {};
        }
        logSection[key][subKey] = currentTime;
      } else {
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

    // this.master.pulmonologyScenarioFeedbackCreate(this.trackingCode, this.log).subscribe({});

    this.showDifferentialDiagnosisModal = false;
    this.fireConfetti();
    this.router.navigateByUrl('/scenarioinit');
    this.playSuccess();
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

    // سطح ۱: دسته‌بندی‌ها
    for (const categoryName in paraclinicAnswers) {
      const categoryText = paraclinicText[categoryName];
      const categoryAnswers = paraclinicAnswers[categoryName];
      const categoryLogs = paraclinicLogs[categoryName];

      this.paraclinicBySection[categoryName] = [];

      // سطح ۲: تست‌های اصلی
      for (const testKey in categoryAnswers) {
        const answerL2 = categoryAnswers[testKey];
        const logL2 = categoryLogs ? categoryLogs[testKey] : 'False';

        // استخراج متن عنوان
        let textL2: any = '';
        if (categoryText) {
          textL2 = categoryText[testKey];
        }

        let finalAnswer: any = '';
        let finalTitle = '';

        // --- ۱. استخراج عنوان دکمه ---
        if (typeof textL2 === 'object' && textL2 !== null && !Array.isArray(textL2)) {
          finalTitle = testKey.replace('_', ' ');
        } else if (typeof textL2 === 'string') {
          finalTitle = textL2;
        } else {
          finalTitle = testKey.replace('_', ' ');
        }

        // --- ۲. منطق ساختاردهی پاسخ ---

        // حالت خاص برای آزمایش‌های خون (چه آبجکت چه رشته ساده مثل CRP)
        if (categoryName === 'basic_blood_tests') {
          // لیست تست‌هایی که می‌خواهیم حتماً خروجی جدولی داشته باشند
          const bloodTableTests = ['BMP', 'CBC', 'VBG', 'LFTs', 'CRP', 'ESR', 'FBS', 'crp', 'esr'];

          if (bloodTableTests.includes(testKey) || (typeof answerL2 === 'object' && !Array.isArray(answerL2))) {
            // ارسال ۳ آرگومان برای رفع خطای TS2554
            finalAnswer = this.processBasicBloodTests(answerL2, textL2, testKey);
          } else {
            finalAnswer = Array.isArray(answerL2) ? answerL2.join(' | ') : answerL2;
          }
        }
        // سایر بخش‌ها (Spirometry و غیره)
        else if (typeof answerL2 === 'object' && answerL2 !== null && !Array.isArray(answerL2)) {
          if (categoryName === 'functional_tests' && testKey === 'Spirometry') {
            finalAnswer = this.processSpirometryData(answerL2, textL2);
          } else {
            finalAnswer = this.processFlattenedObject(answerL2, textL2);
          }
        }
        // پاسخ‌های رشته‌ای معمولی
        else {
          finalAnswer = Array.isArray(answerL2) ? answerL2.join(' | ') : answerL2;
        }

        // تعریف آیتم اصلی (دکمه)
        this.paraclinicBySection[categoryName].push({
          id: testKey,
          title: finalTitle,
          answer: finalAnswer,
          answer_time: logL2,
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


// متد کمکی برای پردازش داده‌های Spirometry
  private processSpirometryData(spirometryData: any, textL2: any): string | ParaclinicResult[] {
    // spirometryData ساختار: { result: {...}, reversibility: "..." }

    if (!spirometryData.result && !spirometryData.reversibility) {
      return 'داده‌ای موجود نیست';
    }

    let resultString = '';

    // پردازش بخش result
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
  private processFlattenedObject(data: any, textL2: any): string {
    let flattenedString = '';

    for (const itemKey in data) {
      // پیدا کردن عنوان فارسی از فایل ترجمه (textL2)
      let title = (textL2 && textL2[itemKey]) ? textL2[itemKey] : itemKey;
      let value = data[itemKey];

      if (typeof value === 'object' && !Array.isArray(value)) {
        // اگر مقدار خودش آبجکت بود، دوباره همین تابع را صدا بزن
        flattenedString += `${title}:\n${this.processFlattenedObject(value, textL2[itemKey])}\n`;
      } else {
        // اگر مقدار نهایی بود (رشته یا عدد)
        flattenedString += `${title}: ${value}\n`;
      }
    }

    return flattenedString;
  }
}
