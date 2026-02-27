import {ChangeDetectorRef, Component, signal} from '@angular/core';
import {DashNav} from '../../../../../shared/components/dash-nav/dash-nav';
import {ClassesCard} from '../../s-dashboard/classes/classes-card/classes-card';
import {Master} from '../../../../../core/services/master';


@Component({
  selector: 'app-class',
  imports: [
    DashNav,
    ClassesCard
  ],
  templateUrl: './class.html',
  styleUrl: './class.css'
})
export class Class {

  isLoading = signal(false)
  classes: any = []

  constructor(public master: Master, public changeDetectorRef: ChangeDetectorRef) {
  }

  ngOnInit() {
    this.master.sections().subscribe({
      next: data => {
        this.classes = data.body;
      },
      error: err => {
        console.log(err);
      },
      complete: () => {
        this.changeDetectorRef.detectChanges();
      }
    })

  }
}
