import {ChangeDetectorRef, Component, OnInit} from '@angular/core';
import {Master} from '../../../core/services/master';
import {ActivatedRoute} from '@angular/router';
import {CommonModule} from '@angular/common';
import confetti from 'canvas-confetti';
import scenarioData from './../../../../../public/json/senario.json'

@Component({
  selector: 'app-scenario-intro',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './scenario-intro.html',
  styleUrl: './scenario-intro.css'
})
export class ScenarioIntro implements OnInit {
  feedback: any;
  code: any;

  constructor(
    public master: Master,
    public changeDetectorRef: ChangeDetectorRef,
    public route: ActivatedRoute
  ) {
  }

  ngOnInit() {
    this.code = this.route.snapshot.paramMap.get('code')!;
    this.master.pulmonologyScenarioFeedbackRetrieve(this.code).subscribe({
      // این کد را بعد از دریافت دیتا در subscribe اضافه کنید
      next: (data: any) => {
        this.feedback = data.feedback || data;

        // حذف موارد تکراری از لیست noise_items بر اساس ID
        if (this.feedback?.detailed_lists?.noise_items) {
          this.feedback.detailed_lists.noise_items = this.feedback.detailed_lists.noise_items.filter(
            (value: any, index: any, self: any) =>
              index === self.findIndex((t: any) => t.id === value.id)
          );
        }

        if (this.feedback?.detailed_lists?.missed_items) {
          this.feedback.detailed_lists.missed_items = this.feedback.detailed_lists.missed_items.filter(
            (value: any, index: any, self: any) =>
              index === self.findIndex((t: any) => t.question === value.question)
          );
        }

        this.changeDetectorRef.detectChanges();
        this.fireConfetti();
      },
      error: (err) => {
        // this.feedback = Data
        this.changeDetectorRef.detectChanges()
      },
      complete: () => {
        this.changeDetectorRef.detectChanges();
      }
    });
    this.changeDetectorRef.detectChanges()
  }

  fireConfetti() {
    confetti({
      particleCount: 150,
      spread: 80,
      origin: {y: 0.6},
      colors: ['#148691', '#216067', '#FFD700']
    });
  }

  shareResults() {
    if (navigator.share) {
      navigator.share({
        title: 'کارنامه ارزیابی بالینی',
        text: `من در سناریوی ${this.feedback.meta.disease} امتیاز ${this.feedback.score.obtained} را کسب کردم.`,
        url: window.location.href
      });
    } else {
      alert('لینک کپی شد: ' + window.location.href);
    }
  }

  getQuestionText(id: string): string {
    if (!id) return '';

    // لیست ترجمه برای موارد خاص
    const manualTranslations: { [key: string]: string } = {

      'FEV1/FVC_Ratio': 'نسبت FEV1/FVC'
    };

    // اول چک کن آیا در لیست دستی ما هست؟
    if (manualTranslations[id]) return manualTranslations[id];

    // پاکسازی مسیر: حذف کلماتی مثل "Result" از مسیر
    const cleanPath = id.replace(/\.Result\./g, '.');
    const path = cleanPath.split('.');

    let current: any = scenarioData;

    for (const key of path) {
      if (current && current[key] !== undefined) {
        current = current[key];
      } else {
        // اگر کلید پیدا نشد، آخرین کلید رو چک کن
        const lastKey = path[path.length - 1];

        // اگه آخرین کلید تو manualTranslations بود، برگردون
        if (manualTranslations[lastKey]) {
          return manualTranslations[lastKey];
        }

        // اگه آخرین کلید شبیه "FVC" یا "FEV1" بود و به Spirometry مربوط میشه
        if (lastKey === 'FVC' || lastKey === 'FEV1' || lastKey === 'FEV1/FVC_Ratio') {
          return manualTranslations[lastKey] || lastKey;
        }

        return '';
      }
    }

    // اگه current یک object بود و خاصیت question داشت
    if (typeof current === 'object' && current !== null) {
      // اگه structure ای مثل { "FVC": "FVC" } داشتیم
      const lastKey = path[path.length - 1];
      if (manualTranslations[lastKey]) {
        return manualTranslations[lastKey];
      }
      return lastKey;
    }

    // اگه current یک string بود، خودش رو برگردون
    if (typeof current === 'string') {
      return current;
    }

    // در نهایت، آخرین کلید مسیر رو با manualTranslations چک کن
    const lastSegment = path[path.length - 1];
    return manualTranslations[lastSegment] || lastSegment;
  }


}
