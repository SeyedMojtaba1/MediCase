import {ChangeDetectorRef, Component} from '@angular/core';
import {ActivatedRoute, RouterLink} from '@angular/router';
import {DashNav} from '../../../../../shared/components/dash-nav/dash-nav';
import {Master} from '../../../../../core/services/master';
import {Card} from '../../../../../layouts/card/card';
import {Tag} from 'primeng/tag';


interface HospitalSubjectData {
  subject: string;
  hospital: string;
  access_status: boolean;
}

@Component({
  selector: 'app-select',
  imports: [
    DashNav,
    Card,
    Tag,
    RouterLink
  ],
  templateUrl: './select.html',
  styleUrl: './select.css'
})
export class Select {

  subject = ''
  data: any

  constructor(public route: ActivatedRoute, public changeDetector: ChangeDetectorRef, public master: Master) {
  }

  ngOnInit() {
    this.subject = this.route.snapshot.paramMap.get('sub')!;
    this.master.hospitalSubject(this.subject).subscribe(
      {
        next: data => {
          this.data = data
        },
        error: error => {

        },
        complete: () => {
          this.changeDetector.detectChanges();
        }
      }
    )
  }
}
