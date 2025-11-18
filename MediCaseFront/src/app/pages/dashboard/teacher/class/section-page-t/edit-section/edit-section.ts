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

  visible = false;
  code = ''

  data = {
    new_name: '',
    semester_code: '',
    description: '',
    start_date: '',
    end_date: '',
    sectionID: ''
  }
  semesters: { code: string, name: string }[] = []
  start_date!: string
  end_date!: string

  section: any

  constructor(public router: Router, public master: Master, public toast: ToastService, public changeDetectorRef: ChangeDetectorRef) {
  }


  ngOnInit() {

    jalaliDatepicker.startWatch({persianDigits: true, showEmptyBtn: false, showTodayBtn: false, showToday: true});


    // 1) دریافت لیست ترم‌ها
    this.master.semesters().subscribe({
      next: res => {
        this.semesters = res.body;
      },
      complete: () => {
        // 2) دریافت اطلاعات سِکشن
        this.master.sectionRetrieve(this.sectionID).subscribe({
          next: res => {
            this.section = res.body;
            this.data.new_name = res.body.name;
            this.data.semester_code = res.body.semester_code;
            this.data.description = res.body.description;
            this.data.start_date = this.timeToJalali(res.body.start_date)
            this.data.end_date = this.timeToJalali(res.body.end_date)
            this.data.sectionID = this.sectionID;
          }
        })
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
    console.log(this.data.start_date);
    console.log(this.data.end_date);

    this.data.start_date = this.jalaliToTimestamp(this.data.start_date)
    this.data.end_date = this.jalaliToTimestamp(this.data.end_date)

    this.master.sectionUpdate(this.data).subscribe({
      next: (data) => {
        this.toast.showSuccess('اطلاعات کلاس با موفقیت به روز شد')
      },
      error: err => {
        this.toast.showError('خطایی وجود دارد')
      },
      complete: () => {
      }
    })
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


  timeToJalali(date: string): string {
    const m = moment(date, 'YYYY-MM-DD');
    return m.format('jYYYY/jM/jD');
  }

  Back() {
    this.close.emit();
  }


}

