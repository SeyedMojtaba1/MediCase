import {Component} from '@angular/core';
import {APP_CONFIG} from '../../../config/app.config';
import {RouterLink, RouterLinkActive} from '@angular/router';

@Component({
  selector: 'app-s-side-bar',
  imports: [
    RouterLinkActive,
    RouterLink
  ],
  templateUrl: './s-side-bar.html',
  styleUrl: './s-side-bar.css'
})
export class SSideBar {

  menu = [
    {
      name: 'داشبورد', image: 'images/svg/dashboard.svg', link: '/dashboard/s', exact: true,
    },
    {
      name: 'کلاس', image: 'images/svg/book-shelf-line.svg', link: '/dashboard/s/class', exact: false,
    },
    // {
    //   name: 'بیمارستان', image: 'images/svg/hospital.svg', link: '/dashboard/s/hospital', exact: false
    // },
    {
      name: 'پایگاه دانش', image: 'images/svg/sutdents.svg', link: '/dashboard/s/blog', exact: false
    },
    {
      name: 'حساب کاربری', image: 'images/svg/profile.svg', link: '/dashboard/s/profile', exact: false
    },
    {
      name: 'گزارش عملکرد', image: 'images/svg/stat.svg', link: '/dashboard/s/stat', exact: false
    }
  ]
  protected readonly APP_CONFIG = APP_CONFIG;
}
