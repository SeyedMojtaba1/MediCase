import {Component, Input, signal} from '@angular/core';
import {Popover} from 'primeng/popover';
import {Master} from '../../../core/services/master';
import {Auth} from '../../../core/guards/auth';
import {RouterLink} from '@angular/router';

@Component({
  selector: 'app-dash-nav-t',
  imports: [
    Popover,
    RouterLink
  ],
  templateUrl: './dash-nav-t.html',
  styleUrl: './dash-nav-t.css'
})
export class DashNavT {
  @Input() title: string = ''
  @Input() welcome = true
  @Input() welcomeMsg: string = ''

  first_name = signal('')
  last_name = signal('')
  avatar = 'images/jpg/avatar.jpg';

  alarms = [
    {
      date: '124/12/12',
      icon: 'images/svg/hospital.svg',
      url: "/sdaf",
      title: 'خطای ورود',
      description: 'این خطا برای مشکلات از پیش تعیین نشده است. پس حواست باشه که یه موقع مشکلی پیش نیاد برات و این داستانان'
    },
    {
      date: '124/12/12',
      icon: 'images/svg/hospital.svg',
      url: "/sdaf",
      title: 'خطای ورود',
      description: 'این خطا برای مشکلات از پیش تعیین نشده است. پس حواست باشه که یه موقع مشکلی پیش نیاد برات و این داستانان'
    }
  ]

  constructor(public master: Master, public auth: Auth) {
  }


  ngOnInit() {
    document.getElementById('head')?.scrollIntoView();

    const first = sessionStorage.getItem('first_name');
    const last = sessionStorage.getItem('last_name');
    const avatar = sessionStorage.getItem('avatar');

    if (first && last) {
      this.first_name.set(first);
      this.last_name.set(last);
      this.avatar = (avatar && avatar !== 'null' && avatar !== '')
        ? avatar
        : 'images/jpg/avatar.jpg';
    } else {
      this.loadProfile();
    }
  }

  loadProfile() {
    this.master.profile().subscribe({
      next: data => {
        const user = data.body;
        if (user) {
          sessionStorage.setItem('first_name', user.first_name || '');
          sessionStorage.setItem('last_name', user.last_name || '');
          sessionStorage.setItem('avatar', user.profile_image ?? '');

          this.first_name.set(user.first_name || '');
          this.last_name.set(user.last_name || '');
          this.avatar = user.profile_image
            ? user.profile_image
            : 'images/jpg/avatar.jpg';
        }
      },
      error: err => {
        console.log(err);
      }
    });
  }


  logout() {
    this.master.logout().subscribe(
      {
        next: (res) => {
          this.auth.logout();
        },
        error: (err) => {
          console.log(err);
        }
      }
    )
  }
}
