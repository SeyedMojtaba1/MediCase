from rest_framework import serializers
from .models import Tutorial, Comment
import logging

logger = logging.getLogger('registery')

class TutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields = ('id', 'title', 'description', 'published')

    def validate(self, attrs):
        """
        این متد برای لاگ کردن داده‌های ورودی قبل از اعتبارسنجی نهایی است.
        """
        try:
            # اینجا می‌توانید قوانین اعتبارسنجی خاص خود را چک کنید
            # فعلاً فقط لاگ می‌کنیم که داده‌ها دریافت شده‌اند
            # logger.debug(f"Validating Tutorial data: {attrs}")
            return super().validate(attrs)
        except serializers.ValidationError as e:
            logger.warning(f"Validation failed for Tutorial: {e.detail}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error during Tutorial validation: {str(e)}")
            raise e

    def create(self, validated_data):
        try:
            instance = super().create(validated_data)
            logger.info(f"New Tutorial created successfully with ID: {instance.id} | Title: {instance.title}")
            return instance
        except Exception as e:
            logger.error(f"Failed to create Tutorial. Error: {str(e)} | Data: {validated_data}")
            raise e

    def update(self, instance, validated_data):
        try:
            instance = super().update(instance, validated_data)
            logger.info(f"Tutorial updated successfully. ID: {instance.id}")
            return instance
        except Exception as e:
            logger.error(f"Failed to update Tutorial {instance.id}. Error: {str(e)}")
            raise e


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'tutorial', 'text', 'created_at') # فیلد 'tutorial' باید باشد تا فارن‌کی مشخص شود

    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except serializers.ValidationError as e:
            logger.warning(f"Validation failed for Comment: {e.detail}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error during Comment validation: {str(e)}")
            raise e

    def create(self, validated_data):
        try:
            instance = super().create(validated_data)
            # لاگ کردن اینکه برای کدام آموزش کامنت گذاشته شده
            tutorial_id = instance.tutorial.id if instance.tutorial else 'Unknown'
            logger.info(f"New Comment created for Tutorial {tutorial_id}. Comment ID: {instance.id}")
            return instance
        except Exception as e:
            logger.error(f"Failed to create Comment. Error: {str(e)}")
            raise e
