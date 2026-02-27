import { Injectable } from '@angular/core';
import { CanActivate, Router, UrlTree } from '@angular/router';
import { Auth} from './auth';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private auth: Auth, private router: Router) {}

  canActivate(): boolean | UrlTree {
    const role = this.auth.getRole();

    // اگه وارد نشده
    if (!this.auth.isLoggedIn()) {
      return this.router.createUrlTree(['/login']);
    }

    // اگه نقش مشخص نیست
    if (!role) {
      return this.router.createUrlTree(['/login']);
    }

    return true;
  }
}
