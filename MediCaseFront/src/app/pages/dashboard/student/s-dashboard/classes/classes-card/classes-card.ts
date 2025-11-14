import {ChangeDetectorRef, Component, Input} from '@angular/core';
import {RouterLink} from '@angular/router';
import {APP_CONFIG} from '../../../../../../config/app.config';
import {Master} from '../../../../../../core/services/master';

@Component({
  selector: 'app-classes-card',
  imports: [
    RouterLink
  ],
  templateUrl: './classes-card.html',
  styleUrl: './classes-card.css'
})
export class ClassesCard {
  @Input() clas: any;
  baseurl = APP_CONFIG.baseURL;
  teacher = ''
  protected readonly localStorage = localStorage;

  constructor(public master: Master, public changeDetectorRef: ChangeDetectorRef) {
  }

  ngOnInit() {
    this.master.user(this.clas.teacher).subscribe({
      next: (data) => {
        this.teacher = " دکتر " + data.body.first_name + ' ' + data.body.last_name;
      },
      error: (err) => {
        console.log(err);
      },
      complete: () => {
        this.changeDetectorRef.detectChanges();
      }
    })
  }
}
