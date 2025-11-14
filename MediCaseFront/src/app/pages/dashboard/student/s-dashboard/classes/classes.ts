import {ChangeDetectorRef, Component} from '@angular/core';
import {ClassesCard} from './classes-card/classes-card';
import {Card} from '../../../../../layouts/card/card';
import {Master} from '../../../../../core/services/master';
import {RouterLink} from '@angular/router';

@Component({
  selector: 'app-classes',
  imports: [
    ClassesCard,
    Card,
    RouterLink
  ],
  templateUrl: './classes.html',
  styleUrl: './classes.css'
})
export class Classes {
  list: any = []
  protected readonly localStorage = localStorage;

  constructor(public changeDetector: ChangeDetectorRef, public master: Master) {
  }

  ngOnInit(): void {
    this.master.sections().subscribe({
      next: data => {
        this.list = data.body;
        this.list = this.list.slice(0, 3)
      },
      error: err => {
        console.log(err);
      },
      complete: () => {
        this.changeDetector.detectChanges();
      }
    })
  }
}
