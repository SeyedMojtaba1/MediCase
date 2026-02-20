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
  list = []

  constructor(public master: Master, public changeDetectorRef: ChangeDetectorRef) {
  }

  ngOnInit() {
    this.master.subjectList().subscribe({
      next: data => {
        this.subjects = data.body;
        this.master.studentSubjectList().subscribe({
          next: data => {
            this.list = data.body;
          },
          error: err => {

          },
          complete: () => {
            this.subjects.sort((a, b) => {
              const aAccess = this.hasAccess(a);
              const bAccess = this.hasAccess(b);

              // دسترسی‌دارها اول
              if (aAccess && !bAccess) return -1;
              if (!aAccess && bAccess) return 1;

              return 0;
            });

            this.changeDetectorRef.detectChanges();
          }
        })
      },
      error: err => {
      },
    })
  }


  hasAccess(sub: any) {
    return this.list.some(
      (x: any) => x.english_name === sub.english_name && x.access_status
    );
  }
}
