import {ChangeDetectorRef, Component} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {Master} from '../../../../../core/services/master';
import {DashNav} from '../../../../../shared/components/dash-nav/dash-nav';
import {Chart} from '../../s-dashboard/chart/chart';
import {Top} from '../../../../../shared/components/top/top';
import {Action} from '../../../../../shared/components/button/action/action';
import {NgClass} from '@angular/common';

@Component({
  selector: 'app-subject-intro',
  imports: [
    DashNav,
    Chart,
    Top,
    Action,
    NgClass,
  ],
  templateUrl: './subject-intro.html',
  styleUrl: './subject-intro.css'
})
export class SubjectIntro {

  subject = ''
  data: any = [];
  isActive = false

  constructor(public route: ActivatedRoute, public master: Master, public changeDetectorRef: ChangeDetectorRef) {
  }

  ngOnInit() {
    this.subject = this.route.snapshot.paramMap.get('subject')!;
    this.master.subjectDetail(this.subject).subscribe({
      next: (data: any) => {
        this.data = data.body;
      },
      error: error => {
        console.log(error);
      },
      complete: () => {
        this.changeDetectorRef.detectChanges();
        this.master.studentSubjectList().subscribe({
          next: (data: any) => {
            this.isActive = data.body.some((x: any) =>
              x.subject === this.subject && x.access_status === true
            );
          },
          error: error => {

          },
          complete: () => {
            this.changeDetectorRef.detectChanges();
          }
        })
      }
    })

  }

}
