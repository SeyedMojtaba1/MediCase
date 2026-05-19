import {ChangeDetectorRef, Component} from '@angular/core';
import {Master} from '../../../../core/services/master';
import {DashNav} from '../../../../shared/components/dash-nav/dash-nav';
import {PersonalInfo} from '../../student/profile/personal-info/personal-info';
import {EductionInfoT} from '../../student/profile/eduction-info-t/eduction-info-t';
import {SetProfileImage} from '../../../../shared/components/set-profile-image/set-profile-image';

@Component({
  selector: 'app-profile',
  imports: [
    DashNav,
    PersonalInfo,
    EductionInfoT,
    SetProfileImage
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
    phone_number: '',
    email: '',
    national_code: '',
  }

  isModalOpen = false
  visible = false;

  constructor(public master: Master, public changeDetector: ChangeDetectorRef) {
  }

  ngOnInit() {
    this.master.profile().subscribe({
      next: data => {
        this.user = {
          first_name: data.body.first_name,
          last_name: data.body.last_name,
          major: data.body.major,
          role: data.body.main_role,
          university: 'علوم پزشکی اصفهان',
          profile: data.body.profile_image,
          personal_number: data.body.personal_number,
          phone: data.body.phone_number,
          email: data.body.email,
          national_code: '',
          username: data.body.username,
          scenario_credit: data.body.scenario_credit
        };
      },
      complete: () => {
        this.changeDetector.detectChanges();
      }
    });
  }
}
