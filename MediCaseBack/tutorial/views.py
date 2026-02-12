from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Tutorial
from .serializers import TutorialSerializer
from .utils import decode_short_uuid

from .models import Tutorial, TutorialPage
from .serializers import TutorialSerializer, TutorialPageSerializer
from .permissions import IsAdminOrAuthenticatedReadOnly

class TutorialViewSet(viewsets.ModelViewSet):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    lookup_field = 'tutorial_id'

    def get_object(self):
        short_id = self.kwargs.get(self.lookup_field)

        try:
            tutorial_uuid = decode_short_uuid(short_id)
        except ValueError:
            tutorial_uuid = None

        obj = get_object_or_404(self.get_queryset(), tutorial_id=tutorial_uuid)
        
        self.check_object_permissions(self.request, obj)
        
        return obj

    def retrieve(self, request, *args, **kwargs):
        short_id = self.kwargs.get(self.lookup_field)
        try:
            uuid_obj = decode_short_uuid(short_id)
        except ValueError:
            return Response({"message": "شناسه آموزشی (ID) نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        short_id = self.kwargs.get(self.lookup_field)
        try:
            uuid_obj = decode_short_uuid(short_id)
        except ValueError:
            return Response({"message": "شناسه آموزشی (ID) نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)


class TutorialPageViewSet(viewsets.ModelViewSet):
    queryset = TutorialPage.objects.all()
    serializer_class = TutorialPageSerializer
    lookup_field = 'page_id'

    def get_queryset(self):
        queryset = super().get_queryset()
        tutorial_short_id = self.request.query_params.get('tutorial_id')
        
        if tutorial_short_id:
            try:
                tutorial_uuid = decode_short_uuid(tutorial_short_id)
                queryset = queryset.filter(tutorial__tutorial_id=tutorial_uuid)
            except ValueError:
                return queryset.none()
                
        return queryset

    def get_object(self):
        short_id = self.kwargs.get(self.lookup_field)

        try:
            page_uuid = decode_short_uuid(short_id)
        except ValueError:
            import uuid
            page_uuid = uuid.uuid4() 

        obj = get_object_or_404(self.get_queryset(), page_id=page_uuid)
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        short_id = self.kwargs.get(self.lookup_field)
        try:
            decode_short_uuid(short_id)
        except ValueError:
            return Response({"message": "شناسه صفحه (Page ID) نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        short_id = self.kwargs.get(self.lookup_field)
        try:
            decode_short_uuid(short_id)
        except ValueError:
            return Response({"message": "شناسه صفحه (Page ID) نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)