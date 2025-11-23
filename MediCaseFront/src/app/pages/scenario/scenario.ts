import {ChangeDetectorRef, Component, signal} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {APP_CONFIG} from '../../config/app.config';
import {NgClass} from '@angular/common';
import {RouterLink} from '@angular/router';
import {Master} from '../../core/services/master';
import Questions from '../../../../public/json/senario.json'
import Log from '../../../../public/json/student_log.json'


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

  timer = signal('15:00')
  logo = APP_CONFIG.logoURL;
  backgroundImage = 'assets/bg.jpg';
  diseases: Disease[] = [];
  sections: Section[] = [];
  activeSection: number | null = 1
  clickSound = new Audio('sounds/click.mp3');
  successSound = new Audio('sounds/success.mp3');
  questions: Question[] = [];
  // لیست متن سوالا
  questionText: any = Questions
  //لیست دیتا های ai
  data: any
  //لیست دیتایی که قراره بفرستیم
  log: any = Log
  physicalExamBySection: Record<string, Question[]> = {};
  questionsBySection: Record<string, Question[]> = {};
  protected readonly APP_CONFIG = APP_CONFIG;
  protected readonly sessionStorage = sessionStorage;
  private timeLeft = 15 * 60;
  private intervalId: any;

  constructor(public changeDetectorRef: ChangeDetectorRef, public master: Master) {
  }


  ngOnInit() {
    this.loadDiseases();
    this.loadSections();
    this.startTimer();


    this.master.pulmonologyScenarioRetrieve('44QGMQQDZJ').subscribe({
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

        console.log(this.data);
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
    ];
  }

  loadSections() {
    this.sections = [
      {id: 1, title: 'اطلاعات بیمار', icon: 'pi pi-id-card'},
      {id: 2, title: 'شرح حال', icon: 'pi pi-list'},
      {id: 3, title: 'معاینه', icon: 'pi pi-heart'},
      {id: 4, title: 'پاراکلینیک', icon: 'pi pi-folder'},
      {id: 5, title: 'تشخیص افتراقی', icon: 'pi pi-pencil'},
      {id: 6, title: 'درمان', icon: 'pi pi-lock'},
    ];
  }

  selectSection(section: Section) {
    this.activeSection = section.id;
    // this.playSuccess();
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


  // ... داخل کلاس Scenario

  handleQuestionClick(question: Question, systemName: string, sectionCategory: 'history_taking' | 'physical_exam') {
    console.log(this.log)
    this.playClick();

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
}
