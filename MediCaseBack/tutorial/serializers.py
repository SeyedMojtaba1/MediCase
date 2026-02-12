from rest_framework import serializers
from .models import Tutorial, TutorialPage

class TutorialPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialPage
        fields = ['page_id', 'tutorial', 'title', 'content', 'order', 'created_at']
        read_only_fields = ['page_id', 'created_at']

class TutorialSerializer(serializers.ModelSerializer):
    total_pages = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tutorial
        fields = ['tutorial_id', 'title', 'description', 'total_pages']
        read_only_fields = ['tutorial_id']

    def get_total_pages(self, obj):
        return obj.pages.count()