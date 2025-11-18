import {ChangeDetectorRef, Component} from '@angular/core';
import {Router, RouterOutlet} from '@angular/router';
import {APP_CONFIG} from '../../config/app.config';
import {TSideBar} from '../../shared/components/t-side-bar/t-side-bar';
import {SSideBar} from '../../shared/components/s-side-bar/s-side-bar';

@Component({
  selector: 'app-dashboard-layout',
  imports: [
    RouterOutlet,
    TSideBar,
    SSideBar,
  ],
  templateUrl: './dashboard-layout.html',
  styleUrl: './dashboard-layout.css'
})
export class DashboardLayout {

  isStudent = false;
  isTeacher = false;
  protected readonly APP_CONFIG = APP_CONFIG;

  constructor(private router: Router, public changeDetector: ChangeDetectorRef,) {
    this.router.events.subscribe(() => {
      const url = this.router.url;
      // this.isStudent = url.includes('/dashboard/s');
      // this.isTeacher = url.includes('/dashboard/t');
      this.isStudent = localStorage.getItem('role') == 'student'
      this.isTeacher = localStorage.getItem('role') == 'teacher'
      this.changeDetector.detectChanges();
    });
  }

  ngOnInit() {
    this.changeDetector.detectChanges();
  }
}
