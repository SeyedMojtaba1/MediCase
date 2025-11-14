import {Routes} from '@angular/router';
import {DashboardLayout} from './layouts/dashboard-layout/dashboard-layout';
import {SDashboard} from './pages/dashboard/student/s-dashboard/s-dashboard';
import {TDashboard} from './pages/dashboard/teacher/t-dashboard/t-dashboard';
import {Hospital} from './pages/dashboard/student/hospital/hospital';
import {Profile} from './pages/dashboard/student/profile/profile';
import {Stat} from './pages/dashboard/student/stat/stat';
import {AuthGuard} from './core/guards/auth-guard';
import {RoleGuard} from './core/guards/role-guard';
import {Login} from './pages/auth/login/login';
import {Changepass} from './pages/auth/changepass/changepass';
import {Forget} from './pages/auth/forget/forget';
import {LoginGuard} from './core/guards/login-guard';
import {SubjectIntro} from './pages/dashboard/student/hospital/subject-intro/subject-intro';
import {Select} from './pages/dashboard/student/hospital/select/select';
import {PProfile} from './pages/dashboard/teacher/profile/profile';
import {Statt} from './pages/dashboard/teacher/stat/stat';
import {SectionPageT} from './pages/dashboard/teacher/class/section-page-t/section-page-t';
import {Classs} from './pages/dashboard/teacher/class/class';
import {Class} from './pages/dashboard/student/class/class/class';
import {NotFound404} from './pages/auth/not-found404/not-found404';
import {PublicProfile} from './shared/public-profile/public-profile';
import {SectionPageS} from './pages/dashboard/student/class/section-page-s/section-page-s';

export const routes: Routes = [

  //پروفایل - صفحات عمومی
  {
    path: 'user', component: DashboardLayout, children: [
      {path: '', component: NotFound404},
      {path: ':id', component: PublicProfile, children: []}
    ]
  },

  // داشبورد دانشجو
  {
    path: 'dashboard/s',
    component: DashboardLayout,
    canActivate: [AuthGuard, RoleGuard],
    data: {role: 'student'},
    children: [
      {path: '', component: SDashboard},
      {
        path: 'hospital', children: [
          {path: '', component: Hospital},
          {path: 'intro/:subject', component: SubjectIntro},
          {path: 'select/:sub', component: Select},
        ]
      },
      {
        path: 'class', children: [
          {path: '', component: Class},
          {path: ':id', component: SectionPageS},
        ]
      }, {path: 'profile', component: Profile},
      {path: 'stat', component: Stat},

    ]
  },

  // داشبورد استاد
  {
    path: 'dashboard/t',
    component: DashboardLayout,
    canActivate: [AuthGuard, RoleGuard],
    data: {role: 'teacher'},
    children: [
      {path: '', component: TDashboard},
      {path: 'profile', component: PProfile},
      {path: 'stat', component: Statt},
      {
        path: 'class', children: [
          {path: '', component: Classs},
          {path: ':id', component: SectionPageT},
        ]
      },
    ]
  },

  // مسیرهای عمومی با Guard برای صفحه لاگین
  {
    path: 'login',
    component: Login,
    canActivate: [LoginGuard]
  },
  {path: 'changepass', component: Changepass},
  {path: 'forget', component: Forget},
  {path: 'dashboard', redirectTo: 'dashboard/s', pathMatch: 'full'},
  {path: '', redirectTo: 'dashboard/s', pathMatch: 'full'},
  // {path: '**', redirectTo: '404'},
  // {path: '404', component: NotFound404},
];
