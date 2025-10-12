import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-classes-card',
  imports: [],
  templateUrl: './classes-card.html',
  styleUrl: './classes-card.css'
})
export class ClassesCard {
  @Input() clas: any;
}
