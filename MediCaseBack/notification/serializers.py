from rest_framework import serializers
from .models import Announcement
from classroom.models import Section
from university.models import University

class SystemAnnouncementSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'created_at', 'author']
        read_only_fields = ['author', 'created_at']

class UniversityAnnouncementSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
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
    author = serializers.ReadOnlyField(source='author.username')
    section_id = serializers.PrimaryKeyRelatedField(
        queryset=Section.objects.all(),
        source='target_section', 
        required=True,
        write_only=True
    )

    target_section_id = serializers.UUIDField(source='target_section.section_id', read_only=True)

    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'created_at', 'author', 'section_id', 'target_section_id']
        read_only_fields = ['author', 'created_at', 'target_section_id']