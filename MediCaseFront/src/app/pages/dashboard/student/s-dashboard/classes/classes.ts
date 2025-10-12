import {ChangeDetectorRef, Component} from '@angular/core';
import {ClassesCard} from './classes-card/classes-card';

@Component({
  selector: 'app-classes',
  imports: [
    ClassesCard
  ],
  templateUrl: './classes.html',
  styleUrl: './classes.css'
})
export class Classes {
  list = [
    {name: 'درس ریه گروه 2', image: 'images/jpg/rie.jpg'},
    {name: 'ریه', image: 'images/jpg/rie.jpg'},
    {name: 'درس ریه این متن باید طولانی باشه', image: 'images/jpg/rie.jpg'},
    {name: 'asd', image: 'images/jpg/rie.jpg'},
    {name: 'asd', image: 'images/jpg/rie.jpg'},
  ]

  constructor(public changeDetector: ChangeDetectorRef) {
  }

  ngOnInit(): void {
    this.list = this.list.slice(0, 3)
    this.changeDetector.detectChanges()
  }
}
