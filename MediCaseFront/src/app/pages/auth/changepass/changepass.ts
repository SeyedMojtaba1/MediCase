import {Component, signal} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {APP_CONFIG} from '../../../config/app.config';
import {Password} from 'primeng/password';
import {Router, RouterLink} from '@angular/router';
import {Master} from '../../../core/services/master';
import {ToastService} from '../../../core/services/toast';

@Component({
  selector: 'app-changepass',
  imports: [
    ReactiveFormsModule,
    FormsModule,
    Password,
    RouterLink
  ],
  templateUrl: './changepass.html',
  styleUrl: './changepass.css'
})
export class Changepass {

  password: string = '';
  verifypass: string = '';
  verifying = signal(false)

  protected readonly APP_CONFIG = APP_CONFIG;

  constructor(private router: Router, public master: Master, public toast: ToastService) {
  }

  // بررسی امکان تایید
  canVerify(): boolean {
    return this.password.length >= 8 &&
      this.verifypass.length >= 8 &&
      this.password === this.verifypass;
  }

  // تایید و تغییر رمز عبور
  verifyCode() {
    if (!this.canVerify()) {
      this.toast.showError('رمز عبور جدید و تکرار آن باید یکسان باشد')
      return;
    }

    this.verifying.set(true)
    const email: string = localStorage.getItem('reset_email') ?? '';
    this.master.resetPass(email, this.password).subscribe(
      {
        next: () => {
          this.toast.showSuccess('رمز عبور شما با موفقیت تغییر کرد')
          localStorage.removeItem('reset_email');
          this.verifying.set(false)
          this.router.navigateByUrl('/login');
        },
        error: err => {
          this.toast.showError('خطایی در تغییر رمز عبور وجود دارد')
          this.verifying.set(false)
        }
      }
    )

  }

  // اعتبارسنجی رمز عبور
  isPasswordValid(): boolean {
    return this.password.length >= 6;
  }

  // بررسی مطابقت رمز عبور
  doPasswordsMatch(): boolean {
    return this.password === this.verifypass;
  }

  // نمایش پیام خطا
  getErrorMessage(): string {
    if (this.password.length < 6) {
      return 'رمز عبور باید حداقل ۶ کاراکتر باشد';
    } else if (this.verifypass && !this.doPasswordsMatch()) {
      return 'رمز عبور و تکرار آن مطابقت ندارند';
    }
    return '';
  }
}
