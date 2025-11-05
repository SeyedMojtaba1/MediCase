import {ChangeDetectorRef, Component} from '@angular/core';
import {DashNav} from '../../../../shared/components/dash-nav/dash-nav';
import {HospitalCard} from './hospital-card/hospital-card';
import {Master} from '../../../../core/services/master';


@Component({
  selector: 'app-hospital',
  imports: [
    DashNav,
    HospitalCard
  ],
  templateUrl: './hospital.html',
  styleUrl: './hospital.css'
})
export class Hospital {

  subjects = []

  constructor(public master: Master, public changeDetectorRef: ChangeDetectorRef) {
  }

  ngOnInit() {
    this.master.subjectList().subscribe({
      next: data => {
        this.subjects = data.body;
        this.changeDetectorRef.detectChanges();
      },
      error: err => {
      },
    })
  }
}

//
// description
//   :
//   "روماتولوژی شاخه‌ای از پزشکی است که به مطالعه، تشخیص و درمان بیماری‌های بافت همبند و روماتیسمی می‌پردازد؛ بافت‌هایی که شامل مفاصل، رباط‌ها، تاندون‌ها، پوست و اندام‌های داخلی می‌شوند و پشتیبانی ساختاری و عملکردی بدن را فراهم می‌کنند. بیماری‌های روماتیسمی می‌توانند التهابی، خودایمنی یا دژنراتیو باشند و اغلب با درد مفصل، تورم، محدودیت حرکتی و خستگی همراه هستند. از شایع‌ترین بیماری‌ها می‌توان به آرتریت روماتوئید، لوپوس اریتماتوز سیستمیک (SLE)، اسکلرودرمی، پلی‌میوزیت و آرتروز اشاره کرد. علل شامل پاسخ ایمنی نابجای بدن، عوامل ژنتیکی و محیطی و اختلال در تولید یا عملکرد کلاژن و سایر پروتئین‌های بافت همبند است. بیماری‌ها ممکن است سیستمیک بوده و ارگان‌هایی مانند قلب، ریه و کلیه را درگیر کنند. تشخیص بر پایه معاینه بالینی، آزمایش‌های خودایمنی (ANA، RF، anti-CCP)، تصویربرداری مفصلی و در موارد خاص بیوپسی بافت است. درمان شامل دارودرمانی ضدالتهابی، سرکوب سیستم ایمنی، فیزیوتراپی و مدیریت علائم است و هدف آن کاهش التهاب، حفظ عملکرد مفاصل و پیشگیری از آسیب ارگان‌هاست."
// english_name
//   :
//   "Rheumatology"
// persian_name
//   :
//   "بیماری‌های-بافت-همبند-و-روماتیسمی"
// subject_image
//   :
//   null
// unit
//   :
//   1


//
// name: 'ریه',
//   image: '/images/jpg/rie.jpg',
//   description: 'توضیحات کوتاه در مورد رشته ریه و بیماری های مرتبط و دانشگاه علوم پزشکی اصفهان',
//   url: '/',
//   label: 'جدید',
//   active: false
// },
