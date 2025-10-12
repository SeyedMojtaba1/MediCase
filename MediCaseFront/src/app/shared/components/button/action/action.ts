import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-action',
  imports: [],
  templateUrl: './action.html',
  styleUrl: './action.css'
})
export class Action {

  @Input() text!: string;
  @Input() url!: string;
  @Input() icon!: string;
}
