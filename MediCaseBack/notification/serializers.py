from rest_framework import serializers
from .models import Announcement
from classroom.models import Section
from university.models import University

class SystemAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'created_at', 'author']
        read_only_fields = ['author', 'created_at']

class UniversityAnnouncementSerializer(serializers.ModelSerializer):
    # این فیلد را دستی تعریف میکنیم تا بتوانیم required=False بدهیم 
    # (چون ادمین دانشگاه نیازی به فرستادن آن ندارد، اتوماتیک پر میشود)
    target_university = serializers.PrimaryKeyRelatedField(
        queryset=University.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'created_at', 'author', 'target_university']
        read_only_fields = ['author', 'created_at']

class SectionAnnouncementSerializer(serializers.ModelSerializer):
    target_section = serializers.PrimaryKeyRelatedField(
        queryset=Section.objects.all(),
        required=True
    )

    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'created_at', 'author', 'target_section']
        read_only_fields = ['author', 'created_at']