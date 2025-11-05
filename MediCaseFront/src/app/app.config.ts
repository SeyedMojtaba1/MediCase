import {ApplicationConfig, provideBrowserGlobalErrorListeners, provideZonelessChangeDetection,} from '@angular/core';
import {provideRouter} from '@angular/router';
import {providePrimeNG} from 'primeng/config';
import Aura from '@primeuix/themes/aura';
import {routes} from './app.routes';
import {provideHttpClient, withInterceptors} from '@angular/common/http';
import {HashLocationStrategy, LocationStrategy} from '@angular/common';
import {provideAnimations} from '@angular/platform-browser/animations';
import {provideAnimationsAsync} from '@angular/platform-browser/animations/async';
import {MessageService} from 'primeng/api';
import {ErrorInterceptor} from './core/interceptors/interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withInterceptors([ErrorInterceptor]) // ✅ اینجا مهمه!
    ),
    MessageService,
    provideBrowserGlobalErrorListeners(),
    {provide: LocationStrategy, useClass: HashLocationStrategy},
    provideZonelessChangeDetection(),
    provideRouter(routes),
    provideAnimationsAsync(),
    providePrimeNG({
      theme: {
        preset: Aura,
        options: {darkModeSelector: false},
      },
    }),
    provideAnimations(),
  ],
};
