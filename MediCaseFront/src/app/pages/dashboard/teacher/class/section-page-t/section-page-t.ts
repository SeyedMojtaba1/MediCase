import {ChangeDetectorRef, Component} from '@angular/core';
import {ActivatedRoute, RouterLink} from '@angular/router';
import {Master} from '../../../../../core/services/master';
import {DashNavT} from '../../../../../shared/components/dash-nav-t/dash-nav-t';
import {TableModule} from 'primeng/table';
import {AddStudent} from './add-student/add-student';
import {APP_CONFIG} from '../../../../../config/app.config';
import {forkJoin, switchMap} from 'rxjs';
import {EditSection} from './edit-section/edit-section';
import {Card} from '../../../../../layouts/card/card';

@Component({
  selector: 'app-section-page-t',
  imports: [
    DashNavT,
    TableModule,
    AddStudent,
    RouterLink,
    EditSection,
    Card
  ],
  templateUrl: './section-page-t.html',
  styleUrl: './section-page-t.css'
})
export class SectionPageT {

  section = ''
  section_detail: any
  members: any
  teacher = ''

  visible = false
  isModalOpen = false

  edit_isModalOpen = false
  edit_visible = false
  protected readonly APP_CONFIG = APP_CONFIG;

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
