import {ChangeDetectorRef, Component} from '@angular/core';
import {Master} from '../../../core/services/master';

@Component({
  selector: 'app-scenario-intro',
  imports: [],
  templateUrl: './scenario-intro.html',
  styleUrl: './scenario-intro.css'
})
export class ScenarioIntro {

  feedback: any

  constructor(public master: Master, public changeDetectorRef: ChangeDetectorRef) {
  }

  ngOnInit() {
    this.master.pulmonologyScenarioFeedbackRetrieve('BP3NOKL8YF').subscribe(
      {
        next: (data) => {
          console.log(data);
          this.feedback = data;
          this.changeDetectorRef.detectChanges();

        },
        error: (data) => {
          console.log(data);
        },
      }
    )
  }


}
