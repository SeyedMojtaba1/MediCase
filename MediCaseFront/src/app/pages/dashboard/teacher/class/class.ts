import {ChangeDetectorRef, Component, signal} from '@angular/core';
import {DashNavT} from '../../../../shared/components/dash-nav-t/dash-nav-t';
import {Master} from '../../../../core/services/master';
import {ClassesCard} from '../../student/s-dashboard/classes/classes-card/classes-card';
import {Addsection} from './addsection/addsection';

@Component({
  selector: 'app-class',
  imports: [
    DashNavT,
    ClassesCard,
    Addsection,
  ],
  templateUrl: './class.html',
  styleUrl: './class.css'
})
export class Classs {

  isLoading = signal(false)
  isModalOpen = false;
  classes: any = []
  visible = false

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
