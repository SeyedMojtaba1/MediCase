import {ChangeDetectorRef, Component, OnInit} from '@angular/core';
import {Master} from '../../../core/services/master';
import {ActivatedRoute} from '@angular/router';
import {CommonModule} from '@angular/common';
import confetti from 'canvas-confetti';

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
      next: (data: any) => {
        this.feedback = data.feedback || data;
        this.changeDetectorRef.detectChanges();

        // اگر امتیاز از حدی بالاتر بود یا صرفاً جهت خوش‌آمدگویی
        this.fireConfetti();
      },
      error: (err) => console.error('Error fetching feedback:', err)
    });
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
}
