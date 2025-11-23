import {HttpErrorResponse, HttpInterceptorFn} from '@angular/common/http';
import {switchMap, throwError} from 'rxjs';
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

  // رفرش توکن نباید دوباره رفرش شود
  if (req.url.includes('/token/refresh')) {
    return next(req);
  }

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {

      if (error.status === 401) {
        // تلاش برای گرفتن توکن جدید
        return master.refresh().pipe(
          switchMap((res: any) => {
            // توکن جدید
            localStorage.setItem('access_token', res.body.access);

            // درخواست اصلی را با توکن جدید تکرار کن
            const newReq = req.clone({
              setHeaders: {
                Authorization: `Bearer ${res.body.access}`
              }
            });
            return next(newReq);
          }),
          catchError(err => {
            toast.showError('نشست شما منقضی شده است');
            auth.logout();
            router.navigateByUrl('/login');
            return throwError(() => err);
          })
        );
      }

      return throwError(() => error);
    })
  );
};
