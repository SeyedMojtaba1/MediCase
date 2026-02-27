import {ChangeDetectorRef, Component} from '@angular/core';
import {ActivatedRoute, RouterLink} from '@angular/router';
import {Master} from '../../../../../core/services/master';
import {DashNavT} from '../../../../../shared/components/dash-nav-t/dash-nav-t';
import {TableModule} from 'primeng/table';
import {APP_CONFIG} from '../../../../../config/app.config';
import {forkJoin, switchMap} from 'rxjs';
import {Card} from '../../../../../layouts/card/card';

@Component({
  selector: 'app-section-page-s',
  imports: [
    DashNavT,
    TableModule,
    RouterLink,
    Card
  ],
  templateUrl: './section-page-s.html',
  styleUrl: './section-page-s.css'
})
export class SectionPageS {

  section = ''
  section_detail: any
  members: any
  teacher = ''

  visible = false
  isModalOpen = false
  protected readonly APP_CONFIG = APP_CONFIG;
  protected readonly RouterLink = RouterLink;

  constructor(public route: ActivatedRoute, public master: Master, public changeDetectorRef: ChangeDetectorRef) {
  }

  ngOnInit() {
    this.section = this.route.snapshot.paramMap.get('id')!;

    this.master.sectionRetrieve(this.section).pipe(
      switchMap((sectionRes: any) => {
        this.section_detail = sectionRes.body;

        return forkJoin({
          members: this.master.memberSectionList(this.section),
          teacher: this.master.user(this.section_detail.teacher)
        });
      })
    ).subscribe({
      next: ({members, teacher}) => {
        this.members = members.body;
        this.teacher = "دکتر " + teacher.body.first_name + " " + teacher.body.last_name;
      },
      error: err => console.log(err),
      complete: () => this.changeDetectorRef.detectChanges()
    });
  }

  addStudentClick() {
    this.visible = true
  }
}
