import {Component} from '@angular/core';
import {Action} from '../../../../shared/components/button/action/action';
import {Top} from '../../../../shared/components/top/top';
import {Classes} from '../../student/s-dashboard/classes/classes';
import {DashNavT} from '../../../../shared/components/dash-nav-t/dash-nav-t';

@Component({
  selector: 'app-t-dashboard',
  imports: [
    Action,
    Top,
    Classes,
    DashNavT
  ],
  templateUrl: './t-dashboard.html',
  styleUrl: './t-dashboard.css'
})
export class TDashboard {


}
