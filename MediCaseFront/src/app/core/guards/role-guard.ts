import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, Router, UrlTree } from '@angular/router';
import { Auth} from './auth';

@Injectable({
  providedIn: 'root'
})
export class RoleGuard implements CanActivate {

  constructor(private auth: Auth, private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot): boolean | UrlTree {
    const role = this.auth.getRole();
    const expectedRole = route.data['role'] as 'student' | 'teacher';

    // اگه نقش درست نبود → بفرست لاگین
    if (role !== expectedRole) {
      return this.router.createUrlTree(['/login']);
    }

    return true;
  }
}
