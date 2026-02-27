import {ChangeDetectorRef, Component, EventEmitter, Input, Output} from '@angular/core';
import {Router} from '@angular/router';
import {Master} from '../../../core/services/master';
import {ToastService} from '../../../core/services/toast';
import {FormsModule} from '@angular/forms';
import {Button} from 'primeng/button';
import {Dialog} from 'primeng/dialog';
import {FileUpload} from 'primeng/fileupload';


@Component({
  selector: 'app-set-profile-image',
  imports: [
    FormsModule,
    Button,
    Dialog,
    FileUpload
  ], templateUrl: './set-profile-image.html',
  styleUrl: './set-profile-image.css'
})
export class SetProfileImage {

  @Input() show = false;
  @Output() close = new EventEmitter<void>();

  visible = false;
  data = {
    name: '',
    subject: '',
    semester_code: '',
    description: '',
    start_date: '',
    end_date: '',
  }
  semesters: { code: string, name: string }[] = []
  subjects: {
    english_name: string,
    persian_name: string,
    unit: string,
    description: string,
    subject_image: string
  }[] = []
  subjectOptions: any
  start_date!: string
  end_date!: string

  constructor(public router: Router, public master: Master, public toast: ToastService, public changeDetectorRef: ChangeDetectorRef) {
  }


  ngOnInit() {

  }

  ngOnChanges() {
    this.visible = this.show;   // اگر والد باز کرد، دیالوگ باز شود
  }


  onHide() {
    this.close.emit();          // اگر بیرون کلیک شد یا بسته شد

  }


  onUpload(event: any) {
    const file = event.files[0];

    this.master.setProfileImage(file).subscribe({
      next: (res) => this.toast.showSuccess('تصویر نمایه با موفقیت به روز شد'),
      error: (err) => this.toast.showError('خطایی در تغییر نمایه وجود داشت'),
      complete: () => {
        this.master.profile().subscribe({
          next: (res) => {
            sessionStorage.setItem('avatar', res.body.profile_image);
          },
          complete: () => {
            setTimeout(() => {
                window.location.reload();
              }, 200
            )
          }
        })


      }
    });
  }
}

