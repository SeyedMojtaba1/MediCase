from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from django.db.models import Q

from .models import Announcement
from .serializers import (
    SystemAnnouncementSerializer, 
    UniversityAnnouncementSerializer, 
    SectionAnnouncementSerializer
)
from .permissions import IsSuperAdminRole, IsUniversityAdminRole, IsSectionStaffRole, is_super_admin
from classroom.models import Section, StudentSection
from classroom.utils import decode_short_uuid

class ShortUUIDLookupMixin:
    lookup_field = 'notification_id'

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        short_id = self.kwargs.get(lookup_url_kwarg)

        try:
            uuid_id = decode_short_uuid(short_id)
        except ValueError:
            raise NotFound("شناسه اعلان نامعتبر است.")

        self.kwargs[lookup_url_kwarg] = uuid_id
        
        return super().get_object()


class SystemAnnouncementViewSet(ShortUUIDLookupMixin, viewsets.ModelViewSet):
    serializer_class = SystemAnnouncementSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsSuperAdminRole()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return Announcement.objects.filter(scope='SYSTEM').order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, scope='SYSTEM')


class UniversityAnnouncementViewSet(ShortUUIDLookupMixin, viewsets.ModelViewSet):
    serializer_class = UniversityAnnouncementSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsUniversityAdminRole()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if is_super_admin(user):
            return Announcement.objects.filter(scope='UNIVERSITY').order_by('-created_at')
        if user.university:
            return Announcement.objects.filter(
                scope='UNIVERSITY', 
                target_university=user.university
            ).order_by('-created_at')
        return Announcement.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if not user.university:
             raise PermissionDenied("You must be assigned to a university to post university announcements.")
        
        serializer.save(
            author=user, 
            scope='UNIVERSITY', 
            target_university=user.university
        )


class SectionAnnouncementViewSet(ShortUUIDLookupMixin, viewsets.ModelViewSet):
    serializer_class = SectionAnnouncementSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsSectionStaffRole()]

    def get_queryset(self):
        user = self.request.user
        
        if is_super_admin(user):
            return Announcement.objects.filter(scope='SECTION').order_by('-created_at')

        teacher_sections = Section.objects.filter(teacher=user)
        student_sections_ids = StudentSection.objects.filter(
            student=user, 
            student_status='Active'
        ).values_list('section', flat=True)
        
        admin_university_query = Q()
        if user.main_role and user.main_role.name == 'Admin' and user.university:
             admin_university_query = Q(target_section__teacher__university=user.university)

        return Announcement.objects.filter(
            scope='SECTION'
        ).filter(
            Q(target_section__in=teacher_sections) | 
            Q(target_section__id__in=student_sections_ids) |
            admin_university_query
        ).distinct().order_by('-created_at')

    def perform_create(self, serializer):
        user = self.request.user
        section = serializer.validated_data['target_section']
        
        if is_super_admin(user):
            serializer.save(author=user, scope='SECTION')
            return

        is_owner_teacher = (section.teacher == user)
        is_uni_admin = False
        if user.main_role and user.main_role.name == 'Admin' and user.university:
            if section.teacher and section.teacher.university == user.university:
                is_uni_admin = True
        
        if not (is_owner_teacher or is_uni_admin):
            from classroom.utils import encode_short_uuid
            short_id = encode_short_uuid(section.section_id)
            raise PermissionDenied(f"You do not have permission to post in section {short_id}.")
            
        serializer.save(author=user, scope='SECTION')