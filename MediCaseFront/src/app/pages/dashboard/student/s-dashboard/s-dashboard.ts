import {Component} from '@angular/core';
import {Classes} from './classes/classes';
import {Action} from '../../../../shared/components/button/action/action';

@Component({
  selector: 'app-s-dashboard',
  imports: [
    Classes,
    Action
  ],
  templateUrl: './s-dashboard.html',
  styleUrl: './s-dashboard.css'
})
export class SDashboard {

}
