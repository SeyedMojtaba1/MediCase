import {ChangeDetectorRef, Component} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {DashNav} from '../../../../../shared/components/dash-nav/dash-nav';
import {Master} from '../../../../../core/services/master';


@Component({
  selector: 'app-select',
  imports: [
    DashNav
  ],
  templateUrl: './select.html',
  styleUrl: './select.css'
})
export class Select {

  subject = ''

  constructor(public route: ActivatedRoute, public changeDetector: ChangeDetectorRef, public master: Master) {
  }

  ngOnInit() {
    this.subject = this.route.snapshot.paramMap.get('sub')!;
    this.master.selectHospital(this.subject).subscribe({
      next: data => {
        console.log(data);
      },
      error: err => {

      },
      complete: () => {
        this.changeDetector.detectChanges();
        this.master.pulmonologyScenarioRetrieve('RTXKR8W7ZK').subscribe({
          next: data => {
            console.log(data);
          }
        })
      }
    })
  }


}
