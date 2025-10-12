import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class Auth {

  private role: 'student' | 'teacher' | null = null;

  constructor(private router: Router) {
    const savedRole = localStorage.getItem('role');
    if (savedRole === 'student' || savedRole === 'teacher') {
      this.role = savedRole;
    }
  }

  loginAsStudent() {
    this.role = 'student';
    localStorage.setItem('role', 'student');
    this.router.navigate(['/dashboard/s']);
  }

  loginAsTeacher() {
    this.role = 'teacher';
    localStorage.setItem('role', 'teacher');
    this.router.navigate(['/dashboard/t']);
  }

  logout() {
    this.role = null;
    localStorage.removeItem('role');
    this.router.navigate(['/login']);
  }

  // گرفتن نقش فعلی کاربر
  getRole() {
    return this.role;
  }

  // بررسی اینکه کاربر وارد شده یا نه
  isLoggedIn() {
    return this.role !== null;
  }
}
