import {Component, OnDestroy, OnInit, signal} from '@angular/core';
import {Action} from '../../../shared/components/button/action/action';
import {RouterLink} from '@angular/router';
import {Master} from '../../../core/services/master';

@Component({
  selector: 'app-scenario-start',
  standalone: true,
  imports: [Action, RouterLink],
  templateUrl: './scenario-start.html',
  styleUrl: './scenario-start.css'
})
export class ScenarioStart implements OnInit, OnDestroy {

  value = signal(0);
  interval: any;
  textInterval: any;
  randomText = signal('');
  text = [
    'خروج از روند ویزیت بیمار، به این معناست که شما مطب خود را ترک کرده اید. پس امکان بازگشت مجدد وجود ندارد',
    'در پرسیدن سوالات مختلف از بیمار و همچنین انجام آزمایشات مختلف دقت کنید. چرا که انجام کار های غیر مرتبط، تاثیر منفی در بازخورد نهایی عملکرد شما دارد',
    'در فرایند ویزیت بیمار، به ترتیب انجام امور دقت کنید. عدم رعایت ترتیب درست، نمره منفی به دنبال دارد',
    'با انجام کامل روند ویزیت و تشخیص بیماری، در انتها گزارشی از وضعیت عملکرد شما توسط هوش مصنوعی تهیه می شود.'
  ];
  tracking_code = signal('')


  constructor(public master: Master) {
  }

  ngOnInit() {
    this.selectRandomText();
    this.setTimer();

    // هر ۳ ثانیه یکبار متن تصادفی عوض شود تا حوصله کاربر سر نرود
    this.textInterval = setInterval(() => this.selectRandomText(), 3500);


    this.master.scenarioList().subscribe({
      next: (data: any) => {

        const list = Array.isArray(data) ? data : (data?.body || []);

        if (list.length > 0) {
          const firstPendingTask = list.find((item: any) => item.done === false);

          if (firstPendingTask) {
            this.tracking_code.set(firstPendingTask.tracking_code);
          } else {
            console.warn('تسک انجام نشده‌ای یافت نشد.');
          }
        } else {
          console.warn('لیست دریافتی خالی است یا آرایه نیست.');
        }
      },
      error: err => {
        console.error('خطای ارتباط با سرور:', err);
      },

    });

    // لیسنر برای پخش ویدیو با اولین کلیک (رفع محدودیت Autoplay)
    window.addEventListener('click', this.playVideoOnce, {once: true});
    window.addEventListener('touchstart', this.playVideoOnce, {once: true});

  }

  playVideoOnce = () => {
    const video = document.getElementById('bgVideo') as HTMLVideoElement;
    if (video) {
      video.play().catch(err => console.log("Autoplay prevented:", err));
    }
  }

  selectRandomText(): void {
    const randomIndex = Math.floor(Math.random() * this.text.length);
    this.randomText.set(this.text[randomIndex]);
  }

  setTimer() {
    const duration = 10000; // ۱۰ ثانیه
    const steps = 100;
    const stepTime = duration / steps;

    this.interval = setInterval(() => {
      if (this.value() < 100) {
        this.value.update(v => v + 1);
      } else {
        this.completeLoading();
      }
    }, stepTime);
  }

  completeLoading() {
    clearInterval(this.interval);
    clearInterval(this.textInterval);
    // در صورت تمایل می‌توان اینجا ویدیو را به صورت خودکار Play کرد
    // (اگر قبلاً کاربر جایی کلیک کرده باشد)
    this.playVideoOnce();
  }

  ngOnDestroy() {
    if (this.interval) clearInterval(this.interval);
    if (this.textInterval) clearInterval(this.textInterval);
    window.removeEventListener('click', this.playVideoOnce);
    window.removeEventListener('touchstart', this.playVideoOnce);
  }
}
