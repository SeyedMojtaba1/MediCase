import {ChangeDetectorRef, Component} from '@angular/core';
import {APP_CONFIG} from '../../../config/app.config';
import {InputText} from 'primeng/inputtext';
import {FormsModule} from '@angular/forms';
import {Password} from 'primeng/password';
import {NgClass} from '@angular/common';

@Component({
  selector: 'app-login',
  imports: [
    InputText,
    FormsModule,
    Password,
    NgClass
  ],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class Login {
  username!: string;
  showPassword = false;
  loading = false;
  protected readonly APP_CONFIG = APP_CONFIG;
  protected readonly alert = alert;

  constructor(public changeDetectorRef: ChangeDetectorRef) {
  }

  onLogin() {
    if (this.loading) return;
    this.loading = true;

    // شبیه‌سازی درخواست API
    setTimeout(() => {
      this.loading = false;
      this.changeDetectorRef.detectChanges();
    }, 2000);
  }
}
