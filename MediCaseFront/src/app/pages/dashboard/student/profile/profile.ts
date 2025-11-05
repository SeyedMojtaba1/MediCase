import {Component, signal} from '@angular/core';
import {DashNav} from '../../../../shared/components/dash-nav/dash-nav';
import {PersonalInfo} from './personal-info/personal-info';
import {EductionInfo} from './eduction-info/eduction-info';
import {Master} from '../../../../core/services/master';

@Component({
  selector: 'app-profile',
  imports: [
    DashNav,
    PersonalInfo,
    EductionInfo
  ],
  templateUrl: './profile.html',
  styleUrl: './profile.css'
})
export class Profile {

  user: any;
  first_name = signal('');
  last_name = signal('');
  major = signal('پزشکی');
  role = 'دانشجو'
  university = signal('علوم پزشکی اصفهان')

  constructor(public master: Master) {
  }

  ngOnInit() {
    this.master.profile().subscribe({
      next: data => {
        this.first_name.set(data.body.first_name);
        this.last_name.set(data.body.last_name);
      },
      error: err => {
      }
    })
  }
}
