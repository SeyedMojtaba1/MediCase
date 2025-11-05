import {Component, Input} from '@angular/core';
import {RouterLink} from '@angular/router';

@Component({
  selector: 'app-action',
  imports: [
    RouterLink
  ],
  templateUrl: './action.html',
  styleUrl: './action.css'
})
export class Action {

  @Input() text!: string;
  @Input() url!: string;
  @Input() icon!: string;
}
