import {ChangeDetectorRef, Component} from '@angular/core';
import {Master} from '../../../../core/services/master';
import {DashNav} from '../../../../shared/components/dash-nav/dash-nav';
import {EductionInfo} from '../../student/profile/eduction-info/eduction-info';
import {PersonalInfo} from '../../student/profile/personal-info/personal-info';
import {EductionInfoT} from '../../student/profile/eduction-info-t/eduction-info-t';

@Component({
  selector: 'app-profile',
  imports: [
    DashNav,
    EductionInfo,
    PersonalInfo,
    EductionInfoT
  ],
  templateUrl: './profile.html',
  styleUrl: './profile.css'
})
export class PProfile {


  user: any = {
    first_name: '',
    last_name: '',
    major: 'پزشکی',
    role: '',
    university: 'علوم پزشکی اصفهان',
    profile: '',
    phone: '',
    email: '',
    national_code: '',
  }

  constructor(public master: Master, public changeDetector: ChangeDetectorRef) {
  }

  ngOnInit() {
    this.master.profile().subscribe({
      next: data => {
        this.user = {
          first_name: data.body.first_name,
          last_name: data.body.last_name,
          major: 'پزشکی',
          role: data.body.main_role,
          university: 'علوم پزشکی اصفهان',
          profile: data.body.profile_image,
          phone: data.body.phone_number,
          email: data.body.email,
          national_code: '',
          username: data.body.username,
        };
      },
      complete: () => {
        this.changeDetector.detectChanges();
      }
    });
  }
}
