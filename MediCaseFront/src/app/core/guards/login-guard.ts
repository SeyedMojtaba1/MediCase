import {Injectable} from '@angular/core';
import {CanActivate, Router, UrlTree} from '@angular/router';
import {Auth} from './auth';

@Injectable({
  providedIn: 'root'
})
export class LoginGuard implements CanActivate {

  constructor(private auth: Auth, private router: Router) {
  }

  canActivate(): boolean | UrlTree {
    // اگر کاربر لاگین کرده باشد، به داشبورد هدایت شود
    if (this.auth.isLoggedIn()) {
      const role = this.auth.getRole();
      if (role === 'student') {
        return this.router.createUrlTree(['/dashboard/s']);
      } else if (role === 'teacher') {
        return this.router.createUrlTree(['/dashboard/t']);
      }
    }

    // اگر لاگین نکرده باشد، اجازه دسترسی به صفحه لاگین را دارد
    return true;
  }
}
