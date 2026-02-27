import {ChangeDetectorRef, Component} from '@angular/core';
import {DashNav} from '../../../../shared/components/dash-nav/dash-nav';
import {PersonalInfo} from './personal-info/personal-info';
import {EductionInfo} from './eduction-info/eduction-info';
import {Master} from '../../../../core/services/master';
import {SetProfileImage} from '../../../../shared/components/set-profile-image/set-profile-image';


@Component({
  selector: 'app-profile',
  imports: [
    DashNav,
    PersonalInfo,
    EductionInfo,
    SetProfileImage
  ],
  templateUrl: './profile.html',
  styleUrl: './profile.css'
})
export class Profile {


  isModalOpen = false
  visible = false;

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
