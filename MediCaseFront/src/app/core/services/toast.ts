import {inject, Injectable} from '@angular/core';
import {MessageService} from 'primeng/api';

@Injectable({
  providedIn: 'root'
})
export class ToastService {
  private messageService = inject(MessageService);

  // نمایش پیام موفقیت
  showSuccess(message: string, title: string = 'موفقیت') {
    this.messageService.add({
      severity: 'success',
      summary: title,
      detail: message,
      life: 3000,
      
    });
  }

  // نمایش پیام خطا
  showError(message: string, title: string = 'خطا') {
    this.messageService.add({
      severity: 'error',
      summary: title,
      detail: message,
      life: 3000
    });
  }

  // نمایش پیام هشدار
  showWarn(message: string, title: string = 'هشدار') {
    this.messageService.add({
      severity: 'warn',
      summary: title,
      detail: message,
      life: 3000
    });
  }

  // نمایش پیام اطلاعات
  showInfo(message: string, title: string = 'اطلاعات') {
    this.messageService.add({
      severity: 'info',
      summary: title,
      detail: message,
      life: 3000
    });
  }

  // پاک کردن همه پیام‌ها
  clear() {
    this.messageService.clear();
  }
}
