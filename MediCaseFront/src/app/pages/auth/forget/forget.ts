import {ChangeDetectorRef, Component, OnDestroy, signal} from '@angular/core';
import {InputText} from 'primeng/inputtext';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {APP_CONFIG} from '../../../config/app.config';
import {InputOtp} from 'primeng/inputotp';
import {Router, RouterLink} from '@angular/router';
import {Master} from '../../../core/services/master';
import {ToastService} from '../../../core/services/toast';

@Component({
  selector: 'app-forget',
  imports: [
    InputText,
    ReactiveFormsModule,
    FormsModule,
    InputOtp,
    RouterLink
  ],
  templateUrl: './forget.html',
  styleUrl: './forget.css'
})
export class Forget implements OnDestroy {

  username = '';
  verificationCode = '';
  loading = signal(false);
  verifying = false;
  timerActive = false;
  haveError = signal(false);
  codeSent = false;
  remainingTime = 0;
  intervalId: any;
  protected readonly APP_CONFIG = APP_CONFIG;

  constructor(
    private changedetector: ChangeDetectorRef,
    public toast: ToastService,
    public router: Router,
    public master: Master
  ) {
  }

  // ارسال کد به API
  sendCode() {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    this.haveError.set(!emailRegex.test(this.username));

    if (!this.username || (this.timerActive && this.remainingTime > 0) || this.haveError()) return;

    this.loading.set(true);
    this.master.sendOTP(this.username).subscribe({
      next: (response) => {
        this.loading.set(false);
        this.codeSent = true; // اضافه شده
        this.timerActive = true; // اضافه شده
        this.startTimer();
        this.toast.showSuccess('کد تأیید با موفقیت ارسال شد'); // اختیاری
      },
      error: (error) => {
        this.loading.set(false);
        this.username = '';
        this.haveError.set(true);
      }
    });
  }

  // شروع تایمر ۲ دقیقه‌ای
  startTimer() {
    this.remainingTime = 2 * 60;
    this.timerActive = true; // اضافه شده
    clearInterval(this.intervalId);

    this.intervalId = setInterval(() => {
      this.remainingTime--;

      if (this.remainingTime <= 0) {
        clearInterval(this.intervalId);
        this.timerActive = false;
        this.verificationCode = '';
        this.toast.showWarn('زمان وارد کردن کد به پایان رسید'); // اختیاری
      }

      this.changedetector.detectChanges();
    }, 1000);
  }

  // فرمت زمان به صورت MM:SS
  formatTime(seconds: number): string {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  }

  // بررسی امکان تایید
  canVerify(): boolean {
    this.verificationCode.slice(0, 6);
    return this.codeSent &&
      this.verificationCode.length === 6 &&
      this.timerActive &&
      this.remainingTime > 0; // اضافه شده شرط زمان
  }

  // تایید کد
  verifyCode() {
    // if (!this.canVerify()) return;

    this.verifying = true;

    // استفاده از API واقعی - مثال:
    this.master.verifyOTP(this.username, this.verificationCode).subscribe({
      next: () => {
        this.verifying = false;
        localStorage.setItem('reset_email', this.username); // ذخیره ایمیل برای صفحه بعد
        this.toast.showSuccess('کد با موفقیت تأیید شد');
        this.router.navigateByUrl('/changepass');
      },
      error: () => {
        this.verifying = false;
        this.verificationCode = ''; // پاک کردن کد برای ورود مجدد
        this.toast.showError("کد وارد شده نادرست است")
      }
    });

  }

  // پاکسازی interval هنگام از بین رفتن کامپوننت
  ngOnDestroy() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }
}
