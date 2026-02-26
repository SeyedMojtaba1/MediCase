import {ChangeDetectorRef, Component, signal} from '@angular/core';
import {DashNav} from '../../../../shared/components/dash-nav/dash-nav';
import {Master} from '../../../../core/services/master';
import {Action} from '../../../../shared/components/button/action/action';
import {ToastService} from '../../../../core/services/toast';
import {Card} from '../../../../layouts/card/card';

@Component({
  selector: 'app-stat',
  imports: [
    DashNav,
    Action,
    Card
  ],
  templateUrl: './stat.html',
  styleUrl: './stat.css'
})
export class Stat {

  data: any
  resData: any
  credit = signal(0)
  expandedAlerts: { [key: string]: boolean } = {
    alert1: false,
    alert2: false
  };
  selectedPatient: any = null; // برای ذخیره اطلاعات بیماری که روی آن کلیک شده
  protected readonly console = console;

  constructor(public master: Master, public changeDetectorRef: ChangeDetectorRef, public toastService: ToastService) {
  }

  ngOnInit() {
    this.getList()
    this.getCredit()
  }

// متدی برای پیدا کردن اطلاعات بیمار از لیست فیدبک‌ها
  getPatientInfo(scenarioCode: string) {
    if (!this.resData) return null;
    const feedback = this.resData.find((f: any) => f.scenario_tracking_code === scenarioCode);
    return feedback?.patient_profile || null;
  }

// متدی برای باز کردن مودال جزئیات
  showPatientDetails(patient: any) {
    this.selectedPatient = patient;
  }

// متدی برای بستن مودال
  closeModal() {
    this.selectedPatient = null;
  }

  getCredit() {
    this.master.profile().subscribe(profile => {
      this.credit.set(profile.body.scenario_credit)
    })
  }

  getList() {
    this.master.scenarioList().subscribe({
      next: data => {
        this.data = data;
        this.changeDetectorRef.detectChanges();

        this.master.feedbackList().subscribe({
          next: feedbackData => {
            // با توجه به پاسخ شما، اگر دیتا مستقیماً در بدنه است یا در feedbackData.body
            this.resData = feedbackData.body || feedbackData;
            this.changeDetectorRef.detectChanges();
          }
        });
      }
    });
  }

  getFeedbackCode(scenarioCode: string): string | null {
    if (!this.resData) return null;

    // فیلتر کردن فیدبک‌های مربوط به این سناریو که با موفقیت تولید شده‌اند
    const feedbacks = this.resData.filter(
      (f: any) =>
        f.scenario_tracking_code === scenarioCode &&
        f.generated === true
    );

    if (!feedbacks.length) return null;

    // بازگرداندن اولین فیدبک (اولین تلاش) به جای آخرین
    return feedbacks[0].tracking_code;
  }

  getFirstScore(scenarioCode: string): string | number {
    if (!this.resData) return '—';

    const feedbacks = this.resData.filter(
      (f: any) => f.scenario_tracking_code === scenarioCode && f.generated === true
    );

    // اگر فیدبکی پیدا شد، نمره اولین تلاش را برگردان، در غیر این صورت نمره پیش‌فرض سناریو
    return feedbacks.length > 0 ? feedbacks[0].score : '—';
  }

  createScenrio() {
    // this.master.pulmonologyScenarioCreate().subscribe({
    //   next: data => {
    //
    //   },
    //   complete: () => {
    //     setTimeout(() => {
    //       window.location.reload();
    //     }, 3000)
    //     this.toastService.showSuccess('سناریوی درخواستی در صف تولید قرار گرفت. پس از حدود 30 ثانیه، صفحه را رفرش کرده و سناریو را مشاهده کنید')
    //
    //   }
    // })
    this.toastService.showWarn('جهت پذیرش بیمار، از صفحه کلاس اقدام نمایید')
  }


  formatDate(dateStr: string): string {
    if (!dateStr) return '—';

    const date = new Date(dateStr);
    return new Intl.DateTimeFormat('fa-IR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  }

}
