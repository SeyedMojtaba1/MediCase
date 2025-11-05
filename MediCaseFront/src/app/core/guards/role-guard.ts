import {Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, CanActivate, Router, UrlTree} from '@angular/router';
import {Auth} from './auth';

@Injectable({
  providedIn: 'root'
})
export class RoleGuard implements CanActivate {

  constructor(private auth: Auth, private router: Router) {
  }

  canActivate(route: ActivatedRouteSnapshot): boolean | UrlTree {
    const role = this.auth.getRole();
    const expectedRole = route.data['role'] as 'student' | 'teacher';

    if (role !== expectedRole) {
      // اگر نقش مطابقت ندارد، کاربر را به داشبورد مربوط به نقشش هدایت کن
      if (role === 'student') {
        return this.router.createUrlTree(['/dashboard/s']);
      } else if (role === 'teacher') {
        return this.router.createUrlTree(['/dashboard/t']);
      } else {
        return this.router.createUrlTree(['/login']);
      }
    }

    return true;
  }
}
