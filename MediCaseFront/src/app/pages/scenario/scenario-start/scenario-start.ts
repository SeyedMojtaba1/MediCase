import {Component, signal} from '@angular/core';
import {NgClass} from '@angular/common';
import {ProgressBar} from 'primeng/progressbar';


@Component({
  selector: 'app-scenario-start',
  imports: [
    NgClass,
    ProgressBar
  ],
  templateUrl: './scenario-start.html',
  styleUrl: './scenario-start.css'
})
export class ScenarioStart {


  value = signal(0)
  interval: any;


  text = [
    'خروج از روند ویزیت بیمار، به این معناست که شما مطب خود را ترک کرده اید. پس امکان بازگشت مجدد وجود ندارد',
    'در پرسیدن سوالات مختلف از بیمار و همچنین انجام آزمایشات مختلف دقت کنید. چرا که انجام کار های غیر مرتبط، تاثیر منفی در بازخورد نهایی عملکرد شما دارد',
    'در فرایند ویزیت بیمار، به ترتیب انجام امور دقت کنید. عدم رعایت ترتیب درست، نمره منفی به دنبال دارد',
    'با انجام کامل روند ویزیت و تشخیص بیماری، در انتها گزارشی از وضعیت عملکرد شما و همچنین پیشنهاداتی برای بهبود عملکرد شما توسط هوش مصنوعی تهیه می شود.'
  ]
  randomText = signal('')

  ngOnInit() {
    this.selectRandomText()
    this.setTimer()
    document.addEventListener('click', this.playVideoOnce);

  }


  playVideoOnce = () => {
    const video = document.getElementById('myVideo') as HTMLVideoElement;

    if (video && video.paused) {
      video.play().catch(err => console.log('Autoplay blocked:', err));

      // بعد از اولین کلیک، لیسنر رو پاک کن
      document.removeEventListener('click', this.playVideoOnce);
    }
  }

  selectRandomText(): void {
    const randomIndex = Math.floor(Math.random() * this.text.length);
    this.randomText.set(this.text[randomIndex])
  }

  setTimer() {
    const duration = 20000;      // 10 seconds
    const steps = 100;          // reach 100
    const stepTime = duration / steps; // 50 ms

    this.interval = setInterval(() => {
      const v = this.value() + 1
      this.value.set(v)

      if (this.value() >= 100) {
        this.value.set(100)
        clearInterval(this.interval);
      }
    }, stepTime);
  }


}
