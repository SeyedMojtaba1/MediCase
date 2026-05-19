import {ChangeDetectorRef, Component, EventEmitter, Input, Output} from '@angular/core';
import {Router} from '@angular/router';
import {Master} from '../../../../../../core/services/master';
import {Button} from 'primeng/button';
import {Dialog} from 'primeng/dialog';
import {ToastService} from '../../../../../../core/services/toast';
import {FormsModule} from '@angular/forms';
import {InputText} from 'primeng/inputtext';

@Component({
  selector: 'app-add-student',
  imports: [
    Button,
    Dialog,
    FormsModule,
    InputText,

  ],
  templateUrl: './add-student.html',
  styleUrl: './add-student.css'
})
export class AddStudent {

  @Input() show = false;
  @Output() close = new EventEmitter<void>();
  @Input() sectionID = ''

  visible = false;
  code = ''


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

  Confirm() {
    this.master.addStudent(this.sectionID, this.code).subscribe({
      next: (data) => {
        this.toast.showSuccess('دانشجو با موفقیت به کلاس افزوده شد')
        setTimeout(() => {
            window.location.reload();
          }, 500
        )
      },
      error: err => {
        this.toast.showError(err.error.student[0])
        this.code = ''

      },
      complete: () => {
      }
    })
    this.close.emit();
  }

  Back() {
    this.close.emit();
  }


}

