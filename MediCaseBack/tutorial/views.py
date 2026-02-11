from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Tutorial, TutorialPage
from .serializers import TutorialSerializer, TutorialPageSerializer
from .permissions import IsAdminOrAuthenticatedReadOnly

class TutorialViewSet(viewsets.ModelViewSet):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    permission_classes = [IsAdminOrAuthenticatedReadOnly]

    @action(detail=True, methods=['get'])
    def page(self, request, pk=None):
        tutorial = self.get_object()
        page_number = request.query_params.get('number', 1)
        
        page = get_object_or_404(TutorialPage, tutorial=tutorial, page_number=page_number)
        serializer = TutorialPageSerializer(page)
        
        has_next = TutorialPage.objects.filter(tutorial=tutorial, page_number=int(page_number) + 1).exists()
        has_prev = int(page_number) > 1

        return Response({
            'tutorial_title': tutorial.title,
            'page_data': serializer.data,
            'has_next': has_next,
            'has_prev': has_prev,
            'total_pages': tutorial.pages.count()
        })


class TutorialPageViewSet(viewsets.ModelViewSet):
    queryset = TutorialPage.objects.all()
    serializer_class = TutorialPageSerializer
    permission_classes = [IsAdminOrAuthenticatedReadOnly]