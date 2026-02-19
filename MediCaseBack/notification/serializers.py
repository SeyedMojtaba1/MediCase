from rest_framework import serializers
from .models import Announcement
from classroom.models import Section
from university.models import University
from classroom.utils import encode_short_uuid, decode_short_uuid

class SystemAnnouncementSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    notification_id = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = ['notification_id', 'title', 'content', 'created_at', 'author']
        read_only_fields = ['author', 'created_at', 'notification_id']

    def get_notification_id(self, obj):
        return encode_short_uuid(obj.notification_id)

class UniversityAnnouncementSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    target_university = serializers.CharField(source='target_university.english_name', read_only=True)
    notification_id = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = ['notification_id', 'title', 'content', 'created_at', 'author', 'target_university']
        read_only_fields = ['author', 'created_at', 'target_university', 'notification_id']

    def get_notification_id(self, obj):
        return encode_short_uuid(obj.notification_id)

class SectionAnnouncementSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    notification_id = serializers.SerializerMethodField()
    section_id = serializers.CharField(write_only=True, required=True)
    target_section_id = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = ['notification_id', 'title', 'content', 'created_at', 'author', 'section_id', 'target_section_id']
        read_only_fields = ['author', 'created_at', 'target_section_id', 'notification_id']

    def get_notification_id(self, obj):
        return encode_short_uuid(obj.notification_id)

    def get_target_section_id(self, obj):
        if obj.target_section:
            return encode_short_uuid(obj.target_section.section_id)
        return None

    def validate_section_id(self, value):
        try:
            uuid_obj = decode_short_uuid(value)
            section = Section.objects.get(section_id=uuid_obj)
            return section
        except (ValueError, Section.DoesNotExist):
            raise serializers.ValidationError("شناسه کلاس نامعتبر است یا یافت نشد.")

    def create(self, validated_data):
        section_obj = validated_data.pop('section_id')
        validated_data['target_section'] = section_obj
        return super().create(validated_data)