import {Component} from '@angular/core';
import {RouterLink, RouterLinkActive} from '@angular/router';

@Component({
  selector: 'app-t-side-bar',
  imports: [
    RouterLinkActive,
    RouterLink
  ],
  templateUrl: './t-side-bar.html',
  styleUrl: './t-side-bar.css'
})
export class TSideBar {

  menu = [
    {
      name: 'داشبورد', image: 'images/svg/dashboard.svg', link: '/dashboard/t', exact: true,
    },
    {
      name: 'کلاس', image: 'images/svg/book-shelf-line.svg', link: '/dashboard/t/class', exact: false,
    },
    // {
    //   name: 'بیمارستان', image: 'images/svg/hospital.svg', link: '/dashboard/s/hospital', exact: false
    // },
    {
      name: 'پایگاه دانش', image: 'images/svg/sutdents.svg', link: '/blog', exact: false
    },
    {
      name: 'حساب کاربری', image: 'images/svg/profile.svg', link: '/dashboard/t/profile', exact: false
    },
    {
      name: 'گزارش عملکرد', image: 'images/svg/stat.svg', link: '/dashboard/t/stat', exact: false
    }
  ]
}
