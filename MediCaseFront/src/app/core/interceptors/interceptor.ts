import {HttpErrorResponse, HttpInterceptorFn} from '@angular/common/http';
import {throwError} from 'rxjs';
import {catchError} from 'rxjs/operators';
import {ToastService} from '../services/toast';
import {inject} from '@angular/core';
import {Router} from '@angular/router';
import {Auth} from '../guards/auth';
import {Master} from '../services/master';

export const ErrorInterceptor: HttpInterceptorFn = (req, next) => {
  const toast = inject(ToastService);
  const router = inject(Router);
  const auth = inject(Auth);
  const master = inject(Master);

  const excludedApis = [
    '/token/refresh',
  ];

  const isExcluded = excludedApis.some(api => req.url.includes(api));

  if (isExcluded) {
    return next(req);
  }


  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 0) {
        toast.showError('سرور در دسترس نیست');
      } else if (error.status === 401) {
        master.refresh().subscribe({
          next: err => {
            localStorage.setItem('access_token', err.body.access);
          },
          error: err => {
            toast.showError('نشست شما منقضی شده است')
            auth.logout();
          }
        })
        router.navigateByUrl('/login');

      } else if (error.status === 404) {
        alert(' داده مورد نظر یافت نشد.');
      } else if (error.status >= 500) {
        alert(' خطای سرور رخ داده است.');
      }

      return throwError(() => error);
    })
  );
};
