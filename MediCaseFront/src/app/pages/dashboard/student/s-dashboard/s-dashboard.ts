import {Component} from '@angular/core';
import {Classes} from './classes/classes';
import {Action} from '../../../../shared/components/button/action/action';
import {DashNav} from '../../../../shared/components/dash-nav/dash-nav';
import {Top} from '../../../../shared/components/top/top';
import {HospitalCard} from './hospital-card/hospital-card';
import {Chart} from './chart/chart';

@Component({
  selector: 'app-s-dashboard',
  imports: [
    Classes,
    Action,
    DashNav,
    Top,
    HospitalCard,
    Chart
  ],
  templateUrl: './s-dashboard.html',
  styleUrl: './s-dashboard.css'
})
export class SDashboard {

}
