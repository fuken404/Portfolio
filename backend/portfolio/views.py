from django.db.models import Prefetch
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .i18n import current_lang
from .models import Certification, Education, Experience, Profile, Project, Skill
from .serializers import (
    CertificationSerializer,
    ContactMessageSerializer,
    EducationSerializer,
    ExperienceSerializer,
    ProfileSerializer,
    ProjectSerializer,
    SkillSerializer,
)

# El idioma de cada respuesta lo decide LocaleMiddleware a partir del
# encabezado Accept-Language (es | en).


def projects_queryset():
    """Proyectos con sus tecnologías en el orden de la sección Stack."""
    return Project.objects.prefetch_related(
        Prefetch('skills', queryset=Skill.objects.order_by('order', 'name_es'))
    )


@api_view(['GET'])
def health(request):
    """Sonda de salud para Container Apps: no toca la base de datos."""
    return Response({'status': 'ok'})


@api_view(['GET'])
def profile(request):
    obj = Profile.objects.first()
    if obj is None:
        return Response({'detail': 'Perfil no configurado.'}, status=404)
    return Response(ProfileSerializer(obj).data)


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.filter(show_in_stack=True)
    serializer_class = SkillSerializer
    pagination_class = None


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """Proyectos. `?skill=<slug>` filtra por tecnología, ej. /api/projects/?skill=react"""

    serializer_class = ProjectSerializer
    lookup_field = 'slug'
    pagination_class = None

    def get_queryset(self):
        qs = projects_queryset()
        skill = self.request.query_params.get('skill')
        if skill:
            qs = qs.filter(skills__slug=skill)
        return qs


class ExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    pagination_class = None


class EducationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    pagination_class = None


class CertificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    pagination_class = None


class ContactCreateView(generics.CreateAPIView):
    serializer_class = ContactMessageSerializer
    # Endpoint público: sin sesión, así que no aplica CSRF.
    authentication_classes = []

    def perform_create(self, serializer):
        serializer.save(lang=current_lang())
