from rest_framework import serializers
from .models import Tutorial, TutorialPage

class TutorialPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialPage
        fields = ['id', 'tutorial', 'title', 'content', 'page_number']

class TutorialSerializer(serializers.ModelSerializer):
    total_pages = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tutorial
        fields = ['id', 'title', 'description', 'total_pages']

    def get_total_pages(self, obj):
        return obj.pages.count()