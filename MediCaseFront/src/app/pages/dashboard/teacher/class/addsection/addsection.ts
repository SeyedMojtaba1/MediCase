import {AfterViewInit, ChangeDetectorRef, Component, EventEmitter, Input, Output} from '@angular/core';
import {Router} from '@angular/router';
import {Master} from '../../../../../core/services/master';
import {Button} from 'primeng/button';
import {InputText} from 'primeng/inputtext';
import {Dialog} from 'primeng/dialog';
import {ToastService} from '../../../../../core/services/toast';
import {Select} from 'primeng/select';
import {FormsModule} from '@angular/forms';
import moment from 'moment-jalaali';


declare var jalaliDatepicker: any;


@Component({
  selector: 'app-addsection',
  imports: [
    Button,
    InputText,
    Dialog,
    Select,
    FormsModule
  ],
  templateUrl: './addsection.html',
  styleUrl: './addsection.css'
})
export class Addsection implements AfterViewInit {

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


  ngAfterViewInit() {
    // شروع کار datepicker
    jalaliDatepicker.startWatch({
      // تنظیمات اختیاری
      minDate: "today",
      maxDate: "attr",
      date: {
        // تاریخ پیش‌فرض
        year: 1403,
        month: 1,
        day: 1
      }
    });
  }

  ngOnInit() {

    jalaliDatepicker.startWatch({persianDigits: true, showEmptyBtn: false, showTodayBtn: false, showToday: true});

    this.master.semesters().subscribe({
      next: data => {
        this.semesters = data.body
        this.master.subjectList().subscribe({
          next: data => {
            this.subjects = data.body
            this.subjectOptions = this.subjects.map((s: any) => ({
              ...s,
              label: s["persian-name"],
              value: s.id
            }));
            console.log(this.subjectOptions);
          },
          error: err => {
            this.toast.showError('خطایی در دریافت اطلاعات وجود دارد')
          },
          complete: () => {
            this.changeDetectorRef.detectChanges()
          }
        })
      },
      error: err => {
        this.toast.showError("خطایی در دریافت اطلاعات وجود دارد")
      },
      complete: () => {
        this.changeDetectorRef.detectChanges()
      }
    })
  }

  ngOnChanges() {
    this.visible = this.show;   // اگر والد باز کرد، دیالوگ باز شود
  }


  onHide() {
    this.close.emit();          // اگر بیرون کلیک شد یا بسته شد

  }

  Confirm() {

    this.master.createSection(this.data)
    this.close.emit();
  }

  Back() {
    this.close.emit();
  }


  onDialogShow() {
    setTimeout(() => {
      jalaliDatepicker.startWatch();
    }, 10);
  }


  jalaliToTimestamp(jdate: string): string {
    const m = moment(jdate, 'jYYYY/jM/jD');
    return m.format('YYYY-MM-DD');

  }

  submitClick() {
    // چک کردن خالی نبودن فیلدها
    if (!this.data.name ||
      !this.data.subject ||
      !this.data.semester_code ||
      !this.start_date ||
      !this.end_date
    ) {

      this.toast.showError("لطفاً تمام فیلدها را تکمیل کنید");
      return;
    }

    // تبدیل تاریخ‌ها
    this.data.start_date = this.jalaliToTimestamp(this.start_date)
    this.data.end_date = this.jalaliToTimestamp(this.end_date)

    // ارسال به API
    this.master.createSection(this.data).subscribe({
      next: data => {
        this.toast.showSuccess("کلاس با موفقیت ایجاد شد");
        setTimeout(() => {
            window.location.reload();
          }, 200
        )
        this.close.emit();
      },
      error: err => {
        console.log(err);
        this.toast.showError("خطایی رخ داد");
      }
    });
  }
}
