import {ChangeDetectorRef, Component, EventEmitter, Input, Output} from '@angular/core';
import {Router} from '@angular/router';
import {Master} from '../../../core/services/master';
import {ToastService} from '../../../core/services/toast';
import {FormsModule} from '@angular/forms';
import {Dialog} from 'primeng/dialog';
import {Auth} from '../../../core/guards/auth';
import {Button} from 'primeng/button';
import {Password} from 'primeng/password';


@Component({
  selector: 'app-change-login',
  imports: [
    FormsModule,
    Dialog,
    Button,
    Password,
  ],
  templateUrl: './change-login.html',
  styleUrl: './change-login.css'
})
export class ChangeLogin {

  @Input() show = false;
  @Output() close = new EventEmitter<void>();

  visible = false;
  password = ''
  new_password = ''
  new_password2 = ''

  constructor(public auth: Auth, public router: Router, public master: Master, public toast: ToastService, public changeDetectorRef: ChangeDetectorRef) {
  }

  submit() {
    if (this.new_password != this.new_password2) {
      this.toast.showError("رمز های عبور برابر نیستند");
      return;
    }
    this.master.changePassword(
      this.password, this.new_password2
    ).subscribe({
      next: (res) => {
        this.toast.showSuccess("رمز عبور با موفقیت تغییر کرد")

        setTimeout(() => {
          this.auth.logout();
        }, 2000);
      },
      error: (err) => {
        this.toast.showError("رمز عبور انتخابی باید حداقل 8 کارکتر باشد")
      }
    })
  }

  ngOnInit() {

  }

  ngOnChanges() {
    this.visible = this.show;   // اگر والد باز کرد، دیالوگ باز شود
  }


  onHide() {
    this.close.emit();          // اگر بیرون کلیک شد یا بسته شد

  }


}

