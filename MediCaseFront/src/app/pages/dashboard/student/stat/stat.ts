import {ChangeDetectorRef, Component} from '@angular/core';
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
  protected readonly console = console;

  constructor(public master: Master, public changeDetectorRef: ChangeDetectorRef, public toastService: ToastService) {
  }

  ngOnInit() {


    this.master.scenarioList().subscribe({
      next: data => {
        console.log(data);
        this.data = data
        this.changeDetectorRef.detectChanges();
      }
    })
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
}
