import {ChangeDetectorRef, Component, EventEmitter, Input, Output} from '@angular/core';
import {Router} from '@angular/router';
import {Master} from '../../../../../../core/services/master';
import {Button} from 'primeng/button';
import {Dialog} from 'primeng/dialog';
import {ToastService} from '../../../../../../core/services/toast';
import {FormsModule} from '@angular/forms';
import {InputText} from 'primeng/inputtext';
import {Select} from 'primeng/select';
import moment from 'moment-jalaali';


declare var jalaliDatepicker: any;


@Component({
  selector: 'app-edit-section',
  imports: [Button,
    Dialog,
    FormsModule,
    InputText, Select,
  ],
  templateUrl: './edit-section.html',
  styleUrl: './edit-section.css'
})
export class EditSection {

  @Input() show = false;
  @Output() close = new EventEmitter<void>();
  @Input() sectionID = ''

  code = ''
  start_date: string = '';
  end_date: string = '';

  data = {
    new_name: '',
    semester_code: '',
    description: '',
    start_date: '',
    end_date: '',
    sectionID: ''
  }
  semesters: { code: string, name: string }[] = []


  section: any

  constructor(public router: Router, public master: Master, public toast: ToastService, public changeDetectorRef: ChangeDetectorRef) {
  }

  ngOnInit() {
    // مقداردهی اولیه دیت‌پیکر با تنظیم minDate روی حالت attr
    jalaliDatepicker.startWatch({
      persianDigits: true,
      showEmptyBtn: false,
      showTodayBtn: false,
      showToday: true,
      minDate: "attr" // بسیار مهم
    });

    this.master.semesters().subscribe({
      next: res => {
        this.semesters = res.body.sort((a: any, b: any) => Number(a.code) - Number(b.code));
      },
      complete: () => {
        this.master.sectionRetrieve(this.sectionID).subscribe({
          next: res => {
            this.section = res.body;
            this.data.new_name = res.body.name;
            this.data.semester_code = res.body.semester_code;
            this.data.description = res.body.description;

            // تبدیل تاریخ‌ها برای نمایش در اینپوت
            this.start_date = this.timeToJalali(res.body.start_date);
            this.end_date = this.timeToJalali(res.body.end_date);

            this.data.sectionID = this.sectionID;

            // اعمال محدودیت بلافاصله بعد از دریافت داده‌های قدیمی
            setTimeout(() => {
              this.updateMinEndDate(this.start_date);
            }, 100);
          }
        })
      }
    })
  }

  // متد کلیدی برای مدیریت محدودیت تاریخ پایان
  updateMinEndDate(newStartDate: string) {
    const endDateElement = document.getElementById('end-date-input');
    if (endDateElement && newStartDate) {
      endDateElement.setAttribute('data-jdp-min-date', newStartDate);

      // اگر تاریخ پایان فعلی قبل از تاریخ شروع جدید است، آن را پاک کن
      if (this.end_date && this.end_date < newStartDate) {
        this.end_date = '';
      }
    }
  }

  Confirm() {
    // انتقال مقادیر از متغیرهای محلی به آبجکت data قبل از ارسال
    this.data.start_date = this.jalaliToTimestamp(this.start_date);
    this.data.end_date = this.jalaliToTimestamp(this.end_date);

    this.master.sectionUpdate(this.data).subscribe({
      next: (data) => {
        this.toast.showSuccess('اطلاعات کلاس با موفقیت به روز شد');
        setTimeout(() => {
          window.location.reload();
        }, 200);
      },
      error: () => this.toast.showError('خطایی وجود دارد')
    });
    this.close.emit();
  }

  onDialogShow() {
    setTimeout(() => {
      // مجدداً استارت‌واچ را صدا می‌زنیم تا المان‌های داخل دایالوگ شناسایی شوند
      jalaliDatepicker.startWatch({minDate: "attr"});
      // بعد از باز شدن دایالوگ هم مطمئن می‌شویم محدودیت ست شده است
      this.updateMinEndDate(this.start_date);
    }, 50);
  }

  onHide() {
    this.close.emit();          // اگر بیرون کلیک شد یا بسته شد
  }


  jalaliToTimestamp(jdate: string): string {
    const m = moment(jdate, 'jYYYY/jM/jD');
    return m.format('YYYY-MM-DD');

  }


  timeToJalali(date: string): string {
    const m = moment(date, 'YYYY-MM-DD');
    return m.format('jYYYY/jM/jD');
  }

  Back() {
    this.close.emit();
  }


}

