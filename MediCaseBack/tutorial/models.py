from django.db import models

class Tutorial(models.Model):
    """
    مدل اصلی درسنامه (مثلا: پنومونی)
    """
    title = models.CharField(max_length=255, verbose_name="عنوان درسنامه")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات کلی")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "درسنامه"
        verbose_name_plural = "درسنامه‌ها"

    def __str__(self):
        return self.title


class TutorialPage(models.Model):
    """
    مدل صفحات درسنامه (مثلا: فیزیوپاتولوژی، پاتولوژی و ...)
    """
    tutorial = models.ForeignKey(
        Tutorial, 
        on_delete=models.CASCADE, 
        related_name='pages', 
        verbose_name="درسنامه مربوطه"
    )
    title = models.CharField(max_length=255, verbose_name="عنوان صفحه (زیرعنوان)")
    content = models.TextField(verbose_name="محتوای صفحه")
    page_number = models.PositiveIntegerField(verbose_name="شماره صفحه / ترتیب")

    class Meta:
        verbose_name = "صفحه درسنامه"
        verbose_name_plural = "صفحات درسنامه"
        # مرتب‌سازی پیش‌فرض بر اساس شماره صفحه
        ordering = ['page_number']
        # جلوگیری از ثبت دو صفحه با یک شماره برای یک درسنامه
        unique_together = ('tutorial', 'page_number') 

    def __str__(self):
        return f"{self.tutorial.title} - {self.title} (صفحه {self.page_number})"