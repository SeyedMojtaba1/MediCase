import {Injectable} from '@angular/core';
import {Router} from '@angular/router';
import {ToastService} from '../services/toast';

@Injectable({
  providedIn: 'root'
})
export class Auth {

  private role: 'student' | 'teacher' | null = null;

  constructor(private router: Router, public toast: ToastService) {
    this.loadRoleFromStorage();
  }

  // متد برای لاگین با نقش دریافتی از API
  login(role: 'student' | 'teacher', access_token: string, refresh_token: string) {
    this.role = role;
    localStorage.setItem('role', role);
    localStorage.setItem('access_token', access_token);

    //********************************************
    localStorage.setItem('refresh_token', refresh_token);
    //********************************************

    // هدایت به داشبورد مناسب
    if (role === 'student') {
      this.router.navigateByUrl('/dashboard/s');
    } else {
      this.router.navigateByUrl('/dashboard/t');
    }
  }


  logout() {
    this.role = null;
    this.toast.showSuccess('با موفقیت از حساب خود خارج شدید')
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('role');
    this.router.navigateByUrl('/login');
  }

  getRole() {
    return this.role;
  }

  isLoggedIn() {
    return this.role !== null;
  }

  private loadRoleFromStorage() {
    const savedRole = localStorage.getItem('role');
    if (savedRole === 'student' || savedRole === 'teacher') {
      this.role = savedRole;
    }
  }
}
