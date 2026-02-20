import {ChangeDetectorRef, Component} from '@angular/core';
import {DashNav} from '../../shared/components/dash-nav/dash-nav';
import {Master} from '../../core/services/master';
import {RouterLink} from '@angular/router';

@Component({
  selector: 'app-blog',
  imports: [
    DashNav,
    RouterLink,


  ],
  templateUrl: './blog.html',
  styleUrl: './blog.css'
})
export class Blog {


  subjects: any[] = []
  list: any = []

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


            this.changeDetectorRef.detectChanges();
          }
        })
      },
      error: err => {
      },
    })
  }


}
