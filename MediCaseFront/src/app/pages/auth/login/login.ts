import {ChangeDetectorRef, Component, signal} from '@angular/core';
import {APP_CONFIG} from '../../../config/app.config';
import {InputText} from 'primeng/inputtext';
import {FormsModule} from '@angular/forms';
import {Password} from 'primeng/password';
import {NgClass} from '@angular/common';
import {Router, RouterLink} from '@angular/router';
import {Master} from '../../../core/services/master';
import {ToastService} from '../../../core/services/toast';
import {Auth} from '../../../core/guards/auth';

@Component({
  selector: 'app-login',
  imports: [
    InputText,
    FormsModule,
    Password,
    NgClass,
    RouterLink
  ],
  templateUrl: './login.html',
  styleUrl: './login.css',
  standalone: true
})
export class Login {
  username!: string;
  password!: string;
  showPassword = false;
  loading = signal(false)
  protected readonly APP_CONFIG = APP_CONFIG;
  protected readonly alert = alert;

  constructor(public auth: Auth, public changeDetectorRef: ChangeDetectorRef, public master: Master, public router: Router, public toast: ToastService) {
  }

  onLogin() {
    if (this.loading()) return;
    if (!this.username || !this.password) {
      this.toast.showWarn('لطفا تمام فیلد ها را وارد کنید', 'خطا');
      return;
    }
    this.loading.set(true);
    this.master.login(this.username, this.password).subscribe(
      {
        next: (res) => {
          this.toast.showSuccess('ورود شما به مدیکیس موفقیت آمیز بود', 'خوش آمدید')
          this.router.navigateByUrl('/dashboard/s');
          sessionStorage.clear();
          this.loading.set(false);

          const userRole = res.body.user.main_role // response.role;

          if (userRole == 'student' || userRole == 'teacher') {
            this.auth.login(userRole, res.body.access_token);
          } else {
            console.error('نقش کاربر نامعتبر است');
          }

          sessionStorage.setItem('first_name', res.body.user.first_name);
          sessionStorage.setItem('last_name', res.body.user.last_name);
          sessionStorage.setItem('email', res.body.user.email);
          sessionStorage.setItem('avatar', res.body.user.profile_image);
          sessionStorage.setItem('role', res.body.user.main_role);
          sessionStorage.setItem('username', res.body.user.username);
          sessionStorage.setItem('phone_number', res.body.user.phone_number);
          sessionStorage.setItem('university', res.body.user.university);
          sessionStorage.setItem('faculty', res.body.user.faculty);
          sessionStorage.setItem('department', res.body.user.department);


        },
        error: err => {
          this.toast.showError('نام کاربری یا رمز عبور اشتباه است', 'خطا')
          this.password = ''
          this.username = ''
          this.loading.set(false);
        }
      }
    )

  }
}
