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
  protected readonly console = console;

  constructor(public master: Master, public changeDetectorRef: ChangeDetectorRef, public toastService: ToastService) {
  }


  ngOnInit() {
    this.getList()
    this.getCredit()
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

    const feedbacks = this.resData.filter(
      (f: any) =>
        f.scenario_tracking_code === scenarioCode &&
        f.generated === true
    );

    if (!feedbacks.length) return null;

    return feedbacks[feedbacks.length - 1].tracking_code;
  }

  createScenrio() {
    this.master.pulmonologyScenarioCreate().subscribe({
      next: data => {

      },
      complete: () => {
        setTimeout(() => {
          window.location.reload();
        }, 3000)
        this.toastService.showSuccess('سناریوی درخواستی در صف تولید قرار گرفت. پس از حدود 30 ثانیه، صفحه را رفرش کرده و سناریو را مشاهده کنید')

      }
    })
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
