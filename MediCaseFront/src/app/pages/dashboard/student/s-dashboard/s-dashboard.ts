import {Component} from '@angular/core';
import {Classes} from './classes/classes';
import {DashNav} from '../../../../shared/components/dash-nav/dash-nav';
import {Top} from '../../../../shared/components/top/top';
import {HospitalCard} from './hospital-card/hospital-card';
import {Chart} from './chart/chart';

@Component({
  selector: 'app-s-dashboard',
  imports: [
    Classes,
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
